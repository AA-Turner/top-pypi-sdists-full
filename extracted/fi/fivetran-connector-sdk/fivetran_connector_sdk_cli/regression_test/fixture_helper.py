"""
Shared knowledge of the fixture layout, used by both the record and the replay side.

Scenario folders (meant to be committed), under <project>/fixtures/<scenario>/:

    record_start/    snapshot of files/ taken just before the record run;
                     the canonical starting state of the scenario
        warehouse.db
        state.json
    record_data/
        fixture.jsonl    captured @action calls, one JSON object per line
    record_end/      output of the record run (seeded from record_start/)
        warehouse.db
        state.json

Fixture format (JSONL, one JSON object per line):
    line 1:  {"__fixture_header__": {"fixture_version": "1.0", "capped_count": 30}}
    line 2+: {"interaction": "<name>", "arguments": {...}, "result": ...}
"""

import json
import shutil
from pathlib import Path

from fivetran_connector_sdk_common.constants import FIXTURES_DIR

class RecordError(RuntimeError):
    """A record run failed for a reason of its own (lock, scenario folder, state.json, nothing captured), not in the connector."""


RECORD_START_DIR = "record_start"
RECORD_DATA_DIR = "record_data"
RECORD_END_DIR = "record_end"
FIXTURE_JSONL = "fixture.jsonl"

WAREHOUSE_DB = "warehouse.db"
STATE_JSON = "state.json"
FIXTURE_VERSION = "1.0"
FIXTURE_HEADER_KEY = "__fixture_header__"


def scenario_root(project_path: str, scenario: str) -> Path:
    """Return <project>/fixtures/<scenario>/. The caller must have validated the scenario name."""
    return Path(project_path) / FIXTURES_DIR / scenario


def build_fixture_header(capped_count: int) -> dict:
    """Return the dict written as the first line of fixture.jsonl."""
    return {
        FIXTURE_HEADER_KEY: {
            "fixture_version": FIXTURE_VERSION,
            "capped_count": capped_count,
        }
    }


def copy_initial_state(source_dir: Path, dest_dir: Path) -> None:
    """Copy the whole files snapshot (warehouse.db, state.json and the uploaded files under storage/) from source_dir to dest_dir.
    Does nothing if source_dir is missing."""
    if source_dir.exists():
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True, copy_function=shutil.copy2)


def read_state(directory: Path) -> dict:
    """
    Read state.json from a directory; empty dict if absent.

    Raises:
        RecordError: If state.json is unreadable, not valid JSON, or not a JSON object.
    """
    state_file = directory / STATE_JSON
    if not state_file.exists():
        return {}
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
    except (OSError, ValueError) as e:
        raise RecordError(f"Invalid {STATE_JSON} at '{state_file}': {e}") from e
    if not isinstance(state, dict):
        raise RecordError(f"Invalid {STATE_JSON} at '{state_file}': expected a JSON object, got {type(state).__name__}")
    return state
