"""Parse an ai-note Markdown file and extract its Open questions."""

import re
from dataclasses import dataclass

from ...common.glab.templates import find_section

_QUESTION_RE = re.compile(
    r"^\s*-\s+(?P<resolved>\[✓\s*#\d+\]\s+)?(?P<prio>🔴|🟡|🟢)\s+" r"\*\*(?P<title>[^*]+)\*\*\s*:\s*(?P<detail>.+)$"
)
_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True)
class OpenQuestion:
    priority: str
    title: str
    detail: str
    source_issue_url: str | None


def _parse_frontmatter(text: str) -> dict[str, str]:
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    out: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def parse_ai_note(markdown: str, only: list[str] | None = None) -> list[OpenQuestion]:
    frontmatter = _parse_frontmatter(markdown)
    issue_url = frontmatter.get("issue")

    body_after_fm = _FRONTMATTER_RE.sub("", markdown, count=1)
    section = find_section(body_after_fm, "Open questions")
    if section is None:
        return []

    questions: list[OpenQuestion] = []
    for line in section.body.splitlines():
        match = _QUESTION_RE.match(line)
        if not match:
            continue
        if match.group("resolved"):
            continue
        prio = match.group("prio")
        if only and prio not in only:
            continue
        questions.append(
            OpenQuestion(
                priority=prio,
                title=match.group("title").strip(),
                detail=match.group("detail").strip(),
                source_issue_url=issue_url,
            )
        )
    return questions
