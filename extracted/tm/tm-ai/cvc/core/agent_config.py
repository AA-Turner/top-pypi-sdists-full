"""
cvc.core.agent_config — Unified tunable configuration for the CVC agent loop.

Single source of truth for every "magic number" that previously lived as a
module-level constant inside cvc/gateway.py and cvc/agent/*. Every value here
is surfaced through `cvc setup` (interactive editor) and the
`cvc agent-config` CLI subcommand.

Persistence: ~/.cvc/agent.toml   (override path via CVC_AGENT_CONFIG env var)

Precedence (lowest → highest):
  1. Defaults declared in this dataclass
  2. ~/.cvc/agent.toml file
  3. Environment variables (CVC_<UPPER_SNAKE>)
  4. Programmatic overrides at runtime

The gateway and the CLI read **the exact same** AgentConfig object so behavior
stays consistent between `cvc` (CLI) and `cvc gateway` (dashboard).
"""
from __future__ import annotations

import logging
import os
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any

try:
    import tomllib  # py311+
except ModuleNotFoundError:  # py310 fallback
    import tomli as tomllib  # type: ignore

try:
    import tomli_w
except ModuleNotFoundError:  # pragma: no cover
    tomli_w = None  # type: ignore

logger = logging.getLogger("cvc.agent_config")


# ─── Section helpers ────────────────────────────────────────────────────────


@dataclass
class _Tunable:
    """Metadata for a single tunable field (used by setup wizard)."""

    section: str
    label: str
    help: str
    cast: type = int
    minimum: float | None = None
    maximum: float | None = None


