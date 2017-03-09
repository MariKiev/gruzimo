from django.forms import forms

from orders.models import Order
from orders.utils import convert_meter_to_centimeter


# class OrderCostForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['from_address', 'from_house', 'from_entrance', 'to_address', 'to_house',
#                   'length', 'width', 'height']
#
#         # widgets = {
#         #     'length': forms.widgets.Input(attrs={"step": "0.01"}),
#         #     'width': forms.widgets.Input(attrs={"step": "0.01"}),
#         #     'height': forms.widgets.Input(attrs={"step": "0.01"})
#         # }
#
#     def clean_length(self):
#         return convert_meter_to_centimeter(self.cleaned_data.get('length'))
#
#     def clean_width(self):
#         return convert_meter_to_centimeter(self.cleaned_data.get('width'))
#
#     def clean_height(self):
#         return convert_meter_to_centimeter(self.cleaned_data.get('height'))
