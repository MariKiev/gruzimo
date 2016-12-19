import logging

from django import forms
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from accounts.models import User

logger = logging.getLogger(__name__)


def create_registration_form(queryset):
    class RegistrationForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['email', 'first_name', 'get_news', 'city', 'phone']

        email = forms.EmailField(label="Email")
        first_name = forms.CharField(label="Имя")
        phone = PhoneNumberField(label="Телефон")
        city = forms.ModelChoiceField(queryset, label="Город")
        get_news = forms.CheckboxInput()
        password1 = forms.CharField(label="Пароль", required=True, widget=forms.TextInput(attrs={'type': 'password'}))
        password2 = forms.CharField(label="Подтверждение пароля	", required=True,
                                    widget=forms.TextInput(attrs={'type': 'password'}))

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
    return RegistrationForm