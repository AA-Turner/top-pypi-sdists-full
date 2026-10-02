"""textual_query() — read a value locally, then via the flat perception.

Kept for recordings and generated tests that already carry it. New mobile
recordings use ``textual_analyzer`` (a recorded Python extraction over the
viewport tree); the analyze loop no longer records this verb.

When the generated action carries selectors and a selected attribute, a strict
unique Appium lookup reads that attribute without AI. A miss retains the analyzer
flow below.

Runs the analyzer's two-step ``dom`` leg on the v16-server host resolved by
``_config._resolve_ai_api_host()``, the same shape the web bindings use:

1. identify — the flat wire entries (``_perception.capture_perception``) go up as
   ``full_dom_list``; the answer is a ``dom_index`` into them.
2. extract — the identified entry's retained descriptor is rendered as an
   ``element_snapshot`` and the value is read from it.

If the DOM extract leg explicitly abstains with ``__not_visible__``, the same
semantic query is retried once against a fresh screenshot via ``vision_query``.
Transport, authentication and malformed-response failures stay hard failures;
they do not silently change modalities.

The web bindings build step 2's snapshot over CDP. A native session has no CDP
and no executable JS, so the snapshot is built from the descriptor map the
perception keeps back at capture time.
"""
import logging

from selenium.common.exceptions import StaleElementReferenceException

from testmu_appium import _config
from testmu_appium._errors import (
    TestmuConfigError,
    UnknownStrategy,
    UnsupportedOnPlatform,
)
from testmu_appium._helpers._analyzer_result import is_not_visible
from testmu_appium._helpers._http import auth, headers, request_with_retry
from testmu_appium._helpers._perception import capture_perception, element_snapshot
from testmu_appium._helpers._return_type import coerce
from testmu_appium._helpers._strategy import (
    compile_selector,
    known_strategies,
    order_by_score,
    selected_attribute,
)
from testmu_appium._helpers.vision_query import vision_query
from testmu_appium._vars import set_var, var

_log = logging.getLogger("testmu_appium")

_ENDPOINT = "/api/v1/analyzer"

_LOCAL_MISS = object()


def _resolve_query(query: str) -> str:
    resolved = var(query)
    return resolved if isinstance(resolved, str) else str(resolved)


def _post(url: str, body: dict, *, stage: str) -> dict:
    """One analyzer call, with the failure modes named for the calling stage."""
    response = request_with_retry(
        "POST", url, headers=headers(), json_data=body, auth=auth(),
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"textual_query: {_ENDPOINT} {stage} returned "
            f"{response.status_code}: {response.text[:500]}"
        )
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"textual_query: {_ENDPOINT} {stage} returned a non-JSON body: "
            f"{response.text[:500]}"
        ) from exc
    if not isinstance(data, dict):
        raise RuntimeError(
            f"textual_query: {_ENDPOINT} {stage} response is not an object: {data!r}"
        )
    return data


def _read_local(driver, selectors, selected_attribute_name: str, *, description: str):
    """Read one attribute from the first ranked selector with one live match.

    A local miss is deliberately not an action-engine miss: query reads retain their
    legacy analyzer as the fallback, so there is no polling, healing, coordinate
    route, or approximate choice among several elements here.
    """
    platform = _config.platform()
    known = known_strategies(platform)
    for selector in selectors:
        strategy = selector.get("strategy")
        if strategy not in known:
            raise UnknownStrategy(str(strategy), platform, known)

    attribute_name = selected_attribute(selected_attribute_name, platform)
    if attribute_name is None:
        _log.info(
            "[textual_query] %s | local field=%r unsupported on %s; using analyzer",
            description, selected_attribute_name, platform,
        )
        return _LOCAL_MISS

    for stale_attempt in range(2):
        try:
            for selector in order_by_score(selectors):
                # Compilation stays outside the Appium-error fallback contract.
                # Producer/binding strategy skew must be visible, never disguised
                # as a successful legacy AI read.
                by, value = compile_selector(selector, platform)
                try:
                    matches = driver.find_elements(by, value)
                except StaleElementReferenceException:
                    raise
                except Exception as exc:  # noqa: BLE001 — Appium lookup falls back to AI
                    _log.info(
                        "[textual_query] %s | local lookup failed (%s); using analyzer",
                        description, exc,
                    )
                    return _LOCAL_MISS

                if len(matches) != 1:
                    if matches:
                        _log.info(
                            "[textual_query] %s | local strategy %s matched %d "
                            "elements; trying the next",
                            description, selector.get("strategy"), len(matches),
                        )
                    continue

                try:
                    value = matches[0].get_attribute(attribute_name)
                except StaleElementReferenceException:
                    raise
                except Exception as exc:  # noqa: BLE001 — Appium read falls back to AI
                    _log.info(
                        "[textual_query] %s | local attribute read failed (%s); "
                        "using analyzer",
                        description, exc,
                    )
                    return _LOCAL_MISS

                if value is None or value == "":
                    _log.info(
                        "[textual_query] %s | local attribute %s was empty; "
                        "using analyzer",
                        description, attribute_name,
                    )
                    return _LOCAL_MISS
                _log.info(
                    "[textual_query] %s | local strategy=%s attribute=%s",
                    description, selector.get("strategy"), attribute_name,
                )
                return value
            return _LOCAL_MISS
        except (UnknownStrategy, UnsupportedOnPlatform):
            raise
        except StaleElementReferenceException:
            if stale_attempt == 0:
                _log.info(
                    "[textual_query] %s | local element went stale; retrying once",
                    description,
                )
                continue
            _log.info(
                "[textual_query] %s | local element stayed stale; using analyzer",
                description,
            )
            return _LOCAL_MISS
    return _LOCAL_MISS


