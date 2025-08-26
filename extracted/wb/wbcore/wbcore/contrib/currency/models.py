from __future__ import annotations

from datetime import date as date_lib
from decimal import Decimal

from django.db import models
from django.db.models import Expression, ExpressionWrapper, Subquery

from wbcore.contrib.io.mixins import ImportMixin
from wbcore.models import WBModel
from wbcore.utils.models import LabelKeyMixin

from .import_export.handlers import CurrencyFXRatesImportHandler, CurrencyImportHandler


class Currency(ImportMixin, LabelKeyMixin, WBModel):
    import_export_handler_class = CurrencyImportHandler

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ("title",)

    def __str__(self):
        symbol = f"({self.symbol})" if self.symbol else ""
        return f"{self.key} {symbol}"

    def __repr__(self):
        return self.key

    title = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10, blank=True, null=True)
    key = models.CharField(max_length=3, unique=True)

    objects = models.Manager()

    LABEL_KEY = "{{key}} ({{symbol}})"

    def convert(self, valuation_date: date_lib, other_currency: Currency, exact_lookup: bool = False) -> Decimal:
        """
        Change the base currency of one of its related fx rates

        Arguments:
            valuation_date {datetime.date} -- The convertion date
            other_currency {Currency} -- The convertion currency
        Returns:
            float -- The fx rate value with the new base currency
        """
        if self == other_currency:
            return Decimal(1.0)
        try:
            if exact_lookup:
                base = CurrencyFXRates.objects.get(date=valuation_date, currency=self)
                other = CurrencyFXRates.objects.get(date=valuation_date, currency=other_currency)
            else:
                base = (
                    CurrencyFXRates.objects.filter(date__lte=valuation_date, currency=self).order_by("-date").first()
                )
                other = (
                    CurrencyFXRates.objects.filter(date__lte=valuation_date, currency=other_currency)
                    .order_by("-date")
                    .first()
                )
                if not base or not other:
                    raise CurrencyFXRates.DoesNotExist
            return (1 / base.value) * other.value
        except CurrencyFXRates.DoesNotExist:
            if exact_lookup:
                return self.convert(valuation_date, other_currency, exact_lookup=False)
            raise CurrencyFXRates.DoesNotExist

    @classmethod
    def get_endpoint_basename(cls) -> str:
        return "wbcore:currency:currency"

    @classmethod
    def get_representation_endpoint(cls) -> str:
        return "wbcore:currency:currencyrepresentation-list"

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{key}} ({{symbol}})"


class CurrencyFXRates(ImportMixin, models.Model):
    import_export_handler_class = CurrencyFXRatesImportHandler

    date = models.DateField()
    currency = models.ForeignKey(to="Currency", related_name="fx_rates", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=20, decimal_places=6)

    class Meta:
        verbose_name = "FX Rate"
        verbose_name_plural = "FX Rates"
        unique_together = ("date", "currency")
        indexes = [
            models.Index(
                name="currency_fx_rate_idx",
                fields=["date", "currency"],
            )
        ]

    def __str__(self) -> str:
        return f"{self.date:%d.%m.%Y} {self.currency.key}"

    @classmethod
    def get_fx_rates_subquery(
        cls,
        val_date: date_lib | str,
        currency: str = "product__currency",
        lookup_expr: str = "lte",
    ) -> Expression:
        """
        Create a subquery to annotate the rate at a given date based on currency__key

        Arguments:
            date {datetime.date|str} -- The fx date
            is_outerref_key {bool} -- Determines the type of date variable, if true is outerref key string
            currency_key {str} -- The Outerref field for currency__key
        Returns:
            Subquery -- Subquery for rates at a certain date
        """
        fx_rates = (
            cls.objects.filter(
                **{f"date__{lookup_expr}": models.OuterRef(val_date) if isinstance(val_date, str) else val_date},
                currency=models.OuterRef(currency),
            )
            .order_by("-date")
            .values("value")[:1]
        )

        return ExpressionWrapper(1 / Subquery(fx_rates), output_field=models.DecimalField())

    @classmethod
    def get_fx_rates_subquery_for_two_currencies(
        cls,
        date_key: str,
        start_currency: str | Currency,
        target_currency: str | Currency,
    ) -> Expression:
        """
        Create a subquery to returns the convertion rate from a start to a target currency

        Arguments:
            date_key {datetime.date} -- The convertion date
            start_currency {str} -- The Outerref field for start currency
            target_currency {str} -- The Outerref field for target currency
        Returns:
            Subquery -- Subquery for the convertion rate rates at a certain date
        """
        fx_rates_start = (
            CurrencyFXRates.objects.filter(
                date=models.OuterRef(date_key),
                currency=models.OuterRef(start_currency) if isinstance(start_currency, str) else start_currency,
            )
            .order_by("-date")
            .values("value")[:1]
        )
        fx_rates_target = (
            CurrencyFXRates.objects.filter(
                date=models.OuterRef(date_key),
                currency=models.OuterRef(target_currency) if isinstance(target_currency, str) else target_currency,
            )
            .order_by("-date")
            .values("value")[:1]
        )
        return ExpressionWrapper(
            Subquery(fx_rates_target) / Subquery(fx_rates_start), output_field=models.DecimalField()
        )

    @classmethod
    def get_representation_value_key(cls) -> str:
        return "id"

    @classmethod
    def get_representation_label_key(cls) -> str:
        return "{{value}} ({{currency__symbol}})"
