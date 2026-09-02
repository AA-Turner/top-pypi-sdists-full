"""Table streaming stability — regression guard for the phantom-block class.

A multi-table message streamed at token-size chunks must reconcile to exactly
the blocks the final split produces: no phantom per-row text blocks left
unretracted, no table content frozen under a stale block type.

History (2026-07-16): each table row arriving byte-by-byte was briefly
classified as its own `text` block ("| One"), emitted to the client, then
silently dropped when the completed row was absorbed into the table — the
client kept every phantom forever. Fixes: partial-table-row emission
suppression, retraction events on phantom drop, and streaming re-type when the
re-split disagrees with a block's created type.
"""

from matrx_ai.processing.blocks.stream_processor import StreamBlockProcessor


def _make_table(start: int) -> str:
    cols = list(range(start, start + 18))
    header = "| FEC Rank | " + " | ".join(map(str, cols)) + " |"
    sep = "|---|" + "|".join(["---"] * len(cols)) + "|"
    names = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"]
    rows = [
        "| " + n + " | " + " | ".join(str(c + r + 2) for c in cols) + " |"
        for r, n in enumerate(names)
    ]
    return "\n".join([header, sep] + rows)


CONTENT = "\n".join(
    [
        "Read down to the entry corresponding to the applicable rank.",
        "",
        "**Impairment Standard: 1-20**",
        "",
        _make_table(1),
        "",
        "**Impairment Standard: 21-40**",
        "",
        _make_table(21),
        "",
        "Done.",
    ]
)


def _stream(chunk_size: int):
    proc = StreamBlockProcessor()
    events = []
    for i in range(0, len(CONTENT), chunk_size):
        events.extend(proc.process_chunk(CONTENT[i : i + chunk_size]))
    events.extend(proc.finalize())
    return events


def _final_state(events):
    """Last-write-wins view — mirrors the client's replace-on-upsert store."""
    final = {}
    for ev in events:
        d = ev.model_dump(by_alias=True)
        final[d["blockId"]] = d
    return final


def test_tables_stream_to_exact_block_set_at_all_chunk_sizes():
    for chunk_size in (1, 2, 3, 7, 16, 50, len(CONTENT)):
        final = _final_state(_stream(chunk_size))
        # Visible = what the client renders (blocks with non-empty content).
        visible = [d for d in final.values() if (d.get("content") or "").strip()]
        types = [d["type"] for d in sorted(visible, key=lambda d: d["blockIndex"])]
        assert types == ["text", "table", "text", "table", "text"], (
            f"chunk={chunk_size}: got {types}"
        )
        # Every visible block ends COMPLETE.
        assert all(d["status"] == "complete" for d in visible), f"chunk={chunk_size}"
        # Both tables carry the full 10-line markdown.
        tables = [d for d in visible if d["type"] == "table"]
        for t in tables:
            assert t["content"].count("\n") == 9, f"chunk={chunk_size}"
            assert "FEC Rank" in t["content"]


def test_phantom_blocks_are_retracted_not_orphaned():
    """Any block ever emitted that is absent from the final split must end as
    an empty COMPLETE emit (retraction) — never left status=streaming."""
    for chunk_size in (1, 3, 7):
        final = _final_state(_stream(chunk_size))
        for d in final.values():
            if not (d.get("content") or "").strip():
                assert d["status"] == "complete", (
                    f"chunk={chunk_size}: phantom {d['blockId']} left streaming"
                )


def test_table_content_never_ends_under_non_table_type():
    for chunk_size in (1, 2, 3, 7, 16, 50):
        final = _final_state(_stream(chunk_size))
        for d in final.values():
            content = d.get("content") or ""
            if "FEC Rank" in content and "|---" in content:
                assert d["type"] == "table", (
                    f"chunk={chunk_size}: table content typed {d['type']!r}"
                )
