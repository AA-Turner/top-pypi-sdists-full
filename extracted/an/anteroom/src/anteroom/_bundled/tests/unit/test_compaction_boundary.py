"""Tests for boundary-based compaction (#1413).

Covers :func:`services.compaction._find_tail_boundary` directly and the
``preserve_tail`` behaviour of :func:`services.compaction.compact_messages`
exposed through the agent-loop wrapper.  Also validates the provider-safe
ordering invariant and the ``CliConfig.compact_preserve_tail`` config
contract.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock

import pytest

from anteroom.services.compaction import _find_tail_boundary

# ---------------------------------------------------------------------------
# _find_tail_boundary
# ---------------------------------------------------------------------------


class TestFindTailBoundary:
    """Unit tests for the tail boundary selection algorithm."""

    def test_basic_split(self) -> None:
        """Simple case: enough messages, clean user boundary."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "m0"},
            {"role": "assistant", "content": "m1"},
            {"role": "user", "content": "m2"},
            {"role": "assistant", "content": "m3"},
            {"role": "user", "content": "m4"},
            {"role": "assistant", "content": "m5"},
            {"role": "user", "content": "m6"},
            {"role": "assistant", "content": "m7"},
        ]
        # preserve_count=4 -> candidate = 8-4 = 4 (msgs[4] is user) -> split at 4
        idx = _find_tail_boundary(msgs, preserve_count=4)
        assert idx == 4
        assert msgs[idx]["role"] == "user"

    def test_tool_orphan_prevention(self) -> None:
        """Split point walks back past orphaned tool results."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "m0"},
            {"role": "assistant", "content": "m1"},
            {"role": "user", "content": "m2"},
            {"role": "assistant", "content": "m3", "tool_calls": [{"id": "tc1"}]},
            {"role": "tool", "content": "result1", "tool_call_id": "tc1"},
            {"role": "tool", "content": "result2", "tool_call_id": "tc2"},
            {"role": "user", "content": "m6"},
            {"role": "assistant", "content": "m7"},
        ]
        idx = _find_tail_boundary(msgs, preserve_count=3)
        assert idx == 2
        assert msgs[idx]["role"] == "user"

    def test_user_first_guarantee(self) -> None:
        """Tail must start with user for provider-safe ordering."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "m0"},
            {"role": "assistant", "content": "m1"},
            {"role": "assistant", "content": "m2"},
            {"role": "user", "content": "m3"},
            {"role": "assistant", "content": "m4"},
        ]
        idx = _find_tail_boundary(msgs, preserve_count=2)
        assert idx == 3
        assert msgs[idx]["role"] == "user"

    def test_walks_back_to_user(self) -> None:
        """When candidate lands on assistant, walks back to find user."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "m0"},
            {"role": "assistant", "content": "m1"},
            {"role": "user", "content": "m2"},
            {"role": "assistant", "content": "m3"},
            {"role": "assistant", "content": "m4"},
        ]
        idx = _find_tail_boundary(msgs, preserve_count=2)
        assert idx == 2
        assert msgs[idx]["role"] == "user"

    def test_fallback_too_few_messages(self) -> None:
        """Returns 0 when fewer than preserve_count + 2 messages."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "m0"},
            {"role": "assistant", "content": "m1"},
        ]
        assert _find_tail_boundary(msgs, preserve_count=6) == 0

    def test_fallback_all_assistant_messages(self) -> None:
        """Returns 0 when no user message in range."""
        msgs: list[dict[str, Any]] = [
            {"role": "system", "content": "sys"},
            {"role": "assistant", "content": "m1"},
            {"role": "assistant", "content": "m2"},
            {"role": "assistant", "content": "m3"},
            {"role": "assistant", "content": "m4"},
            {"role": "assistant", "content": "m5"},
            {"role": "assistant", "content": "m6"},
            {"role": "assistant", "content": "m7"},
            {"role": "assistant", "content": "m8"},
            {"role": "assistant", "content": "m9"},
        ]
        assert _find_tail_boundary(msgs, preserve_count=4) == 0

    def test_preserve_zero_returns_zero(self) -> None:
        """preserve_count=0 short-circuits to full-summary fallback."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "q"},
            {"role": "assistant", "content": "a"},
            {"role": "user", "content": "q2"},
            {"role": "assistant", "content": "a2"},
        ]
        assert _find_tail_boundary(msgs, preserve_count=0) == 0

    def test_single_user_at_start(self) -> None:
        """When only user message is at index 0, returns 0 (degenerate case)."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "m0"},
            {"role": "assistant", "content": "m1"},
            {"role": "assistant", "content": "m2"},
            {"role": "assistant", "content": "m3"},
            {"role": "assistant", "content": "m4"},
            {"role": "assistant", "content": "m5"},
            {"role": "assistant", "content": "m6"},
            {"role": "assistant", "content": "m7"},
        ]
        assert _find_tail_boundary(msgs, preserve_count=4) == 0

    def test_system_messages_skipped(self) -> None:
        """System messages don't satisfy the user-first rule."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "m0"},
            {"role": "assistant", "content": "m1"},
            {"role": "user", "content": "m2"},
            {"role": "system", "content": "injected"},
            {"role": "assistant", "content": "m4"},
            {"role": "user", "content": "m5"},
            {"role": "assistant", "content": "m6"},
        ]
        idx = _find_tail_boundary(msgs, preserve_count=3)
        assert idx == 2
        assert msgs[idx]["role"] == "user"


# ---------------------------------------------------------------------------
# compact_messages integration (exercised via the agent-loop wrapper)
# ---------------------------------------------------------------------------


def _make_ai_service() -> Any:
    """Construct a fake ``AIService`` whose ``complete()`` is asyncmockable."""
    from anteroom.config import AIConfig
    from anteroom.services.ai_service import AIService

    cfg = AIConfig(base_url="http://localhost/v1", api_key="k", model="m", request_timeout=10, verify_ssl=True)
    return AIService(cfg)


@pytest.mark.asyncio
async def test_compact_preserves_tail_messages_intact() -> None:
    """After compaction, tail messages are preserved unmodified."""
    from anteroom.services.agent_loop import _compact_messages

    svc = _make_ai_service()
    svc.complete = AsyncMock(return_value="Summary of old stuff")

    msgs: list[dict[str, Any]] = [
        {"role": "user", "content": "old question 1"},
        {"role": "assistant", "content": "old answer 1"},
        {"role": "user", "content": "old question 2"},
        {"role": "assistant", "content": "old answer 2"},
        {"role": "user", "content": "old question 3"},
        {"role": "assistant", "content": "old answer 3"},
        {"role": "user", "content": "old question 4"},
        {"role": "assistant", "content": "old answer 4"},
        {"role": "user", "content": "recent question"},
        {"role": "assistant", "content": "recent answer"},
    ]

    result = await _compact_messages(svc, msgs, preserve_tail=4)
    assert result is True

    # First message is the summary
    assert msgs[0]["role"] == "user"
    assert "auto-compacted" in msgs[0]["content"]
    assert "Summary of old stuff" in msgs[0]["content"]

    # Tail preserved — last two should be the recent exchange
    assert msgs[-2]["content"] == "recent question"
    assert msgs[-1]["content"] == "recent answer"


@pytest.mark.asyncio
async def test_compact_summary_only_covers_old_messages() -> None:
    """The summary prompt only includes messages from the head (old) portion."""
    from anteroom.services.agent_loop import _compact_messages

    svc = _make_ai_service()
    captured_prompt: list[str] = []

    async def fake_complete(messages: list[dict[str, Any]], **kwargs: Any) -> str:
        captured_prompt.append(messages[0]["content"])
        return "Summary"

    svc.complete = fake_complete  # type: ignore[assignment]

    msgs: list[dict[str, Any]] = [
        {"role": "user", "content": "old stuff"},
        {"role": "assistant", "content": "old response"},
        {"role": "user", "content": "more old"},
        {"role": "assistant", "content": "more old response"},
        {"role": "user", "content": "SHOULD_NOT_BE_IN_SUMMARY"},
        {"role": "assistant", "content": "tail response"},
    ]

    await _compact_messages(svc, msgs, preserve_tail=2)

    assert captured_prompt
    assert "SHOULD_NOT_BE_IN_SUMMARY" not in captured_prompt[0]
    assert "old stuff" in captured_prompt[0]


@pytest.mark.asyncio
async def test_compact_fallback_full_summary() -> None:
    """When _find_tail_boundary returns 0, all messages get summarised (fallback)."""
    from anteroom.services.agent_loop import _compact_messages

    svc = _make_ai_service()
    svc.complete = AsyncMock(return_value="Full summary")

    # Only 4 messages, preserve_tail=6 -> tail_boundary returns 0 (too few).
    msgs: list[dict[str, Any]] = [
        {"role": "user", "content": "q"},
        {"role": "assistant", "content": "a"},
        {"role": "user", "content": "q2"},
        {"role": "assistant", "content": "a2"},
    ]

    result = await _compact_messages(svc, msgs, preserve_tail=6)
    assert result is True
    # Fallback: all messages summarised, result is just the summary
    assert len(msgs) == 1
    assert "Full summary" in msgs[0]["content"]


@pytest.mark.asyncio
async def test_compact_preserve_tail_zero_full_summary() -> None:
    """preserve_tail=0 always does full summary (legacy behavior)."""
    from anteroom.services.agent_loop import _compact_messages

    svc = _make_ai_service()
    svc.complete = AsyncMock(return_value="Full summary")

    msgs: list[dict[str, Any]] = [
        {"role": "user", "content": "q1"},
        {"role": "assistant", "content": "a1"},
        {"role": "user", "content": "q2"},
        {"role": "assistant", "content": "a2"},
        {"role": "user", "content": "q3"},
        {"role": "assistant", "content": "a3"},
    ]

    result = await _compact_messages(svc, msgs, preserve_tail=0)
    assert result is True
    assert len(msgs) == 1
    assert "Full summary" in msgs[0]["content"]


@pytest.mark.asyncio
async def test_compact_messages_empty_summary_leaves_history_untouched() -> None:
    """If ``ai_service.complete()`` returns falsy, messages are unchanged.

    Guards the contract #1421 established: provider errors must never silently
    collapse a live conversation.
    """
    from anteroom.services.agent_loop import _compact_messages

    svc = _make_ai_service()
    svc.complete = AsyncMock(return_value=None)

    msgs: list[dict[str, Any]] = [
        {"role": "user", "content": "q1"},
        {"role": "assistant", "content": "a1"},
        {"role": "user", "content": "q2"},
        {"role": "assistant", "content": "a2"},
        {"role": "user", "content": "q3"},
        {"role": "assistant", "content": "a3"},
        {"role": "user", "content": "q4"},
        {"role": "assistant", "content": "a4"},
    ]
    snapshot = [dict(m) for m in msgs]

    result = await _compact_messages(svc, msgs, preserve_tail=4)
    assert result is False
    assert msgs == snapshot


@pytest.mark.asyncio
async def test_compact_with_preserve_tail_llm_exception_leaves_history_untouched() -> None:
    """``complete()`` raising on a boundary-mode call leaves messages alone.

    Parallels the legacy exception test in ``test_compaction.py`` but exercises
    the ``preserve_tail > 0`` code path so exception handling inside the
    boundary branch is explicitly covered.
    """
    from anteroom.services.agent_loop import _compact_messages

    svc = _make_ai_service()
    svc.complete = AsyncMock(side_effect=RuntimeError("LLM unavailable"))

    msgs: list[dict[str, Any]] = [
        {"role": "user", "content": "q1"},
        {"role": "assistant", "content": "a1"},
        {"role": "user", "content": "q2"},
        {"role": "assistant", "content": "a2"},
        {"role": "user", "content": "q3"},
        {"role": "assistant", "content": "a3"},
        {"role": "user", "content": "q4"},
        {"role": "assistant", "content": "a4"},
    ]
    snapshot = [dict(m) for m in msgs]

    result = await _compact_messages(svc, msgs, preserve_tail=4)
    assert result is False
    assert msgs == snapshot


@pytest.mark.asyncio
async def test_compact_messages_summarised_count_equals_head_length() -> None:
    """The rendered summary template counts ``len(head)``, not full history.

    Guards the docstring promise that ``original_count`` in the compacted
    template text equals the number of *summarised* messages (head), not the
    total input length, when a tail is preserved.  Full-summary path
    (``split == 0``) reports the full count exactly as before.
    """
    from anteroom.services.compaction import AGENT_LOOP_CONTENT_TEMPLATE, compact_messages

    svc = _make_ai_service()
    svc.complete = AsyncMock(return_value="The summary")

    # 10 messages total; preserve_tail=4 -> head length should be 6.
    msgs: list[dict[str, Any]] = [
        {"role": "user", "content": "q1"},
        {"role": "assistant", "content": "a1"},
        {"role": "user", "content": "q2"},
        {"role": "assistant", "content": "a2"},
        {"role": "user", "content": "q3"},
        {"role": "assistant", "content": "a3"},
        {"role": "user", "content": "q4"},
        {"role": "assistant", "content": "a4"},
        {"role": "user", "content": "q5"},
        {"role": "assistant", "content": "a5"},
    ]

    result = await compact_messages(svc, msgs, preserve_tail=4)
    assert result.success is True
    # The template is rendered with summarised_count=len(head)=6.
    expected = AGENT_LOOP_CONTENT_TEMPLATE.format(original_count=6, summary="The summary")
    assert msgs[0]["content"] == expected
    # Shape: [summary, boundary_marker, *tail] — summary + marker + 4 tail messages.
    assert len(msgs) == 1 + 1 + 4
    assert msgs[1]["role"] == "system"
    assert msgs[1]["metadata"]["compact_boundary"] is True
    assert msgs[1]["metadata"]["preserved_count"] == 4


@pytest.mark.asyncio
async def test_compact_messages_full_summary_path_reports_original_count() -> None:
    """When split == 0 (full-summary fallback), count equals full history length.

    The backward-compat guarantee is that ``preserve_tail=0`` or a forced
    fallback produces the same rendered text as the legacy (#1421) shape.
    """
    from anteroom.services.compaction import AGENT_LOOP_CONTENT_TEMPLATE, compact_messages

    svc = _make_ai_service()
    svc.complete = AsyncMock(return_value="Full summary")

    msgs: list[dict[str, Any]] = [
        {"role": "user", "content": "q1"},
        {"role": "assistant", "content": "a1"},
        {"role": "user", "content": "q2"},
        {"role": "assistant", "content": "a2"},
        {"role": "user", "content": "q3"},
        {"role": "assistant", "content": "a3"},
    ]

    result = await compact_messages(svc, msgs, preserve_tail=0)
    assert result.success is True
    expected = AGENT_LOOP_CONTENT_TEMPLATE.format(original_count=6, summary="Full summary")
    assert msgs[0]["content"] == expected
    assert len(msgs) == 1


class TestFindTailBoundaryWalkBackInteraction:
    """Rule 1 (tool-orphan) + Rule 2 (user-first) firing sequentially."""

    def test_single_tool_directly_after_assistant_walks_past_both(self) -> None:
        """One tool message at the boundary: walk past tool (Rule 1), past
        the parent assistant (Rule 2), land on the preceding user."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "m0"},
            {"role": "assistant", "content": "m1"},
            {"role": "user", "content": "m2"},
            {"role": "assistant", "content": "m3", "tool_calls": [{"id": "tc1"}]},
            {"role": "tool", "content": "result1", "tool_call_id": "tc1"},
            {"role": "assistant", "content": "m5"},
            {"role": "user", "content": "m6"},
            {"role": "assistant", "content": "m7"},
        ]
        # preserve_count=4 -> candidate = 8-4 = 4, msgs[4] is tool.
        # Rule 1: walk back 4 -> 3 (assistant, stop tool-loop).
        # Rule 2: msgs[3] is assistant, walk back to msgs[2] (user).
        idx = _find_tail_boundary(msgs, preserve_count=4)
        assert idx == 2
        assert msgs[idx]["role"] == "user"


