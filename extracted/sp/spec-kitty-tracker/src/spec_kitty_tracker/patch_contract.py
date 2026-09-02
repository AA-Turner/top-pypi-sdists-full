"""Shared strict patch-key rejection for connector egress paths.

TRK-M1-03 A6 (TRK-M1-01 contract-freeze draft §3.2): every connector
(``InMemoryConnector``, ``BeadsConnector``, ``FPConnector``) rejects patch
keys outside :data:`~spec_kitty_tracker.policy.CORE_ISSUE_FIELDS` with
``IssuePayloadContractError(kind="patch", field_path=<key>, reason="PK-001")``
before issuing any write. This module is the single place that check is
implemented so every connector enforces the identical rule (N1).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from spec_kitty_tracker.errors import IssuePayloadContractError
from spec_kitty_tracker.policy import CORE_ISSUE_FIELDS

_ALLOWED_PATCH_KEYS = frozenset(CORE_ISSUE_FIELDS)


def reject_unknown_patch_keys(patch: Mapping[str, Any], *, provider: str | None = None) -> None:
    """Raise ``IssuePayloadContractError`` (PK-001) for any key outside
    ``CORE_ISSUE_FIELDS``. Called at the top of every connector's
    ``update_issue`` before any write is issued.
    """

    for key in patch:
        if key not in _ALLOWED_PATCH_KEYS:
            raise IssuePayloadContractError(
                f"Unknown patch key: {key!r}",
                provider=provider,
                kind="patch",
                field_path=key,
                reason="PK-001",
            )
