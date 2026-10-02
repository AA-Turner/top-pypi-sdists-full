# -*- coding: utf-8 -*-
# WSMTXCA - Web Service de Factura Electronica con detalle (Matriz de datos)
# Segun RG 2904 / RG 3749 - ARCA (ex AFIP)

from datetime import datetime, date

from zeep import helpers

from .error import AfipError
from .invoice import ElectronicInvoiceValidator
from l10n_ar_api.afip_webservices import config
# Reutilizamos el cliente con el parche de ciphers DH para los servidores de ARCA
from l10n_ar_api.afip_webservices.wsfe.wsfe import ApiClient

# Namespace de los tipos del WSDL de WSMTXCA (notacion Clark para get_type)
NS = '{http://impl.service.wsmtxca.afip.gov.ar/service/}'


class WsmtxcaInvoiceDetails(object):
    """
    Arma el ComprobanteType (comprobanteCAERequest) de WSMTXCA a partir de un
    objeto MtxElectronicInvoice.

    :param client: Cliente zeep / Webservice.
    :param invoice: Objeto MtxElectronicInvoice con los datos del documento.
    :param invoice_number: Numero de comprobante a autorizar.
    :param pos: Numero de punto de venta.
    """

    def __init__(self, client, invoice, invoice_number, pos):
        self.client = client
        self.invoice = invoice
        self.invoice_number = invoice_number
        self.pos = pos

    def get_comprobante(self):
        comprobante_type = self.client.get_type(NS + 'ComprobanteType')

        kwargs = dict(
            codigoTipoComprobante=self.invoice.document_code,
            numeroPuntoVenta=self.pos,
            numeroComprobante=self.invoice_number,
            fechaEmision=self.invoice.document_date,
            codigoTipoDocumento=self.invoice.customer_document_type,
            numeroDocumento=self.invoice.customer_document_number,
            condicionIVAReceptor=self.invoice.customer_fiscal_position,
            importeGravado=round(self.invoice.taxed_amount, 2),
            importeNoGravado=round(self.invoice.untaxed_amount, 2),
            importeExento=round(self.invoice.exempt_amount, 2),
            importeSubtotal=round(self._get_subtotal(), 2),
            importeTotal=round(self.invoice.get_total_amount(), 2),
            codigoMoneda=self.invoice.mon_id,
            cotizacionMoneda=round(self.invoice.mon_cotiz, 6),
            codigoConcepto=self.invoice.concept,
            arrayItems=self._get_array_items(),
            arraySubtotalesIVA=self._get_array_subtotales_iva(),
        )

        # Fechas de servicio y vencimiento de pago solo para servicios (concepto 2 o 3)
        if self.invoice.concept in (2, 3):
            kwargs['fechaServicioDesde'] = self.invoice.service_from
            kwargs['fechaServicioHasta'] = self.invoice.service_to
            kwargs['fechaVencimientoPago'] = self.invoice.payment_due_date

        # Comprobantes asociados (NC/ND) o periodo asociado
        asociados = self._get_array_comprobantes_asociados()
        if asociados:
            kwargs['arrayComprobantesAsociados'] = asociados
        periodo = self._get_periodo_comprobantes_asociados()
        if periodo:
            kwargs['periodoComprobantesAsociados'] = periodo

        # Otros tributos (percepciones, impuestos internos, etc.): el importe y el detalle
        # deben informarse juntos o no informarse (validación 114 de ARCA).
        otros_tributos = self._get_array_otros_tributos()
        if otros_tributos:
            kwargs['arrayOtrosTributos'] = otros_tributos
            kwargs['importeOtrosTributos'] = round(self.invoice.get_total_tributes(), 2)

        return comprobante_type(**kwargs)

    def _get_subtotal(self):
        """ importeSubtotal (encabezado) = neto gravado + no gravado + exento. """
        return (self.invoice.taxed_amount or 0) \
            + (self.invoice.untaxed_amount or 0) \
            + (self.invoice.exempt_amount or 0)

    def _get_array_items(self):
        item_type = self.client.get_type(NS + 'ItemType')
        array_type = self.client.get_type(NS + 'ArrayItemsType')
        items = []
        for item in self.invoice.array_items:
            items.append(item_type(
                unidadesMtx=item.unidades_mtx,
                codigoMtx=item.codigo_mtx,
                codigo=item.codigo,
                descripcion=item.description,
                cantidad=item.quantity,
                codigoUnidadMedida=item.measurement_unit,
                precioUnitario=item.unit_price,
                importeBonificacion=round(item.bonification, 2) if item.bonification else None,
                codigoCondicionIVA=item.iva_code,
                importeIVA=round(item.iva_amount, 2) if item.iva_amount is not None else None,
                importeItem=round(item.item_amount, 2),
            ))
        return array_type(item=items)

    def _get_array_subtotales_iva(self):
        if not self.invoice.array_iva:
            return None
        subtotal_type = self.client.get_type(NS + 'SubtotalIVAType')
        array_type = self.client.get_type(NS + 'ArraySubtotalesIVAType')
        subtotales = [
            subtotal_type(codigo=iva.document_code, importe=round(iva.amount, 2))
            for iva in self.invoice.array_iva
        ]
        return array_type(subtotalIVA=subtotales)

    def _get_array_otros_tributos(self):
        if not self.invoice.array_tributes:
            return None
        tributo_type = self.client.get_type(NS + 'OtroTributoType')
        array_type = self.client.get_type(NS + 'ArrayOtrosTributosType')
        tributos = [
            tributo_type(
                codigo=tribute.document_code,
                descripcion='Tributo codigo {}'.format(tribute.document_code),
                baseImponible=round(tribute.taxable_base, 2),
                importe=round(tribute.amount, 2),
            )
            for tribute in self.invoice.array_tributes
        ]
        return array_type(otroTributo=tributos)

    def _get_array_comprobantes_asociados(self):
        if not self.invoice.associated_documents:
            return None
        asoc_type = self.client.get_type(NS + 'ComprobanteAsociadoType')
        array_type = self.client.get_type(NS + 'ArrayComprobantesAsociadosType')
        asociados = []
        for doc in self.invoice.associated_documents:
            kwargs = dict(
                codigoTipoComprobante=doc.document_type,
                numeroPuntoVenta=doc.point_of_sale,
                numeroComprobante=doc.number,
                fechaEmision=self._parse_associated_date(doc.document_date),
            )
            # El cuit del comprobante asociado solo corresponde cuando el emisor es otro
            # (p.ej. comprobantes de un tercero). Para NC/ND del propio emisor no debe enviarse.
            if getattr(doc, 'send_cuit', False) and doc.cuit:
                kwargs['cuit'] = doc.cuit
            asociados.append(asoc_type(**kwargs))
        return array_type(comprobanteAsociado=asociados)

    def _parse_associated_date(self, value):
        """ Los WsfeAssociatedDocument guardan la fecha como string YYYYMMDD; WSMTXCA usa date. """
        if not value:
            return None
        if isinstance(value, str):
            return datetime.strptime(value, '%Y%m%d').date()
        return value

    def _get_periodo_comprobantes_asociados(self):
        if not (self.invoice.period_from and self.invoice.period_to):
            return None
        periodo_type = self.client.get_type(NS + 'PeriodoComprobantesAsociadosType')
        return periodo_type(
            fechaDesde=self.invoice.period_from,
            fechaHasta=self.invoice.period_to,
        )


