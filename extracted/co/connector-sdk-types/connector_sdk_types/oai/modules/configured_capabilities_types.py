from __future__ import annotations

import typing as t
from collections.abc import Callable

from pydantic import BaseModel, Field, field_validator

# Import directly from modules to avoid circular import through generated/__init__.py
from connector_sdk_types.generated.models.standard_capability_name import StandardCapabilityName

CapabilityGate: t.TypeAlias = Callable[[t.Any], bool]
"""Whether one connection serves a capability, given its validated settings (an instance of
the integration's `settings_model`). `app_info` carries no credentials, so this reads settings
only."""

UNGATED_CAPABILITIES: frozenset[StandardCapabilityName] = frozenset(
    {
        StandardCapabilityName.APP_INFO,
        StandardCapabilityName.INFO,
        StandardCapabilityName.CONNECTED_INFO,
        StandardCapabilityName.VALIDATE_CREDENTIALS,
        StandardCapabilityName.VALIDATE_CREDENTIAL_CONFIG,
        StandardCapabilityName.PROBE_INTEGRATION,
        StandardCapabilityName.GET_AUTHORIZATION_URL,
        StandardCapabilityName.HANDLE_AUTHORIZATION_CALLBACK,
        StandardCapabilityName.HANDLE_CLIENT_CREDENTIALS_REQUEST,
        StandardCapabilityName.REFRESH_ACCESS_TOKEN,
    }
)
"""Capabilities a connection needs before its settings mean anything, so none can be gated."""


class ConfiguredCapabilities(BaseModel):
    """Capabilities a connection serves only when its settings configure them.

    For a configuration-driven connector, where a capability works only once a setting
    describes it. `app_info` runs each gate against the connection's settings and leaves the
    capabilities whose gate is false out of `x-capabilities` and `paths`:

    ```python
    integration = Integration(
        ...,
        settings_model=MySettings,
        configured_capabilities=ConfiguredCapabilities(
            gates={
                StandardCapabilityName.LIST_ACCOUNTS: lambda s: bool(s.accounts_query),
                StandardCapabilityName.CREATE_TICKET: lambda s: bool(s.ticket_create_config),
            },
        ),
    )
    ```

    A capability without a gate is always advertised. Hiding only affects what `app_info`
    advertises; a hidden capability can still be called.

    Without settings on the request, or when they don't validate or a gate fails, `app_info`
    returns the static answer: every registered capability.
    """

    gates: dict[StandardCapabilityName, CapabilityGate] = Field(
        description="Capability -> whether a connection with these settings serves it.",
    )

    @field_validator("gates")
    @classmethod
    def _no_ungated_capabilities(
        cls, gates: dict[StandardCapabilityName, CapabilityGate]
    ) -> dict[StandardCapabilityName, CapabilityGate]:
        ungated = sorted(c.value for c in gates if c in UNGATED_CAPABILITIES)
        if ungated:
            raise ValueError(f"These capabilities can't be gated on settings: {ungated}")
        return gates


__all__ = [
    "UNGATED_CAPABILITIES",
    "CapabilityGate",
    "ConfiguredCapabilities",
]
