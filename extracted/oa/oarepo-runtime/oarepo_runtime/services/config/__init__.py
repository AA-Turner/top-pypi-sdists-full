#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Service config module."""

from __future__ import annotations

from .link_conditions import (
    has_draft,
    has_draft_permission,
    has_permission,
    has_published_record,
    is_draft,
    is_published_record,
)
from .permissions import EveryonePermissionPolicy

__all__ = (
    "EveryonePermissionPolicy",
    "has_draft",
    "has_draft_permission",
    "has_permission",
    "has_published_record",
    "is_draft",
    "is_published_record",
)
