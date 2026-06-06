"""Knowledge extraction helpers for workflow phase completion.

Handles two extraction scenarios:
1. After retrospective phase: import entries from knowledge_extracted.json
2. Quick mode archive: lightweight extraction from pitfalls/decisions files
"""

from __future__ import annotations

import json as _json

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.types import Phase


def clip_evidence(text: str, section_title: str = "", max_length: int = 1000) -> str:
    """Deterministically clip evidence text from execution artifacts. (#529)

    Splits by ## headings, finds the matching section, clips to max_length.
    Falls back to full text truncation when no headings found.
    """
    if not text or max_length <= 0:
        return ""
    if len(text) <= max_length:
        return text
    # Try section-based clipping
    if "\n## " in text:
        sections = text.split("\n## ")
        target = section_title.lower().lstrip("#").strip() if section_title else ""
        for sec in sections:
            heading = sec.split("\n", 1)[0].lower().strip()
            if target and target in heading:
                clipped = _clip_to_boundary(sec, max_length)
                return clipped
        # No matching section — use first section
        clipped = _clip_to_boundary(sections[0], max_length)
        return clipped
    # No headings — truncate full text
    return _clip_to_boundary(text, max_length)


def _clip_to_boundary(text: str, max_length: int) -> str:
    """Clip text to max_length at sentence/line boundary."""
    if len(text) <= max_length:
        return text
    # Try sentence boundary (。or \n)
    for boundary in ("。", "\n", "；", ". "):
        pos = text.rfind(boundary, 0, max_length)
        if pos > max_length // 2:
            return text[:pos + len(boundary)].rstrip()
    # No good boundary — hard clip with ellipsis
    return text[:max_length - 3].rstrip() + "..."


def extract_knowledge(task, fs: Filesystem) -> dict:
    """Extract and import knowledge entries after retrospective or in quick-mode archive."""
    knowledge_result: dict = {}

    # After retrospective: import from knowledge_extracted.json
    if task.phase == Phase.RETROSPECTIVE:
        knowledge_result = _import_retrospective_knowledge(task, fs)

    # Quick mode: lightweight knowledge extraction during archive
    if (getattr(task, 'mode', '') == 'quick'
            and task.phase == Phase.ARCHIVE
            and not knowledge_result):
        knowledge_result = _extract_quick_archive_knowledge(task, fs)

    return knowledge_result


def _import_retrospective_knowledge(task, fs: Filesystem) -> dict:
    """Import knowledge entries from knowledge_extracted.json after retrospective."""
    from kanban_framework.domain.knowledge import KnowledgeManager
    km = KnowledgeManager(fs)
    try:
        task_dir = fs.task_dir(task.id)
        iter_dir = task_dir / f"iteration-{task.iteration}"
        biz_tag = getattr(task, 'biz_tag', None)
        ke_file = iter_dir / "knowledge_extracted.json"
        if not ke_file.exists():
            ke_file = task_dir / "knowledge_extracted.json"
        if ke_file.exists():
            try:
                data = _json.loads(ke_file.read_text(encoding="utf-8"))
                entries = data.get("entries", data.get("items", []))
                added = []
                skipped = 0
                for e in entries:
                    title = e.get("title", "")
                    content = e.get("content", "")
                    if not title.strip() and not content.strip():
                        skipped += 1
                        continue
                    entry = km.add_entry(
                        domain=e.get("domain", "infra"),
                        category=e.get("category", "general"),
                        title=title,
                        content=content,
                        tags=e.get("tags", []),
                        severity=e.get("severity", "medium"),
                        source=e.get("source", {}),
                        biz_context=biz_tag,
                        status="pending",
                    )
                    added.append(entry["id"])
                result = {"knowledge_imported": len(added), "knowledge_ids": added,
                          "knowledge_status": "pending",
                          "knowledge_review_hint": "自动提取的知识条目需要人工审核，使用 kanban knowledge pending 查看待审核条目，kanban knowledge approve <id> 批准入库"}
                if skipped:
                    result["knowledge_skipped_empty"] = skipped
                return result
            except Exception as exc:
                return {"knowledge_imported": 0, "knowledge_warning": f"import failed: {exc}"}
        return {"knowledge_imported": 0, "knowledge_warning": "no knowledge_extracted.json found"}
    finally:
        km._conn.close()


def _extract_quick_archive_knowledge(task, fs: Filesystem) -> dict:
    """Lightweight knowledge extraction during archive in quick mode."""
    from kanban_framework.domain.knowledge import KnowledgeManager
    km = KnowledgeManager(fs)
    try:
        task_dir = fs.task_dir(task.id)
        iter_dir = task_dir / f"iteration-{task.iteration}"
        biz_tag = getattr(task, 'biz_tag', None)
        _quick_sources = [
            (iter_dir / "execution_pitfalls.md", "踩坑"),
            (iter_dir / "execution_decisions.md", "最佳实践"),
            (task_dir / "execution_pitfalls.md", "踩坑"),
            (task_dir / "execution_decisions.md", "最佳实践"),
        ]
        _quick_added = []
        for _src_path, _category in _quick_sources:
            if not _src_path.is_file() or _src_path.stat().st_size == 0:
                continue
            try:
                _text = _src_path.read_text(encoding="utf-8").strip()
            except Exception:
                continue
            if len(_text) < 20:
                continue
            _sections = _text.split('\n## ')
            for _sec in _sections:
                _sec = _sec.strip()
                if not _sec or len(_sec) < 20:
                    continue
                _lines = _sec.split('\n', 1)
                _title = _lines[0].lstrip('#').strip()[:100]
                _content = _lines[1].strip() if len(_lines) > 1 else _sec
                if not _title:
                    _title = _content[:60] + "..."
                _existing = km.search(_title, limit=3)
                if any(_title.lower() in e.get("title", "").lower()
                       for e in _existing):
                    continue
                _evidence = clip_evidence(_text, _title, max_length=1000)
                _entry = km.add_entry(
                    domain="infra",
                    category=_category,
                    title=_title,
                    content=_content[:3000],
                    tags=["quick-mode", "auto-extracted"],
                    severity="medium",
                    source={"task_id": task.id, "source_file": _src_path.name,
                            "extraction_mode": "quick_archive",
                            "section_title": _title},
                    biz_context=biz_tag,
                    status="pending",
                    evidence=_evidence or None,
                )
                if not _entry.get("skipped"):
                    _quick_added.append(_entry["id"])
        return {
            "knowledge_imported": len(_quick_added),
            "knowledge_ids": _quick_added,
            "knowledge_status": "pending",
            "knowledge_review_hint": "自动提取的知识条目需要人工审核，使用 kanban knowledge pending 查看待审核条目，kanban knowledge approve <id> 批准入库",
            "extraction_mode": "quick_archive",
        }
    finally:
        km._conn.close()
