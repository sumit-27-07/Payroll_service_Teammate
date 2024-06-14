from django.db import models
from django.contrib.auth.models import User

class HR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    hr_id = models.CharField(max_length=10, unique=True)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=10, unique=True)
    hr = models.ForeignKey(HR, on_delete=models.SET_NULL, null=True)
    contact = models.CharField(max_length=15)
    status = models.CharField(max_length=10, default='inactive')
    job_type = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, default='pending')

    def __str__(self):
        return f"{self.employee.name} - {self.status}"
