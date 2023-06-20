from django.shortcuts import render
from .models import Employee
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")


def task_list(request):
    return render(request, "task_list.html")


@login_required(login_url="login")
def employee_list(request):
    return render(request, "employee_list.html")


@login_required
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


# ============================================================================ #


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("employee_list")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("employee_list")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