class TestBoundaryMarker:
    """Verify the boundary marker emitted between summary and tail."""

    @pytest.mark.asyncio
    async def test_boundary_marker_inserted_between_summary_and_tail(self) -> None:
        """Shape is ``[summary, boundary, *tail]`` when a tail is preserved."""
        from anteroom.services.agent_loop import _compact_messages

        svc = _make_ai_service()
        svc.complete = AsyncMock(return_value="S")

        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "q2"},
            {"role": "assistant", "content": "a2"},
            {"role": "user", "content": "q3"},
            {"role": "assistant", "content": "a3"},
            {"role": "user", "content": "q4"},
            {"role": "assistant", "content": "a4"},
        ]

        await _compact_messages(svc, msgs, preserve_tail=4)

        # [summary (user), boundary (system), 4 tail messages]
        assert len(msgs) == 6
        assert msgs[1]["role"] == "system"
        assert msgs[1]["metadata"]["compact_boundary"] is True
        # Tail untouched.
        assert msgs[-1]["content"] == "a4"

    @pytest.mark.asyncio
    async def test_boundary_marker_metadata_fields(self) -> None:
        """Marker carries original/preserved counts + summary token estimate."""
        from anteroom.services.agent_loop import _compact_messages

        svc = _make_ai_service()
        svc.complete = AsyncMock(return_value="This is the summary text.")

        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "q2"},
            {"role": "assistant", "content": "a2"},
            {"role": "user", "content": "q3"},
            {"role": "assistant", "content": "a3"},
            {"role": "user", "content": "q4"},
            {"role": "assistant", "content": "a4"},
        ]

        await _compact_messages(svc, msgs, preserve_tail=4)

        marker = msgs[1]
        meta = marker["metadata"]
        assert meta["compact_boundary"] is True
        assert meta["original_count"] == 4  # summarised head length
        assert meta["preserved_count"] == 4
        assert isinstance(meta["summary_tokens"], int)
        assert meta["summary_tokens"] > 0
        assert "compacted_at" in meta

    @pytest.mark.asyncio
    async def test_no_boundary_marker_in_full_summary_fallback(self) -> None:
        """``preserve_tail=0`` → legacy shape, no boundary marker."""
        from anteroom.services.agent_loop import _compact_messages

        svc = _make_ai_service()
        svc.complete = AsyncMock(return_value="Full summary")

        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "q2"},
            {"role": "assistant", "content": "a2"},
        ]

        await _compact_messages(svc, msgs, preserve_tail=0)
        assert len(msgs) == 1
        assert msgs[0].get("metadata", {}).get("compact_boundary") is not True

    @pytest.mark.asyncio
    async def test_summary_metadata_compact_summary_flag(self) -> None:
        """Summary carries ``metadata.compact_summary: True`` for #1414 detection."""
        from anteroom.services.agent_loop import _compact_messages

        svc = _make_ai_service()
        svc.complete = AsyncMock(return_value="Summary")

        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "q1"},
            {"role": "assistant", "content": "a1"},
            {"role": "user", "content": "q2"},
            {"role": "assistant", "content": "a2"},
            {"role": "user", "content": "q3"},
            {"role": "assistant", "content": "a3"},
            {"role": "user", "content": "q4"},
            {"role": "assistant", "content": "a4"},
        ]

        await _compact_messages(svc, msgs, preserve_tail=4)
        assert msgs[0].get("metadata", {}).get("compact_summary") is True


