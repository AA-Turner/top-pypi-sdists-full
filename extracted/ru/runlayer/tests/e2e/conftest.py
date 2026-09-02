"""E2E test fixtures for CLI against a real running backend."""

import contextlib
import os
import time
import uuid

import httpx
import pytest
from typer.testing import CliRunner

from runlayer_cli import regex_safe
from runlayer_cli.api import PluginDetail, PluginServerRef, RunlayerClient
from runlayer_cli.models import ServerDetails

API_KEY_HEADER = "x-runlayer-api-key"


def _backend_healthy(base_url: str, api_key: str) -> bool:
    """Check if backend is reachable and API key works."""
    try:
        resp = httpx.get(
            f"{base_url}/api/v1/utils/health-check/",
            headers={API_KEY_HEADER: api_key},
            timeout=5,
        )
        return resp.status_code == 200
    except httpx.ConnectError:
        return False


def _is_e2e_item(item):
    return "/e2e/" in str(item.fspath)


def pytest_collection_modifyitems(config, items):
    """Mark e2e items; skip backend e2e if creds or backend are unavailable."""
    e2e_items = [item for item in items if _is_e2e_item(item)]
    for item in e2e_items:
        item.add_marker(pytest.mark.e2e)

    if not e2e_items:
        return

    backend_e2e_items = [
        item for item in e2e_items if item.get_closest_marker("no_backend_e2e") is None
    ]

    if not backend_e2e_items:
        return

    api_key = os.environ.get("RUNLAYER_API_KEY")
    base_url = os.environ.get("RUNLAYER_BASE_URL", "http://localhost:3000")

    if not api_key:
        skip = pytest.mark.skip(reason="RUNLAYER_API_KEY not set")
        for item in backend_e2e_items:
            item.add_marker(skip)
        return

    if not _backend_healthy(base_url, api_key):
        skip = pytest.mark.skip(reason=f"Backend not reachable at {base_url}")
        for item in backend_e2e_items:
            item.add_marker(skip)


@pytest.fixture(scope="session")
def api_key():
    return os.environ["RUNLAYER_API_KEY"]


