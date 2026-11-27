"""How Meta bills a WABA («facturación de la WABA», api-chatty `docs/meta-gastos/tdd.md`): its currency and its time zone,
as Meta answers `GET /{waba_id}?fields=currency,timezone_id`. Its own document per WABA, not a field of
`whatsapp_wabas`: that document is rewritten whole by every upsert, and a writer that does not know the currency would
erase it. The month of a WABA starts at 00:00 of its zone, as Meta's.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Protocol


#: Where a WABA's billing came from: Meta's answer, or the Chatty team's correction when Meta does not answer.
FROM_META = "meta"
BY_HAND = "a_mano"


@dataclass(frozen=True)
class WabaBilling:
    waba_id: str
    currency: Optional[str]
    timezone_id: Optional[str]
    read_at: datetime
    source: str = FROM_META


class WabaBillingRepository(Protocol):
    async def of(self, waba_ids: List[str]) -> Dict[str, WabaBilling]:
        """The billing of each WABA that has one stored; a WABA without it is absent (never guessed)."""
        ...

    async def save(self, billing: WabaBilling) -> None:
        """Stores (or replaces) the billing of the WABA (from Meta or by hand)."""
        ...

    async def all(self) -> List[WabaBilling]:
        """Every stored billing (the backoffice list)."""
        ...
