from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from kanban_framework.infra.filesystem import Filesystem

DOMAIN_KEYWORDS = {
    "testing": ["测试", "test", "pytest", "coverage", "覆盖率", "assert"],
    "cli": ["命令", "command", "CLI", "参数", "argparse", "dispatch"],
    "infra": ["性能", "数据库", "缓存", "配置", "config", "文件系统", "git"],
    "workflow": ["流程", "FSM", "阶段", "phase", "iteration", "迭代"],
    "agent": ["agent", "prompt", "模型", "role"],
}

PRIORITY_KEYWORDS = {
    "high": ["紧急", "bug", "修复", "崩溃", "失败", "报错", "错误", "严重"],
    "medium": ["补充", "优化", "改进", "增加", "新增"],
    "low": ["建议", "考虑", "美化", "文档"],
}

# Keywords that suggest the user wants to restart from Plan
REPLAN_KEYWORDS = [
    "重新开始", "重新检查spec", "重新检查plan", "重新检查 spec", "重新检查 plan",
    "要改spec", "要改 spec", "要改plan", "要改 plan",
    "回到plan", "回到 plan", "重走plan", "重走 plan",
    "完整重新规划", "从plan开始", "从 plan 开始",
    "重新设计", "重新规划",
]

# Keywords that suggest out-of-scope / migration
MIGRATION_KEYWORDS = [
    "下一个任务", "后续任务", "下个迭代", "下次", "另开任务",
    "新任务", "迁移到", "转到", "分配到",
]


