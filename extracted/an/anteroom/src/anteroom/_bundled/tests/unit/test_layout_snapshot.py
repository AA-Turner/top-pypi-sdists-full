"""Snapshot coverage for CLI input toolbar fragments (#1369)."""

from __future__ import annotations

from anteroom.cli.layout import build_input_toolbar_fragments


class _ViState:
    def __init__(self, input_mode: str) -> None:
        self.input_mode = input_mode


class _App:
    def __init__(self, input_mode: str) -> None:
        self.vi_state = _ViState(input_mode)


class TestInputToolbarSnapshot:
    def test_idle_emacs_default_snapshot(self, snapshot) -> None:  # type: ignore[no-untyped-def]
        assert (
            build_input_toolbar_fragments(
                editing_mode="emacs",
                hint_context="idle",
                show_mode_badge=False,
            )
            == snapshot
        )

    def test_idle_emacs_with_mode_badge_snapshot(self, snapshot) -> None:  # type: ignore[no-untyped-def]
        assert (
            build_input_toolbar_fragments(
                editing_mode="emacs",
                hint_context="idle",
                show_mode_badge=True,
            )
            == snapshot
        )

    def test_vi_multiline_snapshot(self, snapshot) -> None:  # type: ignore[no-untyped-def]
        assert (
            build_input_toolbar_fragments(
                editing_mode="vi",
                app=_App("InputMode.NAVIGATION"),
                hint_context="multiline",
                paste_line_count=9,
            )
            == snapshot
        )
