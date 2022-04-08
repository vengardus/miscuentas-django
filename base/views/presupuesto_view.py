'''
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
__date__
'''
from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from base.choices import MonedaChoices

from base.libs.template import Template
from base.libs.listview import ListView
from base import config as PARAMS
from base.business.bpresupuesto import BPresupuesto
from base.models import Presupuesto
from base.forms.presupuesto_form import PresupuestoForm


@login_required(login_url='login')
def presupuesto_list(request):
    oListView = ListView(Presupuesto)
    oListView.template_container = PARAMS.TemplateContainerMain
    oListView.template = PARAMS.Template.presupuesto_list
    oListView.actions['action_new'] = reverse('presupuesto_form', args=['new', 0])
    oListView.set_context()
    return render(request, oListView.template, context=oListView.context)


@login_required(login_url='login')
def presupuesto_form(request, mode, id):
    url_return = 'presupuesto_list'
    oBModel = BPresupuesto()

    if mode != 'new':
        oTO = oBModel.get(id)
        if oTO == None:
            messages.error(request, f'No se encontraron datos para el id = {id}' )
            return redirect(url_return)
    
    if request.method == 'POST':
        # self.context['global_stock_minimo'] = float(oCompania.get_stock_minimo(current_user.license_id))
        if mode == 'new':
            form = PresupuestoForm(request, request.POST)
        else:
            form = PresupuestoForm(request, request.POST, instance=oTO)
        if not form.is_valid():
            messages.error(request, 'Error en ingreso de datos')
        elif not oBModel.save(request, mode, id, form.cleaned_data):
            messages.error(request, oBModel.message)
        else:
            messages.success(request, oBModel.message)
            return redirect(url_return)
    else:
        if mode == 'new':
            form = PresupuestoForm(request)
            form.fields['anio'].initial = str(datetime.now().year)
            form.fields['moneda'].initial = MonedaChoices.moneda_local
        else:
            form = PresupuestoForm(request, instance=oTO)

    oTemplate = Template(Presupuesto)
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.presupuesto_form
    oTemplate.set_template_title(mode)
    oTemplate.actions['action_cancel'] = reverse(url_return)
    oTemplate.data['mode'] = mode
    oTemplate.data['id'] = id
    oTemplate.form = form
    oTemplate.set_context()

    return render(request, oTemplate.template, context=oTemplate.context)

@login_required(login_url='login')
def genpresupuesto_form(request):
    url_return = 'main'
    oTemplate = Template(None)
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.genpresupuesto_form
    oTemplate.template_title = 'Genera presupuesto'
    oTemplate.actions['action_cancel'] = reverse(url_return)
    oTemplate.set_context()

    oBModel = BPresupuesto()
    oTemplate.data['aResumen'] = oBModel.generar_presupuesto(request)

    return render(request, oTemplate.template, context=oTemplate.context)
