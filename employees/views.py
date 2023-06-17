from django.shortcuts import render
from .models import Employee
from django.http import JsonResponse
from django.db.models import Q


def index(request):
    return render(request, "index.html")


def employee_list(request):
    return render(request, "employee_list.html")


def employee_list_ajax(request):
    print(request.GET)
    sort_field = request.GET.get("sort", "full_name")
    search_query = request.GET.get("search", "")

    employees = Employee.objects.filter(
        Q(full_name__icontains=search_query)
        | Q(position__icontains=search_query)
        | Q(salary__icontains=search_query)
    ).order_by(sort_field)

    data = []
    for employee in employees:
        data.append(
            {
                "full_name": employee.full_name,
                "position": employee.position,
                "hire_date": employee.hire_date.strftime("%Y-%m-%d"),
                "salary": str(employee.salary),
            }
        )

    return JsonResponse({"employees": data})
