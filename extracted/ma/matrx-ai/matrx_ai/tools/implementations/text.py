from __future__ import annotations

import re
import time
from collections import Counter
from typing import Any

from matrx_graph.nodes.text.regex import RegexExtractOutput

from matrx_ai.tools.arg_models.text_args import RegexExtractArgs, TextAnalyzeArgs
from matrx_ai.tools.kinds.text_tools import TextAnalysis
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult


async def text_analyze(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = TextAnalyzeArgs(**args)
    text = parsed.text

    analysis_type = parsed.analysis_type.lower()
    output: dict[str, Any] = {"analysis_type": analysis_type}

    if analysis_type == "summary":
        words = text.split()
        output["word_count"] = len(words)
        output["char_count"] = len(text)
        output["sentence_count"] = len(re.split(r"[.!?]+", text.strip()))
        output["paragraph_count"] = len([p for p in text.split("\n\n") if p.strip()])

    elif analysis_type == "keywords":
        words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
        stop_words = {
            "the",
            "and",
            "for",
            "are",
            "but",
            "not",
            "you",
            "all",
            "can",
            "her",
            "was",
            "one",
            "our",
            "out",
            "has",
            "have",
            "with",
            "this",
            "that",
            "from",
            "they",
            "been",
            "said",
            "each",
            "which",
            "their",
            "will",
            "other",
            "about",
        }
        filtered = [w for w in words if w not in stop_words]
        counter = Counter(filtered)
        output["keywords"] = [
            {"word": w, "count": c} for w, c in counter.most_common(20)
        ]

    elif analysis_type == "entities":
        patterns = {
            "emails": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "urls": r"https?://[^\s<>\"]+",
            "phones": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "dates": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        }
        for entity_type, pattern in patterns.items():
            output[entity_type] = list(set(re.findall(pattern, text)))

    elif analysis_type == "language":
        output["char_count"] = len(text)
        output["word_count"] = len(text.split())
        output["unique_words"] = len(set(text.lower().split()))
        output["avg_word_length"] = round(
            sum(len(w) for w in text.split()) / max(len(text.split()), 1), 1
        )
    else:
        output["message"] = (
            f"Unknown analysis type '{analysis_type}'. Supported: summary, keywords, entities, language."
        )

    return ToolResult(
        success=True,
        # KindModel result (KIND_TOOL_LEDGER): one union shape across the four
        # analysis modes; `analysis_type` names the projection.
        output=TextAnalysis(**output).model_dump(mode="json"),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="text_analyze",
        call_id=ctx.call_id,
    )


async def text_regex_extract(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    from matrx_ai.tools._generated_declarations import TextRegexExtractArgs
    TextRegexExtractArgs.model_validate(args)  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    parsed = RegexExtractArgs(**args)

    # RESULT KIND = the registered `regex_extract_result` (KIND_TOOL_LEDGER):
    # the tool returns matrx-graph's own RegexExtractOutput rather than minting
    # a near-duplicate slug. All three branches (find_all / one match / no
    # match) are the SAME shape — matches + count + first; "no match" is the
    # honest empty result, not a prose message. The old single-match `span` key
    # was dropped with the reshape (no consumer read it; the kind's contract is
    # the platform-wide one).
    try:
        if parsed.find_all:
            found = re.findall(parsed.pattern, parsed.text)
            # findall yields tuples when the pattern has 2+ groups — serialize
            # them as lists, exactly as the workflow regex node's schema says.
            matches = [list(m) if isinstance(m, tuple) else m for m in found]
        else:
            match = re.search(parsed.pattern, parsed.text)
            matches = [match.group(parsed.group)] if match else []
        return ToolResult(
            success=True,
            output=RegexExtractOutput(
                matches=matches,
                count=len(matches),
                first=matches[0] if matches else None,
            ).model_dump(mode="json"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="regex_extract",
            call_id=ctx.call_id,
        )
    except re.error as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="regex",
                message=f"Invalid regex pattern: {exc}",
                suggested_action="Check the regex syntax and try again.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="regex_extract",
            call_id=ctx.call_id,
        )
