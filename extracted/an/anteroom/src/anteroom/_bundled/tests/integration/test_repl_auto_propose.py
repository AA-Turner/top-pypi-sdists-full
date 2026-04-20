"""CLI inline-notice integration coverage for auto-propose (#1454).

The post-turn REPL wiring at ``cli/repl.py:7548`` invokes the runner and
then calls ``renderer.render_auto_propose_notice(items)``. The runner
itself is exhaustively unit-tested in ``tests/unit/test_auto_propose_runner.py``;
these tests pin the user-visible CLI surface so regressions in the
inline notice copy or rendering get caught at the UX boundary.
"""

from __future__ import annotations

import io

from rich.console import Console

from anteroom.cli import renderer


def _captured_console() -> tuple[Console, io.StringIO]:
    buf = io.StringIO()
    return Console(file=buf, force_terminal=False, no_color=True, width=120), buf


def _items(n: int = 1) -> list[dict[str, str]]:
    return [
        {
            "fqn": f"@user/memory/pref-abc{i}-20260419",
            "category": "preference",
            "content_preview": f"User prefers {['tabs', 'dark mode', 'vim', 'espresso'][i % 4]}.",
        }
        for i in range(n)
    ]


def test_render_auto_propose_notice_single_item() -> None:
    console, buf = _captured_console()
    original = renderer.console
    try:
        renderer.console = console
        renderer.render_auto_propose_notice(_items(1))
    finally:
        renderer.console = original

    output = buf.getvalue()
    assert "1 memory queued for review" in output
    assert "@user/memory/pref-abc0-20260419" in output
    assert "/memory candidates" in output


def test_render_auto_propose_notice_plural_items() -> None:
    console, buf = _captured_console()
    original = renderer.console
    try:
        renderer.console = console
        renderer.render_auto_propose_notice(_items(3))
    finally:
        renderer.console = original

    output = buf.getvalue()
    # Plural noun.
    assert "3 memories queued for review" in output
    # Only the first FQN is shown to keep the line short.
    assert "@user/memory/pref-abc0-20260419" in output
    assert "@user/memory/pref-abc2-20260419" not in output


def test_render_auto_propose_notice_empty_renders_nothing() -> None:
    console, buf = _captured_console()
    original = renderer.console
    try:
        renderer.console = console
        renderer.render_auto_propose_notice([])
        renderer.render_auto_propose_notice(None)
    finally:
        renderer.console = original

    assert buf.getvalue() == ""


def test_set_and_get_last_auto_propose_notice_roundtrip() -> None:
    items = _items(2)
    renderer.set_last_auto_propose_notice(items)
    try:
        assert renderer.get_last_auto_propose_notice() == items
    finally:
        renderer.set_last_auto_propose_notice(None)


def test_set_last_auto_propose_notice_clears_on_empty() -> None:
    renderer.set_last_auto_propose_notice(_items(1))
    renderer.set_last_auto_propose_notice([])
    assert renderer.get_last_auto_propose_notice() is None
    renderer.set_last_auto_propose_notice(None)


# ---------------------------------------------------------------------------
# Replay parity (#1454): the inline notice survives resume/reload alongside
# the attribution footer.  Drives the same `_restore_last_attribution_from`
# helper that every CLI resume path calls (--continue, /last, /resume,
# /fork, /rewind), with persisted message metadata that carries the
# `memory_auto_proposed` field the chat router and CLI both write.
# ---------------------------------------------------------------------------


def _stored_messages_with_auto_propose(items: list[dict[str, str]]) -> list[dict[str, object]]:
    """Build a stored-message list shaped like storage.list_messages() output.

    The most recent assistant message carries the `memory_auto_proposed`
    metadata field — the restore function should pick that up and seed
    the renderer cache.
    """
    return [
        {"role": "user", "metadata": None, "content": "hi"},
        {
            "role": "assistant",
            "metadata": {"memory_auto_proposed": items, "attribution": None},
            "content": "hello",
        },
    ]


def test_restore_from_assistant_metadata_seeds_cache() -> None:
    """Live-stream parity: after resume the cached notice matches what we'd
    have shown live for that turn."""
    from anteroom.cli.repl import _restore_last_attribution_from

    renderer.set_last_auto_propose_notice(None)
    items = _items(2)
    _restore_last_attribution_from(_stored_messages_with_auto_propose(items))
    try:
        assert renderer.get_last_auto_propose_notice() == items
    finally:
        renderer.set_last_auto_propose_notice(None)


def test_restore_clears_cache_when_metadata_absent() -> None:
    """No metadata on the last assistant turn → cache must be cleared.

    Stops a stale notice from a prior session leaking into the new resume.
    """
    from anteroom.cli.repl import _restore_last_attribution_from

    renderer.set_last_auto_propose_notice(_items(1))
    _restore_last_attribution_from(
        [
            {"role": "user", "metadata": None, "content": "hi"},
            {"role": "assistant", "metadata": None, "content": "hello"},
        ]
    )
    assert renderer.get_last_auto_propose_notice() is None


def test_restore_from_json_string_metadata() -> None:
    """The persisted ``metadata`` column comes back as a JSON string for some
    storage backends; restore must parse defensively and still seed the cache."""
    import json

    from anteroom.cli.repl import _restore_last_attribution_from

    items = _items(1)
    stored = [
        {
            "role": "assistant",
            "metadata": json.dumps({"memory_auto_proposed": items}),
            "content": "hello",
        }
    ]
    renderer.set_last_auto_propose_notice(None)
    _restore_last_attribution_from(stored)
    try:
        assert renderer.get_last_auto_propose_notice() == items
    finally:
        renderer.set_last_auto_propose_notice(None)


def test_restore_ignores_non_list_memory_auto_proposed() -> None:
    """Defensive: a malformed metadata value (e.g., dict instead of list) must
    leave the cache cleared — never crash, never render junk."""
    from anteroom.cli.repl import _restore_last_attribution_from

    renderer.set_last_auto_propose_notice(_items(1))
    _restore_last_attribution_from(
        [
            {
                "role": "assistant",
                "metadata": {"memory_auto_proposed": {"not": "a list"}},
                "content": "hello",
            }
        ]
    )
    assert renderer.get_last_auto_propose_notice() is None


def test_restore_with_empty_messages_clears_cache() -> None:
    """Brand-new conversation (no messages yet) → both caches reset cleanly."""
    from anteroom.cli.repl import _restore_last_attribution_from

    renderer.set_last_auto_propose_notice(_items(1))
    renderer.set_last_attribution({"turns": []})
    _restore_last_attribution_from([])
    assert renderer.get_last_auto_propose_notice() is None
    assert renderer.get_last_attribution() is None
