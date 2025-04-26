from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.catalog_integration import CatalogIntegration, CatalogIntegrationCollection, ObjectStore

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core.catalog_integration._generated.api_client.ApiClient.request"
CATALOG_INTEGRATION = CatalogIntegration(
    name="my_catalog_integration", catalog=ObjectStore(), table_format="", enabled=False)


@pytest.fixture()
def catalog_integrations(fake_root):
    return CatalogIntegrationCollection(fake_root)


@pytest.fixture()
def catalog_integration(catalog_integrations):
    return catalog_integrations["my_catalog_integration"]


def test_create_async(fake_root, catalog_integrations):
    args = (
        fake_root,
        "POST",
        BASE_URL + "/catalog-integrations?createMode=errorIfExists",
    )
    kwargs = extra_params(
        query_params=[("createMode", "errorIfExists")],
        body={
            "name": "my_catalog_integration",
            "catalog": {"catalog_source": "OBJECT_STORE"},
            "table_format": "",
            "enabled": False,
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        catalog_integration_res = catalog_integrations.create(CATALOG_INTEGRATION)
        assert catalog_integration_res.name == "my_catalog_integration"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = catalog_integrations.create_async(CATALOG_INTEGRATION)
        assert isinstance(op, PollingOperation)
        catalog_integration_res = op.result()
        assert catalog_integration_res.name == "my_catalog_integration"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_async(fake_root, catalog_integrations):
    args = (
        fake_root,
        "GET",
        BASE_URL + "/catalog-integrations",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        it = catalog_integrations.iter()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = catalog_integrations.iter_async()
        assert isinstance(op, PollingOperation)
        it = op.result()
        assert list(it) == []
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_fetch_async(fake_root, catalog_integration):
    from snowflake.core.catalog_integration._generated.models import CatalogIntegration as CatalogIntegrationModel
    from snowflake.core.catalog_integration._generated.models import ObjectStore as ObjectStoreModel


    model = CatalogIntegrationModel(name="my_catalog_integration", catalog=ObjectStoreModel(), table_format="",
                                    enabled=False)
    args = (
        fake_root,
        "GET",
        BASE_URL + "/catalog-integrations/my_catalog_integration",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        my_catalog_integration = catalog_integration.fetch()
        assert my_catalog_integration.to_dict() == CATALOG_INTEGRATION.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response(model.to_json())
        op = catalog_integration.fetch_async()
        assert isinstance(op, PollingOperation)
        my_catalog_integration = op.result()
        assert my_catalog_integration.to_dict() == CATALOG_INTEGRATION.to_dict()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_drop_async(fake_root, catalog_integration):
    args = (
        fake_root,
        "DELETE",
        BASE_URL + "/catalog-integrations/my_catalog_integration",
    )
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        catalog_integration.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = catalog_integration.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)
