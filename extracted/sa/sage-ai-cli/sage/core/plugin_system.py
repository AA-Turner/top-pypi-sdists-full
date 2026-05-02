"""Plugin integration system for SAGE model-driven orchestration.

This module provides a typed plugin contract, registry, planner, and executor
so SAGE can integrate external capability logic through a consistent Python API.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

from sage.devops import CICDMonitor, GitHubOps, GitOps
from sage.plugins.catalog import iter_claude_plugin_groups


class PluginErrorType(Enum):
    """Normalized error categories for plugin execution."""

    VALIDATION = "validation"
    AUTH = "auth"
    TIMEOUT = "timeout"
    DEPENDENCY = "dependency"
    NOT_FOUND = "not_found"
    INTERNAL = "internal"


@dataclass(frozen=True)
class PluginCapability:
    """Describes one callable plugin capability."""

    plugin_id: str
    name: str
    description: str
    mutating: bool = False
    tags: tuple[str, ...] = ()

    @property
    def key(self) -> str:
        return f"{self.plugin_id}.{self.name}"

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation."""
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "key": self.key,
            "description": self.description,
            "mutating": self.mutating,
            "tags": list(self.tags),
        }


@dataclass
class PluginInvocation:
    """A normalized plugin action request."""

    capability_key: str
    args: dict[str, Any] = field(default_factory=dict)
    idempotency_key: str | None = None
    timeout_seconds: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation."""
        return {
            "capability_key": self.capability_key,
            "args": self.args,
            "idempotency_key": self.idempotency_key,
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass
class PluginInvocationResult:
    """A normalized plugin action result."""

    capability_key: str
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    error_type: PluginErrorType | None = None
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a serializable representation."""
        return {
            "capability_key": self.capability_key,
            "success": self.success,
            "data": self.data,
            "error_type": self.error_type.value if self.error_type else None,
            "error_message": self.error_message,
        }


class PluginAdapter(Protocol):
    """Adapter contract for plugin integrations."""

    @property
    def plugin_id(self) -> str: ...

    def capabilities(self) -> list[PluginCapability]: ...

    def invoke(self, capability_name: str, args: dict[str, Any]) -> dict[str, Any]: ...


def _parse_jsonish(value: Any) -> dict[str, Any]:
    """Parse model output into dict in a permissive but predictable way."""
    if value is None:
        return {}
    if isinstance(value, dict):
        # Some providers wrap the real JSON payload in "result" or "response".
        for wrapped_key in (
            "actions",
            "plugin_actions",
            "tool_calls",
            "result",
            "response",
            "raw_text",
        ):
            wrapped_value = value.get(wrapped_key)
            if isinstance(wrapped_value, str):
                parsed_wrapped = _parse_jsonish(wrapped_value)
                if parsed_wrapped:
                    if wrapped_key in {"actions", "plugin_actions", "tool_calls"}:
                        if "actions" not in parsed_wrapped:
                            parsed_wrapped["actions"] = parsed_wrapped.get("items", [])
                    return parsed_wrapped
        return value
    if isinstance(value, list):
        return {"items": value, "actions": value}
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return {}
        try:
            parsed = json.loads(text)
        except (json.JSONDecodeError, TypeError):
            return {"raw_text": text}
        return _parse_jsonish(parsed)
    return {"raw_value": str(value)}


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-zA-Z0-9_]+", text.lower()) if len(token) >= 3}


def _derive_workflow_steps(
    workflow_steps: Any,
    instruction_markdown: str,
    *,
    limit: int = 25,
) -> list[str]:
    """Normalize workflow steps with fallback extraction from instructions."""
    if isinstance(workflow_steps, list):
        normalized = [str(step).strip() for step in workflow_steps if str(step).strip()]
        if normalized:
            return normalized[:limit]
    if not instruction_markdown:
        return []
    steps: list[str] = []
    for line in instruction_markdown.splitlines():
        text = line.strip()
        if not text:
            continue
        if re.match(r"^\d+[.)]\s+", text):
            cleaned = re.sub(r"^\d+[.)]\s*", "", text).strip()
            if cleaned:
                steps.append(cleaned)
        elif re.match(r"^[-*]\s+", text):
            cleaned = re.sub(r"^[-*]\s*", "", text).strip()
            if cleaned:
                steps.append(cleaned)
    deduped: list[str] = []
    seen: set[str] = set()
    for step in steps:
        if step in seen:
            continue
        seen.add(step)
        deduped.append(step)
    return deduped[:limit]


