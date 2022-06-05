from django.contrib import admin
from .models import Client,Device,Client_Group,Device_Group,Parameter,Parameter_threshold,Alarmed_Parameter

# Register your models here.

admin.site.register(Client)
admin.site.register(Device)
admin.site.register(Client_Group)
admin.site.register(Device_Group)
admin.site.register(Parameter)
admin.site.register(Parameter_threshold)
admin.site.register(Alarmed_Parameter)
