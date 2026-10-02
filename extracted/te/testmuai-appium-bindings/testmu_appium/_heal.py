"""Autoheal client — v16-server /api/v1/autoheal, with typed outcomes.

Runs when element-mode strategy lookup is exhausted inside an active step. Nothing
else calls this — stale elements re-find, blocked elements retry, and driver-mode
verbs never had a locator to lose.

Flow:
  fresh perception (page source → flat entries + retained descriptors)
  → POST {action_instruction, action_type, full_dom_list, screenshot_b64}
  → dom_index → the RETAINED descriptor for that index
  → compile a fresh strict lookup and require exactly one live match.

The last step is the load-bearing one: parsed entries are static dictionaries, never
actable handles, and no element is cached across the HTTP call. The server's answer
identifies WHICH element; the binding still has to go and find it.

Outcomes are typed because their consequences differ:
  HealHit           → act on the re-found element
  HealNoMatch       → authoritative; the caller may cache the negative sentinel.
                      Native actions may unlock their gated coordinate fallback;
                      web actions never do. ONLY a 404 produces this.
  HealUnresolved    → the server answered, but the LOCAL re-find of its answer resolved
                      to zero or several live elements. Not authoritative: no 404 was
                      received, and a screen that moved between the perception snapshot
                      and the re-find explains the miss just as well as absence does.
                      NOT cached, does NOT unlock coordinates, one fresh-perception
                      retry allowed.
  HealUnavailable   → transport/5xx/timeout; NOT authoritative, NOT cached — the next
                      attempt in the same step should be allowed to try again
  HealDisabled      → the caller explicitly disabled autoheal with TESTMU_HEAL;
                      execute only point-grounded recorded coordinates
  HealProtocolError → malformed body; same non-authoritative treatment

The per-step cache lives here (it is heal state) but is written by the engine: only
the engine knows which selector set an attempt belonged to.
"""
import json
import logging
import time
from dataclasses import dataclass
from typing import Any, Optional

import httpx

from testmu_appium import _config
from testmu_appium._helpers._http import auth, headers, request_with_retry
from testmu_appium._helpers._perception import capture_perception
from testmu_appium._helpers._strategy import compile_descriptor, disambiguate_by_centre
from testmu_appium._step import current_step, get_heal_cache

_log = logging.getLogger("testmu_appium")

#: Action types the server's autoheal model is trained on. Anything else is either a
#: driver-mode verb or falls through to coordinates — it must not reach the endpoint.
VALID_ACTION_TYPES = frozenset({"click", "type", "select", "scroll"})

HEAL_SOURCE = "v16-autoheal"

#: Distinguishes "no cache entry" from the negative sentinel `None`.
CACHE_ABSENT = object()

#: Used when `heal_timeout_ms` is absent or non-positive.
_DEFAULT_HEAL_TIMEOUT_S = 60


@dataclass
class HealHit:
    """The server resolved the target and the binding re-found exactly one live match."""

    element: Any
    by: str
    value: str
    dom_index: int
    reasoning: str = ""
    descriptor: Optional[dict] = None
    source: str = HEAL_SOURCE


@dataclass
class WebHealHit:
    """The server selected one private DOM descriptor.

    The engine must resolve it against a fresh web capture before acting; no DOM
    row or geometry from the HTTP round trip is actable.
    """

    descriptor: dict
    dom_index: int
    reasoning: str = ""
    source: str = HEAL_SOURCE


@dataclass
class _HealSelection:
    descriptor: dict
    dom_index: int
    reasoning: str = ""


@dataclass
class HealNoMatch:
    """Authoritative miss: the element is not on this screen (or is not uniquely
    identifiable on it). Cacheable; unlocks coordinate fallback."""

    reason: str
    authoritative: bool = True


