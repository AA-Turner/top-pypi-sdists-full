from contextlib import suppress

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.catalog_integration import CatalogIntegration, Glue, OAuth, ObjectStore, Polaris, RestConfig
from snowflake.core.exceptions import ConflictError, NotFoundError
from tests.integ.utils import random_string


pytestmark = [pytest.mark.min_sf_ver("8.37.0"),
            pytest.mark.usefixtures("internal_only", "setup_credentials_fixture")]


def test_create_by_glue_and_fetch(catalog_integrations):
    catalog_integration_name = random_string(10, "test_catalog_integration_")

    catalog_integration = CatalogIntegration(
        name=catalog_integration_name,
        catalog = Glue(
            catalog_namespace="abcd-ns",
            glue_aws_role_arn="arn:aws:iam::123456789012:role/sqsAccess",
            glue_catalog_id="1234567",
        ),
        table_format="ICEBERG",
        enabled=True,
    )

    catalog_integration_handle = catalog_integrations.create(catalog_integration)

    try:
        fetch_handle = catalog_integration_handle.fetch()

        assert fetch_handle.name.upper() == catalog_integration_name.upper()
        assert isinstance(fetch_handle.catalog, Glue)
        assert fetch_handle.catalog.catalog_namespace == catalog_integration.catalog.catalog_namespace
        assert fetch_handle.catalog.glue_aws_role_arn == catalog_integration.catalog.glue_aws_role_arn
        assert fetch_handle.catalog.glue_catalog_id == catalog_integration.catalog.glue_catalog_id
        assert fetch_handle.table_format == catalog_integration.table_format
        assert fetch_handle.enabled == catalog_integration.enabled

    finally:
        with suppress(NotFoundError):
            catalog_integration_handle.drop()


def test_create_by_object_store_and_fetch(catalog_integrations):
    catalog_integration_name = random_string(10, "test_catalog_integration_")

    catalog_integration = CatalogIntegration(
        name=catalog_integration_name,
        catalog = ObjectStore(),
        table_format="ICEBERG",
        enabled=True,
    )

    catalog_integration_handle = catalog_integrations.create(catalog_integration)

    try:
        fetch_handle = catalog_integration_handle.fetch()

        assert fetch_handle.name.upper() == catalog_integration_name.upper()
        assert isinstance(fetch_handle.catalog, ObjectStore)
        assert fetch_handle.table_format == catalog_integration.table_format
        assert fetch_handle.enabled == catalog_integration.enabled
    finally:
        with suppress(NotFoundError):
            catalog_integration_handle.drop()


def test_create_by_polaris_and_fetch(catalog_integrations, set_internal_params):
    catalog_integration_name = random_string(10, "test_catalog_integration_")

    with set_internal_params({'ENABLE_FIX_1692844_ENABLE_VALIDATION_ON_CATALOG_INT_CREATION': False}):
        catalog_integration = CatalogIntegration(
            name = catalog_integration_name,
            catalog = Polaris(
                catalog_namespace="abcd-ns",
                rest_config=RestConfig(
                    catalog_uri="https://my_account.snowflakecomputing.com/polaris/api/catalog",
                    warehouse="my-warehouse",
                ),
                rest_authentication=OAuth(
                    type="OAUTH",
                    oauth_client_id="my_client_id",
                    oauth_client_secret="my_client_secret",
                    oauth_allowed_scopes=["PRINCIPAL_ROLE:ALL"],
                ),
            ),
            table_format="ICEBERG",
            enabled=True
        )

        catalog_integration_handle = catalog_integrations.create(catalog_integration)

        try:
            fetch_handle = catalog_integration_handle.fetch()

            assert fetch_handle.name.upper() == catalog_integration_name.upper()
            assert isinstance(fetch_handle.catalog, Polaris)
            assert fetch_handle.catalog.catalog_namespace == catalog_integration.catalog.catalog_namespace
            assert fetch_handle.catalog.rest_config.catalog_uri == catalog_integration.catalog.rest_config.catalog_uri
            assert fetch_handle.catalog.rest_config.warehouse == catalog_integration.catalog.rest_config.warehouse
            assert fetch_handle.catalog.rest_authentication.oauth_client_id ==\
                catalog_integration.catalog.rest_authentication.oauth_client_id
            assert fetch_handle.catalog.rest_authentication.oauth_client_secret == ""
            assert fetch_handle.catalog.rest_authentication.oauth_allowed_scopes ==\
                catalog_integration.catalog.rest_authentication.oauth_allowed_scopes
            assert fetch_handle.table_format == catalog_integration.table_format
            assert fetch_handle.enabled == catalog_integration.enabled
        finally:
            with suppress(NotFoundError):
                catalog_integration_handle.drop()


def test_create_mode(catalog_integrations):
    catalog_integration_name = random_string(10, "test_catalog_integration_")

    catalog_integration = CatalogIntegration(
        name=catalog_integration_name,
        catalog = ObjectStore(),
        table_format="ICEBERG",
        enabled=True,
    )

    catalog_integrations.create(catalog_integration)

    with pytest.raises(ConflictError):
        catalog_integrations.create(catalog_integration)

    catalog_integrations.create(
        catalog_integration,
        mode = CreateMode.or_replace
    )
