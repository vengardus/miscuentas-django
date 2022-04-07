'''
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
__date__
'''
from django import forms
from django.utils.translation import gettext_lazy as _
#from django.core.exceptions import ValidationError
from base.models import Movimiento
from base.business.bcuenta import BCuenta
from base.business.bconceptodiario import BConceptoDiario

 
class MovimientoForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        oBCuenta = BCuenta()
        oBConceptoDiario = BConceptoDiario()
        self.fields['cuenta'].queryset = oBCuenta.get_all(request.user.license_id)
        self.fields['concepto_gasto'].queryset = oBConceptoDiario.get_all(request.user.license_id)
        self.fields['cuenta'].widget.attrs['autofocus'] = True

    class Meta:
        model = Movimiento
        fields = [  'cuenta', 'monto', 'tipo_movimiento', 'tipo_operacion',
                    'concepto_gasto', 'fecha_movimiento', 'obs',
                    
        ]
        widgets = {'id_movimiento': forms.HiddenInput()}
        error_messages = {
            'cuenta': {
                'unique': _("Ya existe rubro con esa descripción."),
            },
        }

    def clean(self):
        return super().clean()
    
    def clean_cuenta(self):
        data = self.cleaned_data['cuenta']
        print('gar', data)
        return data

    def clean_id_movimiento(self):
        data = 0
        # if Movimiento.objects.filter(desc=data).exists() :
        #     raise ValidationError("Descripción ya registrada!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        print('ed', data)
        return data