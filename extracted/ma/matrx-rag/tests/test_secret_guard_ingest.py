"""Forcing function for the RAG secret guard (2026-09-13 leak class).

The leak: a ``workbench.notes`` row whose body was a raw ``.env`` dump was
resolved, chunked, embedded and stored verbatim — and ``knowledge_search``
then served the live values of ``ADMIN_API_TOKEN`` and several provider keys
back to any agent that asked.

These tests drive the REAL seams (``sources.resolve`` over a stand-in Notes
row, and ``chunking.chunk_text`` / ``chunk_code``) with a fixture that has the
exact shape of the offending note, and assert that no fixture VALUE survives
into anything that would be stored or embedded. Delete the guard call in
either seam and these go red on the first assert.
"""

from __future__ import annotations

import pytest
from matrx_rag import chunking, sources

# Synthetic values with the shape of the real ones. If any of these strings
# appears in a chunk, the pipeline would have stored a live credential.
FIXTURE_VALUES = {
    "ADMIN_API_TOKEN": "9f8b7a6c5d4e3f2a1b0c9d8e7f6a5b4c",
    "AHREFS_MATRIX_API_KEY": "0Ab1Cd2Ef3Gh4Ij5Kl6Mn7Op8Qr9St",
    "ANTHROPIC_KEY": "sk-ant-api03-AbCdEf0123456789AbCdEf0123456789xyz",
    "OPENAI_API_KEY": "sk-proj-ZZZZaaaa1111bbbb2222cccc3333dddd",
    "SUPABASE_SERVICE_ROLE_KEY": "eyJhbGciOiJIUzI1NiJ9.eyJyb2xlIjoic2VydmljZSJ9.QQQQQQQQQQQQ",
    "DATABASE_URL_PASSWORD": "s3cr3tp4ssw0rd",
}

ENV_NOTE = f"""my .env backup

ADMIN_API_TOKEN={FIXTURE_VALUES["ADMIN_API_TOKEN"]}
AHREFS_MATRIX_API_KEY={FIXTURE_VALUES["AHREFS_MATRIX_API_KEY"]}
ANTHROPIC_KEY={FIXTURE_VALUES["ANTHROPIC_KEY"]}
OPENAI_API_KEY={FIXTURE_VALUES["OPENAI_API_KEY"]}
SUPABASE_SERVICE_ROLE_KEY={FIXTURE_VALUES["SUPABASE_SERVICE_ROLE_KEY"]}
DATABASE_URL=postgres://app:{FIXTURE_VALUES["DATABASE_URL_PASSWORD"]}@db.internal:5432/main
PORT=8000
APP_NAME=aidream
"""

NOTE_ID = "00000000-0000-4000-8000-00000000feed"
USER_ID = "00000000-0000-4000-8000-0000000000aa"


def _install_fake_notes(monkeypatch: pytest.MonkeyPatch, content: str) -> None:
    """Stand in for the ORM's Notes model with ONE row holding ``content``."""

    class _NotesQuery:
        async def values(self, *fields: str) -> list[dict[str, object]]:
            return [
                {
                    "id": NOTE_ID,
                    "created_by": USER_ID,
                    "organization_id": "00000000-0000-4000-8000-0000000000bb",
                    "label": "env backup",
                    "content": content,
                    "home_scope_id": None,
                    "tags": None,
                    "metadata": {},
                }
            ]

    class _Notes:
        @classmethod
        def filter(cls, **kwargs: object) -> _NotesQuery:
            return _NotesQuery()

    monkeypatch.setattr(sources, "get_db_model", lambda name: _Notes)


@pytest.mark.asyncio
async def test_resolved_note_carries_no_secret_values_and_reports_the_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_notes(monkeypatch, ENV_NOTE)

    resolved = await sources.resolve("note", NOTE_ID, user_id=USER_ID)
    assert resolved is not None

    for name, value in FIXTURE_VALUES.items():
        assert value not in resolved.text, f"{name} value survived into resolved text"

    # The names stay — the text still documents WHAT the note held.
    assert "ADMIN_API_TOKEN=<redacted:ADMIN_API_TOKEN>" in resolved.text
    # Non-secrets are untouched.
    assert "PORT=8000" in resolved.text
    assert "APP_NAME=aidream" in resolved.text

    meta = resolved.metadata
    assert meta.get("secrets_redacted") == 6
    names = meta.get("secret_names")
    assert isinstance(names, list)
    assert "ADMIN_API_TOKEN" in names
    # The census never carries a value.
    for value in FIXTURE_VALUES.values():
        assert value not in str(meta)


@pytest.mark.asyncio
async def test_chunks_of_an_env_note_contain_no_secret_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End of the road: what would actually be written to rag.kg_chunks."""
    _install_fake_notes(monkeypatch, ENV_NOTE)

    resolved = await sources.resolve("note", NOTE_ID, user_id=USER_ID)
    assert resolved is not None
    chunks = chunking.chunk_text(resolved.text)

    assert chunks, "the note must still be indexed — redaction never blocks ingestion"
    for chunk in chunks:
        for name, value in FIXTURE_VALUES.items():
            assert value not in chunk.content_text, f"{name} value reached a stored chunk"
    assert any("ADMIN_API_TOKEN" in c.content_text for c in chunks)


def test_chunking_guards_text_that_never_passed_through_resolve() -> None:
    """The PDF / image / workflow callers build their own text. Guard holds."""
    chunks = chunking.chunk_text(ENV_NOTE)
    assert chunks
    for chunk in chunks:
        for value in FIXTURE_VALUES.values():
            assert value not in chunk.content_text


def test_code_chunking_guards_too() -> None:
    code = f'ANTHROPIC_KEY = "{FIXTURE_VALUES["ANTHROPIC_KEY"]}"\n\n\ndef main():\n    pass\n'
    chunks = chunking.chunk_code(code, language="python")
    assert chunks
    for chunk in chunks:
        assert FIXTURE_VALUES["ANTHROPIC_KEY"] not in chunk.content_text


def test_ordinary_note_is_not_touched(monkeypatch: pytest.MonkeyPatch) -> None:
    """A detector that mangles normal notes gets turned off — and then it
    protects nothing. Prose, SHAs and UUIDs must survive byte-identical."""
    prose = (
        "The key insight from the meeting: the primary key is id, and the "
        "foreign key is organization_id.\n"
        "commit 8f14e45fceea167a5a36dedd4bea2543b4f4a2b8 fixed it.\n"
        "note id 1558abb7-7d1f-42dd-a297-ebe8a805e60d\n"
        "API_BASE_URL=https://server.app.matrxserver.com/api/v1\n"
    )
    chunks = chunking.chunk_text(prose)
    joined = "\n".join(c.content_text for c in chunks)
    assert "<redacted" not in joined
    assert "8f14e45fceea167a5a36dedd4bea2543b4f4a2b8" in joined
    assert "1558abb7-7d1f-42dd-a297-ebe8a805e60d" in joined
    assert "https://server.app.matrxserver.com/api/v1" in joined
