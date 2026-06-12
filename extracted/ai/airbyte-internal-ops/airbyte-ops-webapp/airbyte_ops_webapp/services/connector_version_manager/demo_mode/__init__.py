"""Demo-mode adapter implementations for Connector Pinning."""

from airbyte_ops_webapp.services.connector_version_manager.demo_mode.mock_adapter import (
    MockPinningAdapter,
)

__all__ = ["MockPinningAdapter"]
