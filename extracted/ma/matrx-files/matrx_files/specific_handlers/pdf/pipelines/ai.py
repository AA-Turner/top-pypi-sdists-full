"""AI chunk processor — dispatches each chunk through a caller-supplied callable.

By default all chunks are fired in parallel via ``asyncio.gather`` to preserve
the original behavior. Pass ``max_concurrent=N`` to gate dispatch through an
``asyncio.Semaphore`` — useful when the *ai_processor* hits an upstream LLM
provider with per-second rate limits.
"""

from __future__ import annotations

import asyncio
from typing import Any

from ..internal import build_info_payload
from ..models import AiChunkProcessor


async def process_chunks_with_ai(
    chunks: list[str],
    ai_processor: AiChunkProcessor,
    emitter: Any | None = None,
    max_concurrent: int | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    if max_concurrent is not None and max_concurrent > 0:
        sem = asyncio.Semaphore(max_concurrent)

        async def _bounded(chunk: str) -> dict[str, Any]:
            async with sem:
                return await ai_processor(chunk)

        tasks = [_bounded(chunk) for chunk in chunks]
    else:
        tasks = [ai_processor(chunk) for chunk in chunks]

    responses = await asyncio.gather(*tasks, return_exceptions=True)

    for idx, resp in enumerate(responses):
        if isinstance(resp, Exception):
            print(f"[matrx-pdf-ai] chunk {idx} failed: {resp}")
            results.append({"error": str(resp), "chunk_index": idx})
        else:
            content = resp.get("content") if isinstance(resp, dict) else None
            results.append({"content": content, "chunk_index": idx})

        if emitter:
            await emitter.send_info(
                build_info_payload(
                    code="pdf_chunk_progress",
                    system_message=f"ai_chunks {idx + 1}/{len(chunks)}",
                    user_message=f"AI processed chunk {idx + 1} of {len(chunks)}",
                )
            )

    return results


__all__ = ["process_chunks_with_ai"]
