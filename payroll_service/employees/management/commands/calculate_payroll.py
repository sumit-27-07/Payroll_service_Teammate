# employees/management/commands/calculate_payroll.py

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from employees.models import Employee, Leave
from django.db.models import ExpressionWrapper, F, DurationField, Sum

class Command(BaseCommand):
    help = 'Calculate payroll for the current month'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_current_month = (first_day_of_current_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        month = first_day_of_current_month.strftime('%B %Y')

        # Calculate payroll for each employee
        employees = Employee.objects.all()
        for employee in employees:
            # Calculate total leave days for the current month
            total_leave_days = Leave.objects.filter(
                employee=employee,
                status='Approved',
                start_date__gte=first_day_of_current_month,
                end_date__lte=last_day_of_current_month
            ).annotate(
                duration=ExpressionWrapper(
                    F('end_date') - F('start_date') + timedelta(days=1),
                    output_field=DurationField()
                )
            ).aggregate(total_days=Sum('duration'))

            leave_days = total_leave_days['total_days'].days if total_leave_days['total_days'] else 0

            # Call the calculate_payroll method from LeaveManager
            payroll = Leave.objects.calculate_payroll(employee, leave_days)
            if payroll:
                self.stdout.write(self.style.SUCCESS(f'Successfully calculated payroll for {employee.user.username} for {month}'))
            else:
                self.stdout.write(self.style.WARNING(f'No payroll record created for {employee.user.username} for {month}'))