@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("RUNLAYER_BASE_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def security_scan_api_key(api_key):
    key = os.environ.get("RUNLAYER_SECURITY_SCAN_API_KEY")
    if key:
        return key
    if api_key.startswith("rl_org_"):
        return api_key
    pytest.skip("RUNLAYER_SECURITY_SCAN_API_KEY not set")


@pytest.fixture(scope="session")
def api_client(api_key, base_url):
    """Direct API client for verification outside CLI."""
    return RunlayerClient(hostname=base_url, secret=api_key)


@pytest.fixture(scope="session")
def cleanup_deployments(api_client):
    """Safety net: track deployment IDs and delete them in teardown."""
    ids: list[str] = []
    yield ids
    for dep_id in ids:
        try:
            api_client.delete_deployment(dep_id)
        except Exception:
            pass


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def cli_args(api_key, base_url):
    return ["--secret", api_key, "--host", base_url]


@pytest.fixture
def unique_id():
    return uuid.uuid4().hex[:8]


@pytest.fixture
def runlayer_home(tmp_path, monkeypatch):
    """Isolate ~/.runlayer to a temp dir."""
    home = tmp_path / ".runlayer"
    home.mkdir()
    monkeypatch.setattr("runlayer_cli.paths.get_runlayer_dir", lambda: home)
    monkeypatch.setattr("runlayer_cli.config.get_runlayer_dir", lambda: home)
    monkeypatch.setattr("runlayer_cli.oauth.get_runlayer_dir", lambda: home)
    return home


# Active-server creation runs a real backend connection test (spawns
# `npx ...` for stdio servers). Under CI load that spawn can exceed the
# backend's 15s connection-test timeout, returning a transient 400.
_CONNECT_FLAKE_MARKERS = ("Failed to connect to server", "Connection test timed out")
_CONNECT_FLAKE_RETRIES = 2


def _is_connection_test_flake(resp: httpx.Response) -> bool:
    if resp.status_code != 400:
        return False
    try:
        detail = resp.json().get("detail", "")
    except ValueError:
        return False
    message = detail.get("message", "") if isinstance(detail, dict) else str(detail)
    return any(marker in message for marker in _CONNECT_FLAKE_MARKERS)


def _post_server(client: httpx.Client, server_json: dict) -> httpx.Response:
    for attempt in range(_CONNECT_FLAKE_RETRIES + 1):
        resp = client.post("/api/v1/servers", json=server_json)
        if attempt < _CONNECT_FLAKE_RETRIES and _is_connection_test_flake(resp):
            time.sleep(2)
            continue
        if resp.is_error:
            # Include the body: the backend packs the actual failure reason
            # (e.g. connection-test error log) into the 4xx detail.
            raise AssertionError(
                f"POST /api/v1/servers failed: {resp.status_code} {resp.text}"
            )
        return resp
    raise AssertionError("unreachable")


def _create_server_with_policy(
    client: httpx.Client, server_json: dict
) -> tuple[ServerDetails, str]:
    resp = _post_server(client, server_json)
    server = ServerDetails.model_validate(resp.json())

    policy_resp = client.post(
        "/api/v1/policies",
        json={
            "principal": {"type": "any"},
            "action": "allow",
            "scope": {"servers": [server.id], "tools": "*", "resources": "*"},
        },
    )
    policy_resp.raise_for_status()
    policy_id = policy_resp.json()["id"]

    for _ in range(30):
        r = client.get(f"/api/v1/proxy/{server.id}/tools")
        if r.status_code == 200:
            break
        time.sleep(1)

    return server, policy_id


@pytest.fixture
def create_e2e_server(api_key, base_url, unique_id):
    """Factory: create server + policy, return ServerDetails, cleanup on teardown."""
    created: list[tuple[httpx.Client, str, str]] = []

    def _create(server_json: dict) -> ServerDetails:
        client = httpx.Client(
            headers={API_KEY_HEADER: api_key, "Content-Type": "application/json"},
            base_url=base_url,
            timeout=30,
        )
        server_json["name"] = f"e2e-{unique_id}-{server_json['name']}"
        server, policy_id = _create_server_with_policy(client, server_json)
        created.append((client, server.id, policy_id))
        return server

    yield _create

    for client, server_id, policy_id in created:
        with contextlib.suppress(Exception):
            client.delete(f"/api/v1/policies/{policy_id}")
        with contextlib.suppress(Exception):
            client.delete(f"/api/v1/servers/{server_id}")
        client.close()


@pytest.fixture
def create_e2e_plugin(api_key, base_url, unique_id, create_e2e_server):
    """Factory: create server + policy + plugin, return PluginDetail, cleanup on teardown."""
    created: list[tuple[str, str, str]] = []  # (plugin_id, namespace, name)

    def _create(
        plugin_name: str = "test-plugin",
        description: str | None = "e2e test plugin",
        namespace: str | None = None,
    ) -> PluginDetail:
        server = create_e2e_server(
            {
                "name": f"plug-{plugin_name}",
                "url": "npx",
                "transport_type": "stdio",
                "transport_config": {"args": ["-y", "mcp-echo-server"]},
            }
        )

        api = RunlayerClient(hostname=base_url, secret=api_key)
        ns = namespace or f"e2e-plug/{unique_id}"
        plugin = api.create_plugin(
            name=f"e2e-{unique_id}-{plugin_name}",
            namespace=ns,
            path=plugin_name,
            description=description,
            is_public=False,
            use_dynamic_tools=False,
            servers=[PluginServerRef(server_id=server.id)],
            skill_ids=[],
        )
        created.append((plugin.id, ns, plugin.name))
        return plugin

    yield _create

    api = RunlayerClient(hostname=base_url, secret=api_key)
    for plugin_id, _ns, _name in created:
        with contextlib.suppress(Exception):
            api.delete_plugin(plugin_id)


ANSI_RE = regex_safe.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)