@dataclass
class HealUnresolved:
    """The server named an element; the binding could not turn that into one live match.

    Deliberately NOT a HealNoMatch. Only the server can say the element is gone, and it
    says so with a 404. This outcome means the answer arrived and the LOCAL re-find of
    it came back with zero or several matches — which a screen that moved on between
    the perception snapshot and the lookup explains just as well as absence does. It
    is neither cached nor a coordinate unlock.
    """

    reason: str
    authoritative: bool = False
    #: The retained descriptor the server named, when there was one. Carries the
    #: bounds and centre from the same parse the dom_index refers to, which is
    #: where the element was when the server chose it.
    descriptor: Optional[dict] = None
    #: How many live elements the lookup matched. Zero means the query reached
    #: nothing; several means it reached too much, and the centre already had its
    #: chance to separate them.
    matched: int = 0


@dataclass
class HealUnavailable:
    """Heal could not be consulted. Not authoritative — do not cache, do not treat
    as evidence that the element is gone."""

    cause: str


@dataclass
class HealDisabled:
    """Autoheal was explicitly disabled with ``TESTMU_HEAL``.

    This is deliberately a sibling of :class:`HealUnavailable`: a configured
    deterministic run may use its own point-grounded recording, while a transport
    failure or ``TESTMU_SMART=0`` must preserve the existing fail-loudly behavior.
    """

    reason: str


@dataclass
class HealProtocolError:
    """The server answered with something this binding cannot interpret. Not
    authoritative, for the same reason as HealUnavailable."""

    detail: str


def cache_key(selectors) -> tuple:
    """A stable, hashable key for a recorded selector set."""
    return tuple(
        (s.get("strategy"), s.get("selector")) for s in (selectors or [])
    )


def read_cache(key):
    """Read the per-step remap cache. Returns CACHE_ABSENT when there is no entry,
    None for the negative sentinel, or the cached (by, value) pair."""
    cache = get_heal_cache()
    if cache is None:
        return CACHE_ABSENT
    return cache.get(key, CACHE_ABSENT)


def write_cache(key, value) -> None:
    """Write the per-step remap cache. Dropped outside a step (nothing to scope to)."""
    cache = get_heal_cache()
    if cache is None:
        return
    cache[key] = value


def invalidate_cache(key) -> None:
    """Drop a cache entry so the next attempt re-asks the server.

    Used when a cached POSITIVE remap stops resolving: the screen moved on, so the
    entry is stale rather than wrong. Dropping it is the only way to reach a fresh
    heal; the negative sentinel is reserved for an authoritative 404.
    """
    cache = get_heal_cache()
    if cache is None:
        return
    cache.pop(key, None)


def _endpoint() -> str:
    host = _config.resolved("ai_api_host", _config._resolve_ai_api_host)
    return f"{str(host).rstrip('/')}/api/v1/autoheal"


