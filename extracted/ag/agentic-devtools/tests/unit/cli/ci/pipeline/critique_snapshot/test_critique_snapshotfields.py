from agentic_devtools.cli.ci.pipeline.critique_snapshot import CritiqueSnapshotFields


def test_as_kwargs_returns_all_snapshot_fields() -> None:
    fields = CritiqueSnapshotFields(critique_headline_classification="critique")

    assert fields.as_kwargs()["critique_task_state_available"] is True
    assert fields.as_kwargs()["critique_headline_classification"] == "critique"
    assert fields.as_kwargs()["critique_adjudicated_review_id"] is None
