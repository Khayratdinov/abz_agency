from django.db import models

# Create your models here.


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    employee_level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.full_name
