"""A TRL job's run key (`external_id = trl:<key>`): minted on a fresh start and kept in the job's `output_dir`,
so only that job's own `resume_from_checkpoint` continues its run. DESIGN.md "Run key"."""

from __future__ import annotations

import os
import re
import tempfile
import uuid
from dataclasses import dataclass
from typing import Any

#: The key file, inside the job's `output_dir`.
KEY_FOLDER = ".probe"
KEY_FILE = "run-key"
#: A TRL run's external_id prefix.
KEY_PREFIX = "trl:"
#: A key this module wrote: 32 hex digits (`uuid4().hex`).
_KEY = re.compile(r"^[0-9a-f]{32}$")
#: How many of the project's newest runs a pre-key resume looks through for the run it came from.
LEGACY_SCAN_LIMIT = 200


@dataclass(frozen=True)
class RunKey:
    """What a job opens its run with."""

    #: `trl:<key>`, or None when the folder could not keep one: that run cannot be resumed onto.
    external_id: str | None
    #: The key came from the folder: this resume continues that job's run (a rewind).
    is_continued: bool = False
    #: A resume whose folder holds no key (a checkpoint from before keys): it starts a new run.
    is_legacy_resume: bool = False
    #: Why the folder could not keep a key, for the warning.
    save_error: str | None = None


def make_run_key(output_dir: str | None, *, is_resume: bool) -> RunKey:
    """A resume reads the job's key from ``output_dir``; a fresh start (a new job) always mints and saves a new
    one, so it never supersedes the folder's last run. A resume finding no key mints one too: from here on its
    own relaunches continue the new run."""
    if is_resume:
        key = load_run_key(output_dir)
        if key is not None:
            return RunKey(f"{KEY_PREFIX}{key}", is_continued=True)
    key = uuid.uuid4().hex
    error = save_run_key(output_dir, key)
    if error is not None:
        return RunKey(None, is_legacy_resume=is_resume, save_error=error)
    return RunKey(f"{KEY_PREFIX}{key}", is_legacy_resume=is_resume)


def load_run_key(output_dir: str | None) -> str | None:
    """The key a fresh start saved in ``output_dir``; None when there is none or it is not one of ours."""
    if not output_dir:
        return None
    try:
        with open(os.path.join(output_dir, KEY_FOLDER, KEY_FILE), encoding="utf-8") as handle:
            key = handle.read().strip()
    except (OSError, UnicodeDecodeError):
        return None
    return key if _KEY.match(key) else None


def save_run_key(output_dir: str | None, key: str) -> str | None:
    """Write ``key`` to ``output_dir/.probe/run-key`` whole or not at all (a temp file, then a rename). Returns
    None when saved, else why not. Only the world-zero process calls it: it alone opens the run."""
    if not output_dir:
        return "the trainer has no output_dir"
    folder = os.path.join(output_dir, KEY_FOLDER)
    temp = None
    try:
        os.makedirs(folder, exist_ok=True)
        handle, temp = tempfile.mkstemp(prefix=f".{KEY_FILE}.", dir=folder)
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            file.write(key + "\n")
        os.replace(temp, os.path.join(folder, KEY_FILE))
        return None
    except OSError as exc:
        if temp is not None:
            try:
                os.unlink(temp)
            except OSError:
                pass
        return f"{type(exc).__name__}: {exc}"


def find_legacy_parent(run: Any, legacy_external_id: str) -> str | None:
    """A pre-key checkpoint's run: the one run in ``run``'s own project with the old shared key (`trl:<name>`) and
    ``run``'s source, among its newest `LEGACY_SCAN_LIMIT`. None when there is no single such run: a link names
    what is certain, and a run in another project is never looked at."""
    client, project_id = getattr(run, "_client", None), getattr(run, "project_id", None)
    if client is None or project_id is None:
        return None
    source = str((getattr(run, "data", None) or {}).get("source") or "").strip().lower()
    page = client.list_runs(project_id=project_id, limit=LEGACY_SCAN_LIMIT)
    found = [row for row in page.items or []
             if row.get("external_id") == legacy_external_id and str(row.get("id")) != str(run.id)
             and str(row.get("source") or "").strip().lower() == source
             and str(row.get("project_id")) == str(project_id)]
    return str(found[0]["id"]) if len(found) == 1 else None
