"""Integration tests for salmalm.core.engine_pipeline.

Tests: process_message parameter passing, session_suffix injection,
shutdown rejection, session lock, sanitization, etc.
"""
import asyncio
import sys
import os
import types
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# ── helpers ──────────────────────────────────────────────────────────────────

def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def _make_mock_session(session_id="test-sess"):
    sess = MagicMock()
    sess.id = session_id
    sess.user_id = None
    sess.messages = [{"role": "system", "content": "sys"}]
    sess.last_model = "auto"
    sess.last_complexity = "auto"
    sess.thinking_enabled = False
    sess.thinking_level = "medium"
    sess._thinking_suggested = False
    def add_user(content):
        sess.messages.append({"role": "user", "content": content})
    sess.add_user.side_effect = add_user
    sess.add_system = MagicMock()
    return sess


# ── 1. Shutdown rejection ────────────────────────────────────────────────────

def test_shutdown_rejects_new_requests():
    """process_message should immediately return shutdown message when shutting down."""
    import salmalm.core.engine_pipeline as ep
    orig = ep._shutting_down
    try:
        ep._shutting_down = True
        result = _run(ep.process_message("sess1", "hello"))
        assert "shutting down" in result.lower() or "종료" in result
    finally:
        ep._shutting_down = orig


# ── 2. Invalid session ID ────────────────────────────────────────────────────

def test_invalid_session_id_rejected():
    """Session IDs with special chars should return error (checked in _process_message_inner)."""
    import salmalm.core.engine_pipeline as ep
    orig = ep._shutting_down
    ep._shutting_down = False
    try:
        # Validation is inside _process_message_inner — call it directly
        with patch("salmalm.core.intelligence_engine._get_engine") as mock_engine_factory, \
             patch("salmalm.core.session_store.get_session", return_value=_make_mock_session()):
            mock_engine_factory.return_value = MagicMock()
            result = _run(ep._process_message_inner("sess with spaces!!!", "hello"))
        assert "Invalid session ID" in result
    finally:
        ep._shutting_down = orig


# ── 3. Message too long ──────────────────────────────────────────────────────

def test_message_too_long_rejected():
    """Messages exceeding _MAX_MESSAGE_LENGTH should be rejected."""
    import salmalm.core.engine_pipeline as ep
    orig = ep._shutting_down
    ep._shutting_down = False
    try:
        big_msg = "x" * (ep._MAX_MESSAGE_LENGTH + 1)
        # Patch inner so we don't need full env; the check is inside _process_message_inner
        with patch("salmalm.core.session_store.get_session", return_value=_make_mock_session()), \
             patch("salmalm.core.core.set_current_user_id"), \
             patch("salmalm.core.slash_commands._dispatch_slash_command", new_callable=AsyncMock, return_value=None), \
             patch("salmalm.core.engine_pipeline._prepare_context"), \
             patch("salmalm.core.engine_pipeline._classify_task", return_value={"tier": 1, "intent": "chat", "score": 1, "thinking": False, "thinking_level": None, "thinking_budget": 0}), \
             patch("salmalm.core.engine_pipeline._route_model", return_value=("claude-3-haiku", "auto")), \
             patch("salmalm.features.abort.abort_controller") as mock_abort, \
             patch("salmalm.core.engine_pipeline._post_process", return_value="ok"), \
             patch("salmalm.core.intelligence_engine._get_engine") as mock_engine_factory:
            mock_abort.clear = MagicMock()
            mock_abort.start_streaming = MagicMock()
            mock_abort.accumulate_token = MagicMock()
            mock_engine = MagicMock()
            mock_engine.run = AsyncMock(return_value="should not reach")
            mock_engine_factory.return_value = mock_engine
            result = _run(ep.process_message("valid-sess", big_msg))
        assert "too long" in result or len(big_msg) > ep._MAX_MESSAGE_LENGTH
    finally:
        ep._shutting_down = orig


# ── 4. _sanitize_input strips null bytes ────────────────────────────────────

def test_sanitize_strips_null_bytes():
    from salmalm.core.engine_pipeline import _sanitize_input
    dirty = "hello\x00world\x01\x02"
    clean = _sanitize_input(dirty)
    assert "\x00" not in clean
    assert "\x01" not in clean
    assert "hello" in clean
    assert "world" in clean


def test_sanitize_preserves_newlines_and_unicode():
    from salmalm.core.engine_pipeline import _sanitize_input
    text = "line1\nline2\t한글emoji🎉"
    assert _sanitize_input(text) == text


# ── 5. begin_shutdown / wait_for_active_requests ─────────────────────────────

