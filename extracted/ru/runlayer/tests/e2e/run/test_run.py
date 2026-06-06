import contextlib
import json
import os
import select
import socket
import subprocess
import sys
import threading
import time
from pathlib import Path

import httpx
import pytest
import yaml
from fastmcp import FastMCP

from runlayer_cli.config import url_to_host_key


def _send_jsonrpc(proc: subprocess.Popen, msg: dict) -> None:
    line = json.dumps(msg) + "\n"
    proc.stdin.write(line)
    proc.stdin.flush()


def _read_jsonrpc(proc: subprocess.Popen, timeout: float = 30) -> dict:
    """Read next JSON-RPC response, auto-replying to server-initiated requests."""
    deadline = time.monotonic() + timeout
    buf = ""
    while time.monotonic() < deadline:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        ready, _, _ = select.select([proc.stdout], [], [], min(remaining, 0.5))
        if ready:
            chunk = proc.stdout.readline()
            if not chunk:
                break
            buf += chunk
            try:
                msg = json.loads(buf.strip())
            except json.JSONDecodeError:
                continue
            buf = ""
            if "method" in msg and "id" in msg:
                _send_jsonrpc(
                    proc,
                    {
                        "jsonrpc": "2.0",
                        "id": msg["id"],
                        "result": {},
                    },
                )
                continue
            if "method" in msg:
                continue
            return msg
    raise TimeoutError(f"No JSON-RPC response within {timeout}s. Buffer: {buf!r}")


@contextlib.contextmanager
def _run_cli(
    server_id: str,
    base_url: str,
    api_key: str | None = None,
    home_dir: Path | None = None,
):
    args = [
        sys.executable,
        "-c",
        "from runlayer_cli.main import cli; cli()",
        "run",
        server_id,
        "--host",
        base_url,
    ]
    if api_key:
        args.extend(["--secret", api_key])

    env = os.environ.copy()
    if home_dir is not None:
        env["HOME"] = str(home_dir)

    proc = subprocess.Popen(
        args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        env=env,
    )
    try:
        time.sleep(3)
        assert proc.poll() is None, f"Process exited early: {proc.stderr.read()}"
        yield proc
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()


def _assert_mcp_tools(proc: subprocess.Popen) -> set[str]:
    """Initialize MCP session and return tool names."""
    _send_jsonrpc(
        proc,
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "e2e-test", "version": "1.0"},
            },
        },
    )

    resp = _read_jsonrpc(proc)
    assert resp["id"] == 1
    assert "capabilities" in resp["result"]

    _send_jsonrpc(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})
    time.sleep(0.5)

    _send_jsonrpc(
        proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
    )
    tools_resp = _read_jsonrpc(proc)
    assert tools_resp["id"] == 2
    tools = tools_resp["result"]["tools"]
    assert len(tools) > 0
    return {t["name"] for t in tools}


def _write_runlayer_config(runlayer_home: Path, base_url: str, api_key: str) -> None:
    config = {
        "default_host": base_url,
        "hosts": {
            url_to_host_key(base_url): {
                "url": base_url,
                "secret": api_key,
            }
        },
    }
    (runlayer_home / "config.yaml").write_text(yaml.safe_dump(config))


def _non_loopback_ipv4_host() -> str:
    """Return an address that another local process can use without loopback."""
    candidates: list[str] = []
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("8.8.8.8", 80))
            candidates.append(sock.getsockname()[0])
    except OSError:
        pass

    try:
        for result in socket.getaddrinfo(
            socket.gethostname(),
            None,
            socket.AF_INET,
            socket.SOCK_DGRAM,
        ):
            candidates.append(result[4][0])
    except OSError:
        pass

    for host in candidates:
        if not host.startswith("127."):
            return host

    pytest.skip("No non-loopback IPv4 address available for hosted MCP e2e")


