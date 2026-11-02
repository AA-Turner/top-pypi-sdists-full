from unittest.mock import MagicMock

import pytest

from agentic_devtools.cli.ci.critique_adjudicator import build_critique_task_comment, build_critique_task_id_marker
from agentic_devtools.cli.ci.pipeline.actions.critique_task_binding import bind_critique_task_id
from agentic_devtools.cli.ci.pipeline.snapshot_models import PRStateSnapshot


def test_bind_critique_task_id_verifies_persisted_marker() -> None:
    snapshot = PRStateSnapshot(pr_number=42, head_sha="head")
    marker_body = build_critique_task_comment(42, "head", 100, 1) + "\n" + build_critique_task_id_marker("task-123")
    provider = MagicMock()
    provider.find_comment.return_value = (77, marker_body)

    bind_critique_task_id(provider, snapshot, (77, 100, 1), "task-123")

    provider.update_comment_as_pr_token.assert_called_once_with(77, marker_body)
    provider.find_comment.assert_called_once_with(42, marker_body.splitlines()[0])


@pytest.mark.parametrize(
    ("marker", "expected_error"),
    [(None, "marker is required"), ((77, 100, 1), "could not be verified")],
)
def test_bind_critique_task_id_requires_verified_marker(marker, expected_error) -> None:
    provider = MagicMock()
    provider.find_comment.return_value = None

    with pytest.raises(ValueError if marker is None else RuntimeError, match=expected_error):
        bind_critique_task_id(provider, PRStateSnapshot(pr_number=42, head_sha="head"), marker, "task-123")
