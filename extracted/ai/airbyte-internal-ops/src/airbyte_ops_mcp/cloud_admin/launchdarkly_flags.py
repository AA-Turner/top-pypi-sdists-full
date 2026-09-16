# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""API client functions for LaunchDarkly flag organization targeting.

This module provides HTTP access to the LaunchDarkly REST API for reading
feature flags and managing individual organization targets on allowlisted
flags. Only flags tagged `ops-mcp` in the `default` project are eligible
for writes, and only `addTargets`/`removeTargets` semantic-patch
instructions on the `organization` context kind are ever emitted.

LaunchDarkly API docs: https://launchdarkly.com/docs/api
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any, Literal
from urllib.parse import quote

import requests

from airbyte_ops_mcp.constants import USER_AGENT

logger = logging.getLogger(__name__)

LD_API_BASE_URL = "https://app.launchdarkly.com/api/v2"
"""Base URL for the LaunchDarkly REST API."""

ENV_LAUNCHDARKLY_API_TOKEN = "LAUNCHDARKLY_API_TOKEN"
"""Environment variable name for the LaunchDarkly API token."""

LD_PROJECT_KEY = "default"
"""LaunchDarkly project containing the ops-targetable flags."""

LD_ENVIRONMENT_KEY = "production"
"""LaunchDarkly environment whose organization targets are managed."""

LD_ORG_CONTEXT_KIND = "organization"
"""LaunchDarkly context kind used for organization targets."""

LD_OPS_MCP_TAG = "ops-mcp"
"""Tag marking a LaunchDarkly flag as eligible for Ops MCP targeting."""

LD_SEMANTIC_PATCH_CONTENT_TYPE = (
    "application/json; domain-model=launchdarkly.semanticpatch"
)
"""Content-Type required for semantic-patch flag updates."""


class LaunchDarklyAPIError(Exception):
    """Raised when a LaunchDarkly API call fails."""


class LaunchDarklyFlagNotEligibleError(LaunchDarklyAPIError):
    """Raised when a flag is not eligible for Ops MCP organization targeting."""


class LaunchDarklyVerificationError(LaunchDarklyAPIError):
    """Raised when the post-write re-read does not reflect the requested change.

    `new_targets` carries the target list observed in the re-read so callers
    can report the actual state.
    """

    def __init__(self, message: str, new_targets: list[str]) -> None:
        super().__init__(message)
        self.new_targets = new_targets


def _get_ld_api_token() -> str:
    """Resolve the LaunchDarkly API token from the environment.

    Raises:
        LaunchDarklyAPIError: If `LAUNCHDARKLY_API_TOKEN` is not configured.
    """
    token = os.environ.get(ENV_LAUNCHDARKLY_API_TOKEN)
    if not token:
        raise LaunchDarklyAPIError(
            "LAUNCHDARKLY_API_TOKEN not configured. The LaunchDarkly "
            "organization-targeting tools require an API token; see "
            "docs/launchdarkly-flag-targeting.md."
        )
    return token


def _ld_headers() -> dict[str, str]:
    """Build common HTTP headers for LaunchDarkly API requests."""
    return {
        "Authorization": _get_ld_api_token(),
        "User-Agent": USER_AGENT,
    }


def _flag_endpoint(flag_key: str) -> str:
    """Return the flag REST endpoint, percent-encoding `flag_key`."""
    return f"{LD_API_BASE_URL}/flags/{LD_PROJECT_KEY}/{quote(flag_key, safe='')}"


def get_flag(flag_key: str) -> dict[str, Any]:
    """Fetch a flag with its `production` environment configuration.

    Returns the raw flag dict from the LaunchDarkly API, including `tags`,
    `kind`, `variations`, and `environments.production.contextTargets`.

    Raises:
        LaunchDarklyAPIError: If the flag is not found or the API call fails.
    """
    endpoint = _flag_endpoint(flag_key)
    try:
        response = requests.get(
            endpoint,
            params={"env": LD_ENVIRONMENT_KEY},
            headers=_ld_headers(),
            timeout=30,
        )
    except requests.RequestException as e:
        raise LaunchDarklyAPIError(f"LaunchDarkly request failed: {e}") from e
    if response.status_code == 404:
        raise LaunchDarklyAPIError(
            f"LaunchDarkly flag {flag_key!r} not found in project {LD_PROJECT_KEY!r}."
        )
    if response.status_code != 200:
        raise LaunchDarklyAPIError(
            f"LaunchDarkly get flag failed: {response.status_code} {response.text}"
        )
    return response.json()


