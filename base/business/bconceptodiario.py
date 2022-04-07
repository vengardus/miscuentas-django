from base.libs.table import Table
from base import config as PARAMS
from base.models import ConceptoDiario
from base.choices import TipoMovimientoChoices


class BConceptoDiario(Table):
    aMessage = []           # lista de mensajes

    def __init__(self):
        self.TO = ConceptoDiario
        self.message_tablename = self.TO._meta.verbose_name
        self.aMessage = []

    def get_aTO_toArray(self):
        array = list()
        for oTO in self.aTO:
            array.append(self.get_oTO_toDict(oTO))
        return array
    
    def get_oTO_toDict(self, oTO:ConceptoDiario):
        # acá se genera diccionario con los atributos a retornar
        return {
            'id':oTO.id,
            'desc':oTO.desc,
            'rubro_diario_desc': oTO.rubro_diario.desc,
            'tipo_movimiento_desc': TipoMovimientoChoices.get_desc(oTO.rubro_diario.tipo_movimiento)
        }

    ''' ----------------------
        Métodos personalizados
    '''
    def _set_oTO(self, oTO:ConceptoDiario, data:list(), mode, request):
        '''
            Personalizar oTO
        '''
        
        oTO.desc = data['desc']
        oTO.rubro_diario = data['rubro_diario']

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
    
    def get_all_servicios(self, license_id:int=None):
        if license_id == None:
            self.aTO = self.TO.objects.all().filter(rubro_diario__is_servicio=True).order_by('desc')
        else:
            self.aTO = self.TO.objects.all().filter(
                license_id=license_id).order_by('date_created')
        return self.aTO
