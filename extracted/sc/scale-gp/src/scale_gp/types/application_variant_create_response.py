# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Annotated, TypeAlias

from .._utils import PropertyInfo
from .application_variant_v0_response import ApplicationVariantV0Response
from .offline_application_variant_response import OfflineApplicationVariantResponse

__all__ = ["ApplicationVariantCreateResponse"]

ApplicationVariantCreateResponse: TypeAlias = Annotated[
    Union[ApplicationVariantV0Response, "ApplicationVariantAgentsServiceResponse", OfflineApplicationVariantResponse],
    PropertyInfo(discriminator="version"),
]

from .application_variant_agents_service_response import ApplicationVariantAgentsServiceResponse
