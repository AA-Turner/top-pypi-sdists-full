# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import contextlib
import threading
from functools import cached_property

from contrast_fireball import ProtectEventOutcome

import contrast
import contrast_rewriter
from contrast.agent import (
    agent_state,
    request_state,
    scope,
)
from contrast.agent.assess.rules.response.analyze import analyze_response_rules
from contrast.agent.assess.rules.response.xss import analyze_xss
from contrast.agent.context import ContrastContext, WebContext
from contrast.agent.exclusions import evaluate_exclusions
from contrast.agent.protect import input_analysis
from contrast.api.attack import PROTECT_RULE_TO_REPORTABLE_NAME
from contrast.utils import timer
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.loggers.logger import setup_basic_agent_logger
from contrast.utils.monitoring import Profiler, tracer

# initialize a basic logger until config is parsed
logger = setup_basic_agent_logger()


@contextlib.contextmanager
def log_request_start_and_end(request_method, request_path):
    start_time = timer.now_ms()
    logger.debug(
        "Beginning request analysis",
        request_method=request_method,
        request_path=request_path,
    )
    try:
        yield
    finally:
        logger.debug(
            "Ending request analysis",
            request_method=request_method,
            request_path=request_path,
        )
        logger.info(
            "request summary",
            request_path=request_path,
            request_method=request_method,
            elapsed_time_ms=timer.now_ms() - start_time,
            # native thread id is useful for lining up viztracer threads to requests,
            # but it requires a syscall so we don't want it in every log message
            native_thread_id=threading.get_native_id(),
        )


