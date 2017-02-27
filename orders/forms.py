from django.forms import forms

from orders.models import Order


class OrderCostForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['from_address', 'from_house', 'from_entrance', 'to_address', 'to_house',
                  'length', 'width', 'height']