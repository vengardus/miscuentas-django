'''
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
__date__
'''
from datetime import datetime
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from base.choices import MonedaChoices
from base.models import ConceptoDiario, Cuenta, Movimiento

 
class PagosVariosForm(forms.ModelForm):
    
    def __init__(self, request, *args, **kwargs):
        self.request = request
        print(self.request.user.license_id)
        super().__init__(*args, **kwargs)
        self.fields['concepto_gasto'].queryset = ConceptoDiario.objects.filter(rubro_diario__is_servicio=True)
        self.fields['cuenta'].queryset = Cuenta.objects.filter(moneda=MonedaChoices.moneda_local).order_by('desc')
        self.set_data()

    def set_data(self):
        self.fields['cuenta'].widget.attrs['autofocus'] = True
        print(datetime.now())

    
    class Meta:
        model = Movimiento
        fields = [  'concepto_gasto', 'monto', 'cuenta', 'fecha_movimiento', 
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
        
        return super().clean()
    