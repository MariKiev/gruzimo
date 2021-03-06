import logging

from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from accounts.models import User
from locations.models import Location
from orders.models import Order
from orders.utils import convert_meter_to_centimeter

logger = logging.getLogger(__name__)


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'get_news', 'city', 'phone']

    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    phone = PhoneNumberField(label="Телефон")
    city = forms.ModelChoiceField(queryset=Location.objects.all(), label="Город", initial=1)
    get_news = forms.CheckboxInput()
    password1 = forms.CharField(label="Пароль", required=True, widget=forms.TextInput(attrs={'type': 'password'}))
    password2 = forms.CharField(label="Подтверждение пароля	", required=True,
                                widget=forms.TextInput(attrs={'type': 'password'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) == 10:
            return '+38' + phone
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            message = 'Юзер с таким email {} уже существует'.format(email)
            raise ValidationError(message, code='invalid')
        return email

    def clean(self):
        if self.cleaned_data.get("password1") != self.cleaned_data.get("password2"):
            raise ValidationError('Пароли не совпадают', code='invalid')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))

        if commit:
            user.save()
        return user


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['from_address', 'from_house', 'from_entrance', 'to_address', 'to_house', 'order_date', 'name',
                  'phone', 'length', 'width', 'height', 'info']

        labels = {
            'from_address': 'Адрес подачи:',
            'from_house': 'Дом:',
            'from_entrance': 'Подъезд:',
            'to_address': 'Адрес доставки:',
            'to_house': 'Дом:',
            'order_date': 'Когда ехать:',
            'name': 'Ваше имя:',
            'phone': 'Телефон:',
            'length': 'Длина, м:',
            'width': 'Ширина, м:',
            'height': 'Высота, м:',
            'info': 'Опишите ваш груз',
        }

        widgets = {
            'from_address': forms.widgets.Input(attrs={'autocomplete': 'on'}),
            'to_address': forms.widgets.Input(attrs={'autocomplete': 'on'}),
            'length': forms.widgets.Input(attrs={"step": "0.01"}),
            'width': forms.widgets.Input(attrs={"step": "0.01"}),
            'height': forms.widgets.Input(attrs={"step": "0.01"})
        }

    length = forms.FloatField()
    width = forms.FloatField()
    height = forms.FloatField()

    def clean_length(self):
        return convert_meter_to_centimeter(self.cleaned_data.get('length'))

    def clean_width(self):
        return convert_meter_to_centimeter(self.cleaned_data.get('width'))

    def clean_height(self):
        return convert_meter_to_centimeter(self.cleaned_data.get('height'))
