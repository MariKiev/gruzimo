
from django.db import models

from accounts.models import User
from locations.models import Location
from vehicles.models import Vehicle


class Order (models.Model):
    """Order business model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    from_address = models.CharField(max_length=1024)
    to_address = models.CharField(max_length=1024)
    city = models.ForeignKey(Location, default=1)
    order_date = models.DateTimeField()
    user = models.ForeignKey(User)
    vehicle = models.ForeignKey(Vehicle)
