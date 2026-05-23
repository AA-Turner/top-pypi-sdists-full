from collections.abc import Iterable
from typing import Any, Dict, List, Optional, Set, Union

from .base import AgentTools


def to_connections(c: Optional[Union[str, Iterable[str]]]) -> Optional[Set[str]]:
    if c is None:
        return None
    elif isinstance(c, list):
        return set(c)
    elif isinstance(c, str):
        return set([c])
    raise ValueError(f"Invalid connection: {c}")


def to_actions(a: Optional[Union[str, Iterable[str]]]) -> Optional[Set[str]]:
    if a is None:
        return None
    elif isinstance(a, list):
        return set(a)
    elif isinstance(a, str):
        return set([a])
    raise ValueError(f"Invalid action: {a}")


def to_params(p: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return p or {}


class ConnectorsTools(AgentTools):
    """
    Toolkit that lets an agent call your project's configured connectors (Slack, Stripe, email providers, custom HTTP integrations, etc.). The agent gets a single `call(connection, action, params)` tool, optionally restricted to specific connections and actions.
    """

    connections: Optional[Set[str]]
    actions: Optional[Set[str]]
    params: Dict[str, Any]

    def __init__(
        self,
        connection: Optional[Union[str, Iterable[str]]] = None,
        action: Optional[Union[str, Iterable[str]]] = None,
        params: Optional[Dict[str, Any]] = None,
    ):
        """
        Build a ConnectorsTools toolkit, optionally scoped to specific connections, actions, and default params.

        Args:
            connection (Optional): Restrict the agent to a single connection name (e.g. `"slack"`) or a list of names. `None` allows any configured connection. Defaults to None.
            action (Optional): Restrict the agent to a single action name (e.g. `"send_message"`) or a list of names. `None` allows any action. Defaults to None.
            params (Optional): Default parameters merged into every `call()` (call-site values take precedence). Useful for fixed values like channel IDs or API versions. Defaults to None.
        """
        self.connections = to_connections(connection)
        self.actions = to_actions(action)
        self.params = to_params(params)

    def call(self, connection: str, action: str, params: Dict[str, Any] = {}) -> Any:
        from abstra.connectors import run_connection_action

        if self.connections is not None and connection not in self.connections:
            raise ValueError(f"Connection '{connection}' is not allowed.")

        if self.actions is not None and action not in self.actions:
            raise ValueError(f"Action '{action}' is not allowed.")
        # Defaults are filled in only when the agent did not pass the key —
        # call-site values win. Matches the documented "default" semantics
        # (TablesTools.where is the opposite: it scopes, so toolkit wins.)
        params = {**self.params, **params}
        return run_connection_action(connection, action, params)

    def __tools__(self) -> List[str]:
        return [
            self.call.__name__,
        ]
