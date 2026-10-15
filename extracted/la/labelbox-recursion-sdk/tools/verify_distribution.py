"""Verify published artifacts with only the installed SDK's runtime dependencies."""

from __future__ import annotations

import asyncio
import importlib.metadata
import importlib.util
import sys
import tarfile
import zipfile
from pathlib import Path

import httpx

import recursion_sdk
from recursion_sdk import AsyncRecursion, Recursion, models

REQUIRED_PACKAGE_FILES = frozenset(
    {
        "recursion_sdk/py.typed",
        "recursion_sdk/_generated/openapi.json",
        "recursion_sdk/_generated/models.py",
        "recursion_sdk/_generated/client.py",
    }
)
DEVELOPMENT_MODULES = ("datamodel_code_generator", "mypy", "pytest", "ruff")
API_KEY_PAYLOAD_LENGTH = 43
DISTRIBUTION_NAME = "labelbox-recursion-sdk"
NORMALIZED_DISTRIBUTION_NAME = DISTRIBUTION_NAME.replace("-", "_")
API_KEY = "rma_" + "A" * API_KEY_PAYLOAD_LENGTH
RESPONSE_ETAG = '"installed-wheel"'


def handle_request(request: httpx.Request) -> httpx.Response:
    assert request.url.path == "/managed-agents/v1/sessions"
    assert request.headers["authorization"] == f"Bearer {API_KEY}"
    return httpx.Response(200, json={"sessions": []}, headers={"etag": RESPONSE_ETAG})


async def verify_async_client() -> None:
    async with AsyncRecursion(
        api_key=API_KEY, transport=httpx.MockTransport(handle_request)
    ) as client:
        result = await client.managed_agents.list_sessions()
        assert isinstance(result.data, models.SessionListResponse)
        assert result.data.sessions == []
        assert result.response.headers["etag"] == RESPONSE_ETAG


def main() -> None:
    wheel_path, source_path = (Path(argument) for argument in sys.argv[1:])
    distribution = importlib.metadata.distribution(DISTRIBUTION_NAME)
    assert distribution.metadata["Name"] == DISTRIBUTION_NAME
    assert wheel_path.name == (
        f"{NORMALIZED_DISTRIBUTION_NAME}-{distribution.version}-py3-none-any.whl"
    )
    assert source_path.name == f"{NORMALIZED_DISTRIBUTION_NAME}-{distribution.version}.tar.gz"
    with zipfile.ZipFile(wheel_path) as wheel:
        missing = REQUIRED_PACKAGE_FILES.difference(wheel.namelist())
        assert not missing, f"Wheel is missing {missing}"
    with tarfile.open(source_path) as source:
        names = {"/".join(name.split("/")[2:]) for name in source.getnames()}
        missing = REQUIRED_PACKAGE_FILES.difference(names)
        assert not missing, f"Source distribution is missing {missing}"
    assert recursion_sdk.__file__ is not None
    installed_path = Path(recursion_sdk.__file__).resolve()
    source_root = Path(__file__).resolve().parents[1] / "src"
    assert not installed_path.is_relative_to(source_root), installed_path
    for module in DEVELOPMENT_MODULES:
        assert importlib.util.find_spec(module) is None, f"Unexpected development module: {module}"
    with Recursion(api_key=API_KEY, transport=httpx.MockTransport(handle_request)) as client:
        result = client.managed_agents.list_sessions()
        assert isinstance(result.data, models.SessionListResponse)
        assert result.data.sessions == []
        assert result.response.headers["etag"] == RESPONSE_ETAG
    asyncio.run(verify_async_client())
    print(f"Installed {DISTRIBUTION_NAME} {distribution.version}: sync/async OK")


if __name__ == "__main__":
    main()
