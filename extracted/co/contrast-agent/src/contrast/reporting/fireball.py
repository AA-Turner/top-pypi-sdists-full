# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations


from collections import deque
import contextlib
from dataclasses import replace
from enum import Enum
from functools import partial
from typing import Final
from collections.abc import Generator

import contrast
from contrast.agent.disable_reaction import DisableReaction
from contrast.agent.request import Request
from contrast.configuration.agent_config import AgentConfig
from contrast.configuration.config_option import DEFAULT_VALUE_SRC
from contrast.reporting.reporting_client import ReportingClient
from contrast import get_canonical_version
import contrast_fireball

from contrast.utils.configuration_utils import DEFAULT_PATHS
from contrast_vendor import structlog as logging, wrapt

logger = logging.getLogger("contrast")


def _handle_errors(return_value=None) -> wrapt.FunctionWrapper:
    """
    A decorator that catches and logs errors that occur while reporting to Contrast.

    Disabling the agent in response to authentication errors or archived applications
    is handled here.

    Errors that indicate a bug in the agent or Fireball are reported to telemetry.

    This decorator should only be used on Client methods, since it expects the
    wrapped function to be a method with AgentConfig stored on the instance.
    """

    @wrapt.function_wrapper
    def wrapper(wrapped, instance, args, kwargs):
        try:
            return wrapped(*args, **kwargs)
        except contrast_fireball.Error as e:
            if isinstance(
                e,
                (
                    contrast_fireball.ConfigurationError,
                    contrast_fireball.AuthenticationError,
                    contrast_fireball.AppArchivedError,
                ),
            ):
                # These error messages are user-facing. Log them directly without
                # the stack trace to reduce the noise in the message.
                logger.error(e.message)
            else:
                logger.error(
                    "An error occurred while reporting to Contrast", exc_info=e
                )

            if (
                isinstance(
                    e,
                    (
                        contrast_fireball.Panic,
                        contrast_fireball.ArgumentValidationError,
                        contrast_fireball.UnexpectedError,
                    ),
                )
                and contrast.TELEMETRY is not None
            ):
                contrast.TELEMETRY.report_error(e, wrapped)

            if isinstance(
                e,
                (
                    contrast_fireball.AppArchivedError,
                    contrast_fireball.AuthenticationError,
                ),
            ):
                DisableReaction.run(instance.config)

            return return_value

    return wrapper


@wrapt.function_wrapper
def _queue_if_app_uninitialized(wrapped, instance, args, kwargs):
    """
    A decorator that queues the wrapped function call if the application hasn't been
    initialized.

    This decorator should only be used on Client methods.
    """
    if not hasattr(instance, "app_id"):
        instance.queued_postinit_actions.append(partial(wrapped, *args, **kwargs))
        return None
    return wrapped(*args, **kwargs)


