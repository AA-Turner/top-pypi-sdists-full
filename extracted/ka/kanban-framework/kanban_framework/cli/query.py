from __future__ import annotations
import json
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.infra.time_tracking import TimeTracker
from kanban_framework.infra.token_tracking import TokenTracker
from kanban_framework.domain.task import TaskManager
from kanban_framework.domain.progress import ProgressTracker


def _resolve(task_id: str) -> tuple[Filesystem, Config, TaskManager]:
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    cfg = Config(fs)
    tm = TaskManager(fs, cfg)
    return fs, cfg, tm


def cmd_score(args: list[str]) -> dict:
    if args and args[0] == "record":
        return _cmd_score_record(args[1:])

    task_id = args[0] if args else "unknown"
    fs, _, tm = _resolve(task_id)
    try:
        task = tm.show(task_id)
    except Exception:
        return {"task_id": task_id, "scores": [], "average": None}

    # Read from task.json score_history (primary source)
    if task.score_history:
        latest = task.score_history[-1]
        return {
            "task_id": task_id,
            "scores": [{"role": r, "total": s} for r, s in latest.get("roles", {}).items()],
            "average": latest.get("average"),
            "iteration": latest.get("iteration"),
        }

    # Fallback: read from report files and auto-persist to score_history (#438)
    from kanban_framework.cli.evaluator import _record_score
    sync_result = _record_score(fs, tm, task_id)
    if sync_result.get("recorded"):
        task = tm.show(task_id)
        if task.score_history:
            latest = task.score_history[-1]
            return {
                "task_id": task_id,
                "scores": [{"role": r, "total": s} for r, s in latest.get("roles", {}).items()],
                "average": latest.get("average"),
                "iteration": latest.get("iteration"),
                "auto_recorded": True,
            }

    scores = []
    for it in range(1, task.iteration + 1):
        report_dir = fs.report_dir(task_id, it)
        if not report_dir.exists():
            continue
        for role in ["code_reviewer", "qa", "product_reviewer", "pm", "designer"]:
            rf = report_dir / "reviews" / f"{role}_report.json"
            if not fs.file_exists(rf):
                rf = report_dir / f"{role}_report.json"
            if fs.file_exists(rf):
                data = fs.read_json(rf)
                scores.append({
                    "role": role,
                    "iteration": it,
                    "total": data.get("total", 0),
                })
    avg = round(sum(s["total"] for s in scores) / len(scores), 2) if scores else None
    result = {"task_id": task_id, "scores": scores, "average": avg}
    if not scores:
        result["hint"] = "no score_history or report files found — run 'kanban score record <id>' or 'kanban workflow complete-phase'"
    return result


def _cmd_score_record(args: list[str]) -> dict:
    """Record evaluation scores: kanban score record TASK-001 --code-reviewer 8.5 ..."""
    if not args:
        return {"error": "task_id required"}
    task_id = args[0]
    _, _, tm = _resolve(task_id)
    scores = {}
    i = 1
    while i < len(args):
        role = args[i].lstrip("-").replace("-", "_")
        if i + 1 < len(args):
            try:
                scores[role] = float(args[i + 1])
                i += 2
            except (ValueError, TypeError):
                i += 1
        else:
            i += 1

    if not scores:
        return {"error": "no scores provided"}

    task = tm.show(task_id)
    avg = round(sum(scores.values()) / len(scores), 2)
    # Update task scores
    current_scores = dict(task.scores)
    current_scores.update(scores)
    history = list(task.score_history)
    history.append({
        "iteration": task.iteration,
        "average": avg,
        "roles": scores,
    })
    tm.update(task_id, scores=current_scores, score_history=history)
    return {"task_id": task_id, "scores": scores, "average": avg, "recorded": True}


def cmd_summary(args: list[str]) -> dict:
    task_id = args[0] if args else "unknown"
    fs, _, tm = _resolve(task_id)
    try:
        task = tm.show(task_id)
    except Exception:
        return {"task_id": task_id, "summary": "task not found"}
    progress = ProgressTracker(fs)
    return {
        "task_id": task.id,
        "title": task.title,
        "status": task.status.value,
        "phase": task.phase.value,
        "iteration": task.iteration,
        "progress": progress.progress(task_id),
    }


def cmd_progress(args: list[str]) -> dict:
    task_id = args[0] if args else "unknown"
    fs, _, _ = _resolve(task_id)
    tracker = ProgressTracker(fs)
    return {"task_id": task_id, "progress": tracker.progress(task_id)}


def cmd_time(args: list[str]) -> dict:
    sub = args[0] if args else "report"
    # If first arg is not a known subcommand, treat as task_id for report
    if sub not in ("start", "end", "track", "report"):
        sub, task_id = "report", sub
    else:
        task_id = args[1] if len(args) > 1 else "unknown"
    fs, _, _ = _resolve(task_id)
    tracker = TimeTracker(fs.kanban_dir / "reports" / "time_tracking.json")

    if sub == "start":
        phase = args[2] if len(args) > 2 else "unknown"
        tracker.start_phase(task_id, phase)
        return {"task_id": task_id, "phase": phase, "action": "started"}
    if sub == "end":
        phase = args[2] if len(args) > 2 else "unknown"
        tracker.end_phase(task_id, phase)
        return {"task_id": task_id, "phase": phase, "action": "ended"}
    if sub == "track":
        agent = ""
        elapsed = 0.0
        i = 2
        while i < len(args):
            if args[i] == "--agent" and i + 1 < len(args):
                agent = args[i + 1]; i += 2
            elif args[i] == "--elapsed" and i + 1 < len(args):
                elapsed = float(args[i + 1]); i += 2
            elif args[i] == "--phase" and i + 1 < len(args):
                task_id = args[i + 1] if task_id == "unknown" else task_id; i += 2
            else:
                i += 1
        if agent:
            tracker.track_agent(task_id, task_id, agent, elapsed)
        return {"task_id": task_id, "agent": agent, "elapsed": elapsed}
    return {"task_id": task_id, "time": tracker.report(task_id)}


