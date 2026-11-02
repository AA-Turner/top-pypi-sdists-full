"""cli/imports/folder's doors are lazy: a record session's `probe` loads none of the importer, each
module of the folder imports on its own and in any order, and first reads from four threads at
once all land. The eager door hid the import cycles a lazy one exposes, at ~0.3 s per call."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import probe

_SRC = Path(probe.__file__).resolve().parent.parent  # the folder holding probe/
_FOLDER = _SRC / "probe" / "cli" / "imports" / "folder"
_FOLDER_MODULE = "probe.cli.imports.folder"


def _modules() -> list[str]:
    """Every module of the folder import, by dotted name."""
    names = []
    for path in sorted(_FOLDER.rglob("*.py")):
        parts = list(path.relative_to(_SRC).with_suffix("").parts)
        names.append(".".join(parts[:-1] if parts[-1] == "__init__" else parts))
    return names


def _python(code: str, *args: str, **options) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-c", code, *args], capture_output=True, text=True, timeout=120, **options)


def _last_line(text: str) -> str:
    return (text.strip().splitlines() or [""])[-1]


def test_every_module_of_the_folder_import_imports_on_its_own() -> None:
    """Each first, in a fresh interpreter. Behind the eager door 12 could not: cycles through
    agents/argv, flags, launch_once and classify/plan needed the door's load order."""
    def import_alone(name: str) -> tuple[str, str]:
        result = _python(f"import {name}")
        return name, _last_line(result.stderr) if result.returncode else ""

    with ThreadPoolExecutor(4) as pool:
        failed = {name: error for name, error in pool.map(import_alone, _modules()) if error}
    assert failed == {}


def test_the_folder_import_loads_in_either_order() -> None:
    names = _modules()
    code = "import importlib, json, sys\nfor name in json.loads(sys.argv[1]):\n    importlib.import_module(name)\n"
    for order in (names, names[::-1]):
        result = _python(code, json.dumps(order))
        assert result.returncode == 0, result.stderr


def test_the_doors_load_nothing_and_a_read_loads_only_its_piece() -> None:
    code = (
        "import json, sys\n"
        "import probe.cli.imports.folder as door, probe.cli.backfill_evidence as old_evidence\n"
        f"def pieces():\n    return sorted(m for m in sys.modules if m.startswith('{_FOLDER_MODULE}.'))\n"
        "before = pieces()\n"
        "door.human_bytes\n"
        "print(json.dumps({'before': before, 'after': pieces(),\n"
        f"                  'old_path': old_evidence is sys.modules['{_FOLDER_MODULE}.evidence']}}))\n"
    )
    result = _python(code)
    assert result.returncode == 0, result.stderr
    report = json.loads(_last_line(result.stdout))
    assert report["old_path"], "probe.cli.backfill_evidence is the evidence door"
    assert report["before"] == [f"{_FOLDER_MODULE}.evidence"]
    assert report["after"] == [f"{_FOLDER_MODULE}.evidence", f"{_FOLDER_MODULE}.walk", f"{_FOLDER_MODULE}.walk.census"]


#: First read at once, these deadlocked in 7 of 25 interpreters before the door loaded one piece at
#: a time: flow/'s eager door reaches classify/plan, whose last import is flow/landed.
_RACING_NAMES = ("choose_agent", "count_landed", "slug_for", "codex_features")


def test_four_threads_reading_the_door_first_at_once_all_get_their_names() -> None:
    code = (
        "import json, sys, threading\n"
        f"import {_FOLDER_MODULE} as door\n"
        "names = json.loads(sys.argv[1]); start = threading.Barrier(len(names)); errors = []\n"
        "def read(name):\n"
        "    start.wait()\n"
        "    try:\n"
        "        getattr(door, name)\n"
        "    except Exception as exc:  # reported below\n"
        "        errors.append(f'{name}: {type(exc).__name__}: {exc}')\n"
        "threads = [threading.Thread(target=read, args=(name,)) for name in names]\n"
        "for thread in threads:\n    thread.start()\n"
        "for thread in threads:\n    thread.join(60)\n"
        "assert not any(thread.is_alive() for thread in threads), 'a reader hung'\n"
        "print(json.dumps(errors))\n"
    )
    with ThreadPoolExecutor(4) as pool:
        results = list(pool.map(lambda _: _python(code, json.dumps(_RACING_NAMES)), range(8)))
    assert [r.returncode for r in results] == [0] * len(results), [r.stderr for r in results if r.returncode]
    assert [json.loads(_last_line(r.stdout)) for r in results] == [[]] * len(results)


#: A budget, not a target: 42 probe modules today, 38 before agent:14, 263 through the eager door.
_RECORD_CALL_MODULES = 60


def test_a_record_sessions_probe_loads_none_of_the_importer(tmp_path) -> None:
    """Every `probe` the record session's agent runs is a fresh process (record/tool.launcher_script)."""
    from probe.cli.imports.folder.record import tool

    work = tmp_path / "work"
    work.mkdir()
    listing = tmp_path / "listing.json"
    listing.write_text(json.dumps({
        "session": "s1", "folder": str(tmp_path), "writes": {"project": True, "experiments": True, "runs": True},
        "project": {"id": "p1", "slug": "p", "name": "P", "locked": [], "page": {"version": 1, "draft": ""}},
        "experiments": [], "runs": [{"id": "r1", "folder": "sweep/run-a", "slug": "run-a", "name": "run-a",
                                     "experiment": None, "locked": [], "import_notes": []}],
    }))
    launcher = tmp_path / "probe"
    launcher.write_text(tool.launcher_script(listing, work))
    launcher.chmod(0o700)
    # -X importtime's switch: the launcher's own command line, untouched, names every module it imports.
    env = {**os.environ, "PYTHONPROFILEIMPORTTIME": "1"}
    result = subprocess.run([str(launcher), "run", "list"], cwd=work, env=env, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0 and "sweep/run-a" in result.stdout, result.stderr[-2000:]
    loaded = {line.rsplit("|", 1)[-1].strip() for line in result.stderr.splitlines() if line.startswith("import time:")}
    probe_modules = {name for name in loaded if name == "probe" or name.startswith("probe.")}
    importer = sorted(name for name in probe_modules if name.startswith(f"{_FOLDER_MODULE}.")
                      and not name.startswith(f"{_FOLDER_MODULE}.record"))
    assert importer == []
    assert len(probe_modules) <= _RECORD_CALL_MODULES, sorted(probe_modules)
