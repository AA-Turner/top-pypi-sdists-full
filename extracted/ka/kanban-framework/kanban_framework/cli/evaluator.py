from __future__ import annotations
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.infra.config import Config
from kanban_framework.domain.task import TaskManager


def dispatch(args: list[str]) -> dict:
    if not args:
        return {"error": "subcommand required: collect-scores, record-score, collect-plan-review"}
    sub = args[0]
    task_id = args[1] if len(args) > 1 else "unknown"
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    cfg = Config(fs)
    tm = TaskManager(fs, cfg)

    if sub == "collect-scores":
        return _collect_scores(fs, tm, task_id)
    if sub == "record-score":
        return _record_score(fs, tm, task_id)
    if sub == "collect-plan-review":
        return _collect_plan_review_scores(fs, tm, task_id)
    return {"error": f"unknown evaluator subcommand: {sub}"}


def _extract_score(data: dict) -> float:
    """Extract score from report JSON, handling nested formats. (#372)

    Tries: top-level keys (total, score, overall, total_score, average),
    then nested 'scores' dict (scores.total, scores.overall).
    """
    from kanban_framework.domain.guard import _first_score
    top = _first_score(data)
    if top is not None:
        return float(top)
    # Nested: {"scores": {"code_quality": 9, "total": 8.75}}
    nested = data.get("scores")
    if isinstance(nested, dict):
        ns = _first_score(nested)
        if ns is not None:
            return float(ns)
    return 0.0


def _collect_scores(fs: Filesystem, tm: TaskManager, task_id: str) -> dict:
    try:
        task = tm.show(task_id)
    except Exception:
        return {"task_id": task_id, "scores": [], "average": None}

    scores = []
    searched_paths = []
    task_dir = fs.task_dir(task_id)
    for it in range(1, task.iteration + 1):
        report_dir = fs.report_dir(task_id, it)

        # Use mode-specific eval roles as primary source, plus broad fallback
        from kanban_framework.infra.scheduler import Scheduler
        mode = getattr(task, 'mode', None)
        mode_roles = [r["name"] for r in Scheduler.eval_roles(
            lightweight=task.lightweight, mode=mode, kanban_dir=fs.kanban_dir)]
        all_roles = list(dict.fromkeys(mode_roles + [
            "code_reviewer", "qa", "product_reviewer", "pm", "designer", "review"]))
        for role in all_roles:
            filename = f"{role}_report.json"
            # Search multiple locations: iter reviews, iter root, task reviews
            for rf in (report_dir / "reviews" / filename,
                       report_dir / filename,
                       task_dir / "reviews" / filename):
                searched_paths.append(str(rf))
                if fs.file_exists(rf):
                    data = fs.read_json(rf)
                    scores.append({
                        "role": role,
                        "iteration": it,
                        "total": _extract_score(data),
                    })
                    break

    avg = round(sum(s["total"] for s in scores) / len(scores), 2) if scores else None
    result = {"task_id": task_id, "scores": scores, "average": avg}
    if not scores:
        result["searched_paths"] = list(dict.fromkeys(searched_paths))  # dedup preserving order
        result["hint"] = "place review report JSON files at one of the searched paths, then run 'kanban evaluator collect-scores' or 'kanban workflow complete-phase'"
    return result


def _record_score(fs: Filesystem, tm: TaskManager, task_id: str) -> dict:
    scores_data = _collect_scores(fs, tm, task_id)
    try:
        task = tm.show(task_id)
    except Exception:
        return {"task_id": task_id, "error": "task not found"}

    avg = scores_data["average"]
    if avg is None:
        return {"task_id": task_id, "recorded": False, "error": "no scores to record"}

    # Build per-iteration role scores dict
    role_scores = {s["role"]: s["total"] for s in scores_data["scores"]
                   if s["iteration"] == task.iteration}

    # Append to score_history
    entry = {
        "iteration": task.iteration,
        "average": avg,
        "roles": role_scores,
    }
    new_history = list(task.score_history)
    # Replace existing entry for same iteration; otherwise append
    replaced = False
    for i, h in enumerate(new_history):
        if h.get("iteration") == task.iteration:
            new_history[i] = entry
            replaced = True
            break
    if not replaced:
        new_history.append(entry)

    tm.update(task_id, scores=role_scores, score_history=new_history)

    return {
        "task_id": task_id,
        "recorded": True,
        "iteration": task.iteration,
        "average": avg,
    }


_PLAN_REVIEW_DIMENSIONS = [
    "requirement_clarity", "technical_feasibility",
    "task_decomposition", "acceptance_criteria",
    "research_completeness", "parallel_safety",
]


def _collect_plan_review_scores(
    fs: Filesystem, tm: TaskManager, task_id: str
) -> dict:
    try:
        task = tm.show(task_id)
    except Exception:
        return {"task_id": task_id, "dimensions": [], "average": None}

    dimensions = []
    for it in range(1, task.iteration + 1):
        report_dir = fs.report_dir(task_id, it)
        if not report_dir.exists():
            continue

        for dim in _PLAN_REVIEW_DIMENSIONS:
            rf = report_dir / f"{dim}_report.json"
            if fs.file_exists(rf):
                data = fs.read_json(rf)
                applicable = data.get("applicable", True)
                if applicable:
                    dimensions.append({
                        "dimension": dim,
                        "iteration": it,
                        "score": data.get("score", 0),
                        "findings": data.get("findings", []),
                        "issues": data.get("issues", []),
                    })

    avg = round(
        sum(d["score"] for d in dimensions) / len(dimensions), 2
    ) if dimensions else None
    return {"task_id": task_id, "dimensions": dimensions, "average": avg}