class PluginRegistry:
    """Registry for plugin adapters and their capabilities."""

    def __init__(self) -> None:
        self._adapters: dict[str, PluginAdapter] = {}
        self._capabilities: dict[str, PluginCapability] = {}

    def register(self, adapter: PluginAdapter) -> None:
        self._adapters[adapter.plugin_id] = adapter
        for capability in adapter.capabilities():
            if capability.key in self._capabilities:
                raise ValueError(f"Duplicate plugin capability key: {capability.key}")
            self._capabilities[capability.key] = capability

    def list_capabilities(self) -> list[PluginCapability]:
        return sorted(self._capabilities.values(), key=lambda c: c.key)

    def get_capability(self, key: str) -> PluginCapability | None:
        return self._capabilities.get(key)

    def get_adapter_for_capability(self, key: str) -> tuple[PluginAdapter | None, str]:
        capability = self._capabilities.get(key)
        if capability is None:
            return None, ""
        adapter = self._adapters.get(capability.plugin_id)
        return adapter, capability.name


class PluginExecutor:
    """Executes normalized plugin invocations with guardrails."""

    def __init__(self, registry: PluginRegistry) -> None:
        self._registry = registry

    def execute(
        self,
        invocation: PluginInvocation,
        *,
        allow_mutating: bool = False,
    ) -> PluginInvocationResult:
        capability = self._registry.get_capability(invocation.capability_key)
        if capability is None:
            return PluginInvocationResult(
                capability_key=invocation.capability_key,
                success=False,
                error_type=PluginErrorType.NOT_FOUND,
                error_message=f"Unknown capability: {invocation.capability_key}",
            )

        if capability.mutating and not allow_mutating:
            return PluginInvocationResult(
                capability_key=invocation.capability_key,
                success=False,
                error_type=PluginErrorType.VALIDATION,
                error_message=f"Mutating capability blocked: {invocation.capability_key}",
            )

        adapter, capability_name = self._registry.get_adapter_for_capability(
            invocation.capability_key
        )
        if adapter is None:
            return PluginInvocationResult(
                capability_key=invocation.capability_key,
                success=False,
                error_type=PluginErrorType.DEPENDENCY,
                error_message=f"No adapter for capability: {invocation.capability_key}",
            )

        try:
            data = adapter.invoke(capability_name, invocation.args)
            return PluginInvocationResult(
                capability_key=invocation.capability_key,
                success=True,
                data=data if isinstance(data, dict) else {"result": data},
            )
        except ValueError as exc:
            return PluginInvocationResult(
                capability_key=invocation.capability_key,
                success=False,
                error_type=PluginErrorType.VALIDATION,
                error_message=str(exc),
            )
        except TimeoutError as exc:
            return PluginInvocationResult(
                capability_key=invocation.capability_key,
                success=False,
                error_type=PluginErrorType.TIMEOUT,
                error_message=str(exc),
            )
        except PermissionError as exc:
            return PluginInvocationResult(
                capability_key=invocation.capability_key,
                success=False,
                error_type=PluginErrorType.AUTH,
                error_message=str(exc),
            )
        except Exception as exc:  # pragma: no cover - defensive
            return PluginInvocationResult(
                capability_key=invocation.capability_key,
                success=False,
                error_type=PluginErrorType.INTERNAL,
                error_message=str(exc),
            )


