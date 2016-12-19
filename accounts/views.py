import logging

from django.contrib import messages
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.shortcuts import render, redirect

from accounts.forms import create_registration_form
from accounts.models import User
from locations.models import Location

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


def register(request):
    """ Function for registration new user.
    :param request: django.core.handlers.wsgi.WSGIRequest
    """
    Form = create_registration_form(Location.objects.all())

    if request.method == 'POST':
        registration_form = Form(request.POST)

        if User.objects.filter(email=request.POST.get('user-email')).exists():
            message = 'Юзер с таким email {} уже существует'.format(request.POST.get('user-email'))
            messages.success(request, message)
            logger.info(message)
            return render(request, 'user/register.html', {'form': registration_form})

        if registration_form.is_valid():
            with db_transaction.atomic():
                organization = registration_form['organization'].save()
                user = registration_form['user'].save(commit=False)
                user.organization = organization
                user.save()
                organization.owner_user_id = user.pk
                organization.save(update_fields=['owner_user_id'])

            user = authenticate(username=request.POST.get('user-email'), password=request.POST.get('user-password1'))
            django_login(request, user)
            return redirect('dashboard')

        logger.error(registration_form.non_field_errors())
    else:
        registration_form = Form()
    return render(request, 'user/register.html', {'form': registration_form})


def login(request):
    """Log in user by email. Data set during the anonymous session is retained when the user logs in.
    :param request: django.core.handlers.wsgi.WSGIRequest
    """
    if request.user.is_authenticated():
        return redirect('dashboard')

    if request.method == 'POST':
        user = authenticate(username=request.POST['email'], password=request.POST['password'])

        if not user:
            return render(request, 'user/login.html', {'error': 'Email or password mismatch'})

        if not user.is_active:
            return render(request, 'user/login.html', {'error': "You're account has been disabled."})

        django_login(request, user)
        return redirect('dashboard')
    return render(request, 'user/login.html')


@login_required
def logout(request):
    """
    Removes the authenticated user's ID from the request and flushes their
    session data.
    :param request: django.core.handlers.wsgi.WSGIRequest
    """
    django_logout(request)
    return render(request, 'user/logout.html')

