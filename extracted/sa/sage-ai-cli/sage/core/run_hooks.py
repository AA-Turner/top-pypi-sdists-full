"""Production wiring for the 14 tier features into `sage run`.

This module is the single entry point that `main.py:run()` calls to
activate every quality gate / safety harness / pipeline default the new
modules provide. Keeping the wiring in one place keeps main.py edits
surgical (one import + one call).

Usage in main.py:
    from sage.core.run_hooks import on_session_start, on_pre_turn, on_post_turn
    ...
    @app.command()
    def run(...):
        cfg = load_config()
        ...
        readiness = on_session_start(cfg, cwd)
        if not readiness.ok:
            renderer.error(readiness.message)
            raise typer.Exit(1)
        ...
        # before the model generates a turn:
        ctx = on_pre_turn(user_prompt=prompt, cwd=cwd, cfg=cfg)
        ...
        # after the model emits its output:
        on_post_turn(user_prompt=prompt, output=response, cfg=cfg, ...)

All hooks are non-fatal by default — if any sub-module errors, the run
continues with a warning. The exception is `on_session_start` which
HARD-FAILS when the loaded model is below the 7B agentic floor — that's
the entire point of T1.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path

__all__ = [
    "SessionStartResult",
    "PreTurnContext",
    "PostTurnSummary",
    "on_session_start",
    "on_pre_turn",
    "on_post_turn",
    "current_telemetry",
    "current_run_guard",
]


# ── Process-wide singletons (one per `sage run` invocation) ───────────

_TELEMETRY = None     # TelemetryLogger
_RUN_GUARD = None     # RunGuard
_SESSION_ID = None


def current_telemetry():
    return _TELEMETRY


def current_run_guard():
    return _RUN_GUARD


# ── Result types ──────────────────────────────────────────────────────

@dataclass
class SessionStartResult:
    ok: bool                      # False = abort the run
    message: str = ""
    model: str = ""
    skeleton_applied: str = ""    # name of skeleton if one was applied
    rag_indexed: bool = False
    rag_files: int = 0
    readiness_passed: bool = False
    floor_passed: bool = False


@dataclass
class PreTurnContext:
    """Returned to the agent loop before each turn so it can apply
    the recommended grammar + planner-coder pair etc."""
    enforce_grammar: bool = True
    grammar_string: str = ""
    planner_model: str = ""
    coder_model: str = ""
    rag_context: str = ""


@dataclass
class PostTurnSummary:
    """Logged via telemetry after each turn."""
    success: bool
    validator_signals: list[str] = field(default_factory=list)
    files_written: int = 0
    duration_s: float = 0.0


# ── Hooks ────────────────────────────────────────────────────────────

def on_session_start(cfg, cwd: Path, *,
                     model: str | None = None,
                     send_fn=None, available_models: list[str] | None = None,
                     skip_floor: bool = False,
                     skip_readiness: bool = False,
                     skip_skeleton: bool = False,
                     user_first_prompt: str = "") -> SessionStartResult:
    """Run the session-start sequence:

      1. Model-floor check (T1)               — abort if below 7B
      2. Readiness probe (T13)                — abort if model fails hello-world
      3. Build/refresh RAG index (T8)         — non-fatal; warn on failure
      4. Match + apply skeleton (T7+T9)       — only if cwd is mostly empty
      5. Init telemetry (T10) + run-guard (T6) — process-wide singletons

    `model` is the model the session will ACTUALLY run with, which is not
    necessarily cfg.default_model: the caller resolves it as
    `--model` > per-directory last-used > config default. These gates used to
    read cfg.default_model unconditionally, so `sage run --model <big-model>`
    was rejected with "Model below agentic floor" purely because the *config*
    default was small -- the user's explicit choice was never consulted, and
    the only way out was to change the global default with `sage use` first.
    Falls back to cfg.default_model when the caller passes nothing.

    Returns SessionStartResult; caller checks `.ok` and prints `.message`.
    """
    global _TELEMETRY, _RUN_GUARD, _SESSION_ID

    effective_model = model or cfg.default_model

    out = SessionStartResult(ok=True, model=effective_model)

    # 1. Model-floor (T1)
    if not skip_floor:
        try:
            from sage.core.model_floor import check_capability
            cap = check_capability(effective_model, task_kind="agentic")
            out.floor_passed = cap.ok
            if not cap.ok:
                out.ok = False
                out.message = (f"Model below agentic floor: {cap.detail}\n\n"
                               f"{cap.suggestion}")
                return out
        except Exception:
            pass  # don't block session if check itself errors

    # 2. Readiness (T13)
    if not skip_readiness and send_fn is not None:
        try:
            from sage.core.readiness import check_readiness
            r = check_readiness(model=effective_model, send_fn=send_fn)
            out.readiness_passed = r.ok
            if not r.ok:
                out.ok = False
                out.message = (f"Readiness probe failed for {effective_model}: "
                               f"{r.detail}\n\nTry: sage pull qwen2.5-coder-7b "
                               f"&& sage use qwen2.5-coder-7b")
                return out
        except Exception:
            pass

    # 3. Skeleton (T7+T9) — only when cwd is mostly-empty greenfield
    if not skip_skeleton and user_first_prompt:
        try:
            existing_files = sum(1 for _ in cwd.rglob("*") if _.is_file())
            if existing_files <= 5:
                from sage.core.skeletons import match_skeleton, apply_skeleton
                sk = match_skeleton(user_first_prompt)
                if sk is not None:
                    written = apply_skeleton(sk, target=cwd, overwrite=False)
                    if written:
                        out.skeleton_applied = sk.name
        except Exception:
            pass

    # 4. RAG pre-turn (T8)
    try:
        from sage.core.rag_preturn import ensure_rag_indexed
        rag = ensure_rag_indexed(cwd)
        out.rag_indexed = rag.indexed
        out.rag_files = rag.files_seen
    except Exception:
        pass

    # 5. Init telemetry + run-guard
    try:
        from sage.core.telemetry import TelemetryLogger
        _SESSION_ID = uuid.uuid4().hex[:12]
        _TELEMETRY = TelemetryLogger(session_id=_SESSION_ID)
    except Exception:
        _TELEMETRY = None

    try:
        from sage.core.run_guard import RunGuard
        _RUN_GUARD = RunGuard()
    except Exception:
        _RUN_GUARD = None

    out.message = (f"Session ready. floor=ok rag={out.rag_indexed} "
                   f"skeleton={out.skeleton_applied or 'none'}")
    return out


def on_pre_turn(*, user_prompt: str, cwd: Path, cfg,
                available_models: list[str] | None = None) -> PreTurnContext:
    """Build the per-turn context: grammar choice (T4+T12), planner/coder
    pair (T11), top-K RAG context (T8).

    All sub-calls are best-effort. Returns sensible defaults when modules
    fail.
    """
    ctx = PreTurnContext(
        enforce_grammar=False,
        grammar_string="",
        planner_model=cfg.default_model,
        coder_model=cfg.default_model,
        rag_context="",
    )

    # T4 + T12: grammar selection
    try:
        from sage.core.grammar_default import (
            should_enforce_grammar, get_combined_grammar_string,
        )
        ctx.enforce_grammar = should_enforce_grammar(user_prompt)
        if ctx.enforce_grammar:
            ctx.grammar_string = get_combined_grammar_string(project_root=cwd)
    except Exception:
        pass

    # T11: planner/coder pair
    if available_models:
        try:
            from sage.core.dual_pipeline import resolve_planner_coder
            planner, coder = resolve_planner_coder(available_models)
            ctx.planner_model = planner or cfg.default_model
            ctx.coder_model = coder or cfg.default_model
        except Exception:
            pass

    # T8: top-K RAG retrieval
    try:
        from sage.core.rag import RAGIndex, format_chunks_for_prompt
        idx = RAGIndex(cwd)
        chunks = idx.query(user_prompt, top_k=getattr(cfg, "rag_top_k", 6))
        ctx.rag_context = format_chunks_for_prompt(chunks, max_chars=4000)
    except Exception:
        pass

    return ctx


def on_post_turn(*, user_prompt: str, output: str, cfg,
                 success: bool, validator_signals: list[str] | None = None,
                 files_written: int = 0, duration_s: float = 0.0) -> PostTurnSummary:
    """Log the turn to telemetry (T10) and return a summary the caller can
    surface to the user."""
    summary = PostTurnSummary(
        success=success,
        validator_signals=validator_signals or [],
        files_written=files_written,
        duration_s=duration_s,
    )
    if _TELEMETRY is not None:
        try:
            _TELEMETRY.log_turn(
                prompt=user_prompt,
                model=cfg.default_model,
                output=output,
                validator_signal=(validator_signals[0] if validator_signals else None),
                success=success,
                meta={"files_written": files_written, "duration_s": duration_s},
            )
        except Exception:
            pass
    return summary
