'''
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
__date__
'''
from datetime import datetime, timedelta
from base.libs.table import Table
from base import config as PARAMS
from base.models import Compra


class BCompra(Table):
    aMessage = []           # lista de mensajes

    def __init__(self):
        self.TO = Compra
        self.message_tablename = self.TO._meta.verbose_name
        self.aMessage = []

    def get_aTO_toArray(self):
        array = list()
        for oTO in self.aTO:
            array.append(self.get_oTO_toDict(oTO))
        return array
    
    def get_oTO_toDict(self, oTO:Compra):
        # acá se genera diccionario con los atributos a retornar
        return {
            'id':oTO.id,
            'fecha_compra':oTO.fecha_compra,
            'tarjeta_desc':oTO.tarjeta.desc,
            'comercio_desc':oTO.comercio.desc,
            'monto':oTO.monto,
            'cuotas':oTO.cuotas,
            'is_fuera_cierre':oTO.is_fuera_cierre,
            'detalle':oTO.detalle if oTO.detalle else '',
            'obs':oTO.obs if oTO.obs else '',
        }

    ''' ----------------------
        Métodos personalizados
    '''
    def _set_oTO(self, oTO:Compra, data:list(), mode, request):
        '''
            Personalizar oTO
        '''
        
        oTO.fecha_compra = data['fecha_compra']
        oTO.tarjeta = data['tarjeta']
        oTO.comercio = data['comercio']
        oTO.monto = data['monto']
        oTO.cuotas = data['cuotas']
        oTO.monto_cuota = data['monto_cuota'] if oTO.cuotas > 1 else oTO.monto
        oTO.detalle = data['detalle']
        oTO.obs = data['obs']
        oTO.is_fuera_cierre = data['is_fuera_cierre']
        oTO.is_online = data['is_online']

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
            self.aTO = self.TO.objects.all().order_by('-fecha_compra')
        else:
            self.aTO = self.TO.objects.all().filter(license_id=license_id).order_by('-fecha_compra')
        return self.aTO
    
    def get_all_ascendent(self, license_id:int=None):
        if license_id == None:
            self.aTO = self.TO.objects.all().order_by('fecha_compra')
        else:
            self.aTO = self.TO.objects.all().filter(license_id=license_id).order_by('fecha_compra')
        return self.aTO
    
    def generar_cierre(self, license_id:int):
        self.get_all_ascendent(license_id)
        if not self.aTO:
            return []

        # set fecha_transaccion para las fecha_compra se que se procesan fuera del cierre
        oTO:Compra 
        for oTO in self.aTO:
            if not oTO.is_fuera_cierre:
                oTO.fecha_transaccion = oTO.fecha_compra
            else:
                diferencia_dias = oTO.tarjeta.dia_cierre - oTO.fecha_compra.day + 1
                oTO.fecha_transaccion = oTO.fecha_compra + timedelta(diferencia_dias)
        
        self.aTO = sorted(self.aTO, key=lambda x:x.fecha_transaccion)
        for oTO in self.aTO:
            print(oTO)


        # recorrer compras y generar pagos por fecha cierre
        is_nuevo_periodo = True
        aPagoMes = []
        pos = 0
        while pos < len(self.aTO):
            oTO = self.aTO[pos]
            if is_nuevo_periodo:
                total_mes = 0
                portes = oTO.tarjeta.portes
                if oTO.fecha_transaccion.day > oTO.tarjeta.dia_cierre:
                    day = oTO.tarjeta.dia_cierre
                    month = oTO.fecha_transaccion.month+1 if oTO.fecha_transaccion.month < 12 else 1 
                    year = oTO.fecha_transaccion.year if oTO.fecha_transaccion.month < 12 else oTO.fecha_transaccion.year+1
                    fecha_cierre = datetime(year, month, day).date()

                    day = oTO.tarjeta.dia_pago 
                    month = oTO.fecha_transaccion.month+2 if oTO.fecha_transaccion.month < 11 else 2 
                    year = oTO.fecha_transaccion.year if oTO.fecha_transaccion.month < 11 else oTO.fecha_transaccion.year+1 
                    fecha_pago = datetime(year, month, day).date()
                else:
                    fecha_cierre = datetime(                                          
                                            oTO.fecha_transaccion.year,
                                            oTO.fecha_transaccion.month,
                                            oTO.tarjeta.dia_cierre
                                            ).date()
                    print('==)',fecha_cierre)
                    day = oTO.tarjeta.dia_pago 
                    month = oTO.fecha_transaccion.month+1 if oTO.fecha_transaccion.month != 12 else 1
                    year = oTO.fecha_transaccion.year if oTO.fecha_transaccion.month != 12 else oTO.fecha_transaccion.year+1
                    fecha_pago = datetime(year, month, day).date()


            print(oTO.fecha_transaccion, fecha_cierre)

            if oTO.fecha_transaccion > fecha_cierre:
                is_nuevo_periodo = True
                aPagoMes.append({
                    'fecha_cierre': fecha_cierre,
                    'fecha_pago' : fecha_pago,
                    'monto' : total_mes + portes,
                    'tarjeta': oTO.tarjeta.id,
                    'tarjeta_desc': oTO.tarjeta.desc
                })
            else:
                is_nuevo_periodo = False
                total_mes += oTO.monto if oTO.cuotas == 1 else oTO.monto_cuota
                pos +=1

        aPagoMes.append({
                    'fecha_cierre': fecha_cierre,
                    'fecha_pago' : fecha_pago,
                    'monto' : total_mes + portes,
                    'tarjeta': oTO.tarjeta.id,
                    'tarjeta_desc': oTO.tarjeta.desc
                })

        aPagoMes = sorted(aPagoMes, key=lambda x:x['fecha_pago'], reverse=True)

        return aPagoMes