# Single registry — field-name → metadata. Keep keys identical to dataclass
# attribute names so we can drive the wizard generatively.
TUNABLES: dict[str, _Tunable] = {
    # ── Iteration budgets ──
    "max_agent_iterations": _Tunable(
        "Iteration Budgets",
        "Max agent iterations (standard)",
        "Maximum tool-calling loop iterations per turn for standard models. "
        "CVC v2.72 default = 120 (was 25). Upstream baseline = 90. "
        "Heavy refactor / UI build tasks routinely use 80–150.",
        int, 10, 1000,
    ),
    "max_agent_iterations_expensive": _Tunable(
        "Iteration Budgets",
        "Max agent iterations (Opus/expensive)",
        "Iteration cap for expensive models (Opus, GPT-4-Turbo). Keep lower to bound spend.",
        int, 5, 500,
    ),
    "autopilot_max_iterations": _Tunable(
        "Iteration Budgets",
        "Autopilot iterations",
        "Iterations available when autopilot/continuation mode is ON.",
        int, 10, 1000,
    ),
    "autopilot_hard_cap": _Tunable(
        "Iteration Budgets",
        "Autopilot hard cap",
        "Absolute safety ceiling that even autopilot cannot exceed.",
        int, 20, 2000,
    ),
    # ── Unstoppable Loop (v2.72.0) ──
    "max_empty_retries": _Tunable(
        "Iteration Budgets",
        "Max empty-response retries",
        "How many times to silently retry when the model returns a zero-token "
        "response (Gemini thinking-budget exhaustion, transient provider hiccup). "
        "Upstream default = 3.",
        int, 0, 10,
    ),
    "stream_retries": _Tunable(
        "Iteration Budgets",
        "Streaming-call retry attempts",
        "Provider-level retries on transient streaming failures (HTTP 5xx, "
        "connection resets). Applies to Gemini & OpenAI-compatible streams.",
        int, 1, 10,
    ),
    "grace_call_enabled": _Tunable(
        "Iteration Budgets",
        "Grace synth on cap (0/1)",
        "When the iteration ceiling is reached, perform ONE additional no-tools "
        "synthesis call so the model emits a final status summary instead of "
        "freezing silent. Strongly recommended ON.",
        int, 0, 1,
    ),
    "log_exit_reason": _Tunable(
        "Iteration Budgets",
        "Log loop exit reason (0/1)",
        "Emit a structured log line tagging every agentic-loop exit "
        "(budget_exhausted, empty_response_exhausted, final_text, cost_paused, …) "
        "for postmortem and dashboard telemetry.",
        int, 0, 1,
    ),
    # ── Timeouts ──
    "agent_timeout": _Tunable(
        "Timeouts (seconds)",
        "Total turn budget",
        "Maximum wall-clock seconds for a single user turn before the agent yields.",
        float, 30, 7200,
    ),
    "tool_exec_timeout": _Tunable(
        "Timeouts (seconds)",
        "Per-tool timeout",
        "Maximum seconds for a single tool call to return before being killed.",
        float, 5, 1800,
    ),
    "confirm_timeout": _Tunable(
        "Timeouts (seconds)",
        "Tool-confirm prompt timeout",
        "How long the agent waits for a human approve/deny decision.",
        float, 5, 600,
    ),
    "sse_heartbeat_interval": _Tunable(
        "Timeouts (seconds)",
        "SSE heartbeat interval",
        "Keepalive ping cadence on Server-Sent Events streams.",
        float, 2, 120,
    ),
    "autopilot_cost_pause": _Tunable(
        "Timeouts (seconds)",
        "Autopilot cost-pause threshold ($)",
        "Autopilot pauses for human review once estimated spend crosses this dollar amount.",
        float, 0.1, 1000,
    ),
    # ── Turn-resume ring buffer ──
    "turn_ring_size": _Tunable(
        "Resumable Turns",
        "Ring buffer size",
        "Max events buffered per turn for resume-after-disconnect.",
        int, 100, 20000,
    ),
    "turn_gc_interval": _Tunable(
        "Resumable Turns",
        "GC sweep interval (s)",
        "Cadence of stale-turn garbage collection.",
        float, 5, 600,
    ),
    "turn_done_ttl": _Tunable(
        "Resumable Turns",
        "Done-turn retention (s)",
        "How long finished turns stay resumable after completion.",
        float, 30, 3600,
    ),
    "turn_orphan_ttl": _Tunable(
        "Resumable Turns",
        "Orphan turn TTL (s)",
        "Kill un-finished turns with no activity for this long.",
        float, 60, 7200,
    ),
    # ── Tool output caps ──
    "max_tool_output_llm": _Tunable(
        "Tool Output Caps (chars)",
        "Standard model tool output cap",
        "Maximum characters of tool output fed back to standard models.",
        int, 1000, 200000,
    ),
    "max_tool_output_expensive": _Tunable(
        "Tool Output Caps (chars)",
        "Expensive model tool output cap",
        "Tighter cap for expensive models to keep cost predictable.",
        int, 500, 100000,
    ),
    # ── Uploads / vision ──
    "max_upload_bytes": _Tunable(
        "Uploads & Vision (bytes)",
        "Max upload size",
        "Hard cap on a single uploaded artifact. Default = 50 MB.",
        int, 1024 * 1024, 1024 * 1024 * 1024,
    ),
    "inline_image_cap": _Tunable(
        "Uploads & Vision (bytes)",
        "Inline image cap",
        "Images smaller than this are inlined as data URLs to vision models.",
        int, 256 * 1024, 1024 * 1024 * 128,
    ),
    # ── Context window ──
    "auto_compact_threshold": _Tunable(
        "Context Window",
        "Auto-compact threshold (% full)",
        "When context usage crosses this %, CVC auto-compresses the conversation.",
        int, 50, 99,
    ),
    "auto_compact_pct": _Tunable(
        "Context Window",
        "Auto-compact target ratio (0-1)",
        "Target compression ratio after auto-compact fires.",
        float, 0.1, 0.95,
    ),
    # ── Tenacity (Agent 2.0) ──
    "tenacity_mode": _Tunable(
        "Tenacity (Agent 2.0)",
        "Tenacity mode",
        "0 = off, 1 = standard (continuation engine), 2 = aggressive (Ralph loop).",
        int, 0, 2,
    ),
    "goal_persistence": _Tunable(
        "Tenacity (Agent 2.0)",
        "Persistent /goal across turns",
        "1 = pinned goals survive across user turns until /clear-goal.",
        int, 0, 1,
    ),
    "max_consecutive_same_tool": _Tunable(
        "Tenacity (Agent 2.0)",
        "Max consecutive identical tool calls",
        "Anti-loop guard. 0 disables. Upstream parity default = 10.",
        int, 0, 100,
    ),
    "auto_resume_on_restart": _Tunable(
        "Tenacity (Agent 2.0)",
        "Auto-resume sessions on restart",
        "1 = pick up interrupted turns when the gateway/CLI restarts.",
        int, 0, 1,
    ),
    # ── Sampling ──
    "default_temperature": _Tunable(
        "Sampling",
        "Default temperature",
        "LLM sampling temperature for first reasoning call.",
        float, 0.0, 2.0,
    ),
    "tool_loop_temperature": _Tunable(
        "Sampling",
        "Tool-loop temperature",
        "Temperature used during tool-calling iterations (lower = more deterministic).",
        float, 0.0, 2.0,
    ),
}