class AIPluginPlanner:
    """Uses the model to plan plugin invocations from the current task."""

    def __init__(self, send: Callable[[str], dict[str, Any] | str | list[Any] | None]):
        self._send = send

    def plan_actions(
        self,
        task: str,
        capabilities: list[PluginCapability],
    ) -> list[PluginInvocation]:
        capability_lines = "\n".join(f"- {cap.key}: {cap.description}" for cap in capabilities)
        prompt = (
            "Given this task, decide which plugin capabilities should be called.\n"
            "Return JSON with key `actions` as a list of objects:\n"
            "{capability_key: str, args: object}\n"
            "Only use capability keys from the list below.\n\n"
            f"TASK: {task}\n\n"
            f"CAPABILITIES:\n{capability_lines}\n\n"
            "Respond ONLY with valid JSON."
        )

        raw = self._send(prompt)
        parsed = _parse_jsonish(raw)
        actions = (
            parsed.get("actions")
            or parsed.get("plugin_actions")
            or parsed.get("tool_calls")
            or parsed.get("items")
        )
        if not isinstance(actions, list):
            return self._fallback_plan_actions(task, capabilities)

        invocations: list[PluginInvocation] = []
        allowed_keys = {cap.key for cap in capabilities}
        for action in actions:
            if not isinstance(action, dict):
                continue
            key = action.get("capability_key")
            if not isinstance(key, str) or key not in allowed_keys:
                continue
            args = action.get("args")
            invocations.append(
                PluginInvocation(
                    capability_key=key,
                    args=args if isinstance(args, dict) else {},
                )
            )
        if invocations:
            return invocations
        return self._fallback_plan_actions(task, capabilities)

    def _fallback_plan_actions(
        self,
        task: str,
        capabilities: list[PluginCapability],
    ) -> list[PluginInvocation]:
        """Heuristic fallback when model returns no usable plugin actions."""
        task_tokens = _tokenize(task)
        if not task_tokens:
            return []
        scored: list[tuple[int, PluginCapability]] = []
        for capability in capabilities:
            if capability.mutating:
                continue
            haystack = " ".join(
                [
                    capability.key,
                    capability.description,
                    " ".join(capability.tags),
                ]
            )
            cap_tokens = _tokenize(haystack)
            overlap = len(task_tokens & cap_tokens)
            if overlap > 0:
                scored.append((overlap, capability))
        scored.sort(key=lambda item: (-item[0], item[1].key))
        selected = [cap for _, cap in scored[:3]]
        return [
            PluginInvocation(capability_key=cap.key, args={"selection": "fallback"})
            for cap in selected
        ]


class GitDevOpsAdapter:
    """Plugin adapter over `sage.devops.git.GitOps`."""

    plugin_id = "devops.git"

    def __init__(self, repo_path: Path | str | None = None) -> None:
        self._ops = GitOps(repo_path)

    def capabilities(self) -> list[PluginCapability]:
        return [
            PluginCapability(self.plugin_id, "status", "Get git repository status"),
            PluginCapability(self.plugin_id, "diff", "Get git diff", tags=("read_only",)),
            PluginCapability(
                self.plugin_id,
                "create_branch",
                "Create git branch",
                mutating=True,
                tags=("mutating",),
            ),
        ]

    def invoke(self, capability_name: str, args: dict[str, Any]) -> dict[str, Any]:
        if capability_name == "status":
            status = self._ops.get_status()
            return {
                "branch": status.branch,
                "is_clean": status.is_clean,
                "staged_files": status.staged_files,
                "modified_files": status.modified_files,
                "untracked_files": status.untracked_files,
            }
        if capability_name == "diff":
            return {"diff": self._ops.get_diff(staged=bool(args.get("staged", False)))}
        if capability_name == "create_branch":
            name = str(args.get("name", "")).strip()
            if not name:
                raise ValueError("Missing required arg: name")
            self._ops.create_branch(name, checkout=bool(args.get("checkout", True)))
            return {"created": True, "name": name}
        raise ValueError(f"Unsupported capability: {capability_name}")


class GitHubDevOpsAdapter:
    """Plugin adapter over `sage.devops.github.GitHubOps`."""

    plugin_id = "devops.github"

    def __init__(self, repo_path: Path | str | None = None) -> None:
        self._ops = GitHubOps(repo_path)

    def capabilities(self) -> list[PluginCapability]:
        return [
            PluginCapability(self.plugin_id, "repo_info", "Get GitHub repository information"),
            PluginCapability(self.plugin_id, "list_prs", "List pull requests"),
            PluginCapability(self.plugin_id, "get_pr", "Get pull request details"),
        ]

    def invoke(self, capability_name: str, args: dict[str, Any]) -> dict[str, Any]:
        if capability_name == "repo_info":
            return {"repo": self._ops.get_repo_info()}
        if capability_name == "list_prs":
            prs = self._ops.list_prs(
                state=str(args.get("state", "open")),
                limit=int(args.get("limit", 10)),
            )
            return {
                "prs": [
                    {
                        "number": pr.number,
                        "title": pr.title,
                        "state": pr.state.name,
                        "url": pr.url,
                    }
                    for pr in prs
                ]
            }
        if capability_name == "get_pr":
            number = int(args.get("number", 0))
            if number <= 0:
                raise ValueError("Missing required arg: number")
            pr = self._ops.get_pr(number)
            if pr is None:
                return {"pr": None}
            return {
                "pr": {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state.name,
                    "url": pr.url,
                    "head_branch": pr.head_branch,
                    "base_branch": pr.base_branch,
                }
            }
        raise ValueError(f"Unsupported capability: {capability_name}")


