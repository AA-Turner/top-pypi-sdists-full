"""The CLI's one output policy: compact on a pipe, projected on request.

`_print_json` is the single door every read command's output leaves through
(~106 call sites), so its behavior IS the CLI's output contract. Two properties
are pinned here:

  * Whitespace is the only thing that varies by destination. A terminal gets
    indent=2; a pipe gets compact separators — measured at ~19% of a
    `project list` in an agent's context window. Keys and values are identical
    either way, so redirecting to a file can never change what a script parses.

  * `--fields` is a projection, not a filter that can silently miss. An unknown
    field errors loudly and names what the read actually carries: `--fields
    slgu` answering `{}` would read as "the run has no slug", a claim the
    projection has no right to make. (This is the deterministic-gate side of
    field selection — authored once into a script, mistake visible immediately —
    which is why it lives on the CLI and NOT as an MCP query language, where a
    model would re-derive the selection on every call.)
"""

from __future__ import annotations

import json

import pytest
import typer

from probe.cli.main import _print_json, _select_fields


def test_piped_output_is_compact_and_terminal_output_is_pretty(monkeypatch, capsys):
    import sys

    payload = {"slug": "wise-urchin-649", "config": {"kl": 0.04}, "note": "ünïcode"}

    monkeypatch.setattr(sys.stdout, "isatty", lambda: False, raising=False)
    _print_json(payload)
    piped = capsys.readouterr().out
    assert piped == json.dumps(payload, separators=(",", ":"), ensure_ascii=False) + "\n"
    # No \uXXXX escaping: UTF-8 passes through at one byte-cost, not six.
    assert "ünïcode" in piped

    monkeypatch.setattr(sys.stdout, "isatty", lambda: True, raising=False)
    _print_json(payload)
    pretty = capsys.readouterr().out
    assert "  \"slug\"" in pretty
    # Same data both ways — layout is the entire difference.
    assert json.loads(piped) == json.loads(pretty)


def test_select_fields_projects_a_single_object():
    row = {"id": "x", "slug": "wise-urchin-649", "status": "completed", "config": {}}
    assert _select_fields(row, "slug,status") == {
        "slug": "wise-urchin-649",
        "status": "completed",
    }
    # No selection: the object passes through untouched.
    assert _select_fields(row, None) is row


def test_select_fields_projects_page_items_and_keeps_the_cursor():
    page = {
        "items": [
            {"id": "1", "slug": "a", "status": "running"},
            {"id": "2", "slug": "b", "status": "failed"},
        ],
        "next_cursor": "opaque",
    }
    out = _select_fields(page, "slug")
    assert out == {"items": [{"slug": "a"}, {"slug": "b"}], "next_cursor": "opaque"}


def test_display_control_characters_stay_escaped_in_both_modes(monkeypatch, capsys):
    """The third pinned property: C1 controls and bidi overrides — the
    display-manipulation characters ensure_ascii=True used to neutralize for
    free — stay backslash-u-escaped in BOTH modes, while ordinary non-ASCII text
    passes raw (that's the token win). A 'simplify _print_json' edit that
    drops _DISPLAY_CONTROLS must fail here."""
    import sys

    payload = {"name": "ok\u202etxt.exe", "csi": "a\u009bb", "cjk": "研究"}
    for tty in (False, True):
        monkeypatch.setattr(sys.stdout, "isatty", lambda t=tty: t, raising=False)
        _print_json(payload)
        out = capsys.readouterr().out
        assert "\\u202e" in out and "\u202e" not in out
        assert "\\u009b" in out
        assert "研究" in out  # ordinary non-ASCII stays raw
        assert json.loads(out) == payload  # escapes are valid JSON


def test_select_fields_rejects_an_empty_projection():
    """`--fields ","` names nothing; projecting to nothing would print {}
    per row — the silent-empty answer the helper exists to forbid."""
    with pytest.raises(typer.BadParameter):
        _select_fields({"slug": "a"}, " , ")


def test_select_fields_rejects_unknown_fields_loudly():
    with pytest.raises(typer.BadParameter) as err:
        _select_fields({"slug": "a", "status": "running"}, "slgu")
    # The error must name what IS there, so the fix is one glance away.
    assert "slgu" in str(err.value)
    assert "slug" in str(err.value)
