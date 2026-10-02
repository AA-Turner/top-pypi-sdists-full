# -*- coding: utf-8 -*-
# Segun manual para el desarrollador version 30/09/2014
import certifi
from l10n_ar_api.afip_webservices import config
from zeep import Client, Transport, helpers
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from .error import AfipError
from .invoice import ExportationElectronicInvoiceValidator

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


class WsfexInvoiceDetails(object):
    """
    Se encarga de asignar los detalles de una invoice en
    los factories de WSFEX.

    :param wsfex: Objeto Wsfex.
    :param invoice: Objeto ElectronicInvoice para tomar los detalles.
    :param pos: Numero de punto de venta.
    """

    def __init__(self, wsfex, invoice, pos):
        self.wsfex = wsfex
        self.pos = pos
        self.invoice = invoice
        self.detail = None

    def get_details(self):
        """ Devuelve los detalles completos para esa factura """

        self._set_details()
        return self.detail

    def _set_details(self):
        """ Completa los detalles a enviar segun los datos del documento """

        last_document_req = self.wsfex.get_last_number(self.pos, self.invoice.document_code)
        self.detail = self._get_document_request()
        self.detail.Id = self.wsfex.get_last_id().FEXResultGet.Id + 1
        self.detail.Cbte_Tipo = self.invoice.document_code
        self.detail.Fecha_cbte = self.invoice.document_date
        # Se cheque que el document_code sea 19 para saber que es una factura de exportacion y no sea ND expo ni NC expo
        if self.invoice.document_code == 19 and self.invoice.exportation_type in [2, 4]:
            self.detail.Fecha_pago = self.invoice.payment_due_date or self.invoice.document_date

        self.detail.Punto_vta = self.pos
        self.detail.Cbte_nro = last_document_req + 1
        self.detail.Tipo_expo = self.invoice.exportation_type
        self.detail.Permiso_existente = self.invoice.existent_permission
        self.detail.Dst_cmp = self.invoice.destiny_country
        self.detail.Cliente = self.invoice.customer_name
        self.detail.Cuit_pais_cliente = self.invoice.destiny_country_cuit
        self.detail.Domicilio_cliente = self.invoice.customer_street
        self.detail.Moneda_Id = self.invoice.mon_id
        self.detail.Moneda_ctz = round(self.invoice.mon_cotiz, 6)
        self.detail.Imp_total = self.invoice.get_total_amount()
        self.detail.Idioma_cbte = self.invoice.document_language
        self.detail.Incoterms = self.invoice.incoterms
        if self.invoice.tax_id:
            self.detail.Id_impositivo = self.invoice.tax_id
        self._set_associated_documents()
        self._set_items()

    def _serialize_item(self, item):
        return self._get_item()(
            Pro_ds=item.description,
            Pro_qty=item.quantity,
            Pro_umed=item.measurement_unit,
            Pro_precio_uni=round(item.unit_price, 6),
            Pro_total_item=round(item.total_price, 2),
            Pro_bonificacion=round(item.bonification, 2)
        )

    def _serialize_associated_document(self, associated_document):
        return self._get_associated_document()(
            Cbte_tipo=associated_document.document_type,
            Cbte_punto_vta=associated_document.point_of_sale,
            Cbte_nro=associated_document.number,
            Cbte_cuit=associated_document.cuit,
        )

    def _set_items(self):
        if self.invoice.array_items:
            self.detail.Items = self._get_item_array()([
                self._serialize_item(item) for item in self.invoice.array_items
            ])

    def _set_associated_documents(self):
        if self.invoice.associated_documents:
            self.detail.Cmps_asoc = self._get_associated_document_array()([
                self._serialize_associated_document(associated) for associated in self.invoice.associated_documents
            ])

    def _get_associated_document_array(self):
        return self.wsfex.client.get_type('ns0:ArrayOfCmp_asoc')

    def _get_document_request(self):
        return self.wsfex.client.type_factory('ns0').ClsFEXRequest()

    def _get_item_array(self):
        return self.wsfex.client.get_type('ns0:ArrayOfItem')

    def _get_item(self):
        return self.wsfex.client.get_type('ns0:Item')

    def _get_associated_document(self):
        return self.wsfex.client.get_type('ns0:Cmp_asoc')


