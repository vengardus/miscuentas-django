/* 
created by edgard.ramos (ismytv@gmail.com)
generated by alice.bash.v.2203a
sáb 26 mar 2022 12:50:53 -05
*/

let g_aDataTable = []
let g_oForm = Object;
let g_oDatagrid = Object;
let g_oModalDialog = Object;
let controller_name = '/presupuesto_controller/'

// GLOBALES PERSONALIZADAS
// ----------------------- 
let g_msg = {
    'delete' : 'Desea eliminar producto con id='
}

class FormApp extends Form {
    static FORM = {
        fields : {
            filter_input : 'filter_input',
            filter_clear : 'filter_clear',
            filter_search : 'filter_search',
            // fields personalizados
        }
    }

    constructor(aModal) {
        super(aModal);
    }
    
    set_events_form() {
        document.querySelector(`#${FormApp.FORM.fields.filter_input}`).addEventListener(g_events.event_onkeyup, (e) => {
            console.log(e.key)
            this.controller(Lib.actions.action_events_form, e.target.id, e.type, e.key)
        });
        document.querySelector(`#${FormApp.FORM.fields.filter_clear}`).addEventListener(g_events.event_onclick, (e) => {
            this.controller(Lib.actions.action_events_form, e.target.id, e.type)
        });
        document.querySelector(`#${FormApp.FORM.fields.filter_search}`).addEventListener(g_events.event_onclick, (e) => {
            this.controller(Lib.actions.action_events_form, e.target.id, e.type)
        });
    }

    init_data() {
        let data = {
            action: 'action_refresh',
            show_grid_header: true
        }
        let oController = new Controller(`${controller_name}`, data, action_refresh);
        oController.fetch_action();

        this.init_modal_dialog();
    }

    init_modal_dialog() {
        let aOption = [
            { option:'cancel', text:'Cancelar', classname:''},
            { option:'ok', text:'Continuar', classname:''}
        ]
        g_oModalDialog = new ModalDialog('modal_dialog', aOption, '');
    }

    action_events_form(element_id, event_id, event_key) {
        switch (element_id) {
            case FormApp.FORM.fields.filter_search:
                event_key = g_key.enter;

            case FormApp.FORM.fields.filter_input:
                if ( event_key == g_key.enter ) {
                    let str_filter = document.querySelector(`#${FormApp.FORM.fields.filter_input}`).value;
                    let aFilter = this.get_filter(str_filter);
                    g_oDatagrid.current_page = g_oDatagrid.current_page_ini = 1;
                    g_oDatagrid.refresh(aFilter, DataGrid.mode_refresh.filter);
                    calcula_presuesto();
                }
                break;
            
            case FormApp.FORM.fields.filter_clear:
                document.querySelector(`#${FormApp.FORM.fields.filter_input}`).value = '';
                g_oDatagrid.refresh(g_aDataTable, DataGrid.mode_refresh.filter);
                document.querySelector(`#${FormApp.FORM.fields.filter_input}`).focus();
                break;

            // logica eventos fields personalizados
        }
    }

    action_modal_open(parms) {
        let modal_id = parms[0];
        switch (modal_id) {
            case 'modal_dialog':
                let item_id = parms[1];
                g_oModalDialog.item_id = item_id;
                break;
        }
    }

    action_modal_close(modal_id) {
        console.log('Close modal', modal_id);
    }

    action_datagrid_action(datagrid_id, action_id, item_id) {
        console.log('ACTION_DATAGRID_ACTION', datagrid_id, action_id, item_id);
        switch (datagrid_id) {
            case 'datagrid':
                switch (action_id) {
                    case 'delete':
                        g_oModalDialog.text = `${g_msg['delete']} ${item_id}?`;
                        g_oModalDialog.set_text();
                        this.controller(Lib.actions.action_modal_open, 'modal_dialog', item_id);
                        break;
                    
                    case 'edit':
                        let data = {
                            action: 'action_edit',
                            id: item_id
                        }
                        let oController = new Controller(controller_name, data, action_edit);
                        oController.fetch_action();
                        break;
                }
                break;
        }
    }

    action_modal_dialog(modal_dialog_id, option) {
        switch (modal_dialog_id) {
            case 'modal_dialog':
                switch (option) {
                    case 'ok':
                        console.log('delete', g_oModalDialog.item_id);
                        let data = {
                            action: 'action_delete',
                            id: g_oModalDialog.item_id
                        }
                        let oController = new Controller(controller_name, data, action_delete);
                        oController.fetch_action();
                        this.controller(Lib.actions.action_modal_close, 'modal_dialog');
                        break;

                    case 'cancel':
                        this.controller(Lib.actions.action_modal_close, 'modal_dialog');
                        break;
                }
                break;
        }
    }

