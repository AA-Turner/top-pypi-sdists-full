"""Coloring adapter for Selenium, whether SeleniumLibrary owns it or not.

Three things about this stack are traps rather than choices, and each one fails
silently, which is why they are stated here instead of being left to the reader
of the code:

1. `execute_script` takes a **function body**. Handing it the arrow-shaped
   shared constant raises nothing, logs nothing, and colors nothing: the arrow
   function is constructed as an expression statement and thrown away. The
   constants stay the single source of truth, wrapped here (C5).
2. **CDP support is established by calling it**, never by attribute presence.
   Every Selenium driver class reports `execute_cdp_cmd`, Firefox and Safari
   included, and only Chromium implements it (Rule 27, AC45).
3. An init script runs **before any page script**, so `window.$SealightsAgent`
   does not exist yet. A payload that dispatches immediately is lost with
   nothing raised, so it waits for the agent with a bounded timeout and gives up
   quietly (Rule 28, AC47).

Discovery reads library state and never patches a third-party class (C6, AC33).
The standalone listener patches `WebDriver.get/close/quit`; the POC measured what
that costs (one wrapper layer per test, ten after ten tests) and showed the scan
below covers the one case patching was ahead on, a customer library that never
imports SeleniumLibrary.
"""

import json
import logging

from python_agent.test_listener.coloring.playwright_helper import (
    SEND_FOOTPRINTS_JS,
    SET_BAGGAGE_JS,
    baggage_arguments,
)
from python_agent.test_listener.coloring.robot_coloring import (
    COLORED_ONCE_PER_TEST,
    RECOLOR_EVERY_HOOK,
    ColoringAdapter,
)

log = logging.getLogger(__name__)

SELENIUM_LIBRARY_NAME = "SeleniumLibrary"

ADD_INIT_SCRIPT = "Page.addScriptToEvaluateOnNewDocument"
REMOVE_INIT_SCRIPT = "Page.removeScriptToEvaluateOnNewDocument"

# The in-page agent can load after the document does. 5 ms of polling for at most
# 5 seconds is the shape proven in poc/initscript/.
AGENT_POLL_INTERVAL_MS = 5
AGENT_POLL_TIMEOUT_MS = 5000

# `execute_script` wants a statement, so both shared constants are called in
# place. The dropped arrow function is trap 1 above.
SET_CONTEXT_SCRIPT = "return (%s)(arguments[0]);" % SET_BAGGAGE_JS
FLUSH_SCRIPT = "return (%s)();" % SEND_FOOTPRINTS_JS

INIT_SCRIPT_TEMPLATE = """
(function () {
  var args = %(args)s;
  var fire = function () {
    if (!window.$SealightsAgent) { return false; }
    (%(set_baggage)s)(args);
    return true;
  };
  if (!fire()) {
    var poll = setInterval(function () {
      if (fire()) { clearInterval(poll); }
    }, %(interval)d);
    setTimeout(function () { clearInterval(poll); }, %(timeout)d);
  }
})();
"""


def init_script(execution_id, test_name):
    """The payload Chromium runs on every new document, per C7a.

    It waits for the in-page agent rather than dispatching into a document that
    has not run a line of its own script yet (Rule 28).
    """
    return INIT_SCRIPT_TEMPLATE % {
        "args": json.dumps(baggage_arguments(execution_id, test_name)),
        "set_baggage": SET_BAGGAGE_JS,
        "interval": AGENT_POLL_INTERVAL_MS,
        "timeout": AGENT_POLL_TIMEOUT_MS,
    }


def is_a_driver(candidate):
    """Whether `candidate` quacks like a Selenium driver.

    A callable `execute_script` is the whole duck type, which is what found a
    raw `webdriver.Chrome` held by a customer library in the POC.
    """
    return candidate is not None and callable(
        getattr(candidate, "execute_script", None)
    )


def driver_key(driver):
    """A handle identity that survives as long as the driver does.

    `session_id` is a local attribute rather than a round trip. A duck-typed
    driver from a customer library may not have one, so object identity is the
    fallback; both are stable for the lifetime of the handle, which is all the
    seam's per-test guarding needs.
    """
    session_id = getattr(driver, "session_id", None)
    return session_id if session_id else "id:%d" % id(driver)


