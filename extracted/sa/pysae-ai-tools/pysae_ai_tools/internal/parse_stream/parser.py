"""Parse Claude Code stream-json from stdin into readable CI logs.

Usage:
    claude -p --output-format stream-json --verbose "..." | pysae-ai-tools internal parse-stream

Side effects:
    Writes session ID to $CLAUDE_SESSION_FILE (default: <tmpdir>/claude-session-id).
    Writes run stats to $CLAUDE_STATS_FILE (default: <tmpdir>/claude-stats.json).
    When $CLAUDE_TURNS_DIR is set, writes one markdown file per turn (turn-001.md, turn-002.md, …).
"""

import json
import os
import sys
import time
from typing import Any

from ...common.glab.notes import GitLabNotesClient
from ...common.glab.runner import gitlab_token
from ...common.paths import temp_path
from .formatter import StreamFormatter
from .gitlab_formatter import GitLabFormatter

SESSION_FILE_DEFAULT = str(temp_path("claude-session-id"))
STATS_FILE_DEFAULT = str(temp_path("claude-stats.json"))
RESPONSE_FILE_DEFAULT = ""


class TurnWriter:
    """Writes each turn to a file and posts it as a GitLab discussion reply in real time."""

    def __init__(self, turns_dir: str) -> None:
        self.turns_dir = turns_dir
        self.turn_number = 0
        self.ci_buffer = ""  # CI-formatted output for turn files
        self.gitlab_fmt = GitLabFormatter()
        self.file_enabled = bool(turns_dir)
        if self.file_enabled:
            os.makedirs(turns_dir, exist_ok=True)

        # GitLab discussion reply
        self.project_id = os.environ.get("AI_TOOLS_WEBHOOK_PROJECT_ID", "")
        self.issue_iid = os.environ.get("AI_TOOLS_WEBHOOK_ISSUE_IID", "")
        self.discussion_id = os.environ.get("AI_TOOLS_WEBHOOK_DISCUSSION_ID", "")
        self.reply_note_id = os.environ.get("AI_TOOLS_WEBHOOK_REPLY_NOTE_ID", "")
        self.token = gitlab_token()
        self.gitlab_enabled = bool(self.project_id and self.issue_iid and self.token)
        self.notes = GitLabNotesClient(self.project_id, self.issue_iid, self.token)
        self.gitlab_note_id = self._load_note_id()  # Persisted across resume sessions
        self._last_gitlab_update = 0.0
        self._gitlab_dirty = False  # True when formatter has new content not yet pushed

    @property
    def enabled(self) -> bool:
        return self.file_enabled or self.gitlab_enabled

    def append(self, ci_output: str, event: dict[str, Any]) -> None:
        if not self.enabled:
            return
        if ci_output:
            self.ci_buffer += ci_output
        self.gitlab_fmt.process_event(event)

    MIN_UPDATE_INTERVAL = 3  # seconds between GitLab API calls

    def flush_turn(self, force: bool = False) -> None:
        """Write the current buffer to a turn file and update the GitLab note.

        GitLab updates are throttled to avoid race conditions from rapid
        consecutive API calls. Use force=True for the final flush.
        """
        has_ci = self.ci_buffer.strip()
        has_gitlab = self.gitlab_fmt.has_content()
        if not has_ci and not has_gitlab:
            return
        self.turn_number += 1

        if self.file_enabled and has_ci:
            path = os.path.join(self.turns_dir, f"turn-{self.turn_number:03d}.md")
            with open(path, "w") as f:
                f.write(self.ci_buffer)

        if self.gitlab_enabled and has_gitlab:
            self._gitlab_dirty = True
            now = time.monotonic()
            if force or (now - self._last_gitlab_update) >= self.MIN_UPDATE_INTERVAL:
                self._update_or_create_gitlab_note()
                self._last_gitlab_update = now
                self._gitlab_dirty = False

        self.ci_buffer = ""

    def flush_gitlab(self) -> None:
        """Force a final GitLab update if there's pending content."""
        if self._gitlab_dirty and self.gitlab_enabled and self.gitlab_fmt.has_content():
            self._update_or_create_gitlab_note()
            self._gitlab_dirty = False

    def finalize(self) -> None:
        """Mark the session as finished and collapse the activity section."""
        self.gitlab_fmt.finished = True
        if self.gitlab_enabled and self.gitlab_note_id and self.gitlab_fmt.has_content():
            self._update_or_create_gitlab_note()

    def post_error(self, result_event: dict[str, Any]) -> None:
        """Post an error message to the GitLab discussion or as a standalone note."""
        if not self.gitlab_enabled:
            return
        cost = round(float(result_event.get("total_cost_usd") or 0), 4)
        duration_ms = result_event.get("duration_ms") or 0
        duration_s = float(str(duration_ms)) / 1000
        job_url = os.environ.get("CI_JOB_URL", "")
        body = ":x: **Session failed**\n\n"
        body += f"Cost: ${cost} · Duration: {int(duration_s)}s · Turns: {result_event.get('num_turns', 0)}\n"
        if job_url:
            body += f"\n[Job CI]({job_url})"
        if self.gitlab_note_id:
            self.gitlab_fmt.text_parts.append(body)
            self._update_gitlab_note(self.gitlab_fmt.compose())
        else:
            self._post_standalone_note(body)

    def _update_or_create_gitlab_note(self) -> None:
        """Create or update a single GitLab note with composed content."""
        body = self.gitlab_fmt.compose()
        if not body:
            return
        if self.gitlab_note_id:
            self._update_gitlab_note(body)
        else:
            self.gitlab_note_id = self._create_gitlab_note(body)
            self._save_note_id()

    def _update_gitlab_note(self, body: str) -> None:
        """Update an existing GitLab note."""
        self.notes.update_note(self.gitlab_note_id, body)

    def _create_gitlab_note(self, body: str) -> str:
        """Create a new GitLab note and return its ID."""
        self._resolve_discussion_id()
        return self.notes.create_note(body, discussion_id=self.discussion_id)

    GITLAB_NOTE_ID_FILE = str(temp_path("claude-gitlab-note-id"))

    def _load_note_id(self) -> str:
        """Load persisted note ID from previous session (resume support)."""
        try:
            with open(self.GITLAB_NOTE_ID_FILE) as f:
                note_id = f.read().strip()
                if note_id:
                    self._load_previous_note(note_id)
                    return note_id
        except FileNotFoundError:
            pass
        return ""

    def _save_note_id(self) -> None:
        """Persist note ID for resume sessions."""
        if self.gitlab_note_id:
            with open(self.GITLAB_NOTE_ID_FILE, "w") as f:
                f.write(self.gitlab_note_id)

    def _load_previous_note(self, note_id: str) -> None:
        """Load previous session's note body and split into text + activity.

        The previous body is already composed (text + collapsed <details>).
        We parse it back into text_parts and activity_parts so compose()
        can merge new content into the existing structure.
        """
        note = self.notes.get_note(note_id, retries=1)
        if not note:
            return
        body = (note.get("body") or "").strip()
        if not body:
            return

        # Split on the <details> tag to separate text from activity
        details_marker = "<details"
        idx = body.find(details_marker)
        if idx >= 0:
            text_part = body[:idx].strip()
            activity_part = body[idx:]
            # Extract inner content from <details>...\n\nCONTENT\n</details>
            inner_start = activity_part.find("\n\n")
            inner_end = activity_part.rfind("\n</details>")
            if inner_start >= 0 and inner_end > inner_start:
                inner = activity_part[inner_start + 2 : inner_end].strip()
                if inner:
                    # Re-split individual activity entries (separated by double newlines)
                    self.gitlab_fmt.activity_parts.extend(inner.split("\n\n"))
            if text_part:
                self.gitlab_fmt.text_parts.insert(0, text_part)
        else:
            # No <details> block — entire body is text
            self.gitlab_fmt.text_parts.insert(0, body)

    def _resolve_discussion_id(self) -> None:
        """Resolve discussion_id from the reply note if not already set."""
        if self.discussion_id or not self.reply_note_id:
            return
        discussion_id = self.notes.resolve_discussion_id(self.reply_note_id)
        if discussion_id:
            self.discussion_id = discussion_id

    def _post_standalone_note(self, body: str) -> None:
        """Create a standalone note on the issue."""
        if not body:
            return
        self.notes.create_note(body)


