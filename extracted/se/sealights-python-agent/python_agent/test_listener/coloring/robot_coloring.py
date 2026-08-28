"""The browser coloring seam the Robot listener drives (contracts C6, C7, C7a).

One object owns everything the three browser stacks share: finding the Robot
library that holds the handles, deciding which handles still need the current
test's identity, guarding each handle separately, and matching the keyword names
that close a browser. Each stack contributes an adapter that knows only how to
list its own handles and run a script on one of them.

The seam deliberately holds the per-test coloring state rather than letting each
adapter keep its own, because that state is where the C7a navigation mechanisms
differ and where three separate copies would drift.
"""

import logging

log = logging.getLogger(__name__)

try:
    from robot.libraries.BuiltIn import BuiltIn
except ImportError:
    # Rule 21: robotframework ships only in the pinned [robot] extra. Nothing
    # here can run without a Robot process anyway, so absence is a no-op.
    BuiltIn = None

# Keyword names that make a handle disappear. Matched case-insensitively as a
# substring, so a prefixed form like "Browser.Close Page" matches too.
CLOSING_KEYWORD_PATTERNS = (
    "close page",
    "close context",
    "close browser",
    "close all browsers",
    "quit browser",
)

# A state token meaning "this handle is re-colored on every hook". It exists
# for the Selenium stacks without CDP, where C7a measured that reading
# `driver.current_url` to decide (1.83 ms) costs more than re-coloring
# unconditionally (1.07 ms).
RECOLOR_EVERY_HOOK = "sl:recolor-every-hook"

# A state token meaning "once per test is enough, because this handle re-colors
# itself after navigation". Any constant behaves this way, since the per-test
# state is dropped at `end_test`; naming it keeps the adapters from each
# inventing their own spelling of the same thing.
COLORED_ONCE_PER_TEST = "sl:colored-once-per-test"


def default_adapter_classes():
    """Every browser stack the listener supports.

    Imported here rather than at module level because each adapter subclasses
    `ColoringAdapter` from this module.
    """
    from python_agent.test_listener.coloring.browser_library_helper import (
        BrowserLibraryAdapter,
    )
    from python_agent.test_listener.coloring.playwright_helper import PlaywrightAdapter
    from python_agent.test_listener.coloring.selenium_helper import SeleniumAdapter

    return (BrowserLibraryAdapter, SeleniumAdapter, PlaywrightAdapter)


class ColoringAdapter(object):
    """One browser stack: how to list its handles and run a script on one.

    Subclasses implement three things and nothing else. Discovery goes through
    the seam's library lookup, never through patching a third-party class
    (contract C6, AC33).

    `targets()` returns every **live** handle as a `(key, state, handle)`
    triple:

    - `key` identifies the handle for as long as it exists, so per-test
      idempotence can be tracked by handle identity rather than by counting
      calls.
    - `state` is what makes a color stale. Its shape is how a stack expresses
      its C7a navigation mechanism: a page URL for the Browser library (a change
      is a navigation), the test name where the mechanism re-colors itself
      after navigation, or `RECOLOR_EVERY_HOOK` where re-coloring blindly is
      cheaper than detecting the need.

    Failures are the seam's problem, not the adapter's: it guards discovery once
    and every handle separately, so one dead session cannot abort the rest.
    """

    name = None

    def __init__(self, seam):
        self.seam = seam

    def targets(self):
        raise NotImplementedError

    def color(self, handle, execution_id, test_name):
        raise NotImplementedError

    def flush(self, handle):
        raise NotImplementedError


