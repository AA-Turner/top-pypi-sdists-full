"""Which terminals get the agents' logos, and the escapes that draw them.

A wrong guess here is not cosmetic: an image escape a terminal does not parse
prints its payload as text across the menu, and a reply it does send arrives
on stdin as keystrokes. So detection reads only the environment, never asks the
terminal, and anything unrecognised gets the agents' names.
"""

from __future__ import annotations

import pytest

from probe.cli import tui
from probe.cli.tui import ImageProtocol

_TERMINAL_ENV = ("TERM", "TERM_PROGRAM", "KITTY_WINDOW_ID", "TMUX", "STY", tui.ICONS_ENV)


@pytest.fixture
def terminal(monkeypatch):
    for name in _TERMINAL_ENV:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(tui.sys.stdout, "isatty", lambda: True, raising=False)

    def set_env(**env):
        for name, value in env.items():
            monkeypatch.setenv(name, value)
        return tui.image_protocol()

    return set_env


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({"TERM_PROGRAM": "WarpTerminal"}, ImageProtocol.KITTY),
        ({"TERM_PROGRAM": "ghostty"}, ImageProtocol.KITTY),
        ({"TERM": "xterm-kitty"}, ImageProtocol.KITTY),
        ({"TERM_PROGRAM": "WezTerm"}, ImageProtocol.KITTY),
        ({"TERM_PROGRAM": "iTerm.app"}, ImageProtocol.ITERM),
        ({"TERM_PROGRAM": "Apple_Terminal"}, None),
        ({"TERM_PROGRAM": "vscode"}, None),
        # A multiplexer swallows the escapes, whatever terminal is outside it.
        ({"TERM_PROGRAM": "WarpTerminal", "TMUX": "/tmp/tmux-1/default,1,0"}, None),
        ({"TERM": "screen-256color", "TERM_PROGRAM": "iTerm.app"}, None),
        ({"TERM_PROGRAM": "WarpTerminal", tui.ICONS_ENV: "off"}, None),
        ({tui.ICONS_ENV: "kitty"}, ImageProtocol.KITTY),
    ],
)
def test_the_terminal_decides_logos_or_names(terminal, env, expected):
    assert terminal(**env) is expected


def test_output_that_is_not_a_terminal_gets_names(terminal, monkeypatch):
    monkeypatch.setattr(tui.sys.stdout, "isatty", lambda: False, raising=False)
    assert terminal(TERM_PROGRAM="WarpTerminal") is None


def test_a_large_logo_is_sent_in_kitty_chunks_with_replies_off():
    escape = tui.image_escape(b"x" * 9000, ImageProtocol.KITTY, cells=2, image_id=7)
    chunks = escape.split("\x1b_G")[1:]
    assert len(chunks) == 3  # 12000 base64 characters, 4096 at most per chunk
    assert chunks[0].startswith("a=T,f=100,t=d,i=7,p=1,c=2,r=1,C=1,q=2,m=1;")
    assert [chunk.split(";", 1)[0] for chunk in chunks[1:]] == ["m=1", "m=0"]
    assert tui.forget_images(ImageProtocol.KITTY, 2).count("a=d,d=I") == 2
    assert tui.forget_images(ImageProtocol.ITERM, 2) == ""
