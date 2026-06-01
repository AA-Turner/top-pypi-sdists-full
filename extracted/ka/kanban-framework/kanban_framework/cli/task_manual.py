"""Manual task scaffold — generate spec/plan templates for pre-filled tasks.

Invoked only when `kanban create --manual` is used. Creates template files
(spec.md, task_breakdown.json, plan/index.md) so the user can edit them
before running the normal plan workflow.
"""
from __future__ import annotations

import json as _json

from kanban_framework.infra.filesystem import Filesystem
from kanban_framework.domain.task import TaskManager

_SPEC_TEMPLATE = """\
# Spec: {title}

> Task ID: {task_id}

## 目标

{desc}

## 功能需求

<!-- 列出核心功能点，每条一个 FR-NNN -->

- FR-001: （填写功能需求）

## 非功能需求

<!-- 性能/安全/可用性要求 -->

- （如：响应时间 < 200ms、支持并发 100 用户等）

## 验收标准

<!-- 可测试的通过条件，完成后应能逐一勾选 -->

- [ ] （填写验收标准）

## 技术约束

<!-- 语言/框架/依赖/兼容性要求 -->

- （如：Python 3.10+、使用 FastAPI、必须兼容 macOS/Linux）
""".lstrip()


def scaffold_manual(fs: Filesystem, tm: TaskManager, task_id: str,
                   title: str, desc: str) -> dict:
    """Create scaffolded spec/plan templates for user editing.

    Returns scaffold info dict with task_dir, files_created, and next_step.
    """
    task_dir = fs.task_dir(task_id)
    plan_dir = task_dir / "plan"
    fs.ensure_dir(plan_dir)

    files_created: list[str] = []

    # spec.md
    spec_path = task_dir / "spec.md"
    if not spec_path.exists():
        spec_path.write_text(_SPEC_TEMPLATE.format(
            task_id=task_id, title=title, desc=desc or "（填写任务目标）",
        ), encoding="utf-8")
        files_created.append(str(spec_path.relative_to(fs.kanban_dir)))

    # task_breakdown.json
    tb_path = task_dir / "task_breakdown.json"
    if not tb_path.exists():
        tb_path.write_text(_json.dumps({
            "task_id": task_id,
            "subtasks": [{
                "id": "ST-001",
                "title": title,
                "description": desc or "（填写 subtask 描述）",
                "file_ownership": [],
                "dependencies": [],
            }],
        }, indent=2, ensure_ascii=False), encoding="utf-8")
        files_created.append(str(tb_path.relative_to(fs.kanban_dir)))

    # plan/index.md
    index_path = plan_dir / "index.md"
    if not index_path.exists():
        index_path.write_text(
            f"# Plan Index — {task_id}\n\n"
            f"## Overview\n{desc or '（填写实现策略）'}\n\n"
            f"## Subtasks\n- ST-001: {title}\n\n"
            f"## Technical Decisions\n- （填写技术选型）\n",
            encoding="utf-8",
        )
        files_created.append(str(index_path.relative_to(fs.kanban_dir)))

    return {
        "task_dir": str(task_dir),
        "files_created": files_created,
        "next_step": f"Edit templates in {task_dir}, then run: kanban run {task_id}",
    }
