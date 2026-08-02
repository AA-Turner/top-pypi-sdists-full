# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# compat-skip-retention: infrastructure enum for compat artifact lifecycle tracking

from enum import StrEnum


class ArtifactStatus(StrEnum):
    experimental = "experimental"
    candidate = "candidate"
    stable = "stable"
    deprecated = "deprecated"
    retired = "retired"
