"""Board clear / logical-delete primitives.

Clearing a board soft-deletes its tickets (sets `deleted_at`); the board row
stays live. Deleting a board additionally soft-deletes the board itself. Nothing
is ever hard-deleted -- see the board-clear design doc.

TODO: restore command -- undo is currently via re-sync only (a soft-deleted
ticket whose external id is still at source is revived by board_sync_service).
TODO: project-level clear -- when multi-board-per-project is supported, add a
wrapper that iterates a project's boards over clear_board_tickets. Today
BoardRegistration.project_id is unique, so board-clear == project-clear.
"""

from datetime import datetime, timezone

from sqlmodel import Session, select

from src.domain.board import BoardRegistration
from src.domain.ticket import Ticket


def clear_board_tickets(
    session: Session, board_id: str, *, dry_run: bool = False
) -> int:
    """Soft-delete every live (deleted_at IS NULL) ticket for `board_id`.

    Returns the number of tickets cleared (or, if dry_run, that would be
    cleared). Does not modify the board registration row.
    """
    live = session.exec(
        select(Ticket).where(
            Ticket.board_registration_id == board_id,
            Ticket.deleted_at.is_(None),
        )
    ).all()
    if dry_run:
        return len(live)
    now = datetime.now(timezone.utc)
    for ticket in live:
        ticket.deleted_at = now
        session.add(ticket)
    session.commit()
    return len(live)


def soft_delete_board(session: Session, board: BoardRegistration) -> int:
    """Logically delete a board: mark it deleted + inactive and cascade-clear
    its tickets. The board row and ticket rows are preserved for audit.

    Returns the number of tickets cleared.
    """
    count = clear_board_tickets(session, board.id)
    board.deleted_at = datetime.now(timezone.utc)
    board.is_active = False
    session.add(board)
    session.commit()
    return count
