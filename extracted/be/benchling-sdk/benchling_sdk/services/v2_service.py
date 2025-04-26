from __future__ import annotations

from functools import cached_property
from typing import Optional, TYPE_CHECKING

from benchling_api_client.v2.stable.client import Client

from benchling_sdk.helpers.logging_helpers import log_stability_warning, StabilityLevel
from benchling_sdk.helpers.retry_helpers import RetryStrategy
from benchling_sdk.services.v2.base_service import BaseService

if TYPE_CHECKING:
    from benchling_sdk.services.v2.v2_alpha_service import V2AlphaService
    from benchling_sdk.services.v2.v2_beta_service import V2BetaService
    from benchling_sdk.services.v2.v2_stable_service import V2StableService


class V2Service(BaseService):
    """
    V2.

    Namespace containing support for the V2 Benchling API.
    """

    _v2_alpha_service: Optional[V2AlphaService]
    _v2_beta_service: Optional[V2BetaService]

    def __init__(self, client: Client, retry_strategy: Optional[RetryStrategy] = None):
        """
        Initialize a service.

        :param client: Underlying generated Client.
        :param retry_strategy: Retry strategy for failed HTTP calls
        """
        super().__init__(client, retry_strategy)
        self._v2_alpha_service = None
        self._v2_beta_service = None

    # Note that alpha & beta do not use the @cached_property pattern that we've used for all other
    # service accessors; instead, we've rolled our own equivalent caching logic using an attribute.
    # That's because we want some additional behavior - logging a warning message - to happen on
    # every call to those property methods, not just on the first call. We could consider changing
    # this in a future release so it only logs once, in which case we can use @cached_property.

    @property
    def alpha(self) -> V2AlphaService:
        """
        V2-alpha.

        Alpha endpoints have different stability guidelines than other stable endpoints.

        See https://benchling.com/api/v2-alpha/reference
        """
        log_stability_warning(StabilityLevel.ALPHA, package="v2.alpha")

        if self._v2_alpha_service is None:
            from .v2.v2_alpha_service import V2AlphaService

            self._v2_alpha_service = self._create_service(V2AlphaService)

        return self._v2_alpha_service

    @property
    def beta(self) -> V2BetaService:
        """
        V2-beta.

        Beta endpoints have different stability guidelines than other stable endpoints.

        See https://benchling.com/api/v2-beta/reference
        """
        log_stability_warning(StabilityLevel.BETA, package="v2.beta")
        if self._v2_beta_service is None:
            from .v2.v2_beta_service import V2BetaService

            self._v2_beta_service = self._create_service(V2BetaService)

        return self._v2_beta_service

    @cached_property
    def stable(self) -> V2StableService:
        """
        Stable.

        See https://docs.benchling.com/docs/stability#are-breaking-changes-made-to-the-api-or-events
        """
        from .v2.v2_stable_service import V2StableService

        return self._create_service(V2StableService)
