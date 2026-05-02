"""
Tests for subprocess_multitee module.

Run with: pytest test_subprocess.py -v
"""

import io
import os
import subprocess as stdlib_subprocess
import sys
import tempfile

import pytest

import subprocess_multitee as sm
from subprocess_multitee import (
    DEVNULL,
    PIPE,
    STDOUT,
    Popen,
    call,
    check_call,
    check_output,
    run,
    tee,
)


class TestTeeBasic:
    """Basic tee() functionality tests."""

    def test_tee_single_pipe(self):
        """tee with single PIPE destination."""
        t = tee(PIPE)
        assert hasattr(t, "fileno")
        assert hasattr(t, "pipes")
        assert len(t.pipes) == 1
        t.close()

    def test_tee_multiple_pipes(self):
        """tee with multiple PIPE destinations."""
        t = tee(PIPE, PIPE, PIPE)
        assert len(t.pipes) == 3
        t.close()

    def test_tee_with_file_object(self):
        """tee with a file object destination."""
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            fname = f.name
            t = tee(PIPE, f)
            assert len(t.pipes) == 1
        t.close()
        os.unlink(fname)

    def test_tee_with_devnull(self):
        """tee with DEVNULL skips it efficiently."""
        t = tee(DEVNULL, PIPE)
        # DEVNULL should be skipped, only PIPE added
        assert len(t.pipes) == 1
        t.close()

    def test_tee_stdout_not_supported(self):
        """tee raises ValueError for subprocess.STDOUT."""
        with pytest.raises(ValueError, match="STDOUT"):
            tee(STDOUT)

    def test_tee_unsupported_type(self):
        """tee raises TypeError for unsupported types."""
        with pytest.raises(TypeError, match="Unsupported"):
            tee(12345, "not a file")

    def test_tee_context_manager(self):
        """tee works as context manager."""
        with tee(PIPE) as t:
            # Threads should be alive and write fd should be open while context is active
            assert t._reader_thread.is_alive() and t._writer_thread.is_alive()
            assert t._write_fd != -1
        # After exit, write fd should be closed
        assert t._write_fd == -1


class TestTeeWithStdlibPopen:
    """Test tee() with stdlib subprocess.Popen."""

    def test_tee_with_stdlib_popen(self):
        """tee works with stdlib Popen (manual close required)."""
        t = tee(PIPE)
        proc = stdlib_subprocess.Popen(["echo", "hello"], stdout=t)
        proc.wait()
        t.close()  # Must close manually with stdlib Popen
        output = t.pipes[0].read()
        assert output == b"hello\n"

    def test_tee_to_file_with_stdlib_popen(self):
        """tee to file with stdlib Popen."""
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as f:
            fname = f.name
            t = tee(f, PIPE)
            proc = stdlib_subprocess.Popen(["echo", "logged"], stdout=t)
            proc.wait()
            t.close()
            captured = t.pipes[0].read()

        with open(fname, "rb") as f:
            from_file = f.read()

        os.unlink(fname)
        assert captured == b"logged\n"
        assert from_file == b"logged\n"