class TestProviderSafeTail:
    """Verify that the compacted conversation is valid for all providers."""

    def test_compacted_tail_never_starts_with_assistant(self) -> None:
        """The preserved tail always starts with role: user."""
        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "old"},
            {"role": "assistant", "content": "old reply"},
            {"role": "user", "content": "old 2"},
            {"role": "assistant", "content": "old reply 2"},
            {"role": "assistant", "content": "continued"},
            {"role": "user", "content": "recent q"},
            {"role": "assistant", "content": "recent a"},
        ]
        idx = _find_tail_boundary(msgs, preserve_count=2)
        assert idx > 0
        assert msgs[idx]["role"] == "user"

    def test_compacted_tail_fallback_when_no_user_message(self) -> None:
        """Falls back to 0 if no user message exists in the conversation."""
        msgs: list[dict[str, Any]] = [
            {"role": "system", "content": "sys"},
            {"role": "assistant", "content": "a1"},
            {"role": "assistant", "content": "a2"},
            {"role": "assistant", "content": "a3"},
            {"role": "assistant", "content": "a4"},
            {"role": "assistant", "content": "a5"},
            {"role": "assistant", "content": "a6"},
            {"role": "assistant", "content": "a7"},
        ]
        idx = _find_tail_boundary(msgs, preserve_count=3)
        assert idx == 0

    @pytest.mark.asyncio
    async def test_resumed_compacted_conversation_valid_for_anthropic(self) -> None:
        """Simulated resume: summary + user-first tail is valid."""
        from anteroom.services.agent_loop import _compact_messages

        svc = _make_ai_service()
        svc.complete = AsyncMock(return_value="Summary")

        msgs: list[dict[str, Any]] = [
            {"role": "user", "content": "old q"},
            {"role": "assistant", "content": "old a"},
            {"role": "user", "content": "mid q"},
            {"role": "assistant", "content": "mid a"},
            {"role": "user", "content": "recent q"},
            {"role": "assistant", "content": "recent a"},
        ]

        await _compact_messages(svc, msgs, preserve_tail=2)

        # The in-memory form: [summary, boundary_marker, *tail].  Anthropic's
        # ``_convert_messages()`` extracts system messages into the system
        # prompt, so the first non-system message must be ``user``.
        non_system = [m for m in msgs if m.get("role") != "system"]
        if non_system:
            assert non_system[0]["role"] == "user"


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


