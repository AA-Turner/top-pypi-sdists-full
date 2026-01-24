import pytest
from django.apps import apps
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.models.signals import pre_migrate
from pytest_factoryboy import register
from wbcore.contrib.authentication.factories import InternalUserFactory, UserFactory
from wbcore.contrib.geography.tests.signals import app_pre_migration
from wbcore.contrib.currency.factories import CurrencyFactory
from wbcore.tests.conftest import *

from ..factories import (
    AddressContactFactory,
    BankingContactFactory,
    ClientFactory,
    ClientManagerRelationshipFactory,
    CompanyFactory,
    CompanyTypeFactory,
    CustomerStatusFactory,
    EmailContactFactory,
    EmployersCompanyFactory,
    EntryFactory,
    PersonFactory,
    RelationshipFactory,
    RelationshipTypeFactory,
    TelephoneContactFactory,
    UnemployedPersonFactory,
    WebsiteContactFactory,
)
from .signals import *

register(UserFactory)
register(EntryFactory)
register(CompanyFactory)
register(PersonFactory)
register(ClientFactory)
register(InternalUserFactory)
register(UnemployedPersonFactory)
register(EmployersCompanyFactory)
register(BankingContactFactory)
register(AddressContactFactory)
register(TelephoneContactFactory)
register(EmailContactFactory)
register(WebsiteContactFactory)
register(ClientManagerRelationshipFactory)
register(RelationshipFactory)
register(RelationshipTypeFactory)
register(CustomerStatusFactory)
register(CompanyTypeFactory)
register(CurrencyFactory)


@pytest.fixture(autouse=True, scope="session")
def django_test_environment(django_test_environment):
    from django.apps import apps

    get_models = apps.get_models

    for m in [m for m in get_models() if not m._meta.managed]:
        m._meta.managed = True


pre_migrate.connect(app_pre_migration, sender=apps.get_app_config("geography"))
