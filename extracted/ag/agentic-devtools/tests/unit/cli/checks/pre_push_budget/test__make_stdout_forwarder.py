"""Deadline-safe stdout forwarding."""

import io
import os
from unittest.mock import patch

from agentic_devtools.cli.checks import pre_push_budget


def test_text_stream_without_file_descriptor_uses_direct_forwarding():
    stream = io.StringIO()
    with patch.object(pre_push_budget.sys, "stdout", stream):
        forward, restore = pre_push_budget._make_stdout_forwarder()
        forward("complete output")
        restore()
    assert stream.getvalue() == "complete output"


def test_descriptor_forwarding_is_nonblocking_and_restores_mode():
    read_fd, write_fd = os.pipe()
    stream = os.fdopen(write_fd, "w", encoding="utf-8")
    try:
        with patch.object(pre_push_budget.sys, "stdout", stream):
            forward, restore = pre_push_budget._make_stdout_forwarder()
            assert not os.get_blocking(write_fd)
            forward("complete output")
            restore()
            assert os.get_blocking(write_fd)
        assert os.read(read_fd, 100) == b"complete output"
    finally:
        stream.close()
        os.close(read_fd)


def test_full_pipe_and_excess_output_disable_forwarding():
    read_fd, write_fd = os.pipe()
    stream = os.fdopen(write_fd, "w", encoding="utf-8")
    try:
        with patch.object(pre_push_budget.sys, "stdout", stream):
            forward, restore = pre_push_budget._make_stdout_forwarder()
            while True:
                try:
                    os.write(write_fd, b"x" * 4096)
                except BlockingIOError:
                    break
            forward("pending")
            forward("y" * pre_push_budget.MAX_PENDING_STDOUT_BYTES)
            forward("ignored")
            restore()
            assert os.get_blocking(write_fd)
    finally:
        stream.close()
        os.close(read_fd)
