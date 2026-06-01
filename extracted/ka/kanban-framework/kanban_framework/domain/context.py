"""Knowledge retrieval and context building for agent spawn prompts.

Handles auto-knowledge search, prompt hook resolution, and worker context
construction — all separated from the core state machine orchestration.
"""
from __future__ import annotations

import json

from kanban_framework.types import Task
from kanban_framework.infra.config import Config
from kanban_framework.infra.filesystem import Filesystem


def _is_knowledge_available(fs: Filesystem) -> bool:
    """Check if knowledge base has any entries (#216 cold start)."""
    try:
        scope = _get_scope(fs)
        db_name = f"knowledge-{scope}.db" if scope else "knowledge.db"
        db = fs.kanban_dir / "knowledge" / db_name
        if not db.is_file():
            return False
        import sqlite3
        conn = sqlite3.connect(str(db))
        row = conn.execute("SELECT COUNT(*) FROM entries WHERE status='active'").fetchone()
        conn.close()
        return row is not None and row[0] > 0
    except Exception:
        return False


def _get_scope(fs: Filesystem) -> str:
    """Read knowledge.scope from config.json."""
    cfg_path = fs.config_file()
    if cfg_path.is_file():
        try:
            raw = json.loads(cfg_path.read_text(encoding="utf-8"))
            return raw.get("knowledge", {}).get("scope", "")
        except Exception:
            pass
    return ""


def _load_knowledge_summary(fs: Filesystem, task: Task) -> dict | None:
    """Load knowledge_used.json and return a lightweight summary for next-step output."""
    kf = fs.task_dir(task.id) / "plan" / "knowledge_used.json"
    if not kf.is_file():
        return None
    try:
        data = json.loads(kf.read_text(encoding="utf-8"))
        matched = data.get("matched", [])
        # Auto-record usage for knowledge entries matched during plan (#365)
        if matched:
            try:
                from kanban_framework.domain.knowledge import KnowledgeManager
                km = KnowledgeManager(fs)
                for m in matched:
                    eid = m.get("id", "")
                    if eid:
                        try:
                            km.record_usage(eid, task.id)
                        except Exception:
                            pass
            except Exception:
                pass
        return {
            "matched_count": len(matched),
            "top_matches": [
                {"id": m["id"], "title": m["title"], "relevance": m.get("relevance", ""),
                 "how_to_apply": m.get("how_to_apply", "")[:100]}
                for m in matched[:5]
            ],
            "no_match_reason": data.get("no_match_reason"),
        }
    except (json.JSONDecodeError, OSError):
        return None


# Hardcoded fallback for built-in steps (backward compat)
_LEGACY_KNOWLEDGE: dict[str, dict] = {
    "plan.plan_A":    {"max_results": 3, "categories": ["架构", "接口", "流程", "工具"],
                       "min_score": 0.15},
    "execute.spawn":  {"intent": "pitfall_check", "max_results": 3,
                       "categories": ["踩坑", "优化"], "severity": ["high", "medium"]},
}


