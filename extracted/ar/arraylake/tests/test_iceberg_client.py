"""Client/CLI contracts that do not require a running Arraylake service."""

import asyncio
import base64
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import Mock
from uuid import uuid4

import httpx
import pytest
from typer.testing import CliRunner

from arraylake import AsyncClient, Client
from arraylake.cli.main import app
from arraylake.types import IcebergNamespaceActions, IcebergNamespaceResponse, RepoVisibility

URL = "https://example.test"
NS_URL = f"{URL}/orgs/my-org/iceberg/namespaces"


def namespace(name="observations"):
    return dict(
        id=str(uuid4()),
        org="my-org",
        name=name,
        prefix="abc/observations",
        created="2026-09-09T00:00:00Z",
        updated="2026-09-09T00:00:00Z",
        effective_actions=["CAN_READ"],
        table_count=2,
    )


@pytest.fixture
def http_routes(respx_mock):
    respx_mock.post(f"{URL}/user/diagnostics").respond(200, json={})
    return respx_mock


async def test_management_roundtrip(http_routes, test_token):
    create = http_routes.post(NS_URL).respond(201, json=namespace())
    get = http_routes.get(f"{NS_URL}/observations").respond(200, json=namespace())
    patch = http_routes.patch(f"{NS_URL}/observations").respond(200, json=namespace())
    restore = http_routes.post(f"{NS_URL}/observations/restore").respond(204)
    client = AsyncClient(URL, token=test_token)
    await client.create_iceberg_namespace(
        "my-org",
        "observations",
        bucket_config_nickname="bucket",
        description="Weather",
        metadata={"count": 0, "public": False},
        properties={"owner": "science"},
        visibility=RepoVisibility.AUTHENTICATED_PUBLIC,
    )
    assert json.loads(create.calls.last.request.content) == {
        "name": "observations",
        "bucket_nickname": "bucket",
        "description": "Weather",
        "metadata": {"count": 0, "public": False},
        "properties": {"owner": "science"},
        "visibility": "AUTHENTICATED_PUBLIC",
    }
    result = await client.get_iceberg_namespace("my-org", "observations")
    assert result.effective_actions == {IcebergNamespaceActions.CAN_READ}
    await client.modify_iceberg_namespace(
        "my-org",
        "observations",
        description="",
        add_metadata={"a": 0},
        remove_metadata=["old"],
        update_metadata={"b": False},
        visibility=RepoVisibility.PRIVATE,
    )
    assert json.loads(patch.calls.last.request.content) == {
        "description": "",
        "add_metadata": {"a": 0},
        "remove_metadata": ["old"],
        "update_metadata": {"b": False},
        "visibility": "PRIVATE",
    }
    await client.restore_iceberg_namespace("my-org", "observations")
    assert get.called and restore.called


def test_sync_management(http_routes, test_token):
    http_routes.post(NS_URL).respond(201, json=namespace())
    http_routes.get(f"{NS_URL}/observations").respond(200, json=namespace())
    patch = http_routes.patch(f"{NS_URL}/observations").respond(200, json=namespace())
    restore = http_routes.post(f"{NS_URL}/observations/restore").respond(204)
    client = Client(URL, token=test_token)
    assert client.create_iceberg_namespace("my-org", "observations", description="hello").name == "observations"
    assert client.get_iceberg_namespace("my-org", "observations").table_count == 2
    client.modify_iceberg_namespace("my-org", "observations", description="updated")
    assert json.loads(patch.calls.last.request.content) == {"description": "updated"}
    client.restore_iceberg_namespace("my-org", "observations")
    assert restore.called


@pytest.mark.parametrize("kind", ["namespaces", "tables"])
@pytest.mark.parametrize("sync_client", [False, True])
async def test_pagination_is_lazy_and_preserves_filters(http_routes, test_token, kind, sync_client):
    url = f"{NS_URL}/paginated" if kind == "namespaces" else f"{NS_URL}/observations/tables/paginated"

    def respond(request):
        page = int(request.url.params["page"])
        row = (
            namespace(f"item-{page}")
            if kind == "namespaces"
            else dict(
                name=f"item-{page}",
                namespace="observations",
                table_uuid=str(uuid4()),
                created="2026-09-09T00:00:00Z",
                updated="2026-09-09T00:00:00Z",
                effective_actions=["CAN_READ"],
            )
        )
        return httpx.Response(200, json=dict(items=[row], page=page, pages=2, size=1, total=2))

    route = http_routes.get(url).mock(side_effect=respond)
    client = Client(URL, token=test_token) if sync_client else AsyncClient(URL, token=test_token)
    args = ("my-org",) if kind == "namespaces" else ("my-org", "observations")
    kwargs = dict(search="item", sort="updated", direction="asc", page_size=1)
    if kind == "namespaces":
        kwargs.update(filter_metadata={"active": False}, include_ghosts=True)
    iterator = getattr(client, f"list_iceberg_{kind}_paginated")(*args, **kwargs)
    assert not route.called
    first = next(iterator) if sync_client else await anext(iterator)
    assert first.name == "item-1" and route.call_count == 1
    rest = list(iterator) if sync_client else [row async for row in iterator]
    assert [row.name for row in rest] == ["item-2"]
    params = route.calls.last.request.url.params
    assert params["search"] == "item" and params["sort"] == "updated" and params["direction"] == "asc"
    assert params["size"] == "1" and params["page"] == "2"
    if kind == "namespaces":
        assert json.loads(params["filter_metadata"]) == {"active": False}
        assert params["include_ghosts"] == "true"


