from django.shortcuts import render, redirect
import pandas as pd
import django_tables2 as tables
from django_tables2 import RequestConfig
from django_tables2.export import TableExport
from sqlalchemy import create_engine
from pandas_highcharts.core import serialize
    # Create your views here.
from boreas_web.models import Device
from django.utils.translation import ugettext as _

engine=create_engine('postgresql+psycopg2://boreas:Boreas1234@82.223.204.102:5432/boreas')

#Pablo Alonso+

def index(request):
    # pend_sols = cm_rc_sol.objects.filter(login_id=request.user.id,estado=1).count()
    # asignadas_sols = cm_rc_sol.objects.filter(login_id=request.user.id,estado=2).count()
    # asignadas_agente_sols = cm_rc_sol.objects.filter(login_ag_id=request.user.id,estado=2).count()
    # pendientes_agentes_sols = cm_rc_sol.objects.filter(estado=1).count()
    # cerradas_sols = cm_rc_sol.objects.filter(login_id=request.user.id,estado=3).count()
    # completadas_sols = cm_rc_sol.objects.filter(login_id=request.user.id,estado=4).count()
    # equipo_sols = cm_rc_sol.objects.filter(manager_id=request.user.id).count()
    # noticias=Noticias.objects.filter(noticia_is_active=True).order_by('-noticia_fecha')
    #
    # context = {
    #     'pend_sols': pend_sols,
    #     'pendientes_agentes_sols': pendientes_agentes_sols,
    #     'asignadas_sols': asignadas_sols,
    #     'asignadas_agente_sols': asignadas_agente_sols,
    #     'cerradas_sols': cerradas_sols,
    #     'completadas_sols': completadas_sols,
    #     'equipo_sols': equipo_sols,
    #     'noticias':noticias,
    # }
    #return render(request, 'index.html', context=context)
    return render(request, 'index.html')

def measures_chart(request):
    df = pd.read_sql('select * from view_mqtt_data', engine)
    cols=[i for i in df.columns if i not in ['uuid','timestamp']]
    for col in cols:
        df[col]=pd.to_numeric(df[col])
    df['timestamp']=pd.to_datetime(df['timestamp'])
    chart = serialize(df, render_to='measures_chart', output_type='json',x='timestamp',title='IAQ_measures')
    return render(request, 'boreas_web/measures_chart.html', {'chart':chart})

def device_status(request,id):
    uuid=Device.objects.values_list('uuid',flat=True).get(id=id)
    delta_days='1 day'
    query="""select * from view_mqtt_data where uuid = %(uuid)s and timestamp >= CURRENT_DATE- interval %(delta_days)s """
    df = pd.read_sql(query, engine,params={'uuid':uuid,'delta_days':delta_days})
    cols=[i for i in df.columns if i not in ['uuid','timestamp']]
    for col in cols:
        df[col]=pd.to_numeric(df[col])
    df['timestamp']=pd.to_datetime(df['timestamp'])
    chart = serialize(df, render_to='measures_chart', output_type='json',x='timestamp',title='IAQ_measures')
    return render(request, 'boreas_web/measures_chart.html', {'chart':chart})

class measure_table(tables.Table):
    uuid=tables.Column()
    timestamp=tables.Column()
    co2=tables.Column()
    voc=tables.Column()
    co=tables.Column()
    pm10=tables.Column()
    pm25=tables.Column()
    temp=tables.Column()
    hum=tables.Column()
    prb=tables.Column()
    pm1=tables.Column()
    pm4=tables.Column()

    class Meta:
        attrs = {"class": "table table-bordered"}


def device_info(request,id):
    uuid=Device.objects.values_list('uuid',flat=True).get(id=id)
    query="""select * from view_mqtt_data where uuid = %(uuid)s order by timestamp desc limit 10 """
    df = pd.read_sql(query, engine,params={'uuid':uuid})
    data=df.to_dict(orient='records')
    table=measure_table(data)
    template='boreas_web/show_device_info.html'
    RequestConfig(request).configure(table)
    export_format=request.GET.get("_export",None)
    if TableExport.is_valid_format(export_format):
        exporter=TableExport(export_format,table)
        return exporter.response("table.{}".format(export_format))
    return render(request,template,{'table':table})


