"""SmartWait — pre-action network-idle + DOM-idle wait for the V3 Selenium binding.

Ported from the V2 SmartWait implementation. Differences here:
DOM-idle added (not in any V2 checkout reviewed), Chrome
gate explicit, KANEAI_FEATURE_FLAGS read from env, and the V3-only on/off env
dropped — SmartWait is always-on like V2.

Guarantees:
- Chrome-only: get_log('performance') is Chrome-only; no-op on other browsers.
- Always-on: no enable/disable switch; set a *_max to 0 to skip that wait.
- Never raises: every path degrades to a debug line and returns.
"""
import json
import logging
import os
import time

logger = logging.getLogger(__name__)

# Chrome devtools network event names (same as V2 NETWORK_REQUEST/RESPONSE_EVENTS).
_NETWORK_REQUEST_EVENTS = ["Network.requestWillBeSent"]
_NETWORK_RESPONSE_EVENTS = [
    "Network.responseReceived",
    "Network.BlockedReason",  # V2-parity: a CDP type, not an emitted event method — effectively a no-op, kept to match the V2 source
    "Network.loadingFailed",
]

# 200 ms quiet buffer after the last response before declaring network idle (V2 WAIT_BUFFER).
_WAIT_BUFFER_S = 0.2
# Poll cadence for the network-idle loop.
_POLL_INTERVAL_S = 0.05
# Extra seconds added to the browser script timeout over dom_idle_max so the
# async MutationObserver script always has room to resolve its callback.
_SCRIPT_TIMEOUT_MARGIN_S = 5.0

_CHROME_NAMES = ("chrome", "chromium")

# Defaults mirror V2 DEFAULT_SMART_WAIT_CONFIG plus the DOM-idle knobs from the
# reference logs (max 1.5s, threshold 300ms).
_DEFAULT_CONFIG: dict = {
    "vision_min": 5.0,
    "vision_max": 5.0,
    "non_vision_max": 10.0,
    "dom_idle_threshold": 0.3,
    "dom_idle_max": 1.5,
}


def load_feature_flags() -> dict | None:
    """Parse the KANEAI_FEATURE_FLAGS env var (JSON) to a dict, or None if unset/invalid."""
    raw = os.getenv("KANEAI_FEATURE_FLAGS")
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:  # noqa: BLE001 — malformed flags must not break a test
        return None


def _parse_feature_flags(feature_flags: dict | None) -> dict:
    """Extract the web smart-wait config; fall back to defaults for missing/invalid keys.

    Expected shape: {"kaneai_web_smart_wait": {"payload": {<known keys>}}}.
    """
    config = _DEFAULT_CONFIG.copy()
    if not feature_flags or not isinstance(feature_flags, dict):
        return config
    web_flag = feature_flags.get("kaneai_web_smart_wait")
    if not web_flag or not isinstance(web_flag, dict):
        return config
    payload = web_flag.get("payload", {})
    if not isinstance(payload, dict):
        return config
    config.update({k: v for k, v in payload.items() if k in _DEFAULT_CONFIG})
    return config


def _is_chrome(driver) -> bool:
    """True only for chrome/chromium; any access error is treated as non-chrome."""
    try:
        return (driver.capabilities or {}).get("browserName", "").lower() in _CHROME_NAMES
    except Exception:  # noqa: BLE001
        return False


def _process_browser_logs_for_network_events(driver) -> list:
    """Pull Chrome performance logs and return parsed network events (noise filtered)."""
    try:
        logs = driver.get_log("performance")
    except Exception as exc:  # noqa: BLE001
        logger.debug("[SmartWait] Could not retrieve performance logs: %s", exc)
        return []
    events = []
    for entry in logs:
        try:
            log = json.loads(entry["message"])["message"]
            method = log.get("method", "")
            params = log.get("params", {})
            if method not in _NETWORK_REQUEST_EVENTS and method not in _NETWORK_RESPONSE_EVENTS:
                continue
            if params.get("type") in ("Other", "Document", "Ping"):
                continue
            events.append({
                "timestamp": entry["timestamp"],
                "method": method,
                "requestId": params.get("requestId", ""),
                "type": params.get("type", ""),
            })
        except Exception:  # noqa: BLE001
            continue
    return events


def _smart_network_wait(driver, timeout: float, start_ts: float = 0.0) -> None:
    """Poll performance logs until the network is idle or ``timeout`` (s) expires.

    Network is idle when no tracked request is in flight AND the last response was
    at least ``_WAIT_BUFFER_S`` ago. ``start_ts`` (epoch ms) ignores request events
    older than it; 0 accepts all (the default, matching the V2 port). Never raises.
    """
    try:
        start_ms = time.time() * 1000
        request_map: dict[str, float] = {}
        most_recent_network_ts = start_ms
        while True:
            for event in _process_browser_logs_for_network_events(driver):
                if event["method"] in _NETWORK_REQUEST_EVENTS and event["timestamp"] >= start_ts:
                    request_map[event["requestId"]] = event["timestamp"]
                elif event["method"] in _NETWORK_RESPONSE_EVENTS:
                    if event["requestId"] in request_map:
                        most_recent_network_ts = event["timestamp"]
                        del request_map[event["requestId"]]
            now_ms = time.time() * 1000
            elapsed_ms = now_ms - start_ms
            quiet_ms = now_ms - most_recent_network_ts
            if len(request_map) == 0 and quiet_ms >= _WAIT_BUFFER_S * 1000:
                logger.info("[SmartWait] Network idle after %.2fs", elapsed_ms / 1000.0)
                return
            if elapsed_ms > timeout * 1000:
                logger.info("[SmartWait] Network wait timeout after %.2fs", elapsed_ms / 1000.0)
                return
            time.sleep(_POLL_INTERVAL_S)
    except Exception as exc:  # noqa: BLE001
        logger.debug("[SmartWait] Error in network wait: %s", exc)


