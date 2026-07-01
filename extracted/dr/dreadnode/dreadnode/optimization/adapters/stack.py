import asyncio
import json
import re
import shutil
import statistics
import tempfile
import typing as t
from dataclasses import dataclass
from pathlib import Path

import yaml
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from dreadnode.agents.skills import attach_capability_skills
from dreadnode.agents.trajectory import Trajectory, trajectory_to_turns
from dreadnode.app.server.app import create_agent
from dreadnode.capabilities.capability import Capability
from dreadnode.capabilities.loader import _parse_frontmatter
from dreadnode.capabilities.types import AgentDef
from dreadnode.evaluations.evaluation import Evaluation
from dreadnode.optimization.backends.base import OptimizationEvaluationBatch
from dreadnode.optimization.result import OptimizationEvaluation

CapabilityImprovementSurface = t.Literal[
    "agent_prompt",
    "capability_prompt",
    "skill_descriptions",
    "skill_bodies",
]

DEFAULT_SURFACES: tuple[CapabilityImprovementSurface, ...] = (
    "agent_prompt",
    "capability_prompt",
    "skill_descriptions",
    "skill_bodies",
)


def skill_description_component(skill_name: str) -> str:
    """Return the flat component key for a skill description."""
    return f"skill_description:{skill_name}"


def skill_body_component(skill_name: str) -> str:
    """Return the flat component key for a skill body."""
    return f"skill_body:{skill_name}"


@dataclass(frozen=True)
class _EditableComponent:
    """Metadata needed to map flat candidate keys back to capability files."""

    key: str
    relative_path: Path
    kind: str
    name: str | None = None


@dataclass
class MaterializedCapabilityCandidate:
    """A temp capability workspace with a resolved capability and selected agent."""

    root: Path
    capability: Capability
    agent_def: AgentDef
    _temp_dir: tempfile.TemporaryDirectory[str] | None = None

    def cleanup(self) -> None:
        """Delete the backing temp directory if this candidate owns one."""
        if self._temp_dir is not None:
            self._temp_dir.cleanup()
            self._temp_dir = None


class CapabilityProposalResponse(BaseModel):
    """Structured response contract for proposer capabilities."""

    proposals: dict[str, str]
    rationale: str | None = None


