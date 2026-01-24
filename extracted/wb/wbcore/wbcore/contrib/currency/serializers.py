from rest_framework.reverse import reverse

from wbcore import serializers as wb_serializers

from .models import Currency, CurrencyFXRates


class CurrencyRepresentationSerializer(wb_serializers.RepresentationSerializer):
    """Representation Serializer for Currencies"""

    name_repr = wb_serializers.SerializerMethodField(read_only=True)
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:currency:currency-detail")

    def get_name_repr(self, obj):
        return str(obj)

    class Meta:
        model = Currency
        fields = ("id", "name_repr", "key", "_detail")


class CurrencyModelSerializer(wb_serializers.ModelSerializer):
    """Model Serializer for Currencies"""

    rates_sparkline = wb_serializers.SparklineField(
        x_data_label="fx_rates_date", y_data_label="fx_rates_value", label="Rates"
    )

    @wb_serializers.register_resource()
    def currency_currencyfxrates(self, instance, request, user):
        return {
            "currency_currencyfxrates": reverse(
                "wbcore:currency:currency-currencyfxrates-list", args=[instance.id], request=request
            )
        }

    class Meta:
        model = Currency
        fields = ("id", "title", "symbol", "key", "rates_sparkline", "_additional_resources")


class CurrencyFXRatesModelSerializer(wb_serializers.ModelSerializer):
    class Meta:
        model = CurrencyFXRates
        fields = ("id", "date", "currency", "value")
