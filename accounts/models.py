from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from locations.models import Location


class User(AbstractBaseUser):
    """User business model"""
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30, default="")
    phone = PhoneNumberField(default="")
    city = models.ForeignKey(Location, default=1)
    get_news = models.BooleanField(default=False)
    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as '
                                              'active. Unselect this instead of deleting accounts.'
                                    )
    is_superuser = models.BooleanField('superuser status', default=False,
                                       help_text='Designates that this user has all permissions without '
                                                 'explicitly assigning them.')
    is_verify_email = models.BooleanField(default=False)
