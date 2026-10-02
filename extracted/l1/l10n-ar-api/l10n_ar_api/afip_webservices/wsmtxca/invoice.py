# -*- coding: utf-8 -*-
from datetime import date
from l10n_ar_api.documents import invoice as inv


class ElectronicInvoiceValidator(object):

    def validate_invoice(self, invoice):
        """
        Valida que los campos de la factura cumplan con los requisitos de la AFIP
        :param invoice: Factura a validar, objeto MtxElectronicInvoice
        """

        self._validate_document_date(invoice)
        self._validate_concept(invoice)
        self._validate_mon_cotiz(invoice)
        self._validate_items(invoice)

    def _validate_document_date(self, invoice):
        assert invoice.concept, "El documento no tiene concepto"
        assert invoice.document_date, "El documento no tiene fecha"

        # En WSMTXCA las fechas se manejan como objetos date (xsd:date), no como string YYYYMMDD.
        invoice_date = invoice.document_date

        if (invoice.concept != 1 and abs(date.today() - invoice_date).days > 10 or
                invoice.concept == 1 and abs(date.today() - invoice_date).days > 5):

            raise AttributeError("La fecha del documento debe ser\
                mayor o menor a 5 dias de la fecha de generacion para concepto\
                igual a 1, o a 10 dias para concepto 2 o 3")

    def _validate_concept(self, invoice):
        if invoice.concept not in (1, 2, 3):
            raise AttributeError('Concepto invalido')

    def _validate_mon_cotiz(self, invoice):
        if invoice.mon_id == 'PES' and invoice.mon_cotiz != 1:
            raise AttributeError("Para Pesos, la cotizacion debe ser 1")

    def _validate_items(self, invoice):
        if not invoice.array_items:
            raise AttributeError("El comprobante debe tener al menos un item")


class MtxItem(object):
    """ Item de detalle de un comprobante WSMTXCA (ItemType).

    :param description: Descripcion del item (descripcion).
    :param quantity: Cantidad (cantidad).
    :param measurement_unit: Codigo de unidad de medida AFIP (codigoUnidadMedida).
    :param unit_price: Precio unitario (precioUnitario).
    :param bonification: Importe de bonificacion (importeBonificacion).
    :param iva_code: Codigo de condicion / alicuota de IVA del item (codigoCondicionIVA).
    :param iva_amount: Importe de IVA del item (importeIVA).
    :param item_amount: Importe total del item (importeItem).
    :param codigo: Codigo del producto (codigo), opcional.
    :param codigo_mtx: Codigo MTX / GTIN (codigoMtx), opcional.
    :param unidades_mtx: Unidades MTX (unidadesMtx), opcional.
    """

    def __init__(self, description, quantity=None, measurement_unit=None, unit_price=None,
                 bonification=None, iva_code=None, iva_amount=None, item_amount=None,
                 codigo=None, codigo_mtx=None, unidades_mtx=None):
        self.description = description
        self.quantity = quantity
        self.measurement_unit = measurement_unit
        self.unit_price = unit_price
        self.bonification = bonification
        self.iva_code = iva_code
        self.iva_amount = iva_amount
        self.item_amount = item_amount
        self.codigo = codigo
        self.codigo_mtx = codigo_mtx
        self.unidades_mtx = unidades_mtx


class MtxElectronicInvoice(inv.Invoice):

    def __init__(self, document_code):

        self.concept = None

        # Fechas (objetos date, WSMTXCA usa xsd:date)
        self._service_from = None
        self._service_to = None
        self._payment_due_date = None

        # Fechas Periodo Asociado
        self._period_from = None
        self._period_to = None

        # Tributos
        self.array_iva = []
        self.array_tributes = []

        # Items
        self.array_items = []

        # Cliente
        self.customer_document_type = None
        self.customer_document_number = None
        self.customer_fiscal_position = None

        # Moneda
        self.mon_id = None
        self.mon_cotiz = None

        # Comprobantes asociados
        self.associated_documents = []

        super(MtxElectronicInvoice, self).__init__(document_code)

    def get_total_iva(self):
        return sum(iva.amount for iva in self.array_iva)

    def get_total_tributes(self):
        return sum(tribute.amount for tribute in self.array_tributes)

    def get_total_items_amount(self):
        return sum(item.item_amount or 0 for item in self.array_items)

    def get_total_amount(self):
        total_amount = super(MtxElectronicInvoice, self).get_total_amount()
        try:
            total_amount += self.get_total_iva() + self.get_total_tributes()
        except TypeError:
            raise AttributeError("Falta especificar algun importe en la factura")
        return total_amount

    def add_iva(self, iva):
        if not iva.amount:
            return

        # Buscar si ya existe un IVA con el mismo document_code para acumular
        existing = next((x for x in self.array_iva if x.document_code == iva.document_code), None)
        if existing:
            existing.amount += iva.amount
            existing.taxable_base += iva.taxable_base
        else:
            self.array_iva.append(iva)

    def add_tribute(self, tribute):
        if tribute.amount:
            self.array_tributes.append(tribute)

    def add_item(self, item):
        self.array_items.append(item)

    @property
    def document_date(self):
        return self._document_date

    @document_date.setter
    def document_date(self, value):
        self._document_date = value

    @property
    def service_from(self):
        return self._service_from

    @service_from.setter
    def service_from(self, value):
        self._service_from = value

    @property
    def service_to(self):
        return self._service_to

    @service_to.setter
    def service_to(self, value):
        self._service_to = value

    @property
    def payment_due_date(self):
        return self._payment_due_date

    @payment_due_date.setter
    def payment_due_date(self, value):
        self._payment_due_date = value

    @property
    def period_from(self):
        return self._period_from

    @period_from.setter
    def period_from(self, value):
        self._period_from = value

    @property
    def period_to(self):
        return self._period_to

    @period_to.setter
    def period_to(self, value):
        self._period_to = value
