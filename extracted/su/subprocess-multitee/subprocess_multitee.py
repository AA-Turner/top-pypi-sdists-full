"""
Subprocess utilities for multiplexing stdout/stderr to multiple destinations.
"""

import errno
import inspect
import io
import os
import queue
import select
import subprocess as _subprocess
import sys
import threading
from subprocess import (
    DEVNULL,
    PIPE,
    STDOUT,
    CalledProcessError,
    CompletedProcess,
    SubprocessError,
    TimeoutExpired,
    check_output,
    getoutput,
    getstatusoutput,
)
from typing import IO, Any, List, Optional

# use presence of msvcrt to detect Windows-like platforms (see bpo-8110)
try:
    import msvcrt
except ModuleNotFoundError:
    _mswindows = False
else:
    _mswindows = True

__all__ = [
    "tee",
    "Popen",
    "PIPE",
    "STDOUT",
    "call",
    "check_call",
    "getstatusoutput",
    "getoutput",
    "check_output",
    "run",
    "CalledProcessError",
    "DEVNULL",
    "SubprocessError",
    "TimeoutExpired",
    "CompletedProcess",
]


_READ_CHUNK_SIZE = 65536  # 64KB - matches typical pipe buffer size


def tee(*destinations: Any, read_chunk_size: Optional[int] = None) -> "_Tee":
    """
    Create a tee object that can be passed to subprocess.Popen as stdout/stderr.

    Accepts any number of arguments of the same kind as Popen accepts for
    stdout/stderr (file descriptors, file objects, subprocess.PIPE,
    subprocess.DEVNULL), except for subprocess.STDOUT.

    Spawns a background thread that reads single bytes and writes them to all
    destinations.

    Example using subprocess_multitee.Popen (preferred):
        from subprocess_multitee import Popen, tee, PIPE
        proc = Popen(['ls', '-la'], stdout=tee(PIPE, sys.stdout))
        output = proc.stdout.read()  # Works directly!
        proc.wait()

    Example using stdlib Popen:
        import subprocess
        t = tee(subprocess.PIPE, sys.stdout, open('log.txt', 'wb'))
        proc = subprocess.Popen(['ls', '-la'], stdout=t)
        proc.wait()
        t.close()
        output = t.pipes[0].read()

    Args:
        *destinations: Any number of valid Popen stdout/stderr arguments
                       (except subprocess.STDOUT)

    Returns:
        A _Tee object with a fileno() method for use with Popen
    """
    return _Tee(*destinations, read_chunk_size=read_chunk_size)