class WsmtxcaAssociatedDocument(object):

    def __init__(self, document_type, point_of_sale, number, cuit, document_date):
        self.document_type = document_type
        self.point_of_sale = point_of_sale
        self.number = number
        self.cuit = cuit
        self.document_date = document_date


class Wsmtxca(object):
    """
    Factura electronica con detalle (WSMTXCA).

    :param access_token: AccessToken - Token de acceso
    :param cuit: Cuit de la empresa
    :param homologation: Homologacion si es True
    :param url: Url de servicios para WSMTXCA
    """

    def __init__(self, access_token, cuit, homologation=True, url=None):
        if not url:
            self.url = config.service_urls.get('wsmtxca_homologation') if homologation \
                else config.service_urls.get('wsmtxca_production')
        else:
            self.url = url

        self.accessToken = access_token
        self.cuit = cuit
        self.client = ApiClient(self.url)
        self.auth_request = self._create_auth_request()

    def check_webservice_status(self):
        """ Consulta el estado de los servidores de ARCA via dummy(). """
        res = self.client.service.dummy()

        if res.appserver != 'OK':
            raise Exception('El servidor de aplicaciones no se encuentra disponible. Intente mas tarde.')
        if res.dbserver != 'OK':
            raise Exception('El servidor de base de datos no se encuentra disponible. Intente mas tarde.')
        if res.authserver != 'OK':
            raise Exception('El servidor de auntenticacion no se encuentra disponible. Intente mas tarde.')

    def get_last_number(self, pos_number, document_type_number):
        """
        :param pos_number: Numero de punto de venta
        :param document_type_number: Numero del tipo de documento segun ARCA a consultar
        :return: Numero de ultimo comprobante autorizado para ese tipo
        """
        consulta_type = self.client.get_type(NS + 'ConsultaUltimoComprobanteAutorizadoRequestType')
        consulta = consulta_type(
            codigoTipoComprobante=document_type_number,
            numeroPuntoVenta=pos_number,
        )
        response = self.client.service.consultarUltimoComprobanteAutorizado(
            authRequest=self.auth_request,
            consultaUltimoComprobanteAutorizadoRequest=consulta,
        )

        if response.arrayErrores:
            # 1502: no hay comprobantes emitidos para ese punto de venta / tipo
            if response.arrayErrores.codigoDescripcion[0].codigo not in (1502,):
                raise AfipError.parse_error(response)
        if response.numeroComprobante is None:
            return 0
        return response.numeroComprobante

    def get_cae(self, invoices, pos):
        """
        Autoriza los comprobantes en ARCA. WSMTXCA autoriza un comprobante por request,
        por lo que se itera la lista incrementando la numeracion.

        :param invoices: Lista de objetos MtxElectronicInvoice.
        :param pos: Numero de punto de venta.
        :returns: Tupla (lista_de_responses, lista_de_requests).
        """
        self._validate_invoices(invoices)

        responses = []
        requests = []
        last_number = None

        for invoice in invoices:
            if last_number is None:
                last_number = self.get_last_number(pos, invoice.document_code)
            number = last_number + 1

            comprobante = WsmtxcaInvoiceDetails(self.client, invoice, number, pos).get_comprobante()
            response = self.client.service.autorizarComprobante(
                authRequest=self.auth_request,
                comprobanteCAERequest=comprobante,
            )
            responses.append(response)
            requests.append(helpers.serialize_object(comprobante, dict))
            last_number = number

        return responses, requests

    def show_error(self, response):
        if response.arrayErrores:
            raise AfipError.parse_error(response)

    def retrieve_cae(self, document_type_number, inv_number, pos_number):
        """
        Consulta un comprobante previamente autorizado via consultarComprobante.
        Se usa para recuperar CAEs ante errores de comunicacion.

        :return: Tupla (response_dict, request_dict).
        """
        consulta_type = self.client.get_type(NS + 'ConsultaComprobanteRequestType')
        consulta = consulta_type(
            codigoTipoComprobante=document_type_number,
            numeroPuntoVenta=pos_number,
            numeroComprobante=inv_number,
        )
        response = self.client.service.consultarComprobante(
            authRequest=self.auth_request,
            consultaComprobanteRequest=consulta,
        )
        # Las fechas (xsd:date) se serializan a strings ISO para que el dict resultante sea
        # representable como literal (el consumidor lo persiste y lo relee con ast.literal_eval).
        resp = self._dates_to_iso(helpers.serialize_object(response, dict))
        req = self._dates_to_iso(helpers.serialize_object(consulta, dict))
        return resp, req

    def _dates_to_iso(self, value):
        """ Convierte recursivamente objetos date/datetime de un dict serializado a strings ISO. """
        if isinstance(value, dict):
            return {k: self._dates_to_iso(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._dates_to_iso(v) for v in value]
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value

    def _validate_invoices(self, invoices):
        validator = ElectronicInvoiceValidator()
        for invoice in invoices:
            validator.validate_invoice(invoice)

    def _create_auth_request(self):
        auth_request_type = self.client.get_type(NS + 'AuthRequestType')
        return auth_request_type(
            token=self.accessToken.token,
            sign=self.accessToken.sign,
            cuitRepresentada=self.cuit,
        )
