"""A directive container (`:::tabs` … `:::`) is ONE text region (RC-B8).

Mirror of matrx-frontend `content-splitter-core` step 1c and
`components/markdown-core/directive-container.ts`: a kiln manual's tabs hold a
code fence per firing range; splitting the fence out would leave empty tabs
and a stray fence below them.
"""

from matrx_ai.processing.blocks.block_detector import split_content_into_blocks

TABS = "::::tabs\n:::tab[Cone 6]\n```bash\nkiln fire --cone 6\n```\n:::\n:::tab[Cone 10]\n| shelf | ware |\n|---|---|\n| 1 | mugs |\n:::\n::::"


def _types(md: str) -> list[tuple[str, str]]:
    return [(b.type, b.content) for b in split_content_into_blocks(md)]


def test_container_keeps_its_fences_and_tables():
    blocks = _types(f"Pick a range.\n\n{TABS}\n\nThen load.\n\n```js\nafter()\n```")
    assert blocks[0] == ("text", f"Pick a range.\n\n{TABS}\n\nThen load.")
    assert blocks[1][0] == "code"


def test_colons_inside_a_fence_never_close_the_container():
    md = ":::note\n```\n:::\n```\nstill inside\n:::\n\n```py\nx = 1\n```"
    blocks = _types(md)
    assert blocks[0] == ("text", ":::note\n```\n:::\n```\nstill inside\n:::")
    assert blocks[1][0] == "code"


def test_unclosed_container_streams_to_the_end():
    md = ":::tip[Shelf order]\n```bash\nls\n```\nstill arriving"
    assert _types(md) == [("text", md)]


def test_live_stream_never_splits_a_container_mid_stream():
    """Every live partial event keeps the tabs whole — no code block is ever
    announced for the fence inside them, at any chunk size, and the only code
    block the stream ever emits is the one AFTER the container."""
    from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor

    source = f"Pick a range.\n\n{TABS}\n\nThen load.\n\n```js\nafter()\n```"
    for chunk_size in (1, 5, 17):
        processor = StreamBlockProcessor()
        events = []
        for offset in range(0, len(source), chunk_size):
            events.extend(processor.process_token(source[offset : offset + chunk_size]))
        live = list(events)
        events.extend(processor.finalize())
        leaked = [e for e in live if e.type != "text" and "kiln fire" in (e.content or "")]
        assert leaked == [], f"chunk {chunk_size}: container fence leaked as {leaked[0].type}"
        latest = {e.block_id: e for e in events}
        texts = [e.content for e in latest.values() if e.type == "text"]
        assert any(TABS in (t or "") for t in texts)


def test_titled_image_stays_in_text_for_the_figure_caption():
    titled = '![Kiln shelf](https://example.com/k.png "Cone 6 shelf layout")'
    assert _types(f"Intro.\n\n{titled}\n\nAfter.") == [("text", f"Intro.\n\n{titled}\n\nAfter.")]
    plain = _types("Intro.\n\n![Kiln shelf](https://example.com/k.png)\n\nAfter.")
    assert [t for t, _ in plain] == ["text", "image", "text"]
