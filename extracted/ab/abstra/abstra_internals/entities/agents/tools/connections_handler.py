"""Tool handlers for connector actions.

Actions are spread in the execute tool's description so the agent can find
them directly without a separate search step. A details tool lets the agent
retrieve parameter schemas before executing.
"""

import json
import re
from typing import Any, Dict, List, Optional, Set

from abstra_internals.repositories.connectors import ConnectorsRepository


def _validate_params(
    action_input: Dict[str, Any], valid_keys: Set[str]
) -> Optional[str]:
    """Return an error message if action_input contains unknown keys."""
    unknown = set(action_input.keys()) - valid_keys
    if unknown:
        return (
            f"Unknown parameter(s): {unknown}. "
            f"Valid parameters are: {valid_keys}. "
            f"Use exactly these parameter names."
        )
    return None


_DETAILS_PARAMS = {"connection_name", "action_name", "search"}
_EXECUTE_PARAMS = {"connection_name", "action_name", "parameters"}


def _format_connections_summary(permitted: Dict[str, List[str]]) -> str:
    """Format connection names + action count for the tool description."""
    lines = []
    for conn_name, actions in permitted.items():
        lines.append(f"  {conn_name} ({len(actions)} actions)")
    return "\n".join(lines)


def _filter_actions(actions: List[str], pattern: str) -> List[str]:
    """Filter action names using regex pattern (case-insensitive)."""
    if not pattern:
        return actions
    try:
        regex = re.compile(pattern, re.IGNORECASE)
        return [a for a in actions if regex.search(a)]
    except re.error:
        # Fallback to substring match if regex is invalid
        pattern_lower = pattern.lower()
        return [a for a in actions if pattern_lower in a.lower()]


class GetConnectionActionDetailsHandler:
    """Get details and parameter schema for a connection action, or list available actions."""

    def __init__(
        self,
        permitted_actions: Dict[str, List[str]],
        connectors_repo: ConnectorsRepository,
    ) -> None:
        self._permitted = permitted_actions
        self._connectors_repo = connectors_repo

    @property
    def name(self) -> str:
        return "get_connection_action_details"

    @property
    def description(self) -> str:
        connections = list(self._permitted.keys())
        return (
            f"Discover and inspect connection actions. "
            f"Available connections: {connections}. "
            f"Two modes: "
            f"(1) List actions: provide connection_name and search (regex) to find actions. "
            f"ALWAYS use the search parameter to filter — connections can have hundreds of actions. "
            f"Example: search='user|email|lookup' to find user-related actions. "
            f"(2) Get details: provide connection_name and action_name to get the parameter schema."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "connection_name": {
                    "type": "string",
                    "description": "The name of the connection.",
                },
                "action_name": {
                    "type": "string",
                    "description": "The exact name of the action to get parameter schema for. Omit to list available actions.",
                },
                "search": {
                    "type": "string",
                    "description": "Regex to filter action names when listing (e.g. 'chat|message|send'). Only used when action_name is omitted.",
                },
            },
            "required": ["connection_name"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        error = _validate_params(action_input, _DETAILS_PARAMS)
        if error:
            return json.dumps({"error": error})

        connection_name = action_input.get("connection_name", "")
        action_name = action_input.get("action_name", "")
        search = action_input.get("search", "")

        if connection_name not in self._permitted:
            available = list(self._permitted.keys())
            return json.dumps(
                {
                    "error": f"Connection '{connection_name}' not available. Available: {available}"
                }
            )

        permitted_actions = self._permitted[connection_name]

        # Mode 1: List/search actions (no action_name provided)
        if not action_name:
            filtered = _filter_actions(permitted_actions, search)
            return json.dumps(
                {
                    "connection_name": connection_name,
                    "total_actions": len(permitted_actions),
                    "showing": len(filtered),
                    "actions": filtered,
                    "hint": "Use execute_connection_action with one of these exact action names. "
                    "Call get_connection_action_details with action_name to see required parameters.",
                },
            )

        # Mode 2: Get specific action details
        if action_name not in permitted_actions:
            # Suggest similar actions
            similar = _filter_actions(permitted_actions, action_name.replace("_", "|"))
            return json.dumps(
                {
                    "error": f"Action '{action_name}' not found for '{connection_name}'.",
                    "similar_actions": similar[:10],
                    "hint": "Use search parameter to find the right action name.",
                }
            )

        try:
            result = self._connectors_repo.get_connection_action_details(
                connection_name=connection_name,
                action_name=action_name,
            )
            return json.dumps(result.to_dict(), default=str)
        except Exception:
            # Fallback: endpoint may not be deployed yet — confirm action exists
            return json.dumps(
                {
                    "action_name": action_name,
                    "connection_name": connection_name,
                    "hint": "Action exists but detailed schema is not available. "
                    "Try calling execute_connection_action directly — "
                    "common parameters are usually documented in the API docs for this service.",
                }
            )


class ExecuteConnectionActionHandler:
    """Execute a specific action on a connection."""

    def __init__(
        self,
        permitted_actions: Dict[str, List[str]],
        connectors_repo: ConnectorsRepository,
    ) -> None:
        self._permitted = permitted_actions
        self._connectors_repo = connectors_repo

    @property
    def name(self) -> str:
        return "execute_connection_action"

    @property
    def description(self) -> str:
        summary = _format_connections_summary(self._permitted)
        return (
            f"Execute an action on a connection. "
            f"Available connections:\n{summary}\n"
            f"Use get_connection_action_details to discover action names and get required parameters."
        )

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "connection_name": {
                    "type": "string",
                    "description": "The name of the connection.",
                },
                "action_name": {
                    "type": "string",
                    "description": "The name of the action to execute.",
                },
                "parameters": {
                    "type": "object",
                    "description": 'Parameters for the action as a JSON object. All action-specific fields go INSIDE this object (e.g. {"email": "user@example.com"}). Pass {} if none needed.',
                },
            },
            "required": ["connection_name", "action_name"],
        }

    def execute(self, action_input: Dict[str, Any]) -> str:
        error = _validate_params(action_input, _EXECUTE_PARAMS)
        if error:
            return json.dumps({"error": error})

        connection_name = action_input.get("connection_name", "")
        action_name = action_input.get("action_name", "")
        parameters = action_input.get("parameters", {})

        permitted = self._permitted.get(connection_name, [])
        if not permitted:
            available_connections = list(self._permitted.keys())
            return json.dumps(
                {
                    "error": f"Connection '{connection_name}' not available.",
                    "available_connections": available_connections,
                }
            )
        if action_name not in permitted:
            return json.dumps(
                {
                    "error": f"Action '{action_name}' not found for connection '{connection_name}'.",
                    "hint": "Use get_connection_action_details with only connection_name to list available actions, "
                    "or use search parameter to filter by regex.",
                }
            )

        try:
            result = self._connectors_repo.run_connection_action(
                connection_name=connection_name,
                action=action_name,
                payload=parameters,
            )
            return json.dumps(result, default=str)
        except Exception as e:
            return json.dumps({"error": f"Error executing action: {str(e)}"})
