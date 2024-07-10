# employees/management/commands/process_payroll.py
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from employees.models import Payroll
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Process payroll at the end of the month'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='The date to process payroll for (format: YYYY-MM-DD)')
        parser.add_argument('--bypass-date-check', action='store_true', help='Bypass the date check for testing purposes')

    def handle(self, *args, **kwargs):
        date_str = kwargs['date']
        bypass_date_check = kwargs['bypass_date_check']

        # Get the date to process
        if date_str:
            try:
                today = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid date format. Use YYYY-MM-DD.'))
                return
        else:
            today = timezone.localdate()  # Get the current date in local timezone

        # Check if it's the last day of the month unless bypassing the date check
        if not bypass_date_check:
            first_day_of_next_month = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
            last_day_of_current_month = first_day_of_next_month - timedelta(days=1)

            if today != last_day_of_current_month:
                self.stdout.write(self.style.WARNING(f"Payroll processing is only available on the last day of the month. Today is {today}."))
                return

        # Process payroll for the current month
        first_day_of_current_month = today.replace(day=1)
        last_day_of_current_month = (first_day_of_current_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        month = today.strftime('%B %Y')

        # Debug: Print dates for verification
        print(f"Today: {today}")
        print(f"First day of current month: {first_day_of_current_month}")
        print(f"Last day of current month: {last_day_of_current_month}")

        # Process payroll for each employee
        payrolls = Payroll.objects.filter(month__year=first_day_of_current_month.year, month__month=first_day_of_current_month.month, payment_status='pending')

        # Debug: Print the payroll records to be processed
        print(f"Payroll records to be processed: {list(payrolls)}")

        if not payrolls:
            self.stdout.write(self.style.WARNING(f"No payroll records found for {month}."))
            return
        
        # Debug: Print the number of payrolls to be processed
        print(f"Number of payrolls to process: {payrolls.count()}")
        
        for payroll in payrolls:
            # Update payment status and date
            payroll.payment_status = 'paid'
            payroll.payment_date = today
            payroll.save()

            # Send email to employee
            send_mail(
                'Your Monthly Payroll Details',
                f'Dear {payroll.employee.name},\n\nYour payroll for {month} has been processed.\n'
                f'Total Salary: {payroll.total_salary}\n'
                f'Deductions: {payroll.deduction_amount}\n'
                f'Net Salary: {payroll.net_salary}\n'
                f'Payment Date: {payroll.payment_date}\n\n'
                'Thank you.',
                'from@example.com',
                [payroll.employee.user.email],
                fail_silently=False,
            )

        self.stdout.write(self.style.SUCCESS('Successfully processed payroll for the month.'))
