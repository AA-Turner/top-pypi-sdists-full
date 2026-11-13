# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import replace
from functools import cached_property
from typing import TYPE_CHECKING

from contrast_fireball import (
    AssessFinding,
    AssessRoute,
    AssessRouteObservation,
    Browser,
    ObservedRoute,
    ProtectEventSample,
    RouteSource,
)

import contrast
from contrast.agent import agent_state, scope, thread_watcher
from contrast.agent.assess.preflight import finding_hash, route_hash
from contrast.agent.middlewares import response_wrappers
from contrast.agent.request import Request
from contrast.reporting.request_masker import RequestMasker
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.digest_utils import Digest
from contrast.utils.loggers.logger import security_log_attack
from contrast_vendor import structlog as logging

if TYPE_CHECKING:
    from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
    from contrast.agent.exclusions import Exclusions
    from contrast.agent.middlewares.response_wrappers.base_response_wrapper import (
        BaseResponseWrapper,
    )
    from contrast.agent.policy.registry_v2 import EventHandler
    from contrast.reporting.fireball import ObservabilityTrace

logger = logging.getLogger("contrast")


class ContrastContext:
    @scope.contrast_scope()
    def __init__(
        self,
        *,
        event_handlers: dict[str, list[EventHandler]] | None = None,
        assess_enabled: bool = False,
        observe_enabled: bool = False,
        protect_enabled: bool = False,
        shield_enabled: bool = False,
    ):
        self.event_handlers: dict[str, list[EventHandler]] = event_handlers or {}

        self.assess_enabled = assess_enabled
        self.observe_enabled = observe_enabled
        self.protect_enabled = protect_enabled
        self.shield_enabled = shield_enabled

        self.attack_events: list[ProtectEventSample] = []
        self.findings: list[AssessFinding] = []

        self.source_count = 0
        self.propagation_count = 0
        self.max_sources_logged = False
        self.max_propagators_logged = False

        self.observability_trace: ObservabilityTrace | None = None

    @contextmanager
    def set_contextvar(self):
        """
        Set & reset the CONTEXT contextvar. Unlike `lifespan`, this does not run
        teardown on exit.

        py313 - `set()` itself is a contextmanager in 3.14+. It should be possible to
        make use of that here.
        """
        token = contrast.CONTEXT.set(self)
        try:
            yield self
        finally:
            contrast.CONTEXT.reset(token)

    @contextmanager
    def lifespan(self):
        with self.set_contextvar():
            try:
                yield self
            finally:
                self._teardown()

    @property
    def disabled(self) -> bool:
        return (
            self.assess_enabled is False
            and self.protect_enabled is False
            and self.observe_enabled is False
            # NOTE: ideally, ContrastContext wouldn't be aware of CVE shields
            # because CVE shields run outside of contrast contexts. However,
            # we instrument dangerous capabilities using v2 policy, which only
            # runs outside of Contrast scope, and if a request is started with
            # a disabled ContrastContext, then the WSGI and ASGI middlewares
            # enter Contrast scope for the entire request call. This improves
            # performance, but it's conflating concepts since Contrast scope
            # no longer means "executing within Contrast instrumentation", it's
            # instead closer to "turn off all instrumentation". The former makes
            # sense for v2 policy to exit early on, the latter prevents v2 policy
            # from running outside of request scopes, which isn't ideal.
            # For now, we enable the ContrastContext if shields are enabled, and
            # the base middleware will enter propagation scope if Assess is
            # disabled to preserve some of the performance optimizations.
            and self.shield_enabled is False
        )

    @scope.contrast_scope()
    @fail_loudly("Unable to finalize contrast context")
    def _teardown(self) -> None:
        thread_watcher.ensure_running(agent_state.module)

        self._send_attacks()
        self._send_findings()

    def _send_attacks(self) -> None:
        if self.attack_events:
            agent_state.module.fireball_client.new_protect_events(self.attack_events)
            for sample in self.attack_events:
                security_log_attack(sample)

    def _send_findings(self) -> None:
        if self.findings:
            agent_state.module.fireball_client.new_findings(self.findings)


