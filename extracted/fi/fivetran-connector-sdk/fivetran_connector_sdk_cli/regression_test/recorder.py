"""
Everything `fivetran debug --record` needs on the record side: the scenario
folders on disk, and the Recorder that streams @action calls into the fixture.

The scenario folder layout and fixture format are described in fixture_helper.

files/ is never modified by a record run.
"""

import contextlib
import io
import json
import os
import shutil
import sys
import threading
from pathlib import Path
from typing import Optional

from fivetran_connector_sdk_common.constants import OUTPUT_FILES_DIR
from fivetran_connector_sdk_cli.regression_test.fixture_helper import (
    RECORD_DATA_DIR, RECORD_END_DIR, RECORD_START_DIR, STATE_JSON, RecordError, build_fixture_header,
    copy_initial_state,
)
from fivetran_connector_sdk_cli.regression_test.max_record_helper import DEFAULT_MAX_RECORDS, MaxRecordHandler

RECORD_LOCK_FILE = ".record.lock"


def discard_scenario(scenario_path: Path) -> None:
    """
    Remove the record_start/, record_data/ and record_end/ folders of a scenario that produced no
    usable recording, so a header-only fixture.jsonl is not mistaken for an existing scenario.

    The lock file is removed by scenario_lock when the run ends. Sibling scenarios are untouched.
    """
    for sub in (RECORD_START_DIR, RECORD_DATA_DIR, RECORD_END_DIR):
        shutil.rmtree(scenario_path / sub, ignore_errors=True)


def _lock_file(fd: int) -> None:
    """Take an exclusive, non-blocking OS lock on fd. Raises OSError if another process holds it."""
    if sys.platform == "win32":
        import msvcrt
        msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
    else:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)


def _unlock_file(fd: int) -> None:
    if sys.platform == "win32":
        import msvcrt
        msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
    else:
        import fcntl
        fcntl.flock(fd, fcntl.LOCK_UN)


@contextlib.contextmanager
def scenario_lock(scenario_path: Path):
    """
    Hold an exclusive lock on one scenario folder for the duration of a record or replay run.

    Two record runs of the same scenario would wipe each other's folders and interleave writes to
    fixture.jsonl, and a replay during a record run would read a half-written fixture, so the second
    run fails fast instead. The lock is an OS-level lock on a file in
    the scenario root, outside record_start/, record_data/ and record_end/, so prepare_scenario never
    wipes it. The OS drops the lock when the process ends however it ends (crash, kill -9, closed
    terminal), so a stale lock file never blocks a later run; only a live holder does. The file is
    deleted when the run ends, so nothing is left in the committed fixtures.

    Raises:
        RecordError: If another record or replay run holds the lock, or the lock file cannot be created.
    """
    lock_path = scenario_path / RECORD_LOCK_FILE
    try:
        scenario_path.mkdir(parents=True, exist_ok=True)
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
    except OSError as e:
        raise RecordError(f"Failed to lock scenario folder '{scenario_path}' for recording: {e}") from e

    while True:
        try:
            _lock_file(fd)
        except OSError as e:
            os.close(fd)
            raise RecordError(
                f"Another record or replay run is in progress for scenario '{scenario_path.name}' "
                f"(lock file: {lock_path}). Wait for it to finish and retry."
            ) from e
        # The previous holder deletes the file on exit; if we locked a deleted file, lock the new one instead.
        if _is_current_lock_file(fd, lock_path):
            break
        os.close(fd)
        try:
            fd = os.open(lock_path, os.O_CREAT | os.O_RDWR)
        except OSError as e:
            raise RecordError(f"Failed to lock scenario folder '{scenario_path}' for recording: {e}") from e

    try:
        yield
    finally:
        # Delete while still holding the lock (Windows cannot delete an open file, so it unlinks after closing).
        if sys.platform != "win32":
            lock_path.unlink(missing_ok=True)
        try:
            _unlock_file(fd)
        finally:
            os.close(fd)
            if sys.platform == "win32":
                with contextlib.suppress(OSError):
                    lock_path.unlink()
            # A failed recording leaves nothing behind, so the folders it created go too. rmdir only removes an empty one.
            with contextlib.suppress(OSError):
                scenario_path.rmdir()
            with contextlib.suppress(OSError):
                scenario_path.parent.rmdir()

def _is_current_lock_file(fd: int, lock_path: Path) -> bool:
    """True if the file at lock_path is the one fd has open (it was not deleted by a previous holder)."""
    try:
        return os.path.samestat(os.fstat(fd), os.stat(lock_path))
    except OSError:
        return False


