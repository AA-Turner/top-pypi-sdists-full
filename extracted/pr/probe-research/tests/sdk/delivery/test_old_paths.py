"""Delivery doors keep the old modules' names: every served name resolves, `import *` takes the
old public names, and `python -m probe.sdk.outbox_worker` survives `-W error` (agent:7)."""

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
    # A door stands in for the single-file module it replaced, so it serves that module's public names.
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


#: Old module path -> {name: (new module, name)}: kept one release when a sink moved (queued sink).
SHIMS = {
    "probe.sdk.delivery.sinks.journaled": {
        "JournalSink": ("probe.sdk.delivery.sinks.queued", "QueuedSink"),
        "_usable_journal": ("probe.sdk.delivery.sinks.queued", "_usable_journal"),
        "queue_only": ("probe.sdk.delivery.sender", "queue_only"),
        # Everything else the old module served is forwarded to its new home.
        "is_queue_only": ("probe.sdk.delivery.sinks.queued", "is_queue_only"),
        "HeldClient": ("probe.sdk.delivery.sinks.queued", "HeldClient"),
        "_FALLBACK_WARNED": ("probe.sdk.delivery.sinks.queued", "_FALLBACK_WARNED"),
    },
    "probe.sdk.delivery.sinks.offline": {
        "OfflineClient": ("probe.sdk.delivery.offline.client", "OfflineClient"),
        "OfflineTransport": ("probe.sdk.delivery.offline.client", "OfflineTransport"),
        "LINEAGE_ROUTES": ("probe.sdk.delivery.offline.lineage", "LINEAGE_ROUTES"),
        "JournalSink": ("probe.sdk.delivery.sinks.queued", "QueuedSink"),
        "SinkKind": ("probe.sdk.delivery.sink", "SinkKind"),
        "Client": ("probe.sdk.delivery.offline.client", "Client"),
        "Settings": ("probe.sdk.delivery.offline.client", "Settings"),
    },
}


@pytest.mark.parametrize("shim", sorted(SHIMS))
def test_a_moved_sink_path_serves_the_same_objects_for_one_release(shim: str) -> None:
    # importlib, not an import statement: the A9 guard counts first-party imports of a shim.
    old = importlib.import_module(shim)
    for name, (home, new_name) in SHIMS[shim].items():
        assert getattr(old, name) is getattr(importlib.import_module(home), new_name), f"{shim}.{name}"


def test_the_offline_sink_is_gone_rather_than_aliased() -> None:
    """Every async client uses QueuedSink, so an OfflineSink alias would read online runs as offline."""
    old = importlib.import_module(sorted(SHIMS)[1])  # probe.sdk.delivery.sinks.offline
    with pytest.raises(AttributeError):
        old.OfflineSink


@pytest.mark.parametrize("first", [
    "probe.sdk.delivery.offline.client",
    "probe.sdk.delivery.offline.lineage",
    "probe.sdk.delivery.offline.sync",
    "probe.sdk.delivery.offline.offline",
    "probe.sdk.delivery.sinks.offline",
    "probe.sdk.delivery.sinks.journaled",
])
def test_every_offline_piece_imports_first_in_a_fresh_interpreter(first: str) -> None:
    """The offline door loads its pieces in order; whichever one a caller imports first, none may
    meet another half-loaded (the client moved inside the door with the queued sink)."""
    code = (f"import {first}; from probe.sdk.delivery.offline import OfflineClient, LINEAGE_ROUTES; "
            "print(sorted(LINEAGE_ROUTES), OfflineClient.__module__)")
    ran = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=60)
    assert ran.returncode == 0, ran.stderr
    assert ran.stdout.split() == ["['run_inputs',", "'run_outputs']", "probe.sdk.delivery.offline.client"]
