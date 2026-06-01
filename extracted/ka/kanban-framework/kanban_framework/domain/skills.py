from __future__ import annotations
import json
import time
from pathlib import Path


class SkillManager:
    """Manages skill evolution candidates.

    During archive, framework_assessment.json is scanned for actionable
    improvements, and evolution candidates are created.  These JSON files live
    in .kanban/skills/evolved/ and are reviewed / applied by the orchestrator
    or by the user via ``kanban evolve-skills list``.
    """

    # Categories that map to actual skill/rule files
    CATEGORY_TARGETS = {
        "agent": "agents/",
        "rule": "rules/",
        "skill": "SKILL.md",
        "reference": "references/",
    }

    def __init__(self, kanban_dir: Path | None = None):
        self._kanban_dir = Path(kanban_dir) if kanban_dir else None
        self._evolve_dir = (self._kanban_dir / "skills" / "evolved") if self._kanban_dir else None

    def list_skills(self) -> list[str]:
        return [
            "kanban", "brainstorming", "writing-plans",
            "executing-plans", "test-driven-development",
        ]

    def evolve(self, skill_name: str, direction: str,
               evolve_dir: Path | None = None,
               source_task: str | None = None) -> dict:
        """Record a skill evolution candidate.

        Returns dict with status and candidate file path.
        """
        ed = Path(evolve_dir) if evolve_dir else self._evolve_dir
        if ed is None:
            return {
                "skill_name": skill_name,
                "direction": direction,
                "status": "recorded",
            }
        ed.mkdir(parents=True, exist_ok=True)
        candidate = {
            "skill_name": skill_name,
            "direction": direction,
            "status": "pending",
            "source_task": source_task,
            "created_at": time.time(),
            "applied_at": None,
            "applied_by": None,
        }
        filename = f"candidate_{skill_name}_{int(time.time())}.json"
        candidate_file = ed / filename
        candidate_file.write_text(
            json.dumps(candidate, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return {
            "skill_name": skill_name,
            "direction": direction,
            "status": "candidate_saved",
            "file": str(candidate_file),
        }

    def process_assessment(self, task_id: str, tasks_dir: Path) -> list[dict]:
        """Read framework_assessment.json and create evolution candidates
        for each actionable finding.

        Returns list of created candidates.
        """
        assessment_path = tasks_dir / task_id / "framework_assessment.json"
        if not assessment_path.is_file():
            return []

        try:
            assessment = json.loads(assessment_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

        candidates = []
        findings = assessment.get("findings", [])
        for finding in findings:
            category = finding.get("category", "")
            if category not in self.CATEGORY_TARGETS:
                continue
            direction = finding.get("recommendation", finding.get("summary", ""))
            if not direction:
                continue
            skill_name = finding.get("skill_name", category)
            result = self.evolve(
                skill_name, direction,
                source_task=task_id,
            )
            candidates.append(result)

        # Also process pitfalls
        pitfalls = assessment.get("pitfalls", [])
        for p in pitfalls:
            if p.get("skill_improvement"):
                result = self.evolve(
                    p.get("category", "rule"),
                    p["skill_improvement"],
                    source_task=task_id,
                )
                candidates.append(result)

        return candidates

    def list_candidates(self) -> list[dict]:
        """List all pending evolution candidates."""
        if self._evolve_dir is None or not self._evolve_dir.is_dir():
            return []
        results = []
        for f in sorted(self._evolve_dir.glob("candidate_*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                data["_file"] = str(f)
                results.append(data)
            except (json.JSONDecodeError, OSError):
                pass
        return results

    def apply_candidate(self, candidate_file: str, applied_by: str = "system") -> dict:
        """Mark a candidate as applied."""
        cf = Path(candidate_file)
        if not cf.is_file():
            return {"error": f"candidate file not found: {candidate_file}"}
        data = json.loads(cf.read_text(encoding="utf-8"))
        data["status"] = "applied"
        data["applied_at"] = time.time()
        data["applied_by"] = applied_by
        cf.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"status": "applied", "skill_name": data.get("skill_name", ""),
                "direction": data.get("direction", ""), "file": candidate_file}
