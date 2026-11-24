"""The redaction detector takes a whole phone number (bracket included) and only a real person's name, never a
capitalised common phrase. Scan export hit two instances (RUN-07); these pin the class."""

from __future__ import annotations

import pytest

pytest.importorskip("pikepdf")
pytest.importorskip("pdfplumber")

from _pdf_corpus import _add_text_page, _new_pdf, _save  # noqa: E402

from matrx_files.specific_handlers.pdf.ops.redact_real import find_redaction_hits_bytes  # noqa: E402


def _hits(*lines: str, tier: str = "medium") -> dict[str, list[str]]:
    pdf, font = _new_pdf()
    _add_text_page(pdf, font, [(72, 740 - 20 * i, t) for i, t in enumerate(lines)])
    out: dict[str, list[str]] = {}
    for h in find_redaction_hits_bytes(_save(pdf), {"pii": True, "tier": tier})["hits"]:
        out.setdefault(h["pattern_id"], []).append(h["text"])
    return out


def test_a_bracketed_phone_goes_with_its_opening_bracket() -> None:
    assert _hits("phone (415) 555-0142")["phone_us"] == ["(415) 555-0142"]


@pytest.mark.parametrize(
    "written",
    ["(415) 555-0142", "415-555-0142", "415.555.0142", "415 555 0142", "+1 415 555 0142", "+1 (415) 555-0142",
     "1-415-555-0142", "(415)555-0142", "(415) 555-0142 x123", "415-555-0142 ext. 45"],
)
def test_every_common_phone_shape_is_taken_whole(written: str) -> None:
    assert _hits(f"call {written} today")["phone_us"] == [written]


@pytest.mark.parametrize(
    "phrase",
    ["Social Security", "Dear Sir", "Dear Madam", "United States", "United Kingdom", "Bank Account", "Credit Card",
     "Monday", "January", "Total Amount", "Invoice Summary", "Customer Service", "Driver License"],
)
def test_a_capitalised_common_phrase_is_not_a_name(phrase: str) -> None:
    assert "person_name" not in _hits(f"Note: {phrase} number on file")


def test_social_security_alone_is_not_a_name_but_the_number_still_goes() -> None:
    h = _hits("Social Security number 078-05-1120 on file")
    assert "person_name" not in h and h["ssn_us"] == ["078-05-1120"]


@pytest.mark.parametrize(
    "line,name",
    [("Contact: Dana Reyes, email x", "Dana Reyes"), ("Dear Dana Reyes,", "Dana Reyes"),
     ("Social Security Dana Reyes", "Dana Reyes"), ("Signed Dana M. Reyes", "Dana M. Reyes"),
     ("United States Dana Reyes", "Dana Reyes"), ("Dana Reyes Monday", "Dana Reyes"),
     ("Bank Account Dana Reyes", "Dana Reyes")],
)
def test_a_real_name_next_to_those_words_still_goes(line: str, name: str) -> None:
    assert _hits(line)["person_name"] == [name]