def textual_query(
    driver,
    *,
    query: str,
    description: str = "",
    output_variable: str = "",
    return_type: str | None = None,
    expected_value=None,
    selectors=None,
    selected_attribute_name: str = "",
):
    """Extract a value from the current screen's flat perception via the analyzer.

    Requests: ``POST {ai_api_host}/api/v1/analyzer`` twice — identify with
    ``{"type": "dom", "query": ..., "full_dom_list": perception.entries}``, then
    extract with ``{"type": "dom", "query": ..., "element_snapshot": ...}``.

    Args:
        driver: Live Appium driver — a fresh perception is captured from it.
        query: Natural-language description of what to extract. May carry
            ``{{var}}``/``${var}`` tokens, resolved before the request.
        description: Human-readable label for this read, carried into every
            log line for the call. DEFAULTS TO THE RESOLVED QUERY when empty,
            so every read is identifiable in the log.
        output_variable: When non-empty, the extracted value is written via
            ``set_var(output_variable, value)``.
        expected_value: Rides on the extract call, where it gates the analyzer's
            boolean-check branch. The identify call has no value to check.
        selectors: Optional ranked native selectors. Together with
            ``selected_attribute_name``, these enable a strict unique local Appium
            read before the legacy analyzer path.
        selected_attribute_name: Portable field to read from a uniquely located
            element. Unsupported fields retain the legacy analyzer behavior.

    Returns:
        The DOM-extracted value, or the visual result after one DOM abstention,
        coerced to ``return_type``.

    Raises:
        TestmuConfigError: smart is off and the local read did not produce a value.
        RuntimeError: Either call responded non-200 or unusably, the identify
            answer carried no ``dom_index``, that index names an element this
            capture never saw, or both DOM and visual extraction abstained.
    """
    if selectors and selected_attribute_name:
        step_description = description or query
        raw = _read_local(
            driver, selectors, selected_attribute_name, description=step_description
        )
        if raw is not _LOCAL_MISS:
            extracted = coerce(raw, return_type)
            _log.info(
                "[textual_query] %s | result=%r",
                step_description, str(extracted)[:120],
            )
            if output_variable:
                set_var(output_variable, extracted)
            return extracted

    if not _config.smart_enabled():
        raise TestmuConfigError(
            "textual_query requires TESTMU_SMART=1 (AI-backed read, no local fallback)"
        )

    resolved_query = _resolve_query(query)
    step_description = description or resolved_query
    perception = capture_perception(driver, include_screenshot=False)
    _log.info(
        "[textual_query] %s | query=%r entries=%d",
        step_description, resolved_query, len(perception.entries),
    )

    host = _config.resolved("ai_api_host", _config._resolve_ai_api_host)
    url = f"{host}{_ENDPOINT}"

    identified = _post(url, {
        "type": "dom",
        "query": resolved_query,
        "full_dom_list": perception.entries,
    }, stage="identify")
    dom_index = identified.get("dom_index")
    if dom_index is None:
        raise RuntimeError(
            f"textual_query: identify returned no 'dom_index': {identified!r}"
        )
    dom_index = int(dom_index)
    if dom_index not in perception.descriptors:
        raise RuntimeError(
            f"textual_query: identify returned dom_index={dom_index}, not present "
            f"in this capture's indices {sorted(perception.descriptors)}"
        )
    _log.info(
        "[textual_query] %s | identified index=%d", step_description, dom_index
    )

    body = {
        "type": "dom",
        "query": resolved_query,
        "element_snapshot": element_snapshot(perception, dom_index),
    }
    if expected_value is not None:
        body["expected_value"] = expected_value
    data = _post(url, body, stage="extract")
    if "extracted_value" not in data:
        raise RuntimeError(
            f"textual_query: {_ENDPOINT} extract response missing "
            f"'extracted_value': {data!r}"
        )

    raw = data["extracted_value"]
    if is_not_visible(raw):
        _log.info(
            "[textual_query] %s | DOM extraction abstained; retrying via vision",
            step_description,
        )
        extracted = vision_query(
            driver,
            query=resolved_query,
            description=step_description,
            return_type=return_type,
            expected_value=expected_value,
        )
    else:
        extracted = coerce(raw, return_type)
    _log.info("[textual_query] %s | result=%r", step_description, str(extracted)[:120])
    if output_variable:
        set_var(output_variable, extracted)
    return extracted
