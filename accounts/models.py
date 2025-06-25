from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):
    EMPLOYEE = 'Employee'
    MANAGER = 'Manager'


    ROLE_CHOICES = [
        (EMPLOYEE, 'Employee'),
        (MANAGER, 'Manager'),
    ]

    email = models.EmailField(max_length=100, unique=True)
    image = models.ImageField(upload_to='user_photo/', default='def.png', blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=EMPLOYEE)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'  # or 'email' if you want
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
