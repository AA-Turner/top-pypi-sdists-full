from collections.abc import Iterator

import pytest

from snowflake.core.api_integration import ApiIntegration, GitHook
from tests.integ.utils import random_string


@pytest.fixture(scope="module")
def secret(cursor) -> Iterator[str]:
    secret_name = random_string(10, "test_secret_")
    cursor.execute(f"CREATE SECRET IDENTIFIER('{secret_name}') TYPE = PASSWORD USERNAME = 'admin' PASSWORD = 'test'")
    try:
        yield secret_name
    finally:
        cursor.execute(f"DROP SECRET IF EXISTS IDENTIFIER('{secret_name}')")


def test_create_or_alter(api_integrations, secret, database, schema):
    ai_name = random_string(10, "test_api_integration_create_or_alter_")
    ai_def = ApiIntegration(
        name=ai_name,
        api_hook=GitHook(allow_any_secret=True),
        api_allowed_prefixes=["https://github.com"],
        enabled=True,
        api_blocked_prefixes=["https://github.com/snowflakedb/snowpy"],
        comment="created by test_create_or_alter",
    )
    ai = api_integrations[ai_name]
    ai.create_or_alter(ai_def)
    try:
        fetched_ai = ai.fetch()
        assert fetched_ai.name == ai_name.upper()
        assert isinstance(fetched_ai.api_hook, GitHook)

        fetched_ai.api_hook.allowed_authentication_secrets = [secret]
        fetched_ai.enabled = False
        fetched_ai.api_blocked_prefixes = None
        fetched_ai.comment = "altered by test_create_or_alter"

        ai.create_or_alter(fetched_ai)
        fetched_ai = ai.fetch()
        assert fetched_ai.name == ai_name.upper()
        assert isinstance(fetched_ai.api_hook, GitHook)
        assert fetched_ai.api_hook.allow_any_secret is False
        assert fetched_ai.api_hook.allowed_authentication_secrets == [
            f"{database.name.upper()}.{schema.name.upper()}.{secret.upper()}"
        ]
        assert (
            fetched_ai.api_hook.allowed_api_authentication_integrations
            == ai_def.api_hook.allowed_api_authentication_integrations
        )
        assert fetched_ai.api_allowed_prefixes == ai_def.api_allowed_prefixes
        assert fetched_ai.enabled is False
        # Simulated CoA doesn't support unsetting api_blocked_prefixes
        assert fetched_ai.api_blocked_prefixes == ai_def.api_blocked_prefixes
        assert fetched_ai.comment == "altered by test_create_or_alter"
    finally:
        ai.drop()
