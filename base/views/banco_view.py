from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from base.libs.template import Template
from base.libs.listview import ListView
from base import config as PARAMS
from base.business.bbanco import BBanco
from base.models import Banco
from base.forms.banco_form import BancoForm


@login_required(login_url='login')
def banco_list(request):
    oListView = ListView(Banco)
    oListView.template_container = PARAMS.TemplateContainerMain
    oListView.template = PARAMS.Template.banco_list
    oListView.actions['action_new'] = reverse('banco_form', args=['new', 0])
    oListView.set_context()
    return render(request, oListView.template, context=oListView.context)


@login_required(login_url='login')
def banco_form(request, mode, id):
    url_return = 'banco_list'
    oBModel = BBanco()

    if mode != 'new':
        oTO = oBModel.get(id)
        if oTO == None:
            messages.error(request, f'Error. No se encontraron datos para el id = {id}' )
            return redirect(url_return)
    
    if request.method == 'POST':
        if mode == 'new':
            form = BancoForm(request.POST)
        else:
            form = BancoForm(request.POST, instance=oTO)
        if not form.is_valid():
            messages.error(request, 'Error en ingreso de datos')
        elif not oBModel.save(request, mode, id, form.cleaned_data):
            messages.error(request, oBModel.message)
        else:
            messages.success(request, oBModel.message)
            return redirect(url_return)
    else:
        if mode == 'new':
            form = BancoForm()
        else:
            form = BancoForm(instance=oTO)
    
    oTemplate = Template(Banco)
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.banco_form
    oTemplate.set_template_title(mode)
    oTemplate.actions['action_cancel'] = reverse(url_return)
    oTemplate.data['mode'] = mode
    oTemplate.data['id'] = id
    oTemplate.form = form
    oTemplate.set_context()

    return render(request, oTemplate.template, context=oTemplate.context)
