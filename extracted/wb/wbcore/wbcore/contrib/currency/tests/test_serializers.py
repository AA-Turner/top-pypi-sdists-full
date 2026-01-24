import pytest
from django.utils import timezone
from pytest_mock import MockerFixture

from wbcore.contrib.currency.models import Currency, CurrencyFXRates
from wbcore.contrib.currency.serializers import (
    CurrencyFXRatesModelSerializer,
    CurrencyModelSerializer,
    CurrencyRepresentationSerializer,
)


@pytest.mark.serializer_tests
class TestSerializers:
    @pytest.fixture
    def currency(self, mocker: MockerFixture):
        currency = Currency()
        mocker.patch.object(currency, "id", 1)
        mocker.patch.object(currency, "key", "abc")
        mocker.patch.object(currency, "title", "ABC")
        mocker.patch.object(currency, "symbol", "$")
        return currency

    @pytest.fixture
    def currency_fx_rate(self, mocker: MockerFixture, currency):
        currency_fx_rate = CurrencyFXRates()
        mocker.patch.object(currency_fx_rate, "id", 1)
        mocker.patch.object(currency_fx_rate, "date", timezone.now().date().isoformat())
        mocker.patch.object(currency_fx_rate, "value", "1.150000")
        mocker.patch.object(currency_fx_rate, "currency_id", currency.id)
        return currency_fx_rate

    @pytest.fixture
    def expected_representation_data(self, currency):
        return {"id": currency.id, "name_repr": f"{currency.title} ({currency.symbol})", "key": currency.key}

    @pytest.fixture
    def expected_data(self, currency):
        return {"id": currency.id, "title": currency.title, "key": currency.key, "symbol": currency.symbol}

    @pytest.fixture
    def expected_data_fx_rate(self, currency_fx_rate):
        return {
            "id": currency_fx_rate.id,
            "value": currency_fx_rate.value,
            "date": currency_fx_rate.date,
            "currency": currency_fx_rate.currency_id,
        }

    def test_currency_representation_serializer(self, mocker: MockerFixture, currency, expected_representation_data):
        detail = f"/wbcore/currency/currency/{currency.id}/"
        mocker.patch("wbcore.serializers.fields.fields.HyperlinkField", return_value=detail)
        serializer = CurrencyRepresentationSerializer(instance=currency)
        expected_representation_data["_detail"] = detail
        assert serializer.data == expected_representation_data

    def test_currency_model_serializer(self, mocker: MockerFixture, currency, expected_data):
        mocker.patch(
            "wbcore.serializers.fields.list.SparklineField.to_representation", return_value={"Rates": [1, 2, 3]}
        )
        serializer = CurrencyModelSerializer(instance=currency)
        expected_data.update({"rates_sparkline": {"Rates": [1, 2, 3]}, "_additional_resources": {}})
        assert serializer.data == expected_data

    def test_currency_fx_rate_model_serializer(self, currency_fx_rate, expected_data_fx_rate):
        serializer = CurrencyFXRatesModelSerializer(instance=currency_fx_rate)
        assert serializer.data == expected_data_fx_rate
