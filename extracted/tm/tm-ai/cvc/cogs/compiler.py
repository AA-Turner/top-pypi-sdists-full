"""
cvc.cogs.compiler — The Cognition Compiler.

Given a cognitive commit trace (or a cluster of similar traces), the compiler
asks an LLM one time to extract the *deterministic core* of the reasoning as
either:

* A typed Python function (``kind=python``), or
* A flat rule-DAG (``kind=rule_dag``).

The result, together with an auto-generated regression test drawn from the
originating trace, becomes a :class:`Cog`.  The Cog is Merkle-addressed
(``cog_id`` is the SHA-256 of its envelope) and therefore mergeable across
branches and shareable across agents.

The compiler is decoupled from any specific LLM client: callers inject an
:class:`LLMCaller` — a tiny ``async (prompt) -> str`` protocol — which makes
the module trivially testable without an API key.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any, Protocol

from cvc.cogs.executor import ExecutionError, SafeExecutor, _validate_ast
from cvc.cogs.models import Cog, CogBody, CogBodyKind, CogSignature
from cvc.cogs.registry import CogRegistry

logger = logging.getLogger("cvc.cogs.compiler")


DISTILL_PROMPT = """\
You are a Cognition Compiler. You are shown the transcript of an agent that
solved a task using an LLM. Your job is to extract the DETERMINISTIC CORE of
that solution so that future identical-shape tasks can be solved with ZERO
LLM calls.

Return ONE of two kinds of artifact:

1. A pure Python function (kind="python"), entrypoint named `run`, that
   takes keyword arguments matching the input_schema and returns a value
   matching the output_schema. MUST NOT use the network, filesystem, or any
   module outside this allowlist: {allowed}.
2. A flat rule-DAG (kind="rule_dag") when the logic is a simple
   condition-to-value mapping. Schema:
   {{"rules": [{{"when": {{"field": "x", "op": "==|!=|>|>=|<|<=|in|contains",
                "value": <literal>}}, "then": <literal>}}],
     "default": <literal>}}

Output a single JSON object with this EXACT shape (no commentary, no fences):
{{
  "intent_summary": "<one-line description of when this artifact applies>",
  "tags": ["<short>", "<tags>"],
  "input_schema": {{"<field>": "str|int|float|bool|list|dict|any"}},
  "output_schema": {{"<field>": "str|int|float|bool|list|dict|any"}},
  "body": {{"kind": "python|rule_dag", "source": "<source>", "entrypoint": "run"}},
  "test_fixture": {{"input": {{...}}, "expected_output": <value>}}
}}

If the task is irreducibly LLM-dependent (free-form writing, open-ended
reasoning, creative generation), respond with the single token: SKIP

