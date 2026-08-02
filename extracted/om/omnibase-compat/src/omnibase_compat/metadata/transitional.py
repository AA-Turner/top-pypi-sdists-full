# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: infrastructure model for the compat retention system itself

from pydantic import BaseModel


class TransitionalMeta(BaseModel, frozen=True):
    """Governance metadata required for all transitional artifacts.

    Transitional artifacts are temporary placeholders with a known canonical
    future owner. CI must fail when artifacts exceed their retirement milestone.
    """

    canonical_owner: str
    removal_ticket: str
    removal_milestone: str
    introduced_by_ticket: str
    review_owner: str
    notes: str = ""
