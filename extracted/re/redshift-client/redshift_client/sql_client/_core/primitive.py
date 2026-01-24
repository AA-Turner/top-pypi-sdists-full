from datetime import (
    datetime,
)

from fa_purity import (
    Coproduct,
)
from fa_purity.json import (
    JsonPrimitive,
)

DbPrimitive = Coproduct[JsonPrimitive, datetime]
