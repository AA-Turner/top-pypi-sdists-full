import sys
import os
import subprocess
from metaflow.mflog.mflog import decorate
from metaflow.mflog import TASK_LOG_SOURCE
from typing import Union, TextIO, BinaryIO, Callable, Optional
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
import subprocess


def enqueue_output(file, queue):
    for line in iter(file.readline, ""):
        queue.put(line)
    file.close()


def read_popen_pipes(p: subprocess.Popen):

    with ThreadPoolExecutor(2) as pool:
        q_stdout, q_stderr = Queue(), Queue()
        pool.submit(enqueue_output, p.stdout, q_stdout)
        pool.submit(enqueue_output, p.stderr, q_stderr)
        while True:

            if p.poll() is not None and q_stdout.empty() and q_stderr.empty():
                break

            out_line = err_line = ""

            try:
                out_line = q_stdout.get_nowait()
            except Empty:
                pass
            try:
                err_line = q_stderr.get_nowait()
            except Empty:
                pass

            yield (out_line, err_line)


class LogBroadcaster:
    def __init__(
        self,
        process: subprocess.Popen,
    ):
        self._process = process
        self._file_descriptors_and_parsers = []

    def add_channel(
        self, file_path: str, parser: Optional[Callable[[str], str]] = None
    ):
        self._file_descriptors_and_parsers.append((open(file_path, "a"), parser))

    def _broadcast_lines(self, out_line: str, err_line: str):
        for file_descriptor, parser in self._file_descriptors_and_parsers:
            if out_line != "":
                if parser:
                    out_line = parser(out_line)
                print(out_line, file=file_descriptor, end="", flush=True)
            if err_line != "":
                if parser:
                    err_line = parser(err_line)
                print(err_line, file=file_descriptor, end="", flush=True)

    def publish_line(self, out_line: str, err_line: str):
        self._broadcast_lines(out_line, err_line)

    def broadcast_logs_to_files(self):
        for out_line, err_line in read_popen_pipes(self._process):
            self._broadcast_lines(out_line, err_line)

        self._process.wait()

        for file_descriptor, _ in self._file_descriptors_and_parsers:
            file_descriptor.close()


def run_with_mflog_capture(command, debug=False):
    """
    Run a subprocess with proper mflog integration for stdout/stderr capture.
    This mimics what bash_capture_logs does but in Python.
    """
    # Get the log file paths from environment variables
    stdout_path = os.environ.get("MFLOG_STDOUT")
    stderr_path = os.environ.get("MFLOG_STDERR")

    if not stdout_path or not stderr_path:
        # Fallback to regular subprocess if mflog env vars aren't set
        return subprocess.run(command, check=True, shell=True)

    pipe = subprocess.PIPE if debug else subprocess.DEVNULL
    # Start the subprocess with pipes
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=pipe,
        stderr=pipe,
        text=False,  # Use bytes for proper mflog handling
        bufsize=0,  # Unbuffered for real-time logging
    )

    broadcaster = LogBroadcaster(process)

    broadcaster.add_channel(
        stderr_path, lambda line: decorate(TASK_LOG_SOURCE, line).decode("utf-8")
    )
    broadcaster.publish_line(f"[S3 PROXY] Starting Fast S3 Proxy.....\n", "")
    broadcaster.broadcast_logs_to_files()

    # Check the return code and raise if non-zero
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)

    return process.returncode


if __name__ == "__main__":
    s3_proxy_binary_path = os.environ.get("S3_PROXY_BINARY_COMMAND")
    s3_proxy_debug = bool(os.environ.get("S3_PROXY_BINARY_DEBUG", False))
    if not s3_proxy_binary_path:
        print("S3_PROXY_BINARY_COMMAND environment variable not set")
        sys.exit(1)

    try:
        run_with_mflog_capture(s3_proxy_binary_path, debug=s3_proxy_debug)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except Exception as e:
        print(f"Error running S3 proxy binary: {e}", file=sys.stderr)
        sys.exit(1)
