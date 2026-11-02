"""Tests for _apply_incremental_file_changes."""

from types import SimpleNamespace

from agentic_devtools.cli.azure_devops.review_scaffold_incremental import _apply_incremental_file_changes
from agentic_devtools.cli.azure_devops.review_state import (
    FileEntry,
    FolderGroup,
    OverallSummary,
    ReviewState,
    ReviewStatus,
)


def test_applies_new_modified_deleted_and_folder_changes():
    state = ReviewState(
        prId=1,
        repoId="repo",
        repoName="repo",
        project="project",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00+00:00",
        overallSummary=OverallSummary(threadId=1, commentId=1),
        folders={"removed": FolderGroup(files=["/removed/a.ts"])},
        files={
            "/src/modified.ts": FileEntry(
                threadId=1,
                commentId=1,
                folder="src",
                fileName="modified.ts",
                suggestions=[],
            ),
            "/gone/deleted.ts": FileEntry(threadId=2, commentId=2, folder="gone", fileName="deleted.ts"),
        },
    )
    changes = SimpleNamespace(
        new_files=["/src/new.ts"],
        modified_files=["/src/modified.ts"],
        deleted_files=["/gone/deleted.ts"],
        unchanged_files=[],
    )

    _apply_incremental_file_changes(state, changes)

    assert state.files["/src/new.ts"].status == ReviewStatus.UNREVIEWED.value
    assert state.files["/src/modified.ts"].status == ReviewStatus.UNREVIEWED.value
    assert state.files["/gone/deleted.ts"].summary == "File removed"
    assert "removed" in state.folders
