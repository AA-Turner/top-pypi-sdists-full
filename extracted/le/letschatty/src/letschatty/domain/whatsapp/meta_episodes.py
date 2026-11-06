"""An episode of Meta («episodio de Meta», api-chatty `docs/whatsapp/episodios-de-meta.md`): Meta rejecting a company's
templates for one reason (131042, a payment problem of the WABA; 131048, a number limited for spam) from the first
rejection until Meta delivers again or the rejections stop. The model and the port every store of it implements; one
instance per collection (`meta_problemas_de_pago`, `meta_numeros_limitados`).

«Am I the first?» and «am I the one who closes?» are decided by conditional writes, so only the worker that opened an
episode publishes its banner and its notice, and only the one that closed it takes the banner down. It does not
disconnect the number (api-chatty `docs/problema-de-pago-meta.md`).

The key names the stored `_id`: `<company>:<waba>` (payment), `<company>:<account>` (limited number) or `<company>`
alone (a company without WABA or without accounts, and the payment episodes stored before the accounts). The company
is never part of a filter: the key names the document, as before.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import AsyncIterator, List, Optional, Protocol, Union

from pydantic import BaseModel, ConfigDict

#: The two states of an episode, as they are stored.
OPEN = "abierto"
CLOSED = "cerrado"
#: Why an episode was closed, as it is stored.
CLOSED_BY_DELIVERY = "entrega"
CLOSED_BY_SILENCE = "silencio"


@dataclass(frozen=True)
class EpisodeKey:
    """The company and, when there is one, what the episode is scoped to (the WABA or the account)."""

    company_id: str
    scope: Optional[str] = None

    @property
    def id(self) -> str:
        return f"{self.company_id}:{self.scope}" if self.scope else str(self.company_id)

    @classmethod
    def from_id(cls, episode_id: str) -> "EpisodeKey":
        """The inverse of `id`: `EpisodeKey.from_id(k).id == k` for every text."""
        company_id, separator, scope = str(episode_id).partition(":")
        return cls(company_id, scope if separator else None)


class MetaEpisode(BaseModel):
    """An episode as it was read. Every field but `id` is optional: the episodes stored before the accounts have no
    `waba_id`, `account_id`, `account_name` nor `portfolio_id`. The dates are the stored ones (Mongo returns them
    without zone; they are UTC), read as they are: a date stored as text stays text and fails where `main` failed with
    it (the closing notice, Chatty Health), never here. `rejections` is 0 when the field is missing and None when it is
    stored as `null`."""

    model_config = ConfigDict(frozen=True)

    id: str
    status: Optional[str] = None
    company_id: Optional[str] = None
    company_name: Optional[str] = None
    display_phone_number: Optional[str] = None
    waba_id: Optional[str] = None
    portfolio_id: Optional[str] = None
    account_id: Optional[str] = None
    account_name: Optional[str] = None
    # `Union[…, str, …]` only for the two cases of text `main` handles (prod, 2026-11-04: always a date): a text stays text
    # and fails where `main` failed with it, in the closing notice and in Chatty Health, not when it is read.
    opened_at: Union[datetime, str, None] = None
    last_rejection_at: Union[datetime, str, None] = None
    rejections: Optional[int] = 0
    detail: Optional[str] = None
    banner_notification_id: Optional[str] = None
    closed_at: Union[datetime, str, None] = None
    closed_by: Optional[str] = None

    @property
    def key(self) -> EpisodeKey:
        return EpisodeKey.from_id(self.id)


class MetaEpisodeRepository(Protocol):
    async def add_rejection(self, company_id: str, key: EpisodeKey, at: datetime) -> bool:
        """One more rejection on the open episode of `key` (`rejections + 1`, `last_rejection_at = at`). False when
        it is not open."""
        ...

    async def open(self, company_id: str, episode: MetaEpisode) -> bool:
        """Opens `episode` (open, its fields, one rejection, no banner, no closing) over whatever closed document has
        its key, or as a new one. False when another worker opened it in between: then this rejection was added to
        that one."""
        ...

    async def set_banner(self, company_id: str, key: EpisodeKey, opened_at: datetime, notification_id: str) -> None:
        """Stores the banner of the episode only if it is still the open one opened at `opened_at`."""
        ...

    async def close(self, company_id: str, key: EpisodeKey, *, at: datetime, by: str,
                    last_rejection_before: datetime) -> Optional[MetaEpisode]:
        """Closes the episode of `key` if it is open and its last rejection is before `last_rejection_before`. The
        episode as it was before closing; None when there was nothing to close (another worker closed it)."""
        ...

    def due(self, last_rejection_before: datetime) -> AsyncIterator[EpisodeKey]:
        """The open episodes of every company whose last rejection is before `last_rejection_before`, read as they are
        closed (only their keys)."""
        ...

    async def open_keys(self) -> List[EpisodeKey]:
        """The open episodes of every company (only their keys)."""
        ...


class MetaEpisodeOverviewRepository(Protocol):
    """What Chatty Health reads, of every company. Apart from `MetaEpisodeRepository`: it changes for the board, not for
    the life of an episode. The same Mongo class implements both."""

    async def companies_with_open(self) -> List[Optional[str]]:
        """The distinct `company_id` of the open episodes."""
        ...

    async def count_closed_since(self, since: datetime) -> int:
        """The episodes closed at or after `since`."""
        ...

    async def oldest_open(self, limit: int) -> List[MetaEpisode]:
        """The open episodes of every company, oldest `opened_at` first, at most `limit`."""
        ...
