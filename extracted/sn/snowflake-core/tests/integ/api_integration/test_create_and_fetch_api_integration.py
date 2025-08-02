import pytest

from snowflake.core.api_integration import ApiIntegration, AwsHook, AzureHook, GitHook, GoogleCloudHook
from tests.integ.utils import random_string


@pytest.mark.prodlike_only
@pytest.mark.skip_gov
def test_create_and_fetch_aws(api_integrations):
    ai_name = random_string(10, "test_api_integration_create_")
    ai_def = ApiIntegration(
        name=ai_name,
        api_hook=AwsHook(
            api_provider="AWS_API_GATEWAY",
            api_aws_role_arn="arn:aws:iam::123456789012:role/fake_role",
            api_key="secret",
        ),
        api_allowed_prefixes=["https://xyz.execute-api.us-west-2.amazonaws.com/test"],
        enabled=True,
        comment="created by test_create_and_fetch_aws",
    )
    ai = api_integrations.create(ai_def)
    try:
        fetched_ai = ai.fetch()
        assert fetched_ai.name == ai_name.upper()
        assert isinstance(fetched_ai.api_hook, AwsHook)
        assert fetched_ai.api_hook.api_provider == ai_def.api_hook.api_provider
        assert fetched_ai.api_hook.api_aws_role_arn == ai_def.api_hook.api_aws_role_arn
        assert fetched_ai.api_hook.api_key is not None
        assert fetched_ai.api_allowed_prefixes == ai_def.api_allowed_prefixes
        assert fetched_ai.enabled is ai_def.enabled
        assert fetched_ai.api_blocked_prefixes is None
        assert fetched_ai.comment == ai_def.comment
    finally:
        ai.drop()


@pytest.mark.prodlike_only
def test_create_and_fetch_azure(api_integrations):
    ai_name = random_string(10, "test_api_integration_create_")
    ai_def = ApiIntegration(
        name=ai_name,
        api_hook=AzureHook(
            api_provider="AZURE_API_MANAGEMENT",
            azure_tenant_id="azsnowtestoutlook.onmicrosoft.com",
            azure_ad_application_id="dummy_app_id",
        ),
        api_allowed_prefixes=["https://ext-func-test.azure-api.net/echo"],
        enabled=True,
        comment="created by test_create_and_fetch_azure",
    )
    ai = api_integrations.create(ai_def)
    try:
        fetched_ai = ai.fetch()
        assert fetched_ai.name == ai_name.upper()
        assert isinstance(fetched_ai.api_hook, AzureHook)
        assert fetched_ai.api_hook.api_provider == ai_def.api_hook.api_provider
        assert fetched_ai.api_hook.azure_tenant_id == ai_def.api_hook.azure_tenant_id
        assert fetched_ai.api_hook.azure_ad_application_id == ai_def.api_hook.azure_ad_application_id
        assert fetched_ai.api_hook.api_key is None
        assert fetched_ai.api_allowed_prefixes == ai_def.api_allowed_prefixes
        assert fetched_ai.enabled is ai_def.enabled
        assert fetched_ai.api_blocked_prefixes is None
        assert fetched_ai.comment == ai_def.comment
    finally:
        ai.drop()


@pytest.mark.prodlike_only
def test_create_and_fetch_gc(api_integrations):
    ai_name = random_string(10, "test_api_integration_create_")
    ai_def = ApiIntegration(
        name=ai_name,
        api_hook=GoogleCloudHook(api_provider="GOOGLE_API_GATEWAY", google_audience="dummy_aud"),
        api_allowed_prefixes=["https://fake.uc.gateway.dev"],
        enabled=True,
        comment="created by test_create_and_fetch_gc",
    )
    ai = api_integrations.create(ai_def)
    try:
        fetched_ai = ai.fetch()
        assert fetched_ai.name == ai_name.upper()
        assert isinstance(fetched_ai.api_hook, GoogleCloudHook)
        assert fetched_ai.api_hook.api_provider == ai_def.api_hook.api_provider
        assert fetched_ai.api_hook.google_audience == ai_def.api_hook.google_audience
        assert fetched_ai.api_hook.api_key is None
        assert fetched_ai.api_allowed_prefixes == ai_def.api_allowed_prefixes
        assert fetched_ai.enabled is ai_def.enabled
        assert fetched_ai.api_blocked_prefixes is None
        assert fetched_ai.comment == ai_def.comment
    finally:
        ai.drop()


def test_create_and_fetch_git(api_integrations):
    ai_name = random_string(10, "test_api_integration_create_")
    ai_def = ApiIntegration(
        name=ai_name,
        api_hook=GitHook(allow_any_secret=True),
        api_allowed_prefixes=["https://github.com"],
        enabled=False,
        api_blocked_prefixes=["https://github.com/snowflakedb/snowpy"],
        comment="created by test_create_and_fetch_git",
    )
    ai = api_integrations.create(ai_def)
    try:
        fetched_ai = ai.fetch()
        assert fetched_ai.name == ai_name.upper()
        assert isinstance(fetched_ai.api_hook, GitHook)
        assert fetched_ai.api_hook.allow_any_secret is ai_def.api_hook.allow_any_secret
        assert fetched_ai.api_hook.allowed_authentication_secrets is None
        assert fetched_ai.api_hook.allowed_api_authentication_integrations is None
        assert fetched_ai.api_allowed_prefixes == ai_def.api_allowed_prefixes
        assert fetched_ai.enabled is ai_def.enabled
        assert fetched_ai.api_blocked_prefixes == ai_def.api_blocked_prefixes
        assert fetched_ai.comment == ai_def.comment
    finally:
        ai.drop()
