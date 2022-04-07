from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
import base.choices

# Create your models here.

class Common(models.Model):
    license_id = models.IntegerField()
    user_created_id = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    user_edit_id = models.IntegerField(null=True, blank=True)
    date_edit = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, blank=True, default='')
  
    class Meta:
        abstract = True  


class License(Common):
    license_key = models.CharField(max_length=50, unique=True)
    desc = models.CharField(max_length=40)
    num_licenses = models.IntegerField(default=3)
    user_type = models.CharField(max_length=1, default='A')

    def __str__(self) -> str:
        return self.desc


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    #bio = models.TextField(null=True)
    user_type  = models.CharField(max_length=1, null=True,  default='U')
    image_file = models.ImageField(null=True, default="avatar.svg", upload_to="users/")
    license_id = models.IntegerField(default=1)
    status = models.CharField(max_length=1, default='A')
    modo_apariencia = models.CharField(max_length=1, choices = [('0', 'Claro'), ('1', 'Oscuro')], default='0')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Banco(Common):
    desc = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.desc


class Cuenta(Common):
    desc = models.CharField(max_length=50, unique=True)
    destino_cuenta = models.CharField(max_length=1, choices=base.choices.DestinoCuentaChoices.choices) 
    tipo_cuenta = models.CharField(max_length=1, choices=base.choices.TipoCuentaChoices.choices)
    moneda = models.CharField(max_length=1, choices=base.choices.MonedaChoices.get_choices())
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    numero_cuenta = models.CharField(max_length=20, null=True, blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_apertura = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.desc


class CambioMoneda(Common):
    monto_cambiar = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=4)
    monto_cambiado = models.DecimalField(max_digits=10, decimal_places=2)
    cuenta_origen = models.IntegerField(default=0)
    cuenta_destino_efectivo = models.IntegerField(default=0)
    cuenta_destino_banco = models.IntegerField(default=0)
    monto_deposito_efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monto_deposito_banco = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self) -> str:
        return f'{self.monto_cambiar} x {self.tipo_cambio} = {self.monto_cambiado}'


class RubroDiario(Common):
    desc = models.CharField(max_length=50, unique=True)
    is_servicio = models.BooleanField(default=False)
    tipo_movimiento = models.CharField(max_length=1, choices=base.choices.TipoMovimientoChoices.choices)

    class Meta:
        verbose_name_plural = 'Rubros diario'

    def __str__(self) -> str:
        return self.desc


class ConceptoDiario(Common):
    desc = models.CharField(max_length=50, unique=True)
    rubro_diario = models.ForeignKey(RubroDiario, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.desc


class Movimiento (Common):
    id_movimiento = models.IntegerField(default=0)
    tipo_movimiento = models.CharField(max_length=1, choices=base.choices.TipoMovimientoChoices.choices)
    tipo_operacion = models.CharField(max_length=1, choices=base.choices.TipoOperacionChoices.choices)
    cod_operacion = models.CharField(max_length=10, null=True, blank=True)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    obs = models.CharField(max_length=50, null=True, blank=True)
    cuenta_tercero = models.CharField(max_length=50, null=True, blank=True)
    concepto_gasto = models.ForeignKey(ConceptoDiario, on_delete=models.SET_NULL, null=True)
    fecha_movimiento = models.DateField(default=datetime.now)
    
    def __str__(self) -> str:
        return f'{self.tipo_movimiento} - {self.cuenta} - {self.monto}' 


class Tarjeta(Common):
    desc = models.CharField(max_length=50)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    dia_cierre = models.IntegerField()
    portes = models.DecimalField(max_digits=10, decimal_places=2)
    dia_pago = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'{self.desc}'

class Comercio(Common):
    desc = models.CharField(max_length=50)
    is_servicio = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.desc}'


class Compra(Common):
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    cuotas = models.IntegerField(default=1)
    monto_cuota = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_compra = models.DateField()
    comercio = models.ForeignKey(Comercio, on_delete=models.CASCADE)
    detalle = models.CharField(max_length=100, null=True, blank=True)
    obs = models.CharField(max_length=100, null=True, blank=True)
    is_fuera_cierre = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    fecha_transaccion = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.fecha_compra} {self.fecha_transaccion}, {self.monto}, {self.is_fuera_cierre}'


class Presrubro(Common):
    desc = models.CharField(max_length=50)
    tipo_movimiento = models.CharField(max_length=1, choices=base.choices.TipoMovimientoChoices.choices)

    def __str__(self) -> str:
        return self.desc


class Presconcepto(Common):
    desc = models.CharField(max_length=50, unique=True)
    presrubro = models.ForeignKey(Presrubro, on_delete=models.CASCADE)
    monto_defecto = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=1, choices=base.choices.MonedaChoices.get_choices(), default=base.choices.MonedaChoices.moneda_local)
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000)
    is_tarjeta = models.BooleanField(default=False)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.desc}'


class Presupuesto(Common):
    anio = models.CharField(max_length=4, choices=base.choices.CalendarChoices.year_choices)
    mes = models.CharField(max_length=2, choices=base.choices.CalendarChoices.month_choices)
    presconcepto = models.ForeignKey(Presconcepto, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=1, choices=base.choices.MonedaChoices.get_choices())
    tipo_cambio = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    monto_final = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.anio}-{self.mes} {self.presconcepto.desc} {self.monto_final}'
