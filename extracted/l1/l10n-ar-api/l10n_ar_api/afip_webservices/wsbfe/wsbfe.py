# -*- coding: utf-8 -*-
# Segun manual para el desarrollador version 28/12/2018
import certifi
from l10n_ar_api.afip_webservices import config
from zeep import Client, Transport, helpers
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from .error import AfipError
from .invoice import FiscalElectronicBondValidator

# Exclude DH ciphers to avoid "dh key too small" errors with AFIP servers
AFIP_CIPHERS = "DEFAULT:!DH"


class ApiHTTPAdapter(HTTPAdapter):
    """ An adapter to block DH ciphers which may not work for *.afip.gov.ar """

    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=AFIP_CIPHERS)
        context.load_verify_locations(certifi.where())
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)


class ApiTransport(Transport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session.mount('https://', ApiHTTPAdapter())


class ApiClient(Client):
    def __init__(self, *args, wsdl_cache=None, **kwargs):
        kwargs['transport'] = ApiTransport(operation_timeout=60, timeout=60, cache=wsdl_cache)
        super().__init__(*args, **kwargs)


class WsbfeInvoiceDetails(object):
    """
    Se encarga de asignar los detalles de una invoice en
    los factories de WSBFE.

    :param wsbfe: Objeto Wsbfe.
    :param invoice: Objeto ElectronicInvoice para tomar los detalles.
    :param pos: Numero de punto de venta.
    """

    def __init__(self, wsbfe, invoice, pos):
        self.wsbfe = wsbfe
        self.pos = pos
        self.invoice = invoice
        self.detail = None

    def get_details(self):
        """ Devuelve los detalles completos para esa factura """

        self._set_details()
        return self.detail

    def _set_details(self):
        """ Completa los detalles a enviar segun los datos del documento """

        last_document_req = self.wsbfe.get_last_number(self.pos, self.invoice.document_code)
        self.detail = self._get_document_request()
        self.detail.Id = self.wsbfe.get_last_id().BFEResultGet.Id + 1
        self.detail.Tipo_doc = self.invoice.customer_document_type
        self.detail.Nro_doc = self.invoice.customer_document_number
        self.detail.CondicionIVAReceptorId = self.invoice.customer_fiscal_position
        self.detail.Zona = self.invoice.zone_id
        self.detail.Tipo_cbte = self.invoice.document_code
        self.detail.Punto_vta = self.pos
        self.detail.Cbte_nro = last_document_req + 1
        self.detail.Imp_total = self.invoice.get_total_amount()
        self.detail.Imp_tot_conc = self.invoice.untaxed_amount
        self.detail.Imp_neto = self.invoice.taxed_amount
        self.detail.Impto_liq = self.invoice.pay_off_tax_amount
        self.detail.Impto_liq_rni = self.invoice.rni_pay_off_tax_amount
        self.detail.Imp_op_ex = self.invoice.exempt_amount
        self.detail.Imp_perc = self.invoice.reception_amount
        self.detail.Imp_iibb = self.invoice.iibb_amount
        self.detail.Imp_perc_mun = self.invoice.municipal_reception_amount
        self.detail.Imp_internos = self.invoice.internal_tax_amount
        self.detail.Imp_moneda_Id = self.invoice.mon_id
        self.detail.Imp_moneda_ctz = round(self.invoice.mon_cotiz, 6)
        self.detail.Fecha_cbte = self.invoice.document_date
        # Si el tipo de comprobante que está autorizando es MiPyMEs (FCE),
        # Tipo 201 - FACTURA DE CREDITO ELECTRONICA MiPyMEs (FCE) A
        # Tipo 206 - FACTURA DE CREDITO ELECTRONICA MiPyMEs (FCE) B
        # es obligatorio informar el campo Fecha_vto_pago
        if self.invoice.document_code in [201, 206]:
            self.detail.Fecha_vto_pago = self.invoice.payment_due_date
        self._set_items()
        self._set_optionals()
        self._set_associated_documents()

    def _serialize_item(self, item):
        return self._get_item()(
            Pro_codigo_ncm=item.codigo_prod_ncm,
            Pro_ds=item.description,
            Pro_qty=item.quantity,
            Pro_umed=item.measurement_unit,
            Pro_precio_uni=round(item.unit_price, 6),
            Imp_bonif=item.bonification,
            Imp_total=item.total_price,
            Iva_id=item.iva_id,
        )
    
    def _serialize_optional(self, optional):
        return self._get_optional()(
            Id=optional.optional_id,
            Valor=optional.value,
        )

    def _serialize_associated_document(self, associated_document):
        return self._get_associated_document()(
            Tipo_cbte=associated_document.document_type,
            Punto_vta=associated_document.point_of_sale,
            Cbte_nro=associated_document.number,
            Cuit=associated_document.cuit,
            Fecha_cbte=associated_document.document_date
        )

    def _set_items(self):
        if self.invoice.array_items:
            self.detail.Items = self._get_item_array()([
                self._serialize_item(item) for item in self.invoice.array_items
            ])
    
    def _set_associated_documents(self):
        if self.invoice.associated_documents:
            self.detail.CbtesAsoc = self._get_associated_document_array()([
                self._serialize_associated_document(associated) for associated in self.invoice.associated_documents
            ])

    def _set_optionals(self):
        if self.invoice.array_optionals:
            self.detail.Opcionales = self._get_optional_array()([
                self._serialize_optional(optional) for optional in self.invoice.array_optionals
            ])

    def _get_document_request(self):
        return self.wsbfe.client.type_factory('ns0').ClsBFERequest()

    def _get_item_array(self):
        return self.wsbfe.client.get_type('ns0:ArrayOfItem')

    def _get_item(self):
        return self.wsbfe.client.get_type('ns0:Item')
    
    def _get_associated_document_array(self):
        return self.wsbfe.client.get_type('ns0:ArrayOfCbteAsoc')

    def _get_optional_array(self):
        return self.wsbfe.client.get_type('ns0:ArrayOfOpcional')

    def _get_associated_document(self):
        return self.wsbfe.client.get_type('ns0:CbteAsoc')

    def _get_optional(self):
        return self.wsbfe.client.get_type('ns0:Opcional')


class Wsbfe(object):
    """
    Bono Fiscal Electrónico.

    :param access_token: AccessToken - Token de acceso
    :param cuit: Cuit de la empresa
    :param homologation: Homologacion si es True
    :param url: Url de servicios para Wsbfe
    """

    def __init__(self, access_token, cuit, homologation=True, url=None, wsdl_cache=None):

        if not url:
            self.url = config.service_urls.get('wsbfev1_homologation') if homologation \
                else config.service_urls.get('wsbfev1_production')
        else:
            self.url = url

        self.accessToken = access_token
        self.cuit = cuit
        self.client = ApiClient(self.url, wsdl_cache=wsdl_cache)
        self.auth_request = self._create_auth_request()

    def get_cae(self, invoices, pos):
        """
        :param invoices: Conjunto de Objetos FiscalElectronicBond, documentos a enviar a AFIP.
        :param pos: Numero de punto de venta.
        :returns str: Respuesta de AFIP sobre la validacion del documento.
        """

        # TODO: Ver como integramos el get_cae para ambos servicios
        self._validate_invoices(invoices)

        responses = []
        requests = []
        for invoice in invoices:
            request = self._create_cae_request(invoice, pos)
            response = self.client.service.BFEAuthorize(self.auth_request, request)
            responses.append(response)
            requests.append(request)
        return responses, requests

    def check_webservice_status(self):
        """
        Consulta el estado de los webservices de BFE de AFIP
        :raises Exception: Si alguno de los servidores esta caido
        """

        res = self.client.service.BFEDummy()
        if res.AppServer != 'OK':
            raise Exception('El servidor de aplicaciones no se encuentra disponible. Intente mas tarde.')
        if res.DbServer != 'OK':
            raise Exception('El servidor de base de datos no se encuentra disponible. Intente mas tarde.')
        if res.AuthServer != 'OK':
            raise Exception('El servidor de auntenticacion no se encuentra disponible. Intente mas tarde.')

        return res

    def get_last_number(self, pos_number, document_code):
        """ Recupera el ultimo comprobante autorizado """

        last_document_req = self._set_last_document(pos_number, document_code)
        request = self.client.service.BFEGetLast_CMP(last_document_req)

        self._check_for_errors(request)

        return request.BFEResult_LastCMP.Cbte_nro

    def get_last_id(self):
        """" Recupera el ultimo ID y su fecha """

        request = self.client.service.BFEGetLast_ID(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_measurement_units(self):
        """ Devuelve las unidades de medida y su codigo """

        request = self.client.service.BFEGetPARAM_UMed(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_currencies(self):
        """ Recupera el listado de monedas y su codigo utilizable """

        request = self.client.service.BFEGetPARAM_MON(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_document_codes(self):
        """ Recupera el listado de los tipos de comprobante y su codigo utilizables """

        request = self.client.service.BFEGetPARAM_Tipo_Cbte(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_product_types_ncm(self):
        """Recupera el listado de los tipos de productos según el Nomenclador Común del Sur"""

        request = self.client.service.BFEGetPARAM_NCM(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_zones_codes(self):
        """Recupera el listado de los códigos de zonas"""

        request = self.client.service.BFEGetPARAM_Zonas(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_iva_types(self):
        """Recupera el listado de los tipos de IVA y sus códigos utilizables"""

        request = self.client.service.BFEGetPARAM_Tipo_IVA(self.auth_request)
        self._check_for_errors(request)

        return request

    def _create_cae_request(self, invoice, pos):
        """
        :param invoice: FiscalElectronicBond.
        :param pos: Numero de punto de venta.
        :returns: BFERequest / Envio de documentos para recibir el CAE.
        """

        return WsbfeInvoiceDetails(self, invoice, pos).get_details()

    def _set_last_document(self, pos_number, document_code):
        ClsBFE_LastCMP = self.client.get_type('ns0:ClsBFE_LastCMP')

        last_document_req = ClsBFE_LastCMP(
            Token=self.auth_request.Token,
            Sign=self.auth_request.Sign,
            Cuit=self.auth_request.Cuit,
            Pto_venta=pos_number,
            Tipo_cbte=document_code
        )
        return last_document_req

    def show_error(self, response):
        if response.BFEErr.ErrMsg != 'OK':
            raise AfipError.parse_error(response)

    @staticmethod
    def _validate_invoices(invoices):
        invoiceValidator = FiscalElectronicBondValidator()
        for invoice in invoices:
            invoiceValidator.validate_invoice(invoice)

    @staticmethod
    def _check_for_errors(request):
        if request.BFEErr.ErrMsg != 'OK':
            raise AfipError.parse_error(request)

    def _create_auth_request(self):
        """ Setea el ClsBFEAuthRequest, necesario para utilizar el resto de los metodos """
        ClsBFEAuthRequest = self.client.get_type('ns0:ClsBFEAuthRequest')
        # ns0:ClsBFEAuthRequest(Token: xsd:string, Sign: xsd:string, Cuit: xsd:long)

        auth_request = ClsBFEAuthRequest(
            Token=self.accessToken.token,
            Sign=self.accessToken.sign,
            Cuit=self.cuit
        )
        return auth_request
    
    def retrieve_cae(self, document_type_number, inv_number, pos_number):
        """
        Consulta un bono fiscal previamente autorizado via BFEGetCMP.

        Siempre retorna una tupla (response_dict, request_dict). Si el comprobante no existe
        o hay error, la respuesta incluye 'BFEErr'. Si existe, incluye 'BFEResultGet' con los datos.

        :param document_type_number: Codigo de tipo de documento ARCA.
        :param inv_number: Numero de comprobante a consultar.
        :param pos_number: Numero de punto de venta.
        :return: Tupla (response_dict, request_dict).
        """
        Cmp = self.client.get_type('ns0:ClsFEXGetCMP')
        _Cmp = Cmp(
            Tipo_cbte=document_type_number,
            Cbte_nro=inv_number,
            Punto_vta=pos_number
        )

        cae_details = self.client.service.BFEGetCMP(
            Auth=self.auth_request,
            Cmp=_Cmp
        )
        if cae_details.BFEErr and cae_details.BFEErr.ErrMsg != 'OK':
            # Retornar respuesta serializada con error incluido para que el caller decida
            # (retrocompatible: antes el error checking estaba comentado)
            return helpers.serialize_object(cae_details), helpers.serialize_object(_Cmp)

        res = helpers.serialize_object(cae_details)
        req = helpers.serialize_object(_Cmp)
        return res, req