def list_flags(tag: str | None = None) -> list[dict[str, Any]]:
    """List flags in the default project, optionally filtered by tag.

    Passes `tag` through to the LaunchDarkly `tag` query param when given.
    Follows `_links.next` pagination until all matching flags are collected.

    Raises:
        LaunchDarklyAPIError: If the API call fails.
    """
    endpoint = f"{LD_API_BASE_URL}/flags/{LD_PROJECT_KEY}"
    params: dict[str, Any] = {
        "env": LD_ENVIRONMENT_KEY,
        "limit": 100,
    }
    if tag is not None:
        params["tag"] = tag
    flags: list[dict[str, Any]] = []
    url: str | None = endpoint
    while url:
        try:
            response = requests.get(
                url,
                params=params,
                headers=_ld_headers(),
                timeout=30,
            )
        except requests.RequestException as e:
            raise LaunchDarklyAPIError(f"LaunchDarkly request failed: {e}") from e
        if response.status_code != 200:
            raise LaunchDarklyAPIError(
                f"LaunchDarkly list flags failed: "
                f"{response.status_code} {response.text}"
            )
        data = response.json()
        flags.extend(data.get("items", []))
        next_link = (data.get("_links") or {}).get("next") or {}
        url = next_link.get("href")
        if url and not url.startswith("http"):
            url = f"https://app.launchdarkly.com{url}"
        params = {}  # params are encoded in the next link
    return flags


def flag_is_ops_targetable(flag: dict[str, Any]) -> bool:
    """Return `True` if the flag carries the `ops-mcp` tag."""
    return LD_OPS_MCP_TAG in flag.get("tags", [])


def variation_id_of(variation: dict[str, Any]) -> str:
    """Return the LaunchDarkly variation UUID from a variation dict.

    The API v2 returns the identifier as `_id`; fall back to `id` for
    response shapes that use the bare field name.
    """
    return str(variation.get("_id") or variation.get("id"))


def resolve_variation(
    flag: dict[str, Any],
    variation: str | None,
) -> tuple[int, str]:
    """Resolve a variation selector to `(index, variation_id)`.

    When `variation` is `None`, boolean flags resolve to the variation whose
    value is `True`; multivariate flags require an explicit selection. When
    given, `variation` matches case-insensitively against the variation
    `name`, or against `str(value)` (so `"true"`/`"false"` work).

    Raises:
        LaunchDarklyAPIError: If the variation cannot be resolved.
    """
    variations: list[dict[str, Any]] = flag.get("variations", [])
    available = ", ".join(str(v.get("name") or v.get("value")) for v in variations)

    if variation is None:
        if flag.get("kind") == "boolean":
            for index, v in enumerate(variations):
                if v.get("value") is True:
                    return index, variation_id_of(v)
        raise LaunchDarklyAPIError(
            f"Flag {flag.get('key')!r} is multivariate; `variation` is "
            f"required. Available variations: {available}."
        )

    lowered = variation.lower()
    for index, v in enumerate(variations):
        name = str(v.get("name") or "").lower()
        value = str(v.get("value")).lower()
        if lowered in (name, value):
            return index, variation_id_of(v)
    raise LaunchDarklyAPIError(
        f"Unknown variation {variation!r} for flag {flag.get('key')!r}. "
        f"Available variations: {available}."
    )


def get_org_targets(flag: dict[str, Any], variation_index: int) -> list[str]:
    """Return the organization IDs individually targeted to a variation."""
    env = (flag.get("environments") or {}).get(LD_ENVIRONMENT_KEY) or {}
    targets: list[str] = []
    for target in env.get("contextTargets") or []:
        if (
            target.get("contextKind") == LD_ORG_CONTEXT_KIND
            and target.get("variation") == variation_index
        ):
            targets.extend(str(v) for v in target.get("values") or [])
    return targets


@dataclass(frozen=True)
class VariationSelection:
    """Variation chosen for an organization-target change.

    `index is None` means an implicit remove found no targeting variation and
    the change is an idempotent no-op.
    """

    index: int | None
    variation_id: str | None
    name: str | None
    previous_targets: list[str]


def variations_targeting_org(flag: dict[str, Any], organization_id: str) -> list[int]:
    """Return the variation indices whose organization targets include `organization_id`."""
    return [
        index
        for index in range(len(flag.get("variations") or []))
        if organization_id in get_org_targets(flag, index)
    ]


def select_variation(
    flag: dict[str, Any],
    *,
    action: Literal["add", "remove"],
    organization_id: str,
    variation: str | None,
) -> VariationSelection:
    """Pick the variation an organization-target change applies to.

    For `remove` with `variation=None`, the organization is located on
    whichever variation currently targets it; when none does, the returned
    selection has `index=None` (idempotent no-op). For `add` or an explicit
    `variation`, the selector resolves via `resolve_variation`.

    Raises:
        LaunchDarklyAPIError: If the variation cannot be resolved, or an
            implicit remove finds the organization targeted on more than one
            variation.
    """
    index: int
    if action == "remove" and variation is None:
        targeting = variations_targeting_org(flag, organization_id)
        if len(targeting) > 1:
            raise LaunchDarklyAPIError(
                f"Organization {organization_id} is targeted on multiple "
                f"variations of flag {flag.get('key')!r}; pass `variation` "
                "explicitly."
            )
        if not targeting:
            return VariationSelection(
                index=None,
                variation_id=None,
                name=None,
                previous_targets=[],
            )
        index = targeting[0]
    else:
        index, _ = resolve_variation(flag, variation)
    variation_entry = flag["variations"][index]
    return VariationSelection(
        index=index,
        variation_id=variation_id_of(variation_entry),
        name=variation_entry.get("name"),
        previous_targets=get_org_targets(flag, index),
    )


