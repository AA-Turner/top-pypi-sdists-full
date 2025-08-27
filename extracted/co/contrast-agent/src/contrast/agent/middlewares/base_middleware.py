# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations


from functools import cached_property
import threading
import contextlib

from contrast_fireball import (
    AssessFinding,
    AssessRoute,
    AssessRouteObservation,
    Browser,
    ObservedRoute,
)

import contrast
from contrast.reporting import teamserver_messages
from contrast.agent import (
    agent_state,
    scope,
    thread_watcher,
    request_state,
)
from contrast.agent.protect import input_analysis
from contrast.agent.request_context import RequestContext
from contrast.agent.assess.rules.response.xss import analyze_xss
from contrast.agent.assess.rules.response.analyze import analyze_response_rules
from contrast.agent.assess.preflight import update_preflight_hashes
from contrast.agent.middlewares import response_wrappers
from contrast.agent.middlewares.response_wrappers.base_response_wrapper import (
    BaseResponseWrapper,
)
from contrast.api.attack import ProtectResponse
from contrast.utils.loggers.logger import (
    setup_basic_agent_logger,
)
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils import timer
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


def _log_response_info(response: BaseResponseWrapper):
    if response is None:
        logger.debug("No response info for this request")
        return
    logger.debug(
        "Response summary",
        status_code=response.status_code,
        content_length=response.headers.get("content-length", ""),
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
        # id will be different across processes but also for multiple middlewares
        # within the same process
        self.id = id(self)
        self.settings = None
        self.request_start_time = None

        agent_state.initialize()

        self.settings = agent_state.get_settings()
        if not self.is_agent_enabled():
            return

        self.reporting_client = agent_state.module.reporting_client

    @contextlib.contextmanager
    def request_context_stack(self, request_method: str, request_path: str):
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
        self, stack: contextlib.ExitStack, context: RequestContext
    ):
        """
        Enter the pre-request contexts expected before calling the handler with the agent.
        """
        stack.enter_context(contrast.lifespan(context))
        if context.observe_enabled and self.reporting_client is not None:
            context.observability_trace = stack.enter_context(
                self.reporting_client.observability_trace(send_trace=True)
            )
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

    def should_analyze_request(self, environ) -> RequestContext | None:
        """
        Determine if request should be analyzed based on configured settings.

        While returning different types of objects based on logic is not a good
        pattern, in this case it's an optimization that allows us to create
        the request context obj when we need it.
        """
        path = environ.get("PATH_INFO")

        if not self.is_agent_enabled():
            logger.debug("Will not analyze request: agent disabled.", path=path)
            return None

        # TODO: PYT-3778 As an optimization, we could skip analysis here (return False)
        # if none of the individual agent modes are enabled

        context = RequestContext(
            environ,
            assess_enabled=agent_state.module.assess_enabled,
            exclusions=agent_state.module.exclusions,
            request_data_masker=agent_state.module.request_data_masker,
            event_handlers=agent_state.module.event_handlers,
            observe_enabled=agent_state.module.observe_enabled,
            protect_enabled=agent_state.module.protect_enabled,
        )

        if context.evaluate_exclusions():
            logger.debug(
                "Will not analyze request: request meets exclusions.", path=path
            )
            return None

        from contrast.agent.assess import sampling

        if sampling.meets_criteria(context, agent_state.module.sampling_cfg):
            logger.debug(
                "Will not run Assess analysis on request: request meets sampling.",
                path=path,
            )
            context.assess_enabled = False

        return context

    @fail_loudly("Unable to do handle_ensure")
    def handle_ensure(self, context: RequestContext, request):
        """
        Method that should run for all middlewares AFTER every request is made.
        """
        thread_watcher.ensure_running(agent_state.module)

        if request is not None:
            if context.assess_enabled:
                self._handle_observed_route(context, request)
                update_preflight_hashes(context)
            if context.observe_enabled and (
                (trace := context.observability_trace) is not None
            ):
                http_span_attrs = context.request.get_otel_attributes()
                if context.path_template is not None:
                    http_span_attrs["http.route"] = context.path_template
                if context.response:
                    http_span_attrs.update(
                        response_wrappers.get_otel_attributes(context.response)
                    )
                if context.response_exception is not None:
                    error_type = type(context.response_exception)
                    http_span_attrs["error.type"] = (
                        f"{error_type.__module__}.{error_type.__qualname__}"
                    )
                trace.update(http_span_attrs)

        logger.debug("Sending final messages for reporting.")
        for msg in self.final_ts_messages(context):
            self.reporting_client.add_message(msg)

        self.send_library_observations(context)
        self.send_findings(context)
        self.send_route_observation(context)
        self.send_inventory_components(context)

        _log_response_info(context.response)

        agent_state.set_first_request(False)

    def final_ts_messages(self, context):
        if context is None:
            return []

        messages = []
        if context.attacks:
            messages.append(
                teamserver_messages.ApplicationActivity(
                    attacks=context.attacks,
                    request=context.request,
                    request_data_masker=context.request_data_masker,
                )
            )

        return messages

    def send_library_observations(self, context):
        if library_observations := context.observed_library_usage:
            self.reporting_client.new_library_observations(library_observations)

    def send_findings(self, context):
        if (
            context.assess_enabled
            and context.findings is not None
            and len(context.findings) > 0
        ):
            # Masking can be expensive for large requests, so we only do it if
            # we're sending a message that requires masking, such as findings (here)
            # or application activity (for Protect attack samples).
            if context.request_data_masker:
                context.request_data_masker.mask_sensitive_data(context.request)

            self.reporting_client.new_findings(context.findings, context.request)

    def send_route_observation(self, context):
        # Per the spec, we do not report an observed route if the route signature or URL is empty.
        # Also, we don't report on a subset of error response codes. (PYT-3306)
        if (
            context.assess_enabled
            and context.response is not None
            and self._desired_observation_response_code(context.response.status_code)
            and context.observed_route.signature
            and context.observed_route.url
        ):
            self.reporting_client.new_observed_route(context.observed_route)

    def send_inventory_components(self, context: RequestContext):
        if (
            self.reporting_client is not None
            and context.request is not None
            and context.request.user_agent
        ):
            self.reporting_client.new_inventory_components(
                [Browser(context.request.user_agent)]
            )

    @fail_loudly("Failed to run prefilter.")
    def prefilter(self, context: RequestContext):
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
          in the request context.

        We then call to each rule to determine if they have any special prefilter actions, whether due to not being
        implemented in agent-lib or b/c they need special analysis.
        """
        logger.debug("PROTECT: Running Agent prefilter.")

        input_analysis.analyze_inputs()

        for rule in self.settings.protect_rules.values():
            if rule.is_prefilter():
                rule.prefilter()

    @fail_loudly("Unable to do postfilter")
    def postfilter(self, context):
        """
        For all postfilter enabled rules.
        """
        if context.protect_enabled:
            self.postfilter_protect(context)

        if context.assess_enabled:
            self.response_analysis(context)

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
    def response_analysis(self, context):
        """
        Run postfilter for any assess rules. Reflected xss rule runs by default.
        May be overridden in child classes.

        If the response content type matches a allowed content type, do not run
        assess xss response analysis. This is because the security team
        considers reflected xss within these content types to be a false positive.
        """
        logger.debug("ASSESS: Running response analysis")

        analyze_xss(context, self.trigger_node)
        analyze_response_rules(context)

    @fail_quietly("Failed to run postfilter protect.")
    def postfilter_protect(self, context):
        logger.debug("PROTECT: Running Agent postfilter.")

        for rule in self.settings.protect_rules.values():
            if rule.is_postfilter():
                rule.postfilter()

    @fail_loudly("Unable to do check_for_blocked")
    def check_for_blocked(self, context: RequestContext):
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
        for attack in context.attacks:
            if attack.response == ProtectResponse.BLOCKED:
                raise contrast.SecurityException(rule_name=attack.rule_id)

    def _desired_observation_response_code(self, response_code: int) -> bool:
        """
        If we're filtering route observation by response code, determine if the
        one provided is desired or not. We desire any non-error response by
        default, or any response if filtering has been disabled by the user.
        """
        return response_code not in (
            403,
            404,
            405,
            501,
        ) or self.settings.config.get("agent.route_coverage.report_on_error")

    def _handle_observed_route(self, context: RequestContext, request) -> None:
        """
        Perform any necessary actions related to the observed route (for Assess). By the
        time this function is called, framework-specific logic should have identified
        the route signature for this request, if available.
        """
        context.observed_route = ObservedRoute(
            signature=self._get_signature(context, request),
            url=context.request.get_normalized_uri(),
            verb=request.method,
            sources=context.observed_route.sources,
        )
        logger.debug(
            "stored observed route on context",
            observed_route=context.observed_route,
        )
        self._append_route_to_findings(context.observed_route, context.findings)

    def _get_signature(self, context: RequestContext, request) -> str:
        """
        There are a few different strategies we might use to obtain a route signature.
        In order of preference:

        1.  Obtain a signature at some point during the request; this string is set on
            `context.signature`. For supported frameworks, this is accomplished with
            framework-specific patches. One exception to this is aiohttp, where it
            happens directly in the middleware. It is essential that for a particular
            route this signature exactly matches the one found during route discovery.

        2.  If context.signature isn't set, we didn't get any framework-specific
            information about the view function. In this case we use the request's
            normalized URI as the signature. We expect to hit this case in pure WSGI /
            ASGI.
        """
        if context.signature:
            return context.signature

        logger.debug(
            "Did not find a view function signature for the current request. "
            "Falling back on normalized URI."
        )
        return context.request.get_normalized_uri()

    def _append_route_to_findings(
        self, observed_route: ObservedRoute, findings: list[AssessFinding]
    ):
        """
        Append the observed route to any existing findings. We can't necessarily do this
        at finding creation time, because we might not have route info yet.
        """
        if not findings:
            logger.debug("No findings for the current request")
            return

        for finding in findings:
            if not finding.routes:
                logger.debug(
                    "Appending route %s:%s to %s",
                    observed_route.verb,
                    observed_route.url,
                    finding.rule_id,
                )
                finding.routes.append(
                    AssessRoute(
                        count=1,
                        signature=observed_route.signature,
                        observations=[
                            AssessRouteObservation(
                                url=observed_route.url, verb=observed_route.verb or ""
                            )
                        ],
                    )
                )
