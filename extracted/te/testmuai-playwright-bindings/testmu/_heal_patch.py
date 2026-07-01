"""Heal patch for Playwright Locator methods.

Installs wrappers on Locator action methods that catch TimeoutError
(element not found) and attempt heal via a pluggable heal function.

The patch only fires inside a testmu.step() block (ContextVar check).
Outside a step, the wrapper is a pure passthrough.

heal_fn contract:
    async def heal_fn(page, description, method_name, *args, **kwargs) -> bool

    Returns True if heal handled the action (wrapper returns normally).
    Returns False if heal couldn't help (wrapper re-raises original error).

    Today's default heal does a coordinate lookup via vision API and clicks
    at the returned coordinates for click/hover methods. Other methods are
    not supported until locator re-resolution lands.
"""
import contextvars
import functools
import logging
from testmu import _configure
from testmu._step import _current_step
from testmu._heal_cache import get_cache

_log = logging.getLogger("testmu")

# Re-entry guard for the action engine. Set by _run_verb (imported from here
# by the engine) for the duration of a heal-cascade call so the verb runners'
# own ``await locator.click(...)`` bypass this wrapper instead of recursing back
# into the engine. Default False — inert on the autoheal path.
_in_engine: contextvars.ContextVar = contextvars.ContextVar(
    "testmu_in_engine", default=False
)

# Resolve Playwright's errors once at import time.
#
# `playwright.async_api.TimeoutError` (a subclass of Playwright's internal
# Error, NOT of Python's built-in TimeoutError) is raised when a Locator
# action's auto-wait expires — the element isn't there. We catch both the
# PW and built-in variants so unit tests using the built-in keep working.
#
# A *strict-mode violation* is the opposite problem: the selector matches
# MORE than one element. Playwright raises it as a plain
# `playwright.async_api.Error` (not a TimeoutError) with "strict mode
# violation" in the message. We heal it too — the heal path disambiguates
# the match — but it needs separate handling because, unlike a timeout,
# the element(s) DO exist (count() > 0 is the whole problem).
try:
    from playwright.async_api import (
        TimeoutError as _PWTimeoutError,
        Error as _PWError,
    )
    _TIMEOUT_EXCS: tuple = (_PWTimeoutError, TimeoutError)
    # Broadest net we act on: timeouts plus any PW Error (which we then
    # filter down to strict-mode violations before healing).
    _HEAL_EXCS: tuple = (_PWTimeoutError, TimeoutError, _PWError)
except ImportError:
    _TIMEOUT_EXCS = (TimeoutError,)
    _HEAL_EXCS = (TimeoutError,)


def _is_strict_mode_violation(exc) -> bool:
    """A Playwright strict-mode violation is a plain Error whose message
    names the condition. We match on the message rather than a dedicated
    exception type because Playwright doesn't expose one."""
    return "strict mode violation" in str(exc).lower()

_originals = {}


async def _capture_element_bounds(locator, step):
    """Ship element rect before an action (cloud only, best-effort)."""
    try:
        from testmu import _config
        if _config.run_target != "cloud":
            return
        bbox = await locator.bounding_box(timeout=2000)
        if bbox is None:
            return
        from testmu._reporter import reporter
        await reporter().send_element_bounds(
            bbox, getattr(step, "instruction_id", None)
        )
    except Exception as e:
        _log.debug(f"[bounds] capture skipped: {e}")


def install(target_class, method_names, heal_fn):
    """Patch methods on target_class with heal-on-failure behavior.

    Skips methods missing from the class and methods already wrapped.
    Each method's install is independent — one failure doesn't stop the rest.
    """
    for name in method_names:
        try:
            original = getattr(target_class, name, None)
            if original is None:
                _log.debug("heal patch: %s.%s not present, skipping", target_class.__name__, name)
                continue
            if getattr(original, "_testmu_heal_wrapped", False):
                continue  # idempotent — re-import won't double-wrap
            wrapper = _make_wrapper(name, original, heal_fn)
            wrapper._testmu_heal_wrapped = True
            _originals[(target_class, name)] = original
            setattr(target_class, name, wrapper)
        except Exception as e:
            _log.warning("heal patch: failed to wrap %s.%s (%s) — skipping", target_class.__name__, name, e)


def uninstall(target_class, method_names):
    """Restore original methods."""
    for name in method_names:
        key = (target_class, name)
        original = _originals.pop(key, None)
        if original is not None:
            setattr(target_class, name, original)


def _make_wrapper(name, original, heal_fn):
    @functools.wraps(original)
    async def wrapper(self, *args, **kwargs):
        # Pop fallback_coordinates unconditionally at the patch boundary — it
        # is a testmu-level kwarg consumed only by _run_verb (V3 path), never
        # by the raw Playwright method. Popping before ANY early return keeps
        # it from leaking into e.g. locator.click(**kw) on the passthrough
        # paths (unregistered verb, _in_engine, no step, v4 default).
        fallback_coordinates = kwargs.pop("fallback_coordinates", None)

        # Re-entry short-circuit: the action engine calls back into
        # ``locator.click(...)`` via its verb runners. Without this guard the
        # wrapper would dispatch into the engine again → RecursionError. Inert
        # on the autoheal path (default False).
        if _in_engine.get():
            return await original(self, *args, **kwargs)

        step = _current_step.get()
        if step is None:
            return await original(self, *args, **kwargs)

        # Version-gated path — delegate the whole try → cascade → retry loop to the action
        # engine. Gated strictly on kane_version == "v3"; the default ("v4")
        # falls through to the autoheal cache/heal_fn path below, unchanged.
        if _configure.get("kane_version") == "v3":
            from testmu._action_specs import get_verb_spec
            from testmu._action_engine import _run_verb
            verb_spec = get_verb_spec(name)
            if verb_spec is None:
                # Method not in the verb registry — fall back to original.
                return await original(self, *args, **kwargs)
            return await _run_verb(
                self.page, self, verb_spec, *args,
                description=step.description, verb_name=name,
                fallback_coordinates=fallback_coordinates, **kwargs,
            )

        # Cache fast-path: this locator was already remapped in this step.
        cache = get_cache()
        if cache is not None:
            try:
                cached = cache.get(self)
            except TypeError:
                cached = None  # locator class lacks weakref support
            if cached is not None:
                # Positive entry: skip stale, run on fresh.
                fresh = self.page.locator(cached)
                return await original(fresh, *args, **kwargs)
            elif self in cache:
                # Negative entry: heal already missed for this locator. Run
                # the original so the user sees PW's real diagnostic.
                return await original(self, *args, **kwargs)

        await _capture_element_bounds(self, step)

        try:
            return await original(self, *args, **kwargs)
        except _HEAL_EXCS as exc:
            strict = _is_strict_mode_violation(exc)
            # Only act on timeouts (element missing) and strict-mode
            # violations (element ambiguous). Any other Playwright Error
            # isn't ours to heal — let it propagate untouched.
            if not strict and not isinstance(exc, _TIMEOUT_EXCS):
                raise
            # Timeout with the element present means "there but not
            # actionable" — heal can't help, so re-raise. For a strict-mode
            # violation count() > 0 is expected (that's the violation), so
            # skip the guard and let heal disambiguate.
            if not strict and await self.count() > 0:
                raise
            handled = await heal_fn(
                self.page, step.description, name, self, *args, **kwargs
            )
            if not handled:
                raise

    return wrapper
