from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Client_Group(models.Model):
    name=models.CharField(max_length=500,null=True,blank=True,unique=True)
    nif_cif=models.CharField(max_length=100,null=True,blank=True,unique=True)
    phone=models.IntegerField(null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    zipcode=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name



class Device_Group(models.Model):
    client_group=models.ForeignKey(Client_Group,on_delete=models.CASCADE)
    name=models.CharField(max_length=500,null=True,blank=True,unique=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    client_group=models.ForeignKey(Client_Group,on_delete=models.CASCADE,blank=True,null=True)
    device_group=models.ManyToManyField(Device_Group,blank=True,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.IntegerField(null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    city=models.CharField(max_length=100,null=True,blank=True)
    zipcode=models.IntegerField(null=True,blank=True)
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'user'

    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Client.objects.create(user=instance)
    instance.client.save()


class Parameter(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True,unique=True)
    def __str__(self):
        return self.name

class Alarmed_Parameter(models.Model):
    name=models.CharField(max_length=100,null=True,blank=True,unique=True)
    def __str__(self):
        return self.name


class Device(models.Model):
    client_group=models.ForeignKey(Client_Group,on_delete=models.CASCADE,blank=True,null=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,blank=True,null=True)
    device_group=models.ManyToManyField(Device_Group,blank=True)
    parameter=models.ManyToManyField(Parameter,blank=True)
    alarmed_parameter=models.ManyToManyField(Alarmed_Parameter,blank=True)
    uuid=models.CharField(max_length=100,null=True,blank=True,unique=True)
    aka=models.CharField(max_length=100,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    country=models.CharField(max_length=100,null=True,blank=True)
    description=models.TextField(null=True,blank=True)
    zipcode=models.IntegerField(null=True,blank=True)
    active_device=models.BooleanField(default=True,blank=True,null=True)

    def __str__(self):
        return self.uuid


class Parameter_threshold(models.Model):
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)
    #device = models.ForeignKey(Device, on_delete=models.CASCADE)
    threshold = models.DecimalField(null=True, blank=True, decimal_places=4, max_digits=10)
    sampling_freq = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.parameter.name+'_'+str(self.threshold)