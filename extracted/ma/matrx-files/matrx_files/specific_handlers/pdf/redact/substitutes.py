"""Substitute generators for reversible redaction.

Two flavors per pattern category:
  - bracket style: ``[SSN_001]`` — fast, obvious to humans, may be rejected by LLMs
  - shape-preserving: ``555-00-0001`` — fools shape-checking models but harder to debug

The default map picks bracket-style. Recipes override per-pattern.
"""

from __future__ import annotations

from typing import Callable


def _bracket(category: str) -> Callable[[int], str]:
    def gen(index: int) -> str:
        return f"[{category.upper()}_{index:03d}]"
    return gen


def _ssn_shape() -> Callable[[int], str]:
    def gen(index: int) -> str:
        return f"555-00-{index:04d}"
    return gen


def _phone_shape() -> Callable[[int], str]:
    def gen(index: int) -> str:
        # 555 area code is the canonical "not in service" range for fiction.
        suffix = f"{index:04d}"
        return f"555-000-{suffix}"
    return gen


def _email_shape() -> Callable[[int], str]:
    def gen(index: int) -> str:
        return f"redacted{index:03d}@example.com"
    return gen


def _card_shape() -> Callable[[int], str]:
    """Returns a Luhn-valid placeholder. The last digit is the Luhn check digit."""
    def gen(index: int) -> str:
        body = f"4111000000{index:06d}"[:15]
        total = 0
        parity = (len(body) - 1) % 2
        for i, ch in enumerate(body):
            d = ord(ch) - 48
            if i % 2 == parity:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        check = (10 - (total % 10)) % 10
        full = body + str(check)
        return "-".join(full[i:i + 4] for i in range(0, len(full), 4))
    return gen


def _dob_shape() -> Callable[[int], str]:
    def gen(index: int) -> str:
        return f"1970-01-{(index % 28) + 1:02d}"
    return gen


# Default substitute style per pattern_id → callable(index) → str
DEFAULT_GENERATORS: dict[str, Callable[[int], str]] = {
    "ssn_us":        _bracket("SSN"),
    "ein":           _bracket("EIN"),
    "itin":          _bracket("ITIN"),
    "email":         _bracket("EMAIL"),
    "phone_us":      _bracket("PHONE"),
    "phone_intl":    _bracket("PHONE"),
    "credit_card":   _bracket("CARD"),
    "routing_us":    _bracket("ROUTING"),
    "iban":          _bracket("IBAN"),
    "bank_account":  _bracket("BANK"),
    "passport_us":   _bracket("PASSPORT"),
    "drivers_license_us": _bracket("DL"),
    "dob_iso":       _bracket("DOB"),
    "dob_us":        _bracket("DOB"),
    "dob_long":      _bracket("DOB"),
    "mrn":           _bracket("MRN"),
    "icd10":         _bracket("ICD10"),
    "cpt":           _bracket("CPT"),
    "npi":           _bracket("NPI"),
    "address_us":    _bracket("ADDRESS"),
    "us_zip":        _bracket("ZIP"),
    "person_name":   _bracket("PERSON"),
    "vin":           _bracket("VIN"),
    "ip_address":    _bracket("IP"),
    "mac_address":   _bracket("MAC"),
    "bitcoin_address": _bracket("BTC"),
    "url":           _bracket("URL"),
    "case_number":   _bracket("CASE"),
}

SHAPE_PRESERVING_GENERATORS: dict[str, Callable[[int], str]] = {
    "ssn_us":      _ssn_shape(),
    "phone_us":    _phone_shape(),
    "phone_intl":  _phone_shape(),
    "email":       _email_shape(),
    "credit_card": _card_shape(),
    "dob_iso":     _dob_shape(),
    "dob_us":      _dob_shape(),
}


def make_generator(pattern_id: str, style: str = "bracket") -> Callable[[int], str]:
    """Return a substitute generator for the given pattern + style.

    style: "bracket" or "shape" — falls back to bracket if shape isn't defined.
    """
    if style == "shape":
        gen = SHAPE_PRESERVING_GENERATORS.get(pattern_id)
        if gen is not None:
            return gen
    return DEFAULT_GENERATORS.get(pattern_id, _bracket(pattern_id.upper()))


def format_substitute(pattern_id: str, index: int, *, template: str | None = None, style: str = "bracket") -> str:
    """Top-level helper. ``template`` overrides everything else when set.

    A template may use ``{index}`` / ``{index:03d}`` / ``{pattern}`` placeholders.
    """
    if template:
        try:
            return template.format(index=index, pattern=pattern_id.upper())
        except (IndexError, KeyError, ValueError):
            return template
    return make_generator(pattern_id, style=style)(index)


__all__ = [
    "DEFAULT_GENERATORS",
    "SHAPE_PRESERVING_GENERATORS",
    "make_generator",
    "format_substitute",
]
