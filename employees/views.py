from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

# ============================================================================ #

from .models import Employee
from .forms import EmployeeForm

# ============================================================================ #


def index(request):
    return render(request, "index.html")


def task_list(request):
    return render(request, "task_list.html")


def test(request):
    emplote_list = Employee.objects.all()

    return render(request, "test.html", {"emplote_list": emplote_list})


@login_required(login_url="login")
def employee_list(request):
    employees_for_create = Employee.objects.all()

    return render(
        request, "employee_list.html", {"employees_for_create": employees_for_create}
    )


@login_required
def employee_list_ajax(request):
    sort_field = request.GET.get("sort", "full_name")
    search_query = request.GET.get("search", "")

    employees = Employee.objects.filter(
        Q(full_name__icontains=search_query)
        | Q(position__icontains=search_query)
        | Q(salary__icontains=search_query)
    ).order_by(sort_field)

    # Paginate the results
    page_number = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 2)
    paginator = Paginator(employees, page_size)
    page = paginator.get_page(page_number)

    data = []
    for employee in page:
        data.append(
            {
                "pk": employee.id,
                "full_name": employee.full_name,
                "position": employee.position,
                "hire_date": employee.hire_date.strftime("%Y-%m-%d"),
                "salary": str(employee.salary),
                "low_image": employee.low_image.url if employee.low_image else "",
            }
        )

    # Add pagination metadata to the response
    return JsonResponse(
        {
            "employees": data,
            "page_number": page_number,
            "page_size": page_size,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
        }
    )


@login_required
def get_employee_data(request):
    employee_id = request.GET.get("employee_id")
    employee = get_object_or_404(Employee, id=employee_id)

    # Prepare the employee data to be sent back as JSON
    employee_data = {
        "employee_id": employee_id,
        "full_name": employee.full_name,
        "position": employee.position,
        "hire_date": employee.hire_date,
        "salary": employee.salary,
    }

    return JsonResponse({"employee": employee_data})


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


# ============================================================================ #


@login_required
def employee_detail_ajax(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return JsonResponse(
        {
            "employee": {
                "pk": employee.pk,
                "full_name": employee.full_name,
                "position": employee.position,
                "hire_date": employee.hire_date.strftime("%Y-%m-%d"),
                "salary": employee.salary,
                "image": employee.image.url if employee.image else None,
                "employee_level": employee.employee_level,
            }
        }
    )


@login_required
@csrf_exempt
def employee_update_ajax(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        employee.full_name = request.POST.get("full_name", employee.full_name)
        employee.position = request.POST.get("position", employee.position)
        employee.hire_date = request.POST.get("hire_date", employee.hire_date)
        employee.salary = request.POST.get("salary", employee.salary)
        employee.employee_level = request.POST.get(
            "employee_level", employee.employee_level
        )
        employee.image = request.FILES.get("image", employee.image)
        employee.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@login_required
@csrf_exempt
def employee_delete_ajax(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        employee.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@csrf_exempt
def save_employee_ajax(request):
    print("This hello 1", request.POST)
    form = EmployeeForm(request.POST or None, request.FILES)

    print(form.errors)

    if form.is_valid():
        # if request.FILES.get("image"):
        #     form.instance.image = request.FILES.get("image")
        form.save()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False, "error": form.errors})


def autocomplete(request):
    if "term" in request.GET:
        term = request.GET.get("term")
        languages = Employee.objects.all().filter(full_name__icontains=term)
        return JsonResponse(list(languages.values()), safe=False)
    return render(request, "employee_list.html")
