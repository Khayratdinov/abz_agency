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
    employee_level = models.PositiveIntegerField()

    def __str__(self):
        return self.full_name

    def get_position_display(self):
        return f"{self.position} ({self.full_name})"
