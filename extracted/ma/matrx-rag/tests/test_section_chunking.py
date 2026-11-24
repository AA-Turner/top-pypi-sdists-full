"""Office records chunk one section at a time (W6): a chunk never straddles two sheets, sections or slides."""

from matrx_rag.chunking import chunk_sections, chunk_text, split_sections

WORKBOOK = "# Budget\n\n## Q1\n" + "\n".join(f"Row {i}: Item: a{i}; Cost: {i}" for i in range(2, 6)) + "\n\n## Q2\nRow 2: Item: zebra-7731; Cost: 9"
DOC = "# Plan\n\n# Plan\nintro words\n\n# Goals\nship it\n\n## Risks\nrain"
DECK = "# Pitch\n\n## Slide 1: Intro\nhello\n\n## Slide 2: Problem\n- water is dirty"


def test_workbook_splits_per_sheet_with_title_trail():
    secs = split_sections(WORKBOOK, kind="workbook")
    assert [t for t, _ in secs] == ["Budget > Q1", "Budget > Q2"]


def test_no_chunk_straddles_two_sheets_and_names_its_sheet():
    chunks = chunk_sections(WORKBOOK, kind="workbook")
    assert chunks
    for c in chunks:
        assert not ("Q1" in c.content_text.split("]", 1)[0] and "zebra-7731" in c.content_text)
    hit = [c for c in chunks if "zebra-7731" in c.content_text]
    assert hit and hit[0].content_text.startswith("[Budget > Q2]")
    assert hit[0].metadata["section"] == "Budget > Q2"
    # the old behaviour: one text, one parent holding both sheets
    assert any("Q1" in c.content_text and "zebra-7731" in c.content_text for c in chunk_text(WORKBOOK))


def test_document_sections_follow_heading_path():
    assert [t for t, _ in split_sections(DOC, kind="udt_document")] == ["Plan", "Plan > Goals", "Plan > Goals > Risks"]


def test_deck_is_one_section_per_slide():
    assert [t for t, _ in split_sections(DECK, kind="deck")] == ["Pitch > Slide 1: Intro", "Pitch > Slide 2: Problem"]


def test_chunk_indexes_are_unique_and_parents_resolve():
    chunks = chunk_sections(WORKBOOK, kind="workbook")
    assert [c.chunk_index for c in chunks] == list(range(len(chunks)))
    ids = {c.chunk_id for c in chunks}
    assert all(c.parent_chunk_id in ids for c in chunks if c.parent_chunk_id)


def test_text_without_headings_falls_back_to_plain_chunking():
    assert chunk_sections("just words", kind="udt_document")[0].content_text == "just words"
