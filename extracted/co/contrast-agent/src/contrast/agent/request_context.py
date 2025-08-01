# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations


from functools import cached_property
from typing import TYPE_CHECKING

from contrast.agent import scope

from contrast.agent.agent_lib.input_tracing import InputAnalysisResult
from contrast.agent.exclusions import Exclusions
from contrast.agent.middlewares.response_wrappers.base_response_wrapper import (
    BaseResponseWrapper,
)
from contrast.agent.request import Request
from contrast.agent.settings import Settings
from contrast.agent.inventory.library_reader import LibraryObservations
from contrast_fireball import AssessFinding, ObservedRoute
from contrast.reporting.fireball import ObservabilityTrace
from contrast_vendor import structlog as logging
from contrast.utils.digest_utils import Digest
from contrast.utils.decorators import fail_quietly
from contrast.reporting.request_masker import RequestMasker

if TYPE_CHECKING:
    from contrast.agent.policy.registry_v2 import EventHandler

logger = logging.getLogger("contrast")


class RequestContext:
    @scope.contrast_scope()
    def __init__(
        self,
        environ,
        exclusions: Exclusions | None = None,
        request_data_masker: RequestMasker | None = None,
        event_handlers: dict[str, list[EventHandler]] | None = None,
        *,
        assess_enabled: bool = False,
        observe_enabled: bool = False,
        protect_enabled: bool = False,
    ):
        self.request = Request(environ)
        self.response = None
        self.response_exception: Exception | None = None

        # This contains any Observed Library Usage seen during the life of this request.
        self.observed_libraries = LibraryObservations([])

        self.exclusions = exclusions
        self.event_handlers: dict[str, list[EventHandler]] = event_handlers or {}

        self.observability_trace: ObservabilityTrace | None = None

        self.request_data_masker = None

        if request_data_masker:
            self.request_data_masker = RequestMasker.new_request_masker(
                request_data_masker.mask_rules
            )

        # This contains input exclusions that should always apply regardless of rule on this request
        self.input_exclusions = None

        # This contains exclusions that only apply at trigger time based on the source event
        #
        # Storing this attribute here makes typing difficult.
        # RequestContext now depends on InputExclusion which depends on RequestContext.
        self.input_exclusions_trigger_time = []

        self.excluded_assess_rules = []
        self.excluded_protect_rules = []

        # For protect: store attacks made during a request to report at the end
        self.attacks = []

        # For assess: store findings made during a request to report at the end
        self.findings: list[AssessFinding] = []

        self.user_input_analysis: list[InputAnalysisResult] = []
        self.response = None
        self.do_not_track = False

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

        self.observed_route = ObservedRoute("", "", "", [])

        self.assess_enabled = assess_enabled
        self.observe_enabled = observe_enabled
        self.protect_enabled = protect_enabled

        self.source_count = 0
        self.propagation_count = 0
        self.max_sources_logged = False
        self.max_propagators_logged = False

    @property
    def disabled(self) -> bool:
        return (
            self.assess_enabled is False
            and self.protect_enabled is False
            and self.observe_enabled is False
        )

    @property
    def observed_library_usage(self) -> list[LibraryObservations]:
        """
        Returns a list of library observations for libraries imported within the current request.
        """
        return self.observed_libraries.to_list()

    @cached_property
    @fail_quietly("Unable to compute request hash")
    def hash(self) -> str:
        """
        Generates a CRC32 checksum for the request based on the request method,
        normalized uri and content length.
        """
        hasher = Digest()

        hasher.update(self.request.method + self.request.get_normalized_uri())
        return hasher.finish()

    def stop_source_creation(self, source_type, source_name):
        """
        Compare `source_count` to `max_context_source_events` config option
        :return: true if source_count within this request is equal to or
                 greater than configured threshold for source creation
        """
        if self.max_sources_logged:
            return True

        if self.exclusions and self.exclusions.evaluate_input_exclusions(
            self, source_type, source_name
        ):
            return True

        threshold_reached = self.source_count >= Settings().max_sources
        if threshold_reached:
            logger.warning(
                "Will not create more sources in this request. %s sources reached",
                self.source_count,
            )
            self.max_sources_logged = True

        return threshold_reached

    @property
    def stop_propagation(self):
        """
        Compare `propagation_count` to `max_propagation_events` config option
        :return: true if propagation_count within this request is equal to or
                 greater than configured threshold for propagation
        """
        if self.max_propagators_logged:
            return True

        threshold_reached = self.propagation_count >= Settings().max_propagation
        if threshold_reached:
            logger.warning(
                "Will not propagate any more in this request. %s propagations reached.",
                self.propagation_count,
            )
            self.max_propagators_logged = True

        return threshold_reached

    @property
    def propagate_assess(self):
        # TODO: PYT-644 move this property of out this class?
        return self.assess_enabled and not scope.in_contrast_or_propagation_scope()

    def source_created(self):
        """
        Increase the running count of sources created in this request
        """
        self.source_count += 1

    def propagated(self):
        """
        Increase the running count of propagations created in this request
        """
        self.propagation_count += 1

    def extract_response(self, response: BaseResponseWrapper):
        """
        Fully generate / iterate over the response body and store a reference to the
        response object on this request context.

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

    def evaluate_exclusions(self) -> bool:
        """
        Check if the request is excluded based on the URL or input exclusions.

        :return: True if the request is excluded, False otherwise
        """
        if self.exclusions:
            path = self.request.path_info
            self.exclusions.evaluate_url_exclusions(self, path)
            if self.disabled:
                # Stop analyzing this endpoint since the URL exclusion applies
                return True

            self.exclusions.set_input_exclusions_by_url(self, path)

        return False
