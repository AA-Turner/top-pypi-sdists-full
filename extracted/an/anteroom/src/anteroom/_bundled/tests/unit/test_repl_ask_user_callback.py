"""Unit tests for the CLI ask_user callback plumbing (#1437).

Covers the extracted module-level helpers — ``_strip_option_prefix``,
``_resolve_ask_choice``, and the factory ``_make_ask_user_callback`` — so
the CLI cancel semantics (``x`` / Ctrl-D / Ctrl-C distinguished from empty
Enter) are locked in without booting the full REPL.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from anteroom.cli.repl import (
    _CHOICE_CANCEL_SENTINEL,
    _make_ask_user_callback,
    _resolve_ask_choice,
    _strip_option_prefix,
)


class TestStripOptionPrefix:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("A. Test", "Test"),
            ("B) Another", "Another"),
            ("1. Foo", "Foo"),
            ("1) Foo", "Foo"),
            ("12. Bar", "Bar"),
            ("  A.  Indented  ", "Indented  "),
            ("plain", "plain"),
            # Prefix must be followed by whitespace — "A.B" has no space
            # after the dot, so no stripping.
            ("A.B. Nested", "A.B. Nested"),
        ],
    )
    def test_strips_common_prefixes(self, raw: str, expected: str) -> None:
        assert _strip_option_prefix(raw) == expected

    def test_empty_after_strip_falls_back_to_original(self) -> None:
        assert _strip_option_prefix("A.") == "A."
        assert _strip_option_prefix("1) ") == "1) "

    def test_preserves_labels_with_no_prefix(self) -> None:
        assert _strip_option_prefix("Xenon") == "Xenon"
        assert _strip_option_prefix("choice one") == "choice one"


class TestResolveAskChoice:
    def test_typed_x_returns_cancel_sentinel(self) -> None:
        assert _resolve_ask_choice("x", ["Foo", "Bar"]) == _CHOICE_CANCEL_SENTINEL

    def test_typed_uppercase_x_returns_cancel_sentinel(self) -> None:
        assert _resolve_ask_choice("X", ["Foo", "Bar"]) == _CHOICE_CANCEL_SENTINEL

    def test_typed_x_with_whitespace_returns_cancel_sentinel(self) -> None:
        assert _resolve_ask_choice("  x  ", ["Foo", "Bar"]) == _CHOICE_CANCEL_SENTINEL

    def test_x_short_circuits_even_with_x_option(self) -> None:
        """Typing 'x' always cancels, even when an option starts with 'x'."""
        assert _resolve_ask_choice("x", ["Xenon", "Other"]) == _CHOICE_CANCEL_SENTINEL

    def test_digit_resolves_to_option_by_index(self) -> None:
        assert _resolve_ask_choice("1", ["Alpha", "Beta"]) == "Alpha"
        assert _resolve_ask_choice("2", ["Alpha", "Beta"]) == "Beta"

    def test_digit_returns_original_label_with_prefix(self) -> None:
        """Digit selection returns the ORIGINAL option string, not stripped."""
        assert _resolve_ask_choice("1", ["A. Alpha", "B. Beta"], stripped_opts=["Alpha", "Beta"]) == "A. Alpha"
        assert _resolve_ask_choice("2", ["A. Alpha", "B. Beta"], stripped_opts=["Alpha", "Beta"]) == "B. Beta"

    def test_stripped_text_match_returns_original_label(self) -> None:
        """Text match via stripped form still returns the original label."""
        assert _resolve_ask_choice("Alpha", ["A. Alpha", "B. Beta"], stripped_opts=["Alpha", "Beta"]) == "A. Alpha"

    def test_distinct_prefixed_options_dont_collapse(self) -> None:
        """Options with different prefixes but same stripped label stay distinct.

        Regression for the senior-review parity bug: previously the CLI
        returned the stripped label, so ``"A. Alpha"`` and ``"A) Alpha"``
        would both resolve to ``"Alpha"``. After the fix, digit selection
        (the only unambiguous path) returns the original string.
        """
        opts = ["A. Alpha", "A) Alpha"]
        stripped = ["Alpha", "Alpha"]
        assert _resolve_ask_choice("1", opts, stripped_opts=stripped) == "A. Alpha"
        assert _resolve_ask_choice("2", opts, stripped_opts=stripped) == "A) Alpha"

    def test_out_of_range_digit_falls_back_to_freeform(self) -> None:
        assert _resolve_ask_choice("99", ["Alpha", "Beta"]) == "99"

    def test_unique_prefix_match_resolves(self) -> None:
        assert _resolve_ask_choice("Te", ["Test", "Other"]) == "Test"

    def test_ambiguous_prefix_falls_back_to_freeform(self) -> None:
        # "T" matches both "Test" and "Terminal" — no unique match.
        assert _resolve_ask_choice("T", ["Test", "Terminal"]) == "T"

    def test_freeform_when_no_options(self) -> None:
        assert _resolve_ask_choice("anything", None) == "anything"
        assert _resolve_ask_choice("", None) == ""

    def test_empty_answer_stays_empty_with_options(self) -> None:
        # Empty Enter is a real answer, not a cancel — preserved as "".
        assert _resolve_ask_choice("", ["Alpha"]) == ""

    def test_multiline_answer_stays_freeform_without_options(self) -> None:
        assert _resolve_ask_choice("first line\nsecond line", None) == "first line\nsecond line"

    def test_multiline_answer_with_options_stays_freeform(self) -> None:
        answer = "Alpha\nwith more detail"
        assert _resolve_ask_choice(answer, ["Alpha", "Beta"]) == answer

    def test_x_inside_multiline_answer_does_not_cancel(self) -> None:
        answer = "x\nmore detail"
        assert _resolve_ask_choice(answer, ["Alpha", "Beta"]) == answer


class TestMakeAskUserCallback:
    def _build(
        self,
        *,
        prompt_return: str | None,
        cancel_ref: list[Any] | None = None,
    ) -> tuple[Any, list[Any], list[str]]:
        """Helper: build a callback with a mock prompt.

        Returns (callback, cancel_ref, printed_lines).
        """
        if cancel_ref is None:
            cancel_ref = [asyncio.Event()]
        printed: list[str] = []

        async def _fake_prompt(_text: str) -> str | None:
            return prompt_return

        callback = _make_ask_user_callback(
            sub_prompt_async=_fake_prompt,
            cancel_event_ref=cancel_ref,
            console_print=printed.append,
        )
        return callback, cancel_ref, printed

    @pytest.mark.asyncio
    async def test_typed_x_sets_cancel_event_and_returns_none(self) -> None:
        callback, cancel_ref, _ = self._build(prompt_return="x")
        result = await callback("Which DB?", ["Postgres", "MySQL"])
        assert result is None
        assert cancel_ref[0].is_set()

    @pytest.mark.asyncio
    async def test_typed_uppercase_x_cancels(self) -> None:
        callback, cancel_ref, _ = self._build(prompt_return="X")
        result = await callback("Which DB?", None)
        assert result is None
        assert cancel_ref[0].is_set()

    @pytest.mark.asyncio
    async def test_ctrl_d_returns_none_and_sets_cancel(self) -> None:
        """_sub_prompt_async returns None on Ctrl-D / Ctrl-C."""
        callback, cancel_ref, _ = self._build(prompt_return=None)
        result = await callback("Which DB?", None)
        assert result is None
        assert cancel_ref[0].is_set()

    @pytest.mark.asyncio
    async def test_empty_enter_returns_empty_without_cancel(self) -> None:
        callback, cancel_ref, _ = self._build(prompt_return="")
        result = await callback("Anything?", None)
        assert result == ""
        assert not cancel_ref[0].is_set()

    @pytest.mark.asyncio
    async def test_digit_resolves_to_first_option(self) -> None:
        callback, cancel_ref, _ = self._build(prompt_return="1")
        result = await callback("Pick:", ["Alpha", "Beta"])
        assert result == "Alpha"
        assert not cancel_ref[0].is_set()

    @pytest.mark.asyncio
    async def test_multiline_freeform_answer_with_options_is_preserved(self) -> None:
        answer = "Alpha\nbecause the default needs context"
        callback, cancel_ref, _ = self._build(prompt_return=answer)
        result = await callback("Pick:", ["Alpha", "Beta"])
        assert result == answer
        assert not cancel_ref[0].is_set()

    @pytest.mark.asyncio
    async def test_cli_web_parity_for_prefixed_options(self) -> None:
        """CLI and web must return the same value for the same prefixed options.

        Web: button click posts the original option text (e.g. ``"A. Alpha"``).
        CLI: typing ``1`` or ``Alpha`` must also return ``"A. Alpha"`` — not
        the stripped ``"Alpha"`` — so the tool-level answer is identical.
        """
        opts = ["A. Alpha", "B. Beta"]
        # Digit path
        cb1, _, _ = self._build(prompt_return="1")
        assert await cb1("Pick:", opts) == "A. Alpha"
        # Stripped text path
        cb2, _, _ = self._build(prompt_return="Alpha")
        assert await cb2("Pick:", opts) == "A. Alpha"
        # Full text path (typing the original label)
        cb3, _, _ = self._build(prompt_return="A. Alpha")
        assert await cb3("Pick:", opts) == "A. Alpha"

    @pytest.mark.asyncio
    async def test_text_matches_stripped_option(self) -> None:
        """Typing 'Test' matches the stripped form of 'A. Test' and returns the ORIGINAL."""
        callback, cancel_ref, _ = self._build(prompt_return="Test")
        result = await callback("Pick:", ["A. Test", "B. Other"])
        # Matching uses the stripped label ("Test" startswith stripped
        # first option), but the returned value is the original string
        # so the tool output matches what the web UI sends for the same
        # prefixed option.
        assert result == "A. Test"
        assert not cancel_ref[0].is_set()

    @pytest.mark.asyncio
    async def test_digit_returns_original_prefixed_label(self) -> None:
        """Digit selection returns the ORIGINAL option string with its prefix intact.

        Regression for CLI/web parity: a click on the 'A. Test' button in
        the web UI sends 'A. Test' to the backend; typing '1' in the CLI
        must produce the same tool-level result.
        """
        callback, _, _ = self._build(prompt_return="1")
        result = await callback("Pick:", ["A. Test", "B. Other"])
        assert result == "A. Test"

    @pytest.mark.asyncio
    async def test_x_cancels_even_with_xenon_option(self) -> None:
        callback, cancel_ref, _ = self._build(prompt_return="x")
        result = await callback("Pick:", ["Xenon", "Other"])
        assert result is None
        assert cancel_ref[0].is_set()

    @pytest.mark.asyncio
    async def test_no_cancel_event_ref_tolerated(self) -> None:
        """Callback works when the cancel-event ref holds None."""
        callback, cancel_ref, _ = self._build(
            prompt_return="x",
            cancel_ref=[None],
        )
        result = await callback("Question?", None)
        assert result is None
        assert cancel_ref[0] is None

    @pytest.mark.asyncio
    async def test_before_prompt_hook_runs(self) -> None:
        called: list[bool] = []

        async def _hook() -> None:
            called.append(True)

        async def _fake_prompt(_text: str) -> str | None:
            return "ok"

        callback = _make_ask_user_callback(
            sub_prompt_async=_fake_prompt,
            cancel_event_ref=[None],
            before_prompt=_hook,
            console_print=lambda _msg: None,
        )
        result = await callback("Q?", None)
        assert result == "ok"
        assert called == [True]

    @pytest.mark.asyncio
    async def test_strips_option_prefixes_in_rendered_list(self) -> None:
        callback, _, printed = self._build(prompt_return="1")
        await callback("Pick:", ["A. Alpha", "B. Beta"])
        # Isolate the list-rendering lines ("1. Alpha", "2. Beta") —
        # excludes the post-selection "→ A. Alpha" echo, which legitimately
        # contains the original label because the callback returns the
        # original string (CLI/web parity).
        list_lines = [line for line in printed if "[/#8b8b8b]" in line and "→" not in line]
        rendered_list = "\n".join(list_lines)
        # Stripped labels appear in the displayed list.
        assert "Alpha" in rendered_list
        assert "Beta" in rendered_list
        # The "A." and "B." prefixes are stripped from the displayed list
        # so the CLI's own "1./2." index doesn't double up with the
        # model-supplied enumeration.
        assert "A. Alpha" not in rendered_list
        assert "B. Beta" not in rendered_list

    @pytest.mark.asyncio
    async def test_cancel_prints_cancelled_marker(self) -> None:
        callback, _, printed = self._build(prompt_return="x")
        await callback("Q?", None)
        assert any("(cancelled)" in line for line in printed)

    @pytest.mark.asyncio
    async def test_empty_answer_renders_empty_marker(self) -> None:
        callback, _, printed = self._build(prompt_return="")
        await callback("Q?", None)
        # The echo line for empty should show "(empty)" rather than the
        # (invisible) empty string.
        assert any("(empty)" in line for line in printed)

    @pytest.mark.asyncio
    async def test_inline_help_exposes_multiline_and_cancel_controls(self) -> None:
        callback, _, printed = self._build(prompt_return="ok")
        await callback("Q?", ["Alpha", "Beta"])
        rendered = "\n".join(printed)
        assert "Enter submits" in rendered
        assert "Shift+Enter adds a newline" in rendered
        assert "Ctrl+J or Esc+Enter adds a newline" in rendered
        assert "'x', Ctrl-D, or Ctrl-C cancels" in rendered
