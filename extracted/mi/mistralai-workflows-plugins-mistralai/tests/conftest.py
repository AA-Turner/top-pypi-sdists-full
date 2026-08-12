import os
import socket
import subprocess
import sys
import time
from collections.abc import Iterator
from dataclasses import dataclass

import httpx
import pytest

from mistralai.workflows.testing.fixtures import (
    clear_dependency_cache,  # noqa: F401
    disable_otel_export,  # noqa: F401
    event_loop,  # noqa: F401
    mock_upsert_search_attributes,  # noqa: F401
    setup_test_config,  # noqa: F401
    temporal_env,  # noqa: F401
)


@pytest.fixture(scope="module")
def vcr_config():
    def before_record_request(request):
        url = request.uri
        if "api.mistral.ai" not in url:
            return None
        return request

    return {
        "record_mode": os.getenv("VCR_RECORD_MODE", "none"),
        "match_on": ["method", "host", "path"],
        "filter_headers": [
            ("authorization", "REDACTED"),
            ("x-api-key", "REDACTED"),
            ("set-cookie", "<IGNORED>"),
            ("cf-ray", "<IGNORED>"),
            ("date", "<IGNORED>"),
            ("mistral-correlation-id", "<IGNORED>"),
            ("x-kong-request-id", "<IGNORED>"),
            ("x-envoy-upstream-service-time", "<IGNORED>"),
        ],
        "before_record_request": before_record_request,
        "ignore_localhost": True,
        "cassette_library_dir": "tests/agents/cassettes",
        "decode_compressed_response": True,
    }


@pytest.fixture
def mock_mistral_client():
    """Fixture for mocking mistral client responses."""
    pass


# --- Local hello-world MCP over Streamable HTTP (for MCP client/agent tests) ---

# A minimal FastMCP server with a single `hello` tool, run as a subprocess so the
# MCP client reaches a genuine out-of-process server over a real socket. The
# tool's reply is injected via env so tests can pin a distinctive, stable value.
_HELLO_MCP_SERVER_SRC = """
import os
import sys

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hello-mcp", host="127.0.0.1", port=int(sys.argv[1]))


@mcp.tool()
def hello() -> str:
    \"\"\"Return a friendly greeting.\"\"\"
    return os.environ["HELLO_MCP_REPLY"]


mcp.run(transport="streamable-http")
"""

# Fixed (so a recorded VCR cassette stays valid) and distinctive (so a passing
# agent run cannot be a hallucinated "hello world" - the model can only emit this
# by actually calling the tool).
HELLO_MCP_REPLY = "hello world (mcp-live-ok)"


@dataclass
class HelloMcp:
    url: str
    reply: str


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_until_ready(url: str, proc: "subprocess.Popen[bytes]", timeout: float = 30.0) -> None:
    deadline = time.monotonic() + timeout
    body = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            raise RuntimeError(f"hello MCP server exited early (code {proc.returncode})")
        try:
            resp = httpx.post(url, headers=headers, json=body, timeout=2.0)
            if resp.status_code < 500:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.25)
    raise RuntimeError("hello MCP server did not become ready in time")


@pytest.fixture(scope="module")
def hello_mcp() -> Iterator[HelloMcp]:
    """Spawn a real localhost FastMCP `hello` server for the duration of a module."""
    port = _free_port()
    proc = subprocess.Popen(
        [sys.executable, "-c", _HELLO_MCP_SERVER_SRC, str(port)],
        env={**os.environ, "HELLO_MCP_REPLY": HELLO_MCP_REPLY},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    url = f"http://127.0.0.1:{port}/mcp"
    try:
        _wait_until_ready(url, proc)
        yield HelloMcp(url=url, reply=HELLO_MCP_REPLY)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)
