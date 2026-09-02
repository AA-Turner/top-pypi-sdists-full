"""API version enumeration for Azure Container Apps Sandbox SDK."""

from enum import Enum


class ApiVersion(str, Enum):
    """Azure Container Apps Sandbox API versions.

    Use ``ApiVersion.V2026_02_01_PREVIEW`` (the default) or pass a raw
    version string for forward-compatibility with unreleased API versions.
    """

    V2026_02_01_PREVIEW = "2026-02-01-preview"


DEFAULT_API_VERSION = ApiVersion.V2026_02_01_PREVIEW
