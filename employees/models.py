from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from PIL import Image
import os

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

    @property
    def get_position_display(self):
        return f"{self.position} ({self.full_name})"

    def get_edit_url(self):
        return reverse("update_employee", args=[self.id])


def create_low_image(sender, instance, **kwargs):
    if instance.image:
        image = Image.open(instance.image.path)
        low_image_size = (100, 100)
        image.thumbnail(low_image_size, Image.LANCZOS)
        low_image_path = instance.image.path.replace(".jpg", "_low.jpg")
        image.save(low_image_path)
        instance.low_image.name = low_image_path.replace("employee_images/", "")
        Employee.objects.filter(id=instance.id).update(low_image=instance.low_image)


models.signals.post_save.connect(create_low_image, sender=Employee)
