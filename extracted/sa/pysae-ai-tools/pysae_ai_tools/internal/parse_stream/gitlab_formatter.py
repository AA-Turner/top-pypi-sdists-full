"""Format Claude Code stream-json events as GitLab-flavored Markdown.

Produces readable markdown for GitLab issue/MR discussion notes.
Separates assistant text (shown prominently) from tool activity
(collapsed in a details section).
"""

import re
from dataclasses import dataclass, field
from typing import Any

MAX_RESULT_LINES = 30
TAIL_LINES = 5

# Text containing markdown structure (headers, tables, lists) is "real" content.
# Short text without structure is thinking/narration → goes to activity.
_STRUCTURED_RE = re.compile(r"^#{1,6}\s|^\|.*\|$|^[-*]\s", re.MULTILINE)


def _is_structured_text(text: str) -> bool:
    """Return True if text looks like structured markdown content (headers, tables, lists)."""
    return bool(_STRUCTURED_RE.search(text))


def _tool_detail(name: str, input_data: dict[str, Any]) -> str:
    """Extract the most relevant detail from a tool call's input, single-line."""
    raw = ""
    if "command" in input_data:
        raw = str(input_data["command"])
    elif "pattern" in input_data:
        raw = str(input_data["pattern"])
    elif "file_path" in input_data:
        raw = str(input_data["file_path"])
    elif "skill" in input_data:
        raw = str(input_data["skill"])
    elif "prompt" in input_data:
        raw = str(input_data["prompt"])
    single = raw.replace("\n", " ").strip()
    return single


def _truncate_result(text: str) -> str:
    """Truncate long tool results with head/tail preservation."""
    lines = text.split("\n")
    if len(lines) > MAX_RESULT_LINES:
        head = lines[: MAX_RESULT_LINES - TAIL_LINES - 1]
        tail = lines[-TAIL_LINES:]
        skipped = len(lines) - len(head) - len(tail)
        text = "\n".join(head + [f"… ({skipped} lines omitted)"] + tail)
    return text


def _to_blockquote(text: str) -> str:
    """Convert text to a GitLab blockquote (> prefix on each line)."""
    return "\n".join(f"> {line}" for line in text.split("\n"))


EXT_TO_LANG: dict[str, str] = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".json": "json",
    ".sh": "bash",
    ".bash": "bash",
    ".html": "html",
    ".css": "css",
    ".md": "markdown",
    ".rs": "rust",
    ".go": "go",
    ".rb": "ruby",
    ".java": "java",
    ".toml": "toml",
    ".xml": "xml",
    ".sql": "sql",
}


def _code_fence(text: str, lang: str = "") -> str:
    """Wrap text in a code fence, using enough backticks to avoid conflicts."""
    # Count max consecutive backticks in content to pick a safe fence
    max_ticks = 2
    count = 0
    for ch in text:
        if ch == "`":
            count += 1
            if count > max_ticks:
                max_ticks = count
        else:
            count = 0
    fence = "`" * (max_ticks + 1)
    return f"{fence}{lang}\n{text}\n{fence}"


def _lang_from_path(file_path: str) -> str:
    """Detect language hint from file extension."""
    # Handle Dockerfile specially
    if file_path.endswith("Dockerfile") or file_path.endswith(".dockerfile"):
        return "dockerfile"
    for ext, lang in EXT_TO_LANG.items():
        if file_path.endswith(ext):
            return lang
    return ""


def _detect_lang_from_input(input_data: dict[str, Any]) -> str:
    """Scan tool input values for a file path and return language hint."""
    # Check common keys that hold file paths
    for key in ("file_path", "path", "pattern", "glob", "command"):
        val = input_data.get(key, "")
        if not isinstance(val, str) or not val:
            continue
        if key == "command":
            # Extract last argument that looks like a file path
            for token in reversed(val.split()):
                lang = _lang_from_path(token)
                if lang:
                    return lang
        else:
            lang = _lang_from_path(val)
            if lang:
                return lang
    return ""


