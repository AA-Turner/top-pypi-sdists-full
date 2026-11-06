"""Authoring surface for selecting connectors the Harness must discover at run time.

An authored ``ConnectorSlot`` names one connector at build time. ``AllConnectors``
names none: the set is resolved per Session, against the identity the Session runs
as, so two users of the same Agent get their own connectors.
"""

from collections.abc import Sequence
from dataclasses import dataclass

DEFAULT_CONNECTOR_COUNT_WARNING_THRESHOLD = 20


def _catalog_order(connector_name: str) -> tuple[str, str]:
    """Order connectors the way a reader would, not the way ASCII would.

    Plain ``sorted`` puts every capitalized connector ahead of every lowercase one, so a
    cap would keep ``Drawio`` and drop ``github_app`` for no reason a user could predict.
    The exact name breaks ties so the order stays total.
    """

    return connector_name.casefold(), connector_name


@dataclass(frozen=True, slots=True)
class AllConnectors:
    """Every connector that the user who runs the session has connected, as of the session's start.

    ``agents.all_connectors()`` returns it. A connector is in the set when it is active in the
    user's workspace, has MCP tools, and the user has connected it. With ``auto_auth``, the agent
    can still find the other connectors and ask the user to connect one.

    The set always uses the user's connections: it has no ``run_as="deployment"`` form.
    """

    exclude: tuple[str, ...] = ()
    """Connector names to drop from the set."""
    max_connectors: int | None = None
    """The most discovered connectors the agent mounts, the first by name. ``None`` sets no cap."""
    auto_auth: bool = True
    """Whether the agent may ask the user to connect a connector it found unconnected."""
    allow_mcp_ui: bool = False
    """Whether MCP app resources are shown for every discovered connector."""

    def __post_init__(self) -> None:
        # Validated here rather than in all_connectors(), so a selection built directly
        # from the public class holds the same contract.
        if any(not name.strip() for name in self.exclude):
            raise ValueError("all_connectors(exclude=...) must not contain blank connector names")
        if self.max_connectors is not None and self.max_connectors < 1:
            raise ValueError("all_connectors(max_connectors=...) must be at least 1")

    def candidates(self, connector_names: Sequence[str]) -> list[str]:
        """Narrow one discovered catalog to the connectors worth probing, in a stable order.

        ``max_connectors`` is deliberately not applied here. Whether the Session user has
        signed in to a connector is only known from bootstrap, so a cap applied to the
        catalog would spend its slots on connectors they never connected. :meth:`cap`
        applies it once that is known.
        """

        return sorted({name for name in connector_names if self.admits(name)}, key=_catalog_order)

    def admits(self, connector_name: str) -> bool:
        """Whether this selection covers the connector, before availability is known."""

        return connector_name not in self.exclude

    def cap(self, connector_names: Sequence[str]) -> list[str]:
        """Keep at most ``max_connectors`` of the connectors the user has signed in to.

        The order is the catalog order, so the same user gets the same connectors on
        every Session rather than whichever ones the connectors API happened to list
        first.
        """

        ordered = sorted(connector_names, key=_catalog_order)
        if self.max_connectors is None:
            return ordered
        return ordered[: self.max_connectors]


def all_connectors(
    *,
    exclude: Sequence[str] = (),
    max_connectors: int | None = None,
    auto_auth: bool = True,
    allow_mcp_ui: bool = False,
) -> AllConnectors:
    """Give the agent every connector that the user who runs the session has connected.

    ``exclude`` drops connectors by name. Leave ``max_connectors`` unset: it keeps
    the first connectors by name, not the ones the task needs. Narrow the set with
    ``exclude``.

    ``auto_auth`` and ``allow_mcp_ui`` apply to every discovered connector and
    mean what they mean on :func:`connector`. To give one connector its own
    ``credentials_name`` or ``allow_mcp_ui``, name it with ``agents.connector(...)``
    in the same list, and the named declaration wins for that connector. It must keep the
    same ``auto_auth`` and the default ``run_as``, or the session does not start. For example,
    this agent gets every connector but Jira, and Notion with the ``team`` credentials::

        agents.Agent(
            model="mistral-large-4",
            connectors=[
                agents.all_connectors(exclude=["jira"]),
                agents.connector("notion", credentials_name="team"),
            ]
        )

    Args:
        exclude: Connector names to drop from the set.
        max_connectors: The most discovered connectors the agent mounts, the first by name. Only
            connectors the user can use count, and a connector you name yourself is never capped away.
            ``None`` sets no cap.
        auto_auth: Whether the agent may ask the user to connect a connector it found unconnected.
        allow_mcp_ui: Whether MCP app resources are shown for every discovered connector.
    """

    return AllConnectors(
        exclude=tuple(exclude),
        max_connectors=max_connectors,
        auto_auth=auto_auth,
        allow_mcp_ui=allow_mcp_ui,
    )


__all__ = [
    "DEFAULT_CONNECTOR_COUNT_WARNING_THRESHOLD",
    "AllConnectors",
    "all_connectors",
]
