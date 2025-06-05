from django.db import models

from .order import Order


class Discount(models.Model):
    name = models.CharField(max_length=255)
    percent = models.DecimalField(max_digits=5, decimal_places=2)  # от 0 до 100
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Tax(models.Model):
    name = models.CharField(max_length=255)
    percent = models.DecimalField(max_digits=5, decimal_places=2)  # от 0 до 100
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.percent}%)"