async def test_ghost_listing_and_empty_filtered_results(http_routes, test_token):
    ghosts = http_routes.get(NS_URL).respond(200, json=[namespace()])
    filtered = http_routes.get(f"{NS_URL}/paginated").respond(200, json=dict(items=[], page=1, pages=0, size=50, total=0))
    client = AsyncClient(URL, token=test_token)
    assert len(await client.list_iceberg_namespaces("my-org", include_ghosts=True)) == 1
    assert ghosts.calls.last.request.url.params["include_ghosts"] == "true"
    assert await client.list_iceberg_namespaces("my-org", search="missing") == []
    assert filtered.call_count == 1
    with pytest.raises(ValueError, match="page_size"):
        await anext(client.list_iceberg_namespaces_paginated("my-org", page_size=0))


async def test_catalog_construction_does_not_block_event_loop(monkeypatch, test_token):
    import arraylake.repos.iceberg

    caller = threading.get_ident()
    entered = threading.Event()
    release = threading.Event()
    sentinel = object()

    def construct(**kwargs):
        assert threading.get_ident() != caller
        entered.set()
        assert release.wait(3)
        return sentinel

    monkeypatch.setattr(arraylake.repos.iceberg, "get_iceberg_catalog", construct)
    task = asyncio.create_task(AsyncClient(URL, token=test_token).get_iceberg("my-org"))
    try:
        assert await asyncio.to_thread(entered.wait, 2)
    finally:
        release.set()
    assert await task is sentinel


def jwt(expires_at):
    payload = base64.urlsafe_b64encode(json.dumps({"exp": expires_at}).encode()).decode().rstrip("=")
    return f"header.{payload}.signature"


def set_login(path, token):
    data = json.loads(path.read_text())
    data["id_token"] = token
    path.write_text(json.dumps(data))


def test_login_refresh_is_shared_across_catalogs(monkeypatch, test_token_file, capsys):
    pytest.importorskip("pyiceberg")
    from arraylake.repos.iceberg import auth
    from arraylake.types import OauthTokensResponse

    set_login(test_token_file, jwt(time.time() - 1))
    refreshed_token = jwt(time.time() + 3600)
    refreshes = []

    async def refresh(handler):
        refreshes.append(1)
        handler.update(
            OauthTokensResponse(access_token="new", id_token=refreshed_token, refresh_token="rotated", expires_in=3600, token_type="Bearer")
        )

    monkeypatch.setattr(auth, "_refresh_login", refresh)
    managers = [auth.ArraylakeAuthManager(URL) for _ in range(8)]
    with ThreadPoolExecutor(max_workers=8) as pool:
        headers = list(pool.map(lambda manager: manager.auth_header(), managers))
    assert headers == [f"Bearer {refreshed_token}"] * 8
    assert len(refreshes) == 1
    assert json.loads(test_token_file.read_text())["refresh_token"] == "rotated"
    assert capsys.readouterr().out == ""
    # Subsequent requests pick up a login renewed outside the catalog.
    external_token = jwt(time.time() + 7200)
    set_login(test_token_file, external_token)
    assert managers[0].auth_header() == f"Bearer {external_token}"


async def test_refresh_failure_does_not_overwrite_login(http_routes, monkeypatch, test_token_file):
    pytest.importorskip("pyiceberg")
    from arraylake.exceptions import AuthException
    from arraylake.repos.iceberg.auth import _refresh_login
    from arraylake.token import TokenHandler

    async def request(self):
        return httpx.Request("POST", f"{URL}/refresh")

    monkeypatch.setattr(TokenHandler, "build_refresh_request", request)
    http_routes.post(f"{URL}/refresh").respond(401, json={"error": "invalid_grant"})
    before = test_token_file.read_text()
    with pytest.raises(AuthException, match="al auth login"):
        await _refresh_login(TokenHandler(URL))
    assert test_token_file.read_text() == before


