# SPDX-FileCopyrightText: 2026 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
"""Unit tests for omnibase_compat.protocols.__init__ exports."""

from __future__ import annotations

import pytest


@pytest.mark.unit
def test_protocols_package_importable() -> None:
    import omnibase_compat.protocols  # noqa: F401


@pytest.mark.unit
def test_all_exports_present() -> None:
    from omnibase_compat.protocols import __all__

    expected = {
        "ProtocolProjectionDatabase",
        "ProtocolProjectionDatabaseSync",
        "ProtocolProjectTracker",
    }
    assert set(__all__) == expected


@pytest.mark.unit
def test_protocol_projection_database_exported() -> None:
    from omnibase_compat.protocols import ProtocolProjectionDatabase

    assert ProtocolProjectionDatabase.__name__ == "ProtocolProjectionDatabase"


@pytest.mark.unit
def test_protocol_projection_database_sync_exported() -> None:
    from omnibase_compat.protocols import ProtocolProjectionDatabaseSync

    assert ProtocolProjectionDatabaseSync.__name__ == "ProtocolProjectionDatabaseSync"


@pytest.mark.unit
def test_protocol_project_tracker_exported() -> None:
    from omnibase_compat.protocols import ProtocolProjectTracker

    assert ProtocolProjectTracker.__name__ == "ProtocolProjectTracker"