class TestPopenSubclass:
    """Test the Popen subclass with tee integration."""

    def test_popen_with_tee_pipe(self):
        """Popen exposes tee PIPE as stdout."""
        proc = Popen(["echo", "hello"], stdout=tee(PIPE))
        output = proc.stdout.read()
        proc.wait()
        assert output == b"hello\n"

    def test_popen_with_tee_auto_closes_write_fd(self):
        """Popen automatically closes parent's write fd."""
        t = tee(PIPE)
        proc = Popen(["echo", "test"], stdout=t)
        # Write fd should be closed by Popen
        assert t._write_fd == -1
        proc.stdout.read()
        proc.wait()

    def test_popen_context_manager_joins_threads(self):
        """Popen context manager joins tee threads."""
        with Popen(["echo", "ctx"], stdout=tee(PIPE)) as proc:
            output = proc.stdout.read()
        # Thread should be joined after context exit
        assert output == b"ctx\n"

    def test_popen_text_mode(self):
        """Popen text mode works with tee."""
        proc = Popen(["echo", "text"], stdout=tee(PIPE), text=True)
        output = proc.stdout.read()
        proc.wait()
        assert output == "text\n"
        assert isinstance(output, str)

    def test_popen_encoding(self):
        """Popen with explicit encoding."""
        proc = Popen(["echo", "encoded"], stdout=tee(PIPE), encoding="utf-8")
        output = proc.stdout.read()
        proc.wait()
        assert output == "encoded\n"

    def test_popen_stdout_and_stderr(self):
        """Popen with both stdout and stderr tee'd."""
        proc = Popen(
            ["sh", "-c", "echo out; echo err >&2"], stdout=tee(PIPE), stderr=tee(PIPE)
        )
        stdout = proc.stdout.read()
        stderr = proc.stderr.read()
        proc.wait()
        assert stdout == b"out\n"
        assert stderr == b"err\n"

    def test_popen_communicate(self):
        """Popen.communicate() works with tee."""
        proc = Popen(["cat"], stdin=PIPE, stdout=tee(PIPE))
        stdout, stderr = proc.communicate(input=b"hello\n")
        assert stdout == b"hello\n"
        assert stderr is None

    def test_popen_communicate_text_mode(self):
        """Popen.communicate() in text mode with tee."""
        proc = Popen(["cat"], stdin=PIPE, stdout=tee(PIPE), text=True)
        stdout, stderr = proc.communicate(input="hello\n")
        assert stdout == "hello\n"

    def test_popen_positional_args(self):
        """Popen handles stdout as positional argument."""
        # Popen(args, bufsize, executable, stdin, stdout, ...)
        proc = Popen(["echo", "positional"], -1, None, None, tee(PIPE))
        output = proc.stdout.read()
        proc.wait()
        assert output == b"positional\n"

    def test_popen_without_tee(self):
        """Popen works normally without tee."""
        proc = Popen(["echo", "normal"], stdout=PIPE)
        output = proc.stdout.read()
        proc.wait()
        assert output == b"normal\n"


class TestTeeToTextModeFiles:
    """Test tee with text-mode file objects like sys.stdout."""

    def test_tee_to_stringio_buffer(self):
        """tee handles file objects with .buffer attribute."""
        # Create a text-mode wrapper around a BytesIO
        binary_buf = io.BytesIO()

        # Simulate a text-mode file with .buffer
        class TextWrapper:
            def __init__(self, buf):
                self.buffer = buf

            def write(self, s):
                pass

        wrapper = TextWrapper(binary_buf)
        t = tee(wrapper, PIPE)

        proc = Popen(["echo", "buffered"], stdout=t)
        captured = proc.stdout.read()
        proc.wait()

        binary_buf.seek(0)
        from_buffer = binary_buf.read()

        assert captured == b"buffered\n"
        assert from_buffer == b"buffered\n"

    def test_tee_to_real_stdout(self, capsys):
        """tee to sys.stdout captures and prints."""
        proc = Popen(["echo", "to stdout"], stdout=tee(PIPE, sys.stdout))
        captured = proc.stdout.read()
        proc.wait()

        out, _ = capsys.readouterr()
        assert captured == b"to stdout\n"
        assert "to stdout" in out


class TestTeeToFileDescriptors:
    """Test tee with raw file descriptors."""

    def test_tee_to_raw_fd(self):
        """tee to raw file descriptor."""
        r, w = os.pipe()
        t = tee(w, PIPE)

        proc = Popen(["echo", "raw fd"], stdout=t)
        captured = proc.stdout.read()
        proc.wait()

        os.close(w)  # Close write end so read doesn't block
        from_fd = os.read(r, 1024)
        os.close(r)

        assert captured == b"raw fd\n"
        assert from_fd == b"raw fd\n"


class TestRunHelper:
    """Test the run() helper function."""

    def test_run_basic(self):
        """run() works without tee."""
        result = run(["echo", "hello"], capture_output=True)
        assert result.stdout == b"hello\n"
        assert result.returncode == 0

    def test_run_with_tee(self):
        """run() works with tee."""
        result = run(["echo", "tee run"], stdout=tee(PIPE))
        assert result.stdout == b"tee run\n"

    def test_run_check_raises(self):
        """run() with check=True raises on non-zero exit."""
        with pytest.raises(stdlib_subprocess.CalledProcessError):
            run(["false"], check=True)

    def test_run_input(self):
        """run() with input parameter."""
        result = run(["cat"], input=b"input data", stdout=PIPE)
        assert result.stdout == b"input data"


