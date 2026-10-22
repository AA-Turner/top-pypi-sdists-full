"""What a Cloud Computer launch carries into the worker process.

Read once at the process boundary (``server.py``, the worker's one environment reader) and
passed down; nothing below the entrypoint reads the environment for these values.

The machine files token (``cloud_files:write``) must never be reachable from what an
agent runs on the machine (review 3 D2, 2026-10-21): agents run as the worker's own
uid (and may sudo), so an environment variable is readable from ``/proc/<pid>/environ``
of every process that inherited it. The image's root entrypoint therefore moves the
token out of the environment into :data:`FILES_TOKEN_FILE` before anything starts;
the worker takes it once (:func:`take_files_token`, which deletes the file), keeps it
only in memory, and makes its own process unreadable to other processes
(:func:`hide_process_memory`).
"""

from __future__ import annotations

import ctypes
import logging
import sys
from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)

#: Where the image's root entrypoint leaves the launch token for the worker (one read, then gone).
FILES_TOKEN_FILE = Path("/run/cloud-computer-files/token")
FILES_TOKEN_ENV = "MATRX_CLOUD_FILES_TOKEN"
_PR_SET_DUMPABLE = 4


@dataclass(frozen=True)
class CloudComputerLaunch:
    #: Machine files token minted at launch; empty when the launch carried none (sync stays off).
    files_token: str = ""
    #: The files bridge the token is good for; empty when the launch carried none.
    files_url: str = ""
    #: The process environment the loopback agent daemon starts from (secrets are stripped there).
    process_env: Mapping[str, str] = field(default_factory=dict)


def take_files_token(env: MutableMapping[str, str], path: Path = FILES_TOKEN_FILE) -> str:
    """The launch token, taken ONCE: read from the entrypoint's file (then deleted) or,
    on an image without that step, popped from ``env`` so no child process inherits it."""
    from_env = env.pop(FILES_TOKEN_ENV, "")
    try:
        token = path.read_text().strip()
    except OSError:
        return from_env
    try:
        path.unlink()
    except OSError as exc:
        logger.error("cloud files token file could not be removed (%s); it stays readable", exc)
    return token or from_env


def hide_process_memory() -> bool:
    """Mark this process non-dumpable: its ``/proc/<pid>/environ``, ``mem`` and ptrace
    are then closed to every other process of the same uid (only CAP_SYS_PTRACE, which
    the machine's processes do not have, opens them). Children reset it at exec.
    False (and logged) where it cannot be set."""
    if not sys.platform.startswith("linux"):
        return False
    try:
        libc = ctypes.CDLL(None, use_errno=True)
        if libc.prctl(_PR_SET_DUMPABLE, 0, 0, 0, 0) != 0:
            raise OSError(ctypes.get_errno(), "prctl(PR_SET_DUMPABLE, 0) failed")
    except OSError as exc:
        logger.error("worker memory stays readable by same-uid processes: %s", exc)
        return False
    return True


def launch_from_environment(
    env: MutableMapping[str, str], *, token_file: Path = FILES_TOKEN_FILE
) -> CloudComputerLaunch:
    """The launch, read at the process boundary (``server.py`` passes ``os.environ``):
    the token is taken out of ``env`` (so no child inherits it), this process is made
    unreadable to the others, and the agent daemon's starting environment is what is
    left."""
    files_token = take_files_token(env, token_file)
    hide_process_memory()
    return CloudComputerLaunch(
        files_token=files_token,
        files_url=env.get("MATRX_CLOUD_FILES_URL", ""),
        process_env=dict(env),
    )
