# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_infra.adapters.adapter_project_tracker_linear
# COMPAT_REMOVAL_DATE: 2026-10-01
# COMPAT_RETENTION_NOTE: extended 2026-09-01 -> 2026-10-01 under OMN-16602.
# The original date expired mid-flight and hard-fails the required `validate`
# job for EVERY PR on this repo, so extending is the retention policy's own
# sanctioned action (see scripts/check_compat_retention.py: "migrate or extend
# the date"). Extended rather than removed on purpose: removal is a breaking
# API change to a published package and needs its own version bump and
# release, not a documentation PR. Live readiness measured 2026-09-02 and
# recorded on OMN-16602 — see that ticket before extending a second time.

from __future__ import annotations

import json
import urllib.request
from typing import Any, cast

from omnibase_compat.config import resolve_endpoint_url
from omnibase_compat.models.model_project_tracker import (
    ModelIssueStatus,
    ModelLabel,
    ModelTeam,
)
from omnibase_compat.protocols.protocol_project_tracker import ProtocolProjectTracker

# Logical endpoint key resolved from the compat contract/overlay surface
# (``omnibase_compat.config``). The URL itself lives in the overlay document,
# never as a Python literal here (OMN-13564 / url-authority).
_LINEAR_ENDPOINT_KEY = "project_tracker_linear"


def _nested_id(raw: dict[str, Any], key: str) -> str | None:
    val = raw.get(key)
    if isinstance(val, dict):
        inner = val.get("id")
        return inner if isinstance(inner, str) else None
    return None


class AdapterProjectTrackerLinear(ProtocolProjectTracker):
    def __init__(self, api_key: str, *, base_url: str | None = None) -> None:
        # base_url resolves from the contract/overlay surface when not supplied
        # by the caller; fail-closed if the endpoint is undeclared.
        self._api_key = api_key
        self._base_url = base_url or resolve_endpoint_url(_LINEAR_ENDPOINT_KEY)

    def _graphql(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {"query": query}
        if variables is not None:
            body["variables"] = variables
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            self._base_url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": self._api_key,
            },
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            return cast(dict[str, Any], json.loads(resp.read()))

    def list_teams(self) -> list[ModelTeam]:
        result = self._graphql(
            """query {
                teams { nodes { id name key } }
            }"""
        )
        nodes = _extract_nodes(result, "teams")
        return [
            ModelTeam(
                id=n["id"],
                name=n["name"],
                key=n["key"],
            )
            for n in nodes
        ]

    def list_issue_labels(self, team: str) -> list[ModelLabel]:
        result = self._graphql(
            """query ($filter: IssueLabelFilter!) {
                issueLabels(filter: $filter) {
                    nodes { id name color team { id } }
                }
            }""",
            {"filter": {"team": {"key": {"eq": team}}}},
        )
        nodes = _extract_nodes(result, "issueLabels")
        out: list[ModelLabel] = []
        for n in nodes:
            out.append(
                ModelLabel(
                    id=n["id"],
                    name=n["name"],
                    color=n.get("color"),
                    team_id=_nested_id(n, "team"),
                )
            )
        return out

    def list_issue_statuses(self, team: str) -> list[ModelIssueStatus]:
        result = self._graphql(
            """query ($filter: WorkflowStateFilter!) {
                workflowStates(filter: $filter) {
                    nodes { id name type team { id } }
                }
            }""",
            {"filter": {"team": {"key": {"eq": team}}}},
        )
        nodes = _extract_nodes(result, "workflowStates")
        out: list[ModelIssueStatus] = []
        for n in nodes:
            out.append(
                ModelIssueStatus(
                    id=n["id"],
                    name=n["name"],
                    type=n["type"],
                    team_id=_nested_id(n, "team"),
                )
            )
        return out


def _extract_nodes(payload: dict[str, Any], root_key: str) -> list[dict[str, Any]]:
    data = payload.get("data")
    if not isinstance(data, dict):
        raise ValueError(f"Unexpected Linear response: {payload}")
    root = data.get(root_key)
    if not isinstance(root, dict):
        raise ValueError(f"Missing '{root_key}' in Linear response: {data}")
    nodes = root.get("nodes")
    if not isinstance(nodes, list):
        raise ValueError(f"Missing 'nodes' under '{root_key}': {root}")
    return nodes


__all__: list[str] = [
    "AdapterProjectTrackerLinear",
]
