"""Doctor copying must preserve the whole report and reach the user's clipboard."""

import base64
import subprocess

import pytest
from prompt_toolkit.output import DummyOutput

from probe.cli import tui

# Every test here drives a prompt_toolkit app session and asserts on the frames
# it rendered. That is a finished-render measurement, so it belongs in the serial
# lane with the pty tests -- see the `tui` marker in agent/pyproject.toml.
pytestmark = pytest.mark.tui


class ClipboardOutput(DummyOutput):
    def __init__(self):
        self.raw = ""

    def write_raw(self, data):
        self.raw += data


@pytest.fixture(autouse=True)
def isolated_clipboard(monkeypatch):
    for name in ("SSH_CONNECTION", "SSH_TTY", "WAYLAND_DISPLAY", "DISPLAY"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(tui, "interactive", lambda: True)
    monkeypatch.setattr(tui.shutil, "which", lambda _name: None)


@pytest.mark.parametrize(
    "platform,display,command,encoding",
    [
        ("darwin", None, ["pbcopy"], "utf-8"),
        ("win32", None, ["clip.exe"], "utf-16le"),
        ("linux", "WAYLAND_DISPLAY", ["wl-copy"], "utf-8"),
        ("linux", "DISPLAY", ["xclip", "-selection", "clipboard"], "utf-8"),
        ("linux", "DISPLAY", ["xsel", "--clipboard", "--input"], "utf-8"),
    ],
)
def test_native_clipboard_preserves_unicode_and_does_not_use_a_shell(
    monkeypatch, platform, display, command, encoding
):
    monkeypatch.setattr(tui.sys, "platform", platform)
    if display:
        monkeypatch.setenv(display, "test-display")
    monkeypatch.setattr(tui.shutil, "which", lambda name: name if name == command[0] else None)
    text = "Probe doctor\n  Path  /home/研究\n  Status  ✔\n$(do-not-execute)"
    calls = []
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kwargs: calls.append((cmd, kwargs)))
    output = ClipboardOutput()
    assert "copied" in tui._copy_to_clipboard(text, output)
    cmd, kwargs = calls[0]
    assert cmd == command
    assert kwargs["input"].decode(encoding) == text
    assert not kwargs.get("shell")
    assert output.raw == ""


@pytest.mark.parametrize("ssh_variable", ["SSH_CONNECTION", "SSH_TTY"])
def test_ssh_sends_full_report_to_terminal_instead_of_remote_desktop(monkeypatch, ssh_variable):
    monkeypatch.setenv(ssh_variable, "test-ssh")
    monkeypatch.setenv("DISPLAY", ":0")
    monkeypatch.setattr(tui.shutil, "which", lambda name: name)
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_k: pytest.fail("remote clipboard"))
    text = "Full doctor report ✔\n" * 1000
    output = ClipboardOutput()
    assert "sent to terminal" in tui._copy_to_clipboard(text, output)
    assert output.raw.startswith("\033]52;c;") and output.raw.endswith("\a")
    assert base64.b64decode(output.raw[7:-1]).decode() == text


@pytest.mark.parametrize("failure", [OSError(), subprocess.TimeoutExpired("pbcopy", 2)])
def test_failed_clipboard_command_falls_back_to_terminal(monkeypatch, failure):
    monkeypatch.setattr(tui.sys, "platform", "darwin")
    monkeypatch.setattr(tui.shutil, "which", lambda name: name)

    def fail(*args, **kwargs):
        raise failure

    monkeypatch.setattr(subprocess, "run", fail)
    output = ClipboardOutput()
    assert "sent to terminal" in tui._copy_to_clipboard("report", output)
    assert output.raw.startswith("\033]52;c;")


def test_copyable_page_is_plain_text_when_piped(monkeypatch, capsys):
    monkeypatch.setattr(tui, "interactive", lambda: False)
    monkeypatch.setattr(tui, "_copy_prompt", lambda *_: pytest.fail("interactive prompt in pipe"))
    text = "Probe doctor\n" + "long path " * 100
    assert tui.page([text], prompt="Enter to return", copyable=True) == ""
    assert capsys.readouterr().out == text + "\n"


def test_unavailable_clipboard_has_actionable_feedback(monkeypatch):
    monkeypatch.setenv("TERM", "dumb")
    output = ClipboardOutput()
    message = tui._copy_to_clipboard("report", output)
    assert "Could not copy" in message and "probe doctor" in message
    assert output.raw == ""
