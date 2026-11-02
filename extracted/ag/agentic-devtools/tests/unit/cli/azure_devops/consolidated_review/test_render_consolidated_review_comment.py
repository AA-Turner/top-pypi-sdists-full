"""Tests for render_consolidated_review_comment and render_commit_review_comments."""

from agentic_devtools.cli.azure_devops.consolidated_review import (
    HARD_CAP_CHARS,
    SMART_CUTOFF_CHARS,
    _render_activity_log_block,
    _render_narrative_section,
    _render_previous_reviews_index,
    _short_hash,
    _split_into_comments,
    is_review_complete,
    render_commit_review_comments,
    render_consolidated_review_comment,
)
from agentic_devtools.cli.azure_devops.review_state import (
    CommitComment,
    FileEntry,
    FolderGroup,
    ModelCommentRef,
    OverallSummary,
    ReviewSession,
    ReviewState,
    ReviewStatus,
    SkippedFile,
    SuggestionEntry,
)

_BASE_URL = "https://dev.azure.com/org/proj/_git/repo/pullRequest/42"


def _suggestion(
    thread_id: int = 100,
    line: int = 10,
    end_line: int = 10,
    severity: str = "high",
    out_of_scope: bool = False,
    content: str = "Fix this issue",
) -> SuggestionEntry:
    return SuggestionEntry(
        threadId=thread_id,
        commentId=1,
        line=line,
        endLine=end_line,
        severity=severity,
        outOfScope=out_of_scope,
        linkText=(f"line {line}" if line == end_line else f"lines {line} - {end_line}"),
        content=content,
    )


def _file(
    name: str,
    folder: str = "src",
    status: str = ReviewStatus.APPROVED.value,
    summary: str | None = "Looks good.",
    suggestions=None,
    thread_id: int = 10,
) -> FileEntry:
    return FileEntry(
        threadId=thread_id,
        commentId=1,
        folder=folder,
        fileName=name,
        status=status,
        summary=summary,
        suggestions=suggestions or [],
    )


def _state(
    files=None,
    sessions=None,
    commit_hash: str = "4a8685bda246f3bf826efabaf990fe9c3d1da125",
    model_id: str | None = "claude-opus-4.6",
    narrative: str | None = "Overall this PR looks reasonable.",
    rebase_conflicts: bool = False,
    skipped=None,
    commit_comments=None,
) -> ReviewState:
    files = files or {}
    folders: dict[str, FolderGroup] = {}
    for path, fe in files.items():
        folders.setdefault(fe.folder, FolderGroup(files=[])).files.append(path)
    return ReviewState(
        prId=42,
        repoId="repo-guid",
        repoName="repo",
        project="proj",
        organization="https://dev.azure.com/org",
        latestIterationId=1,
        scaffoldedUtc="2026-01-01T00:00:00Z",
        overallSummary=OverallSummary(threadId=1, commentId=1, narrativeSummary=narrative),
        folders=folders,
        files=files,
        commitHash=commit_hash,
        modelId=model_id,
        sessions=sessions or [],
        rebaseConflicts=rebase_conflicts,
        skippedFiles=skipped or [],
        commitComments=commit_comments or {},
    )


class TestIsReviewComplete:
    """Tests for the completion-detection helper."""

    def test_no_files_is_incomplete(self):
        assert is_review_complete(_state(files={})) is False

    def test_unreviewed_file_is_incomplete(self):
        state = _state(files={"/src/a.py": _file("a.py", status=ReviewStatus.UNREVIEWED.value)})
        assert is_review_complete(state) is False

    def test_in_progress_file_is_incomplete(self):
        state = _state(files={"/src/a.py": _file("a.py", status=ReviewStatus.IN_PROGRESS.value)})
        assert is_review_complete(state) is False

    def test_all_terminal_is_complete(self):
        state = _state(
            files={
                "/src/a.py": _file("a.py", status=ReviewStatus.APPROVED.value),
                "/src/b.py": _file("b.py", status=ReviewStatus.NEEDS_WORK.value),
            }
        )
        assert is_review_complete(state) is True


class TestLightweightInProgress:
    """While in progress, only a lightweight status headline is rendered."""

    def test_in_progress_returns_single_lightweight_comment(self):
        state = _state(
            files={
                "/src/a.py": _file("a.py", status=ReviewStatus.APPROVED.value),
                "/src/b.py": _file("b.py", status=ReviewStatus.UNREVIEWED.value),
            }
        )
        comments = render_commit_review_comments(state, _BASE_URL)
        assert len(comments) == 1
        body = comments[0]
        assert body.startswith("<!-- agdt-review:v2 type:consolidated")
        assert "Being reviewed by" in body
        assert "1/2 reviewed" in body
        # No heavy content sections while in progress.
        assert "Review Narrative" not in body
        assert "<details" not in body

    def test_complete_uses_reviewed_verb_and_full_content(self):
        state = _state(files={"/src/a.py": _file("a.py", status=ReviewStatus.APPROVED.value)})
        body = render_consolidated_review_comment(state, _BASE_URL)
        assert "Reviewed by" in body
        assert "Being reviewed by" not in body
        assert "Review Narrative" in body
        assert "1/1 reviewed" in body

    def test_force_in_progress_keeps_lightweight_when_complete(self):
        state = _state(files={"/src/a.py": _file("a.py", status=ReviewStatus.APPROVED.value)})
        comments = render_commit_review_comments(state, _BASE_URL, force_in_progress=True)
        assert len(comments) == 1
        body = comments[0]
        assert "Being reviewed by" in body
        assert "Review Narrative" not in body
        assert "<details" not in body
        assert "1/1 reviewed" in body


