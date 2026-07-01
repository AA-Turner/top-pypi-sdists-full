"""
cvc.agent.subagent — Sub-agent architecture (Claude Code-style).

Enables the parent agent to spawn lightweight child agents with:
  - Isolated context windows (no shared history with parent)
  - Restricted tool sets (e.g. read-only for Explore)
  - Configurable max turns and model selection
  - Single-string result returned to the parent

Built-in agents:
  - Explore: Fast read-only codebase exploration (cheapest model, read-only tools)
  - Plan:    Analyze and propose without modifying (current model, read-only tools)

Custom agents can be defined in `.cvc/agents/<name>/agent.md` with YAML frontmatter.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from collections.abc import Callable
from typing import Any

logger = logging.getLogger("cvc.agent.subagent")

# Read-only tools that sub-agents with restricted access can use
READ_ONLY_TOOLS = frozenset(
    {
        "read_file",
        "multi_read",
        "grep",
        "semantic_grep",
        "glob",
        "list_dir",
        "cvc_status",
        "cvc_log",
        "cvc_search",
        "cvc_smart_search",
        "cvc_diff",
        "cvc_document_search",
        "cvc_list_documents",
        "think",
        "todo",
        "web_fetch",
    }
)

# Full coding tools — read + write + execute
CODING_TOOLS = frozenset(
    {
        "read_file",
        "multi_read",
        "write_file",
        "edit_file",
        "multi_edit",
        "patch_file",
        "bash",
        "grep",
        "semantic_grep",
        "glob",
        "list_dir",
        "cvc_status",
        "cvc_log",
        "cvc_commit",
        "cvc_branch",
        "cvc_search",
        "cvc_smart_search",
        "cvc_diff",
        "web_search",
        "web_fetch",
        "think",
        "todo",
        "git",
    }
)

# Research tools — read + web
RESEARCH_TOOLS = frozenset(
    {
        "read_file",
        "multi_read",
        "grep",
        "semantic_grep",
        "glob",
        "list_dir",
        "bash",
        "web_search",
        "web_fetch",
        "cvc_status",
        "cvc_log",
        "cvc_search",
        "cvc_smart_search",
        "cvc_diff",
        "cvc_document_search",
        "cvc_list_documents",
        "think",
        "todo",
    }
)

# Orchestration tools — everything including sub-agents
ORCHESTRATION_TOOLS = frozenset(
    {
        "read_file",
        "multi_read",
        "write_file",
        "edit_file",
        "multi_edit",
        "patch_file",
        "bash",
        "grep",
        "semantic_grep",
        "glob",
        "list_dir",
        "web_search",
        "web_fetch",
        "agent",
        "parallel_agents",
        "cvc_status",
        "cvc_log",
        "cvc_commit",
        "cvc_branch",
        "cvc_restore",
        "cvc_merge",
        "cvc_search",
        "cvc_smart_search",
        "cvc_diff",
        "cvc_ingest_document",
        "cvc_document_search",
        "cvc_list_documents",
        "think",
        "todo",
        "context_compact",
        "git",
    }
)


@dataclass
class SubAgentConfig:
    """Configuration for a sub-agent."""

    name: str
    description: str = ""
    model: str = ""  # Empty = use parent's model
    tools: frozenset[str] = field(default_factory=lambda: READ_ONLY_TOOLS)
    max_turns: int = 10
    system_prompt: str = ""  # Additional instructions prepended to system prompt
    custom_instructions: str = ""  # From agent.md file


# ── Built-in agent configs ──────────────────────────────────────────────────

BUILTIN_AGENTS: dict[str, SubAgentConfig] = {
    "Explore": SubAgentConfig(
        name="Explore",
        description="Fast read-only codebase exploration. Cheapest model, read-only tools.",
        tools=READ_ONLY_TOOLS,
        # v2.88 — Raised baselines so big monorepo enumeration (the canonical
        # "Analyze entire project" prompt) completes without ever bumping the
        # ceiling. Dynamic expansion + stall detector still apply.
        max_turns=240,
        system_prompt=(
            "Read-only codebase explorer. Search and read files to answer the question. "
            "No file modifications. Be concise — return findings as a brief summary, "
            "not a narrative. Prefer tool calls over text.\n\n"
            "PRODUCTIVITY RULES:\n"
            "  • Never read the same file twice — the runtime caches reads anyway.\n"
            "  • Prefer `glob` + `multi_read` (batch) over single `read_file` storms.\n"
            "  • Use `list_dir` ONCE per directory — re-listing is wasted budget.\n"
            "  • If you've made >40 tool calls, START SYNTHESIZING — you have plenty.\n"
            "  • Stop the moment you can answer; do not exhaustively read every file."
        ),
    ),
    "Plan": SubAgentConfig(
        name="Plan",
        description="Read-only analysis and implementation planning.",
        tools=READ_ONLY_TOOLS,
        max_turns=80,
        system_prompt=(
            "Planning agent. Read-only access. Analyze codebase, return a structured "
            "plan: file paths, specific changes, ordering. No prose — just the plan."
        ),
    ),
    "Security": SubAgentConfig(
        name="Security",
        description="Security scanner: OWASP Top 10, CVEs, secrets, dependency audits.",
        tools=RESEARCH_TOOLS,
        max_turns=100,
        system_prompt=(
            "Security analyst. Scan for: OWASP Top 10, hardcoded secrets, CVEs, "
            "insecure crypto, access control flaws. Output: prioritized findings "
            "(CRITICAL→LOW) with file:line, description, fix. No filler text."
        ),
    ),
    "AI": SubAgentConfig(
        name="AI",
        description="AI/ML engineer: LLMs, RAG, embeddings, training, inference.",
        tools=CODING_TOOLS,
        max_turns=140,
        system_prompt=(
            "AI/ML engineer. Build production-grade AI systems in Python: LLM integrations, "
            "RAG pipelines, model training, inference optimization. Write clean async code "
            "with type hints. Use tools to implement — don't describe what you'd do."
        ),
    ),
    "UI": SubAgentConfig(
        name="UI",
        description="UI/UX and frontend: web, terminal TUI, CLI interfaces.",
        tools=CODING_TOOLS,
        max_turns=100,
        system_prompt=(
            "UI/UX developer. Build accessible, responsive interfaces: React, Vue, "
            "Tailwind, Rich/Textual TUI, CLI. Implement directly via tools. "
            "Prioritize UX. Keep explanations minimal."
        ),
    ),
    "Data": SubAgentConfig(
        name="Data",
        description="Data analytics/engineering: SQL, ETL, viz, statistics.",
        tools=CODING_TOOLS,
        max_turns=100,
        system_prompt=(
            "Data analyst/engineer. pandas, SQL, ETL, visualization. "
            "Validate data quality first. Implement via tools. "
            "Brief interpretations alongside code — no verbose explanations."
        ),
    ),
    "Orchestrator": SubAgentConfig(
        name="Orchestrator",
        description="Coordinates sub-agents for complex multi-domain tasks.",
        tools=ORCHESTRATION_TOOLS,
        max_turns=300,
        system_prompt=(
            "Orchestrator. Delegate to: Explore, Plan, Security, AI, UI, Data via "
            "'agent' tool. Decompose → delegate → integrate → verify. "
            "Can also directly edit files and run commands. Minimize narration."
        ),
    ),
}


def _get_cheap_model(provider: str, parent_model: str) -> str:
    """Pick the cheapest model for the given provider (for Explore agent)."""
    cheap_models = {
        "anthropic": "claude-haiku-4-5",
        "openai": "gpt-5-mini",
        "google": "gemini-3-flash-preview",
        "ollama": parent_model,  # Use whatever's loaded locally
        "lmstudio": parent_model,
    }
    return cheap_models.get(provider, parent_model)


def load_custom_agents(workspace: Path) -> dict[str, SubAgentConfig]:
    """Load custom agent definitions from .cvc/agents/<name>/agent.md."""
    agents_dir = workspace / ".cvc" / "agents"
    if not agents_dir.is_dir():
        return {}

    custom: dict[str, SubAgentConfig] = {}

    for agent_dir in agents_dir.iterdir():
        if not agent_dir.is_dir():
            continue

        agent_file = agent_dir / "agent.md"
        if not agent_file.exists():
            continue

        try:
            text = agent_file.read_text(encoding="utf-8")
            config = _parse_agent_md(agent_dir.name, text)
            if config:
                custom[config.name] = config
        except Exception as e:
            logger.warning("Failed to load agent %s: %s", agent_dir.name, e)

    return custom


def _parse_agent_md(name: str, text: str) -> SubAgentConfig | None:
    """Parse an agent.md file with optional YAML frontmatter."""
    frontmatter: dict[str, Any] = {}
    body = text

    # Extract YAML frontmatter (between --- markers)
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if fm_match:
        body = text[fm_match.end() :]
        try:
            import yaml

            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except ImportError:
            # Minimal YAML parsing fallback
            for line in fm_match.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k, v = k.strip(), v.strip()
                    if v.startswith("[") and v.endswith("]"):
                        v = [x.strip().strip("'\"") for x in v[1:-1].split(",")]
                    frontmatter[k] = v

    # Build tool set from frontmatter
    tools_list = frontmatter.get("tools", None)
    if isinstance(tools_list, list):
        tools = frozenset(tools_list)
    else:
        tools = READ_ONLY_TOOLS

    return SubAgentConfig(
        name=frontmatter.get("name", name),
        description=frontmatter.get("description", ""),
        model=frontmatter.get("model", ""),
        tools=tools,
        max_turns=int(frontmatter.get("max_turns", 10)),
        system_prompt=frontmatter.get("system_prompt", ""),
        custom_instructions=body.strip(),
    )


def get_available_agents(workspace: Path) -> dict[str, SubAgentConfig]:
    """Return all available agents (built-in + custom)."""
    agents = dict(BUILTIN_AGENTS)
    agents.update(load_custom_agents(workspace))
    return agents


class SubAgent:
    """
    Run an isolated sub-agent session and return its result.

    The sub-agent gets:
    - Its own context window (no shared history)
    - A restricted tool set
    - A configurable turn limit
    - A specialized system prompt
    """

    def __init__(
        self,
        config: SubAgentConfig,
        workspace: Path,
        provider: str,
        api_key: str,
        parent_model: str,
        base_url: str = "",
        event_emitter: "Callable[[dict], None] | None" = None,
        agent_index: int = 1,
        agent_total: int = 1,
        depth: int = 1,
    ) -> None:
        self.config = config
        self.workspace = workspace
        self.provider = provider
        self.api_key = api_key
        self.parent_model = parent_model
        self.base_url = base_url
        # Thread-safe callable invoked by the sub-agent runtime to surface
        # progress events (tool_start / tool_result / start / done) back to
        # the parent stream so the dashboard can render nested activity.
        # None → silent legacy behaviour (CLI, tests). Must never raise.
        self._emit = event_emitter
        # v2.83 — each SubAgent run carries a stable run_id so the dashboard
        # can render N concurrent panes (one per parallel sub-agent) instead
        # of collapsing them onto a single activity strip. agent_index and
        # agent_total let the UI render "Explore (2/3)" labels for parallel
        # spawns; default to 1/1 for single-agent runs.
        import uuid as _uuid
        self.run_id = _uuid.uuid4().hex[:12]
        self.agent_index = max(1, int(agent_index))
        self.agent_total = max(1, int(agent_total))
        # v2.84 — nesting depth. Top-level subagent = 1. When an
        # Orchestrator spawns parallel_agents, each child carries
        # depth = parent.depth + 1. Anti-recursion guard caps this so a
        # buggy LLM can't fork-bomb the runtime by recursively asking for
        # more Orchestrators. Read by parallel_agents callback in
        # gateway.py to choke off out-of-budget spawns.
        self.depth = max(1, int(depth))

    async def run(self, prompt: str) -> str:
        """Execute the sub-agent and return its final response."""
        from cvc.agent.llm import AgentLLM
        from cvc.agent.tools import AGENT_TOOLS, get_tools_for_provider

        # Pick model
        model = self.config.model
        if not model:
            if self.config.name == "Explore":
                model = _get_cheap_model(self.provider, self.parent_model)
            else:
                model = self.parent_model

        # Build LLM client for this sub-agent
        llm = AgentLLM(
            provider=self.provider,
            api_key=self.api_key,
            model=model,
            base_url=self.base_url,
        )

        # Attach the workspace's shared CognomeRuntime so the sub-agent
        # gets automatic memory (engram injection, scratchpad, handoff)
        # exactly like the parent agent.  Built lazily below from the
        # per-sub-agent engine; if construction fails we fall through
        # — memory is an enhancement, never a blocker.
        _sub_runtime = None

        try:
            # Filter tools to only those allowed by the config
            allowed_tools = [t for t in AGENT_TOOLS if t["function"]["name"] in self.config.tools]
            provider_tools = get_tools_for_provider(self.provider, allowed_tools)

            # Build system prompt
            sys_parts = []
            if self.config.system_prompt:
                sys_parts.append(self.config.system_prompt)
            if self.config.custom_instructions:
                sys_parts.append(self.config.custom_instructions)
            sys_parts.append(
                f"\nWorkspace: {self.workspace}\n"
                f"Sub-agent: {self.config.name}. "
                "Be terse. Use tools, not prose. Return only the essential answer."
            )

            messages: list[dict[str, Any]] = [
                {"role": "system", "content": "\n\n".join(sys_parts)},
                {"role": "user", "content": prompt},
            ]

            # Build a minimal executor for the sub-agent
            from cvc.agent.permissions import PermissionEngine
            from cvc.core.database import ContextDatabase
            from cvc.core.models import CVCConfig
            from cvc.operations.engine import CVCEngine

            config = CVCConfig.for_project(
                project_root=self.workspace,
                provider=self.provider,
                model=model,
                mode="cli",
            )
            config.ensure_dirs()
            db = ContextDatabase(config)
            engine = CVCEngine(config, db)

            # Wire the shared CognomeRuntime into the sub-agent LLM so
            # engram injection + scratchpad fire automatically on every
            # turn — matching CLI/Gateway semantics.
            try:
                from cvc.operations.cognome_runtime import CognomeRuntime

                _sub_runtime = CognomeRuntime.for_engine(engine)
                llm.set_memory_runtime(_sub_runtime)
            except Exception as _exc:  # pragma: no cover — defensive
                import logging as _logging

                _logging.getLogger("cvc.agent.subagent").debug(
                    "sub-agent memory wire failed (non-fatal): %s", _exc
                )

            # Sub-agent permission engine: only allow configured tools
            perm = PermissionEngine()
            from cvc.agent.permissions import PermissionRule

            for tool_name in self.config.tools:
                perm.add_rule(PermissionRule.parse(tool_name, "allow"))

            from cvc.agent.executor import ToolExecutor

            executor = ToolExecutor(self.workspace, engine, permission_engine=perm)
            # v2.84 — stamp this executor with the depth of THIS sub-agent
            # so gateway._parallel_cb (if reached via the parallel_agents
            # tool) knows the parent depth and can refuse over-deep nests.
            try:
                executor._subagent_depth = int(self.depth)
            except Exception:
                pass

            # ── Local helper: never raise out of the sub-agent loop ──
            # v2.83 — auto-stamp every event with run_id + cumulative
            # telemetry so the dashboard can:
            #   • Render N parallel agent panes keyed by run_id (no more
            #     three Explores collapsing onto one strip).
            #   • Show cumulative "47 tools · 92s" headline that doesn't
            #     reset on every turn boundary.
            import time as _t_mod
            _run_t0 = _t_mod.monotonic()
            _tools_run_total = 0  # incremented in tool dispatch loop below

            def _safe_emit(evt: dict) -> None:
                if self._emit is None:
                    return
                try:
                    # Stamp run-identity + cumulative telemetry. Never
                    # overwrite fields the caller already set.
                    evt.setdefault("run_id", self.run_id)
                    evt.setdefault("agent_index", self.agent_index)
                    evt.setdefault("agent_total", self.agent_total)
                    evt.setdefault(
                        "elapsed_total_s",
                        round(_t_mod.monotonic() - _run_t0, 1),
                    )
                    evt.setdefault("tools_run", _tools_run_total)
                    self._emit(evt)
                except Exception:
                    pass

            _safe_emit({
                "type": "subagent_start",
                "agent": self.config.name,
                "model": model,
            })

            # ── v2.74 self-tuning loop state ─────────────────────────────
            #   • read-cache: identical tool calls (read_file / multi_read /
            #     list_dir / glob / grep) return the cached result instead
            #     of re-burning a tool slot. This is what killed the
            #     Windows "Analyze the entire project" run — duplicate reads
            #     ate the whole budget.
            #   • dynamic max_turns: start at the configured value, expand
            #     up to a hard ceiling when productivity (novel tool calls /
            #     total tool calls in the last 3 turns) stays healthy, halt
            #     early when productivity collapses.
            #   • repeat-call refusal: after CVC_SUBAGENT_REPEAT_LIMIT
            #     identical invocations of the same (name,args), the agent
            #     gets a runtime nudge instead of another redundant result.
            #   • wall-clock watchdog: hard ceiling on real seconds so a
            #     subagent never silently runs forever even if novel-ratio
            #     stays artificially high (e.g. infinite directory descent).
            #   • mid-turn heartbeat: emits a subagent_progress event every
            #     CVC_SUBAGENT_HEARTBEAT_S while a single tool runs long, so
            #     the dashboard never goes dark.
            import os as _os, hashlib as _hashlib, json as _json, time as _time
            _CACHEABLE = {"read_file", "multi_read", "list_dir", "glob", "grep", "semantic_grep"}
            _tool_cache: dict[str, str] = {}
            _call_counts: dict[str, int] = {}  # arg-hash → invocation count
            _novel_window: list[tuple[int, int]] = []  # (novel, total) per turn
            _base_max_turns = max(1, int(self.config.max_turns))
            # v2.88 — Generous ceilings. Big monorepos genuinely need >400
            # turns to enumerate. Stall/repeat detectors still guard against
            # actual loops, so a higher ceiling is safe.
            _hard_ceiling = int(_os.environ.get("CVC_SUBAGENT_HARD_CEILING", "1000"))
            _max_turns = _base_max_turns
            # 60-minute wall budget by default. CVC_SUBAGENT_WALL_S=0 means
            # "no wall budget" (truly unlimited; only stall/repeat halts apply).
            _wall_budget_s = float(_os.environ.get("CVC_SUBAGENT_WALL_S", "3600"))
            _unlimited_wall = _wall_budget_s <= 0
            _repeat_limit = int(_os.environ.get("CVC_SUBAGENT_REPEAT_LIMIT", "3"))
            _stall_ratio = float(_os.environ.get("CVC_SUBAGENT_STALL_RATIO", "0.20"))
            # v2.88 — Tighter mid-tool heartbeat (5s default) so the dashboard
            # NEVER appears frozen during a long multi_read or grep.
            _heartbeat_s = float(_os.environ.get("CVC_SUBAGENT_HEARTBEAT_S", "5"))
            _t_start = _time.monotonic()
            _wall_warned = False

            def _arg_hash(name: str, args: dict) -> str:
                try:
                    ser = _json.dumps(args or {}, sort_keys=True, default=str)
                except Exception:
                    ser = str(args)
                return _hashlib.md5(f"{name}|{ser}".encode("utf-8", errors="replace")).hexdigest()  # noqa: S324

            def _narrate(turn_idx: int, tcs: list, novel: int, cached: int) -> str:
                """Build a human-readable progress line."""
                if not tcs:
                    return f"thinking… (turn {turn_idx+1}/{_max_turns})"
                # Summarise tool calls by name with counts
                from collections import Counter
                names = Counter(tc.name for tc in tcs)
                top = ", ".join(f"{k}×{v}" if v > 1 else k for k, v in names.most_common(3))
                cache_note = f" · {cached} cached" if cached else ""
                return f"turn {turn_idx+1}/{_max_turns} · {top}{cache_note}"
            # ─────────────────────────────────────────────────────────────

            # Agentic loop (simplified — no streaming, no commit)
            final_text = ""
            import json as _json

            for turn in range(10_000):  # bounded below by _max_turns
                if turn >= _max_turns:
                    break
                # ── Wall-clock watchdog: stop spending tokens once real-time
                #    budget is exhausted. Final turn allowed to produce text.
                #    v2.88 — _unlimited_wall=True (CVC_SUBAGENT_WALL_S=0)
                #    disables this entirely for power users.
                _elapsed_total = _time.monotonic() - _t_start
                if (not _unlimited_wall) and _elapsed_total > _wall_budget_s and not _wall_warned:
                    _wall_warned = True
                    messages.append({
                        "role": "user",
                        "content": (
                            f"[runtime] Wall-clock budget exhausted "
                            f"({int(_elapsed_total)}s > {int(_wall_budget_s)}s). "
                            "Stop calling tools and return your best answer NOW."
                        ),
                    })
                    _max_turns = min(_max_turns, turn + 2)
                response_text = ""
                tool_calls = []
                # Mirror gateway's pattern: streamed args arrive as string
                # deltas. Accumulate them in a separate buffer and parse to
                # dict on completion so tc.arguments stays well-typed.
                tool_call_args_buffer: dict[int, str] = {}

                # Collect full response.
                # AgentLLM exposes chat_stream (see cvc/agent/llm.py:393).
                # Older parallel/fallback paths used stream_chat — that name
                # only exists on FallbackChain, never on AgentLLM. Sub-agents
                # use AgentLLM directly, so call the right method.
                # v2.80: emit a "thinking" heartbeat on the first text_delta
                # of each turn so the dashboard never goes dark while the
                # model is generating (vs. running tools).
                # v2.88: also emit a periodic "still thinking" pulse every
                # _heartbeat_s seconds during long generations (slow models
                # or large outputs) so the UI shows continuous liveness.
                _thinking_announced = False
                _last_think_pulse = _time.monotonic()
                async for event in llm.chat_stream(
                    messages=messages,
                    tools=provider_tools,
                ):
                    if event.type == "text_delta":
                        if not _thinking_announced and not response_text:
                            _thinking_announced = True
                            _safe_emit({
                                "type": "subagent_progress",
                                "agent": self.config.name,
                                "turn": turn + 1,
                                "max_turns": _max_turns,
                                "narration": f"turn {turn+1}/{_max_turns} · thinking…",
                                "phase": "thinking",
                            })
                        response_text += event.text
                        # Periodic generation heartbeat
                        _now_h = _time.monotonic()
                        if _now_h - _last_think_pulse >= _heartbeat_s:
                            _last_think_pulse = _now_h
                            _gen_elapsed = int(_now_h - _t_start)
                            _safe_emit({
                                "type": "subagent_progress",
                                "agent": self.config.name,
                                "turn": turn + 1,
                                "max_turns": _max_turns,
                                "narration": (
                                    f"turn {turn+1}/{_max_turns} · "
                                    f"thinking… ({len(response_text):,} chars generated)"
                                ),
                                "phase": "thinking",
                                "elapsed_total_s": _gen_elapsed,
                            })
                    elif event.type == "tool_call_start" and event.tool_call:
                        tool_calls.append(event.tool_call)
                        tool_call_args_buffer[event.tool_call_index] = ""
                    elif event.type == "tool_call_delta":
                        idx = event.tool_call_index
                        if idx in tool_call_args_buffer:
                            tool_call_args_buffer[idx] += event.args_delta
                        if tool_calls and idx < len(tool_calls):
                            try:
                                tool_calls[idx].arguments = _json.loads(
                                    tool_call_args_buffer[idx]
                                )
                            except (_json.JSONDecodeError, ValueError):
                                pass

                if not tool_calls:
                    final_text = response_text
                    break

                # Ensure every tool call has parsed (dict) arguments
                for i, tc in enumerate(tool_calls):
                    if isinstance(tc.arguments, str):
                        try:
                            tc.arguments = _json.loads(tc.arguments) if tc.arguments else {}
                        except (_json.JSONDecodeError, ValueError):
                            tc.arguments = {}
                    elif tc.arguments is None:
                        tc.arguments = {}

                # Build assistant history entry in provider's native format.
                # OpenAI / GitHub Copilot / Ollama / LMStudio: tool_calls
                #   must be [{"id", "type":"function", "function":{"name",
                #   "arguments": <JSON string>}}, ...]
                # Anthropic: content blocks with tool_use entries.
                # Google: tool_calls in OpenAI shape (LLM module normalises).
                provider = getattr(llm, "provider", "") or ""
                if provider == "anthropic":
                    content_blocks = []
                    if response_text:
                        content_blocks.append({"type": "text", "text": response_text})
                    for tc in tool_calls:
                        content_blocks.append(
                            {
                                "type": "tool_use",
                                "id": tc.id,
                                "name": tc.name,
                                "input": tc.arguments,
                            }
                        )
                    messages.append({"role": "assistant", "content": content_blocks})
                else:
                    # openai / github / google / ollama / lmstudio / unknown → OpenAI shape
                    messages.append(
                        {
                            "role": "assistant",
                            "content": response_text or "",
                            "tool_calls": [
                                {
                                    "id": tc.id,
                                    "type": "function",
                                    "function": {
                                        "name": tc.name,
                                        "arguments": _json.dumps(tc.arguments),
                                    },
                                }
                                for tc in tool_calls
                            ],
                        }
                    )

                # ── v2.85 prep pass: collect metadata for every tool call
                #    so we can dispatch safe read-only ones in parallel.
                _tc_meta: list[dict] = []
                for tc in tool_calls:
                    _display_args = {}
                    try:
                        for _k, _v in (tc.arguments or {}).items():
                            _sv = str(_v)
                            _display_args[_k] = _sv[:200] + "…" if len(_sv) > 200 else _sv
                    except Exception:
                        _display_args = {}

                    # ── v2.74 read-cache + repeat-call accounting ─────────
                    _cache_hit = False
                    _ch_key = _arg_hash(tc.name, tc.arguments) if tc.arguments is not None else _arg_hash(tc.name, {})
                    _call_counts[_ch_key] = _call_counts.get(_ch_key, 0) + 1
                    _repeat_n = _call_counts[_ch_key]
                    if tc.name in _CACHEABLE and _ch_key in _tool_cache:
                        _cache_hit = True

                    # ── v2.84 HARD anti-loop refusal ──────────────────────
                    # Soft nudge at _repeat_limit was insufficient — some
                    # models ignore the warning and keep calling. After
                    # 2× the limit (default 6), short-circuit the tool
                    # entirely: don't dispatch, just return a refusal
                    # message. The forced-synthesis tail will still kick
                    # in if the agent loops on refusals.
                    _hard_loop = _repeat_n > (_repeat_limit * 2)

                    # Stash everything we need for the dispatch + emit pass.
                    _tc_meta.append({
                        "tc": tc,
                        "display_args": _display_args,
                        "ch_key": _ch_key,
                        "repeat_n": _repeat_n,
                        "cache_hit": _cache_hit,
                        "hard_loop": _hard_loop,
                    })

                # ── v2.85 PARALLEL BATCH for safe read-only tools ──────────
                # Goal: when the LLM emits >=2 independent read calls in
                # one turn (multi_read + glob + list_dir + ...), dispatch
                # them concurrently instead of strictly serial.
                #
                # Safe set: cacheable, side-effect-free, no shared mutable
                # state inside the executor. We exclude:
                #   • hard_loop refusals (no dispatch needed)
                #   • cache hits (no dispatch needed)
                #   • anything NOT in _CACHEABLE (may have side-effects)
                #
                # Cross-platform: concurrent.futures + ThreadPoolExecutor
                # is stdlib, identical behaviour on Win/WSL/Linux/macOS.
                # Tool funcs already handle their own path normalization.
                _parallel_workers = max(2, int(
                    os.environ.get("CVC_SUBAGENT_PARALLEL_TOOLS", "6")
                ))
                _batch_indices = [
                    i for i, m in enumerate(_tc_meta)
                    if (not m["hard_loop"])
                    and (not m["cache_hit"])
                    and (m["tc"].name in _CACHEABLE)
                ]
                _dispatch_results: dict = {}  # i -> (result, ok, elapsed_s)
                if len(_batch_indices) >= 2:
                    import time as _time_p
                    from concurrent.futures import ThreadPoolExecutor as _TPE, as_completed as _ac

                    def _run_one(_i: int):
                        _m = _tc_meta[_i]
                        _tc_local = _m["tc"]
                        _t_local = _time_p.monotonic()
                        try:
                            _r = executor.execute(_tc_local.name, _tc_local.arguments)
                            return _i, _r, True, _time_p.monotonic() - _t_local
                        except Exception as _e:
                            return _i, f"Error: {_e}", False, _time_p.monotonic() - _t_local

                    # Emit a batch-start telemetry so the dashboard can
                    # show "running 4 tools in parallel" instead of a
                    # mystery delay.
                    _safe_emit({
                        "type": "subagent_parallel_batch",
                        "agent": self.config.name,
                        "count": len(_batch_indices),
                        "tools": [_tc_meta[i]["tc"].name for i in _batch_indices],
                        "workers": min(_parallel_workers, len(_batch_indices)),
                    })

                    with _TPE(max_workers=min(_parallel_workers, len(_batch_indices))) as _pool:
                        _futures = [_pool.submit(_run_one, _i) for _i in _batch_indices]
                        for _fut in _ac(_futures):
                            _i, _r, _ok_b, _el = _fut.result()
                            _dispatch_results[_i] = (_r, _ok_b, _el)
                            # Cache successful read-only results immediately.
                            _m = _tc_meta[_i]
                            if _ok_b and _m["tc"].name in _CACHEABLE and len(_r) < 256_000:
                                _tool_cache[_m["ch_key"]] = _r

                # ── Serial emit / dispatch pass (preserves original order) ──
                for _i, _meta in enumerate(_tc_meta):
                    tc = _meta["tc"]
                    _display_args = _meta["display_args"]
                    _ch_key = _meta["ch_key"]
                    _repeat_n = _meta["repeat_n"]
                    _cache_hit = _meta["cache_hit"]
                    _hard_loop = _meta["hard_loop"]
                    _was_parallel = _i in _dispatch_results

                    _safe_emit({
                        "type": "subagent_tool_start",
                        "agent": self.config.name,
                        "name": tc.name,
                        "args": _display_args,
                        "cached": _cache_hit,
                        "repeat": _repeat_n,
                        "parallel": _was_parallel,
                        "phase": "loop_refused" if _hard_loop else (
                            "cached" if _cache_hit else (
                                "parallel_running" if _was_parallel else "tool_running"
                            )
                        ),
                    })
                    _tools_run_total += 1
                    import time as _time
                    _t0 = _time.monotonic()
                    if _hard_loop:
                        result = (
                            f"[runtime] REFUSED: {tc.name}({_display_args}) "
                            f"has been called {_repeat_n} times this run "
                            f"(limit: {_repeat_limit * 2}). The runtime is "
                            "no longer dispatching this call. Stop calling "
                            "it and return your final answer using the data "
                            "you already have."
                        )
                        _ok = False
                        _elapsed = 0.0
                    elif _cache_hit:
                        result = _tool_cache[_ch_key]
                        _ok = True
                        _elapsed = 0.0
                    elif _was_parallel:
                        # Result already computed by the thread pool above.
                        result, _ok, _elapsed = _dispatch_results[_i]
                    else:
                        # ── Mid-tool heartbeat: while a single tool runs long
                        #    (e.g. a 60s grep), emit progress events every
                        #    _heartbeat_s so the dashboard never goes dark.
                        import threading as _threading
                        _hb_stop = _threading.Event()

                        def _hb_loop():
                            _hb_t0 = _time.monotonic()
                            while not _hb_stop.wait(_heartbeat_s):
                                _elapsed_tool = _time.monotonic() - _hb_t0
                                _safe_emit({
                                    "type": "subagent_progress",
                                    "agent": self.config.name,
                                    "turn": turn + 1,
                                    "max_turns": _max_turns,
                                    "narration": (
                                        f"turn {turn+1}/{_max_turns} · "
                                        f"{tc.name} running ({int(_elapsed_tool)}s)…"
                                    ),
                                    "phase": "tool_running",
                                    "tool": tc.name,
                                    "elapsed_s": round(_elapsed_tool, 1),
                                })

                        _hb_thread = _threading.Thread(target=_hb_loop, daemon=True)
                        _hb_thread.start()
                        try:
                            result = executor.execute(tc.name, tc.arguments)
                            _ok = True
                        except Exception as e:
                            result = f"Error: {e}"
                            _ok = False
                        finally:
                            _hb_stop.set()
                        if _ok and tc.name in _CACHEABLE and len(result) < 256_000:
                            _tool_cache[_ch_key] = result
                        _elapsed = _time.monotonic() - _t0

                    # ── Repeat-call refusal: if this exact (name,args) has
                    #    been invoked more than _repeat_limit times, append
                    #    a runtime nudge AFTER returning the result so the
                    #    LLM gets the data once and the warning once.
                    if _repeat_n > _repeat_limit:
                        result = (
                            f"{result}\n\n[runtime] You have called "
                            f"{tc.name}({_display_args}) {_repeat_n} times this run. "
                            "Stop re-fetching this and proceed with what you have."
                        )
                    # Truncate display payload — full text still goes to the LLM.
                    _display_output = (
                        result[:1500] + f"\n... ({len(result):,} chars total)"
                        if len(result) > 1500 else result
                    )
                    _safe_emit({
                        "type": "subagent_tool_result",
                        "agent": self.config.name,
                        "name": tc.name,
                        "output": _display_output,
                        "elapsed_s": round(_elapsed, 2),
                        "ok": _ok,
                    })

                    if provider == "anthropic":
                        messages.append(
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tc.id,
                                        "content": result,
                                    }
                                ],
                            }
                        )
                    else:
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.id,
                                "content": result,
                            }
                        )

                # ── v2.69 turn-end: narrate + dynamic expansion / halt ─────
                _total_calls = len(tool_calls)
                _cached_calls = sum(
                    1 for tc in tool_calls
                    if tc.name in _CACHEABLE
                    and _arg_hash(tc.name, tc.arguments) in _tool_cache
                    # heuristic: if it's already in cache after this turn,
                    # and showed up >1 in cache lookups, it was a re-read.
                )
                # More precise: track novel this turn via local set.
                _seen_this_turn: set[str] = set()
                _novel = 0
                _cached_now = 0
                for tc in tool_calls:
                    if tc.name in _CACHEABLE:
                        h = _arg_hash(tc.name, tc.arguments)
                        if h in _seen_this_turn:
                            _cached_now += 1
                        else:
                            _seen_this_turn.add(h)
                            _novel += 1
                    else:
                        _novel += 1
                _novel_window.append((_novel, _total_calls))
                if len(_novel_window) > 3:
                    _novel_window.pop(0)

                _safe_emit({
                    "type": "subagent_progress",
                    "agent": self.config.name,
                    "turn": turn + 1,
                    "max_turns": _max_turns,
                    "novel": _novel,
                    "cached": _cached_now,
                    "total_calls": _total_calls,
                    "narration": _narrate(turn, tool_calls, _novel, _cached_now),
                })

                # Dynamic expansion: when we're within 3 turns of the cap
                # AND the last window shows healthy productivity (≥40% novel),
                # extend by another 25% of the base (up to hard ceiling).
                if turn + 1 >= _max_turns - 3 and _max_turns < _hard_ceiling:
                    if _novel_window:
                        _win_novel = sum(n for n, _ in _novel_window)
                        _win_total = max(1, sum(t for _, t in _novel_window))
                        if _win_novel / _win_total >= 0.4:
                            _grow = max(5, _base_max_turns // 4)
                            _max_turns = min(_hard_ceiling, _max_turns + _grow)

                # Early-halt: if last 3 turns produced ≥10 calls but the
                # novel ratio is below _stall_ratio (default 20%), the agent
                # is spinning. Force a final-answer turn and tell the user.
                if len(_novel_window) == 3:
                    _win_novel = sum(n for n, _ in _novel_window)
                    _win_total = sum(t for _, t in _novel_window)
                    if _win_total >= 10 and (_win_novel / _win_total) < _stall_ratio:
                        messages.append({
                            "role": "user",
                            "content": (
                                "[runtime] Productivity has collapsed (mostly "
                                "re-reads / cache hits). Stop calling tools and "
                                "return your best answer now."
                            ),
                        })
                        _max_turns = min(_max_turns, turn + 2)
                        _safe_emit({
                            "type": "subagent_progress",
                            "agent": self.config.name,
                            "turn": turn + 1,
                            "max_turns": _max_turns,
                            "narration": "stall detected — forcing final answer",
                            "phase": "stall",
                        })

            # ── v2.80 forced final-synthesis ──────────────────────────────
            # If the loop exited via max_turns / wall-budget / stall WITHOUT
            # the model emitting a final text answer, do ONE final no-tools
            # call asking the model to summarize everything it has gathered.
            # This is the fix for the canonical Windows symptom:
            # "Analyze the entire project" → 80+ tool calls → silent end.
            if not final_text:
                _safe_emit({
                    "type": "subagent_progress",
                    "agent": self.config.name,
                    "turn": turn + 1,
                    "max_turns": _max_turns,
                    "narration": "finalizing — synthesizing answer from gathered context…",
                    "phase": "finalizing",
                })
                messages.append({
                    "role": "user",
                    "content": (
                        "[runtime] Iteration budget exhausted. You have already "
                        "gathered substantial context from prior tool calls. "
                        "Do NOT call any more tools. Synthesize and return your "
                        "complete final answer NOW using only what you already "
                        "know. Be thorough — this is your last chance to reply."
                    ),
                })
                try:
                    _synth_text = ""
                    async for event in llm.chat_stream(
                        messages=messages,
                        tools=None,  # no tools — force a text reply
                    ):
                        if event.type == "text_delta":
                            _synth_text += event.text
                    if _synth_text.strip():
                        final_text = _synth_text
                except Exception as _synth_err:
                    _safe_emit({
                        "type": "subagent_progress",
                        "agent": self.config.name,
                        "turn": turn + 1,
                        "max_turns": _max_turns,
                        "narration": f"final-synthesis error: {type(_synth_err).__name__}",
                        "phase": "finalizing_error",
                    })

            _final = final_text or (
                "(Sub-agent completed without producing a response. "
                "Iteration budget was exhausted before the model emitted a "
                "final answer. Consider increasing CVC_SUBAGENT_HARD_CEILING "
                "or narrowing the prompt.)"
            )
            _safe_emit({
                "type": "subagent_done",
                "agent": self.config.name,
                "ok": bool(final_text),
                "turns": turn + 1,
                "max_turns": _max_turns,
            })
            return _final

        finally:
            await llm.close()