class BaseMiddleware:
    """
    BaseMiddleware contains all the initial setup for the framework middlewares

    Requirements:

        1. It's callable
        2. It has call_with_agent
        3. It has call_without_agent

    Pre and post filter calls should not block the flow that this class has.

    Pre -> get_response -> post
    """

    # TODO: PYT-2852 Revisit application name detection
    app_name = ""  # This should be overridden by child classes

    DIAGNOSTIC_ENDPOINT = "/save-contrast-security-config"
    DIAGNOSTIC_ALLOWED_SERVER = "localhost"
    DIAGNOSTIC_ALLOWED_IP = "127.0.0.1"

    @scope.contrast_scope()
    def __init__(self):
        """
        Most agent initialization is now done by the agent state module

        This method calls agent state initialization if it hasn't been done
        already and then loads the settings and reporting client.

        Config scanning still happens here since the behavior is framework-specific.
        """

        if contrast_rewriter.is_startup_profiler_enabled():
            contrast_rewriter.stop_profiler("start_middleware_init")
            contrast_rewriter.start_profiler()

        # id will be different across processes but also for multiple middlewares
        # within the same process
        self.id = id(self)
        self.settings = None
        self.request_start_time = None

        agent_state.initialize()

        self.settings = agent_state.get_settings()
        if not self.is_agent_enabled():
            return

        self.fireball_client = agent_state.module.fireball_client

        if contrast_rewriter.is_startup_profiler_enabled():
            contrast_rewriter.stop_profiler("end_middleware_init")
            contrast_rewriter.start_profiler()

    @contextlib.contextmanager
    def context_stack(self, request_method: str, request_path: str):
        """
        Create a combined context manager for request processing that includes:
        - request_id_context
        - cProfiler (if enabled)
        - log_request_start_and_end
        - VizTracer (if enabled)

        This consolidates duplicate code across middleware implementations.
        """
        with contextlib.ExitStack() as stack:
            # the request_id context manager must come first!
            stack.enter_context(request_state.request_id_context())
            stack.enter_context(log_request_start_and_end(request_method, request_path))

            # TODO: PYT-3337 - we should issue a deprecation warning if
            # agent.python.enable_profiler is used
            profiler_enabled = self.settings.config.get(
                "agent.python.enable_profiler"
            ) or self.settings.config.get("agent.python.profiler.enable")
            if profiler_enabled:
                stack.enter_context(Profiler(request_path))
            tracer_enabled = self.settings.config.get("agent.python.tracer.enable")
            if tracer_enabled:
                min_duration_ms = self.settings.config.get(
                    "agent.python.tracer.min_duration_ms", 0
                )
                stack.enter_context(tracer(request_path, min_duration_ms))

            yield stack

    def enter_agent_call_contexts(
        self,
        stack: contextlib.ExitStack,
        context: ContrastContext,
        web_context: WebContext,
    ):
        """
        Enter the contexts expected before calling the handler with the agent.
        """
        stack.enter_context(context.lifespan())
        if not context.assess_enabled:
            # PERF: Assess C extensions for propagators exit early if they're within
            # propagation scope. This optimization targets requests with Assess sampling,
            # where other modes (like Protect or Shield) cause the request to be called
            # with the agent, but we want Assess functionality off and low-overhead.
            stack.enter_context(scope.propagation_scope())
        if context.observe_enabled and self.fireball_client is not None:
            context.observability_trace = stack.enter_context(
                self.fireball_client.observability_trace(send_trace=True)
            )
        stack.enter_context(web_context.lifespan())
        return stack

    @cached_property
    def name(self):
        raise NotImplementedError("Must implement name")

    def is_agent_enabled(self):
        """
        Agent is considered enabled if the config value for 'enable' is True (or empty,
        defaults to True). Errors during initialization or runtime will set this value
        to False.
        """
        if self.settings is None:
            return False

        return self.settings.is_agent_config_enabled()

    def call_with_agent(self, *args):
        raise NotImplementedError("Must implement call_with_agent")

    def call_without_agent(self, *args):
        """
        The agent does not set context when this function is called so all other patches
        (e.g propagators) that check context shouldn't run.
        """
        raise NotImplementedError("Must implement call_without_agent")

    def should_analyze_request(
        self, environ
    ) -> tuple[ContrastContext, WebContext] | tuple[None, None]:
        """
        Determine if request should be analyzed based on configured settings.

        While returning different types of objects based on logic is not a good
        pattern, in this case it's an optimization that allows us to create
        the ContrastContext obj when we need it.
        """
        path = environ.get("PATH_INFO")

        # TODO: PYT-3778 As an optimization, we could skip analysis here (return False)
        # if none of the individual agent modes are enabled

        context = ContrastContext(
            assess_enabled=agent_state.module.assess_enabled,
            event_handlers=agent_state.module.event_handlers,
            observe_enabled=agent_state.module.observe_enabled,
            protect_enabled=agent_state.module.protect_enabled,
            shield_enabled=agent_state.module.shield_enabled,
        )
        if not self.is_agent_enabled() or context.disabled:
            logger.debug("Will not analyze request: agent disabled.", path=path)
            return None, None

        web_context = WebContext(
            environ,
            exclusions=agent_state.module.exclusions,
            request_data_masker=agent_state.module.request_data_masker,
            first_request=agent_state.claim_first_request(),
        )

        if evaluate_exclusions(web_context, context):
            logger.debug(
                "Will not analyze request: request meets exclusions.", path=path
            )
            return None, None

        from contrast.agent.assess import sampling

        if sampling.meets_criteria(web_context, agent_state.module.sampling_cfg):
            logger.debug(
                "Will not run Assess analysis on request: request meets sampling.",
                path=path,
            )
            context.assess_enabled = False

        return context, web_context

    @fail_loudly("Failed to run prefilter.")
    def prefilter(self, context: ContrastContext):
        """
        Run all of our prefilter, those that happen before handing execution to the application code, here.
        """
        if context.protect_enabled:
            self.prefilter_protect()

    @fail_quietly("Failed to run prefilter protect.")
    def prefilter_protect(self):
        """
        Prefilter - AKA input analysis - is performed mostly with agent-lib but partly in the agent.

        In this method we call on agent-lib to do input analysis, which can result in:
        1. agent-lib finds an attack in which case we block the request
        2. agent-lib returns input analysis to use for later sink / infilter analysis, in which case we store it here
          in the WebContext.

        We then call to each rule to determine if they have any special prefilter actions, whether due to not being
        implemented in agent-lib or b/c they need special analysis.
        """
        logger.debug("PROTECT: Running Agent prefilter.")

        protect_rules = list(self.settings.protect_rules.values())

        input_analysis.analyze_inputs(protect_rules)

        for rule in protect_rules:
            if rule.is_prefilter():
                rule.prefilter()

    @fail_loudly("Unable to do postfilter")
    def postfilter(self, context, web_context: WebContext):
        """
        For all postfilter enabled rules.
        """
        if context.protect_enabled:
            self.postfilter_protect(context)

        if context.assess_enabled:
            self.response_analysis(context, web_context)

    def _process_trigger_handler(self, handler):
        """
        Gather metadata about response handler callback for xss trigger node

        We need to check whether the response handler callback is an instance method or
        not. This affects the way that our policy machinery works, and it also affects
        reporting, so we need to make sure to account for the possibility that handler
        is a method of some class rather than a standalone function.

        This should be called by the `trigger_node` method in child classes.
        """
        module = handler.__module__
        class_name = ""

        if hasattr(handler, "__self__"):
            class_name = handler.__self__.__class__.__name__
            args = (handler.__self__,)
            instance_method = True
        else:
            args = ()
            instance_method = False

        return module, class_name, args, instance_method

    @cached_property
    def trigger_node(self):
        """
        Trigger node property used by assess reflected xss postfilter rule

        This must be overridden by child classes that make use of the reflected
        xss postfilter rule.
        """
        raise NotImplementedError("Children must define trigger_node property")

    @fail_loudly("Unable to do assess response analysis")
    def response_analysis(self, context, web_context: WebContext):
        """
        Run postfilter for any assess rules. Reflected xss rule runs by default.
        May be overridden in child classes.

        If the response content type matches a allowed content type, do not run
        assess xss response analysis. This is because the security team
        considers reflected xss within these content types to be a false positive.
        """
        logger.debug("ASSESS: Running response analysis")

        analyze_xss(self.trigger_node, web_context)
        analyze_response_rules(context, web_context)

    @fail_quietly("Failed to run postfilter protect.")
    def postfilter_protect(self, context):
        logger.debug("PROTECT: Running Agent postfilter.")

        for rule in self.settings.protect_rules.values():
            if rule.is_postfilter():
                rule.postfilter()

    @fail_loudly("Unable to do check_for_blocked")
    def check_for_blocked(self, context: ContrastContext):
        """
        Checks for BLOCK events in case SecurityException was caught by app code

        This should be called by each middleware after the view is generated
        but before returning the response (it can be before or after
        postfilter).

        If we make it to this call, it implies that either no SecurityException
        occurred, or if one did occur, it was caught by the application. If we
        find a BLOCK here, it necessarily implies that an attack was detected
        in the application, but the application caught our exception. If the
        application hadn't caught our exception, we never would have made it
        this far because the exception would have already bubbled up to the
        middleware exception handler. So this is really our first and our last
        opportunity to check for this particular edge case.
        """
        for attack_event in context.attack_events:
            if attack_event.outcome == ProtectEventOutcome.BLOCKED:
                raise contrast.AttackBlockedException(
                    rule_name=PROTECT_RULE_TO_REPORTABLE_NAME[
                        attack_event.rule.__class__
                    ]
                )
