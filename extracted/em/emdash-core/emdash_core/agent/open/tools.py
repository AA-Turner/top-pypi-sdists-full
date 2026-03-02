"""Self-modification tools for Open Agent.

These tools allow the agent to manage its own capabilities
and evolve over time.
"""

from typing import TYPE_CHECKING, List, Optional
from pathlib import Path
import json

from ..tools.base import BaseTool, ToolResult, ToolCategory

if TYPE_CHECKING:
    from .capabilities import CapabilityRegistry, Capability


class AddCapabilityTool(BaseTool):
    """Tool for adding new capabilities."""

    name = "add_capability"
    description = "Add a new capability based on user needs. Use when the user wants you to consistently handle certain types of requests in a specific way."
    category = ToolCategory.LEARNING

    def __init__(self, capability_registry: "CapabilityRegistry"):
        super().__init__()
        self._registry = capability_registry

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "name": {
                    "type": "string",
                    "description": "Short name for this capability (e.g., 'pr-review-helper')",
                },
                "description": {
                    "type": "string",
                    "description": "Description of what this capability does",
                },
                "trigger_patterns": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Phrases that trigger this capability (e.g., ['review.*pr', 'pull request'])",
                },
                "tools": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tools this capability uses (optional)",
                    "default": [],
                },
                "prompt_addition": {
                    "type": "string",
                    "description": "Additional guidance to add to your system prompt when this capability is active",
                },
                "examples": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Example interactions (optional)",
                    "default": [],
                },
            },
            required=["name", "description", "trigger_patterns", "prompt_addition"],
        )

    def execute(
        self,
        name: str,
        description: str,
        trigger_patterns: List[str],
        prompt_addition: str,
        tools: Optional[List[str]] = None,
        examples: Optional[List[str]] = None,
    ) -> ToolResult:
        try:
            from .capabilities import Capability

            capability = Capability(
                name=name,
                description=description,
                trigger_patterns=trigger_patterns,
                tools=tools or [],
                prompt_addition=prompt_addition,
                examples=examples or [],
            )

            self._registry.register(capability)

            return ToolResult(
                success=True,
                data={
                    "message": f"Added capability: {name}",
                    "capability": name,
                    "total_capabilities": len(self._registry.capabilities),
                },
            )
        except ValueError as e:
            return ToolResult(
                success=False,
                error=str(e),
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Failed to add capability: {str(e)}",
            )


class RemoveCapabilityTool(BaseTool):
    """Tool for removing capabilities."""

    name = "remove_capability"
    description = "Remove a previously learned capability. Use when the user asks you to forget a specific behavior or capability."
    category = ToolCategory.LEARNING

    def __init__(self, capability_registry: "CapabilityRegistry"):
        super().__init__()
        self._registry = capability_registry

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "name": {
                    "type": "string",
                    "description": "Name of the capability to remove",
                },
            },
            required=["name"],
        )

    def execute(self, name: str) -> ToolResult:
        if self._registry.unregister(name):
            return ToolResult(
                success=True,
                data={
                    "message": f"Removed capability: {name}",
                    "remaining_capabilities": len(self._registry.capabilities),
                },
            )
        else:
            return ToolResult(
                success=False,
                error=f"Capability '{name}' not found",
            )


class ListCapabilitiesTool(BaseTool):
    """Tool for listing capabilities."""

    name = "list_capabilities"
    description = "List all learned capabilities with their usage statistics. Use when the user asks what you know or what you can do."
    category = ToolCategory.LEARNING

    def __init__(self, capability_registry: "CapabilityRegistry"):
        super().__init__()
        self._registry = capability_registry

    def get_schema(self) -> dict:
        return self._make_schema(
            properties={
                "show_details": {
                    "type": "boolean",
                    "description": "Show full details for each capability",
                    "default": False,
                },
            },
        )

    def execute(self, show_details: bool = False) -> ToolResult:
        capabilities = self._registry.list_all()

        if not capabilities:
            return ToolResult(
                success=True,
                data={
                    "message": "No capabilities learned yet.",
                    "capabilities": [],
                    "count": 0,
                },
            )

        if show_details:
            caps_data = [
                {
                    "name": c.name,
                    "description": c.description,
                    "usage_count": c.usage_count,
                    "enabled": c.enabled,
                    "trigger_patterns": c.trigger_patterns,
                }
                for c in capabilities
            ]
        else:
            caps_data = [
                {
                    "name": c.name,
                    "description": c.description,
                    "usage_count": c.usage_count,
                    "enabled": c.enabled,
                }
                for c in capabilities
            ]

        return ToolResult(
            success=True,
            data={
                "capabilities": caps_data,
                "count": len(capabilities),
                "active": sum(1 for c in capabilities if c.enabled),
            },
        )
