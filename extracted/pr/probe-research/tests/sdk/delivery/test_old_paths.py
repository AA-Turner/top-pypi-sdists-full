"""Old delivery paths (each IS its door) keep working: every served name resolves, `import *` takes
the old public names, and `python -m probe.sdk.outbox_worker` survives `-W error` (agent:7)."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys

import pytest

DOORS = (
    "probe.sdk.client",
    "probe.sdk.fluent",
    "probe.sdk.run",
    "probe.sdk.delivery.journal",
    "probe.sdk.delivery.offline",
    "probe.sdk.delivery.outbox",
    "probe.sdk.delivery.transport",
)


def _entries():
    for door in DOORS:
        for name, home in importlib.import_module(door)._HOMES.items():
            yield pytest.param(door, name, home, id=f"{door.rsplit('.', 1)[-1]}.{name}")


@pytest.mark.parametrize(("door", "name", "home"), list(_entries()))
def test_every_name_a_door_serves_resolves_to_its_home(door: str, name: str, home: str) -> None:
    # A piece module named like a served name shadows it (`transport/errors.py` hid `errors`).
    piece = importlib.import_module(home)
    assert hasattr(piece, name), f"{home} no longer binds {name}"
    assert getattr(importlib.import_module(door), name) is getattr(piece, name)


def test_the_transport_door_serves_the_sdk_errors_module() -> None:
    import probe.sdk.delivery.transport
    import probe.sdk.errors

    assert probe.sdk.delivery.transport.errors is probe.sdk.errors


@pytest.mark.parametrize("door", DOORS)
def test_a_star_import_of_a_door_takes_every_public_name(door: str) -> None:
    # Each old path (probe.sdk.journal, ...) IS its door, aliased in sys.modules.
    namespace: dict = {}
    exec(f"from {door} import *", namespace)
    public = {name for name in importlib.import_module(door)._HOMES if not name.startswith("_")}
    assert public <= namespace.keys()


def test_the_old_worker_entry_runs_when_runtime_warnings_are_errors(tmp_path) -> None:
    """Spawned workers inherit PYTHONWARNINGS; runpy re-running a loaded piece warned, so died."""
    outbox = tmp_path / "outbox"
    outbox.mkdir()
    ran = subprocess.run(
        [sys.executable, "-W", "error::RuntimeWarning", "-m", "probe.sdk.outbox_worker", "--rescue", str(outbox)],
        env={**os.environ, "HOME": str(tmp_path / "home")}, capture_output=True, text=True, timeout=60)
    assert ran.returncode == 0, ran.stderr
    assert "RuntimeWarning" not in ran.stderr


def test_the_client_loads_the_request_log_with_itself() -> None:
    """Transport no longer imports diagnostics, so the client must, or it is first imported at
    exit (an uncaught Ctrl-C then exits 1, tests/test_ctrlc_exit_code.py)."""
    ran = subprocess.run(
        [sys.executable, "-c", "import sys, probe.sdk.client; print('probe.sdk.diagnostics' in sys.modules)"],
        capture_output=True, text=True, timeout=60)
    assert ran.stdout.strip() == "True", ran.stderr