def _run_codeburn(cmd: list[str]) -> dict:
    """Run a codeburn subcommand and return its JSON output."""
    import subprocess, shutil
    exe = shutil.which("codeburn") or shutil.which("npx")
    if not exe:
        return {"error": "codeburn not installed. Install: npm install -g codeburn", "install_hint": "npm install -g codeburn"}
    try:
        full_cmd = [exe] if exe.endswith("codeburn") else [exe, "codeburn"]
        full_cmd.extend(cmd)
        result = subprocess.run(full_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            import json as _json
            return _json.loads(result.stdout)
        return {"error": result.stderr.strip() or "codeburn returned no data"}
    except Exception as e:
        return {"error": str(e)}


def cmd_tokens(args: list[str]) -> dict:
    """Token usage — JSONL-based report + CodeBurn integration."""
    sub = args[0] if args else "report"

    # CodeBurn-powered subcommands
    if sub == "dashboard":
        return _run_codeburn([])
    if sub == "optimize":
        period = "week"
        for i, a in enumerate(args):
            if a == "-p" and i + 1 < len(args):
                period = args[i + 1]
        result = _run_codeburn(["optimize", "-p", period])
        if "error" not in result:
            return result
        # optimize doesn't support --json, capture text output
        import subprocess, shutil
        exe = shutil.which("codeburn") or shutil.which("npx")
        full = [exe] if (exe or "").endswith("codeburn") else ["npx", "codeburn"]
        full.extend(["optimize", "-p", period])
        try:
            r = subprocess.run(full, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
            return {"text_output": r.stdout.strip()}
        except Exception as e:
            return {"error": str(e)}
    if sub == "yield":
        return _run_codeburn(["yield", "--format", "json"])
    if sub == "models":
        return _run_codeburn(["models", "--format", "json"])
    if sub == "status":
        return _run_codeburn(["status", "--format", "json"])
    if sub == "cost":
        return _run_codeburn(["report", "-p", "week", "--format", "json"])

    if sub == "per-step":
        from kanban_framework.domain.jsonl_reader import attribute_tokens_to_steps
        result = attribute_tokens_to_steps(days=30)
        return {"per_step_tokens": result}

    # Default: JSONL-based report
    from kanban_framework.domain.jsonl_reader import collect_all_sessions, aggregate_stats
    days = 30
    i = 0 if args else 0
    while i < len(args):
        if args[i] == "--days" and i + 1 < len(args):
            days = int(args[i + 1]); i += 2
        else:
            i += 1

    sessions = collect_all_sessions(days=days)
    aggr = aggregate_stats(sessions)

    return {
        "period_days": days,
        "sessions": aggr["sessions"],
        "total_turns": aggr["total_turns"],
        "total_input": aggr["total_input"],
        "total_output": aggr["total_output"],
        "total_tokens": aggr["total_input"] + aggr["total_output"],
        "cache_read": aggr["total_cache_read"],
        "cache_write": aggr["total_cache_write"],
        "duration_minutes": round(aggr["total_duration_minutes"], 1),
        "tool_counts": dict(sorted(aggr["tool_counts"].items(), key=lambda x: -x[1])[:10]),
        "models": aggr["models"],
        "recent_sessions": aggr["per_session"][:10],
    }


def cmd_dashboard(args: list[str]) -> dict:
    from kanban_framework.infra.dashboard import DashboardManager
    from kanban_framework.infra.filesystem import Filesystem
    root = Filesystem.find_project_root()
    fs = Filesystem(root)
    mgr = DashboardManager(fs.kanban_dir)

    sub = args[0] if args else None

    # Parse --port flag
    port = None
    i = 0
    while i < len(args):
        if args[i] == "--port" and i + 1 < len(args):
            try:
                port = int(args[i + 1])
            except ValueError:
                return {"dashboard": {"error": f"invalid port: {args[i+1]}"}}
            i += 2
        else:
            i += 1

    if sub in ("--help", "-h", "help"):
        return {"dashboard": {
            "help": True,
            "message": "Usage: kanban dashboard [start|stop|status|restart|deploy] [--port N]",
            "commands": {
                "start":   "部署并启动 Dashboard 服务器 (--port 指定端口，默认 3000)",
                "stop":    "停止 Dashboard 服务器",
                "status":  "显示 Dashboard 运行状态",
                "restart": "重启 Dashboard 服务器",
                "deploy":  "仅部署文件到 .kanban/dashboard/",
            },
            "default": "无参数时默认执行 start",
        }}

    if sub == "deploy":
        return {"dashboard": mgr.deploy()}
    elif sub == "check":
        return {"dashboard": mgr.check_env()}
    elif sub == "start":
        return {"dashboard": mgr.start(port)}
    elif sub == "stop":
        return {"dashboard": mgr.stop()}
    elif sub == "status":
        return {"dashboard": mgr.status()}
    elif sub == "restart":
        return {"dashboard": mgr.restart(port)}
    elif sub is None:
        return {"dashboard": mgr.start(port)}
    else:
        return {"dashboard": {"error": f"unknown subcommand: {sub}", "help_hint": "Try: kanban dashboard --help"}}
