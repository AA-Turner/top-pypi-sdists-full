"""Tests for flashcard_parser.py."""

from matrx_ai.processing.blocks.parsers.flashcard_parser import parse_flashcards


class TestParseFlashcards:
    def test_basic_cards_streaming(self):
        # Without closing tag, the last card is partial (streaming behavior)
        content = """Front: What is Python?
Back: A programming language

---

Front: What is 2+2?
Back: 4"""
        result = parse_flashcards(content)
        # New streaming model (no partial_card): one growing `cards` list; the
        # in-progress last card is appended with back=None until finalize.
        assert len(result.cards) == 2
        assert result.cards[0].front == "What is Python?"
        assert result.cards[0].back == "A programming language"
        assert result.cards[1].front == "What is 2+2?"
        assert result.cards[1].back is None
        assert result.is_complete is False

    def test_basic_cards_complete(self):
        content = """Front: What is Python?
Back: A programming language

---

Front: What is 2+2?
Back: 4
</flashcards>"""
        result = parse_flashcards(content)
        assert len(result.cards) == 2
        assert result.is_complete is True

    def test_question_answer_format(self):
        # Question/Answer maps to front/back. is_final=True flushes the last card's
        # back (streaming would withhold it as still-being-written).
        content = """Question: What is AI?
Answer: Artificial Intelligence"""
        result = parse_flashcards(content, is_final=True)
        assert len(result.cards) == 1
        assert result.cards[0].front == "What is AI?"
        assert result.cards[0].back == "Artificial Intelligence"

    def test_incomplete_card(self):
        content = """Front: Complete card
Back: Has answer

---

Front: Incomplete card"""
        # is_final=True: the incomplete last card (front sealed, no Back:) is
        # flushed with back=None (streaming withholds it entirely until finalize).
        result = parse_flashcards(content, is_final=True)
        assert len(result.cards) == 2
        assert result.cards[0].front == "Complete card"
        assert result.cards[1].front == "Incomplete card"
        assert result.cards[1].back is None

    def test_is_complete_flag(self):
        content = """Front: Q
Back: A
</flashcards>"""
        result = parse_flashcards(content)
        assert result.is_complete is True

    def test_empty_content(self):
        result = parse_flashcards("")
        assert len(result.cards) == 0
