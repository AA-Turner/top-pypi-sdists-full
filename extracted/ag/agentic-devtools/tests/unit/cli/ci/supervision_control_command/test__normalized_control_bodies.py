"""Tests for _normalized_control_bodies."""

import pytest

from agentic_devtools.cli.ci.supervision_control import CONTROL_MARKER
from agentic_devtools.cli.ci.supervision_control_command import _normalized_control_bodies


def test_rejects_malformed_terminal_label_on_protocol_state() -> None:
    with pytest.raises(ValueError, match="malformed terminal label"):
        _normalized_control_bodies([f"{CONTROL_MARKER}\n{{}}\n🤖 AI PR Loop ·"])


def test_skips_malformed_terminal_label_without_protocol_state() -> None:
    assert _normalized_control_bodies(["ordinary text\n🤖 AI PR Loop ·"]) == []
