from __future__ import annotations

from typing import Any

import httpx
import pytest
from pydantic import ValidationError

from matrx_ai.tools import _sandbox_proxy
from matrx_ai.tools._sandbox_proxy import SandboxBinding, SandboxReadResult
from matrx_ai.tools.arg_models.fs_args import FsListArgs
from matrx_ai.tools.implementations import filesystem
from matrx_ai.tools.models import ToolContext


@pytest.mark.parametrize(
    ("root", "raw", "expected"),
    [
        ("/home/agent", "project/src", "/home/agent/project/src"),
        ("/home/agent", "/tmp/x", "/tmp/x"),
        (r"C:\Users\Arman", r"project\src", r"C:\Users\Arman\project\src"),
        (r"C:\Users\Arman", r"D:\code\repo", r"D:\code\repo"),
        (r"C:\Users\Arman", r"\\server\share\repo", r"\\server\share\repo"),
    ],
)
def test_bound_path_resolution_uses_target_os_rules(
    root: str,
    raw: str,
    expected: str,
) -> None:
    binding = SandboxBinding(
        sandbox_id="target",
        base_url="https://target.invalid",
        access_token="token",
        root_path=root,
        target_kind="local_machine",
    )

    assert filesystem._resolve_sandbox_path(binding, raw) == expected


def test_bound_path_resolution_rejects_windows_drive_relative_path() -> None:
    binding = SandboxBinding(
        sandbox_id="target",
        base_url="https://target.invalid",
        access_token="token",
        root_path=r"C:\Users\Arman",
        target_kind="local_machine",
    )

    with pytest.raises(_sandbox_proxy.SandboxProxyError, match="Drive-relative"):
        filesystem._resolve_sandbox_path(binding, r"D:repo\file.py")


@pytest.mark.parametrize("unsupported", [{"limit": 25}, {"page_token": "next"}])
def test_fs_list_rejects_internal_pagination_controls(
    unsupported: dict[str, Any],
) -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        FsListArgs.model_validate({"path": ".", **unsupported})


@pytest.mark.asyncio
async def test_bound_fs_read_forwards_offset_and_limit_semantics(monkeypatch) -> None:
    binding = SandboxBinding("target", "https://target.invalid", "token")

    received: dict[str, Any] = {}

    async def proxy_read(*_args: Any, **kwargs: Any) -> SandboxReadResult:
        received.update(kwargs)
        return SandboxReadResult(
            content="3456",
            size=10,
            offset=3,
            limit=4,
            next_offset=7,
            truncated=True,
            server_bounded=True,
        )

    monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: binding)
    monkeypatch.setattr(filesystem, "_proxy_fs_read", proxy_read)

    result = await filesystem.fs_read(
        {"path": "sample.txt", "offset": 3, "limit": 4},
        ToolContext(call_id="read-1", tool_name="fs_read"),
    )

    assert result.success is True
    # ``__kind`` is part of the data, not decoration (KINDS_EVERYWHERE_PLAN §4.2):
    # fs_read returns a ``file_read_result`` and the marker is a declared field of
    # it. An exact-dict assertion here is the point — it fails loudly if the
    # marker is ever stripped back off this payload.
    assert result.output == {
        "__kind": "file_read_result",
        "content": "3456",
        "size": 10,
        "offset": 3,
        "limit": 4,
        "next_offset": 7,
        "truncated": True,
        "path": "/home/agent/sample.txt",
    }
    assert received == {"encoding": "utf8", "offset": 3, "limit": 4}


@pytest.mark.asyncio
async def test_bound_fs_read_preserves_json_file_as_opaque_text(monkeypatch) -> None:
    binding = SandboxBinding("target", "https://target.invalid", "token")

    async def proxy_read(*_args: Any, **_kwargs: Any) -> SandboxReadResult:
        return SandboxReadResult(
            content='{"answer": 42}',
            size=14,
            offset=0,
            limit=1024,
            next_offset=None,
            truncated=False,
            server_bounded=True,
        )

    monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: binding)
    monkeypatch.setattr(filesystem, "_proxy_fs_read", proxy_read)

    result = await filesystem.fs_read(
        {"path": "data.json", "limit": 1024},
        ToolContext(call_id="read-json", tool_name="fs_read"),
    )

    assert result.success is True
    assert result.output["content"] == '{"answer": 42}'


