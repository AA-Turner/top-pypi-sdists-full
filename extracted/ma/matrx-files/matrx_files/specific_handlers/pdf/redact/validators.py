"""Validator functions for tier-strict pattern matching.

Each validator takes the matched string and returns True if the value
satisfies the strict-tier criterion (Luhn check for credit cards, mod-97
for IBAN, etc.). Validators are looked up by ID so catalogs loaded from
the DB can reference them by name.
"""

from __future__ import annotations

import re
from typing import Callable


def _digits_only(s: str) -> str:
    return re.sub(r"\D", "", s)


def luhn_valid(card: str) -> bool:
    digits = _digits_only(card)
    if not (13 <= len(digits) <= 19):
        return False
    total = 0
    parity = (len(digits) - 2) % 2
    for i, ch in enumerate(digits):
        d = ord(ch) - 48
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def ssn_valid(s: str) -> bool:
    digits = _digits_only(s)
    if len(digits) != 9:
        return False
    area = digits[:3]
    group = digits[3:5]
    serial = digits[5:]
    if area in ("000", "666") or area.startswith("9"):
        return False
    if group == "00" or serial == "0000":
        return False
    return True


def iban_valid(iban: str) -> bool:
    s = iban.replace(" ", "").upper()
    if not re.match(r"^[A-Z]{2}\d{2}[A-Z0-9]+$", s):
        return False
    if not (15 <= len(s) <= 34):
        return False
    rearranged = s[4:] + s[:4]
    expanded: list[str] = []
    for ch in rearranged:
        expanded.append(str(ord(ch) - 55) if ch.isalpha() else ch)
    try:
        return int("".join(expanded)) % 97 == 1
    except ValueError:
        return False


def routing_valid(num: str) -> bool:
    digits = _digits_only(num)
    if len(digits) != 9:
        return False
    d = [int(c) for c in digits]
    total = (
        3 * (d[0] + d[3] + d[6])
        + 7 * (d[1] + d[4] + d[7])
        + 1 * (d[2] + d[5] + d[8])
    )
    return total % 10 == 0 and total != 0


def npi_valid(num: str) -> bool:
    digits = _digits_only(num)
    if len(digits) != 10:
        return False
    # NPI uses Luhn with prefix "80840".
    return luhn_valid("80840" + digits)


def vin_valid(vin: str) -> bool:
    s = vin.upper()
    if len(s) != 17 or any(c in "IOQ" for c in s):
        return False
    transliterate = {
        "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
        "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
        "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
    }
    weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
    total = 0
    for i, ch in enumerate(s):
        if ch.isdigit():
            v = int(ch)
        elif ch in transliterate:
            v = transliterate[ch]
        else:
            return False
        total += v * weights[i]
    check = total % 11
    expected = "X" if check == 10 else str(check)
    return s[8] == expected


def cpt_valid(num: str) -> bool:
    # CPT codes are 5-digit numerics in the 00100-99999 range (loose check).
    digits = _digits_only(num)
    if len(digits) != 5:
        return False
    return 100 <= int(digits) <= 99999


VALIDATORS: dict[str, Callable[[str], bool]] = {
    "luhn": luhn_valid,
    "ssn": ssn_valid,
    "iban": iban_valid,
    "routing": routing_valid,
    "npi": npi_valid,
    "vin": vin_valid,
    "cpt": cpt_valid,
}


__all__ = [
    "luhn_valid",
    "ssn_valid",
    "iban_valid",
    "routing_valid",
    "npi_valid",
    "vin_valid",
    "cpt_valid",
    "VALIDATORS",
]
