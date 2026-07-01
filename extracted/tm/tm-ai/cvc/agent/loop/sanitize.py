"""Sanitization & scrubbing: JSON repair, surrogates, <think> blocks, secrets."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List


# ─────────────────────────────────────────────────────────
# 2.10 — Tool argument JSON repair
# ─────────────────────────────────────────────────────────

def _strip_code_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```[a-zA-Z]*\n?", "", s)
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()


def _balance_braces(s: str) -> str:
    """Add missing closing braces/brackets to a truncated JSON string."""
    stack: list[str] = []
    in_str = False
    esc = False
    for ch in s:
        if esc:
            esc = False
            continue
        if ch == "\\":
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch in "{[":
            stack.append(ch)
        elif ch in "}]" and stack:
            top = stack[-1]
            if (top == "{" and ch == "}") or (top == "[" and ch == "]"):
                stack.pop()
    if in_str:
        s += '"'
    closers = {"{": "}", "[": "]"}
    for opener in reversed(stack):
        s += closers[opener]
    return s


def _unescape_inner_quotes(s: str) -> str:
    """Try to fix \" inside string values that should be raw quotes."""
    # Simple heuristic: replace doubled escapes around obvious value tokens.
    return s.replace('\\\\"', '\\"')


def repair_tool_call_arguments(raw: Any) -> Dict[str, Any]:
    """Best-effort repair of tool call argument JSON.

    Accepts a string, dict, or anything; returns a dict.
    """
    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        try:
            return dict(raw)  # type: ignore[arg-type]
        except Exception:  # noqa: BLE001
            return {}
    s = _strip_code_fences(raw)
    if not s:
        return {}

    # Pass 1 — direct.
    try:
        v = json.loads(s)
        return v if isinstance(v, dict) else {"value": v}
    except json.JSONDecodeError:
        pass

    # Pass 2 — fix escaped quotes.
    try:
        v = json.loads(_unescape_inner_quotes(s))
        return v if isinstance(v, dict) else {"value": v}
    except json.JSONDecodeError:
        pass

    # Pass 3 — balance braces (truncated JSON).
    try:
        v = json.loads(_balance_braces(s))
        return v if isinstance(v, dict) else {"value": v}
    except json.JSONDecodeError:
        pass

    # Pass 4 — non-strict.
    try:
        v = json.loads(s, strict=False)
        return v if isinstance(v, dict) else {"value": v}
    except json.JSONDecodeError:
        pass

    # Last resort — return raw under a key so caller can decide.
    return {"_raw": s}


# ─────────────────────────────────────────────────────────
# 2.11 — Unicode / surrogate sanitization
# ─────────────────────────────────────────────────────────

_SURROGATE_RE = re.compile(r"[\ud800-\udfff]")


def sanitize_surrogates(text: str, *, replacement: str = "\ufffd") -> str:
    if not isinstance(text, str):
        return text
    if not _SURROGATE_RE.search(text):
        # Fast path; also re-encode to drop lone surrogates the regex can't.
        try:
            text.encode("utf-8")
            return text
        except UnicodeEncodeError:
            pass
    cleaned = _SURROGATE_RE.sub(replacement, text)
    try:
        cleaned.encode("utf-8")
    except UnicodeEncodeError:
        cleaned = cleaned.encode("utf-8", errors="replace").decode("utf-8")
    return cleaned


def strip_non_ascii(text: str) -> str:
    if not isinstance(text, str):
        return text
    return text.encode("ascii", errors="replace").decode("ascii")


def sanitize_messages(messages: List[Dict[str, Any]], *, ascii_only: bool = False) -> List[Dict[str, Any]]:
    fix = strip_non_ascii if ascii_only else sanitize_surrogates
    out: List[Dict[str, Any]] = []
    for m in messages:
        nm = dict(m)
        c = nm.get("content")
        if isinstance(c, str):
            nm["content"] = fix(c)
        elif isinstance(c, list):
            new_blocks = []
            for blk in c:
                if isinstance(blk, dict):
                    nb = dict(blk)
                    if isinstance(nb.get("text"), str):
                        nb["text"] = fix(nb["text"])
                    new_blocks.append(nb)
                elif isinstance(blk, str):
                    new_blocks.append(fix(blk))
                else:
                    new_blocks.append(blk)
            nm["content"] = new_blocks
        # Tool calls
        if isinstance(nm.get("tool_calls"), list):
            new_tcs = []
            for tc in nm["tool_calls"]:
                if isinstance(tc, dict):
                    ntc = dict(tc)
                    fn = ntc.get("function")
                    if isinstance(fn, dict) and isinstance(fn.get("arguments"), str):
                        fn = dict(fn)
                        fn["arguments"] = fix(fn["arguments"])
                        ntc["function"] = fn
                    new_tcs.append(ntc)
                else:
                    new_tcs.append(tc)
            nm["tool_calls"] = new_tcs
        out.append(nm)
    return out


