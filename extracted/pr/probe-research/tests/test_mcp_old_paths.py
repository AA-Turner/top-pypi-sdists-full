"""Old MCP paths keep working after the agent:17 split: each door serves every name its old module
had, a patch through it reaches every piece, and each moved module answers at its old path."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys

import pytest

#: Old module -> its door (each split module IS its door now, or a shim aliased to it).
DOORS = {
    "probe.mcp.server": "probe.mcp.server",
    "probe.mcp.service": "probe.mcp.tools",
    "probe.mcp.source": "probe.mcp.source",
}
#: Modules moved whole -> where they live now (the old path is a shim aliased in sys.modules).
MOVED = {
    "probe.mcp.accounting": "probe.mcp.delivery.accounting",
    "probe.mcp.branches": "probe.mcp.tools.views.branch_projection",
    "probe.mcp.browse_delivery": "probe.mcp.delivery.browse",
    "probe.mcp.continuation": "probe.mcp.delivery.delivery",
    "probe.mcp.delivery_context": "probe.mcp.delivery.context",
}


def _entries():
    for old, door in DOORS.items():
        for name, home in importlib.import_module(door)._HOMES.items():
            yield pytest.param(old, name, home, id=f"{old.rsplit('.', 1)[-1]}.{name}")


@pytest.mark.parametrize(("old", "name", "home"), list(_entries()))
def test_every_name_an_old_path_had_resolves_to_its_piece(old: str, name: str, home: str) -> None:
    piece = importlib.import_module(home)
    assert hasattr(piece, name), f"{home} no longer binds {name}"
    assert getattr(importlib.import_module(old), name) is getattr(piece, name)


@pytest.mark.parametrize("old", sorted(MOVED))
def test_a_moved_module_answers_at_its_old_path(old: str) -> None:
    assert importlib.import_module(old) is importlib.import_module(MOVED[old])


def test_a_patch_through_the_server_door_reaches_every_piece_that_reads_it(monkeypatch) -> None:
    import probe.mcp.server as server
    from probe.mcp.server import limits, tool_runner

    monkeypatch.setattr(server, "_QUEUE_TIMEOUT_S", 0.25)
    assert limits._QUEUE_TIMEOUT_S == tool_runner._QUEUE_TIMEOUT_S == 0.25


def test_a_patch_through_the_old_service_path_reaches_the_view_builders(monkeypatch) -> None:
    import probe.mcp.service as service  # restructure-guard-ok: the old path is what this test pins
    from probe.mcp.tools import entity
    from probe.mcp.tools.views import files, runs

    monkeypatch.setattr(service, "_PAGE_FETCH", 3)
    assert files._PAGE_FETCH == entity._PAGE_FETCH == runs._PAGE_FETCH == 3


def test_the_read_service_is_one_class_as_before() -> None:
    from probe.mcp import ResearchOSSource, ResearchReadService

    # compose() folds the mixins back: no bases, every member in the class's own namespace.
    assert ResearchReadService.__bases__ == (object,)
    assert ResearchOSSource.__bases__ == (object,)
    assert "browse_list" in vars(ResearchReadService) and "search" in vars(ResearchOSSource)


def test_the_server_door_keeps_the_dunder_name_the_old_module_imported() -> None:
    import probe
    import probe.mcp.server as server

    assert server.__version__ == probe.__version__  # `from .. import __version__` in the old server.py


def test_the_old_logger_names_are_kept() -> None:
    from probe.mcp.delivery import accounting
    from probe.mcp.server import pool

    # Log filters and dashboards match these names; the split must not rename them.
    assert pool._logger.name == "probe.mcp.server"
    assert accounting._logger.name == "probe.mcp.accounting"


def test_python_m_probe_mcp_server_still_runs_the_stdio_server(tmp_path) -> None:
    """The old module ended in `if __name__ == "__main__": main()`; the package keeps that entry."""
    ran = subprocess.run(
        [sys.executable, "-W", "error", "-m", "probe.mcp.server"], stdin=subprocess.DEVNULL,
        env={**os.environ, "HOME": str(tmp_path)}, capture_output=True, text=True, timeout=60)
    assert ran.returncode == 0, ran.stderr
