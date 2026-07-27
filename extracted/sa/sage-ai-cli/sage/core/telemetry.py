"""T10 — Telemetry logging.

Append-only JSONL logger for every (prompt, model, output, validator_signal,
success) tuple. Two purposes:
  1. Per-session summarization for "what's failing on small models"
  2. Future training data for distillation (compile_into_corpus pulls from
     the distill log already; this is the broader telemetry that captures
     even non-tool-call turns)

Privacy: secrets are redacted before write (API keys, passwords, JWTs).
Storage: ~/.sage/telemetry/<session_id>.jsonl, append-only.
"""

from __future__ import annotations

import json
import re
import time
import uuid
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

__all__ = ["TelemetryLogger", "summarize", "redact_secrets"]


_SECRET_PATTERNS = (
    re.compile(r"\b(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|GEMINI_API_KEY|"
               r"GITHUB_TOKEN|AWS_(?:ACCESS|SECRET)_KEY[A-Z_]*|"
               r"GOOGLE_API_KEY|GROQ_API_KEY|BRAVE_API_KEY|HF_TOKEN)\s*=\s*"
               r"\S+", re.IGNORECASE),
    re.compile(r"\bsk-[a-zA-Z0-9]{16,}\b"),                # OpenAI / Anthropic
    re.compile(r"\bgh[ps]_[A-Za-z0-9]{36,}\b"),            # GitHub PAT
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),                   # AWS access key
    re.compile(r"\beyJ[\w-]+\.[\w-]+\.[\w-]+\b"),          # JWT
    re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b"),       # Slack
)


def redact_secrets(text: str) -> str:
    out = text
    for pattern in _SECRET_PATTERNS:
        out = pattern.sub("***REDACTED***", out)
    return out


@dataclass
class TelemetryLogger:
    session_id: str = ""
    root: Path | None = None

    def __post_init__(self) -> None:
        if not self.session_id:
            self.session_id = uuid.uuid4().hex[:12]
        if self.root is None:
            self.root = Path.home() / ".sage" / "telemetry"
        self.root.mkdir(parents=True, exist_ok=True)

    @property
    def path(self) -> Path:
        return self.root / f"{self.session_id}.jsonl"

    def log_turn(
        self, *,
        prompt: str,
        model: str,
        output: str,
        validator_signal: str | None,
        success: bool,
        meta: dict | None = None,
    ) -> None:
        def _clean(val: str) -> str:
            if not val:
                return ""
            val = re.sub(r'\x1b\[[0-9;]*[mGKHFABCDEJst]', '', val)
            val = re.sub(r'\x1b\].*?\x07', '', val)
            return val.replace('\x1b', '')

        cleaned_prompt = _clean(prompt or "")
        cleaned_output = _clean(output or "")

        record = {
            "ts": time.time(),
            "session": self.session_id,
            "model": model,
            "prompt": redact_secrets(cleaned_prompt)[:4000],
            "output": redact_secrets(cleaned_output)[:8000],
            "validator_signal": validator_signal,
            "success": bool(success),
            "meta": meta or {},
        }
        try:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")
        except OSError:
            pass

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        out: list[dict] = []
        for line in self.path.read_text("utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return out


def summarize(*, session_id: str, root: Path | None = None) -> dict:
    """Roll up a session's telemetry into a small dict."""
    base = root or (Path.home() / ".sage" / "telemetry")
    path = base / f"{session_id}.jsonl"
    if not path.exists():
        return {"total": 0, "successful": 0, "failed": 0, "signals": {}}
    total = 0
    successful = 0
    signals: Counter = Counter()
    for line in path.read_text("utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        total += 1
        if row.get("success"):
            successful += 1
        if row.get("validator_signal"):
            signals[row["validator_signal"]] += 1
    return {
        "total": total,
        "successful": successful,
        "failed": total - successful,
        "signals": dict(signals),
    }