class _Tee:
    """Internal class implementing the tee functionality."""

    def __init__(self, *destinations: Any, read_chunk_size: Optional[int] = None):
        if read_chunk_size is None:
            read_chunk_size = _READ_CHUNK_SIZE
        self._read_fd, self._write_fd = os.pipe()

        # Set inheritability: write fd should be inherited by child,
        # read fd stays in parent only
        try:
            os.set_inheritable(self._read_fd, False)
            os.set_inheritable(self._write_fd, True)
        except (AttributeError, OSError):
            pass  # Not available on all platforms

        self._outputs: List[tuple] = []  # (kind, dest, owned)
        self._owned_fds: List[int] = []
        self.pipes: List[IO[bytes]] = []
        self._read_chunk_size = read_chunk_size

        for dest in destinations:
            if dest == STDOUT:
                raise ValueError("subprocess.STDOUT is not supported by tee()")
            elif dest == PIPE:
                r, w = os.pipe()
                try:
                    os.set_inheritable(r, False)
                    os.set_inheritable(w, False)
                except (AttributeError, OSError):
                    pass
                self._outputs.append(("fd", w))
                self._owned_fds.append(w)
                pipe_read = os.fdopen(r, "rb")
                self.pipes.append(pipe_read)
            elif dest == DEVNULL:
                # Skip DEVNULL destinations entirely - no need to write to them
                continue
            elif isinstance(dest, int):
                # Borrowed fd - wrap without taking ownership
                self._outputs.append(("fd", dest))
            elif hasattr(dest, "write"):
                # File-like object - check for .buffer for text mode files
                if hasattr(dest, "buffer"):
                    # Text wrapper - use underlying binary buffer
                    self._outputs.append(("file", dest.buffer))
                else:
                    self._outputs.append(("file", dest))
            else:
                raise TypeError(f"Unsupported destination type: {type(dest)}")

        self._queue: queue.Queue = queue.Queue()

        self._reader_thread = threading.Thread(
            target=self._reader_loop, daemon=True, name="subprocess_multitee.reader"
        )
        self._writer_thread = threading.Thread(
            target=self._writer_loop, daemon=True, name="subprocess_multitee.writer"
        )
        self._reader_thread.start()
        self._writer_thread.start()

    def fileno(self) -> int:
        """Return the file descriptor for use with Popen."""
        return self._write_fd

    def _reader_loop(self) -> None:
        """Read chunks from pipe and enqueue them as soon as available."""
        try:
            if sys.platform != "win32":
                os.set_blocking(self._read_fd, False)
                while True:
                    # Wait for data to be available
                    select.select([self._read_fd], [], [])

                    # Drain all currently available data
                    while True:
                        try:
                            data = os.read(self._read_fd, self._read_chunk_size)
                            if not data:
                                return  # EOF
                            self._queue.put(data)
                        except OSError as e:
                            if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK):
                                break  # No more data right now, back to select
                            raise
            else:
                # Windows: select() doesn't work on pipes, use blocking reads
                while True:
                    data = os.read(self._read_fd, self._read_chunk_size)
                    if not data:
                        return
                    self._queue.put(data)
        finally:
            self._queue.put(None)  # EOF sentinel
            os.close(self._read_fd)

    def _writer_loop(self) -> None:
        """Drain queue and write to all destinations."""
        outputs = self._outputs[:]
        try:
            while True:
                data = self._queue.get()
                if data is None:
                    break

                dead = []
                for i, (kind, dest) in enumerate(outputs):
                    try:
                        if kind == "fd":
                            os.write(dest, data)
                        else:
                            dest.write(data)
                            dest.flush()
                    except (OSError, IOError, ValueError):
                        dead.append(i)

                for i in reversed(dead):
                    outputs.pop(i)
        finally:
            for fd in self._owned_fds:
                try:
                    os.close(fd)
                except OSError:
                    pass

    def close(self) -> None:
        """Close the write end and wait for the thread to finish."""
        if self._write_fd != -1:
            try:
                os.close(self._write_fd)
            except OSError:
                pass
            self._write_fd = -1
        self._reader_thread.join()
        self._writer_thread.join()

    def __enter__(self) -> "_Tee":
        return self

    def __exit__(self, *args) -> None:
        self.close()


class Popen(_subprocess.Popen):
    """
    Popen subclass with tee support.

    When stdout or stderr is a tee() object containing PIPE, the first
    PIPE destination is automatically exposed as self.stdout or self.stderr,
    allowing normal usage patterns:

        proc = Popen(['cmd'], stdout=tee(PIPE, open('log.txt', 'wb')))
        output = proc.stdout.read()  # Works!
        proc.wait()

    Also properly handles closing the parent's copy of the write fd after
    fork so the tee thread sees EOF when the subprocess exits.
    """

    def __init__(self, *args, **kwargs):
        # Use inspect.signature to robustly extract stdout/stderr regardless
        # of whether they were passed positionally or as keywords
        sig = inspect.signature(_subprocess.Popen.__init__)
        try:
            bound = sig.bind(self, *args, **kwargs)
            bound.apply_defaults()
            stdout = bound.arguments.get("stdout")
            stderr = bound.arguments.get("stderr")
        except TypeError:
            # Fallback if binding fails
            stdout = kwargs.get("stdout")
            stderr = kwargs.get("stderr")

        self._stdout_tee = stdout if isinstance(stdout, _Tee) else None
        self._stderr_tee = stderr if isinstance(stderr, _Tee) else None

        super().__init__(*args, **kwargs)

        # Close parent's copy of write fds after fork - child has its own copy.
        # This ensures the tee thread sees EOF when the subprocess exits.
        # Without this, the parent keeps the write fd open and the thread blocks.
        if self._stdout_tee:
            self._close_tee_write_fd(self._stdout_tee)
        if self._stderr_tee:
            self._close_tee_write_fd(self._stderr_tee)

        # If tee was used with PIPE, expose the first pipe as stdout/stderr
        if self._stdout_tee and self._stdout_tee.pipes:
            self.stdout = self._stdout_tee.pipes[0]
            if self.text_mode:
                self.stdout = io.TextIOWrapper(
                    self.stdout, encoding=self.encoding, errors=self.errors
                )

        if self._stderr_tee and self._stderr_tee.pipes:
            self.stderr = self._stderr_tee.pipes[0]
            if self.text_mode:
                self.stderr = io.TextIOWrapper(
                    self.stderr, encoding=self.encoding, errors=self.errors
                )

    @staticmethod
    def _close_tee_write_fd(tee_obj: _Tee) -> None:
        """Close the tee's write fd in the parent process."""
        if tee_obj._write_fd != -1:
            try:
                os.close(tee_obj._write_fd)
            except OSError:
                pass
            tee_obj._write_fd = -1

    def __exit__(self, exc_type, value, traceback):
        result = super().__exit__(exc_type, value, traceback)
        # Join tee threads (they should already be done since subprocess exited
        # and we closed the write fds, so the threads saw EOF)
        if self._stdout_tee:
            self._stdout_tee._reader_thread.join()
            self._stdout_tee._writer_thread.join()
        if self._stderr_tee:
            self._stderr_tee._reader_thread.join()
            self._stderr_tee._writer_thread.join()
        return result


