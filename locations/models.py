from django.db import models


class Location (models.Model):
    """Locations business model"""
    CITY_CHOICES = (
        ('KYIV', 'Киев'),
    )

    city = models.CharField(max_length=5, choices=CITY_CHOICES, default='KYIV')

