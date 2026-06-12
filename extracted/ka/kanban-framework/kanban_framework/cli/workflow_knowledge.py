"""Knowledge extraction helpers for workflow phase completion.

Handles two extraction scenarios:
1. After retrospective phase: import entries from knowledge_extracted.json
2. Archive fallback: auto-extract from pitfalls/decisions files

The archive fallback runs for ALL modes by default unless explicitly
disabled via gates.knowledge_extraction: false in mode config.
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


def _is_gate_disabled(task, fs: Filesystem, gate_name: str) -> bool:
    """Check if a named gate is disabled for the task's mode.

    Follows the same priority as brainstorming gate:
    1. modes.<mode>.gates.<gate_name>: false
    2. gates.<gate_name>.enabled: false
    3. .kanban/workflows/<mode>.json gates.<gate_name>: false
    """
    from kanban_framework.infra.config import Config
    cfg = Config(fs)
    workflow = cfg.workflow
    mode = getattr(task, 'mode', None)

    if workflow and isinstance(workflow, dict):
        if mode:
            modes_cfg = workflow.get("modes", {})
            mode_cfg = modes_cfg.get(mode, {}) if isinstance(modes_cfg, dict) else {}
            mode_gates = mode_cfg.get("gates", {}) if isinstance(mode_cfg, dict) else {}
            if isinstance(mode_gates, dict) and mode_gates.get(gate_name) is False:
                return True
        top_gates = workflow.get("gates", {})
        if isinstance(top_gates, dict) and top_gates.get(gate_name, {}).get("enabled") is False:
            return True

    if mode:
        try:
            wf_file = fs.kanban_dir / "workflows" / f"{mode}.json"
            if wf_file.is_file():
                mode_data = _json.loads(wf_file.read_text(encoding="utf-8"))
                g = mode_data.get("gates", {})
                if isinstance(g, dict) and g.get(gate_name) is False:
                    return True
        except Exception:
            pass

    return False


def extract_knowledge(task, fs: Filesystem) -> dict:
    """Extract and import knowledge entries.

    Two paths:
    1. After retrospective phase: import from knowledge_extracted.json
    2. Archive fallback: auto-extract from pitfalls/decisions (all modes)

    The archive fallback is ON by default. Disable per-mode via:
      gates.knowledge_extraction: false
    """
    knowledge_result: dict = {}

    # After retrospective: import from knowledge_extracted.json
    if task.phase == Phase.RETROSPECTIVE:
        knowledge_result = _import_retrospective_knowledge(task, fs)

    # Archive fallback: auto-extract unless disabled via gate
    if task.phase == Phase.ARCHIVE and not knowledge_result:
        if not _is_gate_disabled(task, fs, "knowledge_extraction"):
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
            (iter_dir / "execute" / "execution_pitfalls.md", "踩坑"),
            (iter_dir / "execute" / "execution_decisions.md", "最佳实践"),
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
        result = {
            "knowledge_imported": len(_quick_added),
            "knowledge_ids": _quick_added,
            "knowledge_status": "pending",
            "knowledge_review_hint": "自动提取的知识条目需要人工审核，使用 kanban knowledge pending 查看待审核条目，kanban knowledge approve <id> 批准入库",
            "extraction_mode": "quick_archive",
        }
        if not _quick_added:
            _existing = sum(1 for e in km.list_entries()
                           if e.get("source", {}).get("task_id") == task.id)
            result["knowledge_info"] = (
                f"0 new entries extracted during archive. "
                f"{_existing} entries already imported from previous phase."
                if _existing else
                "No knowledge artifacts found in execution summary."
            )
            result["knowledge_status"] = "no_new_entries"
        return result
    finally:
        km._conn.close()