class Wsfex(object):
    """
    Factura electronica de exportacion.

    :param access_token: AccessToken - Token de acceso
    :param cuit: Cuit de la empresa
    :param homologation: Homologacion si es True
    :param url: Url de servicios para Wsfe
    """

    def __init__(self, access_token, cuit, homologation=True, url=None, wsdl_cache=None):

        if not url:
            self.url = config.service_urls.get('wsfexv1_homologation') if homologation \
                else config.service_urls.get('wsfexv1_production')
        else:
            self.url = url

        self.accessToken = access_token
        self.cuit = cuit
        self.client = ApiClient(self.url, wsdl_cache=wsdl_cache)
        self.auth_request = self._create_auth_request()

    def get_cae(self, invoices, pos):
        """
        :param invoices: Conjunto de Objetos ExportationElectronicInvoice, documentos a enviar a AFIP.
        :param pos: Numero de punto de venta.
        :returns str: Respuesta de AFIP sobre la validacion del documento.
        """

        # TODO: Ver como integramos el get_cae para ambos servicios
        self._validate_invoices(invoices)

        responses = []
        requests = []
        for invoice in invoices:
            request = self._create_cae_request(invoice, pos)
            response = self.client.service.FEXAuthorize(self.auth_request, request)
            self._check_for_errors(response)
            responses.append(response)
            requests.append(request)

        return responses, requests

    def check_webservice_status(self):
        """
        Consulta el estado de los webservices de FEX de AFIP
        :raises Exception: Si alguno de los servidores esta caido
        """

        res = self.client.service.FEXDummy()
        if res.AppServer != 'OK':
            raise Exception('El servidor de aplicaciones no se encuentra disponible. Intente mas tarde.')
        if res.DbServer != 'OK':
            raise Exception('El servidor de base de datos no se encuentra disponible. Intente mas tarde.')
        if res.AuthServer != 'OK':
            raise Exception('El servidor de auntenticacion no se encuentra disponible. Intente mas tarde.')

        return res

    def get_last_number(self, pos_number, document_type_number):
        """ Recupera el ultimo comprobante autorizado """

        last_document_req = self._set_last_document(pos_number, document_type_number)
        request = self.client.service.FEXGetLast_CMP(last_document_req)

        self._check_for_errors(request)

        return request.FEXResult_LastCMP.Cbte_nro

    def get_last_id(self):
        """" Recupera el ultimo ID y su fecha """

        request = self.client.service.FEXGetLast_ID(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_exportation_types(self):
        """ Recupera el listado de los tipos de exportacion y sus codigos """

        request = self.client.service.FEXGetPARAM_Tipo_Expo(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_measurement_units(self):
        """ Devuelve las unidades de medida y su codigo """

        request = self.client.service.FEXGetPARAM_UMed(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_point_of_sales(self):
        """ Recupera el listado de los puntos de venta registrados para fex """

        request = self.client.service.FEXGetPARAM_PtoVenta(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_currencies(self):
        """ Recupera el listado de monedas y su codigo utilizable """

        request = self.client.service.FEXGetPARAM_MON(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_incoterms(self):
        """ Recupera el listado Incoterms utilizables """

        request = self.client.service.FEXGetPARAM_Incoterms(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_languages(self):
        """ Recupera el listado de los idiomas y sus codigos utilizables """

        request = self.client.service.FEXGetPARAM_Idiomas(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_countries(self):
        """ Recupera el listado de paises """

        request = self.client.service.FEXGetPARAM_DST_pais(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_countries_cuit(self):
        """ Recupera el listado CUIT de los paises """

        request = self.client.service.FEXGetPARAM_DST_CUIT(self.auth_request)
        self._check_for_errors(request)

        return request

    def get_currency_value(self, currency):
        """ Recupera la cotizacion de la moneda consultada """

        request = self.client.service.FEXGetPARAM_Ctz(self.auth_request, currency)
        self._check_for_errors(request)

        return request

    def get_document_codes(self):
        """ Recupera el listado de los tipos de comprobante y su codigo utilizables """

        request = self.client.service.FEXGetPARAM_Cbte_Tipo(self.auth_request)
        self._check_for_errors(request)

        return request

    def _create_cae_request(self, invoice, pos):
        """
        :param invoice: ExportationElectronicInvoice.
        :param pos: Numero de punto de venta.
        :returns: FECAERequest / Envio de documentos para recibir el CAE.
        """

        return WsfexInvoiceDetails(self, invoice, pos).get_details()

    def _set_last_document(self, pos_number, document_type_number):
        ClsFEX_LastCMP = self.client.get_type('ns0:ClsFEX_LastCMP')

        last_document_req = ClsFEX_LastCMP(
            Token=self.auth_request.Token,
            Sign=self.auth_request.Sign,
            Cuit=self.auth_request.Cuit,
            Pto_venta=pos_number,
            Cbte_Tipo=document_type_number
        )
        return last_document_req

    def show_error(self, response):
        if response.FEXErr.ErrMsg != 'OK':
            raise AfipError.parse_error(response)

    @staticmethod
    def _validate_invoices(invoices):
        invoiceValidator = ExportationElectronicInvoiceValidator()
        for invoice in invoices:
            invoiceValidator.validate_invoice(invoice)

    @staticmethod
    def _check_for_errors(request):
        if request.FEXErr.ErrMsg != 'OK':
            raise AfipError().parse_error(request)

    def _create_auth_request(self):
        """ Setea el ClsFEXAuthRequest, necesario para utilizar el resto de los metodos """
        ClsFEXAuthRequest = self.client.get_type('ns0:ClsFEXAuthRequest')
        # ns0:ClsFEXAuthRequest(Token: xsd:string, Sign: xsd:string, Cuit: xsd:long)

        auth_request = ClsFEXAuthRequest(
            Token=self.accessToken.token,
            Sign=self.accessToken.sign,
            Cuit=self.cuit
        )
        return auth_request
    
    def retrieve_cae(self, document_type_number, inv_number, pos_number):
        """
        Consulta un comprobante de exportacion previamente autorizado via FEXGetCMP.

        Siempre retorna una tupla (response_dict, request_dict). Si el comprobante no existe
        o hay error, la respuesta incluye 'FEXErr'. Si existe, incluye 'FEXResultGet' con los datos.

        :param document_type_number: Codigo de tipo de documento ARCA.
        :param inv_number: Numero de comprobante a consultar.
        :param pos_number: Numero de punto de venta.
        :return: Tupla (response_dict, request_dict).
        """
        Cmp = self.client.get_type('ns0:ClsFEXGetCMP')
        _Cmp = Cmp(
            Cbte_tipo=document_type_number,
            Cbte_nro=inv_number,
            Punto_vta=pos_number
        )

        cae_details = self.client.service.FEXGetCMP(
            Auth=self.auth_request,
            Cmp=_Cmp
        )
        if cae_details.FEXErr and cae_details.FEXErr.ErrMsg != 'OK':
            # Retornar respuesta serializada con error incluido para que el caller decida
            # (retrocompatible: antes el error checking estaba comentado)
            return helpers.serialize_object(cae_details), helpers.serialize_object(_Cmp)

        res = helpers.serialize_object(cae_details)
        req = helpers.serialize_object(_Cmp)
        return res, req


class WsfexAssociatedDocument(object):

    def __init__(self, document_type, point_of_sale, number, cuit):
        self.document_type = document_type
        self.point_of_sale = point_of_sale
        self.number = number
        self.cuit = cuit