class WebContext:
    @scope.contrast_scope()
    def __init__(
        self,
        environ,
        *,
        exclusions: Exclusions | None = None,
        request_data_masker: RequestMasker | None = None,
        first_request: bool = False,
    ):
        self.request = Request(environ)
        self.exclusions = exclusions
        self.first_request = first_request
        self.request_data_masker = (
            RequestMasker.new_request_masker(request_data_masker.mask_rules)
            if request_data_masker
            else None
        )

        self.response = None
        self.response_exception: Exception | None = None

        self.input_exclusions = None

        # This contains exclusions that only apply at trigger time based on the source event
        #
        # Storing this attribute here makes typing difficult.
        # WebContext now depends on InputExclusion which depends on WebContext.
        self.input_exclusions_trigger_time = []

        self.excluded_assess_rules = []
        self.excluded_protect_rules = []

        self.user_input_analysis: list[InputAnalysisResult] = []

        self.signature: str | None = None
        self.path_template: str | None = None
        """
        Framework-specific representation of the URL structure for this request. This
        must exactly match the corresponding discovered route's URL. It also must not
        contain any user-specific data (ie never requires masking).

        This is not a normalized URL. Using Contrast's normalization algorithm on the
        concrete path for this request will not produce a correct path template. If a
        path template cannot be obtained from the framework, do not set this value.

        Example (flask): "/users/<user_id>/posts/<int:post_id>"
        """

        self.route_sources: list[RouteSource] = []

    @contextmanager
    def set_contextvar(self):
        """
        Set & reset the WEB_CONTEXT contextvar. Unlike `lifespan`, this does not run
        teardown on exit.

        py313 - `set()` itself is a contextmanager in 3.14+. It should be possible to
        make use of that here.
        """
        token = contrast.WEB_CONTEXT.set(self)
        try:
            yield self
        finally:
            contrast.WEB_CONTEXT.reset(token)

    @contextmanager
    def lifespan(self):
        assert (orig_contrast_context := contrast.CONTEXT.get()) is not None
        with self.set_contextvar():
            try:
                yield self
            finally:
                self._teardown()
                assert contrast.CONTEXT.get() is orig_contrast_context

    @scope.contrast_scope()
    @fail_loudly("Unable to finalize web context")
    def _teardown(self) -> None:
        """
        Perform actions that should run for all middlewares after every request,
        once this WebContext is no longer needed. Requires getting the active
        ContrastContext; this should always exist, since its lifetime always encompasses
        WebContext's.
        """
        context = contrast.CONTEXT.get()
        if context is None:
            logger.debug(
                "WARNING: ContrastContext doesn't exist in WebContext teardown"
            )
            return

        if context.assess_enabled:
            observed_route = ObservedRoute(
                signature=self._get_signature(),
                url=self.request.get_normalized_uri(),
                verb=self.request.method,
                sources=self.route_sources,
            )
            logger.debug("observed route", observed_route=observed_route)
            self._send_route_observation(observed_route)
            self._update_findings(context, observed_route)

        if context.observe_enabled and (
            (trace := context.observability_trace) is not None
        ):
            http_span_attrs = self.request.get_otel_attributes()
            if self.path_template is not None:
                http_span_attrs["http.route"] = self.path_template
            if self.response:
                http_span_attrs.update(
                    response_wrappers.get_otel_attributes(self.response)
                )
            if self.response_exception is not None:
                error_type = type(self.response_exception)
                http_span_attrs["error.type"] = (
                    f"{error_type.__module__}.{error_type.__qualname__}"
                )
            trace.update(http_span_attrs)

        self._send_inventory_components()
        self._log_response_info()

    def _get_signature(self) -> str:
        """
        There are a few different strategies we might use to obtain a route signature.
        In order of preference:

        1.  Obtain a signature at some point during the request; this string is set on
            `WEB_CONTEXT.signature`. For supported frameworks, this is accomplished with
            framework-specific patches. One exception to this is aiohttp, where it
            happens directly in the middleware. It is essential that for a particular
            route this signature exactly matches the one found during route discovery.

        2.  If the web context's signature isn't set, we didn't get any framework-
            specific information about the view function. In this case we use the
            request's normalized URI as the signature. We expect to hit this case in
            pure WSGI / ASGI.
        """
        if self.signature:
            return self.signature

        logger.debug(
            "Did not find a view function signature for the current request. "
            "Falling back on normalized URI."
        )
        return self.request.get_normalized_uri()

    def _send_route_observation(self, observed_route: ObservedRoute) -> None:
        # Per the spec, we do not report an observed route if the route signature or
        # URL is empty. Also, we don't report on a subset of error response codes.
        # (PYT-3306)
        if (
            self.response is not None
            and self._desired_observation_response_code(self.response.status_code)
            and observed_route.signature
            and observed_route.url
        ):
            agent_state.module.fireball_client.new_observed_route(observed_route)

    @fail_loudly("Failed to update findings")
    def _update_findings(
        self, context: ContrastContext, observed_route: ObservedRoute
    ) -> None:
        """
        Attach the observed route and request to this request's findings, and calculate
        preflight hashes.
        """
        if not context.findings:
            logger.debug("No findings for the current request")
            return

        self._attach_observed_route_to_findings(context, observed_route)
        self._attach_request_to_findings(context)
        self._update_preflight_hashes(context, observed_route)

    def _attach_observed_route_to_findings(
        self, context: ContrastContext, observed_route: ObservedRoute
    ) -> None:
        for finding in context.findings:
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
                                url=observed_route.url,
                                verb=observed_route.verb or "",
                            )
                        ],
                    )
                )

    def _attach_request_to_findings(self, context: ContrastContext) -> None:
        if self.request_data_masker:
            self.request_data_masker.mask_sensitive_data(self.request)

        fireball_request = self.request.to_fireball_request()
        context.findings[:] = [
            replace(finding, request=fireball_request) for finding in context.findings
        ]

    def _update_preflight_hashes(
        self, context: ContrastContext, observed_route: ObservedRoute
    ) -> None:
        web_route_hash = route_hash(self, observed_route)
        context.findings = [
            replace(finding, hash=finding_hash(finding, web_route_hash))
            for finding in context.findings
        ]

    @staticmethod
    def _desired_observation_response_code(response_code: int) -> bool:
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
        ) or agent_state.get_settings().config.get(
            "agent.route_coverage.report_on_error"
        )

    def _send_inventory_components(self) -> None:
        if (
            agent_state.module.fireball_client is not None
            and self.request is not None
            and self.request.user_agent
        ):
            agent_state.module.fireball_client.new_inventory_components(
                [Browser(self.request.user_agent)]
            )

    def _log_response_info(self) -> None:
        if self.response is None:
            logger.debug("No response info for this request")
            return
        logger.debug(
            "Response summary",
            status_code=self.response.status_code,
            content_length=self.response.headers.get("content-length", ""),
        )

    @cached_property
    @fail_quietly("Unable to compute request hash")
    def hash(self) -> str | None:
        """
        Generates a CRC32 checksum for the request based on the request method,
        normalized uri and content length.
        """
        hasher = Digest()

        hasher.update(self.request.method + self.request.get_normalized_uri())
        return hasher.finish()

    def extract_response(self, response: BaseResponseWrapper):
        """
        Fully generate / iterate over the response body and store a reference to the
        response object on this web context.

        This function must run as though it were running in the application directly; it
        must not run in scope, and any errors during body iteration must be raised
        externally (not caught by Contrast internal machinery).

        Some applications generate response bodies lazily, meaning content is produced
        at response body iteration time. This is particularly common in apps using html
        template rendering. It's important that body iteration does not occur in scope
        so that dataflow will occur normally during content generation.
        """
        assert not scope.in_contrast_scope()
        _ = response.body
        self.response = response
