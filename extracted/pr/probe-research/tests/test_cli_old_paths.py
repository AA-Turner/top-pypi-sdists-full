"""cli/'s old module paths keep working after the agent:14 split: no old path hides behind a folder
of the same name, `probe.cli.capture` still serves the old module's names, and the pieces
cli/main.py defers register no command (the suite preloads them; production never does)."""

from __future__ import annotations

import importlib
import json
import subprocess
import sys
from pathlib import Path

import probe

_SRC = Path(probe.__file__).resolve().parent


def test_no_module_is_hidden_by_a_package_of_the_same_name() -> None:
    """`x/` beside `x.py`: `import x` finds the package, so `x.py` (an old-path shim) never runs."""
    hidden = [
        str(module.relative_to(_SRC))
        for module in _SRC.rglob("*.py")
        if "__pycache__" not in module.parts and (module.with_suffix("") / "__init__.py").exists()
    ]
    assert hidden == []


def test_the_old_capture_module_path_serves_its_names_without_loading_it_for_state() -> None:
    code = (
        "import sys\n"
        "import probe.cli.capture.state\n"
        "assert 'probe.cli.capture.capture' not in sys.modules, 'state.py never needed capture.py'\n"
        "from probe.cli.capture import OffMode, turn_off\n"
        "import probe.cli.capture as old, probe.cli.capture.capture as new\n"
        "assert old.OffMode is new.OffMode and old.turn_off is new.turn_off\n"
        "assert old._looks_like_the_uploader is new._looks_like_the_uploader\n"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr


def test_the_pieces_cli_main_defers_stay_unloaded_and_register_no_command() -> None:
    code = (
        "import importlib, json, sys\n"
        "from typer.main import get_command\n"
        "import probe.cli.main\n"
        "main = sys.modules['probe.cli.main']  # the package keeps `probe.cli.main` the function\n"
        "def tree(command, path=()):\n"
        "    rows = [' '.join(path)]\n"
        "    for name, sub in sorted(getattr(command, 'commands', {}).items()):\n"
        "        rows += tree(sub, (*path, name))\n"
        "    return rows\n"
        "loaded = sorted(set(main._DEFERRED) & set(sys.modules))\n"
        "before = tree(get_command(main.app))\n"
        "for piece in main._DEFERRED:\n"
        "    importlib.import_module(piece)\n"
        "print(json.dumps({'loaded': loaded, 'same': before == tree(get_command(main.app)), 'n': len(before)}))\n"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout.strip().splitlines()[-1])
    assert report["loaded"] == [], "probe's start loads none of the deferred pieces"
    assert report["same"] and report["n"] > 300, report


def test_every_deferred_piece_imports_on_its_own_after_the_door() -> None:
    """A command imports one deferred piece inside a function, after cli/main.py has loaded."""
    main = importlib.import_module("probe.cli.main")
    for piece in main._DEFERRED:
        assert importlib.import_module(piece).__name__ == piece