def test_real_catalog_uses_auth_manager(monkeypatch, test_token_file):
    pytest.importorskip("pyiceberg")
    from requests import Response, Session

    from arraylake.repos.iceberg.catalog import get_iceberg_catalog

    set_login(test_token_file, jwt(time.time() + 3600))
    headers = []

    def send(self, request, **kwargs):
        headers.append(request.headers["Authorization"])
        response = Response()
        response.status_code = 200
        response._content = b'{"defaults": {}, "overrides": {}}' if "/config" in request.url else b'{"namespaces": []}'
        return response

    monkeypatch.setattr(Session, "send", send)
    catalog = get_iceberg_catalog(name="my-org", service_uri=URL, warehouse="my-org", token=None)
    renewed = jwt(time.time() + 7200)
    set_login(test_token_file, renewed)
    assert catalog.list_namespaces() == []
    assert headers[-1] == f"Bearer {renewed}" and headers[0] != headers[-1]
    catalog.close()
    machine = get_iceberg_catalog(name="my-org", service_uri=URL, warehouse="my-org", token="ema_static")
    assert headers[-1] == "Bearer ema_static"
    machine.close()


@pytest.fixture
def cli_client(monkeypatch):
    client = Mock()
    client.get_iceberg_namespace.return_value = IcebergNamespaceResponse.model_validate(namespace())
    client.create_iceberg_namespace.return_value = client.get_iceberg_namespace.return_value
    client.modify_iceberg_namespace.return_value = client.get_iceberg_namespace.return_value
    client.list_iceberg_namespaces_paginated.return_value = iter([client.get_iceberg_namespace.return_value])
    monkeypatch.setattr("arraylake.cli.iceberg.Client", lambda: client)
    return client


def test_cli_namespace_commands(cli_client):
    runner = CliRunner()
    for command in [
        ["get", "my-org", "observations"],
        ["create", "my-org", "observations", "--metadata", '{"count": 0}', "--visibility", "AUTHENTICATED_PUBLIC"],
        ["update", "my-org", "observations", "--description", "", "--remove-metadata", "old"],
        ["list", "my-org", "--search", "obs", "--sort", "relevance", "--include-ghosts"],
    ]:
        result = runner.invoke(app, ["iceberg", "namespace", *command, "--output", "json"])
        assert result.exit_code == 0, result.exception
        assert json.loads(result.stdout)
    assert cli_client.create_iceberg_namespace.call_args.kwargs["metadata"] == {"count": 0}
    assert cli_client.modify_iceberg_namespace.call_args.kwargs["description"] == ""
    assert cli_client.list_iceberg_namespaces_paginated.call_args.kwargs["include_ghosts"] is True
    result = runner.invoke(app, ["iceberg", "namespace", "restore", "my-org", "observations"])
    assert result.exit_code == 0
    cli_client.restore_iceberg_namespace.assert_called_once_with("my-org", "observations")


def test_cli_delete_confirmation_and_validation(cli_client):
    runner = CliRunner()
    args = ["iceberg", "namespace", "delete", "my-org", "observations"]
    result = runner.invoke(app, args, input="n\n")
    assert result.exit_code != 0
    cli_client.delete_iceberg_namespace.assert_not_called()
    assert runner.invoke(app, [*args, "--confirm"]).exit_code == 0
    cli_client.delete_iceberg_namespace.assert_called_once_with("my-org", "observations", imsure=True, immediate=False, retain_data=False)
    cli_client.delete_iceberg_namespace.reset_mock()
    assert runner.invoke(app, [*args, "--confirm", "--immediate", "--retain-data"]).exit_code == 0
    cli_client.delete_iceberg_namespace.assert_called_once_with("my-org", "observations", imsure=True, immediate=True, retain_data=True)
    result = runner.invoke(app, ["iceberg", "namespace", "create", "my-org", "obs", "--metadata", "[]"])
    assert result.exit_code != 0
    cli_client.create_iceberg_namespace.assert_not_called()


