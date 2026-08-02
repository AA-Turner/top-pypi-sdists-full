"""Layer 2 chunked map-reduce compaction.

Split into its own mixin because it's the single largest method cluster
in the optimizer (~330 lines, 4 methods) and is functionally orthogonal
to the rest of Layer 2 — when the conversation is small enough to fit in
one summarization call, none of these methods run at all.

The mixin has no fields; it reads its configuration off the
``XPanderContextOptimizer`` dataclass via ``self.<field>``.
"""

from __future__ import annotations

import asyncio
import json
import random
import time
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional

from loguru import logger

from agno.models.message import Message

from xpander_sdk.core.context_optimizer.constants import (
    _MAP_CHUNK_RETRY_ATTEMPTS,
    _MAP_CHUNK_RETRY_BASE_DELAY,
    _MAP_CHUNK_RETRY_JITTER,
    _is_rate_limit_error,
)
from xpander_sdk.core.context_optimizer.helpers.chunking import (
    _split_messages_into_chunks,
)
from xpander_sdk.core.context_optimizer.prompts import (
    AUTO_COMPACT_SYSTEM_PROMPT,
    AUTO_COMPACT_USER_PROMPT_TEMPLATE,
    PARTIAL_COMPACT_SYSTEM_PROMPT,
    PARTIAL_COMPACT_USER_PROMPT_TEMPLATE,
)

if TYPE_CHECKING:
    from agno.metrics import RunMetrics


