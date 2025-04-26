import pytest

from snowflake.core.catalog_integration import CatalogIntegration, ObjectStore
from snowflake.core.exceptions import NotFoundError
from tests.integ.utils import random_string


pytestmark = [pytest.mark.min_sf_ver("8.37.0"),
            pytest.mark.usefixtures("internal_only", "setup_credentials_fixture")]

def test_drop(catalog_integrations):
    catalog_integration_name = random_string(10, "test_network_policy_")
    catalog_integration = CatalogIntegration(
        name = catalog_integration_name,
        catalog = ObjectStore(),
        table_format = "ICEBERG",
        enabled = True,
    )

    catalog_integration_handle = catalog_integrations.create(catalog_integration)

    fetch_handle = catalog_integration_handle.fetch()
    assert fetch_handle.name.upper() == catalog_integration_name.upper()

    catalog_integration_handle.drop()

    with pytest.raises(NotFoundError):
        catalog_integration_handle.fetch()

    catalog_integration_handle.drop(if_exists=True)
