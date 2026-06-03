"""Knowledge extraction helpers for workflow phase completion.

Handles two extraction scenarios:
1. After retrospective phase: import entries from knowledge_extracted.json
2. Quick mode archive: lightweight extraction from pitfalls/decisions files
"""

from __future__ import annotations

import json as _json

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.types import Phase


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
    task_dir = fs.task_dir(task.id)
    iter_dir = task_dir / f"iteration-{task.iteration}"
    biz_tag = getattr(task, 'biz_tag', None)
    # Agent may write to iter_dir or task_dir depending on prompt interpretation
    ke_file = iter_dir / "knowledge_extracted.json"
    if not ke_file.exists():
        ke_file = task_dir / "knowledge_extracted.json"
    if ke_file.exists():
        try:
            data = _json.loads(ke_file.read_text(encoding="utf-8"))
            entries = data.get("entries", [])
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
                )
                added.append(entry["id"])
            result = {"knowledge_imported": len(added), "knowledge_ids": added}
            if skipped:
                result["knowledge_skipped_empty"] = skipped
            return result
        except Exception as exc:
            return {"knowledge_imported": 0, "knowledge_warning": f"import failed: {exc}"}
    return {"knowledge_imported": 0, "knowledge_warning": "no knowledge_extracted.json found"}


def _extract_quick_archive_knowledge(task, fs: Filesystem) -> dict:
    """Lightweight knowledge extraction during archive in quick mode."""
    from kanban_framework.domain.knowledge import KnowledgeManager
    km = KnowledgeManager(fs)
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
            _entry = km.add_entry(
                domain="infra",
                category=_category,
                title=_title,
                content=_content[:3000],
                tags=["quick-mode", "auto-extracted"],
                severity="medium",
                source={"task_id": task.id, "source_file": _src_path.name,
                        "extraction_mode": "quick_archive"},
                biz_context=biz_tag,
            )
            if not _entry.get("skipped"):
                _quick_added.append(_entry["id"])
    return {
        "knowledge_imported": len(_quick_added),
        "knowledge_ids": _quick_added,
        "extraction_mode": "quick_archive",
    }
