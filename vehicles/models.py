from django.db import models

# class VehicleType (models.Model):
#     """Vehicle business model"""
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     type =


class Vehicle(models.Model):
    """Vehicle business model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    volume = models.FloatField()  # куб. м.
    weight = models.FloatField()  # тонн
    type = models.CharField(max_length=100)  # for example Фура
