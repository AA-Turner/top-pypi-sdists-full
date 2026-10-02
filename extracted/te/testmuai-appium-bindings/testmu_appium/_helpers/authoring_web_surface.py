"""One-action handoff for a mobile-web surface captured by the authoring host.

Generated replay has no such handoff and follows the binding's ordinary fresh
capture path.  V16 authoring, however, has just read and calibrated the same web
surface while grounding the action target.  Carrying that in memory avoids
settling and calibrating the screen a second time before the immediately following
verb.  A context variable keeps concurrent sessions isolated and makes the value
one execution-scope concern rather than process-global state.
"""
from contextlib import contextmanager
from contextvars import ContextVar


_authoring_web_surface = ContextVar(
    "testmu_appium_authoring_web_surface", default=None,
)


@contextmanager
def use_authoring_web_surface(surface):
    """Make ``surface`` available to one generated action execution."""
    token = _authoring_web_surface.set(surface)
    try:
        yield
    finally:
        _authoring_web_surface.reset(token)


def current_authoring_web_surface():
    """Inspect the live-only prepared surface for the current execution."""
    return _authoring_web_surface.get()


def consume_authoring_web_surface():
    """Take the prepared surface once, including across a guarded retry."""
    surface = _authoring_web_surface.get()
    _authoring_web_surface.set(None)
    return surface