def _auto_knowledge_retrieval(fs: Filesystem, task: Task, step_id: str,
                               step_knowledge: dict | None = None) -> list[dict]:
    """Auto-search knowledge base for a step.

    Priority:
      1. step.knowledge config from workflow.json (per-step)
      2. _LEGACY_KNOWLEDGE hardcoded defaults (built-in steps)
      3. No retrieval (other steps)
    """
    kcfg = step_knowledge if isinstance(step_knowledge, dict) and step_knowledge else \
           _LEGACY_KNOWLEDGE.get(step_id)
    if not kcfg:
        return []

    from kanban_framework.domain.knowledge import KnowledgeManager
    try:
        km = KnowledgeManager(fs)
        query = f"{task.title} {task.description}"
        max_results = kcfg.get("max_results", 3)
        intent = kcfg.get("intent")

        if intent:
            results = km.search_by_intent(intent, query, limit=max_results * 2)
        else:
            results = km.search_hybrid(query, limit=max_results * 2)

        # Apply filters from config
        categories = kcfg.get("categories")
        severity = kcfg.get("severity")
        min_score = kcfg.get("min_score", 0)
        results = [
            r for r in results
            if r.get("status", "active") == "active"
            and (not categories or r.get("category") in categories)
            and (not severity or r.get("severity") in severity)
            and float(r.get("score", 0)) >= min_score
        ]

        # Deduplicate by domain
        seen_domains = set()
        deduped = []
        for r in sorted(results, key=lambda r: float(r.get("score", 0)), reverse=True):
            dom = r.get("domain", "")
            if dom not in seen_domains:
                seen_domains.add(dom)
                deduped.append(r)

        final = deduped[:max_results]
        for r in final:
            try:
                km.record_usage(r["id"], task.id)
            except Exception:
                pass

        return [
            {"id": r["id"], "title": r.get("title", ""),
             "domain": r.get("domain", ""), "category": r.get("category", ""),
             "severity": r.get("severity", ""),
             "snippet": (r.get("content", "") or "")[:120]}
            for r in final
        ]
    except Exception as e:
        import sys as _sys
        print(f"[kanban] knowledge retrieval failed: {e}", file=_sys.stderr)
        return []


_CODEGRAPH_STEPS = frozenset((
    "plan.plan_A", "execute.spawn", "execute.pitfall_check",
))


def _build_codegraph_context(fs: Filesystem, task: Task, step_id: str) -> str:
    """Build codegraph context for agent spawn prompts. (#374)

    Checks if code_index backend is configured, then queries
    architecture/search/impact based on the current step.
    Returns structured text to inject into spawn_prompt.
    """
    if step_id not in _CODEGRAPH_STEPS:
        return ""

    from kanban_framework.infra.code_index_backend import (
        resolve_code_index_backend, CodeIndexNotAvailableError,
    )
    try:
        cfg = Config(fs)
        backend_name = cfg.code_index_backend
        if not backend_name:
            return ""
        backend = resolve_code_index_backend(backend_name)
    except (CodeIndexNotAvailableError, Exception):
        return ""

    repo_path = fs.root
    parts: list[str] = []

    if step_id == "plan.plan_A":
        _codegraph_plan_context(backend, repo_path, task, parts)
    elif step_id == "execute.spawn":
        _codegraph_execute_context(backend, repo_path, task, parts)
    elif step_id == "execute.pitfall_check":
        _codegraph_pitfall_context(backend, repo_path, task, parts)

    return "\n".join(parts) if parts else ""


def _codegraph_plan_context(backend, repo_path, task, parts: list) -> None:
    overview = backend.architecture_overview(repo_path)
    communities = overview.get("communities", [])
    if communities:
        parts.append("## 代码架构概览（codegraph）\n")
        for c in communities[:5]:
            parts.append(f"- **{c['name']}** (规模:{c['size']}, 内聚:{c.get('cohesion', 0)})")
    results = backend.search(task.title, repo_path, limit=5)
    if results:
        parts.append("\n## 任务相关代码节点\n")
        for r in results:
            parts.append(f"- `{r['name']}` ({r['kind']}) @ {r['file_path']}:{r.get('line_start', '')}")


def _codegraph_execute_context(backend, repo_path, task, parts: list) -> None:
    results = backend.search(task.title, repo_path, limit=8)
    if not results:
        return
    parts.append("## 相关代码节点（codegraph）\n")
    for r in results:
        parts.append(f"- `{r['name']}` ({r['kind']}) @ {r['file_path']}")
    files = list({r["file_path"] for r in results if r.get("file_path")})
    for f in files[:3]:
        impact = backend.impact_radius(f, repo_path, depth=1)
        affected = impact.get("affected_files", [])
        if affected:
            parts.append(f"\n### `{f}` 变更影响范围\n")
            parts.append(f"受影响文件: {', '.join(affected[:10])}")


