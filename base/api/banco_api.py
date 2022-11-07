import json
from django.http import JsonResponse
from django.urls import reverse
from django.contrib import messages

from base.libs.controller import Controller
from base.business.bbanco import BBanco


def banco_controller(request):
    oController = ControllerCustom(json.load(request), request)
    context = oController.do_action()
    context = JsonResponse(context)
    return context
    
class ControllerCustom(Controller):

    def __init__(self, data, request):
        super().__init__(data)
        self.request = request
        self.set_actions()
        self.url_action_new = 'banco_form'

    def set_actions(self):
        super().set_actions()
        
        # FUNCIONALIDAD PERSONALIZADA
        # ---------------------------

    def action_save(self):
        return super().action_save()

    def action_edit(self):
        id = self.data['id']
        self.context['action_new'] = reverse(self.url_action_new, args=['edit', id])
        return self.context
        
    def action_delete(self):
        oBModel = BBanco()
        if not oBModel.delete(self.data['id']):
            self.context['status'] = oBModel.error_code
            messages.error(self.request, oBModel.message)
        else:
            oBModel.get_all(self.request.user.license_id)
            self.context['aDataTable'] = oBModel.get_aTO_toArray()
            self.context['action_new'] = reverse(self.url_action_new, args=['new', 0])
            messages.success(self.request, oBModel.message)
            
        self.context['aMessage'].append(oBModel.message)
        return self.context

    def action_refresh(self):
        show_grid_header = self.data['show_grid_header']
        oBModel = BBanco()
        oBModel.get_all(self.request.user.license_id)
        self.context['aDataTable'] = oBModel.get_aTO_toArray()
        self.context['action_new'] = reverse(self.url_action_new, args=['new', 0]); #'banco_form'
        self.context['aHeader'] = self.set_grid_columns() if show_grid_header else []
        return self.context
   
    
    # FUNCIONALIDAD PERSONALIZADA
    # ---------------------------
    def set_grid_columns(self):
        '''
        Retorna lista de tuplas, puede tener una o mas tuplas (de momento se consideran hasta 2)
        La primera tupla tiene las etiquetas para pantallas grandes (width>=768)
        La segunda tupla tiene las etiquetas para pantallas pequeñas
        '''
        return [ 
                ('Id', 'Descripción', 'Acción'),
        ]