@dataclass
class CvcAgentConfig:
    """Every tunable CVC agent capability — single source of truth."""

    # Iteration budgets
    max_agent_iterations: int = 120                   # was 80 — v2.72 unstoppable loop
    max_agent_iterations_expensive: int = 40
    autopilot_max_iterations: int = 150               # was 100
    autopilot_hard_cap: int = 300                     # was 200
    max_empty_retries: int = 3                        # NEW — upstream parity
    stream_retries: int = 3                           # NEW — streaming resilience
    grace_call_enabled: int = 1                       # NEW — synth on cap
    log_exit_reason: int = 1                          # NEW — telemetry

    # Timeouts (seconds)
    agent_timeout: float = 900.0
    tool_exec_timeout: float = 300.0
    confirm_timeout: float = 120.0
    sse_heartbeat_interval: float = 15.0
    autopilot_cost_pause: float = 5.0

    # Turn-resume ring buffer
    turn_ring_size: int = 2000
    turn_gc_interval: float = 60.0
    turn_done_ttl: float = 300.0
    turn_orphan_ttl: float = 1800.0

    # Tool output caps (chars)
    max_tool_output_llm: int = 15000
    max_tool_output_expensive: int = 5000

    # Uploads / vision (bytes)
    max_upload_bytes: int = 50 * 1024 * 1024
    inline_image_cap: int = 6 * 1024 * 1024

    # Context window
    auto_compact_threshold: int = 95
    auto_compact_pct: float = 0.5

    # Tenacity / Agent 2.0
    tenacity_mode: int = 1
    goal_persistence: int = 1
    max_consecutive_same_tool: int = 10
    auto_resume_on_restart: int = 1

    # Sampling
    default_temperature: float = 0.7
    tool_loop_temperature: float = 0.5

    # Free-form section (forwards-compatible)
    extras: dict[str, Any] = field(default_factory=dict)

    # ── (de)serialisation ──────────────────────────────────────────────

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("extras", None)
        if self.extras:
            d["extras"] = dict(self.extras)
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CvcAgentConfig":
        valid = {f.name for f in fields(cls)}
        kwargs: dict[str, Any] = {}
        extras: dict[str, Any] = {}
        for k, v in (data or {}).items():
            if k == "extras" and isinstance(v, dict):
                extras.update(v)
            elif k in valid:
                kwargs[k] = v
            else:
                extras[k] = v
        cfg = cls(**kwargs)
        cfg.extras = extras
        return cfg

    # ── file I/O ───────────────────────────────────────────────────────

    @staticmethod
    def path() -> Path:
        env = os.environ.get("CVC_AGENT_CONFIG")
        if env:
            return Path(env).expanduser()
        return Path.home() / ".cvc" / "agent.toml"

    @classmethod
    def load(cls) -> "CvcAgentConfig":
        p = cls.path()
        if not p.exists():
            return cls()._apply_env_overrides()
        try:
            with p.open("rb") as fh:
                data = tomllib.load(fh)
        except Exception as exc:
            logger.warning("Failed to parse %s (%s) — using defaults", p, exc)
            return cls()._apply_env_overrides()
        return cls.from_dict(data)._apply_env_overrides()

    def save(self) -> Path:
        p = self.path()
        p.parent.mkdir(parents=True, exist_ok=True)
        if tomli_w is None:
            # Last-resort plaintext writer; round-trips for primitives only.
            lines = ["# CVC agent tunables", ""]
            for k, v in self.to_dict().items():
                if isinstance(v, str):
                    lines.append(f'{k} = "{v}"')
                elif isinstance(v, bool):
                    lines.append(f"{k} = {str(v).lower()}")
                elif isinstance(v, (int, float)):
                    lines.append(f"{k} = {v}")
                elif isinstance(v, dict):
                    pass  # extras skipped without tomli_w
            p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        else:
            p.write_bytes(tomli_w.dumps(self.to_dict()).encode("utf-8"))
        logger.info("Saved CvcAgentConfig → %s", p)
        return p

    # ── env-var precedence ─────────────────────────────────────────────

    def _apply_env_overrides(self) -> "CvcAgentConfig":
        for f in fields(self):
            if f.name == "extras":
                continue
            env_key = "CVC_" + f.name.upper()
            raw = os.environ.get(env_key)
            if raw is None:
                # legacy aliases
                if f.name == "max_agent_iterations":
                    raw = os.environ.get("CVC_MAX_ITERATIONS")
                elif f.name == "agent_timeout":
                    raw = os.environ.get("CVC_AGENT_TIMEOUT")
                elif f.name == "tool_exec_timeout":
                    raw = os.environ.get("CVC_TOOL_EXEC_TIMEOUT")
                elif f.name == "autopilot_max_iterations":
                    raw = os.environ.get("CVC_AUTOPILOT_MAX_ITERS")
                elif f.name == "autopilot_cost_pause":
                    raw = os.environ.get("CVC_AUTOPILOT_COST_PAUSE")
            if raw is None:
                continue
            try:
                if f.type in ("int", int):
                    setattr(self, f.name, int(raw))
                elif f.type in ("float", float):
                    setattr(self, f.name, float(raw))
                else:
                    setattr(self, f.name, raw)
            except ValueError:
                logger.warning("Ignoring invalid %s=%r", env_key, raw)
        return self

    # ── validation ─────────────────────────────────────────────────────

    def set_field(self, name: str, value: Any) -> None:
        """Validate-and-set a single field by name. Raises ValueError on bad input."""
        if name not in {f.name for f in fields(self)}:
            raise ValueError(f"Unknown agent-config field: {name}")
        meta = TUNABLES.get(name)
        if meta is None:
            setattr(self, name, value)
            return
        try:
            cast_v = meta.cast(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name}: cannot cast {value!r} to {meta.cast.__name__}") from exc
        if meta.minimum is not None and cast_v < meta.minimum:
            raise ValueError(f"{name}: {cast_v} below minimum {meta.minimum}")
        if meta.maximum is not None and cast_v > meta.maximum:
            raise ValueError(f"{name}: {cast_v} above maximum {meta.maximum}")
        setattr(self, name, cast_v)

    def reset(self) -> "CvcAgentConfig":
        """Replace this instance's fields with their declared defaults."""
        defaults = CvcAgentConfig()
        for f in fields(self):
            setattr(self, f.name, getattr(defaults, f.name))
        return self


# ─── Module-level singleton (lazy) ──────────────────────────────────────────

_INSTANCE: CvcAgentConfig | None = None


def get_agent_config() -> CvcAgentConfig:
    """Return the process-wide AgentConfig, loading from disk on first call."""
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = CvcAgentConfig.load()
    return _INSTANCE


def reload_agent_config() -> CvcAgentConfig:
    """Force a re-read from disk. Call after `cvc setup` writes changes."""
    global _INSTANCE
    _INSTANCE = CvcAgentConfig.load()
    return _INSTANCE


def sections() -> list[tuple[str, list[str]]]:
    """Return ordered (section_label, [field_name, …]) for the wizard."""
    order: dict[str, list[str]] = {}
    for fname, meta in TUNABLES.items():
        order.setdefault(meta.section, []).append(fname)
    return list(order.items())
