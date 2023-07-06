from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.


class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    manager = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )
    employee_level = models.PositiveIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    image = models.ImageField(upload_to="employee_images/")
    low_image = models.ImageField(upload_to="employee_images/", blank=True)

    def __str__(self):
        return self.full_name

    def get_position_display(self):
        return f"{self.position} ({self.full_name})"

    def get_edit_url(self):
        return reverse("update_employee", args=[self.id])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            # Открываем изображение с использованием Pillow
            img = Image.open(self.image.path)

            # Снижаем качество изображения
            output_io = BytesIO()
            #  image size 200x200
            img.thumbnail(
                (
                    200,
                    200,
                ),
                # Image.ANTIALIAS,
            )

            img.save(
                output_io,
                format="JPEG",
                quality=50,
            )  # Установите нужное значение качества (от 1 до 100)

            # Сохраняем измененное изображение в поле low_image
            self.low_image.save(
                f"low_{self.image.name}",
                content=ContentFile(output_io.getvalue()),
                save=False,
            )
            output_io.close()

        super().save(*args, **kwargs)