def _codegraph_pitfall_context(backend, repo_path, task, parts: list) -> None:
    results = backend.search(task.title, repo_path, limit=5)
    if not results:
        return
    parts.append("## 相关代码结构 — 踩坑参考（codegraph）\n")
    for r in results:
        parts.append(f"- `{r['name']}` ({r['kind']}) @ {r['file_path']}")


def _resolve_prompt_hooks(config: Config, phase: str, step_id: str, mode: str = "") -> list[str]:
    """Resolve custom prompt hooks from config for a given phase/step.

    Matches keys in priority order:
      1. "{mode}.{step_id}" (e.g. "quick.execute.spawn")
      2. "{mode}.{phase}"   (e.g. "quick.execute")
      3. "{step_id}"        (e.g. "execute.spawn")
      4. "{phase}"          (e.g. "execute")
    """
    hooks = config.prompt_hooks
    matched = []
    if mode:
        mode_step = f"{mode}.{step_id}"
        if mode_step in hooks:
            matched.append(hooks[mode_step])
        mode_phase = f"{mode}.{phase}"
        if mode_phase in hooks and hooks[mode_phase] not in matched:
            matched.append(hooks[mode_phase])
    if step_id in hooks and hooks[step_id] not in matched:
        matched.append(hooks[step_id])
    if phase in hooks and hooks[phase] not in matched:
        matched.append(hooks[phase])
    return matched


def _get_context_files(fs: Filesystem, task: Task, phase: str) -> list[str]:
    td = fs.task_dir(task.id)
    files = []
    candidates = [
        td / "task.json",
        td / "spec.md",
        td / "inbox.md",
        td / "task_breakdown.json",
        td / "test_spec.md",
    ]
    for c in candidates:
        if c.is_file():
            files.append(str(c.relative_to(fs.kanban_dir)))
    return files


def _build_worker_context(fs: Filesystem, task: Task) -> str:
    """Build worker context text for injection into agent spawn_prompt.

    Reads prior run history and phase handoff entries from task.json history.
    """
    runs_dir = fs.task_dir(task.id) / "runs"
    prior_runs = []
    if runs_dir.is_dir():
        for rf in sorted(runs_dir.glob("*.json")):
            try:
                data = json.loads(rf.read_text(encoding="utf-8"))
                if data.get("status") != "active":
                    prior_runs.append(data)
            except (json.JSONDecodeError, OSError):
                pass

    handoffs = [
        h for h in task.history
        if h.get("summary") or h.get("metadata")
    ]

    if not prior_runs and not handoffs:
        return ""

    lines = ["## Worker Context（结构化交接上下文）\n"]

    if prior_runs:
        lines.append("### 历史执行记录\n")
        for r in prior_runs[-5:]:
            run_id = r.get("run_id", "?")
            status = r.get("status", "?")
            phase = r.get("phase", "?")
            lines.append(f"- **Run #{run_id}** ({phase}, {status})")
            if r.get("summary"):
                lines.append(f"  - 摘要: {r['summary']}")
            if r.get("error"):
                lines.append(f"  - 错误: {r['error']}")
            meta = r.get("metadata", {})
            if meta.get("decisions"):
                lines.append(f"  - 决策: {', '.join(meta['decisions'])}")
            if meta.get("changed_files"):
                lines.append(f"  - 变更文件: {', '.join(meta['changed_files'])}")
        lines.append("")

    if handoffs:
        lines.append("### 上游阶段交接\n")
        for h in handoffs[-3:]:
            phase = h.get("phase", "?")
            lines.append(f"- **{phase}** 阶段完成")
            if h.get("summary"):
                lines.append(f"  - 摘要: {h['summary']}")
            meta = h.get("metadata", {})
            if meta.get("decisions"):
                lines.append(f"  - 决策: {', '.join(meta['decisions'])}")
        lines.append("")

    lines.append("请参考以上上下文，在已有工作的基础上继续，避免重复已完成的工作或已知失败的路径。")
    return "\n".join(lines)
