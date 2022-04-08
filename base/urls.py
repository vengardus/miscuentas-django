from django.urls import path
from base import views

from base.views import home_view
from base.views import login_view
# MIS CUENTAS
from base.views import banco_view, cuenta_view, cambiomoneda_view, movimiento_view
from base.api import banco_api, cuenta_api, cambiomoneda_api, movimiento_api
from base.views import rubrodiario_view, conceptodiario_view
from base.api import rubrodiario_api, conceptodiario_api
from base.views import pagosvarios_view, transferenciaspropias_view
from base.views import comercio_view, tarjeta_view, compra_view, estadocuenta_view
from base.api import comercio_api, tarjeta_api, compra_api
from base.views import presrubro_view, presconcepto_view, presupuesto_view
from base.api import presrubro_api, presconcepto_api, presupuesto_api

urlpatterns = [
    # path('', home_view.main, name='main'),
    path('', cuenta_view.cuenta_list, name='main'),
    path('login/', login_view.login_app, name='login'),
    path('logout/', login_view.logout_app, name='logout'),
    path('account/', login_view.account, name='account'),
    path('register/', login_view.registerUser, name='register'),
    path('about/', login_view.about, name='about'),


    # MIS CUENTAS   
    path('banco_controller/', banco_api.banco_controller, name='banco_controller'),
    path('banco_list/', banco_view.banco_list, name='banco_list'),
    path('banco_form/<str:mode>/<str:id>/', banco_view.banco_form, name='banco_form'),
    
    path('rubrodiario_controller/', rubrodiario_api.rubrodiario_controller, name='rubrodiario_controller'),
    path('rubrodiario_list/', rubrodiario_view.rubrodiario_list, name='rubrodiario_list'),
    path('rubrodiario_form/<str:mode>/<str:id>/', rubrodiario_view.rubrodiario_form, name='rubrodiario_form'),
    
    path('conceptodiario_controller/', conceptodiario_api.conceptodiario_controller, name='conceptodiario_controller'),
    path('conceptodiario_list/', conceptodiario_view.conceptodiario_list, name='conceptodiario_list'),
    path('conceptodiario_form/<str:mode>/<str:id>/', conceptodiario_view.conceptodiario_form, name='conceptodiario_form'),

    path('cuenta_controller/', cuenta_api.cuenta_controller, name='cuenta_controller'),
    path('cuenta_list/', cuenta_view.cuenta_list, name='cuenta_list'),
    path('cuenta_form/<str:mode>/<str:id>/', cuenta_view.cuenta_form, name='cuenta_form'),
    
    path('cambiomoneda_controller/', cambiomoneda_api.cambiomoneda_controller, name='cambiomoneda_controller'),
    path('cambiomoneda_list/', cambiomoneda_view.cambiomoneda_list, name='cambiomoneda_list'),
    path('cambiomoneda_form/<str:mode>/<str:id>/', cambiomoneda_view.cambiomoneda_form, name='cambiomoneda_form'),
    
    path('movimiento_controller/', movimiento_api.movimiento_controller, name='movimiento_controller'),
    path('movimiento_list/', movimiento_view.movimiento_list, name='movimiento_list'),
    path('movimiento_form/<str:mode>/<str:id>/', movimiento_view.movimiento_form, name='movimiento_form'),

    path('pagosvarios_form/', pagosvarios_view.pagosvarios_form, name='pagosvarios_form'),
    
    path('transferenciaspropias_form/', transferenciaspropias_view.transferenciaspropias_form, name='transferenciaspropias_form'),

    path('comercio_controller/', comercio_api.comercio_controller, name='comercio_controller'),
    path('comercio_list/', comercio_view.comercio_list, name='comercio_list'),
    path('comercio_form/<str:mode>/<str:id>/', comercio_view.comercio_form, name='comercio_form'),

    path('tarjeta_controller/', tarjeta_api.tarjeta_controller, name='tarjeta_controller'),
    path('tarjeta_list/', tarjeta_view.tarjeta_list, name='tarjeta_list'),
    path('tarjeta_form/<str:mode>/<str:id>/', tarjeta_view.tarjeta_form, name='tarjeta_form'),
    
    path('compra_controller/', compra_api.compra_controller, name='compra_controller'),
    path('compra_list/', compra_view.compra_list, name='compra_list'),
    path('compra_form/<str:mode>/<str:id>/', compra_view.compra_form, name='compra_form'),

    path('estadocuenta_list/', estadocuenta_view.estadocuenta_list, name='estadocuenta_list'),

    path('presrubro_controller/', presrubro_api.presrubro_controller, name='presrubro_controller'),
    path('presrubro_list/', presrubro_view.presrubro_list, name='presrubro_list'),
    path('presrubro_form/<str:mode>/<str:id>/', presrubro_view.presrubro_form, name='presrubro_form'),
    
    path('presconcepto_controller/', presconcepto_api.presconcepto_controller, name='presconcepto_controller'),
    path('presconcepto_list/', presconcepto_view.presconcepto_list, name='presconcepto_list'),
    path('presconcepto_form/<str:mode>/<str:id>/', presconcepto_view.presconcepto_form, name='presconcepto_form'),

    path('presupuesto_controller/', presupuesto_api.presupuesto_controller, name='presupuesto_controller'),
    path('presupuesto_list/', presupuesto_view.presupuesto_list, name='presupuesto_list'),
    path('presupuesto_form/<str:mode>/<str:id>/', presupuesto_view.presupuesto_form, name='presupuesto_form'),

    path('genpresupuesto_form/', presupuesto_view.genpresupuesto_form, name='genpresupuesto_form'),
]