class CICDDevOpsAdapter:
    """Plugin adapter over `sage.devops.ci_cd.CICDMonitor`."""

    plugin_id = "devops.cicd"

    def __init__(self, repo_path: Path | str | None = None) -> None:
        self._ops = CICDMonitor(repo_path)

    def capabilities(self) -> list[PluginCapability]:
        return [
            PluginCapability(self.plugin_id, "workflow_files", "List CI workflow files"),
            PluginCapability(self.plugin_id, "latest_pipeline", "Get latest CI pipeline"),
        ]

    def invoke(self, capability_name: str, args: dict[str, Any]) -> dict[str, Any]:
        if capability_name == "workflow_files":
            files = self._ops.get_workflow_files()
            return {"files": [str(f) for f in files]}
        if capability_name == "latest_pipeline":
            branch = args.get("branch")
            pipeline = self._ops.get_latest_pipeline(
                branch=str(branch) if isinstance(branch, str) else None
            )
            if pipeline is None:
                return {"pipeline": None}
            return {
                "pipeline": {
                    "id": pipeline.id,
                    "status": pipeline.status.name,
                    "branch": pipeline.branch,
                    "commit_sha": pipeline.commit_sha,
                }
            }
        raise ValueError(f"Unsupported capability: {capability_name}")


class ImportedSkillAdapter:
    """Adapter for imported Claude plugin capabilities vendored into the repo."""

    def __init__(
        self,
        plugin_name: str,
        plugin_description: str,
        skills: list[dict[str, Any]],
        commands: list[dict[str, Any]] | None = None,
        agents: list[dict[str, Any]] | None = None,
        mcp_servers: list[dict[str, Any]] | None = None,
    ) -> None:
        self._plugin_name = plugin_name.strip()
        self._plugin_description = plugin_description.strip()
        self._skills = skills
        self._commands = commands or []
        self._agents = agents or []
        self._mcp_servers = mcp_servers or []
        self.plugin_id = f"claude.{self._plugin_name}" if self._plugin_name else "claude.unknown"

    def _build_execution_prompt(
        self,
        *,
        capability_type: str,
        capability_name: str,
        description: str,
        instruction_markdown: str,
        workflow_steps: list[str],
        args: dict[str, Any],
    ) -> str:
        """Build model-ready execution prompt from imported Claude capability logic."""
        rendered_steps = (
            "\n".join(f"{index + 1}. {step}" for index, step in enumerate(workflow_steps))
            or "1. Interpret the instruction markdown and determine executable steps."
        )
        instruction = instruction_markdown.strip()
        if instruction:
            instruction = instruction[:6000]
        else:
            instruction = "(No explicit instruction markdown provided.)"
        return (
            "Use the imported Claude plugin logic below to produce an executable plan.\n"
            "Return JSON with keys: plan_steps (list), checks (list), suggested_commands (list), "
            "notes (list).\n\n"
            f"PLUGIN: {self._plugin_name}\n"
            f"CAPABILITY_TYPE: {capability_type}\n"
            f"CAPABILITY_NAME: {capability_name}\n"
            f"DESCRIPTION: {description}\n"
            f"ARGS: {json.dumps(args, default=str)}\n\n"
            f"WORKFLOW_STEPS:\n{rendered_steps}\n\n"
            f"INSTRUCTION_MARKDOWN:\n{instruction}\n"
        )

    def capabilities(self) -> list[PluginCapability]:
        capabilities: list[PluginCapability] = []
        for skill in self._skills:
            skill_name = str(skill.get("skill", "")).strip()
            description = str(skill.get("description", "")).strip()
            if not skill_name:
                continue
            capabilities.append(
                PluginCapability(
                    self.plugin_id,
                    skill_name,
                    description or f"Imported workflow skill: {skill_name}",
                    mutating=False,
                    tags=("procedural", "imported"),
                )
            )
        for command in self._commands:
            command_name = str(command.get("command", "")).strip()
            description = str(command.get("description", "")).strip()
            if not command_name:
                continue
            capabilities.append(
                PluginCapability(
                    self.plugin_id,
                    f"command.{command_name}",
                    description or f"Imported command: {command_name}",
                    mutating=False,
                    tags=("command", "imported"),
                )
            )
        for agent in self._agents:
            agent_name = str(agent.get("agent", "")).strip()
            description = str(agent.get("description", "")).strip()
            if not agent_name:
                continue
            capabilities.append(
                PluginCapability(
                    self.plugin_id,
                    f"agent.{agent_name}",
                    description or f"Imported agent: {agent_name}",
                    mutating=False,
                    tags=("agent", "imported"),
                )
            )
        for server in self._mcp_servers:
            server_name = str(server.get("server", "")).strip()
            description = str(server.get("description", "")).strip()
            if not server_name:
                continue
            capabilities.append(
                PluginCapability(
                    self.plugin_id,
                    f"mcp.{server_name}",
                    description or f"Imported MCP server: {server_name}",
                    mutating=False,
                    tags=("mcp", "imported"),
                )
            )
        return capabilities

    def invoke(self, capability_name: str, args: dict[str, Any]) -> dict[str, Any]:
        for skill in self._skills:
            skill_name = str(skill.get("skill", "")).strip()
            if skill_name != capability_name:
                continue
            instruction_markdown = str(skill.get("instruction_markdown", "")).strip()
            workflow_steps = _derive_workflow_steps(
                skill.get("workflow_steps", []),
                instruction_markdown,
            )
            description = str(skill.get("description", "")).strip()
            return {
                "plugin": self._plugin_name,
                "plugin_description": self._plugin_description,
                "capability_type": "skill",
                "capability_name": skill_name,
                "skill": skill_name,
                "description": description,
                "default_prompt": str(skill.get("default_prompt", "")).strip(),
                "workflow_steps": workflow_steps,
                "instruction_markdown": instruction_markdown,
                "source_file": str(skill.get("source_file", "")).strip(),
                "execution_prompt": self._build_execution_prompt(
                    capability_type="skill",
                    capability_name=skill_name,
                    description=description,
                    instruction_markdown=instruction_markdown,
                    workflow_steps=workflow_steps,
                    args=args,
                ),
                "args": args,
            }

        if capability_name.startswith("command."):
            command_name = capability_name.removeprefix("command.")
            for command in self._commands:
                if str(command.get("command", "")).strip() != command_name:
                    continue
                instruction_markdown = str(command.get("instruction_markdown", "")).strip()
                workflow_steps = _derive_workflow_steps(
                    command.get("workflow_steps", []),
                    instruction_markdown,
                )
                description = str(command.get("description", "")).strip()
                return {
                    "plugin": self._plugin_name,
                    "plugin_description": self._plugin_description,
                    "capability_type": "command",
                    "capability_name": command_name,
                    "command": command_name,
                    "description": description,
                    "workflow_steps": workflow_steps,
                    "instruction_markdown": instruction_markdown,
                    "source_file": str(command.get("source_file", "")).strip(),
                    "execution_prompt": self._build_execution_prompt(
                        capability_type="command",
                        capability_name=command_name,
                        description=description,
                        instruction_markdown=instruction_markdown,
                        workflow_steps=workflow_steps,
                        args=args,
                    ),
                    "args": args,
                }

        if capability_name.startswith("agent."):
            agent_name = capability_name.removeprefix("agent.")
            for agent in self._agents:
                if str(agent.get("agent", "")).strip() != agent_name:
                    continue
                instruction_markdown = str(agent.get("instruction_markdown", "")).strip()
                default_prompt = str(agent.get("default_prompt", "")).strip()
                workflow_steps = _derive_workflow_steps([], instruction_markdown or default_prompt)
                description = str(agent.get("description", "")).strip()
                return {
                    "plugin": self._plugin_name,
                    "plugin_description": self._plugin_description,
                    "capability_type": "agent",
                    "capability_name": agent_name,
                    "agent": agent_name,
                    "description": description,
                    "default_prompt": default_prompt,
                    "instruction_markdown": instruction_markdown,
                    "workflow_steps": workflow_steps,
                    "source_file": str(agent.get("source_file", "")).strip(),
                    "execution_prompt": self._build_execution_prompt(
                        capability_type="agent",
                        capability_name=agent_name,
                        description=description,
                        instruction_markdown=instruction_markdown or default_prompt,
                        workflow_steps=workflow_steps,
                        args=args,
                    ),
                    "args": args,
                }

        if capability_name.startswith("mcp."):
            server_name = capability_name.removeprefix("mcp.")
            for server in self._mcp_servers:
                if str(server.get("server", "")).strip() != server_name:
                    continue
                description = str(server.get("description", "")).strip()
                command = str(server.get("command", "")).strip()
                url = str(server.get("url", "")).strip()
                transport = str(server.get("transport", "")).strip()
                instruction_markdown = (
                    f"Use MCP server `{server_name}` via transport `{transport}`. "
                    f"URL: {url or 'N/A'} Command: {command or 'N/A'}."
                )
                return {
                    "plugin": self._plugin_name,
                    "plugin_description": self._plugin_description,
                    "capability_type": "mcp",
                    "capability_name": server_name,
                    "mcp_server": server_name,
                    "description": description,
                    "transport": transport,
                    "url": url,
                    "command": command,
                    "workflow_steps": _derive_workflow_steps([], instruction_markdown),
                    "instruction_markdown": instruction_markdown,
                    "execution_prompt": self._build_execution_prompt(
                        capability_type="mcp",
                        capability_name=server_name,
                        description=description,
                        instruction_markdown=instruction_markdown,
                        workflow_steps=_derive_workflow_steps([], instruction_markdown),
                        args=args,
                    ),
                    "args": args,
                    "server_args": server.get("args", []),
                }
        raise ValueError(f"Unsupported capability: {capability_name}")


