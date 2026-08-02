import logging

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
