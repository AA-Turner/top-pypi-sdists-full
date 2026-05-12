"""Perplexity-style features for sage: citations, focus modes, pro-search.

Sage already has the underlying primitives:
  - SEARCH_WEB / WEB_FETCH tools (exposed in the prompt)
  - Multi-model routing via MultiModelOrchestrator
  - Persistent memory via MemoryStore (D13)

This module adds the user-facing abstractions that mirror Perplexity's
product surface: citation collection, focus-mode selection, and the
multi-step "Pro Search" research plan.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum

__all__ = [
    "Citation",
    "CitationTracker",
    "FocusMode",
    "FocusConfig",
    "ResearchPlan",
    "ResearchStep",
    "build_research_plan",
    "get_focus_config",
]


# ── Citation tracking ───────────────────────────────────────────────


_URL_RE = re.compile(
    r"https?://[^\s)\]>'\"]+",
)


@dataclass
class Citation:
    """A single source citation collected from a model response."""

    url: str
    title: str = ""
    snippet: str = ""

    def short(self) -> str:
        """Compact display form: host + path tail."""
        m = re.match(r"https?://(?:www\.)?([^/]+)(/.*)?", self.url)
        if not m:
            return self.url
        host = m.group(1)
        tail = (m.group(2) or "/").rstrip("/")
        if tail and tail != "/":
            tail = "/" + tail.split("/")[-1]
        return f"{host}{tail}"


class CitationTracker:
    """Collect URLs the model cites across a conversation.

    Use:
        tracker = CitationTracker()
        tracker.ingest(response_text)
        tracker.ingest(another_response)
        prompt += tracker.render_for_prompt()
    """

    def __init__(self) -> None:
        self._urls: list[str] = []
        self._seen: set[str] = set()

    def ingest(self, text: str) -> int:
        """Scan `text` for URLs; add new ones in order. Returns count added."""
        added = 0
        for m in _URL_RE.finditer(text or ""):
            url = m.group(0).rstrip(",.;:")
            if url in self._seen:
                continue
            self._seen.add(url)
            self._urls.append(url)
            added += 1
        return added

    def citations(self) -> list[Citation]:
        return [Citation(url=u) for u in self._urls]

    def render_for_prompt(self) -> str:
        """Format collected citations as `[1] url ...` lines for context."""
        if not self._urls:
            return ""
        lines = ["## Sources"]
        for i, url in enumerate(self._urls, start=1):
            lines.append(f"[{i}] {url}")
        return "\n".join(lines) + "\n"


# ── Focus modes ──────────────────────────────────────────────────────


class FocusMode(Enum):
    GENERAL = "general"
    ACADEMIC = "academic"
    WRITING = "writing"
    MATH = "math"
    CODE = "code"
    YOUTUBE = "youtube"   # transcript-aware reading
    REDDIT = "reddit"     # discussion-thread reading


@dataclass(frozen=True)
class FocusConfig:
    name: str
    system_prompt: str
    preferred_tier: str  # "small" | "medium" | "big"
    use_web: bool = True


_GENERAL_PROMPT = """\
You are SAGE in general-purpose research mode. Answer the user's question
concisely with the most reliable sources available. Cite URLs inline when
you use information from a web source. Prefer official documentation over
blog posts. If unsure, say so explicitly.
"""

_ACADEMIC_PROMPT = """\
You are SAGE in academic-research mode. Answer with the rigor of a
graduate-level researcher:

- Cite primary sources (peer-reviewed papers, official standards) by URL.
- Distinguish established findings from preliminary or contested results.
- Quantify uncertainty when relevant ("studies vary by ±15%").
- Note publication date and methodology when it matters.
- If the user's question has multiple competing positions, present them
  fairly with citations for each.

Never assert a fact without a citation when the question is empirical.
"""

_WRITING_PROMPT = """\
You are SAGE in writing-assistance mode. Help the user write clearly:

- Match the target style and tone (academic vs. casual, formal vs. terse).
- Eliminate filler. Cut redundant phrases. Tighten sentences.
- Prefer active voice unless passive is required for emphasis.
- Vary sentence length for rhythm. Avoid monotonous structure.
- Preserve the writer's voice — improve, don't replace.
- For drafts: offer 2-3 variants when the change is significant.
"""

_MATH_PROMPT = """\
You are SAGE in math-and-reasoning mode. Solve problems step by step:

- Show your work in clear, numbered steps.
- State assumptions explicitly before computing.
- Check edge cases (n=0, n=1, negatives, overflow).
- For proofs, lay out hypothesis → reasoning → conclusion.
- Verify the answer numerically if applicable.
- If a result is approximate, say so and quantify the error bound.

Never skip steps — the reasoning IS the answer.
"""

_CODE_PROMPT = """\
You are SAGE in code-generation mode. Write complete, working code:

- No placeholders. No TODO comments. No "..." or "implement this".
- Match the project's idioms (READ files first if unclear).
- Use the project's test framework. Verify with RUN: before claiming done.
- Cite docs URLs for non-obvious API usage.
- Prefer standard library over external deps unless the dep is canonical.
- Handle error cases — don't assume the happy path.
- For unfamiliar libraries, WEB_FETCH the docs before guessing.
"""

_YOUTUBE_PROMPT = """\
You are SAGE in YouTube/video-research mode. When the user references a
video URL, fetch its transcript (or describe how to) and answer based on
the actual content. Note timestamps for specific claims. Don't summarize
beyond what the transcript supports.
"""

_REDDIT_PROMPT = """\
You are SAGE in discussion-thread mode. When the user references a Reddit
thread or forum URL, distinguish the OP's question from top comments
from late additions. Note vote counts and OP status. Don't treat one
upvoted comment as consensus.
"""


_FOCUS_CONFIGS: dict[FocusMode, FocusConfig] = {
    FocusMode.GENERAL:  FocusConfig("general",  _GENERAL_PROMPT,  "medium", True),
    FocusMode.ACADEMIC: FocusConfig("academic", _ACADEMIC_PROMPT, "big",    True),
    FocusMode.WRITING:  FocusConfig("writing",  _WRITING_PROMPT,  "medium", False),
    FocusMode.MATH:     FocusConfig("math",     _MATH_PROMPT,     "big",    False),
    FocusMode.CODE:     FocusConfig("code",     _CODE_PROMPT,     "big",    True),
    FocusMode.YOUTUBE:  FocusConfig("youtube",  _YOUTUBE_PROMPT,  "medium", True),
    FocusMode.REDDIT:   FocusConfig("reddit",   _REDDIT_PROMPT,   "medium", True),
}


def get_focus_config(mode: FocusMode) -> FocusConfig:
    return _FOCUS_CONFIGS[mode]


# ── Pro Search: multi-step research plan ─────────────────────────────


@dataclass
class ResearchStep:
    kind: str  # "search" | "fetch" | "analyze" | "synthesis"
    description: str


@dataclass
class ResearchPlan:
    question: str
    steps: list[ResearchStep] = field(default_factory=list)


def build_research_plan(question: str) -> ResearchPlan:
    """Mirror Perplexity's "Pro Search" — multi-step research orchestration.

    Plan shape:
      1-2 web searches identifying the most relevant sources
      1-2 specific URL fetches reading the strongest sources in detail
      1 analysis step extracting positions / numbers / quotes
      1 synthesis step producing the answer with citations

    The MultiModelOrchestrator routes each step to the best model for it:
    small models for search-result triage, big models for synthesis.
    """
    q = question.strip()
    steps: list[ResearchStep] = [
        ResearchStep(
            kind="search",
            description=f"Web search for primary sources on: {q}",
        ),
        ResearchStep(
            kind="search",
            description=f"Search for opposing or alternative viewpoints on: {q}",
        ),
        ResearchStep(
            kind="fetch",
            description="Fetch the 2-3 highest-quality sources from the search results "
                        "(prefer official docs, peer-reviewed papers, or canonical references).",
        ),
        ResearchStep(
            kind="analyze",
            description="Extract specific claims, numbers, and direct quotes from the fetched "
                        "sources. Note where sources agree and where they diverge.",
        ),
        ResearchStep(
            kind="synthesis",
            description=f"Synthesize a complete answer to '{q}'. Cite each claim with the "
                        "source URL inline. Be explicit about uncertainty or conflicting evidence.",
        ),
    ]
    return ResearchPlan(question=q, steps=steps)
