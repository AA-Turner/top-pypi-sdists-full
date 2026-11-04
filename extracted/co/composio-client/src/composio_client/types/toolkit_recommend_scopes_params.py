# Manufactured by packages/codegen (`pnpm generate:python`) — edit the generator, not this file.
"""Compatibility types for composio_client.types.toolkit_recommend_scopes_params."""

from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, Required, TypedDict
from .._types import SequenceNotStr


class ToolkitRecommendScopesParams(TypedDict, total=False):
    tools: Required[SequenceNotStr[str]]
    auth_scheme: NotRequired[Literal["OAUTH2", "OAUTH1", "API_KEY", "BASIC", "BILLCOM_AUTH", "BEARER_TOKEN", "GOOGLE_SERVICE_ACCOUNT", "NO_AUTH", "BASIC_WITH_JWT", "CALCOM_AUTH", "SERVICE_ACCOUNT", "SAML", "DCR_OAUTH", "CIMD_OAUTH", "S2S_OAUTH2"]]
    toolkit_version: NotRequired[str]
    grant_context: NotRequired[dict[str, str]]
    include: NotRequired[SequenceNotStr[str]]
    exclude: NotRequired[SequenceNotStr[str]]
    available_scopes: NotRequired[SequenceNotStr[str]]


__all__ = [
    "ToolkitRecommendScopesParams",
]
