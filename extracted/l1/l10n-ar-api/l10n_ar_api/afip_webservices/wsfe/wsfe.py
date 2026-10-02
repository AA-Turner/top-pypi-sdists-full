# -*- coding: utf-8 -*-
# Segun RG 2485 – Proyecto FE v2.8 - 12/09/2016

import certifi
from zeep import Client, Transport, helpers
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from .error import AfipError, AfipServiceError
from l10n_ar_api.afip_webservices import config
from .invoice import ElectronicInvoiceValidator

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


class WsfeInvoiceDetails(object):
    """
    Se encarga de asignar los detalles de una invoice en
    los factories de WSFE.

    :param client: Cliente / Webservice.
    :param invoice: Objeto ElectronicInvoice para tomar los detalles.
    :param last_invoice_number: Ultimo numero de comprobante.
    """

    def __init__(self, client, invoice, last_invoice_number):
        self.client = client
        self.invoice = invoice
        self.last_invoice_number = last_invoice_number
        self.detail = None

    def get_details(self):
        """ Devuelve los detalles completos para esa factura """

        self._set_details()

        return self.detail

    def _set_details(self):
        """ Completa los detalles a enviar segun los datos del documento """

        self.detail = self._get_detail()
        self.detail.Concepto = self.invoice.concept
        self.detail.DocTipo = self.invoice.customer_document_type
        self.detail.DocNro = self.invoice.customer_document_number
        self.detail.CondicionIVAReceptorId = self.invoice.customer_fiscal_position
        self.detail.CbteDesde = self.last_invoice_number+1
        self.detail.CbteHasta = self.last_invoice_number+1
        self.detail.CbteFch = self.invoice.document_date
        self.detail.ImpTotal = round(self.invoice.get_total_amount(), 2)
        self.detail.ImpTotConc = round(self.invoice.untaxed_amount, 2)
        self.detail.ImpNeto = round(self.invoice.taxed_amount, 2)
        self.detail.ImpOpEx = round(self.invoice.exempt_amount, 2)
        self.detail.ImpIVA = round(self.invoice.get_total_iva(), 2)
        self.detail.ImpTrib = round(self.invoice.get_total_tributes(), 2)
        if self.invoice.concept not in [2, 3]:
            self.detail.FchServDesde = ''
            self.detail.FchServHasta = ''
            # Si es factura de crédito hay que informar siempre fecha de vencimiento
            self.detail.FchVtoPago = '' if self.invoice.document_code not in [201, 206, 211] else self.invoice.payment_due_date
        else:
            self.detail.FchServDesde = self.invoice.service_from
            self.detail.FchServHasta = self.invoice.service_to
            # Para notas de crédito / débito FCE no hay que informar fecha de vencimiento de pago.
            self.detail.FchVtoPago = self.invoice.payment_due_date if self.invoice.document_code not in [202, 203, 207, 208, 212, 213] \
                else None
        self.detail.MonId = self.invoice.mon_id
        self.detail.MonCotiz = round(self.invoice.mon_cotiz, 6)
        self._set_iva()
        self._set_tributes()
        self._set_optionals()
        self._set_associated_documents()
        self._set_period()

    def _serialize_period(self, period_from, period_to):
        return self._get_period()(
            FchDesde=period_from,
            FchHasta=period_to
        )

    def _set_period(self):
        """ Agrega al detalle el periodo asociado """
        if self.invoice.period_from and self.invoice.period_to:
            self.detail.PeriodoAsoc = self._serialize_period(self.invoice.period_from, self.invoice.period_to)

    def _serialize_tribute(self, tribute):
        return self._get_tribute()(
            Id=tribute.document_code,
            BaseImp=round(tribute.taxable_base, 2),
            Alic=tribute.aliquot,
            Importe=round(tribute.amount, 2),
            Desc='Impuesto codigo {}'.format(tribute.document_code),
        )

    def _set_tributes(self):
        """ Agrega al detalle el array de tributos del documento """

        if self.invoice.array_tributes:
            self.detail.Tributos = self._get_tribute_array()([
                self._serialize_tribute(tribute) for tribute in self.invoice.array_tributes
            ])

    def _serialize_iva(self, iva):
        return self._get_iva()(
            Id=iva.document_code,
            BaseImp=round(iva.taxable_base, 2),
            Importe=round(iva.amount, 2)
        )

    def _serialize_optional(self, optional):
        return self._get_optional()(
            Id=optional.optional_id,
            Valor=optional.value,
        )

    def _serialize_associated_document(self, associated_document):
        return self._get_associated_document()(
            Tipo=associated_document.document_type,
            PtoVta=associated_document.point_of_sale,
            Nro=associated_document.number,
            Cuit=associated_document.cuit,
            CbteFch=associated_document.document_date
        )

    def _set_iva(self):
        """ Agrega al detalle el array de iva del documento """

        if self.invoice.array_iva:
            self.detail.Iva = self._get_iva_array()([
                self._serialize_iva(iva) for iva in self.invoice.array_iva
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

    def _get_detail(self):
        return self.client.type_factory('ns0').FECAEDetRequest()

    def _get_associated_document_array(self):
        return self.client.get_type('ns0:ArrayOfCbteAsoc')

    def _get_optional_array(self):
        return self.client.get_type('ns0:ArrayOfOpcional')

    def _get_associated_document(self):
        return self.client.get_type('ns0:CbteAsoc')

    def _get_optional(self):
        return self.client.get_type('ns0:Opcional')

    def _get_iva(self):
        return self.client.get_type('ns0:AlicIva')

    def _get_iva_array(self):
        return self.client.get_type('ns0:ArrayOfAlicIva')

    def _get_tribute(self):
        return self.client.get_type('ns0:Tributo')

    def _get_tribute_array(self):
        return self.client.get_type('ns0:ArrayOfTributo')

    def _get_period(self):
        return self.client.get_type('ns0:Periodo')


class WsfeOptional(object):

    def __init__(self, optional_id, value):
        self.optional_id = optional_id
        self.value = value


class WsfeAssociatedDocument(object):

    def __init__(self, document_type, point_of_sale, number, cuit, document_date):
        self.document_type = document_type
        self.point_of_sale = point_of_sale
        self.number = number
        self.cuit = cuit
        self._document_date = None
        self.document_date = document_date

    def _parse_date(self, value):
        return value.strftime('%Y%m%d')

    @property
    def document_date(self):
        return self._document_date

    @document_date.setter
    def document_date(self, value):
        self._document_date = self._parse_date(value)


class Wsfe(object):
    """
    Factura electronica.

    :param access_token: AccessToken - Token de acceso
    :param cuit: Cuit de la empresa
    :param homologation: Homologacion si es True
    :param url: Url de servicios para Wsfe
    """

    def __init__(self, access_token, cuit, homologation=True, url=None, wsdl_cache=None):
        if not url:
            self.url = config.service_urls.get('wsfev1_homologation') if homologation\
                else config.service_urls.get('wsfev1_production')
        else:
            self.url = url

        self.accessToken = access_token
        self.cuit = cuit
        self.client = ApiClient(self.url, wsdl_cache=wsdl_cache)
        self.auth_request = self._create_auth_request()

    def check_webservice_status(self):
        """ Consulta el estado de los webservices de AFIP."""

        res = self.client.service.FEDummy()

        if hasattr(res, 'Errors'):
            raise AfipError.parse_error(res)
        if res.AppServer != 'OK':
            raise Exception('El servidor de aplicaciones no se encuentra disponible. Intente mas tarde.')
        if res.DbServer != 'OK':
            raise Exception('El servidor de base de datos no se encuentra disponible. Intente mas tarde.')
        if res.AuthServer != 'OK':
            raise Exception('El servidor de auntenticacion no se encuentra disponible. Intente mas tarde.')

    def get_cae(self, invoices, pos, last_invoice_override=None):
        """
        :param invoices: Conjunto de Objetos ElectronicInvoice, documentos a enviar a AFIP.
        :param pos: Numero de punto de venta.
        :param last_invoice_override: Ultimo numero autorizado (opcional, evita consulta redundante).
        :returns str: Respuesta de AFIP sobre la validacion del documento.
        """

        self._validate_invoices(invoices)
        FECAERequest = self._set_FECAERequest(invoices, pos, last_invoice_override)
        # FECAESolicitar(Auth: ns0:FEAuthRequest, FeCAEReq: ns0:FECAERequest) ->
        # FECAESolicitarResult: ns0:FECAEResponse
        return self.client.service.FECAESolicitar(
            Auth=self.auth_request,
            FeCAEReq=FECAERequest
        ), FECAERequest

    def get_cotization(self, currency):
        """
        :param currency: Id de la moneda consultar
        :return: Cotización de la moneda para el día de hoy.
        """
        cotiz_response = self.client.service.FEParamGetCotizacion(
            Auth=self.auth_request,
            MonId=currency,
        )
        if cotiz_response.Errors:
            raise AfipError().parse_error(cotiz_response)

        return cotiz_response.ResultGet.MonCotiz

    def show_error(self, response):
        if response.Errors:
            raise AfipError.parse_error(response)

    def get_last_number(self, pos_number, document_type_number):
        """
        :param pos_number: Numero de punto de venta
        :param document_type_number: Numero del tipo de documento segun AFIP a consultar
        :return: Numero de ultimo comprobante autorizado para ese tipo
        """

        # FECompUltimoAutorizado(Auth: ns0:FEAuthRequest, PtoVta: xsd:int, CbteTipo: xsd:int) ->
        # FECompUltimoAutorizadoResult: ns0:FERecuperaLastCbteResponse

        last_number_response = self.client.service.FECompUltimoAutorizado(
            Auth=self.auth_request,
            PtoVta=pos_number,
            CbteTipo=document_type_number,
        )
        if last_number_response.Errors:
            raise AfipError().parse_error(last_number_response)

        return last_number_response.CbteNro

    def get_max_batch_size(self):
        """
        Consulta a ARCA la cantidad maxima de registros permitidos por request de FECAESolicitar.
        :return: int, cantidad maxima de registros por request.
        """
        result = self.client.service.FECompTotXRequest(Auth=self.auth_request)
        if result.Errors:
            raise AfipError.parse_error(result)
        return result.RegXReq

    # Codigos de comprobantes FCE (MiPyMEs) que permiten maximo 1 por request
    FCE_DOCUMENT_CODES = {201, 202, 203, 206, 207, 208, 211, 212, 213}

    def get_cae_batched(self, invoices, pos, last_invoice_number=None):
        """
        Envia facturas en lotes (chunks) a ARCA, respetando el limite de FECompTotXRequest.

        Particiona las facturas en chunks del tamaño maximo permitido por ARCA.
        Para comprobantes FCE (MiPyMEs, codigos 201-213) el limite es 1 por request.

        La numeracion es secuencial entre chunks: el primer chunk arranca en
        last_invoice_number+1 y cada chunk posterior continua donde termino el anterior.

        Retorna una lista de tuplas donde cada tupla contiene:
        - response: Respuesta SOAP de FECAESolicitar (con FECAEDetResponse por cada factura)
        - request: Request SOAP enviado (FECAERequest)
        - indices: Lista de indices originales de las facturas en este chunk,
          para poder mapear cada FECAEDetResponse[i] a invoices[indices[i]]

        :param invoices: Lista de objetos ElectronicInvoice (todos del mismo tipo).
        :param pos: Numero de punto de venta.
        :param last_invoice_number: Ultimo numero autorizado (opcional, evita llamada a FECompUltimoAutorizado).
        :returns: Lista de tuplas (response, request, indices_originales).
        """
        self._validate_invoices(invoices)

        if not invoices:
            return []

        max_batch = self.get_max_batch_size()
        doc_code = self._get_document_type(invoices)

        # FCE: maximo 1 comprobante por request
        if doc_code in self.FCE_DOCUMENT_CODES:
            max_batch = 1

        if last_invoice_number is None:
            last_invoice_number = self.get_last_number(pos, doc_code)

        results = []
        for chunk_start in range(0, len(invoices), max_batch):
            chunk = invoices[chunk_start:chunk_start + max_batch]
            indices = list(range(chunk_start, chunk_start + len(chunk)))

            FECAERequest = self._set_FECAERequest(chunk, pos, last_invoice_number)
            response = self.client.service.FECAESolicitar(
                Auth=self.auth_request,
                FeCAEReq=FECAERequest
            )
            results.append((response, FECAERequest, indices))

            # Avanzar numeracion para el proximo chunk
            last_invoice_number += len(chunk)

        return results

    def _validate_invoices(self, invoices):
        """
        Valida que los campos de la factura electronica sean validos

        :param invoices: Lista de Objetos Invoice, documentos a validar.
        """

        invoiceValidator = ElectronicInvoiceValidator()
        for invoice in invoices:
            invoiceValidator.validate_invoice(invoice)

    def _get_header(self):
        return self.client.get_type('ns0:FECAECabRequest')

    def _get_cae_request(self):
        return self.client.get_type('ns0:FECAERequest')

    def _get_array_cae_request(self):
        return self.client.get_type('ns0:ArrayOfFECAEDetRequest')

    def _get_document_type(self, invoices):
        """Obtiene el codigo de tipo de documento, validando que todas las facturas sean del mismo tipo."""
        document_types = set([invoice.document_code for invoice in invoices])
        if len(document_types) > 1:
            raise AttributeError("Los documentos a enviar deben ser del mismo tipo")

        return next(iter(document_types))

    def _set_FECAERequest(self, invoices, pos, last_invoice_override=None):
        """
        :param invoices: Conjunto de objetos ElectronicInvoice.
        :param pos: Numero de punto de venta.
        :param last_invoice_override: Ultimo numero autorizado (opcional, evita consulta redundante).
        :returns: FECAERequest / Envio de documentos para recibir el CAE.
        """

        header = self._set_header(invoices, pos)
        array_cae_request = self._get_array_cae_request()

        details = []
        last_invoice = last_invoice_override if last_invoice_override is not None \
            else self.get_last_number(header.PtoVta, header.CbteTipo)

        for invoice in invoices:
            details.append(WsfeInvoiceDetails(self.client, invoice, last_invoice).get_details())
            last_invoice += 1

        cae_request = self._get_cae_request()

        # ns0:FECAERequest(FeCabReq: ns0:FECAECabRequest, FeDetReq: ns0:ArrayOfFECAEDetRequest)
        FECAERequest = cae_request(
            FeCabReq=header,
            FeDetReq=array_cae_request(details)
        )

        return FECAERequest

    def _set_header(self, invoices, pos):
        """
        :param invoices: Conjunto de Objetos ElectronicInvoice.
        :param pos: Numero de punto de venta.
        :returns: FeCabReq / cabecera de envio de documentos completo.
        """

        header_request = self._get_header()
        # ns0:FECAECabRequest(CantReg: xsd:int, PtoVta: xsd:int, CbteTipo: xsd:int)
        header = header_request(
            CantReg=len(invoices),
            PtoVta=pos,
            CbteTipo=self._get_document_type(invoices)
        )

        return header

    def _create_auth_request(self):
        """ Setea el FEAuthRequest, necesario para utilizar el resto de los metodos """
        FEAuthRequest = self.client.get_type('ns0:FEAuthRequest')
        # ns0:FEAuthRequest(Token: xsd:string, Sign: xsd:string, Cuit: xsd:long)
        auth_request = FEAuthRequest(
            Token=self.accessToken.token,
            Sign=self.accessToken.sign,
            Cuit=self.cuit
        )
        return auth_request

    def retrieve_cae(self, document_type_number, inv_number, pos_number):
        """
        Consulta un comprobante previamente autorizado en ARCA via FECompConsultar.

        Se usa para:
        - Recuperar CAEs ante errores de comunicacion (la factura fue autorizada pero se perdio la respuesta)
        - Verificar el estado de un comprobante desde el wizard de recupero

        Siempre retorna una tupla (response_dict, request_dict). Si el comprobante no existe
        (error 602) o hay otro error, la respuesta incluye el campo 'Errors' para que el caller
        lo maneje. Si el comprobante existe, la respuesta incluye 'ResultGet' con los datos.

        :param document_type_number: Codigo de tipo de documento ARCA (ej: '001').
        :param inv_number: Numero de comprobante a consultar.
        :param pos_number: Numero de punto de venta.
        :return: Tupla (response_dict, request_dict). response_dict tiene 'ResultGet' o 'Errors'.
        """
        FeCompConsReq = self.client.get_type('ns0:FECompConsultaReq')
        _FeCompConsReq = FeCompConsReq(
            CbteTipo=document_type_number,
            CbteNro=inv_number,
            PtoVta=pos_number
        )

        cae_details = self.client.service.FECompConsultar(
            Auth=self.auth_request,
            FeCompConsReq=_FeCompConsReq
        )
        if cae_details.Errors:
            # Retornar respuesta serializada con Errors incluido para que el caller decida
            # (retrocompatible: antes el error checking estaba comentado)
            return helpers.serialize_object(cae_details), helpers.serialize_object(_FeCompConsReq)

        res = helpers.serialize_object(cae_details)
        req = helpers.serialize_object(_FeCompConsReq)
        return res, req

