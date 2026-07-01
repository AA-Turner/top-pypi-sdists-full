"""
cvc.core.pageindex — Tier 4: LLM-Powered PageIndex Document RAG.

Faithfully adapts the VectifyAI/PageIndex architecture for CVC.
Unlike traditional RAG that chunks documents arbitrarily, PageIndex extracts
the natural Table-of-Contents structure and builds a page-indexed tree.

Architecture (from VectifyAI/PageIndex):
  1. PDF → extract pages → detect TOC → extract TOC structure
  2. Map logical page numbers to physical page indices
  3. Build hierarchical tree: {title, node_id, start_index, end_index, nodes[]}
  4. Recursively split nodes that are too large
  5. Generate LLM summaries for each node
  6. Search = LLM-guided top-down tree navigation

Node structure (matches real PageIndex):
  {
    "title": "Chapter 1: Introduction",
    "node_id": "0001",
    "start_index": 1,      # first page (1-based)
    "end_index": 15,        # last page (inclusive)
    "summary": "...",
    "nodes": [ ... ]        # child nodes
  }

This module is used ONLY by the CLI agent.  The proxy server and MCP server
never import or reference it.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import zstandard as zstd

logger = logging.getLogger("cvc.pageindex")

# ---------------------------------------------------------------------------
# Type alias — the caller injects a simple  prompt → response  function
# ---------------------------------------------------------------------------
LLMCallFn = Callable[[str], str]

# ---------------------------------------------------------------------------
# Configuration defaults (mirrors PageIndex config.yaml)
# ---------------------------------------------------------------------------

TOC_CHECK_PAGE_NUM = 20           # Max pages to scan for TOC
MAX_PAGE_NUM_EACH_NODE = 10       # Max pages per tree node before splitting
MAX_TOKEN_CHARS_EACH_NODE = 80_000  # ~20 000 tokens × 4 chars/token
_GROUP_MAX_CHARS = 40_000         # Max chars per LLM group window
_ZSTD_LEVEL = 3


# ═══════════════════════════════════════════════════════════════════════════
# JSON / LLM-response helpers  (adapted from PageIndex utils.py)
# ═══════════════════════════════════════════════════════════════════════════

def _extract_json(content: str) -> Any:
    """Robustly extract JSON from an LLM response (handles ```json fences)."""
    try:
        start = content.find("```json")
        if start != -1:
            start += 7
            end = content.rfind("```")
            raw = content[start:end].strip()
        else:
            raw = content.strip()

        raw = raw.replace("None", "null")
        raw = " ".join(raw.split())  # normalise whitespace

        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            raw = raw.replace(",]", "]").replace(",}", "}")  # noqa: F841
            return json.loads(raw)
        except Exception:
            return {}
    except Exception:
        return {}


def _convert_physical_index_to_int(
    data: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Convert ``<physical_index_X>`` strings to plain ints."""
    for item in data:
        pi = item.get("physical_index")
        if isinstance(pi, str):
            m = re.search(r"(\d+)", pi)
            item["physical_index"] = int(m.group(1)) if m else None
    return data


# ═══════════════════════════════════════════════════════════════════════════
# Text / PDF / Markdown extraction
# ═══════════════════════════════════════════════════════════════════════════

def _extract_pdf_pages(file_path: Path) -> list[tuple[str, int]]:
    """Return [(page_text, char_count)] for every page in a PDF."""
    try:
        import pymupdf  # type: ignore[import-untyped]
    except ImportError:
        try:
            import fitz as pymupdf  # type: ignore[import-untyped]
        except ImportError:
            raise ImportError(
                "PDF support requires 'pymupdf'.  Install it with:\n"
                "  pip install pymupdf\n"
                "Or install CVC with the pageindex extra:\n"
                "  pip install 'tm-ai[pageindex]'"
            )

    doc = pymupdf.open(str(file_path))
    pages: list[tuple[str, int]] = []
    for page in doc:
        text = page.get_text()
        pages.append((text, len(text)))
    doc.close()
    return pages


def _extract_markdown_sections(file_path: Path) -> list[dict[str, Any]]:
    """Parse a Markdown file into sections based on ``#`` headers."""
    content = file_path.read_text(encoding="utf-8", errors="replace")
    header_re = re.compile(r"^(#{1,6})\s+(.+)$")
    code_fence = re.compile(r"^```")

    lines = content.split("\n")
    sections: list[dict[str, Any]] = []
    in_code = False

    for line_num, line in enumerate(lines, 1):
        if code_fence.match(line.strip()):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = header_re.match(line.strip())
        if m:
            sections.append({
                "title": m.group(2).strip(),
                "level": len(m.group(1)),
                "line_num": line_num,
            })

    # Attach raw text belonging to each section
    for i, sec in enumerate(sections):
        start = sec["line_num"] - 1
        end = sections[i + 1]["line_num"] - 1 if i + 1 < len(sections) else len(lines)
        sec["text"] = "\n".join(lines[start:end]).strip()

    return sections


def _text_to_pseudo_pages(
    text: str, page_size: int = 3000
) -> list[tuple[str, int]]:
    """Split plain text into pseudo-pages (for the no-PDF path)."""
    pages: list[tuple[str, int]] = []
    start = 0
    while start < len(text):
        end = min(start + page_size, len(text))
        if end < len(text):
            para = text.rfind("\n\n", start + page_size // 2, end)
            if para > start:
                end = para + 2
        page_text = text[start:end]
        pages.append((page_text, len(page_text)))
        start = end
    return pages


# ═══════════════════════════════════════════════════════════════════════════
# TOC Detection & Extraction  (from PageIndex page_index.py)
# ═══════════════════════════════════════════════════════════════════════════

def _toc_detector_single_page(page_text: str, llm_call: LLMCallFn) -> str:
    """Ask the LLM whether *page_text* looks like a Table-of-Contents page."""
    prompt = (
        "You will be given a page from a document.\n\n"
        "Your job is to detect if this page contains a table of contents.\n\n"
        f"Given page text:\n{page_text[:3000]}\n\n"
        "Reply format:\n"
        '{\n    "thinking": "<brief reasoning>",\n'
        '    "is_toc": "<yes or no>"\n}\n'
        "Directly return the final JSON structure. Do not output anything else."
    )
    result = _extract_json(llm_call(prompt))
    return result.get("is_toc", "no")


def _find_toc_pages(
    page_list: list[tuple[str, int]],
    llm_call: LLMCallFn,
    max_check: int = TOC_CHECK_PAGE_NUM,
) -> list[int]:
    """Scan the first *max_check* pages to locate contiguous TOC pages."""
    last_was_toc = False
    toc_pages: list[int] = []

    for i in range(min(len(page_list), max_check)):
        if i >= max_check and not last_was_toc:
            break
        detected = _toc_detector_single_page(page_list[i][0], llm_call)
        if detected == "yes":
            toc_pages.append(i)
            last_was_toc = True
        elif last_was_toc:
            break  # TOC ended
        else:
            last_was_toc = False

    return toc_pages


def _detect_page_index_in_toc(toc_content: str, llm_call: LLMCallFn) -> str:
    """Detect whether the raw TOC text includes page numbers/indices."""
    prompt = (
        "You will be given a table of contents.\n\n"
        "Your job is to detect if there are page numbers/indices given "
        "within the table of contents.\n\n"
        f"Given text: {toc_content[:5000]}\n\n"
        "Reply format:\n"
        '{\n    "thinking": "<reasoning>",\n'
        '    "page_index_given_in_toc": "<yes or no>"\n}\n'
        "Directly return the final JSON structure. Do not output anything else."
    )
    result = _extract_json(llm_call(prompt))
    return result.get("page_index_given_in_toc", "no")


def _toc_extractor(
    page_list: list[tuple[str, int]],
    toc_page_list: list[int],
    llm_call: LLMCallFn,
) -> dict[str, Any]:
    """Concatenate TOC pages, clean dot-leaders, detect page indices."""
    toc_text = "".join(page_list[i][0] for i in toc_page_list)
    toc_text = re.sub(r"\.{5,}", ": ", toc_text)
    toc_text = re.sub(r"(?:\. ){5,}\.?", ": ", toc_text)

    has_pi = _detect_page_index_in_toc(toc_text, llm_call)
    return {"toc_content": toc_text, "page_index_given_in_toc": has_pi}


def _toc_transformer(
    toc_content: str, llm_call: LLMCallFn
) -> list[dict[str, Any]]:
    """Transform raw TOC text into a structured JSON list via LLM."""
    prompt = (
        "You are given a table of contents.  Transform the whole table of "
        "contents into a JSON format.\n\n"
        "structure is the numeric system for the hierarchy.  E.g. first "
        "section = 1, first subsection = 1.1, second subsection = 1.2.\n\n"
        "Response format:\n"
        '{\n  "table_of_contents": [\n'
        '    {"structure": "<x.x.x or null>", "title": "<title>", '
        '"page": <page number or null>},\n    ...\n  ]\n}\n'
        "Transform the full table of contents in one go.\n"
        "Directly return the final JSON structure, do not output anything else.\n\n"
        f"Given table of contents:\n{toc_content[:8000]}"
    )
    result = _extract_json(llm_call(prompt))

    if isinstance(result, dict) and "table_of_contents" in result:
        items = result["table_of_contents"]
    elif isinstance(result, list):
        items = result
    else:
        return []

    for item in items:
        p = item.get("page")
        if isinstance(p, str):
            try:
                item["page"] = int(p)
            except (ValueError, TypeError):
                item["page"] = None
    return items


# ═══════════════════════════════════════════════════════════════════════════
# Physical-page-index resolution  (from PageIndex page_index.py)
# ═══════════════════════════════════════════════════════════════════════════

def _page_list_to_groups(
    page_list: list[tuple[str, int]],
    start_index: int = 1,
    max_chars: int = _GROUP_MAX_CHARS,
) -> list[str]:
    """Split tagged pages into groups that fit the LLM context window."""
    tagged: list[str] = []
    for i, (text, _) in enumerate(page_list):
        pi = start_index + i
        tagged.append(
            f"<physical_index_{pi}>\n{text}\n<physical_index_{pi}>\n\n"
        )

    char_lens = [len(t) for t in tagged]
    total = sum(char_lens)
    if total <= max_chars:
        return ["".join(tagged)]

    n_parts = max(1, math.ceil(total / max_chars))
    avg = total // n_parts

    groups: list[str] = []
    cur: list[str] = []
    cur_len = 0
    for t, tl in zip(tagged, char_lens):
        if cur_len + tl > avg and cur:
            groups.append("".join(cur))
            cur, cur_len = [], 0
        cur.append(t)
        cur_len += tl
    if cur:
        groups.append("".join(cur))
    return groups


def _add_page_number_to_toc(
    page_text: str,
    structure: list[dict[str, Any]],
    llm_call: LLMCallFn,
) -> list[dict[str, Any]]:
    """Use LLM to locate physical page indices for TOC entries."""
    prompt = (
        "You are given a JSON structure of a document and a partial document.\n"
        "Check if each section title starts in the partial document.\n\n"
        "The text contains tags like <physical_index_X> indicating page X.\n\n"
        "If the section starts here, set start='yes' and physical_index.\n"
        "If not, set start='no' and physical_index=null.\n\n"
        "Response format:\n"
        "[\n"
        '  {"structure": "...", "title": "...", "start": "yes/no", '
        '"physical_index": "<physical_index_X> or null"},\n  ...\n]\n'
        "Directly return the final JSON. Do not output anything else.\n\n"
        f"Partial Document:\n{page_text[:8000]}\n\n"
        f"Given Structure:\n{json.dumps(structure, indent=2)[:4000]}"
    )
    result = _extract_json(llm_call(prompt))
    if isinstance(result, list):
        for item in result:
            item.pop("start", None)
        return result
    return structure


def _generate_toc_from_text(
    page_list: list[tuple[str, int]],
    llm_call: LLMCallFn,
    start_index: int = 1,
) -> list[dict[str, Any]]:
    """Generate a TOC from scratch when no TOC exists (PageIndex process_no_toc)."""
    groups = _page_list_to_groups(page_list, start_index=start_index)

    prompt_init = (
        "You are an expert in extracting hierarchical tree structure.\n"
        "Generate the tree structure of the document.\n\n"
        "structure = numeric hierarchy index (1, 1.1, 1.2, …).\n"
        "The text has <physical_index_X> tags marking page X.\n\n"
        "Response format:\n"
        "[\n"
        '  {"structure": "x.x.x", "title": "<section title>", '
        '"physical_index": "<physical_index_X>"},\n  ...\n]\n'
        "Directly return the final JSON. Do not output anything else.\n\n"
        f"Given text:\n{groups[0][:8000]}"
    )
    toc = _extract_json(llm_call(prompt_init))
    if not isinstance(toc, list):
        toc = []

    for group in groups[1:]:
        prompt_cont = (
            "Continue the tree structure from the previous part.\n\n"
            "structure = numeric hierarchy index.\n"
            "The text has <physical_index_X> tags marking page X.\n\n"
            "Response format:\n"
            "[\n"
            '  {"structure": "x.x.x", "title": "<section title>", '
            '"physical_index": "<physical_index_X>"},\n  ...\n]\n'
            "Return only the additional part. Do not output anything else.\n\n"
            f"Given text:\n{group[:8000]}\n\n"
            f"Previous structure:\n{json.dumps(toc, indent=2)[:4000]}"
        )
        extra = _extract_json(llm_call(prompt_cont))
        if isinstance(extra, list):
            toc.extend(extra)

    return _convert_physical_index_to_int(toc)


# ═══════════════════════════════════════════════════════════════════════════
# Tree building  (from PageIndex utils.py  list_to_tree / post_processing)
# ═══════════════════════════════════════════════════════════════════════════

def _list_to_tree(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert a flat TOC list with ``structure`` indices to a nested tree."""

    def _parent(structure: str | None) -> str | None:
        if not structure:
            return None
        parts = str(structure).split(".")
        return ".".join(parts[:-1]) if len(parts) > 1 else None

    nodes: dict[str, dict[str, Any]] = {}
    roots: list[dict[str, Any]] = []

    for item in data:
        s = str(item.get("structure", ""))
        node: dict[str, Any] = {
            "title": item.get("title", ""),
            "start_index": item.get("start_index"),
            "end_index": item.get("end_index"),
            "nodes": [],
        }
        nodes[s] = node
        parent_s = _parent(s)
        if parent_s and parent_s in nodes:
            nodes[parent_s]["nodes"].append(node)
        else:
            roots.append(node)

    def _clean(n: dict) -> dict:
        if not n["nodes"]:
            del n["nodes"]
        else:
            for c in n["nodes"]:
                _clean(c)
        return n

    return [_clean(r) for r in roots]


def _post_processing(
    structure: list[dict[str, Any]], end_page: int
) -> list[dict[str, Any]]:
    """Assign ``start_index`` / ``end_index`` and build the tree."""
    for i, item in enumerate(structure):
        item["start_index"] = item.get("physical_index")
        if i < len(structure) - 1:
            nxt = structure[i + 1].get("physical_index")
            item["end_index"] = (nxt - 1) if nxt is not None else end_page
        else:
            item["end_index"] = end_page

    tree = _list_to_tree(structure)
    return tree if tree else structure


def _add_preface_if_needed(
    data: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Insert a 'Preface' node when the first section starts after page 1."""
    if data and (data[0].get("physical_index") or 0) > 1:
        data.insert(0, {"structure": "0", "title": "Preface", "physical_index": 1})
    return data


# ═══════════════════════════════════════════════════════════════════════════
# Node enrichment  (IDs, text, summaries, doc description)
# ═══════════════════════════════════════════════════════════════════════════

def _write_node_ids(
    tree: list[dict[str, Any]], counter: int = 0
) -> int:
    """Assign sequential ``node_id`` values ('0001', '0002', …)."""
    for node in tree:
        node["node_id"] = str(counter).zfill(4)
        counter += 1
        if node.get("nodes"):
            counter = _write_node_ids(node["nodes"], counter)
    return counter


def _add_node_text(
    tree: list[dict[str, Any]],
    page_list: list[tuple[str, int]],
) -> None:
    """Populate each node's ``text`` from its page range."""
    for node in tree:
        s = node.get("start_index", 1) or 1
        e = node.get("end_index", s) or s
        parts: list[str] = []
        for pi in range(s, e + 1):
            idx = pi - 1  # 1-based → 0-based
            if 0 <= idx < len(page_list):
                parts.append(page_list[idx][0])
        node["text"] = "\n".join(parts)
        if node.get("nodes"):
            _add_node_text(node["nodes"], page_list)


def _generate_node_summary(
    node: dict[str, Any], llm_call: LLMCallFn
) -> str:
    """Generate a concise summary for one tree node."""
    text = node.get("text", "")
    if not text.strip():
        return node.get("title", "")
    prompt = (
        "You are given a part of a document.  Generate a concise description "
        "of what this section covers and its main points.\n\n"
        f"Partial Document Text: {text[:6000]}\n\n"
        "Directly return the description, do not include any other text."
    )
    try:
        return llm_call(prompt).strip()
    except Exception:
        return text[:200] + "..."


def _generate_summaries(
    tree: list[dict[str, Any]], llm_call: LLMCallFn
) -> None:
    """Walk the tree and generate summaries for every node."""
    for node in tree:
        node["summary"] = _generate_node_summary(node, llm_call)
        if node.get("nodes"):
            _generate_summaries(node["nodes"], llm_call)


def _generate_doc_description(
    tree: list[dict[str, Any]], llm_call: LLMCallFn
) -> str:
    """Generate a one-sentence description of the whole document."""

    def _mini(nodes: list) -> list:
        out: list[dict[str, Any]] = []
        for n in nodes:
            d: dict[str, Any] = {"title": n.get("title", "")}
            if "summary" in n:
                d["summary"] = n["summary"][:100]
            if n.get("nodes"):
                d["nodes"] = _mini(n["nodes"])
            out.append(d)
        return out

    clean = _mini(tree)
    prompt = (
        "You are an expert in generating descriptions for a document.\n"
        "Generate a one-sentence description that distinguishes this "
        "document from others.\n\n"
        f"Document Structure: {json.dumps(clean, indent=2)[:4000]}\n\n"
        "Directly return the description, do not include any other text."
    )
    try:
        return llm_call(prompt).strip()
    except Exception:
        return f"Document about: {tree[0].get('title', 'unknown')}" if tree else "Document"


# ═══════════════════════════════════════════════════════════════════════════
# Large-node splitting  (from PageIndex process_large_node_recursively)
# ═══════════════════════════════════════════════════════════════════════════

def _split_large_nodes(
    tree: list[dict[str, Any]],
    page_list: list[tuple[str, int]],
    llm_call: LLMCallFn,
    max_pages: int = MAX_PAGE_NUM_EACH_NODE,
    max_chars: int = MAX_TOKEN_CHARS_EACH_NODE,
) -> None:
    """Recursively subdivide tree nodes that span too many pages."""
    for node in tree:
        s = node.get("start_index")
        e = node.get("end_index")
        if s is None or e is None:
            continue

        span = e - s + 1
        chars = sum(
            page_list[i][1]
            for i in range(s - 1, min(e, len(page_list)))
            if 0 <= i < len(page_list)
        )

        if span > max_pages and chars > max_chars and not node.get("nodes"):
            sub_pages = page_list[s - 1 : e]
            if sub_pages:
                sub_toc = _generate_toc_from_text(sub_pages, llm_call, start_index=s)
                sub_toc = [t for t in sub_toc if t.get("physical_index") is not None]
                if len(sub_toc) > 1:
                    sub_tree = _post_processing(sub_toc, e)
                    if sub_tree:
                        # Avoid duplicating the parent title
                        if (
                            sub_tree
                            and sub_tree[0].get("title", "").strip()
                            == node.get("title", "").strip()
                        ):
                            node["nodes"] = sub_tree[1:] if len(sub_tree) > 1 else sub_tree
                        else:
                            node["nodes"] = sub_tree

        if node.get("nodes"):
            _split_large_nodes(node["nodes"], page_list, llm_call, max_pages, max_chars)


# ═══════════════════════════════════════════════════════════════════════════
# Markdown tree builder  (from PageIndex page_index_md.py)
# ═══════════════════════════════════════════════════════════════════════════

def _build_markdown_tree(
    sections: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Build a nested tree from flat header-level sections."""
    if not sections:
        return []

    stack: list[tuple[dict[str, Any], int]] = []
    roots: list[dict[str, Any]] = []

    for sec in sections:
        level = sec["level"]
        node: dict[str, Any] = {
            "title": sec["title"],
            "text": sec.get("text", ""),
            "line_num": sec.get("line_num", 0),
            "nodes": [],
        }
        while stack and stack[-1][1] >= level:
            stack.pop()
        if not stack:
            roots.append(node)
        else:
            stack[-1][0]["nodes"].append(node)
        stack.append((node, level))

    return roots


# ═══════════════════════════════════════════════════════════════════════════
# Helper utilities
# ═══════════════════════════════════════════════════════════════════════════

def _flatten_tree(tree: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten a nested tree into a list of every node."""
    out: list[dict[str, Any]] = []
    for n in tree:
        out.append(n)
        if n.get("nodes"):
            out.extend(_flatten_tree(n["nodes"]))
    return out


def _clean_tree_for_storage(
    tree: list[dict[str, Any]], *, keep_text: bool = False
) -> list[dict[str, Any]]:
    """Strip internal/temporary fields before persisting."""
    cleaned: list[dict[str, Any]] = []
    for node in tree:
        c: dict[str, Any] = {"title": node.get("title", ""), "node_id": node.get("node_id", "")}
        for key in ("start_index", "end_index", "line_num", "summary"):
            if key in node:
                c[key] = node[key]
        if keep_text and "text" in node:
            c["text"] = node["text"]
        if node.get("nodes"):
            c["nodes"] = _clean_tree_for_storage(node["nodes"], keep_text=keep_text)
        cleaned.append(c)
    return cleaned


def _parse_nav_response(response: str, max_index: int) -> list[int]:
    """Parse '1,3,5' → [0, 2, 4] (0-indexed, deduplicated)."""
    indices: list[int] = []
    for tok in re.findall(r"\d+", response):
        idx = int(tok) - 1
        if 0 <= idx < max_index and idx not in indices:
            indices.append(idx)
    if not indices:
        indices = list(range(min(3, max_index)))
    return indices


# ═══════════════════════════════════════════════════════════════════════════
# DocumentIndex  (the serialisable artefact for one document)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class DocumentIndex:
    """The complete PageIndex for a single ingested document."""

    doc_id: str
    doc_name: str
    doc_description: str
    source_path: str
    doc_type: str  # "pdf", "markdown", "text"
    total_pages: int | None
    structure: list[dict[str, Any]]  # the tree
    created_at: float = field(default_factory=time.time)
    llm_calls_used: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "doc_name": self.doc_name,
            "doc_description": self.doc_description,
            "source_path": self.source_path,
            "doc_type": self.doc_type,
            "total_pages": self.total_pages,
            "structure": self.structure,
            "created_at": self.created_at,
            "llm_calls_used": self.llm_calls_used,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DocumentIndex:
        return cls(
            doc_id=d["doc_id"],
            doc_name=d.get("doc_name", ""),
            doc_description=d.get("doc_description", ""),
            source_path=d.get("source_path", ""),
            doc_type=d.get("doc_type", "unknown"),
            total_pages=d.get("total_pages"),
            structure=d.get("structure", []),
            created_at=d.get("created_at", 0.0),
            llm_calls_used=d.get("llm_calls_used", 0),
        )

    @property
    def node_count(self) -> int:
        return len(_flatten_tree(self.structure))


# ═══════════════════════════════════════════════════════════════════════════
# PageIndexStore — the main Tier 4 public interface
# ═══════════════════════════════════════════════════════════════════════════

class PageIndexStore:
    """
    Tier 4: PageIndex-powered hierarchical document index.

    Faithfully adapts the VectifyAI/PageIndex architecture:
      - PDF  → TOC extraction → page-indexed tree → LLM summaries
      - Markdown → header parsing → tree → LLM summaries
      - Text → LLM-generated TOC → tree → LLM summaries

    Stores indices in ``.cvc/pageindex/`` as Zstandard-compressed JSON.
    Uses the agent's existing LLM — no extra API key needed.

    **CLI agent only** — proxy / MCP never use this.
    """

    def __init__(self, persist_dir: Path) -> None:
        self._root = persist_dir
        self._root.mkdir(parents=True, exist_ok=True)
        self._cctx = zstd.ZstdCompressor(level=_ZSTD_LEVEL)
        self._dctx = zstd.ZstdDecompressor()

        self._cache: dict[str, DocumentIndex] = {}
        self._manifest_path = self._root / "manifest.json"
        self._manifest: dict[str, dict[str, Any]] = self._load_manifest()

    # ── Public API ────────────────────────────────────────────────────

    def ingest(
        self,
        file_path: Path,
        llm_call: LLMCallFn,
        *,
        progress_callback: Callable[[str], None] | None = None,
    ) -> DocumentIndex:
        """
        Ingest a document using the real PageIndex architecture.

        Pipeline
        --------
        PDF:      extract pages → detect TOC → build page-indexed tree → summarise
        Markdown: parse ``#`` headers → build tree → summarise
        Text:     LLM-generate TOC → build tree → summarise
        """

        def _progress(msg: str) -> None:
            if progress_callback:
                progress_callback(msg)
            logger.info(msg)

        file_path = Path(file_path).resolve()
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        # Wrap LLM call to count invocations
        call_count = [0]

        def counted(prompt: str) -> str:
            call_count[0] += 1
            return llm_call(prompt)

        # Content-hash for deduplication
        raw = file_path.read_bytes()
        doc_id = hashlib.sha256(raw).hexdigest()

        if doc_id in self._manifest:
            existing = self._load_index(doc_id)
            if existing:
                _progress(f"Document already indexed (hash: {doc_id[:12]}...)")
                return existing

        # Dispatch to the correct pipeline
        if suffix == ".pdf":
            doc_index = self._ingest_pdf(file_path, doc_id, counted, _progress)
        elif suffix in (".md", ".markdown"):
            doc_index = self._ingest_markdown(file_path, doc_id, counted, _progress)
        else:
            doc_index = self._ingest_text(file_path, doc_id, counted, _progress)

        doc_index.llm_calls_used = call_count[0]

        # Persist
        self._save_index(doc_index)
        self._cache[doc_id] = doc_index

        _progress(
            f"Indexed '{file_path.name}': {doc_index.node_count} tree nodes, "
            f"{doc_index.total_pages or 'N/A'} pages, "
            f"{call_count[0]} LLM calls"
        )
        return doc_index

    # ── PDF pipeline ─────────────────────────────────────────────────

    def _ingest_pdf(
        self,
        file_path: Path,
        doc_id: str,
        llm_call: LLMCallFn,
        progress: Callable[[str], None],
    ) -> DocumentIndex:
        progress(f"Extracting pages from {file_path.name}...")
        page_list = _extract_pdf_pages(file_path)
        total_pages = len(page_list)
        progress(f"Extracted {total_pages} pages")

        # ── Step 1: detect TOC ──────────────────────────────────────
        progress("Detecting table of contents...")
        toc_pages = _find_toc_pages(page_list, llm_call)

        if toc_pages:
            progress(f"TOC found on page(s): {[p + 1 for p in toc_pages]}")
            toc_info = _toc_extractor(page_list, toc_pages, llm_call)
            toc_structured = self._process_toc(
                toc_info, toc_pages, page_list, total_pages, llm_call, progress
            )
        else:
            progress("No TOC found — generating structure from content...")
            toc_structured = _generate_toc_from_text(page_list, llm_call)
            toc_structured = [t for t in toc_structured if t.get("physical_index") is not None]

        if not toc_structured:
            toc_structured = [{"structure": "1", "title": file_path.stem, "physical_index": 1}]

        toc_structured = _add_preface_if_needed(toc_structured)

        # ── Step 2: build tree ──────────────────────────────────────
        progress("Building hierarchical tree...")
        tree = _post_processing(toc_structured, total_pages)

        # ── Step 3: split large nodes ───────────────────────────────
        progress("Splitting large nodes...")
        _split_large_nodes(tree, page_list, llm_call)

        # ── Step 4: enrich ──────────────────────────────────────────
        _write_node_ids(tree)
        _add_node_text(tree, page_list)
        progress("Generating node summaries...")
        _generate_summaries(tree, llm_call)

        progress("Generating document description...")
        doc_description = _generate_doc_description(tree, llm_call)

        storage = _clean_tree_for_storage(tree, keep_text=True)

        return DocumentIndex(
            doc_id=doc_id,
            doc_name=file_path.name,
            doc_description=doc_description,
            source_path=str(file_path),
            doc_type="pdf",
            total_pages=total_pages,
            structure=storage,
        )

    def _process_toc(
        self,
        toc_info: dict[str, Any],
        toc_pages: list[int],
        page_list: list[tuple[str, int]],
        total_pages: int,
        llm_call: LLMCallFn,
        progress: Callable[[str], None],
    ) -> list[dict[str, Any]]:
        """Shared logic for TOC-with-page-numbers and TOC-without-page-numbers."""
        toc_content = toc_info["toc_content"]
        has_pi = toc_info["page_index_given_in_toc"]

        progress("Transforming TOC to structured format...")
        toc_structured = _toc_transformer(toc_content, llm_call)

        if has_pi == "yes" and toc_structured:
            progress("TOC has page numbers — mapping to physical indices...")
            start_page = toc_pages[-1] + 2  # first page after TOC

            # Build a sample of tagged page text for the LLM
            sample_end = min(start_page + TOC_CHECK_PAGE_NUM, total_pages)
            sample_text = ""
            for pi in range(start_page, sample_end + 1):
                idx = pi - 1
                if 0 <= idx < len(page_list):
                    sample_text += (
                        f"<physical_index_{pi}>\n"
                        f"{page_list[idx][0]}\n"
                        f"<physical_index_{pi}>\n\n"
                    )

            toc_no_pages = [
                {k: v for k, v in it.items() if k != "page"}
                for it in toc_structured[:10]
            ]

            prompt = (
                "You are given a table of contents in JSON and several document "
                "pages.  Add the physical_index to the sections.\n\n"
                "The text has <physical_index_X> tags for page X.\n\n"
                "Response format:\n"
                '[{"structure":"...","title":"...","physical_index":"<physical_index_X>"},…]\n'
                "Only add physical_index to sections found in the pages.\n"
                "Directly return the final JSON. Do not output anything else.\n\n"
                f"Table of contents:\n{json.dumps(toc_no_pages, indent=2)}\n\n"
                f"Document pages:\n{sample_text[:8000]}"
            )
            mapping_raw = _extract_json(llm_call(prompt))

            if isinstance(mapping_raw, list):
                mapping = _convert_physical_index_to_int(mapping_raw)
                pairs = []
                for pm in mapping:
                    for ts in toc_structured:
                        if (
                            pm.get("title") == ts.get("title")
                            and pm.get("physical_index")
                            and ts.get("page")
                        ):
                            pairs.append(
                                {"page": ts["page"], "physical_index": pm["physical_index"]}
                            )
                if pairs:
                    diffs = [p["physical_index"] - p["page"] for p in pairs]
                    offset = Counter(diffs).most_common(1)[0][0]
                    progress(f"Page offset: {offset}")
                    for it in toc_structured:
                        if it.get("page") is not None and isinstance(it["page"], int):
                            it["physical_index"] = it["page"] + offset
                        it.pop("page", None)
                else:
                    for it in toc_structured:
                        it["physical_index"] = it.pop("page", None)
            else:
                for it in toc_structured:
                    it["physical_index"] = it.pop("page", None)

        else:
            progress("TOC without page numbers — locating sections...")
            groups = _page_list_to_groups(page_list, start_index=1)
            for group in groups:
                toc_structured = _add_page_number_to_toc(group, toc_structured, llm_call)
            toc_structured = _convert_physical_index_to_int(toc_structured)

        return [t for t in toc_structured if t.get("physical_index") is not None]

    # ── Markdown pipeline ────────────────────────────────────────────

    def _ingest_markdown(
        self,
        file_path: Path,
        doc_id: str,
        llm_call: LLMCallFn,
        progress: Callable[[str], None],
    ) -> DocumentIndex:
        progress(f"Parsing markdown structure from {file_path.name}...")
        sections = _extract_markdown_sections(file_path)

        if not sections:
            return self._ingest_text(file_path, doc_id, llm_call, progress)

        progress(f"Found {len(sections)} header sections")
        tree = _build_markdown_tree(sections)
        _write_node_ids(tree)

        progress("Generating node summaries...")
        _generate_summaries(tree, llm_call)

        progress("Generating document description...")
        doc_description = _generate_doc_description(tree, llm_call)

        storage = _clean_tree_for_storage(tree, keep_text=True)

        return DocumentIndex(
            doc_id=doc_id,
            doc_name=file_path.name,
            doc_description=doc_description,
            source_path=str(file_path),
            doc_type="markdown",
            total_pages=None,
            structure=storage,
        )

    # ── Plain-text pipeline ──────────────────────────────────────────

    def _ingest_text(
        self,
        file_path: Path,
        doc_id: str,
        llm_call: LLMCallFn,
        progress: Callable[[str], None],
    ) -> DocumentIndex:
        progress(f"Reading {file_path.name}...")
        text = file_path.read_text(encoding="utf-8", errors="replace")
        if not text.strip():
            raise ValueError(f"No text in {file_path.name}")

        page_list = _text_to_pseudo_pages(text)
        progress(f"Split into {len(page_list)} pseudo-pages")

        progress("Generating document structure with LLM...")
        toc = _generate_toc_from_text(page_list, llm_call)
        toc = [t for t in toc if t.get("physical_index") is not None]
        if not toc:
            toc = [{"structure": "1", "title": file_path.stem, "physical_index": 1}]

        toc = _add_preface_if_needed(toc)
        tree = _post_processing(toc, len(page_list))
        _write_node_ids(tree)
        _add_node_text(tree, page_list)

        progress("Generating summaries...")
        _generate_summaries(tree, llm_call)

        doc_description = _generate_doc_description(tree, llm_call)
        storage = _clean_tree_for_storage(tree, keep_text=True)

        return DocumentIndex(
            doc_id=doc_id,
            doc_name=file_path.name,
            doc_description=doc_description,
            source_path=str(file_path),
            doc_type="text",
            total_pages=None,
            structure=storage,
        )

    # ── Search ───────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        llm_call: LLMCallFn,
        *,
        doc_id: str | None = None,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Search indexed documents using LLM-guided tree navigation.

        The LLM reads node summaries at each level and selects the most
        relevant branches, recursing down until it reaches leaf nodes.
        """
        results: list[dict[str, Any]] = []

        if doc_id:
            full = self._resolve_doc_id(doc_id)
            targets = [full] if full else []
        else:
            targets = list(self._manifest.keys())

        for did in targets:
            idx = self._load_index(did)
            if idx is None:
                continue
            results.extend(self._navigate_tree(idx, query, llm_call, max_results))

        return results[:max_results]

    def _navigate_tree(
        self,
        doc: DocumentIndex,
        query: str,
        llm_call: LLMCallFn,
        max_results: int,
    ) -> list[dict[str, Any]]:
        """Top-down tree navigation guided by LLM reasoning."""
        if not doc.structure:
            return []

        candidates = doc.structure
        depth = 0

        while depth < 5:
            if not candidates:
                break
            all_leaves = all(not c.get("nodes") for c in candidates)
            if all_leaves:
                break

            parts = []
            for i, n in enumerate(candidates):
                summary = n.get("summary", n.get("title", ""))
                title = n.get("title", f"Section {i + 1}")
                parts.append(f"{i + 1}. [{title}] {summary[:200]}")

            prompt = (
                "You are searching a hierarchical document index.\n\n"
                f"User query: {query}\n\n"
                "Below are sections at the current level.  Return the numbers of "
                "sections most likely to contain the answer, separated by commas.  "
                "Return ONLY the numbers (e.g. '1,3').\n\n"
                + "\n".join(parts)
            )
            try:
                selected = _parse_nav_response(llm_call(prompt).strip(), len(candidates))
            except Exception:
                selected = list(range(min(3, len(candidates))))

            nxt: list[dict[str, Any]] = []
            for idx in selected:
                if 0 <= idx < len(candidates):
                    node = candidates[idx]
                    children = node.get("nodes", [])
                    nxt.extend(children if children else [node])

            if not nxt:
                break
            if all(not c.get("nodes") for c in nxt):
                candidates = nxt
                break
            candidates = nxt
            depth += 1

        results: list[dict[str, Any]] = []
        for node in candidates[:max_results]:
            results.append({
                "doc_id": doc.doc_id,
                "doc_id_short": doc.doc_id[:12],
                "filename": doc.doc_name,
                "node_id": node.get("node_id", ""),
                "title": node.get("title", ""),
                "text": node.get("text", ""),
                "summary": node.get("summary", ""),
                "start_index": node.get("start_index"),
                "end_index": node.get("end_index"),
                "line_num": node.get("line_num"),
                "nav_depth": depth,
                "relevance_path": f"tree navigation -> depth {depth}",
            })
        return results

    # ── Listing & stats ──────────────────────────────────────────────

    def list_documents(self) -> list[dict[str, Any]]:
        """List all indexed documents."""
        return [
            {
                "doc_id": doc_id,
                "doc_id_short": doc_id[:12],
                "filename": m.get("doc_name", m.get("filename", "unknown")),
                "source_path": m.get("source_path", ""),
                "doc_type": m.get("doc_type", "unknown"),
                "total_pages": m.get("total_pages"),
                "node_count": m.get("node_count", 0),
                "doc_description": m.get("doc_description", ""),
                "created_at": m.get("created_at", 0.0),
            }
            for doc_id, m in self._manifest.items()
        ]

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document index by its ID (or short prefix)."""
        full = self._resolve_doc_id(doc_id)
        if full is None:
            return False
        (self._root / f"{full}.zst").unlink(missing_ok=True)
        self._manifest.pop(full, None)
        self._cache.pop(full, None)
        self._save_manifest()
        logger.info("Removed document index: %s", full[:12])
        return True

    def get_stats(self) -> dict[str, Any]:
        """Aggregate statistics about the PageIndex store."""
        total_docs = len(self._manifest)
        total_pages = sum(m.get("total_pages", 0) or 0 for m in self._manifest.values())
        total_nodes = sum(m.get("node_count", 0) for m in self._manifest.values())
        disk = sum(f.stat().st_size for f in self._root.iterdir() if f.is_file())
        return {
            "total_documents": total_docs,
            "total_nodes": total_nodes,
            "total_pages": total_pages,
            "disk_usage_bytes": disk,
            "disk_usage_mb": round(disk / (1024 * 1024), 2),
        }

    # ── Persistence ──────────────────────────────────────────────────

    def _save_index(self, doc: DocumentIndex) -> None:
        data = json.dumps(doc.to_dict(), separators=(",", ":"), default=str)
        compressed = self._cctx.compress(data.encode("utf-8"))
        (self._root / f"{doc.doc_id}.zst").write_bytes(compressed)

        self._manifest[doc.doc_id] = {
            "doc_name": doc.doc_name,
            "source_path": doc.source_path,
            "doc_type": doc.doc_type,
            "total_pages": doc.total_pages,
            "node_count": doc.node_count,
            "doc_description": doc.doc_description,
            "created_at": doc.created_at,
        }
        self._save_manifest()

    def _load_index(self, doc_id: str) -> DocumentIndex | None:
        if doc_id in self._cache:
            return self._cache[doc_id]
        path = self._root / f"{doc_id}.zst"
        if not path.exists():
            return None
        try:
            data = json.loads(self._dctx.decompress(path.read_bytes()).decode("utf-8"))
            idx = DocumentIndex.from_dict(data)
            self._cache[doc_id] = idx
            return idx
        except Exception as exc:
            logger.error("Failed to load index %s: %s", doc_id[:12], exc)
            return None

    def _load_manifest(self) -> dict[str, dict[str, Any]]:
        if not self._manifest_path.exists():
            return {}
        try:
            return json.loads(self._manifest_path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_manifest(self) -> None:
        self._manifest_path.write_text(
            json.dumps(self._manifest, indent=2, default=str), encoding="utf-8"
        )

    def _resolve_doc_id(self, prefix: str) -> str | None:
        if prefix in self._manifest:
            return prefix
        hits = [d for d in self._manifest if d.startswith(prefix)]
        return hits[0] if len(hits) == 1 else None
