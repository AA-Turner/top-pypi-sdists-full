import pathlib

import factory
import yaml

from .models import Currency, CurrencyFXRates

with open(pathlib.Path(__file__).parent.joinpath("fixtures").joinpath("currency.yaml"), "r") as yaml_file:
    currency_dict = yaml.load(yaml_file, Loader=yaml.CLoader)  # noqa: S506


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency
        django_get_or_create = ["key"]

    title = factory.Iterator(currency_dict, getter=lambda c: c["fields"]["title"])
    symbol = factory.Iterator(currency_dict, getter=lambda c: c["fields"]["symbol"])
    key = factory.Iterator(currency_dict, getter=lambda c: c["fields"]["key"])

    @classmethod
    def full_db(cls):
        for _ in range(len(currency_dict)):
            cls()


class CurrencyUSDFactory(CurrencyFactory):
    title = "US Dollar"
    symbol = "$"
    key = "USD"


class CurrencyFXRatesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CurrencyFXRates
        django_get_or_create = ["date", "currency"]

    date = factory.Faker("date_object")
    currency = factory.SubFactory(CurrencyFactory)
    value = factory.Faker("pydecimal", min_value=1, max_value=999999, right_digits=6)
