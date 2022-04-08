from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from base.libs.template import Template
from base.libs.listview import ListView
from base import config as PARAMS
from base.business.bconceptodiario import BConceptoDiario
from base.models import ConceptoDiario
from base.forms.conceptodiario_form import ConceptoDiarioForm


@login_required(login_url='login')
def conceptodiario_list(request):
    oListView = ListView(ConceptoDiario)
    oListView.template_container = PARAMS.TemplateContainerMain
    oListView.template = PARAMS.Template.conceptodiario_list
    oListView.actions['action_new'] = reverse('conceptodiario_form', args=['new', 0])
    oListView.set_context()
    return render(request, oListView.template, context=oListView.context)


@login_required(login_url='login')
def conceptodiario_form(request, mode, id):
    url_return = 'conceptodiario_list'
    oBModel = BConceptoDiario()
    
    print('ed-init', mode)
    if mode != 'new':
        oTO = oBModel.get(id)
        if oTO == None:
            messages.error(request, f'Error. No se encontraron datos para el id = {id}' )
            return redirect(url_return)

    if request.method == 'POST':
        if mode == 'new':
            form = ConceptoDiarioForm(request, request.POST)
        else:
            form = ConceptoDiarioForm(request, request.POST, instance=oTO)
        if not form.is_valid():
            messages.error(request, 'Error en ingreso de datos')
        elif not oBModel.save(request, mode, id, form.cleaned_data):
            messages.error(request, oBModel.message)
        else:
            messages.success(request, oBModel.message)
            return redirect(url_return)
    else:
        if mode == 'new':
            form = ConceptoDiarioForm(request)
        else:
            form = ConceptoDiarioForm(request, instance=oTO)

    oTemplate = Template(ConceptoDiario)
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.conceptodiario_form
    oTemplate.set_template_title(mode)
    oTemplate.actions['action_cancel'] = reverse(url_return)
    oTemplate.data['mode'] = mode
    oTemplate.data['id'] = id
    oTemplate.form = form
    oTemplate.set_context()

    return render(request, oTemplate.template, context=oTemplate.context)