# In-browser DOM-idle: install a MutationObserver, resolve when the DOM has been
# quiet for `threshold` ms, or when `maxWait` ms elapse. Returns {reason, elapsed_ms}.
_DOM_IDLE_JS = """
const done = arguments[arguments.length - 1];
const threshold = arguments[0];
const maxWait = arguments[1];
const start = performance.now();
let last = start;
let obs;
try {
  obs = new MutationObserver(function () { last = performance.now(); });
  obs.observe(document.documentElement, {
    childList: true, subtree: true, attributes: true, characterData: true
  });
} catch (e) {
  done({reason: "error", elapsed_ms: 0});
  return;
}
function check() {
  const now = performance.now();
  if (now - last >= threshold) { obs.disconnect(); done({reason: "idle", elapsed_ms: now - start}); return; }
  if (now - start >= maxWait) { obs.disconnect(); done({reason: "max", elapsed_ms: now - start}); return; }
  setTimeout(check, 50);
}
setTimeout(check, 50);
"""


def _smart_dom_wait(driver, threshold_s: float, max_s: float) -> None:
    """Wait until the DOM is quiet for ``threshold_s`` (up to ``max_s``). Never raises.

    Runs the whole wait in-browser via execute_async_script and logs the outcome.
    Bumps the browser script timeout for the call (only when the prior value could
    be read, so it can be restored) and restores it afterwards.
    """
    prev_timeout = None
    try:
        try:
            prev_timeout = driver.timeouts.script
        except Exception:  # noqa: BLE001
            prev_timeout = None
        if prev_timeout is not None:
            driver.set_script_timeout(max_s + _SCRIPT_TIMEOUT_MARGIN_S)
        result = driver.execute_async_script(_DOM_IDLE_JS, threshold_s * 1000, max_s * 1000) or {}
        reason = result.get("reason", "?")
        elapsed_ms = result.get("elapsed_ms", 0)
        if reason == "error":
            logger.debug("[SmartWait] DOM idle wait skipped (observer setup error)")
        else:
            logger.info("[SmartWait] DOM idle after %.2fs (reason: %s)", elapsed_ms / 1000.0, reason)
    except Exception as exc:  # noqa: BLE001
        logger.debug("[SmartWait] Error in DOM idle wait: %s", exc)
    finally:
        if prev_timeout is not None:
            try:
                driver.set_script_timeout(prev_timeout)
            except Exception:  # noqa: BLE001
                pass


class SmartWait:
    """Pre-action quiet wait. Construct per call: SmartWait(driver).smart_wait(...).

    Config resolves from the passed feature_flags dict, else from the
    KANEAI_FEATURE_FLAGS env, else defaults.
    """

    def __init__(self, driver, feature_flags: dict | None = None):
        self.driver = driver
        if feature_flags is None:
            feature_flags = load_feature_flags()
        self.config = _parse_feature_flags(feature_flags)

    def smart_wait(self, is_vision: bool = False) -> None:
        """Single entry point. No-op on non-chrome browsers; never raises."""
        try:
            if not _is_chrome(self.driver):
                logger.debug("[SmartWait] Non-chrome browser; skipping")
                return
            if is_vision:
                self._vision_wait()
            else:
                self._non_vision_wait()
        except Exception as exc:  # noqa: BLE001
            logger.debug("[SmartWait] Unexpected error, skipping: %s", exc)

    def _non_vision_wait(self) -> None:
        timeout = float(self.config["non_vision_max"])
        if timeout > 0:
            logger.info("[SmartWait] Non-vision: network wait with %ss timeout", timeout)
            _smart_network_wait(self.driver, timeout=timeout)
        dom_max = float(self.config["dom_idle_max"])
        dom_threshold = float(self.config["dom_idle_threshold"])
        if dom_max > 0:
            logger.info(
                "[SmartWait] Non-vision: DOM idle wait (max %ss, threshold %sms)",
                dom_max, int(dom_threshold * 1000),
            )
            _smart_dom_wait(self.driver, dom_threshold, dom_max)

    def _vision_wait(self) -> None:
        vision_min = float(self.config["vision_min"])
        vision_max = float(self.config["vision_max"])
        if vision_min > 0:
            logger.info("[SmartWait] Vision: sleeping for %ss (minimum wait)", vision_min)
            time.sleep(vision_min)
        # if vision_min exhausts the full budget, no network budget remains
        remaining = max(0.0, vision_max - vision_min)
        if remaining > 0:
            logger.info("[SmartWait] Vision: network wait with %ss timeout", remaining)
            _smart_network_wait(self.driver, timeout=remaining)