class TestFullContentRendering:
    """Once complete, the full content is rendered at full fidelity."""

    def test_headline_and_v2_marker(self):
        state = _state(files={"/src/a.py": _file("a.py")})
        out = render_consolidated_review_comment(state, _BASE_URL)
        assert out.startswith("<!-- agdt-review:v2 type:consolidated")
        assert "commit:4a8685bda246f3bf826efabaf990fe9c3d1da125" in out
        assert "## 🔍 Pull Request Review" in out

    def test_needs_work_section_present(self):
        state = _state(
            files={
                "/src/a.py": _file(
                    "a.py",
                    status=ReviewStatus.NEEDS_WORK.value,
                    suggestions=[_suggestion()],
                )
            }
        )
        out = render_consolidated_review_comment(state, _BASE_URL)
        assert "📝 Needs Work" in out
        assert "Fix this issue" in out

    def test_suggestions_rendered_at_full_fidelity(self):
        big = "x" * 500
        state = _state(
            files={
                "/src/a.py": _file(
                    "a.py",
                    status=ReviewStatus.NEEDS_WORK.value,
                    suggestions=[_suggestion(content=big)],
                )
            }
        )
        out = render_consolidated_review_comment(state, _BASE_URL)
        assert big in out


class TestPreviousReviewsIndex:
    """The previous-reviews index is a hash + link list, no embedded content."""

    def test_empty_when_no_prior_commits(self):
        state = _state(files={"/src/a.py": _file("a.py")})
        assert _render_previous_reviews_index(state, _BASE_URL) == []

    def test_lists_prior_commit_with_link(self):
        prior = CommitComment(
            commitHash="b" * 40,
            threadId=55,
            models=[ModelCommentRef(modelId="gpt-5.5", commentId=77)],
            status=ReviewStatus.APPROVED.value,
            timestamp="2026-01-01T00:00:00Z",
        )
        state = _state(
            files={"/src/a.py": _file("a.py")},
            commit_comments={"b" * 40: prior},
        )
        lines = _render_previous_reviews_index(state, _BASE_URL)
        joined = "\n".join(lines)
        assert "Previous reviews (1)" in joined
        assert "`bbbbbbbb`" in joined
        assert "discussionId=55&commentId=77" in joined
        assert "gpt-5.5" in joined

    def test_lists_prior_commit_without_link(self):
        # A prior commit whose thread/root comment ids are missing renders a
        # bare hash reference (no jump link).
        prior = CommitComment(
            commitHash="b" * 40,
            threadId=0,
            models=[ModelCommentRef(modelId="gpt-5.5", commentId=0)],
            status=ReviewStatus.APPROVED.value,
            timestamp="2026-01-01T00:00:00Z",
        )
        state = _state(
            files={"/src/a.py": _file("a.py")},
            commit_comments={"b" * 40: prior},
        )
        joined = "\n".join(_render_previous_reviews_index(state, _BASE_URL))
        assert "`bbbbbbbb`" in joined
        assert "discussionId=" not in joined

    def test_excludes_current_commit(self):
        current = "4a8685bda246f3bf826efabaf990fe9c3d1da125"
        cc = CommitComment(commitHash=current, threadId=1, models=[ModelCommentRef(modelId="m", commentId=1)])
        state = _state(files={"/src/a.py": _file("a.py")}, commit_comments={current: cc})
        assert _render_previous_reviews_index(state, _BASE_URL) == []

    def test_newest_first_ordering(self):
        older = CommitComment(
            commitHash="a" * 40,
            threadId=1,
            models=[ModelCommentRef(modelId="m1", commentId=1)],
            timestamp="2026-01-01T00:00:00Z",
        )
        newer = CommitComment(
            commitHash="c" * 40,
            threadId=2,
            models=[ModelCommentRef(modelId="m2", commentId=1)],
            timestamp="2026-02-01T00:00:00Z",
        )
        state = _state(
            files={"/src/a.py": _file("a.py")},
            commit_comments={"a" * 40: older, "c" * 40: newer},
        )
        joined = "\n".join(_render_previous_reviews_index(state, _BASE_URL))
        assert joined.index("cccccccc") < joined.index("aaaaaaaa")


