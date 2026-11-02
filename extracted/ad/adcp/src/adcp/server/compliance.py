"""Compliance test controller handler for ADCP server implementations."""

from __future__ import annotations

from typing import Generic

from adcp.server.base import ADCPHandler, TContext


class ComplianceHandler(ADCPHandler[TContext], Generic[TContext]):
    """Handler for compliance test operations.

    Subclass this to implement compliance sandbox testing.
    Only compliance tools will be exposed via MCP.

    Example:
        class MyComplianceAgent(ComplianceHandler):
            async def comply_test_controller(self, params, context=None):
                # Implement test controller
                pass
    """

    _agent_type = "Compliance agents"
