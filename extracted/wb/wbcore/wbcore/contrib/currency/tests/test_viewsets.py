from datetime import date, timedelta
from decimal import Decimal

import pytest
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.test import APIRequestFactory

from wbcore.contrib.authentication.factories import SuperUserFactory
from wbcore.contrib.currency.factories import CurrencyFactory, CurrencyFXRatesFactory
from wbcore.contrib.currency.models import Currency
from wbcore.contrib.currency.viewsets import (
    CurrencyModelViewSet,
    CurrencyRepresentationViewSet,
)


@pytest.mark.viewset_tests
@pytest.mark.with_db
@pytest.mark.django_db
class TestCurrencyRepresentationViewSets:
    @pytest.fixture()
    def test_request(self):
        factory = APIRequestFactory()
        request = factory.get("")
        request.user = SuperUserFactory()
        return request

    def test_currency_list_representation_viewset(self, test_request, currency_factory):
        # Arrange
        currency_factory.create_batch(2)
        vs = CurrencyRepresentationViewSet.as_view({"get": "list"})
        # Act
        response = vs(test_request)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data
        assert len(response.data["results"]) == 2

    def test_currency_representation_viewset(self, test_request, currency_factory):
        # Arrange
        euro = currency_factory(symbol="€", key="EUR", title="Euro")
        vs = CurrencyRepresentationViewSet.as_view({"get": "retrieve"})
        # Act
        response = vs(test_request, pk=euro.pk)
        instance = response.data.get("instance")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert instance.get("id") == euro.id
        assert instance.get("key") == euro.key
        assert instance.get("name_repr") == f"{euro.title} ({euro.symbol})"


@pytest.mark.viewset_tests
@pytest.mark.with_db
@pytest.mark.django_db
class TestCurrencyViewSets:
    @pytest.fixture()
    def api_rf(self):
        factory = APIRequestFactory()
        return factory

    @pytest.fixture()
    def su(self):
        super_user = SuperUserFactory()
        return super_user

    @pytest.fixture()
    def get_request(self, api_rf, su):
        request = api_rf.get("")
        request.user = su
        return request

    @pytest.fixture()
    def currency(self):
        currency = CurrencyFactory()
        return currency

    @pytest.fixture()
    def currencies(self):
        currency_a = CurrencyFactory()
        currency_b = CurrencyFactory()
        currency_c = CurrencyFactory()
        return [currency_a, currency_b, currency_c]

    def test_get_instance_request(self, get_request, currency):
        # Arrange
        vs = CurrencyModelViewSet.as_view({"get": "retrieve"})
        # Act
        response = vs(get_request, pk=currency.pk)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert not response.data.get("results")
        assert response.data["instance"]["id"] == currency.id

    def test_get_list_request(self, get_request):
        # Arrange
        CurrencyFactory.create_batch(3)
        vs = CurrencyModelViewSet.as_view({"get": "list"})
        # Act
        response = vs(get_request)
        # Assert
        results = response.data.get("results")
        assert response.status_code == status.HTTP_200_OK
        assert not response.data.get("instance")
        assert len(results) == 3

    def test_delete_instance(self, api_rf, su, currency):
        # Arrange
        request = api_rf.delete("")
        request.user = su
        view = CurrencyModelViewSet.as_view({"delete": "destroy"})
        # Act
        response = view(request, pk=currency.id)
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Currency.objects.count() == 0

    def test_update_instance(self, api_rf, su, currency):
        # Arrange
        new_currency = model_to_dict(CurrencyFactory.build())
        # Add missing values to the dict, because we cannot update data with 'None' values
        new_currency["id"] = currency.id
        new_currency["import_source"] = ""
        request = api_rf.put("", data=new_currency)
        request.user = su
        view = CurrencyModelViewSet.as_view({"put": "update"})
        # Act
        response = view(request, pk=currency.id)
        instance = response.data.get("instance")
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert instance["id"] == currency.id
        assert instance["key"] == new_currency["key"]
        assert instance["key"] != currency.key

    @pytest.mark.parametrize("title", ["New_title"])
    def test_patch_instance(self, api_rf, su, currency, title):
        # Arrange
        request = api_rf.patch("", data={"title": title})
        request.user = su
        # Act
        view = CurrencyModelViewSet.as_view({"patch": "partial_update"})
        response = view(request, pk=currency.id)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data["instance"]["title"] == title
        assert currency.title != title
        currency.refresh_from_db()  # The patch changes are only visible after a refresh
        assert currency.title == title

    def test_get_queryset_no_fx_rates(self, currencies):
        viewset = CurrencyModelViewSet()
        qs = viewset.get_queryset()
        last_rate_date = date.today() - timedelta(days=30)
        expected_queryset = Currency.objects.annotate(
            fx_rates_date=ArrayAgg("fx_rates__date", filter=Q(fx_rates__date__gt=last_rate_date)),
            fx_rates_value=ArrayAgg("fx_rates__value", filter=Q(fx_rates__date__gt=last_rate_date)),
        )
        assert list(qs) == list(expected_queryset)
        for currency in qs:
            assert currency.fx_rates_date is None
            assert currency.fx_rates_value is None

    def test_get_queryset_with_fx_rates(self, currencies):
        recent_fx_rate_date, mid_fx_rate_date, past_cutoff_fx_rate_date = (
            date.today() - timedelta(days=5),
            date.today() - timedelta(days=20),
            date.today() - timedelta(days=35),
        )
        value_a, value_b, value_c = (
            Decimal("1.10"),
            Decimal("0.85"),
            Decimal("1.20"),
        )

        fx_rate_data = [
            {"date": recent_fx_rate_date, "value": value_a},
            {"date": mid_fx_rate_date, "value": value_b},
            {"date": past_cutoff_fx_rate_date, "value": value_c},
        ]

        for currency in currencies:
            for data in fx_rate_data:
                CurrencyFXRatesFactory(currency=currency, date=data["date"], value=data["value"])

        viewset = CurrencyModelViewSet()
        qs = viewset.get_queryset()
        expected_rates = [value_a, value_b]
        expected_dates = [recent_fx_rate_date, mid_fx_rate_date]
        assert len(qs) == 3
        for currency in qs:
            assert currency.fx_rates_date == expected_dates
            assert currency.fx_rates_value == expected_rates
