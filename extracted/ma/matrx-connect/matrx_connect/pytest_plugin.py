"""Test-isolation guards for the ambient ``AppContext`` ContextVar.

matrx-connect owns ``matrx_connect.context.app_context._app_context`` — a
process-global ContextVar — so it also owns the guard that stops one test from
leaking it into every test that runs after it.

This module is registered as a ``pytest11`` entry point, so pytest auto-loads it
in any environment where matrx-connect is installed, **regardless of rootdir**.
That is the whole point: several packages define their own
``[tool.pytest.ini_options]``, so running ``pytest packages/matrx-ai/tests``
makes that package the rootdir and the repo-root ``conftest.py`` is never
loaded. An entry-point plugin does not care where rootdir landed, and needs no
conftest edit and no new dependency in any consuming package.

Where matrx-connect is genuinely absent (a bare-venv standalone install of, say,
matrx-orm), so is the ContextVar — there is nothing to guard, and nothing loads.

Opt out for one run with ``-p no:matrx_app_context_guard``.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _no_leaked_app_context(request: pytest.FixtureRequest):
    """Fail any test that leaves an ambient ``AppContext`` in the ContextVar.

    Layer 2 of the ambient-AppContext contract. Layer 1 is each test cleaning up
    after itself (a ``try/finally`` or a yield-fixture around
    ``set_app_context``). This is the backstop that makes a violation impossible
    to miss: it FAILS the polluting test by name instead of silently cleaning
    up, because a leaked context is invisible where it leaks and only breaks
    some unrelated test that runs later (this exact leak broke three later tests
    in two other packages).

    Loud, self-identifying, and it names the fix. The context is restored
    afterwards so the rest of the session is not punished for one test.
    """
    try:
        from matrx_connect.context.app_context import _app_context
    except Exception:  # pragma: no cover — matrx_connect always importable here
        yield
        return

    before = _app_context.get(None)
    yield
    after = _app_context.get(None)

    if after is None or after is before:
        return

    _app_context.set(before)  # don't punish the rest of the session
    pytest.fail(
        "AMBIENT APPCONTEXT LEAKED BY THIS TEST.\n"
        f"  test:    {request.node.nodeid}\n"
        f"  user_id: {getattr(after, 'user_id', None)!r}\n"
        f"  emitter: {type(getattr(after, 'emitter', None)).__name__}\n"
        "  why it matters: the ContextVar is process-global, so every later\n"
        "    test in this session sees this context. Tests that assert 'no\n"
        "    ambient context' fail far away from the real cause.\n"
        "  how to fix: keep the token from set_app_context(...) and call\n"
        "    clear_app_context(token) in a finally block or fixture teardown.",
        pytrace=False,
    )
