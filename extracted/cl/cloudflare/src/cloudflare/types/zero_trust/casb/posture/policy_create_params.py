# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from ....._types import SequenceNotStr

__all__ = ["PolicyCreateParams", "Actions", "ActionsRemediationType", "ActionsWebhookConfig"]


class PolicyCreateParams(TypedDict, total=False):
    account_id: Required[str]

    actions: Required[Actions]
    """
    Actions to execute when this policy is triggered, grouped by action type. A
    policy must contain at least one action across all groups and may include at
    most one remediation.
    """

    applies_to_all_integrations: Required[bool]
    """When true, the policy applies to all integrations for the account.

    When false, integration_ids must be provided.
    """

    display_name: Required[str]
    """Display name for the policy configuration."""

    enabled: Required[bool]
    """Boolean specifying if the policy is enabled or disabled."""

    finding_type_id: Required[str]
    """The finding type this policy is associated with.

    All remediation actions must match this finding type.
    """

    description: str
    """Optional description of what this policy does."""

    integration_ids: SequenceNotStr[str]
    """The integrations this policy applies to.

    Required when applies_to_all_integrations is false.
    """


class ActionsRemediationType(TypedDict, total=False):
    """A remediation action to be executed."""

    remediation_type_id: Required[str]
    """The ID of the remediation type to execute."""


class ActionsWebhookConfig(TypedDict, total=False):
    """A webhook action to be executed."""

    webhook_config_id: Required[str]
    """The ID of the webhook configuration to use."""


class Actions(TypedDict, total=False):
    """
    Actions to execute when this policy is triggered, grouped by action type.
    A policy must contain at least one action across all groups and may include
    at most one remediation.
    """

    remediation_types: Iterable[ActionsRemediationType]
    """Remediation actions to execute (at most one)."""

    webhook_configs: Iterable[ActionsWebhookConfig]
    """Webhook actions to execute."""
