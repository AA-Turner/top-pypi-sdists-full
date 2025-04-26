from contextlib import suppress

import pytest

from snowflake.core.catalog_integration import CatalogIntegration, ObjectStore
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string

from ...utils import ensure_snowflake_version


CATALOG_INTEGRATION_PREFIX = random_string(10, 'test_catalog_integration_iter_')

@pytest.fixture(scope='session')
def catalog_integrations_extended(catalog_integrations, snowflake_version):
    ensure_snowflake_version(snowflake_version, "8.37.0")

    name_list = []
    for _ in range(5):
        name_list.append(random_string(10, CATALOG_INTEGRATION_PREFIX + 'a_'))
    for _ in range(7):
        name_list.append(random_string(10, CATALOG_INTEGRATION_PREFIX + 'b_'))
    for _ in range(3):
        name_list.append(random_string(10, CATALOG_INTEGRATION_PREFIX + 'c_'))

    for catalog_integration_name in name_list:
        catalog_integrations.create(CatalogIntegration(
            name=catalog_integration_name,
            catalog = ObjectStore(),
            table_format = "ICEBERG",
            enabled = True,
        ))

    try:
        yield catalog_integrations
    finally:
        for catalog_integration_name in name_list:
            with suppress(NotFoundError):
                catalog_integrations[catalog_integration_name].drop()

def test_iter_raw(catalog_integrations_extended):
    assert len(list(catalog_integrations_extended.iter())) >= 15


def test_iter_like(catalog_integrations_extended):
    assert len(list(catalog_integrations_extended.iter(like="test_catalog_integration_iter_"))) == 0
    assert len(list(catalog_integrations_extended.iter(like=CATALOG_INTEGRATION_PREFIX + "a_%%"))) == 5
    assert len(list(catalog_integrations_extended.iter(like=CATALOG_INTEGRATION_PREFIX + "b_%%"))) == 7
    assert len(list(catalog_integrations_extended.iter(like=CATALOG_INTEGRATION_PREFIX + "c_%%"))) == 3