class Client(ReportingClient):
    """
    A client for reporting to the Contrast UI using the Fireball library.
    Fireball docs: https://fireball.prod.dotnet.contsec.com/fireball/index.html

    The client will fallback to directly reporting for endpoints that do not
    have Python bindings yet.
    """

    def __init__(self):
        self.config = None
        info = contrast_fireball.get_info()
        super().__init__(instance_id=info["reporting_instance_id"])
        self.queued_postinit_actions = deque(maxlen=10)

    @_handle_errors(return_value=False)
    def initialize_application(self, config: AgentConfig, server_type="") -> bool:
        """
        Initialize an application in the Contrast UI.

        This function must be called before any other reporting functions.
        """

        # Store config on the client for disable reaction on AppArchivedError
        self.config = config

        result = contrast_fireball.initialize_application(
            contrast_fireball.InitOptions(
                app_name=config["application.name"],
                app_path=config["application.path"],
                agent_language=contrast_fireball.AgentLanguage.PYTHON,
                agent_version=get_canonical_version(),
                server_host_name=config["server.name"],
                server_path=config["server.path"],
                server_type=server_type,
                config_paths=list(DEFAULT_PATHS),
                overrides=agent_config_to_plain_dict(config),
            )
        )
        self.app_id = result.data["app_id"]
        config.session_id = result.data["common_config"]["application"].get(
            "session_id", ""
        )
        while self.queued_postinit_actions:
            retry_action = self.queued_postinit_actions.popleft()
            retry_action()

        # This is a workaround to process the startup settings from the UI.
        # Long-term, we'll read the settings from the result, but for now
        # we want to use the well-tested direct response processing behavior.
        return super().initialize_application(config)

    @_queue_if_app_uninitialized
    @_handle_errors()
    def new_discovered_routes(self, routes: set[contrast_fireball.DiscoveredRoute]):
        """
        Report discovered routes to the Contrast UI.

        If an exception occurs, no routes are reported.
        """

        contrast_fireball.new_discovered_routes(self.app_id, list(routes))

    @_handle_errors()
    def new_observed_route(self, route: contrast_fireball.ObservedRoute):
        """
        Record an observed route.

        Routes are reported periodically in batches. This endpoint can be called multiple
        times for the same route, but Fireball will only report duplicate routes at a rate
        of once per minute to avoid overloading TeamServer.
        """

        contrast_fireball.new_observed_route(self.app_id, route)

    @_queue_if_app_uninitialized
    def new_findings(
        self,
        findings: list[contrast_fireball.AssessFinding],
        request: Request | None,
    ):
        """
        Record Assess findings.

        Findings are reported periodically in batches. Failures are handled for each
        individual finding, so that a failure in one finding does not prevent others
        from being reported.
        """
        fireball_request = request.to_fireball_assess_request() if request else None
        for finding in findings:
            self._new_finding(finding, fireball_request)

    @_handle_errors()
    def _new_finding(
        self,
        finding: contrast_fireball.AssessFinding,
        request: contrast_fireball.AssessRequest | None,
    ):
        contrast_fireball.new_finding(self.app_id, replace(finding, request=request))

    @_queue_if_app_uninitialized
    @_handle_errors()
    def new_libraries(self, libraries: list[contrast_fireball.Library]):
        """
        Record libraries that can be imported in the application.
        """
        contrast_fireball.new_libraries(self.app_id, libraries)

    @_queue_if_app_uninitialized
    @_handle_errors()
    def new_library_observations(
        self, observations: list[contrast_fireball.LibraryObservation]
    ):
        """
        Record observations of libraries imported in the application.
        Observations are reported periodically in batches.
        """
        contrast_fireball.new_library_observations(self.app_id, observations)

    @_queue_if_app_uninitialized
    @_handle_errors()
    def new_inventory_components(
        self, components: list[contrast_fireball.InventoryComponent]
    ):
        """
        Record Inventory Components.

        Components are reported periodically in batches. Duplicate items between sends
        will be ignored.
        """
        contrast_fireball.new_inventory_components(self.app_id, components)

    @contextlib.contextmanager
    def observability_trace(
        self,
        *,
        send_trace: bool,
        attributes: contrast_fireball.OtelAttributes | None = None,
    ) -> Generator[ObservabilityTrace | None, None, None]:
        """
        Manages the lifecycle of the root span for observability mode.

        `send_trace` determines whether or not the trace will actually be reported to
        the UI. In the future, we may decide not to send every trace, depending on
        observabilty sampling settings. Traces for requests containing an attack
        (identified by protect) will likely be sent regardless. For now, `send_trace`
        must be given an initial value, but this can be changed later by modifying the
        corresponding attribute on the trace object returned by this contextmanager.
        """
        # A new trace should only be created when a new request comes in to the server.
        # By this point, we must have called `initialize_application`, which sets these
        # critical attributes.
        assert hasattr(self, "app_id")
        assert self.config is not None

        if (
            trace_id := self._start_trace(
                contrast_fireball.SpanType.HttpServerRequest, attributes or {}
            )
        ) is None:
            logger.debug("No trace_id from fireball - not entering root span")
            yield None
            return

        trace = ObservabilityTrace(
            trace_id=trace_id, send_trace=send_trace, client=self
        )
        try:
            yield trace
        finally:
            self._end_trace(trace_id, trace.send_trace)
            logger.debug(
                "Trace sent to Fireball", trace_id=trace_id, send_trace=trace.send_trace
            )

    @_handle_errors()
    def _start_trace(
        self,
        action_type: contrast_fireball.SpanType,
        attributes: contrast_fireball.OtelAttributes,
    ) -> str | None:
        # the undecorated function can only return `str`, but the decorated function
        # returns `None` on error
        params = contrast_fireball.StartTraceParams(
            action_type=action_type,
            attributes=attributes,
        )
        result = contrast_fireball.start_trace(self.app_id, params)
        return result.data.trace_id

    @_handle_errors()
    def _end_trace(self, trace_id: str, send_trace: bool) -> None:
        params = contrast_fireball.EndTraceParams(
            trace_id=trace_id,
            send_trace=send_trace,
        )
        contrast_fireball.end_trace(self.app_id, params)

    @_handle_errors()
    def _update_trace(
        self, trace_id: str, attributes: contrast_fireball.OtelAttributes
    ) -> None:
        params = contrast_fireball.UpdateTraceParams(
            trace_id=trace_id, attributes=attributes
        )
        contrast_fireball.update_trace(self.app_id, params)

    @_handle_errors()
    def _get_trace_info(self, trace_id: str) -> contrast_fireball.TraceInfo | None:
        result = contrast_fireball.get_trace_info(self.app_id, trace_id)
        return result.data

    @_handle_errors()
    def _start_child_span(
        self,
        trace_id: str,
        action_type: contrast_fireball.SpanType,
        attributes: contrast_fireball.OtelAttributes,
        parent_span_id: str | None = None,
    ) -> str | None:
        # the undecorated function can only return `str`, but the decorated function
        # returns `None` on error
        params = contrast_fireball.StartChildSpanParams(
            trace_id=trace_id,
            action_type=action_type,
            attributes=attributes,
            parent_span_id=parent_span_id,
        )
        result = contrast_fireball.start_child_span(self.app_id, params)
        return result.data.id

    @_handle_errors()
    def _end_child_span(self, trace_id: str, span_id: str) -> None:
        params = contrast_fireball.EndChildSpanParams(
            trace_id=trace_id,
            span_id=span_id,
        )
        contrast_fireball.end_child_span(self.app_id, params)

    @_handle_errors()
    def _update_child_span(
        self, trace_id: str, span_id: str, attributes: contrast_fireball.OtelAttributes
    ) -> None:
        params = contrast_fireball.UpdateChildSpanParams(
            trace_id=trace_id,
            span_id=span_id,
            attributes=attributes,
        )
        contrast_fireball.update_child_span(self.app_id, params)


