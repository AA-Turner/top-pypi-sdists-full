from pathlib import Path

from matrx_ai.db.message_positions import APPEND_MESSAGE_POSITION


def test_append_sentinel_fits_smallint_and_stays_negative() -> None:
    assert -(2**15) <= APPEND_MESSAGE_POSITION < 0


def test_allocator_migration_serializes_and_guards_live_positions() -> None:
    repository = Path(__file__).resolve().parents[3]
    sql = (
        repository / "db/migrations/0174_cx_message_atomic_position_allocator.sql"
    ).read_text()

    assert "new.position = -1" in sql.lower()
    assert "pg_advisory_xact_lock" in sql.lower()
    assert "max(candidate_position)" in sql.lower()
    assert "compaction_archive" in sql.lower()
    assert "original_position" in sql.lower()
    assert "before insert on chat.message" in sql.lower()
    assert "cx_message_conversation_position_live_uidx" in sql
    assert "where deleted_at is null" in sql.lower()
    assert "alter column position type integer" in sql.lower()
