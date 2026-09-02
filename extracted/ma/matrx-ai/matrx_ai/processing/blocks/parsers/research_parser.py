"""Research parser — produces the ResearchData shape that ResearchBlock.tsx expects.

Input: raw XML-tagged markdown inside <research>...</research> tags.

The LLM produces free-form markdown with section headers. We parse each
section's content into structured findings.  For sections we can't fully
structure (missing source/significance metadata), we synthesise a single
finding per section from whatever text is available so the renderer always
has something to display.
"""

from __future__ import annotations

import re

from matrx_ai.processing.blocks.models.research import (
    ConvergentTheme,
    ResearchBlockData,
    ResearchChallenge,
    ResearchFinding,
    ResearchMetadata,
    ResearchRecommendation,
    ResearchSection,
)

# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------

_URL_RE = re.compile(r'https?://\S+')
_BOLD_LABEL_RE = re.compile(r'^\*\*([^*]+):\*\*\s*(.+)')
_NUMBERED_RE = re.compile(r'^\d+\.\s+(.+)')
_BULLET_RE = re.compile(r'^[-*]\s+(.+)')
_CONFIDENCE_RE = re.compile(r'\b(HIGH|MEDIUM|LOW)\b', re.IGNORECASE)

# Section names we treat as top-level metadata rather than structured sections
_META_SECTIONS = {
    "overview", "executive summary", "introduction", "conclusion",
    "key takeaways", "takeaways", "limitations", "short-term outlook",
    "short term outlook", "medium-term outlook", "medium term outlook",
    "long-term vision", "long term vision", "convergent themes",
    "challenges", "recommendations", "metadata",
}


def parse_research(content: str) -> ResearchBlockData | None:
    """Parse research markdown into structured ResearchBlockData."""
    try:
        clean = re.sub(r'</?research>', '', content).strip()
        return _parse(clean)
    except Exception:
        return None


