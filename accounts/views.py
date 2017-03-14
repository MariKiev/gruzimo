import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import RegistrationForm, OrderForm
from accounts.models import User
from orders.utils import get_order_cost, get_content_for_mail, send_email

logger = logging.getLogger(__name__)


def home(request):
    if request.method == 'POST':
        logger.info('create order request: {}'.format(request.POST))
        order_form = OrderForm(request.POST)

        if 'calculate_order' in request.POST:
            logger.info('calculate_order request: {}'.format(request.POST))

            if not order_form.is_valid():
                return render(request, 'home.html', {'form': order_form})

            cost = get_order_cost(request.POST)
            return render(request, 'home.html', {'form': order_form,
                                                 'cost': cost})

        else:
            if not order_form.is_valid():
                return render(request, 'home.html', {'form': order_form})

            order = order_form.save()

            # send email about new order
            text_content, html_content = get_content_for_mail(order)
            send_email('New gruzimo order {}'.format(order.id),
                       text_content, html_content, 'gruzimo@sparkpostbox.com', settings.EMAIL_SEND_USER)

            messages.success(request, 'Ваша заявка отправлена')
            return redirect('home')

    else:
        order_form = OrderForm()
    return render(request, 'home.html', {'form': order_form})


def register(request):
    """ Function for registration new user.
    :param request: django.core.handlers.wsgi.WSGIRequest
    """

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)

        if not registration_form.is_valid():
            return render(request, 'user/register.html', {'form': registration_form})

        user = registration_form.save()
        user = authenticate(email=user.email, password=request.POST.get('password1'))
        django_login(request, user)
        return redirect('dashboard')

    else:
        registration_form = RegistrationForm()
    return render(request, 'user/register.html', {'form': registration_form})


def login(request):
    """Log in user by email. Data set during the anonymous session is retained when the user logs in.
    :param request: django.core.handlers.wsgi.WSGIRequest
    """
    if request.user.is_authenticated():
        return redirect('dashboard')

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        if not user:
            return render(request, 'user/login.html', {'error': 'Email или пароль не совпадают'})

        if not user.is_active:
            return render(request, 'user/login.html', {'error': "Ваш аккаунт заблокирован"})

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


@login_required
def dashboard(request):
    return render(request, 'user/dashboard.html')


@login_required
def get_profile(request):
    return render(request, 'user/profile.html')


def create_order(request):
    # if request.method == 'POST':
    #     logger.info('create order request: {}'.format(request.POST))
    #     order_form = OrderForm(request.POST)
    #
    #     if 'calculate_order' in request.POST:
    #         logger.info('calculate_order request: {request.POST}'.format())
    #         form = OrderCostForm(request.POST)
    #
    #         if not form.is_valid():
    #             return render(request, 'home.html', {'form': order_form})
    #
    #         cost = get_order_cost(request.POST)
    #         return render(request, 'home.html', {'form': order_form,
    #                                              'cost': cost})
    #
    #     else:
    #         if not order_form.is_valid():
    #             return render(request, 'home.html', {'form': order_form})
    #
    #         order_form.save()
    #
    #         return redirect('home')
    #
    # else:
    #     order_form = OrderForm()
    # return render(request, 'home.html', {'form': order_form})
    pass
