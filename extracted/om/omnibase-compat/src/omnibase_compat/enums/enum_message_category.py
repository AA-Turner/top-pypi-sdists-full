# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.enums.enum_execution_shape.EnumMessageCategory
# COMPAT_REMOVAL_DATE: 2026-10-01

# SOURCE: omnibase_core/src/omnibase_core/enums/enum_execution_shape.py
# SOURCE VERSION: omnibase-core==0.24.1
# SOURCE COMMIT: a39b9e953c73e33370a87bc3664460e29d1a729c
# Copied 2026-03-08 for omnibase_compat initial seeding.
# Downstream repos should import from omnibase_compat going forward.
#
# NOTE: Canonical owner docs (OMN-4032) state EnumMessageCategory is defined
# only in omnibase_core.enums.enum_execution_shape. This copy is intentionally
# a minimal StrEnum — it omits the helper methods (topic_suffix, from_topic, etc.)
# which belong to the omnibase_core implementation layer. The values are exact.
from enum import StrEnum


class EnumMessageCategory(StrEnum):
    """Categories of messages in ONEX for routing and topic mapping.

    Minimal copy for cross-repo structural compatibility.
    For full implementation with helper methods, use omnibase_core.
    """

    EVENT = "event"
    """Something that happened - a past-tense, immutable fact."""

    COMMAND = "command"
    """A request to do something - an imperative action."""

    INTENT = "intent"
    """A desire to achieve an outcome - goal-oriented."""
