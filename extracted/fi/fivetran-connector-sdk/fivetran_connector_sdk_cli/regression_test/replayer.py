"""
Everything `fivetran debug --replay` needs: the throwaway replay folder, and the Replayer
that serves recorded @action results from fixture.jsonl.

Replay output (never committed), under <project>/.fixtures_replay/<scenario>/:
    warehouse.db
    state.json
It is recreated from fixtures/<scenario>/record_start/ on every run, and the project's
.gitignore is updated so it is never committed.

The recording's --max-records cap is read from the fixture header and enforced here exactly
as it was while recording, so both runs stop at the same write.
"""

import io
import json
import shutil
import threading
from pathlib import Path
from typing import Any, Optional

from fivetran_connector_sdk_common.constants import GITIGNORE_FILENAME, GITIGNORE_REPLAY_PATTERN, REPLAY_ROOT_DIR
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging
from fivetran_connector_sdk_cli.regression_test.fixture_helper import (
    FIXTURE_HEADER_KEY, FIXTURE_JSONL, FIXTURE_VERSION, RECORD_DATA_DIR, RECORD_END_DIR, RECORD_START_DIR,
    copy_initial_state, read_state,
)
from fivetran_connector_sdk_cli.regression_test.max_record_helper import DEFAULT_MAX_RECORDS, MaxRecordHandler


class ReplayError(Exception):
    """A replay could not run, or an @action call has no matching recorded interaction."""


class FixtureVersionError(ReplayError):
    """fixture.jsonl is empty, malformed, or written by an incompatible version."""


RE_RECORD_FIX = "Re-record the scenario."


def _replay_error(problem: str, fix: str = RE_RECORD_FIX, error_class: type = ReplayError) -> ReplayError:
    """A replay error worded as what went wrong, then what to do about it, so every replay error reads the same way."""
    return error_class(f"{problem} {fix}")


def replay_root(project_path: str, scenario: str) -> Path:
    """Return <project>/.fixtures_replay/<scenario>/. The caller must have validated the scenario name."""
    return Path(project_path) / REPLAY_ROOT_DIR / scenario


def ensure_gitignore_entry(project_path: str) -> None:
    """Append .fixtures_replay/ to <project>/.gitignore (creating it if needed) unless present."""
    gitignore_path = Path(project_path) / GITIGNORE_FILENAME
    existing_text = ""
    if gitignore_path.exists():
        existing_text = gitignore_path.read_text(encoding="utf-8")
        if GITIGNORE_REPLAY_PATTERN in (line.strip() for line in existing_text.splitlines()):
            return
    with open(gitignore_path, "a", encoding="utf-8") as f:
        # Decide from the file's terminator, not its last line's content, so trailing whitespace can't swallow the entry.
        if existing_text and not existing_text.endswith(("\n", "\r")):
            f.write("\n")
        f.write(f"{GITIGNORE_REPLAY_PATTERN}\n")


def assert_fixture_exists(scenario_path: Path, scenario: str) -> Path:
    """Return the fixture.jsonl path, or raise ReplayError telling the user to record first."""
    fixture_path = scenario_path / RECORD_DATA_DIR / FIXTURE_JSONL
    if not fixture_path.is_file():
        raise _replay_error(f"No recording found for scenario '{scenario}' ({fixture_path}).", "Record it first.")
    return fixture_path


def assert_recording_complete(scenario_path: Path, scenario: str) -> None:
    """Raise ReplayError naming the first of record_start/ and record_end/ that is missing. Recording always creates both."""
    for folder in (RECORD_START_DIR, RECORD_END_DIR):
        if not (scenario_path / folder).is_dir():
            raise _replay_error(f"The recording of scenario '{scenario}' is incomplete: {folder}/ is missing "
                                f"({scenario_path / folder}).")


def prepare_replay(project_path: str, scenario: str, scenario_path: Path) -> Path:
    """Recreate .fixtures_replay/<scenario>/ from record_start/ and return its path."""
    replay_dir = replay_root(project_path, scenario)
    try:
        ensure_gitignore_entry(project_path)
        if replay_dir.is_symlink():
            raise _replay_error(f"The replay folder {replay_dir} is a symbolic link.", "Delete the link and try again.")
        if replay_dir.exists():
            shutil.rmtree(replay_dir)
        replay_dir.mkdir(parents=True, exist_ok=True)
        copy_initial_state(scenario_path / RECORD_START_DIR, replay_dir)
    except (OSError, UnicodeDecodeError) as e:
        raise _replay_error(f"Cannot prepare the replay folder {replay_dir}: {e}.",
                            "Close any program using files in it, or delete it, and try again.") from e
    return replay_dir


def _canonical_state_value(value) -> str:
    """JSON text of a state value. Unlike Python ==, it keeps 1, 1.0 and true apart, and equates NaN with NaN."""
    return json.dumps(value, sort_keys=True)


def compare_state_files(record_end_dir: Path, replay_dir: Path) -> list:
    """Compare state.json in the two folders key by key; return mismatch messages (empty = equal)."""
    expected = read_state(record_end_dir)
    actual = read_state(replay_dir)
    mismatches = []
    for key in sorted(set(expected) | set(actual)):
        if key not in expected:
            mismatches.append(f"'{key}': the replay saved it, but the recording has no such state value")
        elif key not in actual:
            mismatches.append(f"'{key}': the recording has it, but the replay didn't save it")
        elif _canonical_state_value(expected[key]) != _canonical_state_value(actual[key]):
            mismatches.append(f"'{key}': recorded {expected[key]!r}, replay {actual[key]!r}")
    return mismatches