@dataclass
class GitLabFormatter:
    """Stateful formatter that accumulates text and tool activity separately.

    Call `process_event()` to feed events, then `compose()` to build
    the final note body with text on top and activity collapsed below.

    Text routing: structured markdown (headers, tables, lists) goes to
    text_parts (shown prominently). Plain narration/thinking goes to
    activity_parts (collapsed with tool calls).
    """

    text_parts: list[str] = field(default_factory=list, init=False, repr=False)
    activity_parts: list[str] = field(default_factory=list, init=False, repr=False)
    finished: bool = field(default=False, init=False, repr=False)
    _tool_langs: dict[str, str] = field(default_factory=dict, init=False, repr=False)

    def process_event(self, event: dict[str, Any]) -> None:
        """Route an event to the appropriate bucket (text or activity)."""
        event_type = event.get("type")

        if event_type == "assistant":
            self._process_assistant(event)
        elif event_type == "user":
            self._process_user(event)
        elif event_type == "system":
            self._process_system(event)

    def compose(self) -> str:
        """Build the note body: text first, then activity section below.

        While running, the activity section is open (<details open>).
        Once finished, it collapses (<details>).
        """
        text = "\n\n".join(t for t in self.text_parts if t)
        activity = "\n\n".join(a for a in self.activity_parts if a)

        parts: list[str] = []
        if text:
            parts.append(text)
        if activity:
            tag = "<details>" if self.finished else "<details open>"
            parts.append(f"{tag}<summary>:mag: Détails de l'analyse</summary>\n\n{activity}\n</details>")
        return "\n\n".join(parts)

    def has_content(self) -> bool:
        return bool(self.text_parts or self.activity_parts)

    def _process_system(self, event: dict[str, Any]) -> None:
        subtype = event.get("subtype", "")
        if subtype == "init":
            return
        msg = event.get("message") or event.get("error") or event.get("reason") or ""
        if msg:
            self.activity_parts.append(f"> :information_source: {msg}")

    def _process_assistant(self, event: dict[str, Any]) -> None:
        message = event.get("message") or {}
        contents: list[dict[str, Any]] = message.get("content") or []

        has_tool_use = any(b.get("type") == "tool_use" for b in contents)

        for block in contents:
            if block.get("type") == "text":
                text = str(block.get("text", "")).strip()
                if not text:
                    continue
                # Route text to the right bucket:
                # - Text in a message with tool_use → always thinking
                # - Structured text (headers/tables/lists) → real content
                # - Long unstructured text (>200 chars) → likely final answer
                # - Short unstructured text → thinking/narration
                if has_tool_use:
                    self.activity_parts.append(f":thought_balloon: _{text}_")
                elif _is_structured_text(text) or len(text) > 200:
                    self.text_parts.append(text)
                else:
                    self.activity_parts.append(f":thought_balloon: _{text}_")
            elif block.get("type") == "tool_use":
                name = str(block.get("name", ""))
                tool_input = block.get("input") or {}
                tool_id = str(block.get("id", ""))
                if tool_id:
                    lang = _detect_lang_from_input(tool_input)
                    if lang:
                        self._tool_langs[tool_id] = lang
                detail = _tool_detail(name, tool_input)
                if detail:
                    self.activity_parts.append(f":wrench: **{name}**\n{_to_blockquote(detail)}")
                else:
                    self.activity_parts.append(f":wrench: **{name}**")

    def _process_user(self, event: dict[str, Any]) -> None:
        message = event.get("message") or {}
        contents: list[dict[str, Any]] = message.get("content") or []

        for block in contents:
            if block.get("type") != "tool_result":
                continue
            is_error = bool(block.get("is_error"))
            tool_use_id = str(block.get("tool_use_id", ""))
            lang = self._tool_langs.pop(tool_use_id, "")
            raw_content = block.get("content") or ""
            # Sub-agent results come as a list of content blocks — extract text
            if isinstance(raw_content, list):
                text_parts = [b.get("text", "") for b in raw_content if isinstance(b, dict) and b.get("type") == "text"]
                content = "\n".join(text_parts).strip()
            else:
                content = str(raw_content).strip()
            content = re.sub(r"\[result-id: \w+\]\s*", "", content).strip()

            if is_error:
                if not content:
                    self.activity_parts.append(":x: **Failed**")
                else:
                    truncated = _truncate_result(content)
                    self.activity_parts.append(f":x: **Failed**\n{_code_fence(truncated, lang)}")
            elif content:
                if _is_structured_text(content):
                    self.activity_parts.append(content)
                else:
                    truncated = _truncate_result(content)
                    self.activity_parts.append(_code_fence(truncated, lang))
