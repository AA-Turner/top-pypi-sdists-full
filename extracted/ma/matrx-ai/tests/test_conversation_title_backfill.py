from datetime import UTC, datetime

from matrx_ai.db.conversation_gate import compact_step_label
from matrx_ai.db.conversation_title_backfill import (
    ConversationBackfillRow,
    assign_media_indices,
    build_backfill_plans,
    build_compact_title_plans,
    is_generic_auto_title,
    resolve_backfill_step_label,
    should_backfill_row,
)


def _row(**kwargs: object) -> ConversationBackfillRow:
    base = {
        "id": "00000000-0000-4000-8000-000000000001",
        "title": "AUTO: Podcast",
        "source_feature": "podcasts",
        "parent_conversation_id": "00000000-0000-4000-8000-000000000099",
        "initial_agent_id": None,
        "initial_agent_version_id": None,
        "last_model_id": "model-image",
        "metadata": {},
        "created_at": datetime(2026, 6, 17, 16, 0, tzinfo=UTC),
        "user_id": "user-1",
    }
    base.update(kwargs)
    return ConversationBackfillRow(**base)  # type: ignore[arg-type]


def test_is_generic_auto_title() -> None:
    assert is_generic_auto_title("AUTO: Podcast", "podcasts")
    assert is_generic_auto_title("Auto: Podcast", "podcasts")
    assert not is_generic_auto_title("Auto: Podcast Script", "podcasts")
    assert not is_generic_auto_title("Voice Database Schema Design", "podcasts")


def test_should_backfill_child_or_internal() -> None:
    assert should_backfill_row(_row())
    assert not should_backfill_row(
        _row(title="Auto: Podcast Script", parent_conversation_id=None, source_feature="chat")
    )


def test_resolve_podcast_image_with_index() -> None:
    label = resolve_backfill_step_label(
        source_feature="podcasts",
        agent_name="podcast_image_v1",
        media_kind="image",
        media_index=2,
        metadata={},
    )
    assert label == "Podcast Image 2"


def test_assign_media_indices_within_parent() -> None:
    rows = [
        _row(id="a", created_at=datetime(2026, 6, 17, 16, 0, tzinfo=UTC)),
        _row(id="b", created_at=datetime(2026, 6, 17, 16, 1, tzinfo=UTC)),
    ]
    indices = assign_media_indices(rows, {"model-image": "image"})
    assert indices == {"a": 1, "b": 2}


def test_build_backfill_plans_uses_agent_name_for_text_steps() -> None:
    plans = build_backfill_plans(
        [
            _row(
                title="AUTO: Web Research",
                source_feature="web-research",
                last_model_id="model-text",
                initial_agent_id="agent-1",
            )
        ],
        agent_name_by_id={"agent-1": "Page Summary Agent"},
        version_agent_name_by_id={},
        model_kind_by_id={"model-text": None},
    )
    assert len(plans) == 1
    assert plans[0].new_title == "Auto: Page Summary Agent"


def test_build_compact_title_plans() -> None:
    plans = build_compact_title_plans(
        [
            _row(
                title="AUTO: Generate Podcast Image 3",
                metadata={"conversation_step_label": "Generate Podcast Image 3"},
            )
        ]
    )
    assert len(plans) == 1
    assert plans[0].new_title == "Auto: Podcast Image 3"
    assert compact_step_label(plans[0].step_label) == "Podcast Image 3"
