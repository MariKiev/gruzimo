from django.db import models


class Location (models.Model):
    """Locations business model"""
    CITY_CHOICES = (
        ('KYIV', 'Киев'),
    )

    CITY = {'KYIV': 'Киев'}

    city = models.CharField(max_length=5, choices=CITY_CHOICES, default='KYIV')

    def __str__(self):
        return Location.CITY.get(self.city)
