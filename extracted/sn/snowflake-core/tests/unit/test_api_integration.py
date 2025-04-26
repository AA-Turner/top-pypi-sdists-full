from typing import Any
from unittest import mock
from unittest.mock import MagicMock

import pytest

from snowflake.core import CreateMode
from snowflake.core.api_integration import ApiIntegration, ApiIntegrationCollection, ApiIntegrationResource, AwsHook


@pytest.fixture
def _mock_collection():
    return MagicMock(database=MagicMock())


@pytest.fixture
def _mock_api_integrations_collection(fake_root):
    return ApiIntegrationCollection(fake_root)


@pytest.fixture
def _mock_api():
    with mock.patch("snowflake.core.api_integration._api_integration.ApiIntegrationApi") as mock_api:
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
        _mock_collection._api.fetch_api_integration.assert_called_once_with(
            "my_resource",
            async_req=is_async,
        )

    @parametrize_async()
    def test_create_or_alter_api_integration(self, _mock_collection, is_async):
        api_integration = ApiIntegration(
            name="name",
            api_hook=AwsHook(
                api_provider='AWS_API_GATEWAY',
                api_aws_role_arn="your_arn",
                api_key="dummy_api_key",
            ),
            api_allowed_prefixes=["https://snowflake.com"],
            enabled=True,
        )

        resource = ApiIntegrationResource(name="my_resource", collection=_mock_collection)
        get_method(resource, "create_or_alter", is_async)(api_integration)
        _mock_collection._api.create_or_alter_api_integration.assert_called_once_with(
            name=api_integration.name,
            api_integration=api_integration,
            async_req=is_async,
        )

    @parametrize_if_exists()
    @parametrize_async()
    def test_drop_api_integration(self, _mock_collection, if_exists, is_async):
        api_integration = ApiIntegrationResource(name="my_resource", collection=_mock_collection)
        get_method(api_integration, "drop", is_async)(if_exists=if_exists)
        _mock_collection._api.delete_api_integration.assert_called_once_with(
            "my_resource",
            if_exists=if_exists,
            async_req=is_async,
        )


class TestApiIntegrationCollection:
    def test_schema_collection(self, fake_root):
        assert hasattr(fake_root, "api_integrations")

    @parametrize_async()
    def test_iter(self, _mock_api, fake_root, _mock_api_integrations_collection, is_async):
        get_method(_mock_api_integrations_collection, "iter", is_async)(
            like="%my_resource",
        )

        _mock_api.list_api_integrations.assert_called_once_with(
            like="%my_resource",
            async_req=is_async,
        )

    @parametrize_mode()
    @parametrize_async()
    def test_create_api_integration(self, _mock_api, _mock_api_integrations_collection, mode, is_async):
        api_integration = ApiIntegration(
            name="name",
            api_hook=AwsHook(
                api_provider='AWS_API_GATEWAY',
                api_aws_role_arn="your_arn",
                api_key="dummy_api_key",
            ),
            api_allowed_prefixes=["https://snowflake.com"],
            enabled=True,
        )
        get_method(_mock_api_integrations_collection, "create", is_async)(
            api_integration=api_integration,
            mode=mode,
        )

        _mock_api.create_api_integration.assert_called_once_with(
            api_integration,
            create_mode=mode,
            async_req=is_async,
        )