class SeleniumAdapter(ColoringAdapter):
    """Handles from SeleniumLibrary's driver cache, plus a duck-typed scan.

    The per-driver bookkeeping here is **not** per-test coloring state, which
    the seam owns. It is which drivers have CDP (a fact about the browser, so it
    is learned once) and which init script is currently installed on each (which
    has to be removed before the next one is added, or AC46's count grows by one
    per test).
    """

    name = "Selenium"

    def __init__(self, seam):
        super(SeleniumAdapter, self).__init__(seam)
        self._init_script_ids = {}
        self._without_cdp = set()

    def targets(self):
        return [
            (driver_key(driver), self._state(driver), driver)
            for driver in self._drivers()
        ]

    def color(self, handle, execution_id, test_name):
        """Color the current document, and every future one where CDP allows.

        The `execute_script` call comes first and unconditionally: it is what
        covers the page in front of the test right now, and an init script only
        ever affects the *next* document.
        """
        handle.execute_script(
            SET_CONTEXT_SCRIPT, baggage_arguments(execution_id, test_name)
        )
        key = driver_key(handle)
        if key not in self._without_cdp:
            self._install_init_script(handle, key, execution_id, test_name)

    def flush(self, handle):
        handle.execute_script(FLUSH_SCRIPT)

    def _drivers(self):
        """Every live driver in the suite, SeleniumLibrary's first.

        `active_drivers` and never `.driver` (returns one driver of several,
        returns nothing once the current one closes while others remain, and
        raises `NoOpenBrowser` rather than returning `None`), never
        `driver_cache` (absent on every version from 4.5.0 to 6.9.0, so a
        `getattr` probe against it disables this stack forever), and never
        `_drivers.drivers` (includes closed drivers, one raise per dead
        session).
        """
        drivers, seen = [], set()
        for driver in self._selenium_library_drivers():
            if id(driver) not in seen and is_a_driver(driver):
                seen.add(id(driver))
                drivers.append(driver)
        for driver in self._duck_typed_drivers():
            if id(driver) not in seen:
                seen.add(id(driver))
                drivers.append(driver)
        return drivers

    def _selenium_library_drivers(self):
        library = self.seam.library_instance(SELENIUM_LIBRARY_NAME)
        cache = getattr(library, "_drivers", None)
        return list(getattr(cache, "active_drivers", None) or [])

    def _duck_typed_drivers(self):
        """Drivers held by a library that never imports SeleniumLibrary.

        This is the only route to a customer library wrapping raw Selenium, and
        it is why patching browser creation buys nothing: acquisition by reading
        finds a driver that existed before the listener did.
        """
        drivers = []
        for instance in self.seam.library_instances():
            for attribute in dir(instance):
                if attribute.startswith("__") or attribute.startswith("ROBOT_"):
                    continue
                try:
                    value = getattr(instance, attribute)
                except Exception:
                    # A property that raises without a browser open is ordinary
                    # here: SeleniumLibrary's own `.driver` is one.
                    continue
                if is_a_driver(value):
                    drivers.append(value)
        return drivers

    def _state(self, driver):
        """What makes this driver's color stale, per C7a.

        With CDP, the installed init script re-colors every new document, so one
        color per test is enough. Without it, re-color on every hook: reading
        `driver.current_url` to decide costs 1.83 ms against 1.07 ms to just
        re-color, so diffing does not buy back its own cost.
        """
        if driver_key(driver) in self._without_cdp:
            return RECOLOR_EVERY_HOOK
        return COLORED_ONCE_PER_TEST

    def _install_init_script(self, driver, key, execution_id, test_name):
        """Replace this driver's init script, or record that it has no CDP.

        Remove-then-add rather than add: CDP has no replace, and every add
        without a matching remove stays live and re-dispatches its own dead test
        name on every later navigation (AC46).
        """
        previous = self._init_script_ids.pop(key, None)
        if previous is not None:
            try:
                driver.execute_cdp_cmd(REMOVE_INIT_SCRIPT, {"identifier": previous})
            except Exception as e:
                # Guarded apart from the add below so that a stale identifier,
                # which a browser restart leaves behind, cannot be mistaken for
                # this driver having no CDP at all.
                log.debug(
                    "Failed removing init script %s from Selenium driver %s. Error: %s"
                    % (previous, key, str(e))
                )
        try:
            installed = driver.execute_cdp_cmd(
                ADD_INIT_SCRIPT, {"source": init_script(execution_id, test_name)}
            )
        except Exception as e:
            # Calling it is the capability probe (Rule 27). The current document
            # is already colored, so this driver simply falls back to being
            # re-colored on every hook.
            self._without_cdp.add(key)
            log.debug("Selenium driver %s has no usable CDP. Error: %s" % (key, str(e)))
            return
        identifier = (installed or {}).get("identifier")
        if identifier is not None:
            self._init_script_ids[key] = identifier