class InboxAnalyzer:
    """Read-only analysis of inbox.md feedback items.

    Key difference from v0: this class does NOT modify inbox.md, spec.md,
    or any other task artifact.  Results are returned for the caller to act on.
    """

    def __init__(self, fs: Filesystem):
        self._fs = fs

    # ── public API ──────────────────────────────────────────────────

    def generate_analysis(self, task_id: str) -> dict:
        pending = self.read_pending_items(task_id)
        if not pending:
            return {
                "task_id": task_id,
                "pending_count": 0,
                "extracted_requirements": [],
                "suggested_phase": None,
                "conflicts": [],
                "scope_classifications": [],
                "summary": {"to_implement": 0, "to_migrate": 0, "conflicts": 0, "out_of_scope": 0},
                "suggested_action": "ok_to_archive",
                "inbox_modified": False,
            }
        requirements = self.analyze_requirements(pending)
        classifications = self.classify_scope(task_id, requirements)
        suggested_phase = self.suggest_phase(task_id, requirements)
        conflicts = self.detect_conflicts(task_id, requirements)

        summary = {"to_implement": 0, "to_migrate": 0, "conflicts": 0, "out_of_scope": 0}
        for c in classifications:
            scope = c.get("scope", "current")
            if scope == "conflict":
                summary["conflicts"] += 1
            elif scope in ("migrate", "next-task"):
                summary["to_migrate"] += 1
            elif scope == "out-of-scope":
                summary["out_of_scope"] += 1
            else:
                summary["to_implement"] += 1

        suggested_action = self._decide_suggested_action(
            task_id, classifications, conflicts, summary
        )

        return {
            "task_id": task_id,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "pending_count": len(pending),
            "extracted_requirements": requirements,
            "suggested_phase": suggested_phase,
            "phase_reason": self._phase_reason(suggested_phase),
            "conflicts": conflicts,
            "scope_classifications": classifications,
            "summary": summary,
            "suggested_action": suggested_action,
            "inbox_modified": False,
        }

    # ── reading ─────────────────────────────────────────────────────

    def read_pending_items(self, task_id: str) -> list[str]:
        task_dir = self._fs.task_dir(task_id)
        inbox_path = task_dir / "inbox.md"
        if not self._fs.file_exists(inbox_path):
            return []
        content = inbox_path.read_text(encoding="utf-8")
        items = []
        for line in content.splitlines():
            stripped = line.strip()
            # Only collect unchecked items with checkbox format
            if stripped.startswith("- [ ]"):
                items.append(stripped[5:].strip())
            # Also catch natural-language lines (not headings, not checked, not meta)
            elif stripped and not stripped.startswith("#") and not stripped.startswith("- [x]") and not stripped.startswith("- [X]"):
                if not stripped.startswith("**") and "kanban inbox" not in stripped:
                    if len(stripped) > 5 and not stripped.startswith("---") and not stripped.startswith("可以") and not stripped.startswith("在此"):
                        items.append(stripped)
        return items

    def read_all_items(self, task_id: str) -> list[dict]:
        """Return both pending and checked items with raw line info."""
        task_dir = self._fs.task_dir(task_id)
        inbox_path = task_dir / "inbox.md"
        if not self._fs.file_exists(inbox_path):
            return []
        content = inbox_path.read_text(encoding="utf-8")
        results = []
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("- [x]") or stripped.startswith("* [x]"):
                text = stripped[5:].strip()
                # Parse inline tags
                tags = self._parse_tags(stripped)
                results.append({"text": text, "checked": True, "tags": tags, "raw": stripped})
            elif stripped.startswith("- [ ]") or stripped.startswith("* [ ]"):
                text = stripped[5:].strip()
                tags = self._parse_tags(stripped)
                results.append({"text": text, "checked": False, "tags": tags, "raw": stripped})
        return results

    # ── analysis ────────────────────────────────────────────────────

    def analyze_requirements(self, items: list[str]) -> list[dict]:
        results = []
        for item in items:
            domain = self._match_domain(item)
            priority = self._match_priority(item)
            results.append({
                "requirement": item,
                "domain": domain,
                "priority": priority,
            })
        return results

    def classify_scope(self, task_id: str, requirements: list[dict]) -> list[dict]:
        """Classify each requirement as current / next-task / out-of-scope."""
        task_dir = self._fs.task_dir(task_id)
        task_json = task_dir / "task.json"
        spec_path = task_dir / "spec.md"

        task_desc = ""
        spec_content = ""
        if self._fs.file_exists(task_json):
            try:
                import json
                data = json.loads(task_json.read_text(encoding="utf-8"))
                task_desc = (data.get("title", "") + " " + data.get("description", "")).lower()
            except Exception:
                pass
        if self._fs.file_exists(spec_path):
            spec_content = spec_path.read_text(encoding="utf-8").lower()

        results = []
        for req in requirements:
            text = req.get("requirement", "").lower()
            scope = self._judge_scope(text, task_desc, spec_content)
            results.append({
                "requirement": req["requirement"],
                "scope": scope,
                "domain": req.get("domain", "infra"),
                "priority": req.get("priority", "medium"),
            })
        return results

    def _judge_scope(self, text: str, task_desc: str, spec_content: str) -> str:
        """Judge whether feedback belongs to current task, next task, or out of scope."""
        # Check for migration keywords
        for kw in MIGRATION_KEYWORDS:
            if kw in text:
                return "next-task"

        # Check if text relates to current task description or spec
        words = [w for w in text.split() if len(w) > 1]
        if not words:
            return "current"

        matched = 0
        corpus = task_desc + " " + spec_content
        if corpus.strip():
            for w in words:
                if w in corpus:
                    matched += 1
            if matched >= 2:
                return "current"
            elif matched == 1:
                return "next-task"
            else:
                return "out-of-scope"
        return "out-of-scope"

    def detect_conflicts(self, task_id: str, requirements: list[dict]) -> list[dict]:
        """Detect contradictions between inbox requirements and existing spec.

        Returns conflict descriptions. Each conflict entry now includes a
        'requires_semantic_check' flag when keyword matching is inconclusive.
        """
        conflicts = []
        task_dir = self._fs.task_dir(task_id)
        spec_path = task_dir / "spec.md"
        if not self._fs.file_exists(spec_path):
            return conflicts
        spec_content = spec_path.read_text(encoding="utf-8")

        for req in requirements:
            req_text = req["requirement"]
            req_lower = req_text.lower()
            words = [w for w in req_lower.split() if len(w) > 2]

            conflict = self._check_structural_conflict(req, spec_content, words)
            if conflict:
                conflicts.append(conflict)
            else:
                # Structural check passed, but recommend semantic verification
                if words:
                    conflicts.append({
                        "type": "potential_conflict",
                        "inbox_item": req_text,
                        "severity": "low",
                        "conflicts_with": "通过关键词比对未发现明显冲突，建议语义核查",
                        "resolution": "运行 `kanban inbox process --semantic` 进行语义审核",
                        "requires_semantic_check": True,
                    })
        return conflicts

    def _check_structural_conflict(self, req: dict, spec_content: str, words: list[str]) -> dict | None:
        """Structural-level conflict detection using keyword and negation patterns."""
        req_text = req["requirement"]
        req_lower = req_text.lower()

        # Pattern: spec mentions keyword but inbox says "不要"/"去掉"/"移除"
        negation_patterns = ["不要", "去掉", "移除", "删除", "放弃", "不再", "取消", "替代", "替代方案", "换成", "改用"]
        spec_lower = spec_content.lower()
        for neg in negation_patterns:
            if neg in req_lower:
                # Find what is being negated
                for w in words:
                    if w in spec_lower and w not in ("不要", "去掉", "移除", "删除", "放弃", "不再", "取消", "替代", "替代方案", "换成", "改用"):
                        return {
                            "type": "spec_contradiction",
                            "inbox_item": req_text,
                            "severity": "high",
                            "conflicts_with": f"spec.md 中包含 '{w}' 相关内容，但反馈要求 {neg}",
                            "resolution": "需用户确认是否替换现有设计",
                            "requires_semantic_check": True,
                        }

        # Pattern: "应该用X而不是Y" / "用X替代Y"
        if any(p in req_lower for p in ["而不是", "应该用", "建议用", "用...替代"]):
            for w in words:
                if w in spec_lower and len(w) > 3:
                    return {
                        "type": "spec_alternative",
                        "inbox_item": req_text,
                        "severity": "high",
                        "conflicts_with": f"spec.md 中提到 '{w}'，反馈建议替代方案",
                        "resolution": "需评估替代方案并更新 spec.md",
                        "requires_semantic_check": True,
                    }

        # Pattern: inbox adds something NOT in spec at all ("新增" / "增加" / "补充")
        if any(p in req_lower for p in ["新增", "增加", "补充", "添加"]):
            found = any(w in spec_lower for w in words if len(w) > 3)
            if not found:
                return {
                    "type": "spec_addition",
                    "inbox_item": req_text,
                    "severity": "medium",
                    "conflicts_with": "spec.md 中未找到相关内容，此为全新需求",
                    "resolution": "确认是否在 scope 内，更新 spec.md 和 plan/",
                    "requires_semantic_check": False,
                }

        return None

    def suggest_phase(self, task_id: str, requirements: list[dict]) -> str:
        task_dir = self._fs.task_dir(task_id)
        has_spec = self._fs.file_exists(task_dir / "spec.md")
        has_plan = self._fs.file_exists(task_dir / "plan" / "index.md")
        has_code = bool(list(task_dir.glob("**/*.py")))

        if not has_spec and not has_plan:
            return "plan"
        if has_spec and has_plan and not has_code:
            return "plan"
        if has_code and requirements:
            return "plan"
        if has_code and not requirements:
            return "execute"
        return "plan"

    # ── suggested action logic ──────────────────────────────────────

    def _decide_suggested_action(
        self, task_id: str, classifications: list[dict],
        conflicts: list[dict], summary: dict
    ) -> str:
        # 1. High-severity structural conflicts → pause for user
        if any(c.get("severity") == "high" for c in conflicts):
            return "pause_for_user_decision"

        # 2. Check if task is in active execution
        in_execute = self._task_in_phase(task_id, ("execute", "evaluate"))
        has_current = summary["to_implement"] > 0

        # 3. Check for replan keywords in feedback text
        all_text = " ".join(c.get("requirement", "") for c in classifications)
        if any(kw in all_text for kw in REPLAN_KEYWORDS):
            return "replan"

        # 4. Current-scope items + task in execute → default add subtasks
        if has_current and in_execute:
            return "add_subtasks"

        # 5. Current-scope items + task in plan → already covered by plan phase
        if has_current and self._task_in_phase(task_id, ("plan", "plan_review")):
            return "update_spec"

        # 6. All migrate/out-of-scope
        if not has_current and (summary["to_migrate"] > 0 or summary["out_of_scope"] > 0):
            return "ok_to_archive"

        return "add_subtasks"

    def _task_in_phase(self, task_id: str, phases: tuple[str, ...]) -> bool:
        task_json = self._fs.task_dir(task_id) / "task.json"
        if not self._fs.file_exists(task_json):
            return False
        try:
            import json
            data = json.loads(task_json.read_text(encoding="utf-8"))
            return data.get("phase", "") in phases
        except Exception:
            return False

    # ── tag parsing ─────────────────────────────────────────────────

    def _parse_tags(self, line: str) -> dict:
        """Extract done:/migrated:/wontfix: tags from an inbox line.

        Returns dict with keys: done (path), migrated (task_id), wontfix (reason)
        """
        import re
        tags = {}
        m = re.search(r'done:(\S+)', line)
        if m:
            tags["done"] = m.group(1)
        m = re.search(r'migrated:(\S+)', line)
        if m:
            tags["migrated"] = m.group(1)
        m = re.search(r'wontfix:(.+?)(?:-->|$)', line)
        if m:
            tags["wontfix"] = m.group(1).strip()
        return tags

    # ── internal helpers ────────────────────────────────────────────

    def _match_domain(self, text: str) -> str:
        text_lower = text.lower()
        scores = {}
        for domain, keywords in DOMAIN_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw.lower() in text_lower)
            if score > 0:
                scores[domain] = score
        return max(scores, key=scores.get) if scores else "infra"

    def _match_priority(self, text: str) -> str:
        text_lower = text.lower()
        for priority in ("high", "medium", "low"):
            for kw in PRIORITY_KEYWORDS[priority]:
                if kw in text_lower:
                    return priority
        return "medium"

    def _phase_reason(self, phase: str) -> str:
        reasons = {
            "plan": "存在新需求或 spec.md 未完整，建议从 Plan 阶段开始",
            "execute": "spec.md 和 plan.md 已就绪，可直接进入执行",
            "evaluate": "代码已完成，进入评估阶段",
        }
        return reasons.get(phase, "建议从 Plan 阶段开始")