def main() -> None:
    """Parse Claude Code stream-json output into human-readable text."""
    skip_text = "include-partial-messages" in (
        os.environ.get("DEFAULT_CLAUDE_OPTS", "") + " " + os.environ.get("CLAUDE_OPTS", "")
    )
    fmt = StreamFormatter(skip_assistant_text=skip_text)
    session_file = os.environ.get("CLAUDE_SESSION_FILE", SESSION_FILE_DEFAULT)
    stats_file = os.environ.get("CLAUDE_STATS_FILE", STATS_FILE_DEFAULT)
    turns = TurnWriter(os.environ.get("CLAUDE_TURNS_DIR", ""))

    result_event: dict[str, Any] = {}

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        event_type = event.get("type")

        # Capture session ID from init event
        if event_type == "system" and event.get("subtype") == "init" and event.get("session_id"):
            with open(session_file, "w") as f:
                f.write(event["session_id"])

        # Flush previous turn when a new assistant message starts
        if event_type == "assistant":
            turns.flush_turn()

        if event_type == "result":
            result_event = event

        output = fmt.format_event(event)
        if output:
            sys.stdout.write(output)
            sys.stdout.flush()
        turns.append(output, event)

    # Flush last turn, push pending content, and collapse activity section
    turns.flush_turn(force=True)
    turns.flush_gitlab()
    turns.finalize()

    # Write stats for claude-ci.sh resume logic
    with open(stats_file, "w") as f:
        json.dump({"tool_call_count": fmt.tool_call_count, "num_turns": fmt.num_turns, "is_error": fmt.is_error}, f)

    # Write clean response text for webhook reply
    response_file = os.environ.get("CLAUDE_RESPONSE_FILE", RESPONSE_FILE_DEFAULT)
    if response_file:
        with open(response_file, "w") as f:
            f.write("".join(fmt.response_chunks))

    if fmt.is_error:
        turns.post_error(result_event)
        sys.exit(1)


if __name__ == "__main__":
    main()
