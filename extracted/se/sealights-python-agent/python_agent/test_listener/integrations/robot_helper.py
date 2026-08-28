import logging
import os

from python_agent.common import constants
from python_agent.common.configuration_manager import ConfigurationManager
from python_agent.test_listener.coloring.robot_coloring import RobotBrowserColoring
from python_agent.test_listener.managers.agent_manager import AgentManager
from python_agent.test_listener.sealights_api import SeaLightsAPI
from python_agent.utils import disableable, retries

log = logging.getLogger(__name__)

# Robot statuses that are not PASS, FAIL, or SKIP (NOT RUN, for a test whose
# keywords never ran) report as passed, matching the other integrations, which
# treat "not failed and not skipped" as passed.
_RESULT_BY_ROBOT_STATUS = {"FAIL": "failed", "SKIP": "skipped"}

# Contract C5. The same two keys the in-page browser agent reads, spelled as
# coloring/playwright_helper.py already spells them in its set:context script.
BAGGAGE_KEY_TEST_NAME = "x-sl-test-name"
BAGGAGE_KEY_TEST_SESSION_ID = "x-sl-test-session-id"

SL_TRACER_NAME = "sl-test-listener"

try:
    from opentelemetry import baggage, context, trace

    _tracer = trace.get_tracer(SL_TRACER_NAME)
except ImportError:
    # Rule 21: opentelemetry-api lives only in the pinned [robot] extra, so a
    # customer who installed the agent without it gets a run that differs from
    # an instrumented one in nothing but the span (AC17).
    baggage = context = trace = _tracer = None


def resolve_test_name(data, test_name_format):
    """The one identity string for a Robot test (contract C4).

    This is what `testStart`, `testEnd`, TIA matching, browser baggage, and the
    OpenTelemetry span name all use, so slices 4 through 8 must call this rather
    than read the attributes themselves: a partial switch between formats would
    attribute footprints to a different name than the events.

    `full_name` is Robot 7's spelling of the suite-qualified name and `longname`
    is the pre-7 one. Both carry an identical value on 7.4.2 (measured), so the
    fallback exists for Robot 6 and earlier.
    """
    if test_name_format == constants.TEST_NAME_FORMAT_SHORT:
        return data.name
    return (
        getattr(data, "full_name", None) or getattr(data, "longname", None) or data.name
    )


