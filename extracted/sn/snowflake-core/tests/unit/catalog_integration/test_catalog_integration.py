from unittest import mock

import pytest

from snowflake.core import PollingOperation
from snowflake.core.catalog_integration import (
    CatalogIntegration,
    CatalogIntegrationCollection,
    CatalogIntegrationResource,
    ObjectStore,
)
from snowflake.core.catalog_integration._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ...utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"
CATALOG_INTEGRATION = CatalogIntegration(
    name="my_catalog_integration", catalog=ObjectStore(), table_format="", enabled=False
)


@pytest.fixture()
def catalog_integrations(fake_root):
    return CatalogIntegrationCollection(fake_root)


@pytest.fixture()
def catalog_integration(catalog_integrations):
    return catalog_integrations["my_catalog_integration"]


def test_create_async(fake_root, catalog_integrations):
    args = (fake_root, "POST", BASE_URL + "/catalog-integrations")
    kwargs = extra_params(
        query_params=[],
        body={
            "name": "my_catalog_integration",
            "catalog": {"catalog_source": "OBJECT_STORE"},
            "table_format": "",
            "enabled": False,
        },
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        catalog_integration_res = catalog_integrations.create(CATALOG_INTEGRATION)
        assert isinstance(catalog_integration_res, CatalogIntegrationResource)
        assert catalog_integration_res.name == "my_catalog_integration"
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = catalog_integrations.create_async(CATALOG_INTEGRATION)
        assert isinstance(op, PollingOperation)
        catalog_integration_res = op.result()
        assert catalog_integration_res.name == "my_catalog_integration"
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_iter_async(fake_root, catalog_integrations):
    args = (fake_root, "GET", BASE_URL + "/catalog-integrations")
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

    model = CatalogIntegrationModel(
        name="my_catalog_integration", catalog=ObjectStoreModel(), table_format="", enabled=False
    )
    args = (fake_root, "GET", BASE_URL + "/catalog-integrations/my_catalog_integration")
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
    args = (fake_root, "DELETE", BASE_URL + "/catalog-integrations/my_catalog_integration")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        catalog_integration.drop()
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = catalog_integration.drop_async()
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_set_tags(fake_root, catalog_integration, tag):
    args = (fake_root, "POST", BASE_URL + "/catalog-integrations/my_catalog_integration:set-tags")
    tags = {tag: TagValue(value="value")}
    kwargs = extra_params(
        body=[
            TagAssignment(
                tag_value=v.value, tag_name=k.name, tag_schema=k.schema.name, tag_database=k.database.name
            ).to_dict()
            for k, v in tags.items()
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        catalog_integration.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = catalog_integration.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, catalog_integration, tag):
    args = (fake_root, "POST", BASE_URL + "/catalog-integrations/my_catalog_integration:unset-tags")
    tag_resources = {tag}
    kwargs = extra_params(
        body=[
            TagReference(
                tag_name=tag_res.name, tag_schema=tag_res.schema.name, tag_database=tag_res.database.name
            ).to_dict()
            for tag_res in tag_resources
        ]
    )

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        catalog_integration.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = catalog_integration.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, catalog_integration):
    args = (fake_root, "GET", BASE_URL + "/catalog-integrations/my_catalog_integration:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert catalog_integration.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = catalog_integration.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