def call(*popenargs, timeout=None, **kwargs):
    """Run command with arguments.  Wait for command to complete or
    for timeout seconds, then return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = call(["ls", "-l"])
    """
    with Popen(*popenargs, **kwargs) as p:
        try:
            return p.wait(timeout=timeout)
        except:  # Including KeyboardInterrupt, wait handled that.
            p.kill()
            # We don't call p.wait() again as p.__exit__ does that for us.
            raise


def check_call(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete.  If
    the exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.

    The arguments are the same as for the call function.  Example:

    check_call(["ls", "-l"])
    """
    retcode = call(*popenargs, **kwargs)
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd)
    return 0


def run(
    *popenargs, input=None, capture_output=False, timeout=None, check=False, **kwargs
):
    """Run command with arguments and return a CompletedProcess instance.

    The returned instance will have attributes args, returncode, stdout and
    stderr. By default, stdout and stderr are not captured, and those attributes
    will be None. Pass stdout=PIPE and/or stderr=PIPE in order to capture them,
    or pass capture_output=True to capture both.

    If check is True and the exit code was non-zero, it raises a
    CalledProcessError. The CalledProcessError object will have the return code
    in the returncode attribute, and output & stderr attributes if those streams
    were captured.

    If timeout (seconds) is given and the process takes too long,
     a TimeoutExpired exception will be raised.

    There is an optional argument "input", allowing you to
    pass bytes or a string to the subprocess's stdin.  If you use this argument
    you may not also use the Popen constructor's "stdin" argument, as
    it will be used internally.

    By default, all communication is in bytes, and therefore any "input" should
    be bytes, and the stdout and stderr will be bytes. If in text mode, any
    "input" should be a string, and stdout and stderr will be strings decoded
    according to locale encoding, or by "encoding" if set. Text mode is
    triggered by setting any of text, encoding, errors or universal_newlines.

    The other arguments are the same as for the Popen constructor.
    """
    if input is not None:
        if kwargs.get("stdin") is not None:
            raise ValueError("stdin and input arguments may not both be used.")
        kwargs["stdin"] = PIPE

    if capture_output:
        if kwargs.get("stdout") is not None or kwargs.get("stderr") is not None:
            raise ValueError(
                "stdout and stderr arguments may not be used with capture_output."
            )
        kwargs["stdout"] = PIPE
        kwargs["stderr"] = PIPE

    with Popen(*popenargs, **kwargs) as process:
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        except TimeoutExpired as exc:
            process.kill()
            if _mswindows:
                # Windows accumulates the output in a single blocking
                # read() call run on child threads, with the timeout
                # being done in a join() on those threads.  communicate()
                # _after_ kill() is required to collect that and add it
                # to the exception.
                exc.stdout, exc.stderr = process.communicate()
            else:
                # POSIX _communicate already populated the output so
                # far into the TimeoutExpired exception.
                process.wait()
            raise
        except:  # Including KeyboardInterrupt, communicate handled that.
            process.kill()
            # We don't call process.wait() as .__exit__ does that for us.
            raise
        retcode = process.poll()
        if check and retcode:
            raise CalledProcessError(
                retcode, process.args, output=stdout, stderr=stderr
            )
    return CompletedProcess(process.args, retcode, stdout, stderr)
