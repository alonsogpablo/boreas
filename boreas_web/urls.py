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
from boreas_web import views, tables

urlpatterns = [
    path('boreas/measures_chart', views.measures_chart, name='measures_chart'),
    path('boreas/devices_table',tables.Devices_tableview,name='devices_table'),
    path('boreas/all_devices_table',tables.All_Devices_tableview,name='all_devices_table'),
    path('boreas/device_status/<int:id>', views.device_status, name='device_status'),
    path('boreas/device_info/<int:id>', views.device_info, name='device_info'),

]

