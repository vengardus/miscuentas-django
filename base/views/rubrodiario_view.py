from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from base.libs.template import Template
from base.libs.listview import ListView
from base import config as PARAMS
from base.business.brubrodiario import BRubroDiario
from base.models import RubroDiario
from base.forms.rubrodiario_form import RubroDiarioForm


@login_required(login_url='login')
def rubrodiario_list(request):
    oListView = ListView(RubroDiario)
    oListView.template_container = PARAMS.TemplateContainerMain
    oListView.template = PARAMS.Template.rubrodiario_list
    oListView.actions['action_new'] = reverse('rubrodiario_form', args=['new', 0])
    oListView.set_context()
    return render(request, oListView.template, context=oListView.context)


@login_required(login_url='login')
def rubrodiario_form(request, mode, id):
    url_return = 'rubrodiario_list'
    oBModel = BRubroDiario()

    if mode != 'new':
        oTO = oBModel.get(id)
        if oTO == None:
            messages.error(request, f'No se encontraron datos para el id = {id}' )
            return redirect(url_return)

    if request.method == 'POST':
        # self.context['global_stock_minimo'] = float(oCompania.get_stock_minimo(current_user.license_id))
        if mode == 'new':
            form = RubroDiarioForm(request.POST)
        else:
            form = RubroDiarioForm(request.POST, instance=oTO)
        if not form.is_valid():
            messages.error(request, 'Error en ingreso de datos')
        elif not oBModel.save(request, mode, id, form.cleaned_data):
            messages.error(request, oBModel.message)
        else:
            messages.success(request, oBModel.message)
            return redirect(url_return)
    else:
        if mode == 'new':
            form = RubroDiarioForm()
        else:
            form = RubroDiarioForm(instance=oTO)
    

    oTemplate = Template(RubroDiario)
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.rubrodiario_form
    oTemplate.set_template_title(mode)
    oTemplate.actions['action_cancel'] = reverse(url_return)
    oTemplate.data['mode'] = mode
    oTemplate.data['id'] = id
    oTemplate.form = form
    oTemplate.set_context()

    return render(request, oTemplate.template, context=oTemplate.context)
