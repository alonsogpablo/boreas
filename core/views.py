from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView, DeleteView

from boreas_web.models import Client, Device
from core.forms import SignUpForm, UserForm, CreateDeviceForm, EditDeviceForm
from core.tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        client_form = SignUpForm(request.POST)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.client.phone = client_form.cleaned_data.get('phone')
            user.client.country = client_form.cleaned_data.get('country')
            user.client.city = client_form.cleaned_data.get('city')
            user.client.zipcode = client_form.cleaned_data.get('zipcode')
            user.client.address = client_form.cleaned_data.get('address')
            user.save()
            current_site = get_current_site(request)
            if request.LANGUAGE_CODE == 'es':
                subject = 'Active su cuenta'
            else:
                subject = 'Activate Your MySite Account'

            message = render_to_string('core/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        user_form = UserForm(request.GET)
        client_form = SignUpForm(request.GET)
    if request.LANGUAGE_CODE=='es':
        client_form.fields['phone'].label='Teléfono'
        client_form.fields['country'].label='País'
        client_form.fields['address'].label='Dirección'
        client_form.fields['zipcode'].label='Código Postal'
        client_form.fields['city'].label='Ciudad'
    return render(request, 'core/signup.html', {'user_form': user_form, 'client_form':client_form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.client.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'core/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'core/account_activation_sent.html')

def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request,user)
            if request.LANGUAGE_CODE=='es':
                messages.success(request, 'Su contraseña ha sido cambiada.')
            else:
                messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
        else:
            if request.LANGUAGE_CODE == 'es':
                messages.error(request, 'Por favor corrija el error siguiente:')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
         })


def create_device(request):
    if request.method=='POST':
        client = Client.objects.get(user=request.user.id)
        form=CreateDeviceForm(request.POST)
        if form.is_valid():
            device=form.save(commit=False)
            device.client_id=client.id
            form.save()
            if request.LANGUAGE_CODE == 'es':
                messages.success(request, 'Dispositivo creado')
            else:
                messages.success(request, 'Device created')

            return redirect('devices_table')
    else:
        form=CreateDeviceForm(request.GET)

    if request.LANGUAGE_CODE=='es':
        form.fields['name'].label='Nombre'
        form.fields['country'].label='País'
        form.fields['uuid'].label='Identificador de dispositivo'
        form.fields['aka'].label='Alias'
        form.fields['description'].label='Descripción'
        form.fields['zipcode'].label='Código Postal'

    return render(request, 'core/create_device.html', {'form':form})


class device_updateview(UpdateView):

    model = Device
    template_name = 'core/update_device.html'
    context_object_name = 'device'
    fields = '__all__'

    def form_valid(self, form):
        device_form = form.save(commit=False)
        device_form.save()
        id_device=self.kwargs['pk']
        device = Device.objects.get(id=id_device)
        return redirect('devices_table')

class device_deleteview(SuccessMessageMixin, DeleteView):
    model = Device
    success_url = reverse_lazy('devices_table')
    success_message = 'Device deleted'


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        id=self.object.id
        request.session['id']=id
        messages.success(self.request, self.success_message)
        return super(DeleteView, self).delete(request, *args, **kwargs)