class RobotBrowserColoring(object):
    """The C7 actions, driven by the listener's hooks.

    Nothing here raises: a browser that cannot be colored costs browser
    coverage for that test, never the customer's run (Rule 22).
    """

    def __init__(self, adapter_classes=None):
        if adapter_classes is None:
            adapter_classes = default_adapter_classes()
        self._adapters = [adapter_class(self) for adapter_class in adapter_classes]
        self._libraries = {}
        self._all_libraries = None
        self._colored = {}

    def reset_libraries(self):
        """Forget which libraries are in use. Called on every `start_suite`.

        Library imports are suite-scoped, so the lookup is cached for a suite to
        keep `get_library_instance` from raising once per test. Caching it for
        the whole run instead is a real defect with a fix commit behind it
        (SLDEV-28058, `920fe78`): a sibling suite that does import the library
        would inherit the earlier suite's "absent" answer.
        """
        self._libraries = {}
        self._all_libraries = None

    def clear(self):
        """Drop the per-test coloring state. Called on `end_test`."""
        self._colored = {}

    def library_instance(self, name, capability=None):
        """The library `name` if the suite imported it and it can do `capability`.

        The capability is probed on the **instance**: `get_browser_catalog`
        exists only there, so `hasattr(Browser, ...)` is `False` and a
        class-level probe would disable the stack permanently (C6).

        `capability` is optional because it can only express a **callable**, and
        SeleniumLibrary's handles live behind a plain attribute
        (`_drivers.active_drivers`). Naming some other callable as a proxy would
        add exactly the failure mode C6 warns about with `driver_cache`: a probe
        that answers "no" disables the stack silently and permanently. That
        adapter reads what it needs and guards it itself.
        """
        if name in self._libraries:
            return self._libraries[name]
        instance = None
        try:
            candidate = BuiltIn().get_library_instance(name)
            if capability is None or callable(getattr(candidate, capability, None)):
                instance = candidate
            else:
                log.debug(
                    "Robot library %s is in use but has no callable %s"
                    % (name, capability)
                )
        except Exception as e:
            # get_library_instance raises for a library the suite never
            # imported, which is the ordinary case for two of the three stacks.
            log.debug("Robot library %s is not in use. Error: %s" % (name, str(e)))
        self._libraries[name] = instance
        return instance

    def library_instances(self):
        """Every library instance the suite imported, for duck-typed discovery.

        A customer library that wraps raw Selenium or owns a Playwright page
        answers to no library name, so it can only be found this way (C6).
        """
        if self._all_libraries is None:
            try:
                self._all_libraries = list(
                    BuiltIn().get_library_instance(all=True).values()
                )
            except Exception as e:
                log.debug("Failed listing Robot library instances. Error: %s" % str(e))
                self._all_libraries = []
        return self._all_libraries

    def color(self, execution_id, test_name):
        """Color every handle whose color is missing or stale.

        Driven from `start_test` (handles that already existed) and from every
        `end_keyword` (handles the test itself opened, and re-coloring after
        navigation). Not from `start_keyword`: the handles a keyword creates do
        not exist yet, and the ones that did were colored at the previous
        `end_keyword`.
        """
        for adapter in self._adapters:
            for key, state, handle in self._targets(adapter):
                if state != RECOLOR_EVERY_HOOK and self._colored.get(key) == state:
                    continue
                try:
                    adapter.color(handle, execution_id, test_name)
                    self._colored[key] = state
                except Exception as e:
                    log.debug("Failed coloring %s. Error: %s" % (key, str(e)))

    def flush(self):
        """Ask every live handle to send its footprints.

        Driven from `start_keyword` when the keyword about to run closes a
        handle, and from `end_test` for handles that outlive the test.
        """
        for adapter in self._adapters:
            for key, _state, handle in self._targets(adapter):
                try:
                    adapter.flush(handle)
                except Exception as e:
                    log.debug("Failed flushing %s. Error: %s" % (key, str(e)))

    @staticmethod
    def closes_a_browser(keyword_name):
        keyword_name = (keyword_name or "").lower()
        return any(pattern in keyword_name for pattern in CLOSING_KEYWORD_PATTERNS)

    def _targets(self, adapter):
        try:
            return [
                ((adapter.name, key), state, handle)
                for key, state, handle in adapter.targets()
            ]
        except Exception as e:
            log.debug("Failed listing %s handles. Error: %s" % (adapter.name, str(e)))
            return []