def _parse(text: str) -> ResearchBlockData:
    lines = text.split("\n")

    title = ""
    current_h = ""
    current_lines: list[str] = []
    section_chunks: list[tuple[str, list[str]]] = []  # (header, lines)

    for line in lines:
        hm = re.match(r'^(#{1,6})\s+(.+)', line)
        if hm:
            if current_h or current_lines:
                section_chunks.append((current_h, current_lines))
            current_h = hm.group(2).strip()
            level = len(hm.group(1))
            if level == 1 and not title:
                title = current_h
                current_h = ""
            current_lines = []
        else:
            current_lines.append(line)

    if current_h or current_lines:
        section_chunks.append((current_h, current_lines))

    # ----- Accumulate fields -----
    overview = ""
    introduction = ""
    conclusion = ""
    executive_summary: str | None = None
    research_scope: str | None = None
    key_focus_areas: str | None = None
    analysis_period: str | None = None
    research_questions: list[str] = []
    sections: list[ResearchSection] = []
    convergent_themes: list[ConvergentTheme] = []
    short_term: list[str] = []
    medium_term: list[str] = []
    long_term: list[str] = []
    challenges: list[ResearchChallenge] = []
    recommendations: list[ResearchRecommendation] = []
    key_takeaways: list[str] = []
    limitations: list[str] = []
    metadata = ResearchMetadata()

    section_idx = 0
    finding_idx = 0
    challenge_idx = 0
    rec_idx = 0

    for header, chunk_lines in section_chunks:
        lower = header.lower()
        body = "\n".join(chunk_lines).strip()

        # Extract inline metadata from any section
        for m in re.finditer(r'\*\*Research Scope:\*\*\s*(.+)', body):
            research_scope = m.group(1).strip()
        for m in re.finditer(r'\*\*Key Focus Areas:\*\*\s*(.+)', body):
            key_focus_areas = m.group(1).strip()
        for m in re.finditer(r'\*\*Analysis Period:\*\*\s*(.+)', body):
            analysis_period = m.group(1).strip()

        if not lower:
            continue

        if "overview" in lower or "executive summary" in lower:
            overview = body
            if "executive" in lower:
                executive_summary = body
        elif "introduction" in lower:
            introduction = body
            for m in re.finditer(r'^\d+\.\s+(.+)$', body, re.MULTILINE):
                research_questions.append(m.group(1).strip())
        elif "conclusion" in lower:
            conclusion = body
        elif "key takeaway" in lower or lower == "takeaways":
            for m in re.finditer(r'^[-*\d.]\s*(.+)$', body, re.MULTILINE):
                key_takeaways.append(m.group(1).strip())
        elif "limitation" in lower:
            for m in re.finditer(r'^[-*\d.]\s*(.+)$', body, re.MULTILINE):
                limitations.append(m.group(1).strip())
        elif "short-term" in lower or "short term" in lower:
            for m in re.finditer(r'^[-*\d.]\s*(.+)$', body, re.MULTILINE):
                short_term.append(m.group(1).strip())
        elif "medium-term" in lower or "medium term" in lower:
            for m in re.finditer(r'^[-*\d.]\s*(.+)$', body, re.MULTILINE):
                medium_term.append(m.group(1).strip())
        elif "long-term" in lower or "long term" in lower or "long-term vision" in lower:
            for m in re.finditer(r'^[-*\d.]\s*(.+)$', body, re.MULTILINE):
                long_term.append(m.group(1).strip())
        elif "convergent theme" in lower or "theme" in lower:
            for theme_chunk in _split_bold_items(body):
                if ":" in theme_chunk:
                    t, d = theme_chunk.split(":", 1)
                    convergent_themes.append(ConvergentTheme(theme=t.strip(), description=d.strip()))
                elif theme_chunk:
                    convergent_themes.append(ConvergentTheme(theme=theme_chunk, description=""))
        elif "challenge" in lower:
            for item in _split_numbered_or_bold_items(body):
                title_part, desc_part = _split_title_desc(item)
                cat_raw = "other"
                for kw, cat in [("technical", "technical"), ("ethic", "ethical"),
                                 ("regulat", "regulatory")]:
                    if kw in item.lower():
                        cat_raw = cat
                        break
                challenges.append(ResearchChallenge(
                    id=f"challenge-{challenge_idx}",
                    title=title_part,
                    description=desc_part,
                    category=cat_raw,
                ))
                challenge_idx += 1
        elif "recommendation" in lower:
            for item in _split_numbered_or_bold_items(body):
                target = "general"
                lower_item = item.lower()
                for kw, t in [("researcher", "researchers"), ("industry", "industry"),
                               ("policy", "policymakers")]:
                    if kw in lower_item:
                        target = t
                        break
                recommendations.append(ResearchRecommendation(
                    id=f"rec-{rec_idx}",
                    recommendation=item.strip(),
                    target=target,
                ))
                rec_idx += 1
        elif "metadata" in lower:
            for m in re.finditer(r'\*\*([^*]+):\*\*\s*(.+)', body):
                k = m.group(1).strip().lower()
                v = m.group(2).strip()
                if "date" in k:
                    metadata.research_date = v
                elif "updated" in k:
                    metadata.last_updated = v
                elif "confidence" in k:
                    metadata.confidence_rating = v
                elif "bias" in k:
                    metadata.bias_assessment = v
        else:
            # Treat as a structured research section
            findings = _extract_findings(body, f"sec-{section_idx}", finding_idx)
            finding_idx += len(findings)
            sections.append(ResearchSection(
                id=f"sec-{section_idx}",
                title=header,
                findings=findings,
            ))
            section_idx += 1

    return ResearchBlockData(
        title=title or "Research",
        overview=overview,
        introduction=introduction,
        conclusion=conclusion,
        executive_summary=executive_summary,
        research_scope=research_scope,
        key_focus_areas=key_focus_areas,
        analysis_period=analysis_period,
        research_questions=research_questions,
        sections=sections,
        convergent_themes=convergent_themes,
        short_term_outlook=short_term,
        medium_term_outlook=medium_term,
        long_term_vision=long_term,
        challenges=challenges,
        recommendations=recommendations,
        key_takeaways=key_takeaways,
        limitations=limitations,
        metadata=metadata,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_findings(body: str, section_id: str, start_idx: int) -> list[ResearchFinding]:
    """
    Try to extract structured findings from a section body.
    Falls back to a single synthesised finding if the body is unstructured.
    """
    findings: list[ResearchFinding] = []

    # Look for bold-titled sub-items (each becomes a finding)
    items = _split_bold_items(body)
    if len(items) > 1:
        for i, item in enumerate(items):
            title_part, detail = _split_title_desc(item)
            urls = _URL_RE.findall(detail)
            conf_m = _CONFIDENCE_RE.search(detail)
            confidence = conf_m.group(1).upper() if conf_m else "MEDIUM"
            findings.append(ResearchFinding(
                id=f"finding-{start_idx + i}",
                title=title_part or f"Finding {i + 1}",
                key_details=detail,
                confidence_level=confidence,
                urls=urls,
            ))
    else:
        # Single-body section → one finding
        urls = _URL_RE.findall(body)
        conf_m = _CONFIDENCE_RE.search(body)
        confidence = conf_m.group(1).upper() if conf_m else "MEDIUM"
        first_line = body.split("\n")[0].strip() or "Finding"
        findings.append(ResearchFinding(
            id=f"finding-{start_idx}",
            title=first_line[:80],
            key_details=body,
            confidence_level=confidence,
            urls=urls,
        ))

    return findings


def _split_bold_items(body: str) -> list[str]:
    """Split body on **Bold:** markers, returning one chunk per item."""
    parts = re.split(r'\n(?=\*\*)', body)
    return [p.strip() for p in parts if p.strip()]


def _split_numbered_or_bold_items(body: str) -> list[str]:
    """Split on numbered list items or bold markers."""
    parts = re.split(r'\n(?=\d+\.\s|\*\*)', body)
    result = []
    for p in parts:
        p = p.strip()
        if p:
            # Strip leading number/bold
            p = re.sub(r'^\d+\.\s*', '', p)
            p = re.sub(r'^\*\*([^*]+)\*\*:?\s*', r'\1: ', p)
            result.append(p)
    return result


def _split_title_desc(text: str) -> tuple[str, str]:
    """Split 'Title: description' or '**Title:** description' into (title, desc)."""
    m = re.match(r'^\*\*([^*]+)\*\*:?\s*(.*)', text, re.DOTALL)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    if ":" in text:
        parts = text.split(":", 1)
        return parts[0].strip(), parts[1].strip()
    return text[:60].strip(), text.strip()
