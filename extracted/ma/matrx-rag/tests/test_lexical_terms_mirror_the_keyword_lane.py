"""``matrx_rag.lexical_terms`` judges a match the way ``rag.recall_lexical`` (kg_046) does.

Expected stems are the Snowball english (Porter2) reference outputs — the stemmer Postgres's
``english_stem`` dictionary runs — taken from the Snowball project's published vocabulary/output
pairs, never from this module. Breaks caught: a step of the stemmer wrong (a plural, a gerund, a
derivational suffix), a stop word taking part, a short stem used as a prefix (the SQL only prefixes a
stem of 4+ letters), a digit found inside another number, accent folding the engine does not do.
"""

from __future__ import annotations

import pytest

from matrx_rag.lexical_terms import english_stem, holds_every_term, lexical_terms


@pytest.mark.parametrize(
    ("word", "stem"),
    [
        ("invoices", "invoic"), ("signatures", "signatur"), ("running", "run"), ("runs", "run"),
        ("caresses", "caress"), ("ponies", "poni"), ("cried", "cri"), ("agreed", "agre"),
        ("hoping", "hope"), ("controlled", "control"), ("happiness", "happi"), ("relational", "relat"),
        ("conditional", "condit"), ("electricity", "electr"), ("adjustment", "adjust"), ("adoption", "adopt"),
        ("generously", "generous"), ("communication", "communic"), ("abilities", "abil"), ("skies", "sky"),
        ("succeeded", "succeed"), ("consolidated", "consolid"), ("dental", "dental"), ("cease", "ceas"),
    ],
)
def test_the_stem_is_the_snowball_english_stem(word: str, stem: str) -> None:
    assert english_stem(word) == stem


@pytest.mark.parametrize(
    ("query", "text", "matched"),
    [
        ("invoices", "Invoice 5 total due", True),  # invoic:* finds invoice
        ("signatures", "Patient signature on file", True),
        ("terms of service", "Terms and Service", True),  # "of" is a stop word: no part
        ("running", "runs daily", False),  # stem "run" is under 4 letters: matched only as itself
        ("running", "the pump is running", True),
        ("4", "Room 14", False),  # a digit stands alone
        ("4", "Room 4", True),
        ("zqxjvbn", "Invoice 5 total due", False),
        ("cafe", "Café menu", False),  # the simple config does not fold accents: neither does this
        ("請假申請表", "請假申請表 王小明", True),  # a run without spaces is one word, as in the engine
        ("申請表", "請假申請表 王小明", False),
        ("of the", "the table of contents", True),  # every word a stop word: they all take part
    ],
)
def test_holds_every_term_matches_what_the_keyword_lane_matches(query: str, text: str, matched: bool) -> None:
    assert holds_every_term(lexical_terms(query), text) is matched


def test_a_query_with_search_operators_keeps_its_strict_words() -> None:
    terms = lexical_terms('"repair invoices" -draft')
    assert [t.word for t in terms] == ["repair", "invoices"]
    assert not holds_every_term(terms, "Repair invoice")
