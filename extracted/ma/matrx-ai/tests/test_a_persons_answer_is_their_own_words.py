"""Review 11 (I5): an answer typed into a card's "Other" escape was stored and read as "Other — About $45k a month".
The UI writes its own label "Other" into ``selected`` (or ``action``) beside the typed ``freeform``; that label is the
card's, never the person's. ``matrx_ai.tools.person_answer_words.answer_words`` is the ONE extraction every ask
consumer reads (the Understanding card writer, the agent's answer summary, the chat title)."""

from __future__ import annotations

from matrx_ai.tools.person_answer_words import answer_words


def test_the_cards_other_label_never_rides_into_the_persons_words() -> None:
    assert answer_words({"selected": ["Other"], "freeform": "About $45k a month"}) == "About $45k a month"
    assert answer_words({"action": "Other", "freeform": "I gave up, try again"}) == "I gave up, try again"
    assert answer_words({"selected": ["6-15", "Other"], "freeform": "plus two seasonal"}) == "6-15 — plus two seasonal"


def test_every_other_answer_shape_reads_as_before() -> None:
    assert answer_words({"selected": ["Other"]}) == "Other"  # a pick of an option named Other, nothing typed
    assert answer_words({"selected": ["A", "C"]}) == "A, C"
    assert answer_words({"answer": "  Lakeside Bakery "}) == "Lakeside Bakery"
    assert answer_words({"confirmed": False}) == "No"
    assert answer_words({"action": "Done — I clicked it"}) == "Done — I clicked it"
    assert answer_words({"freeform": "only after 3pm"}) == "only after 3pm"
    assert answer_words({"answer": "x", "cancelled": True}) is None
    assert answer_words({}) is None and answer_words("nope") is None
