"""Tests for _update_incremental_folder_groups."""

from types import SimpleNamespace

from agentic_devtools.cli.azure_devops.review_scaffold_incremental import _update_incremental_folder_groups
from agentic_devtools.cli.azure_devops.review_state import FolderGroup, OverallSummary, ReviewState


def test_rebuilds_folders_and_keeps_removed_folder_empty():
    state = ReviewState(
        prId=1,
        repoId="repo",
        repoName="repo",
        project="project",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1),
        folders={"old": FolderGroup(files=["/old/a.ts"])},
    )

    _update_incremental_folder_groups(
        state,
        SimpleNamespace(new_files=["/src/a.ts"], modified_files=[], unchanged_files=[], deleted_files=[]),
    )

    assert state.folders["src"].files == ["/src/a.ts"]
    assert state.folders["old"].files == []
