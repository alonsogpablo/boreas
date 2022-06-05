import django_tables2 as tables
from django.shortcuts import render
from django_tables2 import TemplateColumn, RequestConfig
from django_tables2.export import TableExport

from .models import Device, Client


class DevicesTable(tables.Table):
    export_formats = 'csv'
    class Meta:
        model = Device
        template_name = "django_tables2/bootstrap.html"
        fields = ('client','uuid','aka','name', )

    info = TemplateColumn(template_name='boreas_web/device_info.html', exclude_from_export=True)
    status = TemplateColumn(template_name='boreas_web/device_status.html', exclude_from_export=True)
    edit = TemplateColumn(template_name='boreas_web/device_edit.html', exclude_from_export=True)
    delete = TemplateColumn(template_name='boreas_web/device_delete.html', exclude_from_export=True)

def Devices_tableview(request):
    client = Client.objects.get(user=request.user.id)
    client_id=client.id
    client_group=client.client_group
    devices=Device.objects.filter(client_group=client_group,active_device=True)
    table = DevicesTable(devices)

    RequestConfig(request).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(request, 'boreas_web/table_devices.html', {"table":table})


def All_Devices_tableview(request):
    client = Client.objects.all()
    devices=Device.objects.filter(active_device=True)
    table = DevicesTable(devices)

    RequestConfig(request).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    return render(request, 'boreas_web/table_devices.html', {"table":table})