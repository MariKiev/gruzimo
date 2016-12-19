from django.conf.urls import url

from accounts import views

urlpatterns = [

    # login stuff
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile/$', views.get_profile, name='get_profile'),

]