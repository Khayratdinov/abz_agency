import random

# ============================================================================ #
from faker import Faker

# ============================================================================ #
from django.core.management.base import BaseCommand

# ============================================================================ #
from employees.models import Employee

fake = Faker()


class Command(BaseCommand):
    help = "Заполните базу данных случайными данными для модели Employee."

    def add_arguments(self, parser):
        parser.add_argument(
            "total",
            type=int,
            help="Указывает количество сотрудников, которые будут созданы",
        )

    def handle(self, *args, **options):
        total = options["total"]
        for _ in range(total):
            Employee.objects.create(
                full_name=fake.name(),
                position=fake.job(),
                hire_date=fake.date_between(start_date="-5y", end_date="today"),
                salary=fake.pydecimal(
                    left_digits=5, right_digits=2, min_value=500, positive=True
                ),
                manager=None,
                employee_level=random.randint(1, 5),
            )

        employees = Employee.objects.all()
        for employee in employees:
            if random.random() < 0.9:  # 90% шанс иметь менеджера
                employee.manager = random.choice(employees)
                employee.save()

        self.stdout.write(self.style.SUCCESS(f"Успешно создано {total} сотрудников"))