class MapReduceMixin:
    """Chunked summarization for conversations too large for a single
    Layer 2 LLM call.
    """

    def _compute_chunk_char_budget(
        self, provider_max_tokens: Optional[int] = None
    ) -> int:
        """Derive a safe per-chunk input char budget.

        Starts from the smaller of the agent-declared ``context_window`` and
        any provider-reported max (set via ``_provider_max_tokens`` or the
        *provider_max_tokens* override), subtracts ``reserved_for_output`` and
        ``buffer_tokens``, and converts to chars using the same chars/token
        heuristic the rest of the optimizer uses (chars ≈ tokens * 4 / 1.2).
        Capped at ``max_chunk_input_tokens`` so chunks stay small enough that
        each map call returns quickly and the gather over chunks parallelizes.
        """
        caps = [self.context_window]
        if self._provider_max_tokens:
            caps.append(self._provider_max_tokens)
        if provider_max_tokens:
            caps.append(provider_max_tokens)
        effective_cap = min(c for c in caps if c and c > 0)
        budget_tokens = max(
            1, effective_cap - self.reserved_for_output - self.buffer_tokens
        )
        if self.max_chunk_input_tokens and self.max_chunk_input_tokens > 0:
            budget_tokens = min(budget_tokens, self.max_chunk_input_tokens)
        # chars ≈ tokens * 4 / 1.2 (matches ``_estimate_tokens`` heuristic).
        return max(1_000, int(budget_tokens * 4 / 1.2))

    async def _map_chunk_with_retry(
        self,
        idx: int,
        total_chunks: int,
        user_prompt: str,
        trigger: Literal["auto", "manual", "emergency", "pre_retry"],
        run_metrics: Optional["RunMetrics"],
        sem: "asyncio.Semaphore",
    ) -> Optional[tuple]:
        """Run a single map call under *sem*, retrying transient 429s.

        Returns ``(idx, partial_text, in_tok, out_tok)`` on success, or
        ``None`` if all retries failed.
        """
        async with sem:
            for attempt in range(_MAP_CHUNK_RETRY_ATTEMPTS):
                try:
                    partial, in_tok, out_tok = await self._run_llm_compaction_call(
                        system_prompt=PARTIAL_COMPACT_SYSTEM_PROMPT,
                        user_prompt=user_prompt,
                        run_metrics=run_metrics,
                        progress_label=f"layer 2 (map {idx}/{total_chunks})",
                        trigger=None,
                        percent_start=None,
                        percent_end=None,
                        progress_detail=None,
                    )
                    return idx, partial, in_tok, out_tok
                except Exception as exc:
                    if (
                        not _is_rate_limit_error(exc)
                        or attempt == _MAP_CHUNK_RETRY_ATTEMPTS - 1
                    ):
                        logger.error(
                            f"[context-optimizer] layer 2 (map {idx}/{total_chunks}): "
                            f"failed (attempt {attempt + 1}/{_MAP_CHUNK_RETRY_ATTEMPTS}): {exc}"
                        )
                        if attempt == _MAP_CHUNK_RETRY_ATTEMPTS - 1:
                            return None
                        raise
                    delay = _MAP_CHUNK_RETRY_BASE_DELAY * (2**attempt)
                    delay += random.uniform(
                        -_MAP_CHUNK_RETRY_JITTER * delay,
                        _MAP_CHUNK_RETRY_JITTER * delay,
                    )
                    logger.warning(
                        f"[context-optimizer] layer 2 (map {idx}/{total_chunks}): "
                        f"rate-limited (attempt {attempt + 1}/{_MAP_CHUNK_RETRY_ATTEMPTS}), "
                        f"retrying in {delay:.1f}s"
                    )
                    await asyncio.sleep(delay)
            return None

    async def _run_chunked_map(
        self,
        messages: List[Any],
        char_budget: int,
        trigger: Literal["auto", "manual", "emergency", "pre_retry"],
        run_metrics: Optional["RunMetrics"],
        recursion_depth: int,
    ) -> tuple:
        """Summarize *messages* chunk-by-chunk. Returns ``(partials, total_tokens)``.

        Map calls run concurrently up to ``map_phase_max_concurrency`` since
        each chunk is independent. If more than half of the chunks fail under
        parallel dispatch, fall back to a serial single-flight pass with the
        same retry policy.
        """
        chunks = _split_messages_into_chunks(messages, char_budget)
        total_chunks = len(chunks)
        total_tokens = 0
        logger.info(
            f"[context-optimizer] layer 2 (chunked): map phase "
            f"depth={recursion_depth} chunks={total_chunks} budget={char_budget:,} chars "
            f"concurrency={self.map_phase_max_concurrency}"
        )

        prompts: List[str] = []
        for idx, chunk in enumerate(chunks, start=1):
            conversation = json.dumps(
                [
                    (
                        m.to_dict()
                        if hasattr(m, "to_dict")
                        else {
                            "role": getattr(m, "role", "user"),
                            "content": str(getattr(m, "content", "")),
                        }
                    )
                    for m in chunk
                ],
                default=str,
                ensure_ascii=False,
            )
            prompts.append(
                PARTIAL_COMPACT_USER_PROMPT_TEMPLATE.format(
                    chunk_index=idx,
                    total_chunks=total_chunks,
                    conversation=conversation,
                )
            )

        await self._emit_progress(
            trigger=trigger,
            percent=5.0,
            detail=f"Analyzing conversation (0 of {total_chunks})",
            force=True,
        )

        sem = asyncio.Semaphore(max(1, self.map_phase_max_concurrency))
        completed = 0
        results_by_idx: Dict[int, tuple] = {}

        async def _wrapped(i: int, prompt: str):
            nonlocal completed
            try:
                res = await self._map_chunk_with_retry(
                    idx=i,
                    total_chunks=total_chunks,
                    user_prompt=prompt,
                    trigger=trigger,
                    run_metrics=run_metrics,
                    sem=sem,
                )
            except Exception as exc:
                logger.error(
                    f"[context-optimizer] layer 2 (map {i}/{total_chunks}): "
                    f"unhandled error: {exc}"
                )
                res = None
            completed += 1
            chunk_span = 65.0 / max(1, total_chunks)
            pct = 5.0 + completed * chunk_span
            await self._emit_progress(
                trigger=trigger,
                percent=pct,
                detail=f"Analyzing conversation ({completed} of {total_chunks})",
            )
            return res

        results = await asyncio.gather(
            *(_wrapped(i, p) for i, p in enumerate(prompts, start=1)),
            return_exceptions=False,
        )

        failures = sum(1 for r in results if r is None)
        if failures and failures * 2 >= total_chunks:
            logger.warning(
                f"[context-optimizer] layer 2 (chunked): {failures}/{total_chunks} "
                f"map chunks failed under parallel dispatch — retrying serially"
            )
            serial_sem = asyncio.Semaphore(1)
            for i, p in enumerate(prompts, start=1):
                if results_by_idx.get(i):
                    continue
                # results list is 0-based aligned with prompts
                if results[i - 1] is not None:
                    results_by_idx[i] = results[i - 1]
                    continue
                res = await self._map_chunk_with_retry(
                    idx=i,
                    total_chunks=total_chunks,
                    user_prompt=p,
                    trigger=trigger,
                    run_metrics=run_metrics,
                    sem=serial_sem,
                )
                if res is not None:
                    results_by_idx[i] = res
        else:
            for r in results:
                if r is not None:
                    results_by_idx[r[0]] = r

        partials: List[str] = []
        for i in range(1, total_chunks + 1):
            res = results_by_idx.get(i)
            if res is None:
                partial = "(empty partial digest — map chunk failed)"
                in_tok = out_tok = 0
            else:
                _, partial, in_tok, out_tok = res
                if not partial:
                    partial = "(empty partial digest)"
            partials.append(
                f'<partial index="{i}" total="{total_chunks}">\n{partial}\n</partial>'
            )
            total_tokens += in_tok + out_tok
        return partials, total_tokens

    async def _layer_2_chunked_compact(
        self,
        messages: List[Message],
        run_metrics: Optional["RunMetrics"],
        custom_instructions: str,
        trigger: Literal["auto", "manual", "emergency", "pre_retry"],
        provider_max_tokens: Optional[int] = None,
    ) -> tuple:
        """Run map-reduce compaction: summarise chunks, then combine.

        Returns ``(summary, total_llm_tokens_used, telemetry)`` where
        telemetry is ``{"chunk_count": int, "map_phase_seconds": float,
        "reduce_phase_seconds": float}``. Raises on unrecoverable failure.
        """
        char_budget = self._compute_chunk_char_budget(provider_max_tokens)
        current_inputs: List[Any] = list(messages)
        total_tokens = 0
        map_seconds = 0.0
        reduce_seconds = 0.0
        first_pass_chunk_count: Optional[int] = None

        for depth in range(self.max_chunked_recursion_depth):
            map_start = time.monotonic()
            partials, tokens_used = await self._run_chunked_map(
                messages=current_inputs,
                char_budget=char_budget,
                trigger=trigger,
                run_metrics=run_metrics,
                recursion_depth=depth,
            )
            map_seconds += time.monotonic() - map_start
            if first_pass_chunk_count is None:
                first_pass_chunk_count = len(partials)
            total_tokens += tokens_used

            if not partials:
                raise RuntimeError("Chunked compaction produced no partial digests")

            combined_text = "\n\n".join(partials)
            combined_chars = len(combined_text)
            logger.info(
                f"[context-optimizer] layer 2 (chunked): depth={depth} "
                f"produced {len(partials)} partials ({combined_chars:,} chars, budget={char_budget:,})"
            )

            if (
                combined_chars <= char_budget
                or depth + 1 >= self.max_chunked_recursion_depth
            ):
                # Final reduce step: use the normal state-capture template.
                plan_section = self._build_plan_section()
                custom_section = (
                    f"\nAdditional focus: {custom_instructions}"
                    if custom_instructions
                    else ""
                )
                reduce_prompt = AUTO_COMPACT_USER_PROMPT_TEMPLATE.format(
                    conversation=(
                        "The original conversation was too large for a single "
                        "summarization call, so it was split into partial digests "
                        f"(R1..R{len(partials)}). Treat these digests as the "
                        "conversation and synthesize the final working-state "
                        "summary below.\n\n" + combined_text
                    ),
                    plan_section=plan_section,
                    custom_instructions_section=custom_section,
                )
                await self._emit_progress(
                    trigger=trigger,
                    percent=70.0,
                    detail="Summarizing analysis",
                )
                reduce_start = time.monotonic()
                summary, in_tok, out_tok = await self._run_llm_compaction_call(
                    system_prompt=AUTO_COMPACT_SYSTEM_PROMPT,
                    user_prompt=reduce_prompt,
                    run_metrics=run_metrics,
                    progress_label="layer 2 (reduce)",
                    trigger=trigger,
                    percent_start=70.0,
                    percent_end=95.0,
                    progress_detail="Summarizing analysis",
                )
                reduce_seconds += time.monotonic() - reduce_start
                total_tokens += in_tok + out_tok
                if not summary:
                    raise RuntimeError(
                        "Chunked compaction reduce step returned empty summary"
                    )
                telemetry = {
                    "chunk_count": first_pass_chunk_count or len(partials),
                    "map_phase_seconds": round(map_seconds, 3),
                    "reduce_phase_seconds": round(reduce_seconds, 3),
                }
                return summary, total_tokens, telemetry

            # Partials still too big for a single reduce call; recurse by
            # summarising the partials themselves.
            current_inputs = [
                SimpleNamespace(
                    role="user",
                    content=p,
                    to_dict=(lambda _p=p: {"role": "user", "content": _p}),
                )
                for p in partials
            ]

        raise RuntimeError(
            f"Chunked compaction exceeded max recursion depth ({self.max_chunked_recursion_depth})"
        )
