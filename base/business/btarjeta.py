'''
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
__date__
'''
from base.libs.table import Table
from base import config as PARAMS
from base.models import Tarjeta


class BTarjeta(Table):
    aMessage = []           # lista de mensajes

    def __init__(self):
        self.TO = Tarjeta
        self.message_tablename = self.TO._meta.verbose_name
        self.aMessage = []

    def get_aTO_toArray(self):
        array = list()
        for oTO in self.aTO:
            array.append(self.get_oTO_toDict(oTO))
        return array
    
    def get_oTO_toDict(self, oTO:Tarjeta):
        # acá se genera diccionario con los atributos a retornar
        return {
            'id':oTO.id,
            'desc':oTO.desc,
            'banco_desc':oTO.banco.desc,
            'dia_cierre':oTO.dia_cierre,
            'portes':oTO.portes,
            'dia_pago':oTO.dia_pago
        }

    ''' ----------------------
        Métodos personalizados
    '''
    def _set_oTO(self, oTO:Tarjeta, data:list(), mode, request):
        '''
            Personalizar oTO
        '''
        
        oTO.desc = data['desc']
        oTO.banco = data['banco']
        oTO.dia_cierre = data['dia_cierre']
        oTO.portes = data['portes']
        oTO.dia_pago = data['dia_pago']

        if mode != 'new':
            oTO.user_edit_id = request.user.id
        else:
            oTO.user_created_id = request.user.id
            oTO.license_id = request.user.license_id
        return oTO
    
    def validate(self, data:list()):
        self.aMessage = []
        return True

    def save(self, request, mode, id, data:list()):
        ok = False
        if mode == 'new' :
            oTO = self.TO()
            oTO = self._set_oTO(oTO, data, mode, request)
            ok = self.insert(oTO)
        
        else: # edit
            oTO = self.get(id)
            if oTO == None:
                self.message = f'No se encontro registro con id={id}'
                self.error_code = PARAMS.ErrorCode.not_found
            else:
                oTO = self._set_oTO(oTO, data, mode, request,)
                ok = self.update(oTO)
            
        return ok
    
    def get_all(self, license_id:int=None):
        if license_id == None:
            self.aTO = self.TO.objects.all().order_by('desc')
        else:
            self.aTO = self.TO.objects.all().filter(license_id=license_id).order_by('desc')
        return self.aTO
    
