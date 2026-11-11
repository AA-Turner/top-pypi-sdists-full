"""Amounts and prices as the SDK prints them - every CLI line, and a chat's repr - by the docs' one rule (reference,
"Amounts and prices"), the console's alike.

In one sentence: an amount in US dollars → two decimals from $1 (`$12.40`, `$1,234.50`), four below (`$0.0042`,
`$0.4200`), `$0.00` for none, `<$0.0001` for one that is not none but rounds to nothing, a credit below zero with its
sign first (`-$5.00`); a price - a card's hour, a core-hour, a GiB-hour, a GB-month - → the same, but to the cent where
it is a whole number of cents (`$0.84`, `$0.12`), four places only where it has a fraction of one (`$0.0396`), and an
hour's said by the hour (`$0.84/h`) - usage is billed by the second, and a price is always said by the hour; a plan's fee
and its monthly credit → whole dollars (`$20`, as in "$20 a month"). Rounded as
the console rounds, so the two never differ in a last digit: from $1 the figure as written rounded half up (its
toLocaleString: $3.465 is $3.47, where Python's own format says $3.46), under $1 the number itself rounded half up (its
toFixed: $0.03125 is $0.0313).

WHY one module: each command wrote its own - `seq eval` four places, `seq usage` two, `seq gpus` a price an hour and
another a second, `seq policy estimate` cents an hour - so one eval's cost read three ways across the CLI and the
console.
It is the library's, not the CLI's, because a chat's repr says its cost too; what a call returns keeps its numbers
(cost_usd), only what is printed is said here.



`--json` and `--csv` print what the gateway sent, for scripts; nothing here touches them.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Any

_CENT, _PLACES4, _DOLLAR = Decimal("0.01"), Decimal("0.0001"), Decimal("1")


def money(v: Any) -> str:
    """An amount: two decimals from $1, four below, `$0.00` for none (None or zero), `<$0.0001` for one under that."""
    x = float(v or 0)
    if not x:
        return "$0.00"
    sign, a = ("-" if x < 0 else ""), abs(x)
    four = Decimal(a).quantize(_PLACES4, rounding=ROUND_HALF_UP)
    if not four:
        return f"{sign}<$0.0001"
    if four < 1:
        return f"{sign}${four}"

    return f"{sign}${Decimal(repr(a)).quantize(_CENT, rounding=ROUND_HALF_UP):,}"


def as_shown(v: Any) -> float:
    """The amount money() shows, as a number: for figures said side by side that must add up (a balance, what is held
    of it and what is left)."""
    return float(money(v).replace("$", "").replace(",", "").replace("<", ""))


def price(v: Any) -> str:
    """A price - a card's hour, a core-hour, a GiB-hour, a GB-month, or a worker's hour from them: as money() says it,
    but to the cent where it is a whole number of cents (`$0.84`, `$5.10`, `$0.12`), so a price list reads one way - four
    places only where it has a fraction of a cent (`$0.0396`, `$0.2021`). Before, every price under $1 had four, so `seq
    gpus` listed an L4 at $0.8400/h beside an A100 at $5.10/h.
"""
    four = Decimal(abs(float(v or 0))).quantize(_PLACES4, rounding=ROUND_HALF_UP)
    if 0 < four < 1 and four == four.quantize(_CENT):
        return f"{'-' if float(v) < 0 else ''}${four.quantize(_CENT)}"
    return money(v)


def per_hour(v: Any) -> str:
    """A price: the amount an hour, by price()'s rule (`$0.84/h`, `$0.9612/h`)."""
    return f"{price(v)}/h"


def whole(v: Any) -> str:
    """A plan's monthly fee or its monthly credit: whole dollars (`$20`)."""
    return f"${Decimal(repr(float(v or 0))).quantize(_DOLLAR, rounding=ROUND_HALF_UP):,}"


def cents(v: Any) -> str:
    """An amount the database already keeps to the cent - a period's spend (period_spent_usd), a monthly figure: two
    decimals, always. money() shows below $1 to four places, which on a cent-rounded value is false precision (and read
    against an un-rounded figure like free credit used, the two looked inconsistent).
"""
    x = float(v or 0)
    sign, a = ("-" if x < 0 else ""), abs(x)
    return f"{sign}${Decimal(repr(a)).quantize(_CENT, rounding=ROUND_HALF_UP):,}"