def build_imported_skill_adapters() -> list[ImportedSkillAdapter]:
    """Build adapters from the vendored plugin catalog snapshot."""
    adapters: list[ImportedSkillAdapter] = []
    for group in iter_claude_plugin_groups():
        plugin_name = str(group.get("name", "")).strip()
        if not plugin_name:
            continue
        plugin_description = str(group.get("description", "")).strip()
        skills = group.get("skills", [])
        commands = group.get("commands", [])
        agents = group.get("agents", [])
        mcp_servers = group.get("mcp_servers", [])
        has_any_caps = any(
            isinstance(collection, list) and bool(collection)
            for collection in (skills, commands, agents, mcp_servers)
        )
        if not has_any_caps:
            continue
        adapters.append(
            ImportedSkillAdapter(
                plugin_name,
                plugin_description,
                skills if isinstance(skills, list) else [],
                commands if isinstance(commands, list) else [],
                agents if isinstance(agents, list) else [],
                mcp_servers if isinstance(mcp_servers, list) else [],
            )
        )
    return adapters


def build_default_plugin_registry(repo_path: Path | str | None = None) -> PluginRegistry:
    """Create a default plugin registry using built-in DevOps adapters."""
    registry = PluginRegistry()
    registry.register(GitDevOpsAdapter(repo_path))
    registry.register(GitHubDevOpsAdapter(repo_path))
    registry.register(CICDDevOpsAdapter(repo_path))
    for adapter in build_imported_skill_adapters():
        registry.register(adapter)
    return registry


__all__ = [
    "AIPluginPlanner",
    "CICDDevOpsAdapter",
    "GitDevOpsAdapter",
    "GitHubDevOpsAdapter",
    "ImportedSkillAdapter",
    "PluginAdapter",
    "PluginCapability",
    "PluginErrorType",
    "PluginExecutor",
    "PluginInvocation",
    "PluginInvocationResult",
    "PluginRegistry",
    "build_default_plugin_registry",
    "build_imported_skill_adapters",
]