class StackAwareCapabilityAdapter(BaseModel):
    """Capability-level adapter for stack-aware local optimization."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    capability: Capability
    model: str
    agent_name: str | None = None
    allowed_surfaces: tuple[CapabilityImprovementSurface, ...] = DEFAULT_SURFACES
    dataset: list[dict[str, t.Any]] = Field(default_factory=list)
    scorers: t.Any = Field(default_factory=list)
    score_name: str | None = None
    goal_field: str = "goal"
    dataset_input_mapping: list[str] | dict[str, str] | None = None
    name: str | None = None
    objective: str | None = None
    proposer_agent: t.Any = None

    # Production-fidelity wiring. None means "do not contribute hooks/tools
    # from this source", matching the historical (pre-fix) shape; capability
    # hooks always flow through.
    policy_factory: t.Callable[[], t.Any] | None = None
    """Optional factory returning a ``SessionPolicy`` whose ``hooks`` are
    layered into the agent on each evaluation (e.g. ``HeadlessSessionPolicy``
    contributing a ``max_steps`` hook). Called per ``_build_agent``."""
    registry: t.Any = None
    """Optional ``CapabilityRegistry`` for cross-capability tool/hook merging.
    When provided, ``registry.all_tools()`` + ``registry.all_hooks()`` are
    layered into the agent alongside the materialized capability's own
    tools/hooks."""
    system_prompt_append: str | None = None
    """Mirrors the production CLI ``--system-prompt`` overlay; appended to the
    final system prompt by ``create_agent`` so optimization sees the same
    prompt-stack production does."""

    _agent_def: AgentDef = PrivateAttr()
    _components: dict[str, _EditableComponent] = PrivateAttr(default_factory=dict)
    _live_candidates: list[MaterializedCapabilityCandidate] = PrivateAttr(default_factory=list)

    def model_post_init(self, __context: t.Any, /) -> None:
        self._agent_def = self._resolve_agent_def(self.capability, self.agent_name)
        self._components = self._build_component_map(self.capability, self._agent_def)

    def seed_candidate(self) -> dict[str, str]:
        """Return the current flat candidate map for mutable capability surfaces."""
        candidate: dict[str, str] = {}

        if "agent_prompt" in self.allowed_surfaces:
            candidate["agent_prompt"] = self._agent_def.system_prompt or ""

        if "capability_prompt" in self.allowed_surfaces:
            capability_prompt_path = self.capability.path / "system-prompt.md"
            candidate["capability_prompt"] = (
                capability_prompt_path.read_text() if capability_prompt_path.exists() else ""
            )

        for key, component in self._components.items():
            if component.kind == "skill_description":
                frontmatter, _body = self._read_markdown_with_frontmatter(
                    self.capability.path / component.relative_path
                )
                candidate[key] = str(frontmatter.get("description", ""))
            elif component.kind == "skill_body":
                _frontmatter, body = self._read_markdown_with_frontmatter(
                    self.capability.path / component.relative_path
                )
                candidate[key] = body

        return candidate

    def component_keys(self) -> list[str]:
        """Return all editable component keys in stable order."""
        return list(self.seed_candidate().keys())

    @property
    def proposal_enabled(self) -> bool:
        """Whether this adapter exposes a custom candidate proposer."""
        return self.proposer_agent is not None

    def materialize_candidate(
        self,
        candidate: dict[str, str],
    ) -> MaterializedCapabilityCandidate:
        """Copy the capability to a temp workspace and apply candidate edits."""
        self._validate_candidate(candidate)

        temp_dir = tempfile.TemporaryDirectory(prefix=f"{self.capability.name}-improve-")
        target_root = Path(temp_dir.name) / self.capability.path.name
        shutil.copytree(self.capability.path, target_root)

        for key, value in candidate.items():
            component = self._components.get(key)
            if key == "agent_prompt":
                self._write_agent_prompt(target_root, value)
                continue
            if key == "capability_prompt":
                self._write_capability_prompt(target_root, value)
                continue
            if component is None:
                raise ValueError(f"Unknown candidate component: {key}")
            self._write_component(target_root, component, value)

        materialized = Capability(target_root)
        selected_agent = self._resolve_agent_def(materialized, self._agent_def.name)
        return MaterializedCapabilityCandidate(
            root=target_root,
            capability=materialized,
            agent_def=selected_agent,
            _temp_dir=temp_dir,
        )

    def apply_candidate(self, candidate: dict[str, str]) -> t.Any:
        """Build an agent from a materialized candidate workspace."""
        materialized = self.materialize_candidate(candidate)
        self._live_candidates.append(materialized)
        return self._build_agent(materialized)

    async def evaluate(
        self,
        batch: list[dict[str, t.Any]],
        candidate: dict[str, str],
        *,
        capture_traces: bool = False,
    ) -> OptimizationEvaluationBatch:
        """Evaluate a candidate by rebuilding the capability and running Evaluation."""
        materialized = await asyncio.to_thread(self.materialize_candidate, candidate)
        try:
            agent = self._build_agent(materialized)
            evaluation = Evaluation(
                name=self.name
                or f"{agent.name or materialized.capability.name} capability optimization",
                task=agent.task(name=agent.name),
                dataset=batch,
                dataset_input_mapping=self._resolve_dataset_input_mapping(batch),
                scorers=self.scorers,
            )
            result = await evaluation.run()
            return OptimizationEvaluationBatch(
                outputs=[sample.output for sample in result.samples],
                scores=[self._sample_score(sample) for sample in result.samples],
                trajectories=(
                    [self._serialize_sample(sample) for sample in result.samples]
                    if capture_traces
                    else None
                ),
                objective_scores=[self._metric_scores(sample) for sample in result.samples] or None,
            )
        finally:
            materialized.cleanup()

    async def evaluate_candidate(
        self,
        candidate: dict[str, str],
        example: dict[str, t.Any] | None = None,
    ) -> OptimizationEvaluation:
        """Evaluate one candidate in GEPA-compatible `(score, side_info)` form."""
        batch = [example] if example is not None else self.dataset
        if not batch:
            raise ValueError("Capability optimization requires at least one dataset example.")
        evaluation_batch = await self.evaluate(
            batch,
            candidate,
            capture_traces=True,
        )
        score = statistics.mean(evaluation_batch.scores) if evaluation_batch.scores else 0.0
        side_info: dict[str, t.Any] = {
            "scores": evaluation_batch.scores,
            "batch_size": len(batch),
        }
        if evaluation_batch.trajectories is not None:
            side_info["trajectories"] = evaluation_batch.trajectories
        return OptimizationEvaluation(score=score, side_info=side_info)

    def make_reflective_dataset(
        self,
        candidate: dict[str, str],
        eval_batch: OptimizationEvaluationBatch,
        components_to_update: list[str],
    ) -> dict[str, list[dict[str, t.Any]]]:
        """Build component-scoped reflective data for GEPA."""
        components = components_to_update or list(candidate.keys())
        trajectories = eval_batch.trajectories or []
        dataset: dict[str, list[dict[str, t.Any]]] = {}

        for component in components:
            component_rows: list[dict[str, t.Any]] = []
            for score, trajectory in zip(eval_batch.scores, trajectories, strict=False):
                component_rows.append(
                    {
                        "Candidate": candidate.get(component, ""),
                        "Inputs": trajectory.get("input"),
                        "Generated Outputs": trajectory.get("output"),
                        "Feedback": self._format_feedback(score=score, trajectory=trajectory),
                    }
                )
            dataset[component] = component_rows

        return dataset

    def propose_new_texts(
        self,
        candidate: dict[str, str],
        reflective_dataset: dict[str, list[dict[str, t.Any]]],
        components_to_update: list[str],
    ) -> dict[str, str]:
        """Delegate candidate proposal to an optional proposer capability agent."""
        components = components_to_update or list(candidate.keys())
        if self.proposer_agent is None:
            return {component: candidate.get(component, "") for component in components}

        prompt = self._build_proposal_prompt(
            candidate=candidate,
            reflective_dataset=reflective_dataset,
            components_to_update=components,
        )
        try:
            output = asyncio.run(self.proposer_agent.run(prompt))
            completion = self._extract_completion_text(output)
            parsed = self._parse_proposal_response(completion)
        except Exception as exc:
            logger.warning("Capability proposer failed: {}", exc)
            return {component: candidate.get(component, "") for component in components}

        proposals: dict[str, str] = {}
        for component in components:
            value = parsed.proposals.get(component)
            proposals[component] = (
                value if isinstance(value, str) and value.strip() else candidate.get(component, "")
            )
        return proposals

    def cleanup(self) -> None:
        """Delete any materialized candidate workspaces retained by apply_candidate()."""
        for materialized in self._live_candidates:
            materialized.cleanup()
        self._live_candidates.clear()

    def _build_agent(self, materialized: MaterializedCapabilityCandidate) -> t.Any:
        # Layer extras the way production does (see ``SessionRuntime._create_agent``):
        # registry tools/hooks (cross-capability), then the materialized capability's
        # own tools/hooks, then policy.hooks (e.g. max_steps). Without this the
        # optimization-time agent runs without compaction, custom guardrails, and
        # policy budgets — and any reflection LM that wins under those conditions
        # produces a candidate that doesn't match what production runs.
        capability_tools = list(materialized.capability.tools or [])
        capability_hooks = list(materialized.capability.hooks or [])

        extra_tools: list[t.Any] = []
        registry_hooks: list[t.Any] = []
        if self.registry is not None:
            extra_tools.extend(self.registry.all_tools() or [])
            registry_hooks.extend(self.registry.all_hooks() or [])

        # Dedup tools by name (registry pool wins; capability tools backfill).
        seen_names = {getattr(t, "name", None) for t in extra_tools}
        for tool in capability_tools:
            name = getattr(tool, "name", None)
            if name and name in seen_names:
                continue
            extra_tools.append(tool)
            seen_names.add(name)

        policy_hooks: list[t.Any] = []
        if self.policy_factory is not None:
            policy = self.policy_factory()
            policy_hooks = list(policy.hooks or [])

        extra_hooks = [*registry_hooks, *capability_hooks, *policy_hooks]

        agent = create_agent(
            self.model,
            capability=materialized.capability,
            agent_def=materialized.agent_def,
            extra_tools=extra_tools,
            extra_hooks=extra_hooks,
            system_prompt_append=self.system_prompt_append,
        )
        attach_capability_skills(agent=agent, capability=materialized.capability)
        return agent

    def _validate_candidate(self, candidate: dict[str, str]) -> None:
        for key, value in candidate.items():
            if not isinstance(value, str):
                raise TypeError(f"Candidate value for {key!r} must be a string.")
            if key not in self._components:
                raise ValueError(f"Unknown candidate component: {key}")

    def _build_component_map(
        self,
        capability: Capability,
        agent_def: AgentDef,
    ) -> dict[str, _EditableComponent]:
        components: dict[str, _EditableComponent] = {}

        if "agent_prompt" in self.allowed_surfaces:
            agent_file = self._resolve_agent_file(capability, agent_def.name)
            components["agent_prompt"] = _EditableComponent(
                key="agent_prompt",
                relative_path=agent_file.relative_to(capability.path),
                kind="agent_prompt",
                name=agent_def.name,
            )

        if "capability_prompt" in self.allowed_surfaces:
            components["capability_prompt"] = _EditableComponent(
                key="capability_prompt",
                relative_path=Path("system-prompt.md"),
                kind="capability_prompt",
            )

        if "skill_descriptions" in self.allowed_surfaces or "skill_bodies" in self.allowed_surfaces:
            for skill_file in self._resolve_skill_files(capability):
                frontmatter, _body = self._read_markdown_with_frontmatter(skill_file)
                skill_name = str(frontmatter.get("name") or skill_file.parent.name)
                relative_path = skill_file.relative_to(capability.path)
                if "skill_descriptions" in self.allowed_surfaces:
                    key = skill_description_component(skill_name)
                    components[key] = _EditableComponent(
                        key=key,
                        relative_path=relative_path,
                        kind="skill_description",
                        name=skill_name,
                    )
                if "skill_bodies" in self.allowed_surfaces:
                    key = skill_body_component(skill_name)
                    components[key] = _EditableComponent(
                        key=key,
                        relative_path=relative_path,
                        kind="skill_body",
                        name=skill_name,
                    )

        return components

    def _resolve_dataset_input_mapping(
        self,
        batch: list[dict[str, t.Any]],
    ) -> list[str] | dict[str, str]:
        if self.dataset_input_mapping is not None:
            return self.dataset_input_mapping
        if not batch:
            return {self.goal_field: "goal"}
        first_row = batch[0]
        if self.goal_field in first_row:
            return {self.goal_field: "goal"}
        if len(first_row) == 1:
            first_key = next(iter(first_row))
            return {first_key: "goal"}
        raise ValueError(
            "Capability optimization examples must provide a goal field or an explicit dataset_input_mapping."
        )

    def _sample_score(self, sample: t.Any) -> float:
        if self.score_name is not None:
            metric = sample.metrics.get(self.score_name)
            if metric is not None and metric.value is not None:
                return float(metric.value)
            return 0.0

        metric_values = [
            metric.value for metric in sample.metrics.values() if metric.value is not None
        ]
        if len(metric_values) == 1:
            return float(metric_values[0])
        if "score" in sample.metrics and sample.metrics["score"].value is not None:
            return float(sample.metrics["score"].value)
        return 1.0 if sample.passed else 0.0

    def _serialize_sample(self, sample: t.Any) -> dict[str, t.Any]:
        output = sample.output
        turns: list[dict[str, t.Any]] | None = None
        output_summary: str | None = None
        if isinstance(output, Trajectory):
            turns = trajectory_to_turns(output)
            output_summary = output.get_summary()

        return {
            "input": sample.input,
            "output": output_summary,
            "metrics": self._metric_scores(sample),
            "passed": sample.passed,
            "error": str(sample.error) if sample.error else None,
            "turns": turns,
        }

    def _metric_scores(self, sample: t.Any) -> dict[str, float]:
        return {
            name: float(metric.value)
            for name, metric in sample.metrics.items()
            if metric.value is not None
        }

    def _format_feedback(self, *, score: float, trajectory: dict[str, t.Any]) -> str:
        parts = [f"Score: {score:.4f}"]
        error = trajectory.get("error")
        if error:
            parts.append(f"Error: {error}")
        metrics = trajectory.get("metrics")
        if metrics:
            parts.append(f"Metrics: {metrics}")
        return " | ".join(parts)

    def _build_proposal_prompt(
        self,
        *,
        candidate: dict[str, str],
        reflective_dataset: dict[str, list[dict[str, t.Any]]],
        components_to_update: list[str],
    ) -> str:
        payload = {
            "objective": self.objective
            or "Improve the capability without regressing holdout quality.",
            "capability": self.capability.name,
            "target_agent": self._agent_def.name,
            "components_to_update": components_to_update,
            "current_candidate": {
                component: candidate.get(component, "") for component in components_to_update
            },
            "reflective_dataset": {
                component: reflective_dataset.get(component, [])
                for component in components_to_update
            },
        }
        request_json = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True)
        return (
            "Generate improved replacement text for the listed capability components.\n"
            "Return JSON only with this exact shape:\n"
            '{"proposals":{"<component>":"<full replacement text>"},'
            '"rationale":"<optional short note>"}\n'
            "Rules:\n"
            "- include every component in components_to_update\n"
            "- keys must exactly match the provided component names\n"
            "- values must be the full replacement text, not a diff\n"
            "- make one general improvement, not benchmark-specific hacks\n"
            "- preserve valid existing text when the evidence is weak\n\n"
            f"{request_json}"
        )

    @staticmethod
    def _extract_completion_text(output: t.Any) -> str:
        if isinstance(output, Trajectory):
            for message in reversed(output.messages):
                if getattr(message, "role", None) != "assistant":
                    continue
                content = getattr(message, "content", "")
                if isinstance(content, str):
                    return content
                if isinstance(content, list):
                    return "".join(
                        block.get("text", "") if isinstance(block, dict) else str(block)
                        for block in content
                    )
            return output.get_summary()
        messages = getattr(output, "messages", None)
        if isinstance(messages, list):
            for message in reversed(messages):
                if getattr(message, "role", None) == "assistant":
                    return str(getattr(message, "content", ""))
        return str(output)

    @staticmethod
    def _parse_proposal_response(raw: str) -> CapabilityProposalResponse:
        text = raw.strip()
        fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
        if fenced:
            text = fenced.group(1).strip()
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start < 0 or end < start:
                raise
            payload = json.loads(text[start : end + 1])
        return CapabilityProposalResponse.model_validate(payload)

    @staticmethod
    def _resolve_agent_def(capability: Capability, agent_name: str | None) -> AgentDef:
        if not capability.agents:
            raise ValueError(f"Capability {capability.name!r} does not expose any agents")
        if agent_name is None:
            return capability.agents[0]
        for candidate in capability.agents:
            if candidate.name == agent_name:
                return candidate
        raise ValueError(f"Agent {agent_name!r} was not found in capability {capability.name!r}")

    @staticmethod
    def _resolve_agent_file(capability: Capability, agent_name: str) -> Path:
        agents_dir = capability.path / "agents"
        if not agents_dir.exists():
            raise FileNotFoundError(f"Capability {capability.name!r} has no agents directory")

        for file_path in sorted(agents_dir.rglob("*.md")):
            frontmatter, _body = StackAwareCapabilityAdapter._read_markdown_with_frontmatter(
                file_path
            )
            resolved_name = str(frontmatter.get("name") or file_path.stem)
            if resolved_name == agent_name:
                return file_path

        raise FileNotFoundError(
            f"Could not resolve an agent file for agent {agent_name!r} in {capability.path}"
        )

    @staticmethod
    def _resolve_skill_files(capability: Capability) -> list[Path]:
        skill_files: list[Path] = []
        for skills_path in capability.skills_paths or []:
            skill_file = skills_path / "SKILL.md"
            if skill_file.exists():
                skill_files.append(skill_file)
        fallback_root = capability.path / "skills"
        if fallback_root.exists():
            skill_files.extend(fallback_root.rglob("SKILL.md"))
        deduped = {path.resolve(): path for path in skill_files}
        skill_files = list(deduped.values())
        return sorted(skill_files)

    @staticmethod
    def _read_markdown_with_frontmatter(path: Path) -> tuple[dict[str, t.Any], str]:
        content = path.read_text()
        frontmatter, body = _parse_frontmatter(content)
        return dict(frontmatter or {}), body

    @staticmethod
    def _render_markdown_with_frontmatter(
        frontmatter: dict[str, t.Any],
        body: str,
    ) -> str:
        serialized = yaml.safe_dump(
            frontmatter,
            sort_keys=False,
            default_flow_style=False,
        ).rstrip()
        normalized_body = body.rstrip()
        if not normalized_body:
            return f"---\n{serialized}\n---\n"
        return f"---\n{serialized}\n---\n{normalized_body}\n"

    def _write_agent_prompt(self, root: Path, body: str) -> None:
        component = self._components["agent_prompt"]
        path = root / component.relative_path
        frontmatter, _existing_body = self._read_markdown_with_frontmatter(path)
        path.write_text(self._render_markdown_with_frontmatter(frontmatter, body))

    def _write_capability_prompt(self, root: Path, body: str) -> None:
        path = root / "system-prompt.md"
        normalized_body = body.rstrip()
        if not normalized_body:
            if path.exists():
                path.write_text("")
            return
        path.write_text(f"{normalized_body}\n")

    def _write_component(self, root: Path, component: _EditableComponent, value: str) -> None:
        path = root / component.relative_path
        frontmatter, body = self._read_markdown_with_frontmatter(path)

        if component.kind == "skill_description":
            frontmatter["description"] = value
            path.write_text(self._render_markdown_with_frontmatter(frontmatter, body))
            return

        if component.kind == "skill_body":
            path.write_text(self._render_markdown_with_frontmatter(frontmatter, value))
            return

        raise ValueError(f"Unsupported component kind: {component.kind}")
