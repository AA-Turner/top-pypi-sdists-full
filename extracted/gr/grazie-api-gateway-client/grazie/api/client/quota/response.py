from decimal import Decimal
from typing import Optional

import attrs

from grazie.api.client.utils import typ


@attrs.define(auto_attribs=True, frozen=True)
class QuotaCredit:
    amount: Decimal


@attrs.define(auto_attribs=True, frozen=True)
class QuotaId:
    quotaId: str
    userId: Optional[str] = None


@attrs.define(auto_attribs=True, frozen=True)
class Quota:
    license: str
    until: int
    current: QuotaCredit = typ(QuotaCredit)
    maximum: QuotaCredit = typ(QuotaCredit)
    quotaID: QuotaId = typ(QuotaId)


@attrs.define(auto_attribs=True, frozen=False)
class QuotaResponse:
    updated: Optional[Quota] = None
    spent: Optional[QuotaCredit] = None
    content: str = ""
