"""FastAPI dashboard backend — replaces Node.js server.js.

Serves both the REST API and the Vue SPA static files.
All data comes from framework internal modules — zero hardcoded definitions.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse


def create_app(kanban_dir: str | Path | None = None) -> FastAPI:
    """Create the FastAPI application wired to a specific .kanban/ directory.

    When called by uvicorn --factory with no arguments, reads KANBAN_ROOT
    from the environment variable set by DashboardManager.start().
    """
    if kanban_dir is None:
        kanban_dir = os.environ.get("KANBAN_ROOT", "")
        if not kanban_dir:
            raise RuntimeError("KANBAN_ROOT env var not set — cannot locate .kanban/")
    kanban = Path(kanban_dir).resolve()

    from kanban_framework.infra.filesystem import Filesystem
    from kanban_framework.infra.config import Config
    from kanban_framework.domain.task import TaskManager

    fs = Filesystem(kanban.parent)
    cfg = Config(fs)
    tm = TaskManager(fs, cfg)

    app = FastAPI(title="Kanban Dashboard", docs_url=None, redoc_url=None)

    # ── Helpers ──────────────────────────────────────────────────────

    def _load_task_json(task_id: str) -> dict:
        """Load and parse a task's JSON file."""
        f = fs.task_dir(task_id) / "task.json"
        if not f.is_file():
            raise HTTPException(404, f"Task {task_id} not found")
        return json.loads(f.read_text(encoding="utf-8"))

    def _load_report_files(task_id: str, iteration: int) -> dict[str, dict]:
        """Load review reports from an iteration directory."""
        reports: dict[str, dict] = {}
        for search_dir in [
            fs.report_dir(task_id, iteration) / "reviews",
            fs.report_dir(task_id, iteration),
            fs.report_dir(task_id, iteration) / "evaluate",
        ]:
            if not search_dir.is_dir():
                continue
            for rf in sorted(search_dir.glob("*_report.json")):
                try:
                    data = json.loads(rf.read_text(encoding="utf-8"))
                    reports[rf.stem] = data
                except (ValueError, OSError):
                    pass
        return reports

    def _discover_agents() -> list[str]:
        """Scan .claude/agents/*.md for available agent types."""
        agents: list[str] = ["general-purpose"]
        agents_dir = kanban.parent / ".claude" / "agents"
        if agents_dir.is_dir():
            for f in sorted(agents_dir.glob("*.md")):
                try:
                    content = f.read_text(encoding="utf-8")
                    match = re.search(r'^---\s*\n\s*name:\s*(.+?)\s*$', content, re.MULTILINE)
                    if match:
                        agents.append(match.group(1).strip())
                except OSError:
                    pass
        return sorted(set(agents))

    # ── Dynamic discovery endpoints ──────────────────────────────────

    @app.get("/api/health")
    def health():
        task_count = len(list(fs.tasks_dir.glob("TASK-*/task.json")))
        return {"status": "ok", "kanban_root": str(kanban), "task_count": task_count}

    @app.get("/api/modes")
    def get_modes():
        from kanban_framework.infra.scheduler import Scheduler
        modes = Scheduler.get_modes(workflow=cfg.workflow, kanban_dir=fs.kanban_dir)
        return {"modes": {k: {"name": k, "phases": v} for k, v in modes.items()}}

    @app.get("/api/phases")
    def get_phases(mode: str | None = None):
        from kanban_framework.infra.scheduler import Scheduler
        from kanban_framework.infra.consts import Consts
        m = mode or cfg.default_mode
        order = Scheduler.dispatch_order(mode=m, workflow=cfg.workflow, kanban_dir=fs.kanban_dir)
        phases = [p.value if hasattr(p, "value") else str(p) for p in order]
        return {"mode": m, "phases": phases}

    @app.get("/api/steps")
    def get_steps(mode: str | None = None):
        from kanban_framework.domain.steps import _get_steps
        from kanban_framework.infra.consts import Consts
        m = mode or cfg.default_mode
        steps_map = _get_steps(m, custom_steps=None)
        result: dict[str, list[dict]] = {}
        for phase, step_list in steps_map.items():
            result[phase] = [
                {
                    "id": s.id,
                    "description": s.description,
                    "agent_type": s.agent_type,
                    "parallel": s.parallel,
                    "user_action": s.user_action,
                    "interactive": s.interactive,
                    "spawn_prompt": s.spawn_prompt,
                    "required_artifacts": s.required_artifacts,
                    "after": s.after,
                    "type": getattr(s, "type", "action"),
                    "guard": getattr(s, "guard", None),
                    "gateway": getattr(s, "gateway", None),
                }
                for s in step_list
            ]
        return {"mode": m, "steps": result}

    @app.get("/api/agents")
    def get_agents():
        return {"agents": _discover_agents()}

    @app.get("/api/step-templates")
    def get_step_templates():
        import json as _json
        # Build deduplicated map: user overrides builtin on same id (#521)
        by_id: dict[str, dict] = {}
        # 1. Built-in templates from package
        pkg_dir = Path(__file__).resolve().parent.parent / "step_templates"
        if pkg_dir.is_dir():
            for f in sorted(pkg_dir.glob("*.json")):
                try:
                    t = _json.loads(f.read_text(encoding="utf-8"))
                    t["source"] = "builtin"
                    t["file"] = f.stem
                    by_id[t.get("id", f.stem)] = t
                except (ValueError, OSError):
                    pass
        # 2. User templates from .kanban/steps/ (override builtin on same id)
        user_dir = fs.kanban_dir / "steps"
        if user_dir.is_dir():
            for f in sorted(user_dir.glob("*.json")):
                try:
                    t = _json.loads(f.read_text(encoding="utf-8"))
                    t["source"] = "user"
                    t["file"] = f.stem
                    by_id[t.get("id", f.stem)] = t
                except (ValueError, OSError):
                    pass
        return {"templates": list(by_id.values())}

    @app.post("/api/step-templates")
    def create_step_template(body: dict):
        import json as _json
        tid = body.get("id", "").strip()
        if not tid:
            raise HTTPException(400, "id is required")
        user_dir = fs.kanban_dir / "steps"
        user_dir.mkdir(parents=True, exist_ok=True)
        target = user_dir / f"{tid}.json"
        if target.exists():
            raise HTTPException(409, f"Template '{tid}' already exists")
        body["source"] = "user"
        body["file"] = tid
        target.write_text(_json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"success": True, "id": tid}

    @app.put("/api/step-templates/{tid}")
    def update_step_template(tid: str, body: dict):
        import json as _json
        user_dir = fs.kanban_dir / "steps"
        target = user_dir / f"{tid}.json"
        if not target.exists():
            raise HTTPException(404, f"Template '{tid}' not found")
        body["source"] = "user"
        body["file"] = tid
        target.write_text(_json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"success": True, "id": tid}

    @app.delete("/api/step-templates/{tid}")
    def delete_step_template(tid: str):
        user_dir = fs.kanban_dir / "steps"
        target = user_dir / f"{tid}.json"
        if not target.exists():
            raise HTTPException(404, f"Template '{tid}' not found")
        target.unlink()
        return {"success": True, "id": tid}

    @app.get("/api/guard-checks")
    def get_guard_checks():
        return {"checks": [
            {"name": "knowledge_references", "label": "知识库引用检查", "phases": ["plan"]},
            {"name": "test_files", "label": "测试文件存在", "phases": ["execute"]},
            {"name": "tdd_evidence", "label": "TDD 证据表", "phases": ["execute"]},
            {"name": "test_spec_coverage", "label": "测试规格覆盖率", "phases": ["execute"]},
            {"name": "knowledge_artifact", "label": "知识产物", "phases": ["execute", "retrospective"]},
            {"name": "quick_scope", "label": "Quick 范围限制", "phases": ["execute"]},
            {"name": "evaluation_reports", "label": "评估报告", "phases": ["evaluate"]},
            {"name": "evaluation_score", "label": "评估评分", "phases": ["evaluate"]},
        ]}

    # ── Task endpoints ───────────────────────────────────────────────

    @app.get("/api/tasks")
    def list_tasks():
        tasks = []
        for td in sorted(fs.tasks_dir.glob("TASK-*/task.json")):
            try:
                data = json.loads(td.read_text(encoding="utf-8"))
                tasks.append(data)
            except (ValueError, OSError):
                pass
        return {"tasks": tasks}

    @app.get("/api/tasks/{task_id}")
    def get_task(task_id: str):
        data = _load_task_json(task_id)
        iteration = data.get("iteration", 1)
        data["reports"] = _load_report_files(task_id, iteration)
        return data

    @app.get("/api/tasks/{task_id}/steps")
    def get_task_steps(task_id: str):
        from kanban_framework.domain.step_progress import load_progress
        try:
            progress = load_progress(fs, task_id)
        except Exception:
            progress = {"steps": {}}
        return progress

    @app.get("/api/tasks/{task_id}/stats")
    def get_task_stats(task_id: str):
        data = _load_task_json(task_id)
        iteration = data.get("iteration", 1)
        score_history = data.get("score_history", [])
        avg_score = 0.0
        if score_history:
            last = score_history[-1]
            for key in ("average", "overall", "score"):
                v = last.get(key)
                if v is not None:
                    try:
                        avg_score = float(v)
                        break
                    except (ValueError, TypeError):
                        pass
        return {
            "task_id": task_id,
            "iteration": iteration,
            "phase": data.get("phase", ""),
            "score": avg_score,
            "score_history": score_history,
            "subtasks": len(data.get("subtasks", [])),
        }

    @app.post("/api/tasks/{task_id}/phase")
    async def transition_phase(task_id: str, request: Request):
        body = await request.json()
        # Run synchronously — phase transitions are fast
        import subprocess, sys
        target = body.get("phase", "")
        if not target:
            raise HTTPException(400, "phase is required")
        result = subprocess.run(
            [sys.executable, "-m", "kanban_framework", "--json", "workflow", "transition", task_id, target],
            capture_output=True, text=True, cwd=str(kanban.parent),
        )
        if result.returncode != 0:
            raise HTTPException(500, result.stderr.strip() or "transition failed")
        try:
            return json.loads(result.stdout)
        except ValueError:
            return {"success": True, "phase": target}

    @app.put("/api/tasks/{task_id}")
    async def update_task(task_id: str, request: Request):
        body = await request.json()
        updates = {}
        for key in ("title", "description", "mode", "priority"):
            if key in body:
                updates[key] = body[key]
        if not updates:
            raise HTTPException(400, "No updatable fields provided")
        try:
            tm.update(task_id, **updates)
        except Exception as e:
            raise HTTPException(500, str(e))
        return {"success": True, "updated": list(updates.keys())}

    @app.post("/api/tasks/{task_id}/step/{step_id}")
    async def update_step(task_id: str, step_id: str, request: Request):
        body = await request.json()
        status = body.get("status", "completed")
        from kanban_framework.domain.step_progress import load_progress, save_progress
        progress = load_progress(fs, task_id)
        import time
        progress["steps"][step_id] = {"status": status, "updated_at": time.time()}
        save_progress(fs, task_id, progress)
        return {"success": True, "step": step_id, "status": status}

    @app.put("/api/tasks/{task_id}/subtask/{st_id}")
    async def update_subtask(task_id: str, st_id: str, request: Request):
        body = await request.json()
        data = _load_task_json(task_id)
        for st in data.get("subtasks", []):
            if st.get("id") == st_id:
                for key in ("status", "title", "description"):
                    if key in body:
                        st[key] = body[key]
                break
        (fs.task_dir(task_id) / "task.json").write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return {"success": True}

    @app.get("/api/tasks/{task_id}/retrospective")
    def get_retrospective(task_id: str):
        retro = fs.task_dir(task_id) / "retrospective.md"
        if not retro.is_file():
            raise HTTPException(404, "retrospective.md not found")
        return {"content": retro.read_text(encoding="utf-8")}

    # ── Archive endpoints ────────────────────────────────────────────

    @app.get("/api/archive")
    def list_archive():
        tasks = []
        for td in sorted(fs.archive_dir().glob("TASK-*/task.json")):
            try:
                data = json.loads(td.read_text(encoding="utf-8"))
                tasks.append({"id": data["id"], "title": data.get("title", ""), "phase": data.get("phase", "")})
            except (ValueError, OSError):
                pass
        return {"tasks": tasks}

    @app.get("/api/archive/{task_id}")
    def get_archived_task(task_id: str):
        task_dir = fs.archive_dir() / task_id
        f = task_dir / "task.json"
        if not f.is_file():
            raise HTTPException(404, f"Archived task {task_id} not found")
        data = json.loads(f.read_text(encoding="utf-8"))
        iteration = data.get("iteration", 1)
        # Try to load reports from task dir
        reports: dict[str, dict] = {}
        for search_dir in [task_dir / "reviews", task_dir / "evaluate", task_dir]:
            if not search_dir.is_dir():
                continue
            for rf in sorted(search_dir.glob("*_report.json")):
                try:
                    reports[rf.stem] = json.loads(rf.read_text(encoding="utf-8"))
                except (ValueError, OSError):
                    pass
        data["reports"] = reports
        return data

    # ── Config endpoints ─────────────────────────────────────────────

    @app.get("/api/config")
    def get_config():
        return cfg.raw

    @app.put("/api/config")
    async def put_config(request: Request):
        body = await request.json()
        if not isinstance(body, dict):
            raise HTTPException(400, "Expected JSON object")
        cfg_path = fs.kanban_dir / "config.json"
        tmp = cfg_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(cfg_path)
        return {"success": True}

    @app.get("/api/workflow")
    def get_workflow():
        return cfg.workflow

    @app.put("/api/workflow")
    async def put_workflow(request: Request):
        body = await request.json()
        if not isinstance(body, dict):
            raise HTTPException(400, "Expected JSON object")
        # Write modes to separate files if present
        modes = body.pop("modes", None)
        if modes and isinstance(modes, dict):
            wf_dir = fs.kanban_dir / "workflows"
            wf_dir.mkdir(parents=True, exist_ok=True)
            for mode_name, mode_cfg in modes.items():
                if isinstance(mode_cfg, dict):
                    (wf_dir / f"{mode_name}.json").write_text(
                        json.dumps(mode_cfg, indent=2, ensure_ascii=False), encoding="utf-8"
                    )
        # Write remaining global config to workflow.json
        wf_path = fs.kanban_dir / "workflow.json"
        tmp = wf_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(wf_path)
        return {"success": True}

    @app.get("/api/workflow/{mode_name}")
    def get_workflow_mode(mode_name: str):
        # Check modes in workflow.json
        modes_cfg = cfg.workflow.get("modes", {})
        if isinstance(modes_cfg, dict) and mode_name in modes_cfg:
            return {"mode": mode_name, **modes_cfg[mode_name]}
        # Check .kanban/workflows/<mode>.json
        wf_file = fs.kanban_dir / "workflows" / f"{mode_name}.json"
        if wf_file.is_file():
            return {"mode": mode_name, **json.loads(wf_file.read_text(encoding="utf-8"))}
        # Check package templates
        from kanban_framework.domain.steps_loader import _load_template_steps
        template = _load_template_steps(mode_name)
        if template is not None:
            return {"mode": mode_name, "phases": [
                {"id": phase, "steps": [
                    {"id": s.id, "description": s.description, "agent_type": s.agent_type}
                    for s in steps
                ]}
                for phase, steps in template.items()
            ]}
        raise HTTPException(404, f"Mode {mode_name} not found")

    @app.put("/api/workflow/{mode_name}")
    async def put_workflow_mode(mode_name: str, request: Request):
        body = await request.json()
        if not isinstance(body, dict):
            raise HTTPException(400, "Expected JSON object")
        wf_dir = fs.kanban_dir / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        wf_file = wf_dir / f"{mode_name}.json"
        tmp = wf_file.with_suffix(".tmp")
        tmp.write_text(json.dumps(body, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp.replace(wf_file)
        return {"success": True}

    # ── Knowledge endpoints (direct domain calls, no subprocess) ────

    def _get_km():
        from kanban_framework.domain.knowledge import KnowledgeManager
        return KnowledgeManager(fs)

    @app.get("/api/knowledge/health")
    def knowledge_health():
        from kanban_framework.cli.knowledge import _handle_health
        try:
            km = _get_km()
            data = _handle_health(km)
            return {"healthy": True, **data}
        except Exception as exc:
            return {"healthy": False, "error": str(exc)}

    @app.get("/api/knowledge/entries")
    def knowledge_entries(q: str | None = None, domain: str | None = None, status: str | None = None):
        try:
            km = _get_km()
            if q:
                # search_hybrid returns top-K by relevance; use small limit for search
                results = km.search_hybrid(q, limit=20, relevance_threshold=0)
                matched_ids = {r["id"] for r in results}
                if matched_ids:
                    entries = km.list_entries(domain=domain, status=status or "active", limit=500)
                    entries = [e for e in entries if e.get("id") in matched_ids]
                else:
                    entries = []
            else:
                entries = km.list_entries(domain=domain, status=status or "active", limit=500)
            return {"entries": entries}
        except Exception:
            return {"entries": []}

    @app.get("/api/knowledge/entries/{entry_id}")
    def knowledge_entry(entry_id: str):
        try:
            km = _get_km()
            entry = km.get_entry(entry_id)
            if not entry:
                raise HTTPException(404, f"Entry {entry_id} not found")
            return entry
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(500, str(exc))

    @app.put("/api/knowledge/entries/{entry_id}")
    async def knowledge_entry_update(entry_id: str, request: Request):
        body = await request.json()
        try:
            km = _get_km()
            entry = km.get_entry(entry_id)
            if not entry:
                raise HTTPException(404, f"Entry {entry_id} not found")
            allowed = {"title", "content", "domain", "category", "severity",
                        "status", "tags", "code_example", "biz_context"}
            updates = {k: v for k, v in body.items() if k in allowed}
            if not updates:
                raise HTTPException(400, "No valid fields to update")
            updated = km.update_entry(entry_id, **updates)
            return updated
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(500, str(exc))

    @app.get("/api/knowledge/pending")
    def knowledge_pending():
        return knowledge_entries(status="pending")

    @app.post("/api/knowledge/approve")
    async def knowledge_approve(request: Request):
        body = await request.json()
        ids = body.get("ids", [])
        results = []
        try:
            km = _get_km()
            for eid in ids:
                try:
                    km.update_entry(eid, status="active")
                    results.append({"id": eid, "success": True})
                except Exception:
                    results.append({"id": eid, "success": False})
        except Exception:
            pass
        return {"results": results}

    @app.post("/api/knowledge/reject")
    async def knowledge_reject(request: Request):
        body = await request.json()
        ids = body.get("ids", [])
        results = []
        try:
            km = _get_km()
            for eid in ids:
                try:
                    km.delete_entry(eid)
                    results.append({"id": eid, "success": True})
                except Exception:
                    results.append({"id": eid, "success": False})
        except Exception:
            pass
        return {"results": results}

    # ── SSE endpoint ─────────────────────────────────────────────────

    @app.get("/api/events")
    async def events(request: Request):
        async def event_stream() -> AsyncGenerator[dict, None]:
            yield {"event": "connected", "data": json.dumps({"status": "ok"})}
            stop = asyncio.Event()
            try:
                import watchfiles
                watch_dirs = [
                    str(fs.tasks_dir),
                    str(fs.archive_dir()),
                ]
                watch_files = [
                    str(fs.kanban_dir / "config.json"),
                    str(fs.kanban_dir / "workflow.json"),
                ]
                async for changes in watchfiles.awatch(*watch_dirs, *watch_files, stop_event=stop):
                    if await request.is_disconnected():
                        stop.set()
                        break
                    evt_map: dict[str, str] = {}
                    for change_type, path in changes:
                        path_str = str(path)
                        if "tasks" in path_str and path_str.endswith("task.json"):
                            evt_map["task_updated"] = path_str
                        elif "archive" in path_str:
                            evt_map["archive:changed"] = path_str
                        elif path_str.endswith("config.json"):
                            evt_map["config:changed"] = path_str
                        elif path_str.endswith("workflow.json"):
                            evt_map["config:changed"] = path_str
                    for evt_name, evt_data in evt_map.items():
                        yield {"event": evt_name, "data": json.dumps({"path": evt_data})}
            except asyncio.CancelledError:
                stop.set()

        return EventSourceResponse(event_stream())

    # ── Token stats ──────────────────────────────────────────────────

    @app.get("/api/token-stats")
    def token_stats():
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "kanban_framework", "--json", "tokens"],
            capture_output=True, text=True, cwd=str(kanban.parent),
        )
        if result.returncode != 0:
            return {"tokens": []}
        try:
            return json.loads(result.stdout)
        except ValueError:
            return {"tokens": []}

    # ── Documentation ─────────────────────────────────────────────────

    @app.get("/api/docs")
    def list_docs():
        """List available reference documents with titles and paths."""
        from kanban_framework.infra.filesystem import Filesystem as FS
        skill_dir = FS.find_skill_dir()
        refs_dir = skill_dir / "references"
        docs = []
        if refs_dir.is_dir():
            _DOC_TITLES = {
                "ci-workflow-guide.md": "CI 工作流配置教程",
                "user-guide.md": "用户上手文档",
                "config-json-reference.md": "config.json 字段参考",
                "workflow-json-reference.md": "workflow.json 字段参考",
                "mode-comparison.md": "模式对比 (Quick/Light/Full)",
                "external-knowledge-backend-integration.md": "知识库后端接入指南",
                "knowledge-cli-reference.md": "知识库 CLI 参考",
                "knowledge-accumulation-guide.md": "知识积累指南",
                "commands.md": "命令速查",
            }
            for f in sorted(refs_dir.glob("*.md")):
                docs.append({
                    "file": f.name,
                    "title": _DOC_TITLES.get(f.name, f.stem.replace("-", " ").title()),
                    "path": str(f),
                })
        return {"docs": docs}

    @app.get("/api/docs/{doc_name}")
    def get_doc(doc_name: str):
        """Return the content of a specific reference document."""
        from kanban_framework.infra.filesystem import Filesystem as FS
        skill_dir = FS.find_skill_dir()
        doc_path = skill_dir / "references" / doc_name
        if not doc_path.is_file() or not doc_path.name.endswith(".md"):
            raise HTTPException(404, f"Document {doc_name} not found")
        return {"file": doc_name, "content": doc_path.read_text(encoding="utf-8")}

    # ── Static file serving (SPA) ────────────────────────────────────

    static_dir = Path(__file__).resolve().parent / "static"
    if static_dir.is_dir():
        from starlette.responses import FileResponse

        @app.middleware("http")
        async def spa_fallback(request: Request, call_next):
            response = await call_next(request)
            if response.status_code == 404 and not request.url.path.startswith("/api"):
                return FileResponse(static_dir / "index.html", media_type="text/html")
            return response

        app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")

    return app
