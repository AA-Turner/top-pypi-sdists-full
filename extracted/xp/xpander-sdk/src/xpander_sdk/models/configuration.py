"""
Configuration model for xpander.ai SDK.

This module contains the Configuration class that manages SDK settings including
API credentials, base URLs, and organization information.
"""

from typing import Optional
from os import getenv
from urllib.parse import urlparse

from pydantic import BaseModel, ConfigDict, Field, field_validator

from xpander_sdk.core.state import State
from xpander_sdk.utils.env import ensure_scheme, get_base_url


class Configuration(BaseModel):
    """
    Configuration settings for the xpander.ai SDK.

    This class manages all configuration parameters required to connect to the xpander.ai
    Backend-as-a-Service platform, including authentication credentials and service endpoints.

    Attributes:
        api_key (Optional[str]): Your xpander.ai API key. Defaults to XPANDER_API_KEY environment variable.
        base_url (Optional[str]): The base URL for xpander.ai API endpoints. Auto-detected from environment.
        organization_id (Optional[str]): Your organization ID. Defaults to XPANDER_ORGANIZATION_ID environment variable.

    Environment Variables:
        XPANDER_API_KEY: Your API key for authentication
        XPANDER_ORGANIZATION_ID: Your organization identifier

    Example:
        >>> config = Configuration(
        ...     api_key="your-api-key",
        ...     organization_id="your-org-id"
        ... )
        >>> full_url = config.get_full_url()
    """

    # Assignments re-validate so base_url invariants survive mutation too.
    model_config = ConfigDict(validate_assignment=True)

    api_key: Optional[str] = Field(
        default_factory=lambda: getenv(key="XPANDER_API_KEY"),
        description="xpander.ai API key for authentication",
    )

    base_url: Optional[str] = Field(
        default_factory=get_base_url,
        validate_default=True,
        description="Base URL for xpander.ai API endpoints",
    )

    agent_id: Optional[str] = Field(default=None, description="Agent ID To work on")

    organization_id: Optional[str] = Field(
        default_factory=lambda: getenv(key="XPANDER_ORGANIZATION_ID"),
        description="Organization identifier for xpander.ai account",
    )

    state: Optional[State] = Field(
        default_factory=State,
        description="Configuration level in-memory state",
        exclude=True,  # This ensures it's excluded by default
    )

    @field_validator("base_url", mode="before")
    @classmethod
    def _normalize_base_url(cls, value: Optional[str]) -> str:
        """Never hold a None/empty or scheme-less base_url - downstream URL
        assembly and hostname routing assume a well-formed absolute URL.
        An explicit falsy value must not silently fall back to the public
        cloud default (on-prem keys would egress to the cloud gateway):
        honor XPANDER_BASE_URL when set, otherwise fail loudly."""
        if not value:
            value = getenv("XPANDER_BASE_URL")
            if not value:
                raise ValueError(
                    "base_url is empty - provide base_url or set the "
                    "XPANDER_BASE_URL environment variable."
                )
        return ensure_scheme(str(value))

    def get_full_url(self) -> str:
        """
        Construct the complete API URL including organization ID when required.

        Some xpander.ai services require the organization ID to be included in the URL path.
        This method automatically detects when this is needed and constructs the appropriate URL.

        Returns:
            str: The complete URL for API requests, with organization ID included if required.

        Example:
            >>> config = Configuration(base_url="https://inbound.xpander.ai", organization_id="org123")
            >>> config.get_full_url()
            'https://inbound.xpander.ai'

            >>> config = Configuration(base_url="https://agent-controller.xpander.ai", organization_id="org123")
            >>> config.get_full_url()
            'https://agent-controller.xpander.ai/org123'
        """
        if not self.base_url:
            raise ValueError(
                "Configuration.base_url is not set - provide base_url or the "
                "XPANDER_BASE_URL environment variable."
            )

        # Org-append contract (mono workspace/functions.py): the SDK appends
        # /{org} when the hostname contains "agent-controller" (covers the
        # generated agent-controller-<customer> ingress hosts), the port is the
        # controller's 9016, or the URL is path-mounted at /agent-controller.
        # Hostname/path-segment checks only - a full-URL substring match would
        # re-trigger the inbound false-positive class this replaced.
        parsed = urlparse(self.base_url)
        host = (parsed.hostname or "").lower()
        first_path_segment = parsed.path.strip("/").split("/", 1)[0].lower()
        is_agent_controller = (
            "agent-controller" in host
            or parsed.port == 9016
            or first_path_segment == "agent-controller"
        )

        if is_agent_controller:
            return f"{self.base_url}/{self.organization_id}"

        return self.base_url
