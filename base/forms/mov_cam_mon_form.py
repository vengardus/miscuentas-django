from django import forms
from base.business.bcuenta import BCuenta

class MovCamMonForm(forms.Form):
    oBCuenta = BCuenta()
    CuentasMonExtranjeraChoices = oBCuenta.get_cuentas_mon_extranjera_choices()
    cuenta_origen = forms.ChoiceField(choices=CuentasMonExtranjeraChoices)