def _heal_timeout_s(budget_s: Optional[float] = None) -> float:
    """The heal request timeout in whole seconds, floored at one.

    httpx takes seconds, so a sub-second `heal_timeout_ms` rounds down to zero and is
    then floored at one: "500ms" becomes one second, not the 60-second default.

    `budget_s` is what remains of the CALLER's per-action deadline. The configured
    timeout and the remaining budget are both ceilings, so the smaller one wins.
    Unlike the configured timeout, an action budget is not rounded up: 400ms left
    means at most a 400ms request, not a new one-second allowance.
    """
    milliseconds = int(_config.get("heal_timeout_ms", 60000) or 0)
    if milliseconds <= 0:
        configured = _DEFAULT_HEAL_TIMEOUT_S
    else:
        configured = max(1, milliseconds // 1000)
    if budget_s is None:
        return configured
    return max(0.0, min(float(configured), float(budget_s)))


def _relaxed_lookup(descriptor: dict, platform: str, compiled: tuple[str, str]):
    """The same descriptor compiled without its text, or None when that changes nothing.

    Plenty of descriptors never had a text clause in their lookup to begin with — a
    bare resource id, an accessibility id — and recompiling those spends a round-trip
    against the device to be told the same thing.
    """
    if not str(descriptor.get("text") or "").strip():
        return None
    try:
        relaxed = compile_descriptor(
            {key: value for key, value in descriptor.items() if key != "text"}, platform
        )
    except Exception:  # noqa: BLE001 — nothing identifying left is a miss, not a crash
        return None
    return None if relaxed == compiled else relaxed


def autoheal(driver, action_instruction: str, action_type: str,
             budget_s: Optional[float] = None, *, allow_inert: bool = False) -> Any:
    """Ask the server which element on the current screen the instruction meant.

    Never raises: every failure mode is one of the typed outcomes, so the caller's
    routing stays a single match statement.

    `budget_s`: what is left of the caller's per-action deadline; caps the HTTP
    timeout. Absent means the configured `heal_timeout_ms` alone applies.
    """
    unavailable = _eligibility_failure(action_type)
    if unavailable is not None:
        return unavailable

    capture_started = time.monotonic()
    try:
        perception = capture_perception(driver)
    except Exception as e:  # noqa: BLE001 — a broken snapshot is not an element verdict
        return HealUnavailable(f"perception failed: {e}")

    if not allow_inert:
        allowed = {
            index for index, descriptor in perception.descriptors.items()
            if descriptor.get("interactive", True)
        }
        perception.entries = [
            entry for entry in perception.entries if entry["index"] in allowed
        ]
        perception.descriptors = {
            index: descriptor
            for index, descriptor in perception.descriptors.items()
            if index in allowed
        }

    request_budget = (
        None if budget_s is None
        else max(0.0, budget_s - (time.monotonic() - capture_started))
    )
    selected = _request_selection(
        perception, action_instruction, action_type, budget_s=request_budget
    )
    if not isinstance(selected, _HealSelection):
        return selected
    descriptor = selected.descriptor
    dom_index = selected.dom_index

    platform = _config.platform()
    try:
        by, value = compile_descriptor(descriptor, platform)
    except Exception as e:  # noqa: BLE001 — an uncompilable descriptor is a miss, not a crash
        return HealProtocolError(f"descriptor for index {dom_index} is not compilable: {e}")

    try:
        matches = driver.find_elements(by, value)
    except Exception as e:  # noqa: BLE001
        return HealUnavailable(f"re-find failed: {e}")

    if not matches:
        # The compiled lookup ANDs the element's text into its identity, and on a
        # value-bearing control the text IS the value: a rating slider reads "0.0",
        # then "Any rating", then "2+ stars". The server round-trip sits between the
        # parse this descriptor came from and this re-find, so a lookup that matches
        # nothing says the text moved, not that the element left. Drop the text and
        # let whatever else names the element stand on its own; the retained centre
        # settles the several matches that can leave behind.
        #
        # Only on ZERO. Several matches is the opposite signal — the lookup was too
        # loose already, and loosening it further is the wrong direction.
        relaxed = _relaxed_lookup(descriptor, platform, (by, value))
        if relaxed is not None:
            _log.info("[autoheal] %s matched 0; retrying without its text", value[:60])
            by, value = relaxed
            try:
                matches = driver.find_elements(by, value)
            except Exception as e:  # noqa: BLE001
                return HealUnavailable(f"re-find failed: {e}")

    if len(matches) != 1:
        # Repeated resource-ids (RecyclerView rows) compile to a lookup that matches
        # every row; the descriptor's bounds and centre name which row was meant.
        chosen = disambiguate_by_centre(matches, descriptor)
        if chosen is None:
            return HealUnresolved(
                f"healed lookup {value!r} matched {len(matches)} live elements, expected 1",
                descriptor=descriptor,
                matched=len(matches),
            )
        _log.info(
            "[autoheal] %d matches for %s; resolved by descriptor centre %s",
            len(matches), value[:60], descriptor.get("center"),
        )
        matches = [chosen]

    _log.info(
        "[autoheal] %s → dom_index=%s via %s", action_instruction[:60], dom_index, value[:80]
    )
    return HealHit(
        element=matches[0],
        by=by,
        value=value,
        dom_index=dom_index,
        reasoning=selected.reasoning,
        descriptor=descriptor,
    )


def autoheal_web(
    driver,
    surface,
    action_instruction: str,
    action_type: str,
    budget_s: Optional[float] = None,
    *,
    allow_inert: bool = False,
) -> Any:
    """Select a DOM candidate using the normal canonical autoheal tree."""
    unavailable = _eligibility_failure(action_type)
    if unavailable is not None:
        return unavailable

    # Local import avoids making the generic heal client depend on web actions at
    # module import time.
    from testmu_appium import _action_web

    capture_started = time.monotonic()
    try:
        perception = _action_web.capture_perception(
            driver, surface, action_type, allow_inert=allow_inert
        )
    except Exception as e:  # noqa: BLE001
        return HealUnavailable(f"web perception failed: {e}")

    request_budget = (
        None if budget_s is None
        else max(0.0, budget_s - (time.monotonic() - capture_started))
    )
    selected = _request_selection(
        perception,
        action_instruction,
        action_type,
        budget_s=request_budget,
        surface="web",
    )
    if not isinstance(selected, _HealSelection):
        return selected
    return WebHealHit(
        descriptor=selected.descriptor,
        dom_index=selected.dom_index,
        reasoning=selected.reasoning,
    )


def _eligibility_failure(action_type: str):
    if current_step() is None:
        return HealUnavailable("no active step — heal is step-scoped")
    # ``heal=False`` is the explicit deterministic-mode switch. ``smart=False``
    # keeps its longstanding master-switch semantics: it prevents AI work but is
    # not evidence that a recorded point may be replayed.
    if not _config.heal:
        return HealDisabled("autoheal is off (TESTMU_HEAL)")
    if not _config.smart_enabled():
        return HealUnavailable("heal is off (TESTMU_SMART)")
    if action_type not in VALID_ACTION_TYPES:
        return HealUnavailable(
            f"action_type {action_type!r} is not healable; "
            f"expected one of {sorted(VALID_ACTION_TYPES)}"
        )
    return None


def _request_selection(
    perception,
    action_instruction: str,
    action_type: str,
    *,
    budget_s: Optional[float],
    surface: str = "native",
):
    if not perception.entries:
        return HealUnavailable("perception produced no interactive entries")
    if budget_s is not None and budget_s <= 0:
        return HealUnavailable("action deadline was exhausted before autoheal request")

    body = {
        "action_instruction": action_instruction,
        "action_type": action_type,
        "full_dom_list": perception.entries,
    }
    if surface != "native":
        body["surface"] = surface
    if perception.screenshot_b64:
        body["screenshot_b64"] = perception.screenshot_b64

    url = _endpoint()
    try:
        response = request_with_retry(
            "POST", url,
            headers=headers(),
            json_data=body,
            timeout=_heal_timeout_s(budget_s),
            total_timeout_s=budget_s,
            auth=auth(),
        )
    except httpx.HTTPError as e:
        return HealUnavailable(f"transport error: {e}")
    except Exception as e:  # noqa: BLE001
        return HealUnavailable(f"transport error: {e}")

    if response.status_code == 404:
        detail = _detail(response)
        _log.info("[autoheal] no_match: %s", detail)
        return HealNoMatch(f"server reported no match: {detail}")
    if response.status_code != 200:
        return HealUnavailable(f"status {response.status_code}: {response.text[:200]}")

    try:
        payload = response.json()
    except (json.JSONDecodeError, ValueError):
        return HealProtocolError(f"response body is not JSON: {response.text[:200]}")
    if not isinstance(payload, dict):
        return HealProtocolError(f"response body is not an object: {payload!r}")

    dom_index = payload.get("dom_index")
    if dom_index is None:
        return HealProtocolError(f"200 with no dom_index: {payload!r}")
    descriptor = perception.descriptors.get(dom_index)
    if descriptor is None:
        indices = [entry.get("index") for entry in perception.entries]
        return HealProtocolError(
            f"dom_index {dom_index} is not in the captured list "
            f"(indices {indices!r})"
        )
    return _HealSelection(
        descriptor=descriptor,
        dom_index=dom_index,
        reasoning=payload.get("reasoning", "") or "",
    )


def _detail(response) -> str:
    try:
        return str((response.json() or {}).get("detail", ""))
    except Exception:  # noqa: BLE001
        return response.text[:200]
