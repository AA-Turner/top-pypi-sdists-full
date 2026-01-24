from datetime import date

import pytest
from faker import Faker
from pandas.tseries.offsets import BDay
from rest_framework.test import APIRequestFactory
from wbcore.configs.registry import ConfigRegistry
from wbcore.contrib.authentication.factories import UserFactory
from wbcore.contrib.geography.tests.conftest import *

fake = Faker()


def app_pre_migration(sender, app_config, **kwargs):
    cur = connection.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    cur.execute("CREATE EXTENSION IF NOT EXISTS btree_gin;")
    cur.execute("CREATE EXTENSION IF NOT EXISTS btree_gist;")


@pytest.fixture(autouse=True, scope="session")
def django_test_environment(django_test_environment):
    from django.apps import apps

    get_models = apps.get_models

    for m in [m for m in get_models() if not m._meta.managed]:
        m._meta.managed = True


@pytest.fixture()
def super_user():
    return UserFactory.create(is_superuser=True)


@pytest.fixture()
def weekday() -> date:
    return (fake.date_object() - BDay(0)).date()


pre_migrate.connect(app_pre_migration)


@pytest.fixture()
def config_registry():
    registry = ConfigRegistry()
    return registry

@pytest.fixture()
def api_request():
    return APIRequestFactory().get("/")

@pytest.fixture
def chrome_options(chrome_options):
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-extensions")
    return chrome_options