def apply_org_target_change(
    flag_key: str,
    *,
    action: Literal["add", "remove"],
    selection: VariationSelection,
    organization_id: str,
    comment: str,
    verify_all_variations: bool,
) -> tuple[list[str], list[str]]:
    """PATCH the target change, then verify it against a post-write re-read.

    Returns `(new_targets, warnings)` where `new_targets` is the confirmed
    target list on `selection.index`. When `verify_all_variations` is `True`
    (an implicit remove), verification requires the organization to be absent
    from every variation.

    Raises:
        LaunchDarklyAPIError: If the PATCH fails or no variation is selected.
        LaunchDarklyVerificationError: If the re-read does not reflect the
            requested change.
    """
    if selection.index is None or selection.variation_id is None:
        raise LaunchDarklyAPIError(
            f"Cannot apply {action} on flag {flag_key!r}: no variation was selected."
        )
    latest_flag = get_flag(flag_key)
    if not flag_is_ops_targetable(latest_flag):
        raise LaunchDarklyFlagNotEligibleError(
            f"Flag {flag_key!r} is not addressable by Ops MCP. Add the "
            f"{LD_OPS_MCP_TAG!r} tag to the flag in LaunchDarkly to opt it in."
        )
    patch_org_targets(
        flag_key,
        action=action,
        variation_id=selection.variation_id,
        organization_id=organization_id,
        comment=comment,
    )
    try:
        updated_flag = get_flag(flag_key)
    except LaunchDarklyAPIError as e:
        if action == "add":
            expected = [*selection.previous_targets, organization_id]
        else:
            expected = [t for t in selection.previous_targets if t != organization_id]
        return expected, [
            f"Post-write verification read failed: {e}; new_targets reflects "
            "the expected state, not a confirmed re-read."
        ]
    new_targets = get_org_targets(updated_flag, selection.index)
    if verify_all_variations:
        is_targeted = bool(variations_targeting_org(updated_flag, organization_id))
    else:
        is_targeted = organization_id in new_targets
    if is_targeted != (action == "add"):
        raise LaunchDarklyVerificationError(
            f"LaunchDarkly accepted the {action} but the re-read of flag "
            f"{flag_key!r} does not reflect it; state is unconfirmed.",
            new_targets,
        )
    return new_targets, []


def patch_org_targets(
    flag_key: str,
    *,
    action: Literal["add", "remove"],
    variation_id: str,
    organization_id: str,
    comment: str,
) -> dict[str, Any]:
    """Add or remove a single organization individual target on a flag.

    Emits exactly one `addTargets`/`removeTargets` semantic-patch instruction
    against the `production` environment.

    Raises:
        LaunchDarklyAPIError: If the API call fails.
    """
    instruction_kind = "addTargets" if action == "add" else "removeTargets"
    body = {
        "environmentKey": LD_ENVIRONMENT_KEY,
        "comment": comment,
        "instructions": [
            {
                "kind": instruction_kind,
                "contextKind": LD_ORG_CONTEXT_KIND,
                "variationId": variation_id,
                "values": [organization_id],
            }
        ],
    }
    endpoint = _flag_endpoint(flag_key)
    headers = _ld_headers()
    headers["Content-Type"] = LD_SEMANTIC_PATCH_CONTENT_TYPE
    try:
        response = requests.patch(
            endpoint,
            json=body,
            headers=headers,
            timeout=30,
        )
    except requests.RequestException as e:
        raise LaunchDarklyAPIError(f"LaunchDarkly request failed: {e}") from e
    if response.status_code // 100 != 2:
        raise LaunchDarklyAPIError(
            f"LaunchDarkly update flag targets failed: "
            f"{response.status_code} {response.text}"
        )
    return response.json()


def build_change_comment(
    action: Literal["add", "remove"],
    organization_id: str,
    approver_email: str,
    agent_session_url: str | None,
) -> str:
    """Build the required semantic-patch comment recording the approval."""
    parts = [
        f"[ops-mcp] {action} organization {organization_id}",
        f"approved by {approver_email}",
    ]
    if agent_session_url:
        parts.append(f"session {agent_session_url}")
    return "; ".join(parts)
