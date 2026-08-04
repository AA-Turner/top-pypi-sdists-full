"""Playwright async-specific wiring.

Heal flow on Locator action timeout (inside testmu.step):
  Autoheal API → fresh selector → retry the same method on a fresh
  page.locator. Capped retry timeout (5s) so a bad heal fails fast.
  Writes the remap into the per-step cache so subsequent actions on
  the same stale locator skip the API entirely.

  On miss (autoheal returned None or the retry on the fresh locator
  also failed), we write a None sentinel into the cache and return
  False. The wrapper then re-raises the original Playwright
  TimeoutError so the user sees PW's real call-log diagnostic.
"""
import logging

from testmu import _config
from testmu._heal_cache import get_cache
from testmu._heal_patch import install, _in_heal

_log = logging.getLogger("testmu")

HEAL_METHODS = [
    "click", "dblclick", "fill", "type", "press",
    "hover", "check", "uncheck", "select_option",
    "set_input_files", "scroll_into_view_if_needed",
    "focus", "tap", "drag_to",
]

# Maps Playwright Locator method → autoheal API action_type enum
# (click | select | type | scroll). Methods omitted skip heal entirely;
# today that's `focus` and `drag_to` since the API has no slot for them.
_METHOD_TO_ACTION_TYPE = {
    "click": "click", "dblclick": "click", "tap": "click",
    "hover": "click", "check": "click", "uncheck": "click",
    "fill": "type", "type": "type", "press": "type", "set_input_files": "type",
    "select_option": "select",
    "scroll_into_view_if_needed": "scroll",
}

_RETRY_TIMEOUT_CAP_MS = 5_000
_DEFAULT_TIMEOUT_MS = 30_000

# Warn once (not per-action) when auto_heal_version is configured to a
# non-empty value that isn't the recognized "AH2" — most likely a typo that
# would otherwise silently fall back to the legacy heal with no signal.
_ah_version_warned = False


def _capped_retry_kwargs(kwargs):
    """Cap explicit timeout so a misidentified fresh selector fails fast."""
    orig = kwargs.get("timeout")
    capped = min(orig if orig is not None else _DEFAULT_TIMEOUT_MS, _RETRY_TIMEOUT_CAP_MS)
    return {**kwargs, "timeout": capped}


async def _default_heal(page, description, method_name, original_locator, *args, **kwargs):
    if not _config.smart:
        return False

    cache = get_cache()
    action_type = _METHOD_TO_ACTION_TYPE.get(method_name)
    if action_type is None:
        # method has no autoheal mapping (focus, drag_to) — nothing to try.
        return False

    # AH2 gate is a GLOBAL binding config (mirror kane_version), not per-step:
    # set once via configure(auto_heal_version="AH2"), read here via _configure.get.
    from testmu import _configure
    global _ah_version_warned
    ah_version = _configure.get("auto_heal_version", "")
    use_ax = ah_version == "AH2"
    if ah_version and not use_ax and not _ah_version_warned:
        _log.warning("[heal] unrecognized auto_heal_version=%r — using legacy heal", ah_version)
        _ah_version_warned = True
    try:
        if use_ax:
            from testmu._helpers.autoheal_ax import run_locator_heal
            # NOTE: `_selector` is a private Playwright internal attribute — no
            # public API exposes the locator's original selector string. If a
            # Playwright upgrade renames/removes it, this degrades to "" (the
            # heal still runs, it just loses the re-anchor hint for the AH2
            # endpoint). test_ah2_extracts_previous_selector_from_real_locator
            # (test_heal_gate.py) asserts non-empty extraction against a REAL
            # page.locator(...), so a rename fails CI loudly instead of
            # silently dropping the hint.
            previous = getattr(getattr(original_locator, "_impl_obj", None), "_selector", "") or ""
            healed = await run_locator_heal(page, description, action_type, previous_selectors=previous)
        else:
            from testmu._helpers.autoheal import autoheal_locator
            healed = await autoheal_locator(page, description, action_type)
    except Exception as e:  # noqa: BLE001
        _log.warning("[heal] heal call raised (treating as miss): %s", e)
        healed = None

    if healed:
        selector = healed["locator"]
        if healed.get("locator_type") == "xpath":
            selector = f"xpath={selector}"

        # Frame-scoped heal: rebuild the frame chain (root→leaf) so an element
        # inside an iframe is retried in its own frame, not at the top level
        # (where a frame-relative selector cannot resolve).
        frame_chain = healed.get("frame_chain") or []
        root = page
        for fr in frame_chain:
            fsel = fr["locator"]
            if fr.get("locator_type") == "xpath":
                fsel = f"xpath={fsel}"
            root = root.frame_locator(fsel)

        # _in_heal makes the wrapped retry run the RAW method — no re-heal on
        # the fresh locator — so heal is exactly one attempt per failure.
        token = _in_heal.set(True)
        try:
            fresh = root.locator(selector)
            await getattr(fresh, method_name)(*args, **_capped_retry_kwargs(kwargs))
        except Exception as e:
            _log.warning(
                "[heal] retry on fresh locator %r failed: %s",
                selector, e,
            )
            # fall through to negative-cache write below
        else:
            # The per-step positive cache replays via page.locator(<selector>) —
            # top-level only, so it cannot carry frame scope. Cache main-frame
            # heals; re-heal a framed element each action (correctness > speed).
            if cache is not None and not frame_chain:
                try:
                    cache[original_locator] = selector
                except TypeError:
                    pass
            _log.info(
                "[heal] %s '%s' → fresh locator %s",
                method_name, description, selector[:80],
            )
            return True
        finally:
            _in_heal.reset(token)

    # Heal missed — write negative sentinel so subsequent actions on the
    # same locator skip the API and surface PW's real diagnostic.
    if cache is not None:
        try:
            cache[original_locator] = None
        except TypeError:
            pass

    return False


def _install_long_press(Locator):
    """Expose ``long_press`` as a METHOD on the native Playwright Locator.

    The code generator emits a selector-bound long press as
    ``await _loc_N.long_press(duration=...)`` — a method call on the materialised
    DOM-selector Locator, mirroring the selectorless ``VisionLocator.long_press``
    method. The native Playwright Locator has no such method, so attach one that
    delegates to the selector-bound ``testmu.long_press`` entry (validate → hover →
    mouse.down → hold → mouse.up; a templated ``variables=`` map passes through).
    Idempotent: a re-import won't re-wrap.
    """
    if getattr(Locator, "long_press", None) is not None:
        return

    async def long_press(self, *, duration, variables=None):
        from testmu._helpers.gesture import long_press as _gesture_long_press
        return await _gesture_long_press(self, duration=duration, variables=variables)

    long_press._testmu_gesture_method = True
    setattr(Locator, "long_press", long_press)


def _install_heal():
    try:
        from playwright.async_api import Locator
    except ModuleNotFoundError:
        _log.warning("playwright not installed — heal patch skipped, continuing without heal")
        return
    except ImportError as e:
        # playwright present but a transitive dep failed to load (e.g. greenlet DLL on Windows)
        _log.warning("playwright internals failed to load (%s) — heal patch skipped, continuing without heal", e)
        return
    try:
        install(Locator, HEAL_METHODS, _default_heal)
        _install_long_press(Locator)
        _log.debug("Heal patch installed on Locator")
    except Exception as e:
        _log.warning("heal patch installation failed (%s) — continuing without heal", e)


_install_heal()
