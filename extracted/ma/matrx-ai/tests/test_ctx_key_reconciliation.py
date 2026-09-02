"""The ``context`` tool reconciles what it can and stops the model when it can't.

Production traces (chat.tool_trace, 7 days to 2026-08-13) showed ``context`` as
the top tool_defect: 60 ``context_not_attached`` FAILs across 59 conversations,
dominated by a model pattern-completing a plausible-but-nonexistent key
(``bundle_members`` when the turn carried ``bundle_member_count``;
``html_content`` when it carried ``html_pages_structure``). The rejection gave
it no inventory in the message and no instruction to stop, so it guessed again.

Two behaviours are pinned here, matching the guard-reconciliation rule
("is there exactly one thing the caller can mean here?"):

- exactly one normalized match  → RECONCILE + notice the model (COERCED)
- more than one / no match      → REFUSE, naming candidates + an explicit stop
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from matrx_ai.tools.implementations.ctx import (
    _normalize_key,
    _resolve_key_alias,
    ctx_get,
)
from matrx_ai.tools.models import ToolContext


def _ctx() -> ToolContext:
    return ToolContext(
        call_id="call_test",
        user_id="user_test",
        conversation_id="conv_test",
        emitter=None,
    )


def _obj(key: str, content: Any = "the content", type_value: str = "text") -> MagicMock:
    o = MagicMock()
    o.key = key
    o.label = key.replace("_", " ").title()
    o.type = MagicMock(value=type_value)
    o.content = content
    o.content_as_str.return_value = content if isinstance(content, str) else str(content)
    o.is_lazy_source.return_value = False
    o.source = None
    o.summary_agent_id = None
    o.descriptor = None
    return o


def _manifest(objs: list[MagicMock]) -> MagicMock:
    by_key = {o.key: o for o in objs}
    m = MagicMock()
    m.get.side_effect = by_key.get
    m.all.return_value = objs
    return m


def _app_ctx() -> Any:
    ac = MagicMock()
    ac.conversation_id = "conv-1"
    ac.user_id = "user_test"
    return ac


async def _call(manifest: MagicMock, args: dict[str, Any]) -> Any:
    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=_app_ctx()),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: manifest),
        patch("matrx_ai._ext.has_ext", return_value=False),
    ):
        return await ctx_get(args, _ctx())


# --------------------------------------------------------------------------
# _normalize_key / _resolve_key_alias — the reconciliation predicate itself
# --------------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("route_brief", "routebrief"),
        ("route-brief", "routebrief"),
        ("Route Brief", "routebrief"),
        ("routeBrief", "routebrief"),
        ("ROUTE_BRIEF", "routebrief"),
    ],
)
def test_normalize_key_collapses_spelling(raw: str, expected: str) -> None:
    assert _normalize_key(raw) == expected


def test_resolve_alias_single_match_reconciles() -> None:
    resolved, ambiguous = _resolve_key_alias("routeBrief", ["route_brief", "user"])
    assert resolved == "route_brief"
    assert ambiguous == []


def test_resolve_alias_refuses_when_more_than_one_candidate() -> None:
    """Two keys that normalize identically → the caller could mean either, so
    the tool must NOT pick one."""
    resolved, ambiguous = _resolve_key_alias("routebrief", ["route_brief", "Route-Brief"])
    assert resolved is None
    assert ambiguous == ["Route-Brief", "route_brief"]


def test_resolve_alias_never_reconciles_a_different_name() -> None:
    """THE REGRESSION THAT MATTERS: 'bundle_members' and 'bundle_member_count'
    are different names. Substituting one for the other would fabricate an
    answer, so reconciliation must refuse."""
    resolved, ambiguous = _resolve_key_alias(
        "bundle_members", ["bundle_member_count", "bundle_count", "selected_bundle"]
    )
    assert resolved is None
    assert ambiguous == []


# --------------------------------------------------------------------------
# ctx_get — reconcile
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_alias_key_is_resolved_and_returns_content() -> None:
    manifest = _manifest([_obj("route_brief", "brief body")])
    result = await _call(manifest, {"key": "routeBrief", "mode": "full"})

    assert result.success is True
    assert result.output.key == "route_brief"
    assert result.output.content == "brief body"


@pytest.mark.asyncio
async def test_alias_resolution_notices_the_model() -> None:
    """Reconciling silently would let the model keep the wrong spelling."""
    manifest = _manifest([_obj("route_brief", "brief body")])
    result = await _call(manifest, {"key": "Route Brief", "mode": "full"})

    assert result.success is True
    notice = result.output.arg_coercion_notice or ""
    assert "route_brief" in notice
    assert "Route Brief" in notice


@pytest.mark.asyncio
async def test_ambiguous_alias_names_every_candidate_and_does_not_guess() -> None:
    manifest = _manifest([_obj("route_brief"), _obj("Route-Brief")])
    result = await _call(manifest, {"key": "routebrief", "mode": "full"})

    assert result.success is False
    assert result.error.error_type == "validation"
    assert "route_brief" in result.error.message
    assert "Route-Brief" in result.error.message


# --------------------------------------------------------------------------
# ctx_get — refuse, but usefully
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_missing_key_message_carries_the_full_inventory() -> None:
    """The model must be able to pick the right key from the REJECTION itself —
    the manifest block is ephemeral and may be many turns back."""
    manifest = _manifest(
        [_obj("bundle_member_count"), _obj("bundle_count"), _obj("selected_bundle")]
    )
    result = await _call(manifest, {"key": "bundle_members", "mode": "full"})

    assert result.success is False
    assert result.error.error_type == "context_not_attached"
    for key in ("bundle_member_count", "bundle_count", "selected_bundle"):
        assert key in result.error.message


@pytest.mark.asyncio
async def test_missing_key_suggests_closest_names_without_substituting() -> None:
    manifest = _manifest([_obj("bundle_member_count"), _obj("selected_bundle")])
    result = await _call(manifest, {"key": "bundle_members", "mode": "full"})

    assert result.success is False
    assert "bundle_member_count" in result.error.message
    # Suggested, explicitly not applied.
    assert "not the same object" in result.error.message


@pytest.mark.asyncio
async def test_missing_key_tells_the_model_to_stop_retrying() -> None:
    """The dominant cost was the SECOND identical call, not the first."""
    manifest = _manifest([_obj("content")])
    result = await _call(manifest, {"key": "html_content", "mode": "full"})

    assert result.success is False
    assert result.error.is_retryable is False
    action = result.error.suggested_action or ""
    assert "Do NOT call context again with 'html_content'" in action


@pytest.mark.asyncio
async def test_missing_key_says_it_is_not_a_timing_problem() -> None:
    """Rules out the model's other reasonable theory — that it called too early
    and the object will show up if it waits or retries."""
    manifest = _manifest([_obj("content")])
    result = await _call(manifest, {"key": "scan_items", "mode": "full"})

    assert "not a timing problem" in result.error.message


@pytest.mark.asyncio
async def test_empty_manifest_is_stated_plainly() -> None:
    manifest = _manifest([])
    result = await _call(manifest, {"key": "anything", "mode": "full"})

    assert result.success is False
    assert "no context objects are attached" in result.error.message


# --------------------------------------------------------------------------
# page / summary must not stringify a whole dict — the matrx_validation_gate
# FAILs (4 live) came from a "slice" that covered the entire value.
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_page_mode_returns_native_dict_when_slice_covers_whole_value() -> None:
    payload = {"a": 1, "b": [2, 3]}
    obj = _obj("cfg", payload, type_value="json")
    obj.content_as_str.return_value = '{"a": 1, "b": [2, 3]}'
    result = await _call(_manifest([obj]), {"key": "cfg", "mode": "page"})

    assert result.success is True
    # Native container, NOT a stringified dict (which the output gate rejects).
    assert result.output.content == payload
    assert not isinstance(result.output.content, str)


@pytest.mark.asyncio
async def test_page_mode_still_returns_a_string_for_a_partial_slice() -> None:
    obj = _obj("cfg", {"a": 1}, type_value="json")
    obj.content_as_str.return_value = '{"a": 1, "bbbbbbbbbb": 2}'
    result = await _call(_manifest([obj]), {"key": "cfg", "mode": "page", "chars": 8})

    assert result.success is True
    assert result.output.content == '{"a": 1,'
    assert result.output.has_more is True


@pytest.mark.asyncio
async def test_summary_fallback_returns_native_dict_for_a_whole_value() -> None:
    payload = {"a": 1}
    obj = _obj("cfg", payload, type_value="json")
    obj.content_as_str.return_value = '{"a": 1}'
    obj.summary_agent_id = None
    result = await _call(_manifest([obj]), {"key": "cfg", "mode": "summary"})

    assert result.success is True
    assert result.output.fell_back_from == "summary"
    assert result.output.content == payload


@pytest.mark.asyncio
async def test_lazy_source_returns_native_json_when_materialization_is_complete() -> None:
    """Production file metadata reached the gate as one complete JSON string."""
    payload = {"requested_file": {"id": "file-1"}, "family_counts": {"file_count": 1}}
    obj = _obj("resource_file_1", type_value="json")
    obj.is_lazy_source.return_value = True
    obj.source = SimpleNamespace(kind="file", id="file-1")
    materialized = SimpleNamespace(
        representation="file_metadata",
        text='{"requested_file":{"id":"file-1"},"family_counts":{"file_count":1}}',
        offset=0,
        total_chars=72,
        has_more=False,
        next_offset=None,
        page_range=None,
    )

    async def materialize(*args: Any, **kwargs: Any) -> Any:
        return materialized

    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=_app_ctx()),
        patch(
            "matrx_ai._ext.get_ext",
            side_effect=lambda name: (
                (lambda _app: _manifest([obj]))
                if name == "load_manifest_from_ctx"
                else materialize
            ),
        ),
        patch("matrx_ai._ext.has_ext", return_value=True),
    ):
        result = await ctx_get({"key": "resource_file_1", "mode": "full"}, _ctx())

    assert result.success is True
    assert result.output.content == payload
    assert not isinstance(result.output.content, str)


@pytest.mark.asyncio
async def test_lazy_source_keeps_partial_json_page_as_text() -> None:
    obj = _obj("resource_file_1", type_value="json")
    obj.is_lazy_source.return_value = True
    obj.source = SimpleNamespace(kind="file", id="file-1")
    materialized = SimpleNamespace(
        representation="file_metadata",
        text='{"requested_file":',
        offset=0,
        total_chars=72,
        has_more=True,
        next_offset=18,
        page_range=None,
    )

    async def materialize(*args: Any, **kwargs: Any) -> Any:
        return materialized

    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=_app_ctx()),
        patch(
            "matrx_ai._ext.get_ext",
            side_effect=lambda name: (
                (lambda _app: _manifest([obj]))
                if name == "load_manifest_from_ctx"
                else materialize
            ),
        ),
        patch("matrx_ai._ext.has_ext", return_value=True),
    ):
        result = await ctx_get({"key": "resource_file_1", "mode": "page"}, _ctx())

    assert result.success is True
    assert result.output.content == '{"requested_file":'
    assert result.output.has_more is True


# --------------------------------------------------------------------------
# create denial — actionable for the MODEL, which cannot flip the caller's gate
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_denial_tells_the_model_what_it_can_do_and_to_stop() -> None:
    """The old message named `allow_context_create=true` — a caller-side switch
    the model cannot touch — so it retried with guessed args instead."""
    from matrx_ai.tools.implementations.ctx import context

    app_ctx = _app_ctx()
    app_ctx.metadata = {"allow_context_create": False}
    with patch("matrx_ai.context.app_context.get_app_context", return_value=app_ctx):
        result = await context(
            {"action": "create", "key": "plan", "content": "{}", "type": "json"}, _ctx()
        )

    assert result.success is False
    assert result.error.error_type == "context_create_disabled"
    msg = result.error.message
    assert "Do NOT retry" in msg
    assert "will not change during this conversation" in msg
    # Names a path the model can actually take.
    assert "pass it directly as an argument" in msg
    # And no longer instructs it to flip a flag it does not control.
    assert "allow_context_create=true" not in msg


# --------------------------------------------------------------------------
# batch — the roll-up must not invite the retry the sub-errors just forbade
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_batch_all_missing_keys_forbids_the_retry() -> None:
    from matrx_ai.tools.implementations.ctx import ctx_batch

    manifest = _manifest([_obj("present")])
    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=_app_ctx()),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: manifest),
        patch("matrx_ai._ext.has_ext", return_value=False),
    ):
        result = await ctx_batch({"requests": [{"key": "nope_one"}, {"key": "nope_two"}]}, _ctx())

    assert result.success is False
    assert result.error.error_type == "context_not_attached"
    assert "Do NOT retry" in (result.error.suggested_action or "")


@pytest.mark.asyncio
async def test_batch_partial_failure_still_reports_the_successful_keys() -> None:
    from matrx_ai.tools.implementations.ctx import ctx_batch

    manifest = _manifest([_obj("present", "value here")])
    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=_app_ctx()),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: manifest),
        patch("matrx_ai._ext.has_ext", return_value=False),
    ):
        result = await ctx_batch({"requests": [{"key": "present"}, {"key": "missing"}]}, _ctx())

    assert result.error.error_type == "context_not_attached"
    assert result.output.results[0].success is True
    assert result.output.results[1].success is False


@pytest.mark.asyncio
async def test_batch_children_get_alias_reconciliation_too() -> None:
    """Batch delegates to the public ctx_get, so reconciliation is not a
    get-only privilege."""
    from matrx_ai.tools.implementations.ctx import ctx_batch

    manifest = _manifest([_obj("route_brief", "brief body")])
    with (
        patch("matrx_ai.context.app_context.get_app_context", return_value=_app_ctx()),
        patch("matrx_ai._ext.get_ext", return_value=lambda _app: manifest),
        patch("matrx_ai._ext.has_ext", return_value=False),
    ):
        result = await ctx_batch({"requests": [{"key": "routeBrief"}]}, _ctx())

    assert result.success is True
    assert result.output.results[0].output["content"] == "brief body"