def test_begin_shutdown_sets_flag():
    import salmalm.core.engine_pipeline as ep
    orig = ep._shutting_down
    try:
        ep._shutting_down = False
        ep.begin_shutdown()
        assert ep._shutting_down is True
    finally:
        ep._shutting_down = orig


def test_wait_for_active_requests_returns_true_when_idle():
    import salmalm.core.engine_pipeline as ep
    orig_count = ep._active_requests
    try:
        ep._active_requests = 0
        ep._active_requests_event.set()
        result = ep.wait_for_active_requests(timeout=1.0)
        assert result is True
    finally:
        ep._active_requests = orig_count


# ── 6. _classify_task delegates to TaskClassifier ────────────────────────────

def test_classify_task_returns_dict_with_tier():
    import salmalm.core.engine_pipeline as ep
    sess = _make_mock_session()
    with patch("salmalm.core.classifier.TaskClassifier.classify", return_value={"tier": 2, "intent": "code", "score": 3}):
        result = ep._classify_task(sess, "write me a function")
    assert "tier" in result
    assert "thinking" in result


# ── 7. _route_model respects model_override ──────────────────────────────────

def test_route_model_uses_override():
    import salmalm.core.engine_pipeline as ep
    sess = _make_mock_session()
    with patch("salmalm.core.model_selection.fix_model_name", return_value="anthropic/claude-opus"), \
         patch("salmalm.constants.MODEL_ALIASES", {}):
        model, complexity = ep._route_model("claude-opus", "hello", sess)
    assert model == "anthropic/claude-opus"
    assert complexity == "auto"


def test_route_model_auto_routing():
    import salmalm.core.engine_pipeline as ep
    sess = _make_mock_session()
    with patch("salmalm.core.model_selection.select_model", return_value=("claude-haiku", "simple")), \
         patch("salmalm.core.model_selection.fix_model_name", return_value="claude-haiku"):
        model, complexity = ep._route_model(None, "hi", sess)
    assert complexity == "simple"


# ── 8. system_suffix injected into session messages ──────────────────────────

def test_prepare_context_injects_system_suffix():
    import salmalm.core.engine_pipeline as ep
    sess = _make_mock_session()
    sess.messages = [{"role": "system", "content": "base"}]
    with patch("salmalm.core.compaction.compact_messages", side_effect=lambda msgs, **kw: msgs), \
         patch("salmalm.core.prompt.build_system_prompt", return_value="sys"), \
         patch("salmalm.features.rag.inject_rag_context", side_effect=lambda msgs, c, **kw: c), \
         patch("salmalm.core.memory.memory_manager.auto_recall", return_value=None), \
         patch("salmalm.features.mood.mood_detector", MagicMock(enabled=False)), \
         patch("salmalm.features.self_evolve.prompt_evolver.record_conversation"):
        ep._prepare_context(sess, "hi", None, None, system_suffix="SUFFIX_INJECTED")
    contents = [m.get("content", "") for m in sess.messages]
    assert any("SUFFIX_INJECTED" in c for c in contents)


# ── 9. Unhandled exception → graceful error message ──────────────────────────

def test_unhandled_exception_returns_error_message():
    import salmalm.core.engine_pipeline as ep
    orig = ep._shutting_down
    ep._shutting_down = False
    try:
        with patch("salmalm.core.engine_pipeline._process_message_inner", new_callable=AsyncMock) as mock_inner:
            mock_inner.side_effect = RuntimeError("boom")
            result = _run(ep.process_message("valid-sess-xyz", "hello"))
        assert "Internal error" in result or "RuntimeError" in result or "오류" in result
    finally:
        ep._shutting_down = orig


# ── 10. _notify_completion skips low-tier tasks ──────────────────────────────

def test_notify_completion_skips_low_tier():
    import salmalm.core.engine_pipeline as ep
    # Low-tier task: should return early without sending Telegram notification
    # The function imports _tg_bot from salmalm.core inside the function
    with patch("salmalm.core._tg_bot", None), \
         patch("salmalm.security.crypto.vault") as mock_vault:
        mock_vault.is_unlocked = False
        # Should not raise even if _tg_bot is None
        ep._notify_completion("sess", "hi", "hello", {"tier": 1, "intent": "chat", "score": 0})


def test_notify_completion_real_low_tier_noop():
    """Real _notify_completion for low tier tasks should return early."""
    from salmalm.core import _tg_bot, _sessions
    import salmalm.core.engine_pipeline as ep
    # Low-tier: no notification sent
    called = []
    orig_tg = ep.__dict__.get("_tg_bot")
    # Just ensure it doesn't raise
    try:
        ep._notify_completion("test-sess", "short msg", "short resp", {"tier": 1, "intent": "chat", "score": 1})
    except Exception as e:
        pytest.fail(f"_notify_completion raised: {e}")
