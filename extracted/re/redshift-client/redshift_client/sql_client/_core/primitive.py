from datetime import date, datetime, time

from fa_purity import (
    Coproduct,
)
from fa_purity.json import (
    JsonPrimitive,
)

DbTimes = Coproduct[datetime, Coproduct[date, time]]
DbPrimitive = Coproduct[JsonPrimitive, DbTimes]
