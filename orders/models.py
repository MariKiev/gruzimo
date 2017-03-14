
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from accounts.models import User
from locations.models import Location
from vehicles.models import Vehicle


class Order (models.Model):
    """Order business model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    from_address = models.CharField(max_length=1024)
    from_house = models.CharField(max_length=20)
    from_entrance = models.IntegerField(null=True)
    to_address = models.CharField(max_length=1024)
    to_house = models.CharField(max_length=20)
    city = models.ForeignKey(Location, default=1)
    order_date = models.DateTimeField()
    user = models.ForeignKey(User, null=True)
    vehicle = models.ForeignKey(Vehicle, null=True)
    phone = PhoneNumberField()
    name = models.CharField(max_length=30)
    length = models.IntegerField()  # in centimeter
    width = models.IntegerField()  # in centimeter
    height = models.IntegerField()  # in centimeter
    info = models.CharField(max_length=1024)
    order_cost = models.IntegerField(null=True)

    def __str__(self):
        return 'Создан: {}, Адрес подачи: {}, Дом: {}, Подъезд: {}, Адрес доставки: {}, Дом: {}, Когда ехать: {},' \
               'имя: {}, Телефон: {}, Длина, м: {}, Ширина, м: {}, Высота, м: {}, Груз: {}, Стоимость: {}'.format(
                self.created, self.from_address, self.from_house, self.from_entrance, self.to_address,
                self.to_house, self.order_date, self.name, self.phone, self.length, self.width, self.height, self.info,
                self.order_cost)
