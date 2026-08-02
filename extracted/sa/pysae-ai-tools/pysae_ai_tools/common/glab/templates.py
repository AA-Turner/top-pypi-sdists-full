"""Shared helpers to parse Pysae issue template sections.

Used by:
- glab/issue_audit (template conformance audit)
- glab/issue_ready_check (autopilot prerequisite gate)

Sections are H2 (##) or H3 (###) headings; H1 is the issue title (rare in
descriptions), H4+ is body. Emojis are stripped from headings for
comparison, accents are folded, casing is normalised.
"""

import re
import unicodedata
from dataclasses import dataclass

_HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
_EMOJI_RE = re.compile(
    r"[\U0001f300-\U0001f9ff\U00002600-\U000027bf\U0000fe00-\U0000fe0f"
    r"\U0000200d\U00002702-\U000027b0\U0001fa00-\U0001fa6f"
    r"\U0001fa70-\U0001faff\U00002500-\U00002bef]+"
)
_MIN_PLACEHOLDER_LEN = 10


@dataclass(frozen=True)
class Section:
    heading: str  # raw heading text, emoji stripped, trimmed
    normalised: str  # lowercased + accents folded + apostrophes -> space
    body: str  # raw body lines between this heading and the next
    level: int = 2  # heading depth (2 for ##, 3 for ###)


def strip_heading_emojis(text: str) -> str:
    return _EMOJI_RE.sub("", text).strip()


def _normalise(text: str) -> str:
    no_accents = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", no_accents.lower()).strip()


def extract_sections(markdown: str) -> list[Section]:
    sections: list[Section] = []
    current_heading: str | None = None
    current_level: int = 2
    current_body: list[str] = []

    def flush() -> None:
        if current_heading is None:
            return
        body = "\n".join(current_body).strip("\n")
        sections.append(
            Section(
                heading=current_heading,
                normalised=_normalise(current_heading),
                body=body,
                level=current_level,
            )
        )

    for line in markdown.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            flush()
            current_heading = strip_heading_emojis(match.group(2))
            current_level = len(match.group(1))
            current_body = []
        elif current_heading is not None:
            current_body.append(line)

    flush()
    return sections


def find_section(markdown: str, heading_name: str) -> Section | None:
    target = _normalise(strip_heading_emojis(heading_name))
    for section in extract_sections(markdown):
        if section.normalised == target:
            return section
    return None


def is_placeholder_only(body: str) -> bool:
    significant_lines: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        if line.startswith(">"):
            # Italic-wrapped blockquote lines like "> _Décrivez ici_" are the
            # Pysae template's placeholder hints. Substantive blockquote content
            # (a real quote or callout) is kept.
            inner = line.lstrip("> ").strip()
            if (inner.startswith("_") and inner.endswith("_")) or (inner.startswith("*") and inner.endswith("*")):
                continue
        significant_lines.append(line)
    significant = " ".join(significant_lines)
    return len(significant) < _MIN_PLACEHOLDER_LEN
