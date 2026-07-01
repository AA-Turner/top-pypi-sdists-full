"""
cvc.agent.hermes_bridge — wire CVC's native tool surface into the agent core.

CVC ships its own tool runtime under ``cvc.core`` and ``cvc.skills``. This
bridge adapts that surface to what the agent executor and chat loop expect.

This bridge:
    1. Imports the native ``cvc.core.tools`` registry (no sys.path tricks, no
       vendored dependencies — fully self-contained).
    2. Calls ``discover_builtin_tools()`` to populate the singleton registry.
       In v4.0 the registry is empty by default — skills (Phase 2) and
       platform adapters (Phase 3) register their own tools at boot.
    3. Exposes:
         - CVC_TOOL_SCHEMAS: OpenAI-format function schemas filtered by
           check_fn (only tools whose credentials/binaries/platform are OK).
         - dispatch_cvc_tool(name, args) -> str: thin handler that
           delegates to the registry's dispatch path.

The bridge is import-safe: any failure (broken individual tool, missing
optional dep) is logged and contained — base CVC tools keep working.

v4.0.0: Zero runtime dependency on Hermes Agent or any vendored tree.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level state populated at import time
# ---------------------------------------------------------------------------

HERMES_AVAILABLE: bool = False
HERMES_TOOL_SCHEMAS: list[dict[str, Any]] = []
HERMES_TOOL_NAMES: set[str] = set()
_HERMES_REGISTRY: Any = None
_INIT_ERROR: str | None = None

# Phase E (4.2): holographic memory provider — fact_store + fact_feedback
# Lazy-initialized; survives missing numpy/sqlite gracefully.
_HOLO_PROVIDER: Any = None
_HOLO_TOOL_NAMES: set[str] = {"fact_store", "fact_feedback"}
_HOLO_INIT_ERROR: str | None = None

# Marker for downstream debug/status — string is part of CVC's public surface
HERMES_SOURCE = "vendored"


def _bootstrap() -> None:
    """Import the vendored registry and populate tool schemas — never raises."""
    global HERMES_AVAILABLE, HERMES_TOOL_SCHEMAS, HERMES_TOOL_NAMES
    global _HERMES_REGISTRY, _INIT_ERROR

    if HERMES_AVAILABLE or _INIT_ERROR:
        return

    # Keep vendor init quiet — we only want the tool registry, not its CLI.
    os.environ.setdefault("HERMES_DISABLE_TELEMETRY", "1")

    # Phase A wiring: redirect vendored Hermes file ops (skills, usage,
    # provenance, hub) to CVC's home so skill_manage writes land under
    # ~/.cvc/skills/ instead of ~/.hermes/skills/. The vendored modules call
    # ``get_hermes_home()`` which honours $HERMES_HOME first.
    os.environ.setdefault(
        "HERMES_HOME", os.path.expanduser("~/.cvc")
    )

    # Phase C wiring: auto-discover existing ~/.hermes/skills/ as an external
    # read-only skills source so the vendored manifest builder
    # (build_skills_system_prompt) surfaces the user's existing skill library
    # without forcing a re-install or symlink. Idempotent: only writes when
    # the dir exists AND isn't already listed in skills.external_dirs.
    try:
        _seed_external_skills_dir()
    except Exception:  # pragma: no cover — never block bootstrap
        pass

    try:
        from cvc.core import tools as _reg_mod
        from cvc.core.tools import discover_builtin_tools

        discover_builtin_tools()
        _HERMES_REGISTRY = _reg_mod.registry  # singleton

        # Pull all tool names and request OpenAI-format schemas. The
        # registry's get_definitions filters out tools whose check_fn
        # returns False (missing creds / wrong platform / missing binary).
        all_names = set(_HERMES_REGISTRY.get_all_tool_names())
        defs = _HERMES_REGISTRY.get_definitions(all_names, quiet=True)

        # Tool names already owned by CVC's native dispatch in
        # cvc.agent.executor.Executor.execute. CVC's behavior wins on
        # those names — we don't shadow them with Hermes versions
        # (different schemas, different side-effects on .cvc/ state).
        # All NEW capability tools (browser, computer_use, vision, video,
        # image_gen, cronjob, delegate_task, mixture_of_agents,
        # session_search, skill_*, text_to_speech, send_message, etc.)
        # still flow through.
        CVC_NATIVE = {
            "read_file", "write_file", "edit_file", "patch_file",
            "bash", "process_manage", "glob", "grep", "list_dir",
            "web_search", "web_fetch", "fetch_docs", "search_docs",
            "lookup_api", "annotate_doc",
            "multi_edit", "multi_read", "think", "context_compact",
            "todo", "semantic_grep", "git", "save_memory",
            "agent", "task_create", "task_get", "task_list", "task_kill",
            "ask_user", "parallel_agents",
            # Native CVC patch/process/search_files use cvc paths,
            # don't let hermes shadow them
            "patch", "process", "search_files",
            # NOTE: `memory` (vendored Hermes MemoryStore tool — manages
            # ~/.cvc/memories/MEMORY.md + USER.md) is INTENTIONALLY NOT
            # blocked here. Phase D item 4.1 exposes it to the agent so
            # it can read/write/edit persistent memory entries that get
            # auto-injected by build_system_prompt (items 4.6/4.7).
            # `save_memory` above is CVC's separate topic-based memory.
        }

        filtered = [d for d in defs if d["function"]["name"] not in CVC_NATIVE]

        HERMES_TOOL_SCHEMAS = filtered
        HERMES_TOOL_NAMES = {d["function"]["name"] for d in filtered}
        HERMES_AVAILABLE = True
        logger.info(
            "cvc: loaded %d tools (of %d registered) from vendored package",
            len(HERMES_TOOL_SCHEMAS), len(all_names),
        )

        # Phase E item 4.2: bring up the holographic MemoryProvider so the
        # agent gets fact_store + fact_feedback tools and the
        # "# Holographic Memory" prompt block. Failures (missing numpy, bad
        # sqlite, etc.) are non-fatal — log and continue.
        try:
            _bootstrap_holographic()
        except Exception as exc:  # pragma: no cover — defensive
            globals()["_HOLO_INIT_ERROR"] = f"{type(exc).__name__}: {exc}"
            logger.warning("cvc: holographic init failed (%s)", _HOLO_INIT_ERROR)
    except Exception as exc:
        _INIT_ERROR = f"{type(exc).__name__}: {exc}"
        logger.warning("cvc: failed to load vendored tools (%s)", _INIT_ERROR)


# ---------------------------------------------------------------------------
# Public dispatch surface
# ---------------------------------------------------------------------------

def dispatch_hermes_tool(name: str, args: dict[str, Any]) -> str:
    """
    Execute a Hermes-bridged tool by name. Returns a string suitable for
    inclusion in the agent's conversation (JSON-encoded errors on failure).
    """
    # Phase E (4.2): holographic provider dispatch — routes fact_store /
    # fact_feedback to the MemoryProvider instance instead of the registry.
    if name in _HOLO_TOOL_NAMES:
        return _dispatch_holographic(name, args)

    if not HERMES_AVAILABLE or _HERMES_REGISTRY is None:
        return json.dumps({
            "error": "hermes_bridge unavailable",
            "detail": _INIT_ERROR or "not initialized",
        })
    if name not in HERMES_TOOL_NAMES:
        return json.dumps({"error": f"Unknown hermes tool: {name}"})
    try:
        result = _HERMES_REGISTRY.dispatch(name, args or {})
        if isinstance(result, (dict, list)):
            return json.dumps(result, default=str)
        return str(result)
    except Exception as exc:
        logger.exception("hermes_bridge dispatch error: %s", name)
        return json.dumps({
            "error": f"hermes tool {name} failed",
            "detail": f"{type(exc).__name__}: {exc}",
        })


def get_hermes_toolset(name: str) -> str | None:
    """Return the toolset a hermes tool belongs to, or None."""
    if name in _HOLO_TOOL_NAMES:
        return "memory"  # virtual toolset; tools always-on
    if not HERMES_AVAILABLE or _HERMES_REGISTRY is None:
        return None
    return _HERMES_REGISTRY.get_toolset_for_tool(name)


# ---------------------------------------------------------------------------
# Phase E (4.2): Holographic memory provider
# ---------------------------------------------------------------------------

def _bootstrap_holographic() -> None:
    """Lazy-init the holographic MemoryProvider + append its tool schemas.

    Idempotent. Adds ``fact_store`` and ``fact_feedback`` to
    ``HERMES_TOOL_SCHEMAS`` / ``HERMES_TOOL_NAMES`` only after the provider
    successfully initialises (numpy + sqlite OK).
    """
    global _HOLO_PROVIDER, _HOLO_INIT_ERROR
    if _HOLO_PROVIDER is not None:
        return
    try:
        from cvc.core.memory_holographic import (
            HolographicMemoryProvider,
            FACT_STORE_SCHEMA,
            FACT_FEEDBACK_SCHEMA,
        )
        provider = HolographicMemoryProvider()
        # Load profile-scoped config (plugins.holographic-memory) from
        # ~/.cvc/config.yaml; helper inside the plugin handles missing keys.
        try:
            from cvc.core.memory_holographic import (
                _load_plugin_config,
            )
            cfg = _load_plugin_config() or {}
            if hasattr(provider, "_config"):
                provider._config.update(cfg)
        except Exception:  # pragma: no cover — config optional
            pass
        provider.initialize(session_id="cvc-bridge")
        _HOLO_PROVIDER = provider

        # Register schemas in OpenAI function-calling format so the agent
        # surfaces them like any other Hermes tool.
        for raw in (FACT_STORE_SCHEMA, FACT_FEEDBACK_SCHEMA):
            wrapped = {
                "type": "function",
                "function": {
                    "name": raw["name"],
                    "description": raw["description"],
                    "parameters": raw["parameters"],
                },
            }
            HERMES_TOOL_SCHEMAS.append(wrapped)
            HERMES_TOOL_NAMES.add(raw["name"])
        logger.info("cvc: holographic memory provider ready (+2 tools)")
    except Exception as exc:
        _HOLO_INIT_ERROR = f"{type(exc).__name__}: {exc}"
        logger.warning("cvc: holographic provider unavailable (%s)", _HOLO_INIT_ERROR)


def _dispatch_holographic(name: str, args: dict[str, Any]) -> str:
    """Route fact_store / fact_feedback to the provider; JSON error if down."""
    if _HOLO_PROVIDER is None:
        return json.dumps({
            "error": "holographic memory provider unavailable",
            "detail": _HOLO_INIT_ERROR or "not initialized",
        })
    try:
        result = _HOLO_PROVIDER.handle_tool_call(name, args or {})
        return result if isinstance(result, str) else json.dumps(result, default=str)
    except Exception as exc:
        logger.exception("hermes_bridge holographic dispatch error: %s", name)
        return json.dumps({
            "error": f"holographic tool {name} failed",
            "detail": f"{type(exc).__name__}: {exc}",
        })


def holographic_system_prompt_block() -> str:
    """System-prompt fragment from the holographic provider, or empty."""
    if _HOLO_PROVIDER is None:
        return ""
    try:
        return _HOLO_PROVIDER.system_prompt_block() or ""
    except Exception:
        return ""


def soul_cold_start_block(persona: str | None = None) -> str:
    """H3 — soul cold-start context for system-prompt injection.

    Per Foundation H3 ('Brain-portable identity'), every agent —
    regardless of underlying LLM — gets the same soul-level identity.
    This block fetches the compact cold-start bundle from the gateway
    and returns it ready to paste into a system prompt.

    Used by the agent loop on cold start AND on provider swap, so
    switching from GPT to Claude mid-project doesn't make the soul
    suddenly forget everything it knew.

    Args:
      persona: optional persona id for H5 framing (default: None)

    Returns:
      The system_prompt_fragment string, or "" if the gateway is
      unavailable / errors out. Never raises — prompt injection must
      be safe-by-default.
    """
    try:
        import urllib.request
        import urllib.parse
        import json as _json
        import os as _os

        # Find the gateway port (default 13421 — matches cvc gateway)
        port = _os.environ.get("CVC_GATEWAY_PORT", "13421")
        host = _os.environ.get("CVC_GATEWAY_HOST", "127.0.0.1")
        params = {}
        if persona:
            params["persona"] = persona
        qs = urllib.parse.urlencode(params)
        url = f"http://{host}:{port}/api/soul/cold-start-context?{qs}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = _json.loads(resp.read().decode("utf-8"))
        return data.get("system_prompt_fragment", "") or ""
    except Exception:
        # Cold-start is best-effort. If the gateway is down or the
        # user has no model yet, fall back to nothing — the soul
        # builds itself; it doesn't require the gateway to operate.
        return ""


def soul_recall_block(query: str, limit: int = 5) -> str:
    """H3 — recall relevant memories for the current query.

    Used by the agent loop on every turn to inject past context
    that's relevant to what the user just said. Falls back to empty
    string on any error.
    """
    try:
        import urllib.request
        import urllib.parse
        import json as _json
        import os as _os

        if not query or not query.strip():
            return ""
        port = _os.environ.get("CVC_GATEWAY_PORT", "13421")
        host = _os.environ.get("CVC_GATEWAY_HOST", "127.0.0.1")
        qs = urllib.parse.urlencode({"query": query, "limit": str(limit)})
        url = f"http://{host}:{port}/api/soul/recall?{qs}"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = _json.loads(resp.read().decode("utf-8"))
        results = data.get("results", [])
        if not results:
            return ""
        lines = ["## What you remember about this"]
        for r in results[:limit]:
            kind = r.get("kind", "memory")
            text = r.get("text", "").strip()
            if not text:
                continue
            lines.append(f"- ({kind}) {text[:200]}")
        return "\n".join(lines)
    except Exception:
        return ""


def holographic_prefetch(query: str) -> str:
    """Retrieve top-trust facts relevant to the next turn's query."""
    if _HOLO_PROVIDER is None or not query:
        return ""
    try:
        return _HOLO_PROVIDER.prefetch(query) or ""
    except Exception:
        return ""