def agent_config_to_plain_dict(config: AgentConfig):
    """
    Convert all set options in the AgentConfig to a plain dictionary.
    """

    def conv(obj: object):
        if isinstance(obj, Enum):
            return obj.name
        return str(obj)

    json_config = {
        key: conv(v)
        for key, opt in config._config.items()
        if opt.source() != DEFAULT_VALUE_SRC and (v := opt.value()) is not None
    }

    # PROD-1745: Make sure to add the artifact hash to the session metadata.
    # This is implemented in get_session_metadata instead of as the
    # ConfigOption.default for application.session_metadata, because we always
    # want to send the artifact hash even if the user has set other session
    # metadata.
    if "application.session_id" not in json_config:
        json_config["application.session_metadata"] = config.get_session_metadata()

    return json_config


class ObservabilityTrace:
    trace_id: Final[str]
    send_trace: bool
    _client: Client

    def __init__(self, trace_id: str, send_trace: bool, client: Client):
        self.trace_id = trace_id
        self.send_trace = send_trace
        self._client = client

    def update(self, attributes: contrast_fireball.OtelAttributes) -> None:
        """
        Updates attributes on an existing trace.
        """
        self._client._update_trace(self.trace_id, attributes)

    def get_info(self) -> contrast_fireball.SpanInfo | None:
        """
        Gets trace info for an unsent trace.

        This function will return None if the root span is not found. Traces are closed
        and unavailable once they are sent.
        """
        if (trace_info := self._client._get_trace_info(self.trace_id)) is None:
            return None
        return trace_info.root_span

    @contextlib.contextmanager
    def child_span(
        self,
        action_type: contrast_fireball.SpanType,
        *,
        attributes: contrast_fireball.OtelAttributes | None = None,
        parent_span_id: str | None = None,
    ) -> Generator[ChildSpan | None, None, None]:
        """
        Manages the lifecycle of a child span for observability mode. The newly created
        child span will be attached to the current trace.
        """
        if (
            span_id := self._client._start_child_span(
                self.trace_id, action_type, attributes or {}, parent_span_id
            )
        ) is None:
            yield None
            return

        child = ChildSpan(span_id, self)
        try:
            yield child
        finally:
            self._client._end_child_span(self.trace_id, span_id)


class ChildSpan:
    span_id: Final[str]
    _trace: ObservabilityTrace

    def __init__(self, span_id: str, trace: ObservabilityTrace):
        self.span_id = span_id
        self._trace = trace

    def update(self, attributes: contrast_fireball.OtelAttributes) -> None:
        """
        Updates a child span with new attributes.
        """
        self._trace._client._update_child_span(
            self._trace.trace_id, self.span_id, attributes
        )