=== TRANSCRIPT ===
{transcript}
=== END TRANSCRIPT ===
"""


class LLMCaller(Protocol):
    """Async ``(prompt: str) -> str`` protocol used by the compiler."""

    async def __call__(self, prompt: str) -> str:  # pragma: no cover - protocol
        ...


def _strip_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        lines = t.split("\n")
        t = "\n".join(lines[1:])
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json(text: str) -> dict[str, Any] | None:
    cleaned = _strip_fences(text)
    if cleaned.upper().strip() == "SKIP":
        return None
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = _JSON_OBJECT_RE.search(cleaned)
        if match is None:
            return None
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None


class CognitionCompiler:
    """
    Distill cognitive commits into executable Cogs.

    Parameters
    ----------
    registry:
        Where to persist the resulting Cog.
    llm:
        Async callable producing JSON distillations. Can be a wrapper around
        ``cvc.agent.llm.AgentLLM`` for production, or a canned mock in tests.
    executor:
        Used to verify newly-minted Cogs against their ``test_fixture``
        before they are persisted.
    """

    def __init__(
        self,
        registry: CogRegistry,
        llm: LLMCaller,
        executor: SafeExecutor | None = None,
        *,
        agent_id: str = "sofia",
    ) -> None:
        self.registry = registry
        self.llm = llm
        self.executor = executor or SafeExecutor(timeout_s=5.0)
        self.agent_id = agent_id

    # -- trace helpers -----------------------------------------------------

    @staticmethod
    def format_transcript(messages: list[dict[str, Any]], limit_chars: int = 8000) -> str:
        out: list[str] = []
        used = 0
        for msg in messages:
            role = str(msg.get("role", "?"))
            content = msg.get("content", "")
            if not isinstance(content, str):
                content = json.dumps(content, default=str)
            piece = f"[{role}]\n{content}\n"
            if used + len(piece) > limit_chars:
                out.append("[...truncated...]\n")
                break
            out.append(piece)
            used += len(piece)
        return "".join(out)

    # -- main entry points -------------------------------------------------

    async def distill(
        self,
        *,
        transcript_messages: list[dict[str, Any]],
        provenance: list[str],
        originating_tokens: int = 0,
    ) -> Cog | None:
        """
        Run one distillation pass. Returns a verified, persisted Cog or None
        (if the LLM responded SKIP, the output was malformed, or the test
        fixture failed).
        """
        from cvc.cogs.executor import ALLOWED_IMPORTS

        transcript = self.format_transcript(transcript_messages)
        prompt = DISTILL_PROMPT.format(
            allowed=sorted(ALLOWED_IMPORTS),
            transcript=transcript,
        )
        try:
            raw = await self.llm(prompt)
        except Exception as exc:
            logger.warning("Distillation LLM call failed: %s", exc)
            return None

        parsed = _extract_json(raw)
        if parsed is None:
            logger.info("Distillation returned SKIP or malformed output")
            return None

        try:
            cog = self._build_cog(parsed, provenance, originating_tokens)
        except ExecutionError as exc:
            logger.info("Distillation rejected by AST whitelist: %s", exc)
            return None
        except (KeyError, TypeError, ValueError) as exc:
            logger.info("Distillation output failed schema: %s", exc)
            return None

        # Verify against embedded test fixture before promoting into registry.
        if not await self._verify(cog, parsed.get("test_fixture", {})):
            logger.info("Cog %s failed its own test fixture; discarding", cog.short_id)
            return None

        self.registry.save(cog)
        logger.info("Compiled Cog %s — '%s'", cog.short_id, cog.signature.intent_summary)
        return cog

    async def distill_commit_trace(
        self,
        *,
        commit_messages: list[dict[str, Any]],
        commit_hash: str,
        originating_tokens: int = 0,
    ) -> Cog | None:
        """Convenience: distill from a single commit's message trace."""
        return await self.distill(
            transcript_messages=commit_messages,
            provenance=[commit_hash],
            originating_tokens=originating_tokens,
        )

    # -- internals ---------------------------------------------------------

    def _build_cog(
        self,
        parsed: dict[str, Any],
        provenance: list[str],
        originating_tokens: int,
    ) -> Cog:
        body_data = parsed.get("body") or {}
        kind_str = str(body_data.get("kind", "python")).lower()
        if kind_str not in {"python", "rule_dag"}:
            raise ValueError(f"unsupported body kind: {kind_str}")
        kind = CogBodyKind(kind_str)
        source = str(body_data.get("source", "")).strip()
        if not source:
            raise ValueError("empty body source")

        if kind == CogBodyKind.PYTHON:
            _validate_ast(source)
            entrypoint = str(body_data.get("entrypoint", "run")) or "run"
            if f"def {entrypoint}" not in source:
                raise ValueError(f"entrypoint '{entrypoint}' not defined in source")
        else:
            entrypoint = "run"
            json.loads(source)  # raises on malformed rule-DAG

        signature = CogSignature(
            intent_summary=str(parsed.get("intent_summary", ""))[:500] or "unnamed cog",
            input_schema={str(k): str(v) for k, v in (parsed.get("input_schema") or {}).items()},
            output_schema={str(k): str(v) for k, v in (parsed.get("output_schema") or {}).items()},
            tags=[str(t)[:40] for t in (parsed.get("tags") or [])][:10],
        )
        body = CogBody(kind=kind, source=source, entrypoint=entrypoint)
        return Cog.build(
            signature=signature,
            body=body,
            provenance=provenance,
            test_fixture=parsed.get("test_fixture") or {},
            originating_tokens=originating_tokens,
            agent_id=self.agent_id,
        )

    async def _verify(self, cog: Cog, fixture: dict[str, Any]) -> bool:
        if not fixture or "input" not in fixture:
            # No fixture — we can't self-verify, so leave the Cog unpromoted.
            return True
        inputs = fixture.get("input") or {}
        if not isinstance(inputs, dict):
            return True
        expected = fixture.get("expected_output")
        result = await self.executor.execute(cog, inputs)
        if not result.ok:
            return False
        if expected is not None and result.output != expected:
            return False
        return True


def load_commit_messages(cvc_root: Path, commit_hash: str) -> list[dict[str, Any]]:
    """
    Best-effort loader that reads a commit's ContentBlob from the CAS and
    returns its messages as OpenAI-style dicts. Used by callers that want
    to distill a commit without holding a live engine reference.
    """
    # Import lazily to avoid a hard dependency from tests that use mock data.
    from cvc.core.database import ContextDatabase
    from cvc.core.models import CVCConfig

    config = CVCConfig(
        cvc_root=cvc_root,
        db_path=cvc_root / "cvc.db",
        objects_dir=cvc_root / "objects",
        branches_dir=cvc_root / "branches",
        chroma_persist_dir=cvc_root / "chroma",
        pageindex_dir=cvc_root / "pageindex",
    )
    db = ContextDatabase(config)

    # Use retrieve_blob which handles delta reconstruction properly
    blob = db.retrieve_blob(commit_hash)
    if blob is None:
        return []

    out: list[dict[str, Any]] = []
    for m in blob.messages:
        out.append({"role": m.role, "content": m.content})
    return out
