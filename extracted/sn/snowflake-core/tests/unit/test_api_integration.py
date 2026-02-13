from typing import Any
from unittest import mock
from unittest.mock import MagicMock

import pytest

from snowflake.core import CreateMode, PollingOperation
from snowflake.core.api_integration import ApiIntegration, ApiIntegrationCollection, ApiIntegrationResource, AwsHook
from snowflake.core.api_integration._generated import TagAssignment, TagReference
from snowflake.core.tag import TagValue

from ..utils import BASE_URL, extra_params, mock_http_response


API_CLIENT_REQUEST = "snowflake.core._generated.api_client.ApiClient.request"


@pytest.fixture
def _mock_collection():
    return MagicMock(database=MagicMock())


@pytest.fixture
def _mock_api_integrations_collection(fake_root):
    return ApiIntegrationCollection(fake_root)


@pytest.fixture()
def api_integrations(fake_root):
    return ApiIntegrationCollection(fake_root)


@pytest.fixture()
def api_integration(api_integrations):
    return api_integrations["my_integration"]


@pytest.fixture
def _mock_api():
    with mock.patch(
        "snowflake.core.api_integration._generated.api.api_integration_api_base.ApiIntegrationApi"
    ) as mock_api:
        yield mock_api.return_value


def parametrize_if_exists():
    return pytest.mark.parametrize("if_exists", [True, False])


def parametrize_mode():
    return pytest.mark.parametrize("mode", [CreateMode.error_if_exists, CreateMode.if_not_exists])


def parametrize_async():
    return pytest.mark.parametrize("is_async", [True, False])


def get_method(resource: Any, name: str, is_async: bool):
    if is_async:
        return getattr(resource, f"{name}_async")
    return getattr(resource, name)


class TestApiIntegrationResource:
    @parametrize_async()
    def test_fetch_api_integration(self, _mock_collection, is_async):
        api_integration = ApiIntegrationResource(name="my_resource", collection=_mock_collection)
        get_method(api_integration, "fetch", is_async)()
        _mock_collection._api.fetch_api_integration.assert_called_once_with("my_resource", async_req=is_async)

    @parametrize_async()
    def test_create_or_alter_api_integration(self, _mock_collection, is_async):
        api_integration = ApiIntegration(
            name="name",
            api_hook=AwsHook(api_provider="AWS_API_GATEWAY", api_aws_role_arn="your_arn", api_key="dummy_api_key"),
            api_allowed_prefixes=["https://snowflake.com"],
            enabled=True,
        )

        resource = ApiIntegrationResource(name="my_resource", collection=_mock_collection)
        get_method(resource, "create_or_alter", is_async)(api_integration)
        _mock_collection._api.create_or_alter_api_integration.assert_called_once_with(
            api_integration.name, api_integration=api_integration, async_req=is_async
        )

    @parametrize_if_exists()
    @parametrize_async()
    def test_drop_api_integration(self, _mock_collection, if_exists, is_async):
        api_integration = ApiIntegrationResource(name="my_resource", collection=_mock_collection)
        get_method(api_integration, "drop", is_async)(if_exists=if_exists)
        _mock_collection._api.delete_api_integration.assert_called_once_with(
            "my_resource", if_exists=if_exists, async_req=is_async
        )


class TestApiIntegrationCollection:
    def test_schema_collection(self, fake_root):
        assert hasattr(fake_root, "api_integrations")

    @parametrize_async()
    def test_iter(self, _mock_api, fake_root, _mock_api_integrations_collection, is_async):
        get_method(_mock_api_integrations_collection, "iter", is_async)(like="%my_resource")

        _mock_api.list_api_integrations.assert_called_once_with(like="%my_resource", async_req=is_async)

    @parametrize_mode()
    @parametrize_async()
    def test_create_api_integration(self, _mock_api, _mock_api_integrations_collection, mode, is_async):
        api_integration = ApiIntegration(
            name="name",
            api_hook=AwsHook(api_provider="AWS_API_GATEWAY", api_aws_role_arn="your_arn", api_key="dummy_api_key"),
            api_allowed_prefixes=["https://snowflake.com"],
            enabled=True,
        )
        get_method(_mock_api_integrations_collection, "create", is_async)(api_integration=api_integration, mode=mode)

        _mock_api.create_api_integration.assert_called_once_with(
            api_integration=api_integration, create_mode=mode, async_req=is_async
        )


def test_set_tags(fake_root, api_integration, tag):
    args = (fake_root, "POST", BASE_URL + "/api-integrations/my_integration:set-tags")
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
        api_integration.set_tags(tags)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = api_integration.set_tags_async(tags)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_unset_tags(fake_root, api_integration, tag):
    args = (fake_root, "POST", BASE_URL + "/api-integrations/my_integration:unset-tags")
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
        api_integration.unset_tags(tag_resources)
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        op = api_integration.unset_tags_async(tag_resources)
        assert isinstance(op, PollingOperation)
        op.result()
    mocked_request.assert_called_once_with(*args, **kwargs)


def test_get_tags(fake_root, api_integration):
    args = (fake_root, "GET", BASE_URL + "/api-integrations/my_integration:get-tags")
    kwargs = extra_params()

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        assert api_integration.get_tags() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)

    with mock.patch(API_CLIENT_REQUEST) as mocked_request:
        mocked_request.return_value = mock_http_response()
        op = api_integration.get_tags_async()
        assert isinstance(op, PollingOperation)
        assert op.result() == {}
    mocked_request.assert_called_once_with(*args, **kwargs)