class Replayer:
    """
    Class-level replay state shared between Connector, which starts and stops a replay, and
    the `@action` decorator, which runs deep inside connector code.

    The fixture stays open for the whole run. Each lookup rewinds it and scans for the first
    interaction with the same name and arguments, so memory use stays constant.
    """

    # Open handle on fixture.jsonl while a replay is running, None otherwise.
    _file_handle: Optional[io.TextIOBase] = None
    # Guards _file_handle, because connectors may call @action functions from several threads.
    _lock: threading.Lock = threading.Lock()
    # The first lookup error of this replay. Connector code can catch that error, so the replay checks this after the sync.
    _lookup_failure: Optional[str] = None

    @classmethod
    def start(cls, fixture_path: str) -> None:
        """Open the fixture, validate its header and apply its recorded --max-records cap."""
        with cls._lock:
            cls._lookup_failure = None
            cls._close_locked()
            try:
                fh = open(fixture_path, "r", encoding="utf-8")
            except OSError as e:
                raise _replay_error(f"Cannot read fixture.jsonl at {fixture_path}: {e}.") from e
            try:
                capped_count = cls._read_header(fh, fixture_path)
            except UnicodeDecodeError as e:
                fh.close()
                raise _replay_error(f"Cannot read {fixture_path}: it is not valid UTF-8.",
                                    error_class=FixtureVersionError) from e
            except Exception:
                fh.close()
                raise
            cls._file_handle = fh
        MaxRecordHandler.start(capped_count)

    @classmethod
    def _body_lines_locked(cls):
        """Yield (line_number, line) for each line after the header; an unreadable line is reported as a ReplayError."""
        fh = cls._file_handle
        fh.seek(0)
        fh.readline()
        try:
            for line_number, line in enumerate(fh, start=2):
                yield line_number, line
        except UnicodeDecodeError as e:
            raise _replay_error(f"Cannot read {fh.name}: it is not valid UTF-8.") from e
        except OSError as e:
            raise _replay_error(f"Cannot read {fh.name}: {e}.") from e

    @classmethod
    def has_interactions(cls) -> bool:
        """True if the open fixture has at least one recorded interaction after its header."""
        with cls._lock:
            if cls._file_handle is None:
                return False
            return any(line.strip() for _, line in cls._body_lines_locked())

    @classmethod
    def stop(cls) -> None:
        """Close the fixture and remove the cap. Safe to call when not replaying."""
        with cls._lock:
            cls._lookup_failure = None
            cls._close_locked()
        MaxRecordHandler.stop()

    @classmethod
    def lookup_failure(cls) -> Optional[str]:
        """The first lookup error since start(), or None. Set even when connector code caught the error."""
        return cls._lookup_failure

    @classmethod
    def _close_locked(cls) -> None:
        if cls._file_handle is not None:
            cls._file_handle.close()
            cls._file_handle = None

    @classmethod
    def lookup(cls, name: str, arguments: dict) -> Any:
        """Return the recorded result of the first interaction matching (name, arguments)."""
        try:
            return cls._find(name, arguments)
        except ReplayError as e:
            # After the cap ends the sync, run_update() ignores connector errors, so a miss from a late worker is not a failure.
            if cls._lookup_failure is None and not MaxRecordHandler.is_stopped_by_cap():
                cls._lookup_failure = str(e)
            raise

    @classmethod
    def _find(cls, name: str, arguments: dict) -> Any:
        target = json.dumps(arguments, sort_keys=True)
        with cls._lock:
            if cls._file_handle is not None:
                for line_number, line in cls._body_lines_locked():
                    try:
                        entry = json.loads(line)
                        entry_matches = (entry["interaction"] == name
                                         and json.dumps(entry["arguments"], sort_keys=True) == target)
                        if entry_matches:
                            return entry["result"]
                    except (ValueError, KeyError, TypeError) as e:
                        raise _replay_error(f"fixture.jsonl line {line_number} is corrupt: {e!r}.") from e
        raise _replay_error(
            f"No recorded interaction for '{name}' with arguments {arguments}. "
            "The connector made a call that was not recorded.",
            "Re-record the scenario to capture it. "
            "If an argument changes on every run (for example a timestamp), use match= on the @action "
            "to leave it out."
        )

    @staticmethod
    def _read_header(fh, fixture_path: str) -> int:
        """Validate the fixture header line and return its capped_count."""
        first_line = fh.readline()
        if not first_line:
            raise _replay_error(f"fixture.jsonl at {fixture_path} is empty.", error_class=FixtureVersionError)
        try:
            header_line = json.loads(first_line)
        except json.JSONDecodeError as e:
            raise _replay_error(f"fixture.jsonl at {fixture_path} has an invalid header line.",
                                error_class=FixtureVersionError) from e
        header = header_line.get(FIXTURE_HEADER_KEY) if isinstance(header_line, dict) else None
        if not isinstance(header, dict):
            raise _replay_error(f"fixture.jsonl at {fixture_path} is missing '{FIXTURE_HEADER_KEY}' on line 1.",
                                error_class=FixtureVersionError)
        version = header.get("fixture_version")
        if version != FIXTURE_VERSION:
            raise _replay_error(f"fixture_version '{version}' is not supported. Supported version: {FIXTURE_VERSION}.",
                                error_class=FixtureVersionError)
        capped_count = header.get("capped_count")
        # Recording always writes a positive integer. A missing or invalid value means the file was edited or damaged,
        # so warn and use the recording default rather than running without a cap.
        if isinstance(capped_count, bool) or not isinstance(capped_count, int) or capped_count <= 0:
            print_library_log(f"fixture.jsonl at {fixture_path} has a missing or incorrect capped_count "
                              f"({capped_count!r}); using the default of {DEFAULT_MAX_RECORDS}.",
                              Logging.Level.WARNING)
            return DEFAULT_MAX_RECORDS
        return capped_count