class TestCompactionConfig:
    """Verify the shared ``CompactionConfig.preserve_tail`` config field (#1413)."""

    def test_default_value(self) -> None:
        from anteroom.config import CompactionConfig

        cfg = CompactionConfig()
        assert cfg.preserve_tail == 6

    def test_custom_value(self) -> None:
        from anteroom.config import CompactionConfig

        cfg = CompactionConfig(preserve_tail=10)
        assert cfg.preserve_tail == 10

    def test_zero_disables_tail_preservation(self) -> None:
        from anteroom.config import CompactionConfig

        cfg = CompactionConfig(preserve_tail=0)
        assert cfg.preserve_tail == 0

    def test_loader_reads_compaction_section(self, tmp_path: Any) -> None:
        """Primary config surface: ``compaction.preserve_tail``."""
        import yaml

        from anteroom.config import load_config

        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(
            yaml.dump(
                {
                    "ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"},
                    "compaction": {"preserve_tail": 12},
                }
            )
        )
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.preserve_tail == 12

    def test_loader_accepts_legacy_cli_key(self, tmp_path: Any) -> None:
        """``cli.compact_preserve_tail`` is accepted as a deprecated alias."""
        import yaml

        from anteroom.config import load_config

        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(
            yaml.dump(
                {
                    "ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"},
                    "cli": {"compact_preserve_tail": 8},
                }
            )
        )
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.preserve_tail == 8

    def test_loader_compaction_overrides_legacy(self, tmp_path: Any) -> None:
        """Explicit ``compaction.preserve_tail`` wins over the legacy CLI key."""
        import yaml

        from anteroom.config import load_config

        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(
            yaml.dump(
                {
                    "ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"},
                    "compaction": {"preserve_tail": 4},
                    "cli": {"compact_preserve_tail": 99},
                }
            )
        )
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.preserve_tail == 4

    def test_loader_clamps_upper_bound(self, tmp_path: Any) -> None:
        """``preserve_tail=999999`` is clamped to the 200 cap."""
        import yaml

        from anteroom.config import load_config

        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(
            yaml.dump(
                {
                    "ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"},
                    "compaction": {"preserve_tail": 999_999},
                }
            )
        )
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.preserve_tail == 200

    def test_loader_clamps_env_upper_bound(self, tmp_path: Any, monkeypatch: Any) -> None:
        """``AI_CHAT_COMPACT_PRESERVE_TAIL=999999`` is clamped to 200."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_COMPACT_PRESERVE_TAIL", "999999")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.preserve_tail == 200

    def test_loader_clamps_negative_to_zero(self, tmp_path: Any) -> None:
        """Negative values clamp to 0 (full-summary)."""
        import yaml

        from anteroom.config import load_config

        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(
            yaml.dump(
                {
                    "ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"},
                    "compaction": {"preserve_tail": -5},
                }
            )
        )
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.preserve_tail == 0


class TestMicrocompactPipelineConfig:
    """Config fields added in #1266 for the multi-stage context pipeline."""

    def test_defaults(self) -> None:
        """Defaults match shipped behavior — microcompact on, legacy thresholds preserved."""
        from anteroom.config import CompactionConfig

        cfg = CompactionConfig()
        assert cfg.microcompact_enabled is True
        assert cfg.summary_trigger_msg_count == 80
        assert cfg.summary_trigger_token_count == 90_000
        assert cfg.reactive_max_attempts == 4

    def test_env_var_parse_microcompact_enabled_false(self, tmp_path: Any, monkeypatch: Any) -> None:
        """AI_CHAT_MICROCOMPACT_ENABLED=false disables the proactive stage."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_MICROCOMPACT_ENABLED", "false")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.microcompact_enabled is False

    def test_env_var_parse_summary_msg_count_clamped_upper(self, tmp_path: Any, monkeypatch: Any) -> None:
        """summary_trigger_msg_count is clamped to [10, 1000]."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_MSG_COUNT", "99999")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.summary_trigger_msg_count == 1000

    def test_env_var_parse_summary_msg_count_clamped_lower(self, tmp_path: Any, monkeypatch: Any) -> None:
        """summary_trigger_msg_count below 10 clamps to 10."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_MSG_COUNT", "3")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.summary_trigger_msg_count == 10

    def test_env_var_parse_summary_token_count_clamped(self, tmp_path: Any, monkeypatch: Any) -> None:
        """summary_trigger_token_count is clamped to [5_000, 500_000]."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_TOKEN_COUNT", "999999999")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.summary_trigger_token_count == 500_000

    def test_env_var_parse_reactive_max_attempts_clamped(self, tmp_path: Any, monkeypatch: Any) -> None:
        """reactive_max_attempts is clamped to [0, 10]."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_REACTIVE_MAX_ATTEMPTS", "99")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.reactive_max_attempts == 10

    def test_yaml_wins_over_env(self, tmp_path: Any, monkeypatch: Any) -> None:
        """YAML config takes precedence over env vars."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_MSG_COUNT", "50")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(
            yaml.dump(
                {
                    "ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"},
                    "compaction": {"summary_trigger_msg_count": 200},
                }
            )
        )
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.summary_trigger_msg_count == 200

    def test_summary_token_count_clamped_lower(self, tmp_path: Any, monkeypatch: Any) -> None:
        """summary_trigger_token_count below 5000 clamps to 5000."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_TOKEN_COUNT", "1")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.summary_trigger_token_count == 5_000

    def test_reactive_max_attempts_clamped_lower(self, tmp_path: Any, monkeypatch: Any) -> None:
        """reactive_max_attempts below 0 clamps to 0 (disabled)."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_REACTIVE_MAX_ATTEMPTS", "-5")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.reactive_max_attempts == 0

    def test_non_numeric_env_falls_back_to_default(self, tmp_path: Any, monkeypatch: Any) -> None:
        """Non-numeric env vars fall back to defaults without crashing."""
        import yaml

        from anteroom.config import load_config

        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_MSG_COUNT", "not-a-number")
        monkeypatch.setenv("AI_CHAT_SUMMARY_TRIGGER_TOKEN_COUNT", "abc")
        monkeypatch.setenv("AI_CHAT_REACTIVE_MAX_ATTEMPTS", "xyz")
        cfg_path = tmp_path / "config.yaml"
        cfg_path.write_text(yaml.dump({"ai": {"base_url": "http://localhost/v1", "api_key": "k", "model": "m"}}))
        cfg, _ = load_config(cfg_path)
        assert cfg.compaction.summary_trigger_msg_count == 80
        assert cfg.compaction.summary_trigger_token_count == 90_000
        assert cfg.compaction.reactive_max_attempts == 4
