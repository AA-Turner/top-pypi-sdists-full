"""SEATS — a human gate addressed to whoever holds a named position.

A decision gate (``control.human_input`` preset ``decision``) may name a SEAT
(``decision.seat.position_id``): an org-chart position such as "Brand owner".
The gate is then addressed to whoever holds that seat AT THE MOMENT THE GATE
OPENS — resolved then, never at design time, so a seat that changes hands
between authoring and running reaches the new holder.

The seat decides who is ASKED. It is not a lock: who may ANSWER stays the
host's existing rule (the run's access, or the subject record's editors), and
the host may additionally admit the asked holder.

Positions live in the host's database, which this package never imports. The
host injects two doors once at startup:

* ``configure_seat_resolver(fn)`` — ``await fn(position_id, user_id=..,
  organization_id=..)`` returns a :class:`SeatHolder` (``holder_user_id`` None
  when nobody holds the seat), or None when no such seat exists.
* ``configure_seat_notifier(fn)`` — ``await fn(holder, run_id=.., node_id=..,
  title=.., prompt=.., organization_id=..)`` puts the question in front of the
  holder through the host's notification path. Must be idempotent per
  (run_id, node_id): a node re-executed after a crash notifies again.

A gate that names a seat while no resolver is configured FAILS — it never
silently falls back to "whoever can open the record".
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class SeatHolder:
    """Who holds a seat right now. ``holder_user_id`` None = the seat is empty."""

    position_id: str
    seat_name: str
    holder_user_id: str | None = None
    holder_name: str | None = None


SeatResolver = Callable[..., Awaitable[SeatHolder | None]]
SeatNotifier = Callable[..., Awaitable[None]]

_resolver: SeatResolver | None = None
_notifier: SeatNotifier | None = None


def configure_seat_resolver(resolver: SeatResolver | None) -> None:
    """Register (or clear, with None) the host's seat resolver."""
    global _resolver
    _resolver = resolver


def configure_seat_notifier(notifier: SeatNotifier | None) -> None:
    """Register (or clear, with None) the host's seat notifier."""
    global _notifier
    _notifier = notifier


def is_seat_resolver_configured() -> bool:
    return _resolver is not None


async def resolve_seat(
    position_id: str, *, user_id: str | None, organization_id: str | None
) -> SeatHolder | None:
    """The seat's current holder. Raises when no resolver is configured."""
    if _resolver is None:
        raise RuntimeError(
            "This decision is addressed to a seat, but no seat resolver is configured "
            "(matrx_graph.configure_seat_resolver). The gate refuses to guess who to ask."
        )
    return await _resolver(position_id, user_id=user_id, organization_id=organization_id)


async def notify_seat(
    holder: SeatHolder,
    *,
    run_id: str,
    node_id: str,
    title: str | None,
    prompt: str,
    organization_id: str | None,
) -> bool:
    """Tell the holder. False when no notifier is configured (the caller records it)."""
    if _notifier is None:
        return False
    await _notifier(
        holder,
        run_id=run_id,
        node_id=node_id,
        title=title,
        prompt=prompt,
        organization_id=organization_id,
    )
    return True


__all__ = [
    "SeatHolder",
    "SeatNotifier",
    "SeatResolver",
    "configure_seat_notifier",
    "configure_seat_resolver",
    "is_seat_resolver_configured",
    "notify_seat",
    "resolve_seat",
]
