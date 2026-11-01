"""Pins the public SDK surface (names, kinds, signatures, members) and every module path that must import.

`sdk_modules.json` only grows on a refresh (UPDATE=1): a path leaves it by hand, never by a move without a shim.
"""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import probe
import probe.sdk
from tests.safety_net.sdk.api_surface import describe
from tests.safety_net.sdk.framework_fakes import frameworks
from tests.test_import_every_module import OPTIONAL

UPDATE = os.environ.get("PROBE_SAFETY_NET_UPDATE") == "1"
SRC = Path(probe.__file__).resolve().parent
MODULES = Path(__file__).resolve().parent / "baselines" / "sdk_modules.json"
CHUNK = 60
#: Integration entry points a customer imports by these exact paths.
ENTRY_MODULES = (
    "probe.integrations",
    "probe.integrations.miles",
    "probe.connectors.miles",
    "probe.integrations.huggingface",
    "probe.integrations.lightning",
)
_ENTRY_NAMES = {
    "probe.integrations.huggingface": ["ProbeCallback"],
    "probe.integrations.lightning": ["ProbeLogger"],
}


def _public_names(module) -> list[str]:
    return sorted(set(getattr(module, "__all__", [])) | set(getattr(module, "_LAZY", [])))


def _surface() -> dict:
    """{"access": public path -> canonical path, "objects": canonical path -> description}."""
    access: dict[str, str] = {}
    objects: dict[str, dict] = {}
    seen: dict[int, str] = {}

    def add(path: str, value) -> None:
        canonical = seen.setdefault(id(value), path) if not _is_literal(value) else path
        access[path] = canonical
        if canonical == path:
            objects[path] = describe(value, path.rsplit(".", 1)[1])

    for module in (probe, probe.sdk):
        for name in _public_names(module):
            add(f"{module.__name__}.{name}", _resolve(module, name))
    for module_name in ENTRY_MODULES:
        module = importlib.import_module(module_name)
        for name in _ENTRY_NAMES.get(module_name) or _public_names(module):
            add(f"{module_name}.{name}", _resolve(module, name))
    return {"access": access, "objects": objects}


class _Unresolved(str):
    """A public name that no longer resolves: pinned as such, so the diff names it."""


def _resolve(module, name: str):
    try:
        return getattr(module, name)
    except Exception as exc:  # noqa: BLE001 -- a lazy name whose import broke
        return _Unresolved(f"UNRESOLVED {type(exc).__name__}: {exc}")


def _is_literal(value) -> bool:
    return isinstance(value, (str, int, float, bool, type(None)))


def test_public_sdk_names_kinds_and_signatures(monkeypatch, baseline):
    with frameworks(monkeypatch):
        surface = _surface()
    baseline("sdk_api", surface)


def _modules_on_disk() -> list[str]:
    found = []
    for path in SRC.rglob("*.py"):
        parts = path.relative_to(SRC.parent).with_suffix("").parts
        if "__pycache__" in parts:
            continue
        found.append(".".join(parts[:-1] if parts[-1] == "__init__" else parts))
    return sorted(found)


def test_module_list_keeps_every_recorded_path():
    """Refresh (UPDATE=1) unions today's modules into the list; it never removes one."""
    recorded = json.loads(MODULES.read_text(encoding="utf-8")) if MODULES.exists() else []
    if UPDATE:
        merged = sorted(set(recorded) | set(_modules_on_disk()))
        if merged != recorded:
            MODULES.parent.mkdir(parents=True, exist_ok=True)
            MODULES.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
        return
    assert recorded, f"no {MODULES}; record it with PROBE_SAFETY_NET_UPDATE=1"


_IMPORT = r"""
import importlib, importlib.util, json, sys, warnings
warnings.simplefilter("ignore")
failures = []
for name in json.loads(sys.argv[1]):
    try:
        if name.rsplit(".", 1)[-1] == "__main__":
            # Importing a __main__ runs it: the path must resolve, nothing more.
            if importlib.util.find_spec(name) is None:
                raise ModuleNotFoundError(f"No module named {name!r}", name=name)
        else:
            importlib.import_module(name)
    except BaseException as exc:
        failures.append([name, type(exc).__name__, getattr(exc, "name", None), str(exc)[:300]])
print(json.dumps(failures))
"""


def _broken(failure: list) -> bool:
    _, kind, missing, _ = failure
    optional = kind in ("ModuleNotFoundError", "ImportError") and (missing or "").split(".")[0] in OPTIONAL
    return not optional


def test_every_recorded_module_path_still_imports(tmp_path):
    names = json.loads(MODULES.read_text(encoding="utf-8"))
    env = {**os.environ, "TMPDIR": str(tmp_path)}
    broken = []
    for start in range(0, len(names), CHUNK):
        chunk = names[start : start + CHUNK]
        done = subprocess.run(
            [sys.executable, "-c", _IMPORT, json.dumps(chunk)],
            capture_output=True, text=True, timeout=300, env=env, cwd=tmp_path,
        )
        assert done.returncode == 0, done.stderr[-2000:]
        broken += [f for f in json.loads(done.stdout.strip().splitlines()[-1]) if _broken(f)]
    assert broken == [], "recorded module paths that no longer import:\n" + "\n".join(map(str, broken))
