import pytest
from matrx_rag import derivation


@pytest.mark.asyncio
async def test_resume_metadata_read_failure_never_degrades_to_redo(monkeypatch) -> None:
    async def broken_lookup(_parent_id: str, _kind: str) -> list[str]:
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(derivation, "_derivative_ids", broken_lookup)

    with pytest.raises(RuntimeError, match="database unavailable"):
        await derivation.existing_section_indexes("doc-1", "section_summary")