class TestCallHelpers:
    """Test call(), check_call(), check_output() helpers."""

    def test_call_returns_code(self):
        """call() returns exit code."""
        assert call(["true"]) == 0
        assert call(["false"]) == 1

    def test_check_call_success(self):
        """check_call() returns 0 on success."""
        assert check_call(["true"]) == 0

    def test_check_call_raises(self):
        """check_call() raises on non-zero exit."""
        with pytest.raises(stdlib_subprocess.CalledProcessError):
            check_call(["false"])

    def test_check_output_captures(self):
        """check_output() captures stdout."""
        output = check_output(["echo", "captured"])
        assert output == b"captured\n"

    def test_check_output_raises(self):
        """check_output() raises on non-zero exit."""
        with pytest.raises(stdlib_subprocess.CalledProcessError):
            check_output(["false"])


class TestThreadBehavior:
    """Test thread management and cleanup."""

    def test_thread_is_daemon(self):
        """Tee threads are daemon threads."""
        t = tee(PIPE)
        assert t._reader_thread.daemon
        assert t._writer_thread.daemon
        t.close()

    def test_thread_has_name(self):
        """Tee threads have descriptive names."""
        t = tee(PIPE)
        assert "subprocess_multitee" in t._reader_thread.name
        assert "subprocess_multitee" in t._writer_thread.name
        t.close()

    def test_thread_exits_on_close(self):
        """Tee threads exit when write fd is closed."""
        t = tee(PIPE)
        assert t._reader_thread.is_alive()
        assert t._writer_thread.is_alive()
        t.close()
        assert not t._reader_thread.is_alive()
        assert not t._writer_thread.is_alive()

    def test_thread_exits_after_subprocess(self):
        """Tee threads exit after subprocess completes."""
        with Popen(["echo", "done"], stdout=tee(PIPE)) as proc:
            proc.stdout.read()
        # After context exit, threads should be joined
        assert not proc._stdout_tee._reader_thread.is_alive()
        assert not proc._stdout_tee._writer_thread.is_alive()


class TestEdgeCases:
    """Edge cases and error handling."""

    def test_empty_output(self):
        """Handle subprocess with no output."""
        proc = Popen(["true"], stdout=tee(PIPE))
        output = proc.stdout.read()
        proc.wait()
        assert output == b""

    def test_large_output(self):
        """Handle large output without deadlock."""
        # Generate 100KB of output
        proc = Popen(
            ["dd", "if=/dev/zero", "bs=1024", "count=100", "status=none"],
            stdout=tee(PIPE),
        )
        output = proc.stdout.read()
        proc.wait()
        assert len(output) == 100 * 1024

    def test_binary_data(self):
        """Handle binary data correctly."""
        proc = Popen(
            [
                sys.executable,
                "-c",
                "import sys; sys.stdout.buffer.write(b'\\x00\\x01\\x02\\xff')",
            ],
            stdout=tee(PIPE),
        )
        output = proc.stdout.read()
        proc.wait()
        assert output == b"\x00\x01\x02\xff"

    def test_multiple_tee_destinations_all_receive_data(self):
        """All tee destinations receive the same data."""
        fname1 = tempfile.NamedTemporaryFile(delete=False).name
        fname2 = tempfile.NamedTemporaryFile(delete=False).name

        try:
            with open(fname1, "wb") as f1:
                with open(fname2, "wb") as f2:
                    proc = Popen(["echo", "multi"], stdout=tee(f1, f2, PIPE))
                    captured = proc.stdout.read()
                    proc.wait()

            with open(fname1, "rb") as f1:
                data1 = f1.read()
            with open(fname2, "rb") as f2:
                data2 = f2.read()

            assert captured == b"multi\n"
            assert data1 == b"multi\n"
            assert data2 == b"multi\n"
        finally:
            os.unlink(fname1)
            os.unlink(fname2)

    def test_rapid_subprocess_exit(self):
        """Handle subprocess that exits immediately."""
        for _ in range(10):
            proc = Popen(["true"], stdout=tee(PIPE))
            proc.stdout.read()
            proc.wait()


class TestModuleExports:
    """Test module exports and constants."""

    def test_pipe_constant(self):
        """PIPE constant matches stdlib."""
        assert sm.PIPE == stdlib_subprocess.PIPE

    def test_stdout_constant(self):
        """STDOUT constant matches stdlib."""
        assert sm.STDOUT == stdlib_subprocess.STDOUT

    def test_devnull_constant(self):
        """DEVNULL constant matches stdlib."""
        assert sm.DEVNULL == stdlib_subprocess.DEVNULL

    def test_all_exports(self):
        """__all__ contains expected exports."""
        assert "tee" in sm.__all__
        assert "Popen" in sm.__all__
        assert "run" in sm.__all__
        assert "PIPE" in sm.__all__


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
