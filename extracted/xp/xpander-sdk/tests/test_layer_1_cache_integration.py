"""Integration test — Layer 1 microcompact through the workspace cache.

Verifies the full ``maybe_offload_content → _save_to_workspace → cache.put``
path returns to the caller without waiting for the workspace HTTP round-trip,
and that ``optimizer.aclose()`` drains pending writes at task end.

Uses a mock ``APIClient.make_request`` so no network is touched. Asserts
on:

* ``_save_to_workspace`` returns the path immediately (background HTTP not
  yet awaited)
* ``maybe_offload_content`` produces the preview + retrieval pointer in
  one tick
* ``aclose()`` actually flushes the queued ``make_request`` call
* the queued bytes match what was put (cache hit invariant)
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
)
from xpander_sdk.core.context_optimizer.encryption import decrypt, derive_key


def _make_optimizer() -> XPanderContextOptimizer:
    opt = XPanderContextOptimizer(
        context_window=200_000,
        reserved_for_output=20_000,
        buffer_tokens=13_000,
        max_content_length=8_000,
        preview_length=2_000,
    )
    opt.agent = SimpleNamespace(
        id="agent-1",
        configuration=SimpleNamespace(organization_id="org-1"),
    )
    opt.task = SimpleNamespace(id="task-1")
    # 80% of the window: exercise the cache path at the base offload threshold
    # rather than the wide low-headroom band.
    opt._last_estimated_tokens = 160_000
    return opt


@pytest.mark.asyncio
async def test_save_to_workspace_returns_immediately_and_aclose_flushes():
    opt = _make_optimizer()
    big = "x" * 12_000  # well above max_content_length = 8K

    write_started = asyncio.Event()
    release = asyncio.Event()
    captured = {}

    async def _gated_make_request(path, method, payload):
        captured["path"] = path
        captured["payload"] = payload
        write_started.set()
        await release.wait()

    with patch(
        "xpander_sdk.core.context_optimizer.context_optimizer.APIClient",
        autospec=True,
    ) as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.make_request = AsyncMock(side_effect=_gated_make_request)

        # _save_to_workspace must return without waiting on make_request.
        ret_path = await opt._save_to_workspace(big)
        assert ret_path is not None
        assert ret_path.startswith("CONTEXT_OPTIMIZATION/")
        assert ret_path.endswith(".xp")

        # Background write was scheduled but is gated — aclose has to drain
        # it. The write hasn't completed yet.
        await write_started.wait()
        assert opt._workspace_cache.has_pending()
        assert opt._workspace_cache.stats["puts"] == 1

        # Cache holds the encrypted bytes already (read-after-write).
        ctx_id = ret_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        entry = opt._workspace_cache.get(ctx_id)
        assert entry is not None
        assert entry.size == len(big)
        assert entry.workspace_path == ret_path
        # Round-trip the encryption to check the cached bytes are the same
        # ones that would land in the workspace.
        key = derive_key(org_id="org-1", agent_id="agent-1", task_id="task-1")
        assert decrypt(entry.encrypted, key) == big

        release.set()
        await opt.aclose()

        # The make_request actually fired with the same path/payload.
        assert captured["path"].endswith("/tools/file_write")
        assert captured["payload"]["path"] == ret_path
        assert captured["payload"]["content"] == entry.encrypted


@pytest.mark.asyncio
async def test_maybe_offload_returns_preview_pointer_with_cache_hit():
    opt = _make_optimizer()
    big = "y" * 12_000

    with patch(
        "xpander_sdk.core.context_optimizer.context_optimizer.APIClient",
        autospec=True,
    ) as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.make_request = AsyncMock(return_value=None)

        replacement, workspace_path = await opt.maybe_offload_content(
            content=big, tool_name="some-tool"
        )

        assert replacement is not None
        assert workspace_path is not None
        assert "TRUNCATED OUTPUT" in replacement
        assert workspace_path in replacement
        assert "xpworkspace-context-retrieve" in replacement

        # Cache holds the entry.
        ctx_id = workspace_path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        entry = opt._workspace_cache.get(ctx_id)
        assert entry is not None

        await opt.aclose()


@pytest.mark.asyncio
async def test_aclose_logs_but_does_not_raise_on_workspace_failure():
    opt = _make_optimizer()
    big = "z" * 12_000

    with patch(
        "xpander_sdk.core.context_optimizer.context_optimizer.APIClient",
        autospec=True,
    ) as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.make_request = AsyncMock(side_effect=RuntimeError("503"))

        ret_path = await opt._save_to_workspace(big)
        assert ret_path is not None  # path returned even though write will fail
        # aclose() drains at task end; spec says don't re-raise here.
        await opt.aclose()

        assert opt._workspace_cache.stats["write_failures"] == 1