SERVERS = [
    pytest.param(
        {
            "name": "echo",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
        },
        None,
        id="stdio-echo",
    ),
    pytest.param(
        {
            "name": "fs",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {
                "args": ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
            },
        },
        {"read_file", "list_directory"},
        id="stdio-filesystem",
    ),
    pytest.param(
        {
            "name": "deepwiki",
            "url": "https://mcp.deepwiki.com/mcp",
            "transport_type": "streaming-http",
            "transport_config": {},
        },
        None,
        id="remote-streamable-http",
    ),
]


@pytest.mark.parametrize("server_json, expected_tools", SERVERS)
def test_run_with_explicit_secret(
    api_key, base_url, create_e2e_server, server_json, expected_tools
):
    server = create_e2e_server(server_json)
    with _run_cli(server.id, base_url, api_key=api_key) as proc:
        tool_names = _assert_mcp_tools(proc)
        if expected_tools:
            assert tool_names >= expected_tools


def test_run_uses_config_credentials_when_secret_is_omitted(
    api_key, base_url, create_e2e_server, runlayer_home
):
    _write_runlayer_config(runlayer_home, base_url, api_key)
    server = create_e2e_server(
        {
            "name": "echo-config-auth",
            "url": "npx",
            "transport_type": "stdio",
            "transport_config": {"args": ["-y", "mcp-echo-server"]},
        }
    )

    with _run_cli(server.id, base_url, home_dir=runlayer_home.parent) as proc:
        tool_names = _assert_mcp_tools(proc)
        assert len(tool_names) > 0


@contextlib.contextmanager
def _local_mcp_server(tool_name: str = "greet"):
    """Spin up a FastMCP server on a random port with streaming-http transport."""
    mcp = FastMCP("e2e-local")

    @mcp.tool(name=tool_name)
    def greet(name: str) -> str:
        return f"Hello {name}!"

    import uvicorn

    config = uvicorn.Config(mcp.http_app(), host="0.0.0.0", port=0)
    server = uvicorn.Server(config)

    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()

    # Wait for server to bind
    for _ in range(50):
        if server.started:
            break
        time.sleep(0.1)
    assert server.started, "Local MCP server failed to start"

    # Get the actual bound port
    sockets = server.servers[0].sockets
    port = sockets[0].getsockname()[1]
    url = f"http://{_non_loopback_ipv4_host()}:{port}/mcp"

    try:
        yield url, tool_name
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def test_streaming_http_syncs_local_capabilities(api_key, base_url, create_e2e_server):
    """After tools/list, local_capabilities should be populated for streaming-http."""
    with _local_mcp_server() as (mcp_url, tool_name):
        server = create_e2e_server(
            {
                "name": "local-sync-test",
                "url": mcp_url,
                "transport_type": "streaming-http",
                "transport_config": {},
            }
        )

        # Verify local_capabilities starts empty
        with httpx.Client(
            headers={"x-runlayer-api-key": api_key},
            base_url=base_url,
            timeout=10,
        ) as client:
            resp = client.get(f"/api/v1/servers/{server.id}")
            resp.raise_for_status()
            assert resp.json().get("local_capabilities") is None

        # Run CLI — tools/list triggers middleware sync
        with _run_cli(server.id, base_url, api_key=api_key) as proc:
            tool_names = _assert_mcp_tools(proc)
            assert tool_name in tool_names

            # Poll for local_capabilities to be populated (sync is inline
            # in on_list_tools, but the DB write may take a moment)
            with httpx.Client(
                headers={"x-runlayer-api-key": api_key},
                base_url=base_url,
                timeout=10,
            ) as client:
                caps = None
                for _ in range(10):
                    resp = client.get(f"/api/v1/proxy/{server.id}/tools")
                    if resp.status_code == 200:
                        tools_list = resp.json()
                        if any(t["name"] == tool_name for t in tools_list):
                            caps = tools_list
                            break
                    time.sleep(1)

                assert caps is not None, (
                    "proxy tools endpoint should return synced tools"
                )
                synced_names = {t["name"] for t in caps}
                assert tool_name in synced_names, (
                    f"Expected '{tool_name}' in synced tools, got: {synced_names}"
                )
