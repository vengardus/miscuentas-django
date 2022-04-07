'''
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
__date__
'''
from datetime import date, datetime
from email.policy import default
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from base.business.bcuenta import BCuenta
from base.choices import MonedaChoices
from base.models import ConceptoDiario, Cuenta, Movimiento

 
class TransferenciasPropiasForm(forms.Form):
    
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        #self.fields['concepto_gasto'].queryset = ConceptoDiario.objects.filter(rubro_diario__is_servicio=True)
        #self.fields['cuenta'].queryset = Cuenta.objects.filter(moneda=MonedaChoices.moneda_local).order_by('desc')
        self.set_data()

    def set_data(self):
        oBCuenta = BCuenta()
        CuentasChoices = oBCuenta.get_all_choices(self.request.user.license_id)
        self.fields['cuenta_origen'] = forms.ChoiceField(choices=CuentasChoices)
        self.fields['monto'] = forms.DecimalField(max_digits=10, decimal_places=2)
        self.fields['cuenta_destino'] = forms.ChoiceField(choices=CuentasChoices)
        self.fields['fecha_movimiento'] = forms.DateField(initial=datetime.now())
        self.fields['obs'] = forms.CharField(max_length=50, required=False)
        # self.fields['cuenta_origen'].widget.attrs['autofocus'] = True

    
    class Meta:
        model = Movimiento
        fields = [  'cuenta_origen', 'monto', 'cuenta_destino', 'fecha_movimiento', 
                    'obs',
        ]
        widgets = {
                'fecha_movimiento': forms.DateInput(format='%Y-%m-%d', attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'autocomplete': 'off',
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'data-target': '#date_joined',
                'data-toggle': 'datetimepicker'
            })


        }
        
        # error_messages = {
        #     'desc': {
        #         'unique': _("Ya existe rubro con esa descripción."),
        #     },
        # }

    def clean(self):

        if self.cleaned_data['monto'] <= 0:
            raise ValidationError("Monto a cambiar debe ser mayor a 0")
        
        if self.cleaned_data['cuenta_origen'] == self.cleaned_data['cuenta_destino']:
            raise ValidationError('Cuentas deben ser distintas')
        return super().clean()
    