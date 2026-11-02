"""Hand an isolated input's terminal exception to its supervisor for the service-side failure record."""

import os
import re
import signal
import sys
import traceback
from pathlib import Path

import labqoat


class FailureReport:
    """Bounded exception summary written by the input process and read once by the supervisor."""

    VARIABLE = "LABQOAT_FAILURE_REPORT"
    LIMIT = 2000

    @classmethod
    def record(cls, error: BaseException) -> None:
        """Keep the exception type, message and innermost frame; never mask the original failure."""
        destination = os.environ.get(cls.VARIABLE)
        if not destination:
            return
        try:
            Path(destination).write_text(cls.summary(error), encoding="utf-8")
        except OSError:
            return

    @classmethod
    def summary(cls, error: BaseException) -> str:
        """Name the exception, its message and where it was raised within the service's detail bound."""
        authored = [frame for frame in traceback.extract_tb(error.__traceback__) if not cls._managed(frame.filename)]
        location = f" at {cls._source(authored[-1].filename)}:{authored[-1].lineno}" if authored else ""
        advice = cls._advice(error)
        return f"{type(error).__name__}: {error}{location}"[: cls.LIMIT - len(advice)] + advice

    @staticmethod
    def _advice(error: BaseException) -> str:
        """How to fix failures whose own message does not say, as the workload itself sees them."""
        filename = getattr(error, "filename", None)
        if isinstance(error, PermissionError) and filename and Path(str(filename)).parent == Path("/"):
            return (
                ". The workload's user cannot create directories at the image root: mount a volume there, or point "
                "the setting that names it (HF_HOME, a cache directory) at /tmp or the home directory"
            )
        if isinstance(error, FileNotFoundError) and re.search(r"/inputs/[0-9a-f]{64}/", str(filename or "")):
            return (
                ". Only the app's .py files are shipped with a run: add data files to the image with "
                ".add_local_file()/.add_local_dir(), put them on a volume, or publish them as an asset"
            )
        if "Failed to find C compiler" in str(error):
            return '. Triton compiles kernels as it runs: add .apt_install("gcc", "libc6-dev") to the image'
        return ""

    @staticmethod
    def _managed(filename: str) -> bool:
        """Frames inside the SDK or the interpreter never locate an authored mistake."""
        return filename.startswith((str(Path(labqoat.__file__).parent), sys.base_prefix, "<"))

    @staticmethod
    def _source(filename: str) -> str:
        """Name delivered application files as their author wrote them, without the worker's content address."""
        return re.sub(r"^.*/inputs/[0-9a-f]{64}/", "", filename)

    @classmethod
    def read(cls, source: Path, status: int) -> str:
        """Prefer the retained exception; otherwise report how the process ended."""
        try:
            summary = source.read_text(encoding="utf-8", errors="replace")[: cls.LIMIT]
        except OSError:
            summary = ""
        return summary or cls._exit(status)

    @staticmethod
    def _exit(status: int) -> str:
        """Explain an exit that raised nothing: a fatal signal, or authored code leaving the process itself."""
        if status < 0:
            name = signal.Signals(-status).name if -status in signal.valid_signals() else f"signal {-status}"
            hint = " (commonly the memory limit was exceeded)" if name == "SIGKILL" else ""
            return f"Input process was terminated by {name}{hint} before reporting an exception"
        return (
            f"Input process exited with status {status} without raising an exception (os._exit or sys.exit); "
            "its last output is in `lab run logs RUN --source app -n 50`"
        )
