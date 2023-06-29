from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("employee_list/", views.employee_list, name="employee_list"),
    path("employee_list_ajax/", views.employee_list_ajax, name="employee_list_ajax"),
    path("get_employee_data/", views.get_employee_data, name="get_employee_data"),
    path("task_list/", views.task_list, name="task_list"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # path("employee/create/", views.create_employee, name="create_employee"),
    path(
        "employee_delete_ajax/<int:employee_id>/",
        views.employee_delete_ajax,
        name="employee_delete_ajax",
    ),
    path(
        "employee_update_ajax/<int:employee_id>/",
        views.employee_update_ajax,
        name="employee_update_ajax",
    ),
    path(
        "employee_detail_ajax/<int:employee_id>/",
        views.employee_detail_ajax,
        name="employee_detail_ajax",
    ),
    path("create_employee/", views.create_employee, name="create_employee"),
    path("save-employee-ajax/", views.save_employee_ajax, name="save_employee_ajax"),
    path("autocomplete/", views.autocomplete, name="autocomplete"),

    path('test/', views.test, name='test'),
]
