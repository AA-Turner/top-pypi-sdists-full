# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo
from .application_configuration_param import ApplicationConfigurationParam
from .offline_application_configuration_param import OfflineApplicationConfigurationParam

__all__ = [
    "ApplicationVariantCreateParams",
    "ApplicationVariantV0Request",
    "ApplicationVariantAgentsServiceRequest",
    "OfflineApplicationVariantRequest",
]


class ApplicationVariantV0Request(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required[ApplicationConfigurationParam]

    name: Required[str]

    version: Required[Literal["V0"]]

    description: str
    """Optional description of the application variant"""

    draft: bool
    """Boolean to indicate whether the variant is in draft mode"""

    published_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """The date and time that the variant was published."""


class ApplicationVariantAgentsServiceRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required["ApplicationAgentsServiceConfigurationParam"]

    name: Required[str]

    version: Required[Literal["AGENTS_SERVICE"]]

    description: str
    """Optional description of the application variant"""

    draft: bool
    """Boolean to indicate whether the variant is in draft mode"""

    published_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """The date and time that the variant was published."""


class OfflineApplicationVariantRequest(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_spec_id: Required[str]

    configuration: Required[OfflineApplicationConfigurationParam]

    name: Required[str]

    version: Required[Literal["OFFLINE"]]

    description: str
    """Optional description of the application variant"""

    draft: bool
    """Boolean to indicate whether the variant is in draft mode"""

    published_at: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]
    """The date and time that the variant was published."""


ApplicationVariantCreateParams: TypeAlias = Union[
    ApplicationVariantV0Request, ApplicationVariantAgentsServiceRequest, OfflineApplicationVariantRequest
]

from .application_agents_service_configuration_param import ApplicationAgentsServiceConfigurationParam
