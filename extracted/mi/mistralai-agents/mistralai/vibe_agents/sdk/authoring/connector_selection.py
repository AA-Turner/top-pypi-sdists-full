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
    """Every MCP-capable connector the Session user can already use.

    A connector is in the set when it is active for that user's workspace and
    organization, it exposes an MCP tool interface, and the user holds a usable
    credential for it. Connectors the user has not connected yet stay out of the
    set; with ``auto_auth`` the Agent can still discover them and ask the user to
    connect one, which is the only path that starts an authorization flow.

    The set is always resolved on behalf of the Session user. There is no
    deployment-identity form: "every connector the deployment can reach" is an
    unbounded service identity, and no interactive authorization can complete
    under it.
    """

    exclude: tuple[str, ...] = ()
    max_connectors: int | None = None
    auto_auth: bool = True
    allow_mcp_ui: bool = False

    def __post_init__(self) -> None:
        # Validated here rather than in all_connectors(), so a selection built directly
        # from the public class holds the same contract.
        if any(not name.strip() for name in self.exclude):
            raise ValueError("all_connectors(exclude=...) must not contain blank connector names")
        if self.max_connectors is not None and self.max_connectors < 1:
            raise ValueError("all_connectors(max_connectors=...) must be at least 1")

    def candidates(self, connector_names: Sequence[str]) -> list[str]:
        """Narrow one discovered catalog to the connectors worth probing, in a stable order.

        ``max_connectors`` is deliberately not applied here. Whether the Session user can
        actually use a connector is only known once its tools have been listed, so a cap
        applied to the catalog would spend its slots on connectors that turn out to be
        unusable. :meth:`cap` applies it once that is known.
        """

        return sorted({name for name in connector_names if self.admits(name)}, key=_catalog_order)

    def admits(self, connector_name: str) -> bool:
        """Whether this selection covers the connector, before availability is known."""

        return connector_name not in self.exclude

    def cap(self, connector_names: Sequence[str]) -> list[str]:
        """Keep at most ``max_connectors`` of the connectors that are usable.

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
    """Select every connector available to the user who runs the Session.

    ``exclude`` drops connectors by name. ``max_connectors`` caps the set; the
    connectors kept are the first by name, so the cap is reproducible. The Agent
    finds connector tools by searching for them rather than receiving them up
    front, so each connector costs its context one prompt line. A large set
    still widens that search; prefer ``exclude`` or naming the connectors the
    Agent needs over a cap, which keeps connectors by name rather than by use.

    ``auto_auth`` and ``allow_mcp_ui`` apply to every discovered connector and
    mean what they mean on :func:`connector`. Name a connector explicitly
    alongside this selection to give that one connector different options - the
    explicit declaration wins::

        agents.Agent(
            model="mistral-medium-latest",
            connectors=[
                agents.all_connectors(exclude=["jira"]),
                agents.connector("notion", credentials_name="team"),
            ]
        )
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
