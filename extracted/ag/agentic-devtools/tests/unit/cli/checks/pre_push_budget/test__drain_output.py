"""Bounded draining and decoder finalization after process-group cleanup."""

import codecs
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.checks import pre_push_budget


@pytest.mark.parametrize("terminal", [b"", BlockingIOError()])
def test_buffered_output_and_partial_characters_are_preserved(terminal, monkeypatch):
    reader = Mock(side_effect=[b"shutdown\xe2\x82", b"\xacpartial\xf0", terminal])
    set_blocking = Mock()
    monkeypatch.setattr(pre_push_budget.os, "read", reader)
    monkeypatch.setattr(pre_push_budget.os, "set_blocking", set_blocking)
    monkeypatch.setattr(pre_push_budget.time, "monotonic", lambda: 0)
    output = []
    pre_push_budget._drain_output(42, codecs.getincrementaldecoder("utf-8")(errors="replace"), output.append)
    assert "".join(output) == "shutdown\u20acpartial\ufffd"
    assert reader.call_count == 3
    set_blocking.assert_called_once_with(42, False)


def test_continuous_output_stops_at_deadline(monkeypatch):
    reader = Mock(return_value=b"buffered output\xe2")
    ticks = iter([0, 0, 2])
    monkeypatch.setattr(pre_push_budget.os, "read", reader)
    monkeypatch.setattr(pre_push_budget.os, "set_blocking", Mock())
    monkeypatch.setattr(pre_push_budget.time, "monotonic", lambda: next(ticks, 2))
    output = []
    pre_push_budget._drain_output(42, codecs.getincrementaldecoder("utf-8")(errors="replace"), output.append)
    reader.assert_called_once_with(42, 4096)
    assert "".join(output) == "buffered output\ufffd"


@pytest.mark.parametrize("failure", ["set_blocking", "read", "emit"])
def test_drain_errors_propagate(failure, monkeypatch):
    reader = Mock(return_value=b"diagnostics")
    set_blocking = Mock()
    emit = Mock()
    {"set_blocking": set_blocking, "read": reader, "emit": emit}[failure].side_effect = OSError("drain failed")
    monkeypatch.setattr(pre_push_budget.os, "read", reader)
    monkeypatch.setattr(pre_push_budget.os, "set_blocking", set_blocking)
    with pytest.raises(OSError, match="drain failed"):
        pre_push_budget._drain_output(42, codecs.getincrementaldecoder("utf-8")(errors="replace"), emit)
