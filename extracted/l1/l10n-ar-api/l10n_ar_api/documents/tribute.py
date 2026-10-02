# -*- coding: utf-8 -*-
import math

def apply_rounding(value, rounding=2):
    multiplier = 10 ** rounding
    return math.floor(round(value * multiplier + 0.5, rounding)) / multiplier


class Activity:

    def __init__(self, minimum_no_aplicable, minimum_tax, percentage):
        """
        :param minimum_no_aplicable: Minimo no imponible de la actividad
        :param minimum_tax: Importe minimo a retener/percibir
        :param percentage: Porcentaje de la actividad
        """
        self.minimum_no_aplicable = minimum_no_aplicable
        self.minimum_tax = minimum_tax
        self.percentage = percentage


class _ActivityProperty:
    """
    Mixin que expone una property ``activity`` (objeto :class:`Activity`) que
    envuelve los atributos directos ``percentage``, ``minimum_no_aplicable``
    y ``minimum_tax`` del tributo.

    Permite configurar el tributo con cualquiera de las dos formas
    (atributos directos o ``Activity``) de modo intercambiable.
    """

    @property
    def activity(self):
        return Activity(self.minimum_no_aplicable, self.minimum_tax, self.percentage)

    @activity.setter
    def activity(self, value):
        if value is None:
            self.percentage = 0.0
            self.minimum_no_aplicable = 0.0
            self.minimum_tax = 0.0
        else:
            self.percentage = value.percentage
            self.minimum_no_aplicable = value.minimum_no_aplicable
            self.minimum_tax = value.minimum_tax


class Tribute:

    @staticmethod
    def get_tribute(tribute_type):
        """ Devuelve la instancia del tipo de percepcion deseado """
        if tribute_type == 'gross_income':
            return GrossIncome()
        elif tribute_type == 'profit':
            return Profit()
        elif tribute_type == 'suss':
            return Suss()
        elif tribute_type == 'vat':
            return Vat()
        else:
            raise NotImplementedError("El tipo de tributo {} No existe".format(tribute_type))


class Suss(_ActivityProperty):

    def __init__(self):
        self.percentage = 0.0
        self.minimum_no_aplicable = 0.0
        self.minimum_tax = 0.0

    def calculate_value(self, amount_to_pay):
        """
        Devuelve el valor del calculo de IIBB
        :param amount_to_pay: Importe a pagar sin impuestos
        :return: Base imponible y Valor calculado
        """

        base = amount_to_pay
        value = apply_rounding(base * (self.percentage / 100))

        if base < self.minimum_no_aplicable or value < self.minimum_tax:
            value = 0

        return base, value


class GrossIncome(_ActivityProperty):

    def __init__(self):
        self.percentage = 0.0
        self.minimum_no_aplicable = 0.0
        self.minimum_tax = 0.0

    def calculate_value(self, amount_to_pay):
        """
        Devuelve el valor del calculo de IIBB
        :param amount_to_pay: Importe a pagar sin impuestos
        :return: Base imponible y Valor calculado
        """

        base = amount_to_pay
        value = apply_rounding(base * (self.percentage / 100))

        if base < self.minimum_no_aplicable or value < self.minimum_tax:
            value = 0

        return base, value


class Vat(_ActivityProperty):
    """
    Calcula la retención de IVA sobre un pago a proveedor.

    Recibe las fuentes ya clasificadas por ``get_amount_to_tax_vat()``
    (dict con 'invoices' y 'on_account') y aplica:
      - MNI solo sobre facturas (si el neto gravado total supera el mínimo)
      - Equivalente 21% sobre importes a cuenta
      - Alícuota del proveedor sobre la base combinada

    ``minimum_tax`` se mantiene como atributo por simetría con los demás
    tributos, aunque ``calculate_value`` no lo utiliza (régimen general IVA
    sólo valida MNI sobre la base).
    """

    VAT_GENERAL_RATE = 21.0

    def __init__(self):
        self.percentage = 0.0
        self.minimum_no_aplicable = 0.0
        self.minimum_tax = 0.0

    def calculate_value(self, sources):
        """
        :param sources: dict devuelto por ``account.payment.get_amount_to_tax_vat()``
            - 'invoices': lista de tuplas (iva_prorrateado, neto_gravado_total)
            - 'on_account': float con el importe a cuenta + saldos iniciales
        :return: tupla (base, retencion)
        """
        total_net = sum(net for _, net in sources['invoices']) + sources['on_account']
        total_invoice_vat = sum(vat for vat, _ in sources['invoices'])

        # MNI solo aplica a facturas; a cuenta siempre retiene
        base = 0.0
        if total_net >= self.minimum_no_aplicable:
            base += total_invoice_vat + sources['on_account'] * (self.VAT_GENERAL_RATE / 100.0)

        if base <= 0:
            return 0, 0

        retention = apply_rounding(base * (self.percentage / 100.0))
        return base, retention


class Profit:
    """
    Tributo para Ganancias. Acepta dos formas equivalentes de configuración:

    Atributos directos (consistente con Suss/Vat/GrossIncome):
        profit.percentage = X
        profit.minimum_no_aplicable = Y
        profit.minimum_tax = Z

    Legacy (mantenida por retrocompatibilidad):
        profit.activity = Activity(MNI, min_tax, percentage)

    A diferencia de los otros tributos, ``Profit`` distingue el estado "no
    configurado" (atributos en ``None``) para levantar ``AttributeError`` si
    se intenta calcular sin haber configurado la actividad.
    """

    def __init__(self):
        self.percentage = None
        self.minimum_no_aplicable = None
        self.minimum_tax = None

    @property
    def activity(self):
        if self.percentage is None and self.minimum_no_aplicable is None and self.minimum_tax is None:
            return None
        return Activity(
            self.minimum_no_aplicable or 0.0,
            self.minimum_tax or 0.0,
            self.percentage or 0.0,
        )

    @activity.setter
    def activity(self, value):
        if value is None:
            self.percentage = None
            self.minimum_no_aplicable = None
            self.minimum_tax = None
        else:
            self.percentage = value.percentage
            self.minimum_no_aplicable = value.minimum_no_aplicable
            self.minimum_tax = value.minimum_tax

    def calculate_value(self, accumulated, amount_to_pay, first_retention=True):
        """
        Devuelve el valor a retener/percibir para la actividad
        :param accumulated: Acumulado de pagos necesario para deducir el valor
        :param amount_to_pay: Importe a pagar sin impuestos
        :param first_retention: Si es la primera retencion, se restará el minimo no imponible
        :return: Base imponible y Valor que se debe retener
        """
        if self.percentage is None and self.minimum_no_aplicable is None and self.minimum_tax is None:
            raise AttributeError("Agregar actividad en el tributo antes de calcular el valor")

        percentage = self.percentage or 0.0
        minimum_no_aplicable = self.minimum_no_aplicable or 0.0
        minimum_tax = self.minimum_tax or 0.0

        # El acumulado se debe restar siempre, excepto en el caso que el acumulado sea mayor al minimo no imponible
        # y no se haya retenido por primera vez (porque no sobrepaso el minimo), entonces en ese caso el valor de la
        # retencion es por la anterior + la actual
        if ((accumulated - minimum_no_aplicable) * percentage / 100) >= minimum_tax and first_retention:
            accumulated = minimum_no_aplicable

        base = amount_to_pay + accumulated - minimum_no_aplicable if first_retention else amount_to_pay + accumulated
        value = apply_rounding(base * (percentage / 100))

        if value < minimum_tax:
            value = 0

        return base, value
