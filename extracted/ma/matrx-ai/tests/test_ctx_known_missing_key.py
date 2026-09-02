"""A KNOWN-BUT-MISSING context key returns actionable guidance, not a dead-end.

When an agent asks for a key that isn't in the current turn's manifest — an
attached document the user detached, or one attached on a prior turn — the
``context`` tool must not return a bare ``not_found`` the agent retries into
oblivion. It returns ``context_not_attached`` with the pd id + a concrete
``document_content(...)`` path (cheap tier), upgraded to the doc's label when a
prior-turn stamp confirms it (confirm tier via the injected ext).
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from matrx_ai.tools.implementations.ctx import ctx_get
from matrx_ai.tools.models import ToolContext


def _ctx() -> ToolContext:
    return ToolContext(
        call_id="call_test",
        user_id="user_test",
        conversation_id="conv_test",
        emitter=None,
    )


def _manifest_with_keys(keys: list[str]) -> MagicMock:
    objs = [MagicMock(key=k) for k in keys]
    m = MagicMock()
    m.get.return_value = None  # requested key is never present
    m.all.return_value = objs
    return m


def _app_ctx(conversation_id: str | None = "conv-1") -> Any:
    ac = MagicMock()
    ac.conversation_id = conversation_id
    return ac


@pytest.mark.asyncio
async def test_manifest_none_attached_doc_key_cheap_tier() -> None:
    """No manifest at all + an attached_document_<id> key → cheap-tier guidance
    with the pd id parsed from the key and put into the message."""
    with (
        patch(
            "matrx_ai.context.app_context.get_app_context",
            return_value=_app_ctx(),
        ),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: None),
        patch("matrx_ai._ext.has_ext", return_value=False),
    ):
        result = await ctx_get({"key": "attached_document_pd-xyz", "mode": "full"}, _ctx())

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "context_not_attached"
    assert "pd-xyz" in result.error.message
    assert "document_content(action='read', document_id='pd-xyz'" in (
        result.error.suggested_action or ""
    )


@pytest.mark.asyncio
async def test_missing_attached_doc_key_confirm_tier() -> None:
    """Key not in manifest + a prior-turn stamp confirms it → confirm-tier
    guidance names the document (label + id) via the injected ext."""
    manifest = _manifest_with_keys(["active_file"])
    load_manifest = lambda _app: manifest  # noqa: E731
    lookup = AsyncMock(return_value={"pd_id": "pd-9", "label": "Q3 Report.pdf"})

    def _get_ext(name: str) -> Any:
        if name == "lookup_prior_attached_document":
            return lookup
        return load_manifest

    def _has_ext(name: str) -> bool:
        return name == "lookup_prior_attached_document"

    with (
        patch(
            "matrx_ai.context.app_context.get_app_context",
            return_value=_app_ctx("conv-1"),
        ),
        patch("matrx_ai._ext.get_ext", side_effect=_get_ext),
        patch("matrx_ai._ext.has_ext", side_effect=_has_ext),
    ):
        result = await ctx_get({"key": "attached_document_pd-9", "mode": "full"}, _ctx())

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "context_not_attached"
    assert "Q3 Report.pdf" in result.error.message
    assert "earlier turn" in result.error.message
    assert "document_content(document_id='pd-9')" in result.error.message
    lookup.assert_awaited_once_with("conv-1", "attached_document_pd-9")


@pytest.mark.asyncio
async def test_confirm_tier_failure_degrades_to_cheap() -> None:
    """A confirm-tier ext that raises must degrade to the cheap tier, never
    break the tool."""
    manifest = _manifest_with_keys(["active_file"])
    load_manifest = lambda _app: manifest  # noqa: E731
    lookup = AsyncMock(side_effect=RuntimeError("db down"))

    def _get_ext(name: str) -> Any:
        if name == "lookup_prior_attached_document":
            return lookup
        return load_manifest

    with (
        patch(
            "matrx_ai.context.app_context.get_app_context",
            return_value=_app_ctx("conv-1"),
        ),
        patch("matrx_ai._ext.get_ext", side_effect=_get_ext),
        patch("matrx_ai._ext.has_ext", return_value=True),
    ):
        result = await ctx_get({"key": "attached_document_pd-7", "mode": "full"}, _ctx())

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "context_not_attached"
    assert "pd-7" in result.error.message
    # cheap tier wording (no confirmed label)
    assert "may have been detached" in result.error.message


@pytest.mark.asyncio
async def test_generic_missing_key_lists_available() -> None:
    """A non-attached-document well-formed key gets the available-keys
    inventory, not the blunt empty message.

    The inventory moved from ``suggested_action`` into ``message`` so the model
    reads WHAT EXISTS in the same breath as the failure; ``suggested_action``
    now carries the do-not-retry instruction. See
    test_ctx_key_reconciliation.py for the full contract.
    """
    manifest = _manifest_with_keys(["active_file", "user_profile"])
    with (
        patch(
            "matrx_ai.context.app_context.get_app_context",
            return_value=_app_ctx(),
        ),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: manifest),
        patch("matrx_ai._ext.has_ext", return_value=False),
    ):
        result = await ctx_get({"key": "some_other_key", "mode": "full"}, _ctx())

    assert result.success is False
    assert result.error is not None
    assert result.error.error_type == "context_not_attached"
    assert "some_other_key" in result.error.message
    assert "active_file" in result.error.message
    assert "user_profile" in result.error.message
    assert "Do NOT call context again" in (result.error.suggested_action or "")