@pytest.mark.asyncio
async def test_bound_fs_list_uses_contract_entry_cap(monkeypatch) -> None:
    binding = SandboxBinding("target", "https://target.invalid", "token")
    received: dict[str, Any] = {}

    async def proxy_list(
        _binding: SandboxBinding,
        path: str,
        *,
        recursive: bool,
        depth: int,
        pattern: str | None,
        limit: int,
        page_token: str | None,
    ) -> dict[str, Any]:
        received.update(
            path=path,
            recursive=recursive,
            depth=depth,
            pattern=pattern,
            limit=limit,
            page_token=page_token,
        )
        return {
            "entries": [
                {"name": "main.py", "path": "/home/agent/src/main.py", "kind": "file"},
            ],
            "truncated": True,
            "nextPageToken": "next-page",
        }

    monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: binding)
    monkeypatch.setattr(filesystem, "_proxy_fs_list", proxy_list)

    result = await filesystem.fs_list(
        {"path": ".", "recursive": True, "pattern": "*.py"},
        ToolContext(call_id="list-1", tool_name="fs_list"),
    )

    assert result.success is True
    assert received == {
        "path": "/home/agent",
        "recursive": True,
        "depth": 10,
        "pattern": "*.py",
        "limit": 500,
        "page_token": None,
    }
    assert [entry["name"] for entry in result.output["entries"]] == ["main.py"]
    assert result.output["recursive"] is True
    assert result.output["pattern"] == "*.py"
    assert result.output["truncated"] is True


@pytest.mark.asyncio
async def test_bound_fs_list_legacy_target_keeps_client_pattern_fallback(monkeypatch) -> None:
    binding = SandboxBinding("target", "https://target.invalid", "token")

    async def proxy_list(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        # Older targets have no pagination metadata and ignore pattern.
        return {
            "entries": [
                {"name": "main.py", "path": "/home/agent/main.py", "kind": "file"},
                {"name": "README.md", "path": "/home/agent/README.md", "kind": "file"},
            ]
        }

    monkeypatch.setattr(filesystem, "get_active_sandbox", lambda: binding)
    monkeypatch.setattr(filesystem, "_proxy_fs_list", proxy_list)

    result = await filesystem.fs_list(
        {"path": ".", "pattern": "*.py"},
        ToolContext(call_id="list-legacy", tool_name="fs_list"),
    )

    assert result.success is True
    assert [entry["name"] for entry in result.output["entries"]] == ["main.py"]
    assert result.output["truncated"] is False


@pytest.mark.asyncio
async def test_proxy_read_uses_daemon_bounds_without_client_slicing(monkeypatch) -> None:
    binding = SandboxBinding("target", "https://target.invalid", "token")
    received: dict[str, Any] = {}

    async def request(
        _binding: SandboxBinding,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        received.update(method=method, path=path, **kwargs)
        return httpx.Response(
            200,
            text="3456",
            headers={
                "X-Matrx-File-Size": "10",
                "X-Matrx-Next-Offset": "7",
                "X-Matrx-Truncated": "true",
            },
        )

    monkeypatch.setattr(_sandbox_proxy, "_request", request)

    result = await _sandbox_proxy.fs_read(binding, "/sample.txt", offset=3, limit=4)

    assert received["params"] == {
        "path": "/sample.txt",
        "encoding": "utf8",
        "offset": 3,
        "limit": 4,
    }
    assert result == SandboxReadResult(
        content="3456",
        size=10,
        offset=3,
        limit=4,
        next_offset=7,
        truncated=True,
        server_bounded=True,
    )


@pytest.mark.asyncio
async def test_proxy_read_falls_back_for_legacy_target_that_ignores_bounds(monkeypatch) -> None:
    binding = SandboxBinding("target", "https://target.invalid", "token")

    async def request(*_args: Any, **_kwargs: Any) -> httpx.Response:
        return httpx.Response(200, text="0123456789")

    monkeypatch.setattr(_sandbox_proxy, "_request", request)

    result = await _sandbox_proxy.fs_read(binding, "/sample.txt", offset=3, limit=4)

    assert result.content == "3456"
    assert result.next_offset == 7
    assert result.truncated is True
    assert result.server_bounded is False


@pytest.mark.asyncio
async def test_proxy_list_forwards_server_filter_and_pagination(monkeypatch) -> None:
    binding = SandboxBinding("target", "https://target.invalid", "token")
    received: dict[str, Any] = {}

    async def request(
        _binding: SandboxBinding,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> httpx.Response:
        received.update(method=method, path=path, **kwargs)
        return httpx.Response(
            200,
            json={"entries": [], "truncated": False, "nextPageToken": None},
        )

    monkeypatch.setattr(_sandbox_proxy, "_request", request)

    result = await _sandbox_proxy.fs_list(
        binding,
        "/home/agent",
        recursive=True,
        depth=10,
        pattern="src/**/*.py",
        limit=25,
        page_token="page-2",
    )

    assert result["truncated"] is False
    assert received["params"] == {
        "path": "/home/agent",
        "recursive": "true",
        "depth": 10,
        "pattern": "src/**/*.py",
        "limit": 25,
        "pageToken": "page-2",
    }
