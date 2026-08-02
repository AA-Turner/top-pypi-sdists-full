"""Single GitLab *issue notes* REST client, shared by the ``internal`` webhook flow.

Replaces the two hand-rolled ``urllib`` clients that lived in
``internal/parse_stream/parser.py`` and ``internal/webhook_reply.py``. It keeps
the retry-on-5xx/429 behaviour those flows relied on, takes an already-resolved
token (see :func:`..runner.gitlab_token`), and never raises on a network error —
every method degrades to ``None``/``False`` so a failed note update can never
break the surrounding pipeline.
"""

import json
import sys
import time
import urllib.error
import urllib.request
from typing import Any

GITLAB_API = "https://gitlab.com/api/v4"
DEFAULT_MAX_RETRIES = 3
DEFAULT_RETRY_DELAY = 2  # seconds


class GitLabNotesClient:
    """Create/update/read notes on a single issue, resolving the discussion thread."""

    def __init__(
        self,
        project_id: str,
        issue_iid: str,
        token: str,
        *,
        api_base: str = GITLAB_API,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay: int = DEFAULT_RETRY_DELAY,
    ) -> None:
        self.project_id = project_id
        self.issue_iid = issue_iid
        self.token = token
        self.api_base = api_base
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def _issue_base(self) -> str:
        return f"{self.api_base}/projects/{self.project_id}/issues/{self.issue_iid}"

    def _request(self, req: urllib.request.Request, retries: int | None = None) -> bytes | None:
        """Execute a request with retries on 5xx/429 and transient network errors."""
        attempts = self.max_retries if retries is None else retries
        for attempt in range(attempts):
            try:
                with urllib.request.urlopen(req) as resp:
                    return bytes(resp.read())
            except urllib.error.HTTPError as exc:
                if exc.code < 500 and exc.code != 429:
                    print(f"GitLab API error (HTTP {exc.code}), not retrying", file=sys.stderr)
                    return None
                if attempt < attempts - 1:
                    delay = self.retry_delay * (attempt + 1)
                    print(f"GitLab API error (HTTP {exc.code}), retrying in {delay}s...", file=sys.stderr)
                    time.sleep(delay)
                else:
                    print(f"GitLab API error (HTTP {exc.code}), all retries exhausted", file=sys.stderr)
            except (urllib.error.URLError, OSError) as exc:
                if attempt < attempts - 1:
                    delay = self.retry_delay * (attempt + 1)
                    print(f"GitLab API network error ({exc}), retrying in {delay}s...", file=sys.stderr)
                    time.sleep(delay)
                else:
                    print(f"GitLab API network error ({exc}), all retries exhausted", file=sys.stderr)
        return None

    def get_note(self, note_id: str, *, retries: int | None = None) -> dict[str, Any] | None:
        """Return a note's JSON, or ``None`` on failure."""
        req = urllib.request.Request(f"{self._issue_base()}/notes/{note_id}", headers={"PRIVATE-TOKEN": self.token})
        raw = self._request(req, retries=retries)
        if not raw:
            return None
        try:
            data: dict[str, Any] = json.loads(raw)
            return data
        except json.JSONDecodeError:
            return None

    def create_note(self, body: str, *, discussion_id: str = "") -> str:
        """Create a note (as a reply in ``discussion_id`` when set); return its id or ``""``."""
        if discussion_id:
            url = f"{self._issue_base()}/discussions/{discussion_id}/notes"
        else:
            url = f"{self._issue_base()}/notes"
        data = json.dumps({"body": body}).encode()
        req = urllib.request.Request(
            url,
            data=data,
            headers={"PRIVATE-TOKEN": self.token, "Content-Type": "application/json"},
        )
        raw = self._request(req)
        if raw:
            return str(json.loads(raw).get("id", ""))
        return ""

    def update_note(self, note_id: str, body: str) -> bool:
        """Update an existing note. Returns ``True`` on success."""
        data = json.dumps({"body": body}).encode()
        req = urllib.request.Request(
            f"{self._issue_base()}/notes/{note_id}",
            data=data,
            headers={"PRIVATE-TOKEN": self.token, "Content-Type": "application/json"},
            method="PUT",
        )
        return self._request(req) is not None

    def resolve_discussion_id(self, reply_note_id: str, *, retries: int = 1) -> str:
        """Return the ``discussion_id`` of ``reply_note_id`` (the note being replied to)."""
        note = self.get_note(reply_note_id, retries=retries)
        if note:
            return str(note.get("discussion_id", "") or "")
        return ""
