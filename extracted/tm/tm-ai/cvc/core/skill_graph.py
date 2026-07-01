"""
cvc.core.skill_graph — Causal Skill Graph (CSG).

Builds a directed graph of skill dependencies using the DAG's parent-child
relationships. Tracks which skills were active during each commit and correlates
with success/failure outcomes.

Key innovation: Every other system has flat skill lists. CVC has a CAUSAL
GRAPH showing which skill combinations work for which task types, derived
from actual execution history.

The graph enables:
  - Auto-routing: "This looks like a security task → invoke Security agent"
  - Skill recommendations: "Users doing X usually benefit from skill Y"
  - Capability assessment: "The agent has 92% success at task type Z"
  - Combinatorial discovery: "Skills A + B together yield better results than either alone"
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger("cvc.skill_graph")


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


@dataclass
class SkillNode:
    """A node in the causal skill graph."""

    skill_name: str
    total_uses: int = 0
    success_count: int = 0
    failure_count: int = 0
    avg_quality_score: float = 0.0
    task_types: dict[str, int] = field(default_factory=dict)  # task_type → count
    last_used: float = 0.0

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0


@dataclass
class SkillEdge:
    """An edge representing co-occurrence of skills in successful commits."""

    source: str  # skill_name
    target: str  # skill_name
    co_occurrences: int = 0
    joint_success_rate: float = 0.0
    task_types: list[str] = field(default_factory=list)


@dataclass
class TaskTypeProfile:
    """Performance profile for a specific task type."""

    task_type: str = ""
    total_attempts: int = 0
    success_count: int = 0
    best_skills: list[str] = field(default_factory=list)  # Ranked by success rate
    best_combos: list[list[str]] = field(default_factory=list)  # Top skill combinations
    avg_turns: float = 0.0
    avg_cost: float = 0.0

    @property
    def success_rate(self) -> float:
        return self.success_count / max(self.total_attempts, 1)


# ---------------------------------------------------------------------------
# Skill Graph
# ---------------------------------------------------------------------------


class CausalSkillGraph:
    """
    Directed graph tracking skill causality with task outcomes.

    Built from commit history, updated incrementally as new commits arrive.
    """

    GRAPH_FILE = "skill_graph.json"

    def __init__(self, cvc_root: Path) -> None:
        self.cvc_root = cvc_root
        self._graph_path = cvc_root / self.GRAPH_FILE
        self.nodes: dict[str, SkillNode] = {}
        self.edges: list[SkillEdge] = []
        self.task_profiles: dict[str, TaskTypeProfile] = {}
        self._load()

    def _load(self) -> None:
        """Load the skill graph from disk."""
        if not self._graph_path.exists():
            return
        try:
            data = json.loads(self._graph_path.read_text(encoding="utf-8"))
            for n in data.get("nodes", []):
                self.nodes[n["skill_name"]] = SkillNode(**n)
            for e in data.get("edges", []):
                self.edges.append(SkillEdge(**e))
            for tp in data.get("task_profiles", []):
                self.task_profiles[tp["task_type"]] = TaskTypeProfile(**tp)
        except Exception as e:
            logger.warning("Failed to load skill graph: %s", e)

    def save(self) -> None:
        """Persist the skill graph to disk."""
        data = {
            "nodes": [
                {
                    "skill_name": n.skill_name,
                    "total_uses": n.total_uses,
                    "success_count": n.success_count,
                    "failure_count": n.failure_count,
                    "avg_quality_score": n.avg_quality_score,
                    "task_types": n.task_types,
                    "last_used": n.last_used,
                }
                for n in self.nodes.values()
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "co_occurrences": e.co_occurrences,
                    "joint_success_rate": e.joint_success_rate,
                    "task_types": e.task_types,
                }
                for e in self.edges
            ],
            "task_profiles": [
                {
                    "task_type": tp.task_type,
                    "total_attempts": tp.total_attempts,
                    "success_count": tp.success_count,
                    "best_skills": tp.best_skills,
                    "best_combos": tp.best_combos,
                    "avg_turns": tp.avg_turns,
                    "avg_cost": tp.avg_cost,
                }
                for tp in self.task_profiles.values()
            ],
            "updated_at": time.time(),
        }
        self._graph_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def record_commit_outcome(
        self,
        active_skills: list[str],
        task_type: str,
        success: bool,
        quality_score: float = 0.0,
        turns: int = 0,
        cost_usd: float = 0.0,
    ) -> None:
        """
        Record a commit's outcome to update the skill graph.

        Called after each commit with the skills that were active during
        the task and whether the outcome was successful.
        """
        # Update nodes
        for skill_name in active_skills:
            if skill_name not in self.nodes:
                self.nodes[skill_name] = SkillNode(skill_name=skill_name)
            node = self.nodes[skill_name]
            node.total_uses += 1
            if success:
                node.success_count += 1
            else:
                node.failure_count += 1
            # Running average of quality
            if quality_score > 0:
                n = node.total_uses
                node.avg_quality_score = (node.avg_quality_score * (n - 1) + quality_score) / n
            node.task_types[task_type] = node.task_types.get(task_type, 0) + 1
            node.last_used = time.time()

        # Update edges (co-occurrence)
        for i, skill_a in enumerate(active_skills):
            for skill_b in active_skills[i + 1 :]:
                edge = self._get_or_create_edge(skill_a, skill_b)
                edge.co_occurrences += 1
                if task_type not in edge.task_types:
                    edge.task_types.append(task_type)
                # Update joint success rate
                if success:
                    total = edge.co_occurrences
                    edge.joint_success_rate = (edge.joint_success_rate * (total - 1) + 1.0) / total
                else:
                    total = edge.co_occurrences
                    edge.joint_success_rate = (edge.joint_success_rate * (total - 1)) / total

        # Update task profile
        if task_type not in self.task_profiles:
            self.task_profiles[task_type] = TaskTypeProfile(task_type=task_type)
        profile = self.task_profiles[task_type]
        profile.total_attempts += 1
        if success:
            profile.success_count += 1
        if turns > 0:
            n = profile.total_attempts
            profile.avg_turns = (profile.avg_turns * (n - 1) + turns) / n
        if cost_usd > 0:
            n = profile.total_attempts
            profile.avg_cost = (profile.avg_cost * (n - 1) + cost_usd) / n

        # Recompute best skills for this task type
        self._recompute_best_skills(task_type)

    def _get_or_create_edge(self, source: str, target: str) -> SkillEdge:
        """Get or create an edge between two skills (order-independent)."""
        a, b = sorted([source, target])
        for edge in self.edges:
            if edge.source == a and edge.target == b:
                return edge
        edge = SkillEdge(source=a, target=b)
        self.edges.append(edge)
        return edge

    def _recompute_best_skills(self, task_type: str) -> None:
        """Recompute the best skills and combos for a task type."""
        profile = self.task_profiles.get(task_type)
        if not profile:
            return

        # Best individual skills
        relevant_skills: list[tuple[str, float]] = []
        for name, node in self.nodes.items():
            if task_type in node.task_types and node.total_uses >= 2:
                relevant_skills.append((name, node.success_rate))
        relevant_skills.sort(key=lambda x: x[1], reverse=True)
        profile.best_skills = [s[0] for s in relevant_skills[:10]]

        # Best skill combos
        relevant_combos: list[tuple[list[str], float]] = []
        for edge in self.edges:
            if task_type in edge.task_types and edge.co_occurrences >= 2:
                relevant_combos.append(([edge.source, edge.target], edge.joint_success_rate))
        relevant_combos.sort(key=lambda x: x[1], reverse=True)
        profile.best_combos = [c[0] for c in relevant_combos[:5]]

    def recommend_skills(
        self,
        task_type: str,
        available_skills: list[str] | None = None,
    ) -> list[tuple[str, float]]:
        """
        Recommend skills for a task type, ranked by success rate.

        Returns list of (skill_name, predicted_success_rate).
        """
        profile = self.task_profiles.get(task_type)
        if not profile:
            # Fallback to overall best skills
            all_skills = sorted(
                self.nodes.values(),
                key=lambda n: n.success_rate,
                reverse=True,
            )
            return [(n.skill_name, n.success_rate) for n in all_skills[:5]]

        recommendations: list[tuple[str, float]] = []
        for skill_name in profile.best_skills:
            if available_skills is None or skill_name in available_skills:
                node = self.nodes.get(skill_name)
                if node:
                    recommendations.append((skill_name, node.success_rate))

        return recommendations[:10]

    def recommend_agent(
        self,
        task_type: str,
        agents: dict[str, list[str]],  # agent_name → [skill_names]
    ) -> str | None:
        """
        Recommend the best agent for a task type based on their skill profiles.

        Used for automatic sub-agent routing.
        """
        best_agent = None
        best_score = 0.0

        for agent_name, agent_skills in agents.items():
            # Compute aggregate score for this agent's skills on this task
            score = 0.0
            count = 0
            for skill in agent_skills:
                node = self.nodes.get(skill)
                if node and task_type in node.task_types:
                    score += node.success_rate
                    count += 1
            if count > 0:
                avg_score = score / count
                if avg_score > best_score:
                    best_score = avg_score
                    best_agent = agent_name

        return best_agent

    def get_capability_summary(self) -> str:
        """
        Generate a natural-language summary of the agent's capabilities.

        Used for self-assessment: "What am I good at?"
        """
        if not self.nodes:
            return "No skill history recorded yet."

        parts = ["## Agent Capability Summary\n"]

        # Top skills by success rate
        top_skills = sorted(
            [
                (n.skill_name, n.success_rate, n.total_uses)
                for n in self.nodes.values()
                if n.total_uses >= 3
            ],
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        if top_skills:
            parts.append("### Strongest Skills")
            for name, rate, uses in top_skills:
                parts.append(f"- **{name}**: {rate:.0%} success ({uses} uses)")

        # Top task types
        top_tasks = sorted(
            [
                (tp.task_type, tp.success_rate, tp.total_attempts)
                for tp in self.task_profiles.values()
                if tp.total_attempts >= 2
            ],
            key=lambda x: x[1],
            reverse=True,
        )[:10]

        if top_tasks:
            parts.append("\n### Best Task Types")
            for task, rate, attempts in top_tasks:
                parts.append(f"- **{task}**: {rate:.0%} success ({attempts} attempts)")

        # Weakest areas
        weak_skills = sorted(
            [
                (n.skill_name, n.success_rate, n.total_uses)
                for n in self.nodes.values()
                if n.total_uses >= 3 and n.success_rate < 0.5
            ],
            key=lambda x: x[1],
        )[:5]

        if weak_skills:
            parts.append("\n### Areas for Improvement")
            for name, rate, uses in weak_skills:
                parts.append(f"- **{name}**: {rate:.0%} success ({uses} uses)")

        return "\n".join(parts)
