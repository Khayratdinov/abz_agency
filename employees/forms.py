from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = (
            "full_name",
            "position",
            "hire_date",
            "salary",
            "manager",
            "employee_level",
        )
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "hire_date": forms.DateInput(attrs={"class": "form-control"}),
            "salary": forms.NumberInput(attrs={"class": "form-control"}),
            "manager": forms.Select(attrs={"class": "form-control"}),
            "employee_level": forms.Select(attrs={"class": "form-control"}),
        }
