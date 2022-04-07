
class DestinoCuentaChoices:
    efectivo = '0'
    banco = '1'
    choices = [
        (efectivo, 'Efectivo'), 
        (banco, 'Banco')
    ]

    @staticmethod
    def get_desc(id):
        list_filter = list(filter(lambda x: x[0]==id, DestinoCuentaChoices.choices))
        return list_filter[0][1] if list else ''


class TipoCuentaChoices:
    monedero = '0'
    ahorro = '1'
    otro = '2'
    choices = [
        (monedero, 'Monedero'), 
        (ahorro, 'Ahorro'), 
        (otro, 'Otro')
    ]

    @staticmethod
    def get_desc(id):
        list_filter = list(filter(lambda x: x[0]==id, TipoCuentaChoices.choices))
        return list_filter[0][1] if list else ''


class MonedaChoices:
    moneda_local = '0'
    soles = moneda_local
    dolares = '1'
    choices = [
        (soles,'Soles', 'S/.'), 
        (dolares,'Dolares', 'USD.')
    ]

    @staticmethod
    def get_choices():
        return list(map(lambda x:(x[0], x[1]), MonedaChoices.choices))

    @staticmethod
    def get_desc(id):
        list_filter = list(filter(lambda x: x[0]==id, MonedaChoices.choices))
        return list_filter[0][1] if list else ''

    @staticmethod
    def get_abrev(id):
        list_filter = list(filter(lambda x: x[0]==id, MonedaChoices.choices))
        return list_filter[0][2] if list else ''

class TipoMovimientoChoices:
    ingreso = '0'
    egreso = '1'
    choices = [
        (ingreso, 'Ingreso'), 
        (egreso, 'Egreso')
    ]

    @staticmethod
    def get_desc(id):
        list_filter = list(filter(lambda x: x[0]==id, TipoMovimientoChoices.choices))
        return list_filter[0][1].upper() if list else ''


class TipoOperacionChoices:
    cambio_moneda = '0'
    transferencia_propias = '1'
    transferencias_terceros = '2'
    pagos_varios = '3'
    compras = '4'
    choices = [
        (cambio_moneda, 'Cambio de moneda'), 
        (transferencia_propias, 'Transferencia cuentas propias'), 
        (transferencias_terceros, 'Transferencia cuentas terceros'), 
        (pagos_varios, 'Pagos varios'),
        (compras, 'Compras'),
    ]

    @staticmethod
    def get_desc(id):
        list_filter = list(filter(lambda x: x[0]==id, TipoOperacionChoices.choices))
        return list_filter[0][1] if list else ''


class CalendarChoices:
    year_choices = [
        ('2022', '2022'),
        ('2023', '2023')
    ]
    month_choices = [
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    ]

    def get_month_desc(id):
        list_filter = list(filter(lambda x: x[0]==id, CalendarChoices.month_choices))
        return list_filter[0][1].upper() if list else ''