def prepare_scenario(project_path: str, scenario_path: Path) -> None:
    """
    Reset one scenario folder and seed it for a record run.

    Wipes and recreates record_start/, record_data/ and record_end/ (sibling
    scenarios are untouched), snapshots files/ into record_start/ (with an empty state.json if files/ has none), then seeds
    record_end/ from record_start/.

    Raises:
        RecordError: If any file operation fails (permissions, locked or missing files, disk full).
    """
    try:
        for sub in (RECORD_START_DIR, RECORD_DATA_DIR, RECORD_END_DIR):
            sub_path = scenario_path / sub
            if sub_path.exists():
                shutil.rmtree(sub_path)
            sub_path.mkdir(parents=True, exist_ok=True)

        copy_initial_state(Path(project_path) / OUTPUT_FILES_DIR, scenario_path / RECORD_START_DIR)
        start_state = scenario_path / RECORD_START_DIR / STATE_JSON
        if not start_state.exists():
            start_state.write_text("{}", encoding="utf-8")
        copy_initial_state(scenario_path / RECORD_START_DIR, scenario_path / RECORD_END_DIR)
    except OSError as e:
        raise RecordError(f"Failed to prepare scenario folder '{scenario_path}' for recording: {e}") from e


class Recorder:
    """
    Class-level recording state shared between the CLI, which starts and stops a
    recording, and the `@action` decorator, which runs deep inside connector code
    where no instance can be passed around.
    """

    # Open handle on fixture.jsonl while a recording is running, None otherwise.
    _file_handle: Optional[io.TextIOBase] = None
    _interaction_count: int = 0
    # Results or arguments that could not be written to the fixture, even if connector code caught the error.
    _failed_count: int = 0

    # Guards _interaction_count, _failed_count and writes to _file_handle, because
    # connectors may call @action functions from several threads.
    _state_lock: threading.Lock = threading.Lock()

    @classmethod
    def start(cls, fixture_path: str, max_records: int = DEFAULT_MAX_RECORDS) -> None:
        """Reset all state, then open fixture.jsonl for writing and emit the header line."""
        with cls._state_lock:
            cls._reset_locked()
            MaxRecordHandler.start(max_records)
            cls._file_handle = open(fixture_path, "w", encoding="utf-8")
            cls._file_handle.write(json.dumps(build_fixture_header(max_records)) + "\n")
            cls._file_handle.flush()

    @classmethod
    def stop(cls) -> None:
        """Close the fixture and reset all state. Safe to call when not recording."""
        with cls._state_lock:
            cls._reset_locked()

    @classmethod
    def _reset_locked(cls) -> None:
        """Close the fixture and zero all counters. Caller must already hold _state_lock."""
        if cls._file_handle is not None:
            try:
                cls._file_handle.close()
            finally:
                cls._file_handle = None

        cls._interaction_count = 0
        cls._failed_count = 0
        MaxRecordHandler.stop()

    @classmethod
    def interaction_count(cls) -> int:
        """Number of @action calls written to the fixture so far."""
        return cls._interaction_count

    @classmethod
    def failed_count(cls) -> int:
        """Number of @action arguments or results that could not be written to the fixture."""
        return cls._failed_count

    @classmethod
    def note_failed_write(cls) -> None:
        """Count an @action argument or result that could not be serialized. Calls after the cap are not counted."""
        with cls._state_lock:
            if cls._file_handle is not None and not MaxRecordHandler.is_stopped_by_cap():
                cls._failed_count += 1

    @classmethod
    def record(cls, name: str, arguments: dict, result) -> None:
        """
        Append one interaction to the fixture and flush.

        Raises TypeError, ValueError (NaN or Infinity) or RecursionError (too deeply nested), before anything is written,
        if the values are not standard JSON. Raises RecordError if the write to the fixture fails.

        A call that arrives after stop(), or after a write was rejected for exceeding the cap
        (a worker thread still running after the sync was halted), is ignored.
        """
        line = json.dumps({"interaction": name, "arguments": arguments, "result": result}, allow_nan=False)
        with cls._state_lock:
            if cls._file_handle is None or MaxRecordHandler.is_stopped_by_cap():
                return
            try:
                cls._file_handle.write(line + "\n")
                cls._file_handle.flush()
            except OSError as e:
                cls._failed_count += 1
                raise RecordError(f"Cannot write interaction '{name}' to {cls._file_handle.name}: {e}") from e
            cls._interaction_count += 1
