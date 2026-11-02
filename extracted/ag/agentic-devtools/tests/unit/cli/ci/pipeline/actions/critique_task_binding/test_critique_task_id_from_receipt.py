import pytest

from agentic_devtools.cli.ci.pipeline.actions.critique_task_binding import critique_task_id_from_receipt


@pytest.mark.parametrize(
    ("receipt", "expected"),
    [
        ("task:owner/repo:77", "77"),
        ("task:owner/repo:task_123-abc", "task_123-abc"),
        (77, None),
        ("task:other/repo:77", None),
        ("task:owner/repo:", None),
        ("task:owner/repo:bad/task", None),
    ],
)
def test_critique_task_id_from_receipt_accepts_only_valid_task_ids(receipt, expected) -> None:
    assert critique_task_id_from_receipt(receipt, "owner/repo") == expected
