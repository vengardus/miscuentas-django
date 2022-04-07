'''
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
__date__
'''
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from base.libs.template import Template
from base.libs.listview import ListView
from base import config as PARAMS
from base.business.bmovimiento import BMovimiento
from base.models import Movimiento
from base.forms.movimiento_form import MovimientoForm


@login_required(login_url='login')
def movimiento_list(request):
    oListView = ListView(Movimiento)
    oListView.template_container = PARAMS.TemplateContainerMain
    oListView.template = PARAMS.Template.movimiento_list
    oListView.actions['action_new'] = reverse('movimiento_form', args=['new', 0])
    oListView.set_context()
    return render(request, oListView.template, context=oListView.context)


@login_required(login_url='login')
def movimiento_form(request, mode, id):
    url_return = 'movimiento_list'
    oBModel = BMovimiento()
    if mode != 'new':
        oTO = oBModel.get(id)
        if oTO == None:
            messages.error(request, f'No se encontraron datos para el id = {id}' )
            return redirect(url_return)
    
    if request.method == 'POST':
        # self.context['global_stock_minimo'] = float(oCompania.get_stock_minimo(current_user.license_id))
        if mode == 'new':
            form = MovimientoForm(request, request.POST)
        else:
            form = MovimientoForm(request, request.POST, instance=oTO)
        if not form.is_valid():
            messages.error(request, 'Error en ingreso de datos')
        elif not oBModel.save(request, mode, id, form.cleaned_data):
            messages.error(request, oBModel.message)
        else:
            messages.success(request, oBModel.message)
            return redirect(url_return)
    else:
        if mode == 'new':
            form = MovimientoForm(request)
        else:
            form = MovimientoForm(request, instance=oTO)
    
    oTemplate = Template(Movimiento)
    oTemplate.template_container = PARAMS.TemplateContainerMain
    oTemplate.template = PARAMS.Template.movimiento_form
    oTemplate.set_template_title(mode)
    oTemplate.actions['action_cancel'] = reverse(url_return)
    oTemplate.data['mode'] = mode
    oTemplate.data['id'] = id
    oTemplate.form = form
    oTemplate.set_context()

    return render(request, oTemplate.template, context=oTemplate.context)