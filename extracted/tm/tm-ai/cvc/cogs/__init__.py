"""
cvc.cogs — Cognition Compiler.

The Cognition Compiler is CVC's answer to the markdown-memory paradigm used by
Claude Code, OpenClaw, Cursor, Letta, upstream, and every other agent today.
Instead of re-ingesting a pile of ``.md`` files on every LLM call, CVC distills
each successful LLM-derived solution into a **Cog** — a compiled, executable,
Merkle-addressed cognitive artifact that runs with zero LLM tokens on future
matching tasks.

The LLM becomes the slow path (novel problems only); compiled Cogs are the
fast path.  Each Cog carries:

* A typed intent/input/output signature (for exact-match routing).
* A semantic embedding of the trigger (for near-match retrieval).
* An executable body (Python function or declarative rule DAG).
* An auto-generated regression test drawn from the originating commit trace.
* Provenance pointers to the cognitive commits that evidenced the pattern.
* Live ROI telemetry (invocations, success_rate_7d, tokens_saved_cumulative).

This package is **purely additive**: it does not modify the engine, adapters,
database, or CLI.  Integration is opt-in via the public API exposed here.
"""

from __future__ import annotations

from cvc.cogs.cache import CogHitResult, CognitiveCache
from cvc.cogs.compiler import CognitionCompiler, LLMCaller
from cvc.cogs.executor import ExecutionError, ExecutionResult, SafeExecutor
from cvc.cogs.integration import CogBridge
from cvc.cogs.models import (
    Cog,
    CogBody,
    CogBodyKind,
    CogSignature,
    CogTelemetry,
    compute_cog_id,
)
from cvc.cogs.registry import CogRegistry, CogVectorIndex
from cvc.cogs.sdcp import ContextAtom, SemanticDeltaContext

__all__ = [
    "Cog",
    "CogBody",
    "CogBodyKind",
    "CogBridge",
    "CogHitResult",
    "CogRegistry",
    "CogSignature",
    "CogTelemetry",
    "CogVectorIndex",
    "CognitionCompiler",
    "CognitiveCache",
    "ContextAtom",
    "ExecutionError",
    "ExecutionResult",
    "LLMCaller",
    "SafeExecutor",
    "SemanticDeltaContext",
    "compute_cog_id",
]
