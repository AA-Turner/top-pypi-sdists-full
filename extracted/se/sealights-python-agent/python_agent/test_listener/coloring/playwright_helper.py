import logging

from python_agent.test_listener.coloring.robot_coloring import (
    COLORED_ONCE_PER_TEST,
    ColoringAdapter,
)

log = logging.getLogger(__name__)

SET_BAGGAGE_JS = """(args) => {
    if (!window.$SealightsAgent) {
        return;
    }
    window.dispatchEvent(new CustomEvent('set:context', {
        detail: {
            baggage: {
                'x-sl-test-session-id': args.executionId,
                'x-sl-test-name': args.testName
            }
        }
    }));
}"""

SEND_FOOTPRINTS_JS = """() => {
    if (window.$SealightsAgent && window.$SealightsAgent.sendAllFootprints) {
        return window.$SealightsAgent.sendAllFootprints();
    }
}"""


def baggage_arguments(execution_id, test_name):
    """The one argument `SET_BAGGAGE_JS` takes, as strings.

    Lives beside the constant because every stack that sends it needs the same
    invariant, and `str` is not decoration: an identity that reaches the page as
    JavaScript `null` or as a bare number is the SLDEV-28058 `8696fc7` failure.
    """
    return {"executionId": str(execution_id), "testName": str(test_name)}


class PlaywrightBrowserAgent:
    """Communicates with the in-page SeaLights browser agent via Playwright's page.evaluate().

    Both public methods are safe to call unconditionally -- they catch exceptions
    internally so test execution is never interrupted by browser-agent failures.
    The presence of window.$SealightsAgent is checked inside the evaluated JS,
    so calls are a single round-trip with no polling.
    """

    def set_test_identifier(self, page, execution_id, test_name):
        """Dispatch a set:context CustomEvent so the in-page browser agent
        colors subsequent coverage with the current test identifiers.

        The browser agent's setContextHandler unpacks ``detail.baggage`` and
        re-emits set:baggage internally, so callers don't need to dispatch
        set:baggage directly.

        No-op inside the page if window.$SealightsAgent is not present.
        """
        try:
            page.evaluate(
                SET_BAGGAGE_JS,
                {
                    "executionId": execution_id,
                    "testName": test_name,
                },
            )
            log.debug("Browser test identifier set: %s/%s", execution_id, test_name)
        except Exception as e:
            log.debug("Failed to set browser test identifier: %s", e)

    def send_all_footprints(self, page):
        """Call sendAllFootprints() in the page to flush coverage to the SeaLights collector.

        No-op inside the page if window.$SealightsAgent is not present.
        """
        try:
            page.evaluate(SEND_FOOTPRINTS_JS)
            log.debug("Browser footprints flushed")
        except Exception as e:
            log.debug("Failed to flush browser footprints: %s", e)


def is_a_page(candidate):
    """Whether `candidate` quacks like a Playwright page.

    Both `evaluate` and `goto` are required. `evaluate` alone matches unrelated
    objects, and the pair is what the POC scan used to find a customer library's
    page with no configuration. Nothing in a Browser Library suite can match:
    that library talks to a Node sidecar over gRPC and has no Python page object
    at all, which is why it needs the catalog route instead.
    """
    return (
        candidate is not None
        and callable(getattr(candidate, "evaluate", None))
        and callable(getattr(candidate, "goto", None))
    )


class PlaywrightAdapter(ColoringAdapter):
    """Pages held by any imported Robot library, re-colored by a load handler.

    C7a is served by Playwright's own `load` event rather than by anything this
    adapter decides. The two alternatives were measured and rejected in
    `poc/initscript/`: `add_init_script` has no remove or replace in Playwright
    1.62, so scripts accumulate and each stale one re-dispatches its own finished
    test's name on every later navigation, and carrying the identity in
    `sessionStorage` is per origin, so it stops coloring at the first SSO
    redirect with nothing raised.

    One handler per page for the life of the run, reading the identity at fire
    time. A handler registered per test would have to be removed at the next one,
    which is the accumulation failure again with a different API.
    """

    name = "Playwright"

    def __init__(self, seam):
        super(PlaywrightAdapter, self).__init__(seam)
        self._identities = {}
        self._handled = set()

    def targets(self):
        return [(id(page), COLORED_ONCE_PER_TEST, page) for page in self._pages()]

    def color(self, handle, execution_id, test_name):
        self._identities[id(handle)] = (execution_id, test_name)
        handle.evaluate(SET_BAGGAGE_JS, baggage_arguments(execution_id, test_name))
        self._watch_for_navigation(handle)

    def flush(self, handle):
        handle.evaluate(SEND_FOOTPRINTS_JS)

    def _pages(self):
        """Every live page any imported library holds.

        Robot has no single context object to read, which is why this is a scan
        rather than one `getattr`; it is the behave `_resolve_browser_page`
        pattern widened to every library instance.
        """
        pages, seen = [], set()
        for instance in self.seam.library_instances():
            for attribute in dir(instance):
                if attribute.startswith("__") or attribute.startswith("ROBOT_"):
                    continue
                try:
                    value = getattr(instance, attribute)
                except Exception:
                    continue
                if not is_a_page(value) or id(value) in seen:
                    continue
                seen.add(id(value))
                if not self._is_closed(value):
                    pages.append(value)
        return pages

    @staticmethod
    def _is_closed(page):
        try:
            return bool(page.is_closed())
        except Exception:
            # Not a real page, or one whose connection is gone. Either way the
            # per-handle guard in the seam covers what happens next.
            return False

    def _watch_for_navigation(self, page):
        """Register this page's one `load` handler, if it has none yet.

        Playwright pumps handlers on Playwright calls rather than on wall-clock
        time, so the event says *when* the page lost its identity without this
        adapter guessing. It does not remove the need to color at a hook: a page
        that never navigates gets no event.
        """
        key = id(page)
        if key in self._handled:
            return
        try:
            page.on("load", lambda _: self._recolor(page))
            self._handled.add(key)
        except Exception as e:
            log.debug("Failed watching Playwright page %s. Error: %s" % (key, str(e)))

    def _recolor(self, page):
        """Re-color after a navigation, with whatever identity is current.

        Called from Playwright's dispatch rather than from the seam, so it owns
        its own guard: an exception here would surface inside a customer's
        keyword rather than in the listener (Rule 22).
        """
        identity = self._identities.get(id(page))
        if identity is None:
            return
        try:
            page.evaluate(SET_BAGGAGE_JS, baggage_arguments(*identity))
        except Exception as e:
            log.debug(
                "Failed re-coloring Playwright page after navigation. Error: %s"
                % str(e)
            )
