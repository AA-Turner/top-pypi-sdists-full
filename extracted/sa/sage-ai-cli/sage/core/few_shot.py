"""Persistent few-shot store: remember what the user accepts vs. rejects.

Sage already has session_state.json for short-lived state. This module adds
a longer-lived store at ~/.sage/few_shot/<project_hash>.json that captures:

  - user_accepted: prompts where Sage's output was kept (good demonstration)
  - user_rejected: prompts where the user said no / undid / asked again

At prompt time we surface a small handful of accepted patterns as few-shot
examples and a brief "do not do this" digest of recent rejections. For
small models, demonstration beats instruction by a wide margin.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

__all__ = ["FewShotExample", "FewShotStore"]

_MAX_EXAMPLES = 24    # Hard cap so the file doesn't grow without bound
_MAX_PROMPT_CHARS = 800
_MAX_RESPONSE_CHARS = 1600


@dataclass
class FewShotExample:
    timestamp: float
    prompt: str
    response: str
    accepted: bool
    tags: list[str] = field(default_factory=list)


def _project_hash(cwd: Path) -> str:
    return hashlib.sha1(str(cwd.resolve()).encode("utf-8")).hexdigest()[:12]


def _truncate(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    return s[: n - 3] + "..."


class FewShotStore:
    """Per-project accepted/rejected examples persisted to disk."""

    def __init__(self, cwd: Path):
        self.cwd = cwd.resolve()
        self.dir = Path.home() / ".sage" / "few_shot"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f"{_project_hash(self.cwd)}.json"
        self._examples: list[FewShotExample] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text("utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        for d in data.get("examples", []):
            try:
                self._examples.append(FewShotExample(**d))
            except (TypeError, KeyError):
                continue

    def _save(self) -> None:
        # Trim to keep file small; oldest first.
        if len(self._examples) > _MAX_EXAMPLES:
            self._examples = self._examples[-_MAX_EXAMPLES:]
        try:
            self.path.write_text(json.dumps(
                {"examples": [asdict(e) for e in self._examples]},
                indent=2,
            ), "utf-8")
        except OSError:
            pass

    # ── Recording ───────────────────────────────────────────────

    def record_accept(self, prompt: str, response: str, tags: list[str] | None = None) -> None:
        self._examples.append(FewShotExample(
            timestamp=time.time(),
            prompt=_truncate(prompt, _MAX_PROMPT_CHARS),
            response=_truncate(response, _MAX_RESPONSE_CHARS),
            accepted=True,
            tags=list(tags or []),
        ))
        self._save()

    def record_reject(self, prompt: str, response: str, reason: str = "") -> None:
        tags = ["rejected"]
        if reason:
            tags.append(f"reason:{_truncate(reason, 80)}")
        self._examples.append(FewShotExample(
            timestamp=time.time(),
            prompt=_truncate(prompt, _MAX_PROMPT_CHARS),
            response=_truncate(response, _MAX_RESPONSE_CHARS),
            accepted=False,
            tags=tags,
        ))
        self._save()

    # ── Retrieval ───────────────────────────────────────────────

    def accepted(self, limit: int = 3) -> list[FewShotExample]:
        accepted = [e for e in self._examples if e.accepted]
        return accepted[-limit:]

    def rejected(self, limit: int = 3) -> list[FewShotExample]:
        rejected = [e for e in self._examples if not e.accepted]
        return rejected[-limit:]

    def format_for_prompt(self, accept_n: int = 3, reject_n: int = 3) -> str:
        """Render a digest of accepted/rejected examples as a prompt section."""
        accepted = self.accepted(accept_n)
        rejected = self.rejected(reject_n)
        if not (accepted or rejected):
            return ""
        parts: list[str] = ["", "## LEARNED PREFERENCES (this project)"]
        if accepted:
            parts.append("\n### Past responses the user kept (do more of this)")
            for ex in accepted:
                parts.append(f"\nUser: {ex.prompt}\nAssistant:\n{ex.response}\n")
        if rejected:
            parts.append("\n### Past responses the user rejected (avoid these patterns)")
            for ex in rejected:
                reason = next((t.split(":", 1)[1] for t in ex.tags if t.startswith("reason:")), "")
                tail = f" — reason: {reason}" if reason else ""
                parts.append(f"\nUser: {ex.prompt}{tail}\n[rejected response truncated]\n")
        return "\n".join(parts) + "\n"