class TestSmartCutoffSplitter:
    """The smart-cutoff splitter rolls overflow into continuation comments."""

    def test_small_review_is_single_comment(self):
        state = _state(files={"/src/a.py": _file("a.py")})
        comments = render_commit_review_comments(state, _BASE_URL)
        assert len(comments) == 1

    def test_large_review_splits_into_continuations(self):
        files = {}
        big = "y" * 4000
        for i in range(40):
            files[f"/src/f{i}.py"] = _file(
                f"f{i}.py",
                status=ReviewStatus.NEEDS_WORK.value,
                suggestions=[_suggestion(thread_id=100 + i, content=big)],
            )
        state = _state(files=files)
        comments = render_commit_review_comments(state, _BASE_URL)
        assert len(comments) >= 2
        assert comments[0].startswith("<!-- agdt-review:v2 type:consolidated")
        assert "Review (continued 1)" in comments[1]
        assert sum(len(c) for c in comments) > SMART_CUTOFF_CHARS

    def test_root_stays_near_cutoff(self):
        files = {}
        big = "z" * 4000
        for i in range(40):
            files[f"/src/f{i}.py"] = _file(
                f"f{i}.py",
                status=ReviewStatus.NEEDS_WORK.value,
                suggestions=[_suggestion(thread_id=200 + i, content=big)],
            )
        state = _state(files=files)
        comments = render_commit_review_comments(state, _BASE_URL)
        assert len(comments[0]) < SMART_CUTOFF_CHARS + 12000

    def test_hard_cap_leaves_room_for_comment_overhead(self):
        headline = "h" * 800
        comments = _split_into_comments(headline, ["s" * HARD_CAP_CHARS], 42, "a" * 40)

        assert len(comments) == 1
        assert len(comments[0]) <= 65536


class TestActivityLog:
    """Activity log rendering (capped, newest-first)."""

    def test_empty_when_no_sessions(self):
        assert _render_activity_log_block(_state(files={})) == []

    def test_caps_entries(self):
        sessions = [
            ReviewSession(
                sessionId=f"sess{i:02d}",
                modelId="m",
                startedUtc=f"2026-01-{i + 1:02d}T00:00:00Z",
                status="completed",
                commitHash="a" * 40,
            )
            for i in range(20)
        ]
        lines = _render_activity_log_block(_state(files={}, sessions=sessions))
        joined = "\n".join(lines)
        assert "older session(s)" in joined

    def test_renders_without_omitted_note_when_under_cap(self):
        sessions = [
            ReviewSession(
                sessionId="sess01",
                modelId="m",
                startedUtc="2026-01-01T00:00:00Z",
                status="completed",
                commitHash="a" * 40,
            )
        ]
        lines = _render_activity_log_block(_state(files={}, sessions=sessions))
        joined = "\n".join(lines)
        assert "Activity Log" in joined
        assert "older session(s)" not in joined


class TestRebaseAndSkipped:
    """Overview section surfaces rebase conflicts and skipped files."""

    def test_rebase_conflict_banner(self):
        state = _state(files={"/src/a.py": _file("a.py")}, rebase_conflicts=True)
        out = render_consolidated_review_comment(state, _BASE_URL)
        assert "Rebase Conflicts Detected" in out

    def test_skipped_files_note(self):
        state = _state(
            files={"/src/a.py": _file("a.py")},
            skipped=[SkippedFile(path="/x.py", reason="not_on_branch")],
        )
        out = render_consolidated_review_comment(state, _BASE_URL)
        assert "Skipped files:" in out


class TestShortHash:
    """The short-hash helper truncates or falls back to ``unknown``."""

    def test_truncates_to_eight_chars(self):
        assert _short_hash("0123456789abcdef") == "01234567"

    def test_empty_returns_unknown(self):
        assert _short_hash("") == "unknown"

    def test_none_returns_unknown(self):
        assert _short_hash(None) == "unknown"


class TestNarrativeSection:
    """The narrative section is omitted when no narrative is present."""

    def test_empty_narrative_returns_empty(self):
        state = _state(files={"/src/a.py": _file("a.py")}, narrative=None)
        assert _render_narrative_section(state) == []

    def test_narrative_rendered_when_present(self):
        state = _state(files={"/src/a.py": _file("a.py")}, narrative="A clear narrative.")
        lines = _render_narrative_section(state)
        assert "A clear narrative." in "\n".join(lines)


class TestBuildSectionsOptionalBlocks:
    """A completed render assembles narrative, prior-review and activity blocks."""

    def test_no_narrative_with_prior_commit_and_sessions(self):
        prior = CommitComment(
            commitHash="b" * 40,
            threadId=55,
            models=[ModelCommentRef(modelId="gpt-5.5", commentId=77)],
            status=ReviewStatus.APPROVED.value,
            timestamp="2026-01-01T00:00:00Z",
        )
        sessions = [
            ReviewSession(
                sessionId="sess01",
                modelId="m",
                startedUtc="2026-01-01T00:00:00Z",
                status="completed",
                commitHash="4a8685bda246f3bf826efabaf990fe9c3d1da125",
            )
        ]
        state = _state(
            files={"/src/a.py": _file("a.py")},
            narrative=None,
            commit_comments={"b" * 40: prior},
            sessions=sessions,
        )
        out = render_consolidated_review_comment(state, _BASE_URL)
        assert "Review Narrative" not in out
        assert "Previous reviews (1)" in out
        assert "Activity Log" in out
