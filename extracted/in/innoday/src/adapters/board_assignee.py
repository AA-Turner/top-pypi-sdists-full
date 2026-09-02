"""The assignee identity a board reported, carried alongside the Ticket.

Adapters build `Ticket` domain objects, and `Ticket` deliberately stores only
the assignee's *display name* (`Ticket.assignee`) — the board's own truth. To
resolve that person to an InnoDay user, board sync also needs the email and the
board's user id where the board exposes them, and neither is a ticket column.

Rather than change what `get_tickets` returns — other callers depend on that
shape — the adapter attaches a `BoardAssignee` to the ticket instance and
`BoardSyncService._ticket_to_external_dict` reads it back out. It is transient:
never persisted, never reloaded, and gone after a session refresh.

`object.__setattr__` is required. `Ticket` is a SQLModel table model, so a plain
`ticket.foo = ...` for a name that is not a mapped field raises
``ValueError: "Ticket" object has no field "foo"``. Writing straight to the
instance dict bypasses both Pydantic's field check and SQLAlchemy's
instrumentation, which only tracks mapped keys — so nothing about this reaches
the database.
"""

from dataclasses import dataclass
from typing import Any, Optional

_ATTR = "_board_assignee"


@dataclass(frozen=True)
class BoardAssignee:
    """Everything a board told us about who a ticket is assigned to."""

    display_name: Optional[str] = None
    email: Optional[str] = None
    board_user_id: Optional[str] = None

    def is_empty(self) -> bool:
        return not (self.display_name or self.email or self.board_user_id)


def attach_board_assignee(ticket: Any, assignee: Optional[BoardAssignee]) -> None:
    """Stash the board's assignee identity on a Ticket instance."""
    object.__setattr__(ticket, _ATTR, assignee)


def read_board_assignee(ticket: Any) -> Optional[BoardAssignee]:
    """Read back what `attach_board_assignee` stashed, if anything."""
    return getattr(ticket, _ATTR, None)
