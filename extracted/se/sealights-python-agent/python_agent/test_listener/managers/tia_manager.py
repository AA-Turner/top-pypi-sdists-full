import logging
import time

from python_agent.common.constants import TEST_RECOMMENDATION, TestSelectionStatus
from python_agent.common.http.backend_proxy import BackendProxy
from python_agent.common.log.console_message_renderer import ConsoleMessageTemplates

log = logging.getLogger(__name__)


class TIAManager(object):
    def __init__(self, config_data):
        self.config_data = config_data
        self.backend_proxy = BackendProxy(config_data)

    def get_excluded_tests(self):
        if not self.config_data.testSelection["enable"]:
            log.warning("Test recommendations disabled by configuration")
            self.config_data.testSelectionStatus = (
                TestSelectionStatus.DISABLED_BY_CONFIGURATION
            )

            return []
        test_recommendations = self.get_recommendations()
        status = self.resolve_test_selection_status(test_recommendations)
        self.config_data.testSelectionStatus = status
        self._send_tia_console_message(status, test_recommendations)
        if (
            self.config_data.testSelectionStatus
            != TestSelectionStatus.RECOMMENDED_TESTS
        ):
            return []
        return test_recommendations.get("excludedTests", [])

    def get_recommendations(self):
        test_recommendations = {
            "testSelectionEnabled": False,
            "recommendationSetStatus": TEST_RECOMMENDATION.RSS_NOT_READY,
            "recommendedTests": [],
            "excludedTests": [],
        }
        interval_sec = self.config_data.testSelection["interval"]
        timeout_sec = self.config_data.testSelection["timeout"]
        interval_sec = (
            interval_sec if interval_sec >= 0 else TEST_RECOMMENDATION.interval_sec
        )
        timeout_sec = (
            timeout_sec if timeout_sec >= 0 else TEST_RECOMMENDATION.timeout_sec
        )

        if timeout_sec == 0 or interval_sec == 0:
            test_recommendations = (
                self.backend_proxy.try_get_recommendations(self.config_data)
                or test_recommendations
            )
            return test_recommendations

        n_retry = 0
        while timeout_sec > 0 and self.is_status_retryable(
            test_recommendations.get(TEST_RECOMMENDATION.RSS)
        ):
            test_recommendations = (
                self.backend_proxy.try_get_recommendations(self.config_data)
                or test_recommendations
            )
            if not (self.is_selection_enabled_and_not_ready(test_recommendations)):
                return test_recommendations
            n_retry += 1
            time.sleep(interval_sec)
            timeout_sec -= interval_sec
            log.debug(
                "Failed to receive test recommendations. remain %d retry"
                % (timeout_sec / interval_sec)
            )
        else:
            log.warning(
                "did not get test recommendations after %d tries and %d seconds"
                % (n_retry, timeout_sec)
            )
            return test_recommendations

    def is_selection_enabled_and_not_ready(self, test_recommendations):
        return (
            test_recommendations.get(TEST_RECOMMENDATION.TEST_SELECTION_ENABLED)
            and test_recommendations.get(TEST_RECOMMENDATION.RSS)
            == TEST_RECOMMENDATION.RSS_NOT_READY
        )

    def resolve_test_selection_status(self, test_recommendations):
        if not test_recommendations.get(
            TEST_RECOMMENDATION.TEST_SELECTION_ENABLED, False
        ):
            return TestSelectionStatus.DISABLED
        recommendation_set_status = test_recommendations.get(TEST_RECOMMENDATION.RSS)
        if recommendation_set_status == TEST_RECOMMENDATION.RSS_NOT_READY:
            return TestSelectionStatus.RECOMMENDATIONS_TIMEOUT
        elif recommendation_set_status == TEST_RECOMMENDATION.RSS_READY:
            return TestSelectionStatus.RECOMMENDED_TESTS
        elif recommendation_set_status == TEST_RECOMMENDATION.RSS_ERROR:
            return TestSelectionStatus.ERROR
        elif recommendation_set_status == TEST_RECOMMENDATION.RSS_WONT_BE_READY:
            return TestSelectionStatus.RECOMMENDATIONS_TIMEOUT_SERVER
        elif recommendation_set_status == TEST_RECOMMENDATION.RSS_NO_HISTORY:
            return TestSelectionStatus.DISABLED
        else:
            return TestSelectionStatus.ERROR

    def is_status_retryable(self, recommendation_set_status):
        return recommendation_set_status != TEST_RECOMMENDATION.RSS_WONT_BE_READY

    def _send_tia_console_message(self, status, test_recommendations):
        if status == TestSelectionStatus.DISABLED_BY_CONFIGURATION:
            return
        recommendation_set_status = test_recommendations.get(TEST_RECOMMENDATION.RSS)
        exclusions = None
        template = None
        if status == TestSelectionStatus.DISABLED:
            template = "common.test-listener.tia-recommendations-disabled"
        elif recommendation_set_status == TEST_RECOMMENDATION.RSS_READY:
            template = "common.test-listener.tia-recommendations-received"
            exclusions = len(test_recommendations.get("excludedTests") or [])
        elif recommendation_set_status == TEST_RECOMMENDATION.RSS_NOT_READY:
            template = "common.test-listener.tia-recommendations-not-ready"
        elif recommendation_set_status == TEST_RECOMMENDATION.RSS_WONT_BE_READY:
            template = "common.test-listener.tia-recommendations-not-provided"
        elif recommendation_set_status == TEST_RECOMMENDATION.RSS_ERROR or status in [
            TestSelectionStatus.ERROR,
            TestSelectionStatus.RECOMMENDATIONS_TIMEOUT,
            TestSelectionStatus.RECOMMENDATIONS_TIMEOUT_SERVER,
        ]:
            template = "common.test-listener.tia-recommendations-failed"
        if template:
            if exclusions is not None:
                ConsoleMessageTemplates.render_and_print(template, count=exclusions)
            else:
                ConsoleMessageTemplates.render_and_print(template)