def test_cli_table_list_and_describe(cli_client):
    from arraylake.types import IcebergTableSummaryResponse

    cli_client.list_iceberg_tables_paginated.return_value = iter(
        [
            IcebergTableSummaryResponse(
                name="weather",
                namespace="observations",
                table_uuid=uuid4(),
                created="2026-09-09T00:00:00Z",
                updated="2026-09-09T00:00:00Z",
            )
        ]
    )
    runner = CliRunner()
    result = runner.invoke(app, ["iceberg", "table", "list", "my-org", "observations", "--output", "json"])
    assert result.exit_code == 0, result.exception
    assert json.loads(result.stdout)[0]["name"] == "weather"
    assert json.loads(result.stdout)[0]["identifier"] == "observations.weather"
    cli_client.get_iceberg.assert_not_called()
    catalog = cli_client.get_iceberg.return_value
    catalog.load_table.return_value.metadata_location = "s3://bucket/metadata.json"
    catalog.load_table.return_value.metadata.model_dump.return_value = {"schemas": []}
    result = runner.invoke(app, ["iceberg", "table", "describe", "my-org", "observations.weather", "--output", "json"])
    assert result.exit_code == 0, result.exception
    assert json.loads(result.stdout)["metadata"] == {"schemas": []}
    catalog.load_table.assert_called_once_with(("observations", "weather"))
    catalog.close.assert_called_once()


@pytest.mark.parametrize(
    "identifier, expected",
    [
        ("observations.weather", ("observations", "weather")),
        ("My-namespace.table_2", ("My-namespace", "table_2")),
        ('"observations.v2"."weather.daily"', ("observations.v2", "weather.daily")),
        ('observations."weather.daily"', ("observations", "weather.daily")),
        ('"a""b"."daily weather"', ('a"b', "daily weather")),
        ('"気象".weather', ("気象", "weather")),
    ],
)
def test_cli_qualified_table_identifier(cli_client, identifier, expected):
    from arraylake.cli.iceberg import _parse_table_identifier, _table_identifier

    catalog = cli_client.get_iceberg.return_value
    catalog.load_table.return_value.metadata_location = "s3://bucket/metadata.json"
    catalog.load_table.return_value.metadata.model_dump.return_value = {}
    result = CliRunner().invoke(app, ["iceberg", "table", "describe", "my-org", identifier, "--output", "json"])
    assert result.exit_code == 0, result.exception
    catalog.load_table.assert_called_once_with(expected)
    assert _parse_table_identifier(json.loads(result.stdout)["identifier"]) == expected
    assert _parse_table_identifier(_table_identifier(*expected)) == expected
    catalog.close.assert_called_once()


@pytest.mark.parametrize(
    "identifier",
    ["weather", "a.b.c", ".weather", "obs.", '"".weather', 'obs.""', '"obs.weather', 'ob"s.weather', '"obs"x.weather', "obs.daily weather"],
)
def test_cli_invalid_table_identifier(cli_client, identifier):
    result = CliRunner().invoke(app, ["iceberg", "table", "describe", "my-org", identifier])
    assert result.exit_code == 2
    assert "Expected NAMESPACE.TABLE" in result.output
    cli_client.get_iceberg.assert_not_called()


def test_cli_table_list_quoted_identifiers():
    from arraylake.cli.iceberg import Output, _show_list

    rows = [{"namespace": "observations.v2", "name": "weather.daily", "updated": "2026-09-09", "has_storage_override": False}]
    # Exercise both user-facing formats without a catalog load.
    import typer

    listing = typer.Typer()

    @listing.command()
    def show(output: Output = Output.rich):
        _show_list(rows, output, namespaces=False)

    runner = CliRunner()
    rich = runner.invoke(listing, [])
    assert rich.exit_code == 0
    assert '"observations.v2"."weather.daily"' in rich.output
    result = runner.invoke(listing, ["--output", "json"])
    assert json.loads(result.stdout)[0]["identifier"] == '"observations.v2"."weather.daily"'


async def test_refresh_success_persists_rotated_tokens_quietly(http_routes, monkeypatch, test_token_file, capsys):
    pytest.importorskip("pyiceberg")
    from arraylake.repos.iceberg.auth import _refresh_login
    from arraylake.token import TokenHandler

    async def request(self):
        return httpx.Request("POST", f"{URL}/refresh")

    monkeypatch.setattr(TokenHandler, "build_refresh_request", request)
    new_token = jwt(time.time() + 3600)
    http_routes.post(f"{URL}/refresh").respond(
        200,
        json={
            "id_token": new_token,
            "access_token": "new-access",
            "refresh_token": "new-refresh",
            "expires_in": 3600,
            "token_type": "Bearer",
        },
    )
    await _refresh_login(TokenHandler(URL))
    saved = json.loads(test_token_file.read_text())
    assert saved["id_token"] == new_token and saved["refresh_token"] == "new-refresh"
    assert capsys.readouterr().out == ""