# ─────────────────────────────────────────────────────────
# 2.13 — ThinkScrubber (streaming-safe <think> remover)
# ─────────────────────────────────────────────────────────

class ThinkScrubber:
    """Stateful streaming scrubber for <think>...</think> blocks.

    Feed deltas via ``feed(delta) -> str``. Returns scrubbed text safe to
    forward to UI consumers. Handles tag boundaries split across deltas.
    """

    OPEN = "<think>"
    CLOSE = "</think>"

    def __init__(self) -> None:
        self._buf = ""
        self._in_think = False

    def feed(self, delta: str) -> str:
        if not delta:
            return ""
        self._buf += delta
        out_parts: list[str] = []

        while True:
            if self._in_think:
                idx = self._buf.find(self.CLOSE)
                if idx == -1:
                    # Still inside; drop accumulated thought BUT keep the
                    # last (len(CLOSE)-1) chars in case a close tag is
                    # split across deltas.
                    keep = len(self.CLOSE) - 1
                    if len(self._buf) > keep:
                        self._buf = self._buf[-keep:]
                    break
                # Drop everything up to and including close tag.
                self._buf = self._buf[idx + len(self.CLOSE):]
                self._in_think = False
                continue

            idx = self._buf.find(self.OPEN)
            if idx == -1:
                # Possible partial tag at the end — hold back last (len(OPEN)-1) chars.
                hold = max(0, len(self._buf) - (len(self.OPEN) - 1))
                if hold > 0:
                    out_parts.append(self._buf[:hold])
                    self._buf = self._buf[hold:]
                break

            # Emit pre-tag content, then enter think mode.
            if idx > 0:
                out_parts.append(self._buf[:idx])
            self._buf = self._buf[idx + len(self.OPEN):]
            self._in_think = True

        return "".join(out_parts)

    def flush(self) -> str:
        if self._in_think:
            self._buf = ""
            self._in_think = False
            return ""
        out = self._buf
        self._buf = ""
        return out


def scrub_think_blocks(text: str) -> str:
    s = ThinkScrubber()
    return s.feed(text) + s.flush()


# ─────────────────────────────────────────────────────────
# 2.14 — Secret redaction
# ─────────────────────────────────────────────────────────

_SECRET_PATTERNS = [
    # Common API key prefixes
    re.compile(r"\b(sk-[A-Za-z0-9_\-]{20,})\b"),
    re.compile(r"\b(sk-ant-[A-Za-z0-9_\-]{20,})\b"),
    re.compile(r"\b(xai-[A-Za-z0-9_\-]{20,})\b"),
    re.compile(r"\b(AIza[0-9A-Za-z_\-]{20,})\b"),                 # Google
    re.compile(r"\b(ghp_[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(gho_[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\b(ghu_[A-Za-z0-9]{20,})\b"),
    re.compile(r"\b(nvapi-[A-Za-z0-9_\-]{20,})\b"),
    # Generic bearer tokens
    re.compile(r"(?i)bearer\s+([A-Za-z0-9._\-]{20,})"),
    # AWS-ish
    re.compile(r"\b(AKIA[0-9A-Z]{16})\b"),
    # Generic "token=" / "api_key=" assignments
    re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|secret|password)\s*[=:]\s*['\"]?([A-Za-z0-9_\-\.]{12,})['\"]?"),
]

_SENSITIVE_QUERY_PARAMS = {"api_key", "apikey", "token", "access_token", "key", "auth", "secret"}


def _mask(token: str) -> str:
    if len(token) < 18:
        return "*" * len(token)
    return f"{token[:6]}…{token[-4:]}"


def redact_text(text: str) -> str:
    if not isinstance(text, str) or not text:
        return text
    out = text
    for pat in _SECRET_PATTERNS:
        def _sub(m: re.Match[str]) -> str:
            tok = m.group(1)
            return m.group(0).replace(tok, _mask(tok))
        out = pat.sub(_sub, out)
    # URL query params
    out = re.sub(
        r"([?&])(" + "|".join(_SENSITIVE_QUERY_PARAMS) + r")=([^&\s'\"]+)",
        lambda m: f"{m.group(1)}{m.group(2)}={_mask(m.group(3))}",
        out,
        flags=re.IGNORECASE,
    )
    return out


def redact_dict(d: Any) -> Any:
    if isinstance(d, dict):
        return {k: redact_dict(v) for k, v in d.items()}
    if isinstance(d, list):
        return [redact_dict(x) for x in d]
    if isinstance(d, str):
        return redact_text(d)
    return d


__all__ = [
    "repair_tool_call_arguments",
    "sanitize_surrogates",
    "strip_non_ascii",
    "sanitize_messages",
    "ThinkScrubber",
    "scrub_think_blocks",
    "redact_text",
    "redact_dict",
]
