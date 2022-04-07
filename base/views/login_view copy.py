import email
import imp
from multiprocessing.spawn import import_main_path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings

from base.models import User as TOUser
from base.business.buser import User
from base.forms_ import UserForm, MyUserCreationForm
from base.libs.template import Template
from base import config as PARAMS
from studybud.settings import BASE_DIR


def login_app(request):
    page = 'login'
    oTemplate = Template(None)
    oTemplate.template_title = f'{PARAMS.AppName} - Home'
    oTemplate.template_container = PARAMS.TemplateContainerLogin
    oTemplate.template = PARAMS.Template.login
    oTemplate.set_context()


    if request.method == 'POST':
        email = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(email, password)
        try:
            oTOUser = TOUser.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')
        
        oTOUser = authenticate(request, username=email, password=password)
        if oTOUser is not None:
            login(request, oTOUser)
            return redirect('main')
        else:
            messages.error(request, 'Username or Password does not exist.')
            print('error 2')


    oTemplate.data['page'] = page
    oTemplate.data['action_register'] = reverse('register')
    return render(request, oTemplate.template, context=oTemplate.context)

def logout_app(request):
    logout(request)
    return redirect('main')

login_required(login_url='login')
def account(request):
    user = request.user
    form = UserForm(instance=user)

    oTemplate = Template()
    oTemplate.form = form
    oTemplate.template_title = f'{PARAMS.AppName} - Mi Cuenta'
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.account
    oTemplate.set_context()

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            try:
                # user = form.save(commit=False)
                # user.save()
                form.save()
            except Exception as e:
                messages.error(request, e)

            return redirect('account')

    return render(request, oTemplate.template, oTemplate.context)

def registerUser(request):
    form = MyUserCreationForm()

    oTemplate = Template()
    oTemplate.form = form
    oTemplate.template_title = f'{PARAMS.AppName} - Registro'
    oTemplate.template_container = PARAMS.TemplateContainerLogin
    oTemplate.template = PARAMS.Template.register
    oTemplate.set_context()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'Error en los datos.')
        else:
            oUser = User()
            user = oUser.save(form)
            if user != None:
                login(request, user)
                return redirect('main')

    return render(request, oTemplate.template, oTemplate.context)

login_required(login_url='login')
def about(request):
    oTemplate = Template()
    oTemplate.title = f'{PARAMS.AppName} - About'
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.about
    # oTemplate.data['env_version'] = env_version
    oTemplate.data['env_version'] = f'{PARAMS.AppName}-{PARAMS.Version}'
    oTemplate.set_context()
    
    return render(request, oTemplate.template, oTemplate.context)


