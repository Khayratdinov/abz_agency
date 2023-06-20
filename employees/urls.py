from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("employee_list/", views.employee_list, name="employee_list"),
    path("employee_list_ajax/", views.employee_list_ajax, name="employee_list_ajax"),
    path("task_list/", views.task_list, name="task_list"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
