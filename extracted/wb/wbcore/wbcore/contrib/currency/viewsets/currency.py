from datetime import date, timedelta

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework import filters

from wbcore import viewsets
from wbcore.filters import DjangoFilterBackend

from ..models import Currency, CurrencyFXRates
from ..serializers import CurrencyModelSerializer, CurrencyRepresentationSerializer
from .display import CurrencyDisplayConfig
from .preview import CurrencyPreviewConfig
from .titles import CurrencyTitleConfig


class CurrencyRepresentationViewSet(viewsets.RepresentationViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencyRepresentationSerializer
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)

    ordering = ["name_repr"]
    search_fields = ("name_repr", "key")


class CurrencyModelViewSet(viewsets.ModelViewSet):
    display_config_class = CurrencyDisplayConfig
    title_config_class = CurrencyTitleConfig
    preview_config_class = CurrencyPreviewConfig

    queryset = Currency.objects.all()
    serializer_class = CurrencyModelSerializer

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)

    filterset_fields = {
        "title": ["exact", "icontains"],
        "symbol": ["exact", "icontains"],
        "key": ["exact", "icontains"],
    }
    ordering_fields = ("title", "symbol", "key")

    ordering = ["title"]

    def get_queryset(self):
        last_rate_date = date.today()
        if CurrencyFXRates.objects.exists():
            last_rate_date = CurrencyFXRates.objects.latest("date").date
        last_rate_date -= timedelta(days=30)
        return (
            super()
            .get_queryset()
            .annotate(
                fx_rates_date=ArrayAgg("fx_rates__date", filter=Q(fx_rates__date__gt=last_rate_date)),
                fx_rates_value=ArrayAgg("fx_rates__value", filter=Q(fx_rates__date__gt=last_rate_date)),
            )
        )
