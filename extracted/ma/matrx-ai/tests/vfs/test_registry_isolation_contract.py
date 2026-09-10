"""The command registry is a process global — emptying it must be recoverable.

THE INCIDENT (2026-09-09). ``tests/vfs/test_command_base.py`` used a fixture
whose teardown called ``registry.clear()``. Because ``@register`` fires at
command-module IMPORT time, a second ``import_module`` is a no-op, so nothing
could ever refill the registry: every test that ran after that module found ZERO
virtual commands and failed for reasons that had nothing to do with it. Running
``pytest packages/matrx-ai/tests`` in reverse collection order was 557 red /
3723 green against the identical, correct code — the classic "fails in the
suite, passes alone" shape, and a real defect rather than a test-ordering quirk.

Two mechanisms close it, and each is pinned here:

  1. ``registry.isolated()`` — a temporary empty registry that ALWAYS restores.
     Anything that needs emptiness for a moment uses this, never a bare
     ``clear()``.
  2. ``load_all()`` actually reloads after a ``clear()``, so the public entry
     point means what its name says instead of silently doing nothing.

Gut check: revert either one and the matching test here fails.
"""

from __future__ import annotations

from matrx_ai.tools.vfs.commands import load_all
from matrx_ai.tools.vfs.commands.registry import (
    all_names,
    clear,
    is_registered,
    isolated,
    register,
)


def test_isolated_gives_an_empty_registry_and_puts_the_real_one_back():
    load_all()
    before = all_names()
    assert "cat" in before, "precondition: the real commands are registered"

    with isolated():
        assert all_names() == [], "isolated() must hand over an EMPTY registry"

        @register("only-inside")
        async def _tmp(ctx):  # pragma: no cover - never invoked
            return None

        assert all_names() == ["only-inside"]

    assert all_names() == before, (
        "isolated() leaked: the process-global registry did not come back. "
        "Every consumer that runs after this point now has no commands."
    )


def test_isolated_restores_even_when_the_block_raises():
    load_all()
    before = all_names()

    class _Boom(Exception):
        pass

    try:
        with isolated():
            raise _Boom
    except _Boom:
        pass

    assert all_names() == before


def test_load_all_refills_a_cleared_registry():
    """``clear()`` must not be a one-way door for the rest of the process."""
    load_all()
    assert is_registered("cat")

    clear()
    assert not is_registered("cat"), "precondition: the registry really is empty"

    load_all()
    assert is_registered("cat"), (
        "load_all() did not refill a cleared registry — the command modules are "
        "already in sys.modules, so importing them again registers nothing. It "
        "must RELOAD them."
    )
    assert len(all_names()) > 40, "the whole command set must come back, not one entry"