class SealightsRobotListener(object):
    """Robot Framework listener (API v3) that owns the Sealights execution.

    `sl-python robot` registers this class through `--listener <dotted path>`,
    which is the same channel a pabot worker loads it through (C9), so a serial
    run and a worker run share one code path. It is not a documented customer
    entry point.

    Listener API v3 is required: `start_keyword` and `end_keyword` reached v3
    only in Robot Framework 7.0, and the browser coloring in C7 is built on
    them.
    """

    ROBOT_LISTENER_API_VERSION = 3

    # Rule 20: the process whose execution this class already owns. Robot builds
    # one instance per registration, and a pabot worker sees the registration
    # twice whenever `ROBOT_OPTIONS` carries it: pabot merges `ROBOT_OPTIONS`
    # into the worker's command line and the worker's own `robot` applies
    # `ROBOT_OPTIONS` again from the inherited environment. The parent cannot
    # prevent that by argument construction (measured against pabot 5.2.2), and
    # two owners open two executions and report every test twice with nothing in
    # the output to say so. Keyed on pid so a forked child claims for itself.
    _owner_pid = None

    def __init__(self):
        self.execution_id = None
        self.config_data = self._claim_this_process()
        self._open_attempted = False
        self._excluded_tests = None
        self._spans = {}
        self._coloring = RobotBrowserColoring()
        # The name of the test currently running, and the seam's guard against
        # coloring a keyword that runs outside one: a Suite Teardown keyword
        # would otherwise be colored with the identity of the test that just
        # ended (SLDEV-28058, 48bd51c).
        self._running_test_name = None

    @classmethod
    def _claim_this_process(cls):
        """The config for the one listener that reports, `None` for the rest.

        A losing instance keeps every callback inert through the same `None`
        path an uninitialized agent takes, so there is one code path for
        "reports nothing" rather than two.
        """
        if cls._owner_pid == os.getpid():
            log.warning(
                "A Sealights Robot listener is already registered in this "
                "process, so this registration will report nothing. Two would "
                "open two executions and report every test twice."
            )
            return None
        config_data = cls._resolve_config_data()
        if config_data is not None:
            cls._owner_pid = os.getpid()
        return config_data

    @staticmethod
    def _resolve_config_data():
        """The config of the agent in this process, building one if a worker.

        `AgentManager()` raises when no agent exists. Under `sl-python robot`
        the CLI already built one; a pabot worker is a bare `robot` process, so
        this is where its agent comes from (C9).
        """
        try:
            return AgentManager().config_data
        except Exception as e:
            log.debug("No Sealights agent exists in this process. Error: %s" % str(e))
        return SealightsRobotListener._bootstrap_worker_agent()

    @staticmethod
    def _bootstrap_worker_agent():
        """Build this process's agent from what the pabot parent published.

        There is no `sl-python` in a worker: pabot spawns the bare `robot`
        command, so the environment variable the parent wrote is the whole
        channel, and `is_master=False` is what keeps the worker from behaving
        as the run's owner. `pytest_helper.try_initialize_agent_on_xdist_node`
        is the same shape.

        Ordering is load-bearing.
        `try_load_configuration_from_config_environment_variable` is a
        `__dict__.update` onto an existing `ConfigData`, so it has to run before
        the manager is built; the other way round the worker would talk to the
        default backend with no build session id.

        Absent variable means this is a Robot run that reached the listener
        without the CLI at all. `None` then short-circuits every `@disableable`
        callback instead of failing the customer's run.
        """
        if not os.environ.get(constants.CONFIG_ENV_VARIABLE):
            log.error(
                "Sealights agent is not initialized and no configuration was "
                "published, so nothing will be reported for this run."
            )
            return None
        try:
            configuration_manager = ConfigurationManager()
            configuration_manager.try_load_configuration_from_config_environment_variable()
            config_data = configuration_manager.config_data
            AgentManager(config_data=config_data, is_master=False)
            log.info("Sealights agent initialized for a pabot worker")
            return config_data
        except Exception as e:
            log.error(
                "Failed initializing a Sealights worker agent. Error: %s" % str(e)
            )
            return None

    def start_suite(self, data, result):
        # Robot fires suite hooks nested, once per suite in the tree, while
        # exactly one execution exists per runner process (Rule 7).
        if not self._open_attempted:
            self._open_attempted = True
            self._open_execution()
        # Library imports are suite-scoped, so which browser libraries are in
        # use is re-established per suite rather than once per run.
        self._coloring.reset_libraries()
        # Every suite in the tree carries its own direct tests, so exclusions
        # apply on each callback even though they are fetched only on the first.
        self._exclude_recommended_tests(data)

    def start_test(self, data, result):
        # No execution means the open was refused, and the C5 baggage is built
        # from its id: a span for a run the backend has no record of colors
        # browser footprints with a session nothing can attribute.
        if not self.execution_id:
            return
        test_name = resolve_test_name(data, self._test_name_format())
        self._running_test_name = test_name
        self._open_span(test_name)
        # Handles that already exist, which is every browser opened in a
        # Suite Setup: no end_keyword fires for those before the test body.
        self._coloring.color(self.execution_id, test_name)
        self._notify_test_start(test_name)

    def start_keyword(self, data, result):
        # Flushing a browser the keyword is about to close has to happen here:
        # by end_keyword the handle is gone (C7). Coloring does not, and must
        # not, happen here: the handles this keyword creates do not exist yet.
        if self._running_test_name and self._coloring.closes_a_browser(data.name):
            self._coloring.flush()

    def end_keyword(self, data, result):
        # Covers browsers opened in the test body, in a Test Setup, or inside a
        # compound user keyword, and re-colors after navigation. The keyword's
        # `owner` is deliberately not consulted: gating on it would skip every
        # wrapper keyword a customer has written (C6).
        if self._running_test_name:
            self._coloring.color(self.execution_id, self._running_test_name)

    def end_test(self, data, result):
        if not self.execution_id:
            return
        test_name = resolve_test_name(data, self._test_name_format())
        self._coloring.flush()
        self._coloring.clear()
        self._running_test_name = None
        self._notify_test_end(
            test_name,
            # notify_test_end multiplies by 1000, as behave's seconds require;
            # Robot's elapsedtime is already milliseconds.
            duration=result.elapsedtime / 1000.0,
            status=_RESULT_BY_ROBOT_STATUS.get(result.status, "passed"),
        )
        self._close_span(test_name)

    def close(self):
        # `close`, not `end_suite`: suite hooks nest, so finding the outermost
        # end_suite would mean counting depth. `close` fires exactly once.
        # No execution_id means the open never succeeded, so there is nothing
        # to close and reporting one would invent an execution.
        if self.execution_id:
            self._close_execution()

    def _open_span(self, test_name):
        """Contract C8: one span per test, carrying the C5 baggage.

        The context is attached rather than only built, so any OpenTelemetry
        instrumentation the customer's keywords reach propagates the test
        identity outward. The attach token is what `_close_span` detaches.
        """
        if _tracer is None or test_name in self._spans:
            return
        try:
            span = _tracer.start_span(test_name)
            span_context = trace.set_span_in_context(span, context.get_current())
            span_context = baggage.set_baggage(
                BAGGAGE_KEY_TEST_NAME, test_name, span_context
            )
            span_context = baggage.set_baggage(
                BAGGAGE_KEY_TEST_SESSION_ID, self.execution_id, span_context
            )
            self._spans[test_name] = (span, context.attach(span_context))
        except Exception as e:
            log.warning(
                "Failed to start a span for %s. Error: %s" % (test_name, str(e))
            )

    def _close_span(self, test_name):
        span_and_token = self._spans.pop(test_name, None)
        if span_and_token is None:
            return
        span, token = span_and_token
        try:
            # Detach before ending: leaving the context attached would carry
            # this test's baggage into the next one.
            context.detach(token)
            span.end()
        except Exception as e:
            log.warning(
                "Failed to end the span for %s. Error: %s" % (test_name, str(e))
            )

    def _exclude_recommended_tests(self, suite):
        excluded_tests = self._excluded_test_names()
        if not excluded_tests:
            return
        test_name_format = self._test_name_format()
        for test in getattr(suite, "tests", None) or []:
            if resolve_test_name(test, test_name_format) not in excluded_tests:
                continue
            try:
                self._skip_inside_robot(test)
                log.info("Set skip on excluded test: %s" % test.name)
            except Exception as e:
                # A model shape this code cannot mutate costs coverage of one
                # test's exclusion, never the customer's run (Rule 22).
                log.error(
                    "Failed to skip excluded test %s. Error: %s" % (test.name, str(e))
                )

    def _excluded_test_names(self):
        """The exclusion set, fetched at most once per process (Rule 10).

        Names are matched against `resolve_test_name`, so a run whose
        `testNameFormat` differs from the one that trained TIA matches nothing.
        That is the same reason C4 freezes identity.
        """
        if self._excluded_tests is None:
            self._excluded_tests = self._fetch_excluded_tests() or set()
        return self._excluded_tests

    @disableable(fail_silently=True)
    def _fetch_excluded_tests(self):
        # No @retries: TIAManager already polls to the constants.TEST_RECOMMENDATION
        # window and answers every failure it sees with zero exclusions, so a
        # retry here would only multiply that window. Rule 10 fails open, which
        # means running everything rather than disabling the agent.
        try:
            return {test.get("name", "") for test in SeaLightsAPI.get_excluded_tests()}
        except Exception as e:
            log.warning("Failed getting excluded tests. Error: %s" % str(e))
            return set()

    @staticmethod
    def _skip_inside_robot(test):
        """Rule 11: the keywords must not execute, and neither must the teardown.

        `create_keyword` appends, so the Skip is moved to the front: Robot runs
        the body in order and Skip aborts the rest, which is what makes this a
        skip rather than a run that merely reports as one. Robot then reports
        the test SKIP, which `end_test` maps to `skipped` for the backend.
        """
        skip_keyword = test.body.create_keyword(name="Skip")
        test.body.pop()
        test.body.insert(0, skip_keyword)
        # A Robot test always has a teardown object; an undefined one is falsy.
        if test.teardown:
            test.teardown = None

    def _test_name_format(self):
        return getattr(
            self.config_data, "testNameFormat", constants.TEST_NAME_FORMAT_FULL
        )

    @disableable(fail_silently=True)
    @retries(log)
    def _open_execution(self):
        execution_id = SeaLightsAPI.create_execution_id()
        SeaLightsAPI.start_execution(execution_id)
        # Assigned only after the backend accepted the open, so a failed open
        # cannot produce a close for an execution that does not exist.
        self.execution_id = execution_id
        log.info("Sealights execution started. Execution Id: %s" % execution_id)

    @disableable(fail_silently=True)
    @retries(log)
    def _notify_test_start(self, test_name):
        SeaLightsAPI.notify_test_start(self.execution_id, test_name)

    @disableable(fail_silently=True)
    @retries(log)
    def _notify_test_end(self, test_name, duration, status):
        SeaLightsAPI.notify_test_end(self.execution_id, test_name, duration, status)

    @disableable(fail_silently=True)
    @retries(log)
    def _close_execution(self):
        # start_execution and end_execution propagate ConnectionError to the
        # caller, unlike push_event and send_all which swallow theirs (Rule
        # 22). @retries is what keeps that out of the customer's Robot run.
        SeaLightsAPI.send_all()
        SeaLightsAPI.end_execution(self.execution_id)
        log.info("Sealights execution ended. Execution Id: %s" % self.execution_id)
