"""``from_env``: the one reader of the ``COMPOSIO_*`` variables.

The constructor reads nothing from the process. ``from_env`` takes the mapping
as an argument, turns the three credential variables into ``auth`` through
``auth_from_credentials``, and lets each keyword it is given replace the field
it names.
"""

from __future__ import annotations

import httpx
import pytest

from composio_client import (
    AsyncComposio,
    AutoAuth,
    Composio,
    ComposioError,
    EnvironmentMap,
    NoAuth,
    OrganizationAuth,
    ProjectAuth,
    Scope,
    UserAuth,
    auth_from_credentials,
)


def _recording_client() -> tuple[httpx.Client, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"ok": True})

    return httpx.Client(transport=httpx.MockTransport(handle)), requests


def test_sync_factory_uses_only_the_supplied_environment_snapshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("COMPOSIO_BASE_URL", "https://ambient.example.test")
    monkeypatch.setenv("COMPOSIO_API_KEY", "ambient-key")
    monkeypatch.setenv("COMPOSIO_CUSTOM_HEADERS", "x-ambient: present")
    http_client, requests = _recording_client()

    environment: EnvironmentMap = {
        "COMPOSIO_BASE_URL": " https://mapped.example.test/ ",
        "COMPOSIO_API_KEY": " mapped-key ",
        "COMPOSIO_CUSTOM_HEADERS": "x-mapped: present",
    }
    client = Composio.from_env(environment, http_client=http_client)

    result = client.get("/api/v3.1/tools")

    assert result == {"ok": True}
    assert client.base_url == "https://mapped.example.test"
    assert client.auth_mode == "project"
    assert requests[0].headers["x-api-key"] == "mapped-key"
    assert requests[0].headers["x-mapped"] == "present"
    assert "x-ambient" not in requests[0].headers
    client.close()


def test_an_override_replaces_the_whole_field_it_names() -> None:
    http_client, requests = _recording_client()
    client = Composio.from_env(
        {
            "COMPOSIO_BASE_URL": "https://mapped.example.test",
            "COMPOSIO_API_KEY": "mapped-key",
            "COMPOSIO_USER_API_KEY": "mapped-user-key",
            "COMPOSIO_CUSTOM_HEADERS": "x-remove: mapped\nx-mapped: present",
        },
        auth=NoAuth(),
        environment="staging",
        default_headers={"x-explicit": "present"},
        http_client=http_client,
    )

    result = client.get("/api/v3.1/tools")

    assert result == {"ok": True}
    assert client.base_url == "https://staging-backend.composio.dev"
    assert client.auth_mode == "none"
    assert "x-api-key" not in requests[0].headers
    assert "x-user-api-key" not in requests[0].headers
    # `default_headers=` replaces COMPOSIO_CUSTOM_HEADERS, it does not merge.
    assert "x-remove" not in requests[0].headers
    assert "x-mapped" not in requests[0].headers
    assert requests[0].headers["x-explicit"] == "present"
    client.close()


def test_the_constructor_reads_nothing_from_the_process(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("COMPOSIO_BASE_URL", "https://ambient.example.test")
    monkeypatch.setenv("COMPOSIO_API_KEY", "ambient-key")
    monkeypatch.setenv("COMPOSIO_CUSTOM_HEADERS", "x-ambient: present")
    client = Composio(auth=NoAuth())

    assert client.base_url == "https://backend.composio.dev"
    assert "x-ambient" not in client.default_headers
    client.close()


def test_sync_factory_empty_snapshot_does_not_fall_back_to_process_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("COMPOSIO_BASE_URL", "https://ambient.example.test")
    monkeypatch.setenv("COMPOSIO_API_KEY", "ambient-key")
    monkeypatch.setenv("COMPOSIO_CUSTOM_HEADERS", "x-ambient: present")
    client = Composio.from_env({})
    derived = client.with_options(max_retries=0)

    assert derived.base_url == "https://backend.composio.dev"
    assert derived.auth_mode == "none"
    assert "x-ambient" not in derived.default_headers
    derived.close()
    client.close()


@pytest.mark.parametrize(
    ("variables", "expected"),
    [
        ({}, NoAuth()),
        ({"COMPOSIO_API_KEY": "ak"}, ProjectAuth("ak")),
        ({"COMPOSIO_USER_API_KEY": "uak"}, UserAuth("uak")),
        ({"COMPOSIO_ORG_API_KEY": "oak"}, OrganizationAuth("oak")),
        ({"COMPOSIO_API_KEY": "ak", "COMPOSIO_USER_API_KEY": "uak"}, AutoAuth(project="ak", user="uak")),
        (
            {"COMPOSIO_API_KEY": "ak", "COMPOSIO_USER_API_KEY": "uak", "COMPOSIO_ORG_API_KEY": "oak"},
            AutoAuth(project="ak", user="uak", organization="oak"),
        ),
        # Empty and blank values are absent.
        ({"COMPOSIO_API_KEY": "  ", "COMPOSIO_USER_API_KEY": "uak"}, UserAuth("uak")),
    ],
)
def test_the_credential_variables_become_auth_by_one_rule(
    variables: dict[str, str], expected: object
) -> None:
    client = Composio.from_env(variables)
    try:
        assert client._auth == expected
        assert client._auth == auth_from_credentials(
            project=variables.get("COMPOSIO_API_KEY", "").strip() or None,
            user=variables.get("COMPOSIO_USER_API_KEY", "").strip() or None,
            organization=variables.get("COMPOSIO_ORG_API_KEY", "").strip() or None,
        )
    finally:
        client.close()


def test_scope_ids_are_not_read_from_the_environment() -> None:
    client = Composio.from_env(
        {"COMPOSIO_API_KEY": "ak", "COMPOSIO_ORG_ID": "org_1", "COMPOSIO_PROJECT_ID": "pr_1"}
    )
    explicit = Composio.from_env({"COMPOSIO_API_KEY": "ak"}, scope=Scope(project_id="pr_2"))
    try:
        assert client.scope is None
        assert explicit.scope == Scope(project_id="pr_2")
    finally:
        client.close()
        explicit.close()


def test_custom_headers_are_held_to_the_reserved_rule() -> None:
    with pytest.raises(ComposioError, match=r"`x-api-key` header is set by `auth`"):
        Composio.from_env({"COMPOSIO_API_KEY": "ak", "COMPOSIO_CUSTOM_HEADERS": "x-api-key: other"})
    with pytest.raises(ComposioError, match=r"`x-org-id` header is set by `scope`"):
        Composio.from_env(
            {"COMPOSIO_CUSTOM_HEADERS": "x-org-id: org_2"}, scope=Scope(organization_id="org_1")
        )
    # With neither configured they are ordinary headers.
    client = Composio.from_env({"COMPOSIO_CUSTOM_HEADERS": "x-api-key: dashboard\nx-project-id: pr_1"})
    try:
        assert client.default_headers == {"x-api-key": "dashboard", "x-project-id": "pr_1"}
    finally:
        client.close()


def test_base_url_and_environment_together_are_ambiguous() -> None:
    with pytest.raises(ValueError, match="cannot be used together"):
        Composio.from_env({}, base_url="https://a.test", environment="staging")


async def test_async_factory_returns_an_async_client() -> None:
    client = AsyncComposio.from_env(
        {"COMPOSIO_API_KEY": "mapped-key"},
        environment="local",
    )

    assert isinstance(client, AsyncComposio)
    assert client.base_url == "http://localhost:9900"
    await client.close()