    /**
     * @function
     * Devuevle una lista filtrada de g_aDataTable
     * @param {*} filter {str}
     * @returns {*} {list of dict}
     */
    get_filter(filter) {
        return g_aDataTable.filter((table) => 
                    table.anio.toLowerCase().indexOf(filter.toLowerCase()) != -1
                ||  table.mes_glosa.toLowerCase().indexOf(filter.toLowerCase()) != -1
                ||  table.presconcepto_desc.toLowerCase().indexOf(filter.toLowerCase()) != -1
            );
    }

}

main();

function main() {
    g_oForm = new FormApp([{id:'modal_dialog', btn_cancel_id:''}])
    g_oForm.init();
    set_focus(`${FormApp.FORM.fields.filter_input}`);
}

function action_refresh(status, data) {
    if (status !== 200) {
        console.log(`Ocurrió un problema. Status code: ${status}`);
        return;
    }
    init_datagrid(data)
}

function action_edit(status, data) {
    if (status !== 200) {
        console.log(`Ocurrió un problema. Status code: ${status}`);
        return;
    }
    action_redirect(data['action_new']);
}

function action_delete(status, data) {
    if (status !== 200) {
        console.log(`Ocurrió un problema. Status code: ${status}`);
        return;
    }
    if ( data.status !== 200)
        action_redirect('');
    else {
        g_oDatagrid.aData = g_aDataTable = data.aDataTable;
        g_oDatagrid.refresh();
    }
}

function _datagrid_action(datagrid_id, action, item_id) {
    console.log('datagrid_action', datagrid_id, action, item_id);
    g_oForm.controller(Lib.actions.action_datagrid_action, datagrid_id, action, item_id);
}

function _action_modal_dialog(modal_dialog_id, option) {
    console.log('action_modal_dialog');
    g_oForm.controller(Lib.actions.action_modal_dialog, modal_dialog_id, option);
}


// FUNCIONALIDAD PERSONALIZADA
// ---------------------------
function init_datagrid(data) {
    g_aDataTable = data.aDataTable;
    g_stock_minimo = data.global_stock_minimo;
    g_oDatagrid = new DataGrid('datagrid',
        g_aDataTable,
        data.aHeader,
        get_data_columns
    );
    g_oDatagrid.refresh();
    calcula_presuesto();
}

function get_data_columns(item) {
    return [
        {
            data: is_type_screen(g_min_size_screen.desktop) ? item.mes_glosa : item.mes_glosa_abrev,
            class: ''
        },
        { data: item.tipo_movimiento_desc.substr(0,3), class: '' },
        { data: item.presconcepto_desc, class: '' },
        { data: (item.monto!=item.monto_final)? `${item.monto_final.toFixed(2)}*` : item.monto_final.toFixed(2), class: '' },
    ]
}

function calcula_presuesto() {
    console.log(g_oDatagrid.aData_current);
    let TIPO_INGRESO = "0";
    x = g_oDatagrid.aData_current.map((item)=> item.tipo_movimiento);
    aIngresos = g_oDatagrid.aData_current.filter((item) => 
        (item.tipo_movimiento == TIPO_INGRESO));
    aEgresos = g_oDatagrid.aData_current.filter((item) => 
        (item.tipo_movimiento != TIPO_INGRESO));

    let total_ingresos = aIngresos.reduce(
        (previous, current) => previous+ current.monto_final, 0.00);
    let total_egresos = aEgresos.reduce(
        (previous, current) => previous + current.monto_final, 0.00);
    let saldo = total_ingresos-total_egresos
    let danger = (saldo>0)? '' : 'danger'

    console.log(total_egresos)
    console.log(total_ingresos)
    
    document.querySelector(`#presupuesto_resumen`).innerHTML = 
            `<div class="resumen">`
            + `<div class="totales">`
            +       `<div class="row header">`
            +       ` <div class="glosa">Totales</div>`
            +       ` <div class="number">Monto S/.</div>`
            +       `</div>`
            
            +       `<div class="row">`
            +       ` <div class="glosa">Total Egresos</div>`
            +       ` <div class="number">${total_egresos.toFixed(2)}</div>`
            +       `</div>`

            +       `<div class="row">`
            +       ` <div class="glosa">Total Ingresos</div>`
            +       ` <div class="number">${total_ingresos.toFixed(2)}</div>`
            +       `</div>`

            +       `<div class="row">`
            +       ` <div class="glosa">Total Egresos</div>`
            +       ` <div class="number ${danger}">${saldo.toFixed(2)}</div>`
            +       `</div>`
            + `</div>`
            + `</div>`

}

/*
<div class="resumen">
        <div class="title">Estado de cuenta:</div>
        <div class="row header">
            <div class="glosa">Fecha de Pago</div>
            <div class="number">Monto S/.</div>
        </div>
        {% for item in data.aPagoMes %}
            <div class="row">
                <div class="glosa">{{item.fecha_pago}}</div>
                <div class="number">{{item.monto}}</div>
            </div>
        {% endfor %} 
    </div>
*/