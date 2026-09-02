from matrx_ai.processing.blocks.parsers.structured_info_parser import parse_structured_info


def test_structured_info_parser_matches_legacy_markdown_vocabulary() -> None:
    parsed = parse_structured_info(
        """**Release Brief**
Ready for review.

**Owners**
* **Backend:** Priya
- Frontend: Marco
Notes stay in the section body.
"""
    )
    assert parsed is not None
    assert parsed.title == "Release Brief"
    assert parsed.description == "Ready for review."
    assert parsed.sections[0].heading == "Owners"
    assert parsed.sections[0].body == "Notes stay in the section body."
    assert parsed.sections[0].items[0].model_dump() == {"text": "Priya", "label": "Backend"}


def test_structured_info_requires_a_bold_heading() -> None:
    assert parse_structured_info("plain markdown only") is None