def _seed_external_skills_dir() -> None:
    """Idempotently add ``~/.hermes/skills/`` to ``skills.external_dirs`` in
    ``~/.cvc/config.yaml`` when present.

    Phase C wiring: lets the vendored ``build_skills_system_prompt`` see the
    user's existing skill library (typically ~116 skills under ~/.hermes/skills)
    without forcing them to copy or symlink. Local ``~/.cvc/skills/`` still wins
    on name collisions; external dirs are scanned read-only.

    Silent no-op when:
      * ~/.hermes/skills/ does not exist (fresh install with no Hermes history)
      * The dir is already listed in ``skills.external_dirs``
      * Config write fails for any reason (we never block bootstrap)
    """
    from pathlib import Path

    hermes_skills = Path(os.path.expanduser("~/.hermes/skills"))
    if not hermes_skills.is_dir():
        return

    cvc_home = Path(os.environ.get("HERMES_HOME", os.path.expanduser("~/.cvc")))
    config_path = cvc_home / "config.yaml"

    # Load existing config (or start fresh)
    try:
        import yaml  # PyYAML — ships with CVC
    except ImportError:
        return

    config: dict[str, Any] = {}
    if config_path.exists():
        try:
            loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                config = loaded
        except Exception:
            return

    skills_cfg = config.get("skills")
    if not isinstance(skills_cfg, dict):
        skills_cfg = {}

    existing = skills_cfg.get("external_dirs") or []
    if isinstance(existing, str):
        existing = [existing]
    if not isinstance(existing, list):
        existing = []

    target = str(hermes_skills)
    # Compare resolved paths to be idempotent across ~/ vs absolute forms
    resolved_target = hermes_skills.resolve()
    for entry in existing:
        try:
            if Path(os.path.expanduser(str(entry))).resolve() == resolved_target:
                return  # already configured
        except Exception:
            continue

    existing.append(target)
    skills_cfg["external_dirs"] = existing
    config["skills"] = skills_cfg

    try:
        cvc_home.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            yaml.safe_dump(config, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        logger.info(
            "Phase C: seeded skills.external_dirs += %s", target
        )
    except Exception:
        # Bootstrap must not fail because we couldn't write config
        pass


def hermes_status() -> dict[str, Any]:
    """Diagnostic snapshot — surfaced via cvc tools/status commands."""
    return {
        "available": HERMES_AVAILABLE,
        "source": HERMES_SOURCE,
        "tool_count": len(HERMES_TOOL_SCHEMAS),
        "tools": sorted(HERMES_TOOL_NAMES),
        "error": _INIT_ERROR,
    }


# Bootstrap at import — failures are logged, not raised.
_bootstrap()
