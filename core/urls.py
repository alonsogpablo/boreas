"""boreas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from core import views as core_views

urlpatterns = [
    path('core/signup',core_views.signup,name='signup'),
    path('core/change_password',core_views.change_password,name='change_password'),
    path('core/account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    path('core/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', core_views.activate, name='activate'),
    path('core/create_device',core_views.create_device,name='create_device'),
    path('core/update_device/<int:pk>', core_views.device_updateview.as_view(), name='update_device'),
    path('core/delete_device/<int:pk>', core_views.device_deleteview.as_view(), name='delete_device'),

]

