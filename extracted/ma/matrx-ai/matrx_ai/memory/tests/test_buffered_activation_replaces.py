"""The Observer returns the COMPLETE observation list (existing + new). A
buffered activation must therefore replace the active block, never append to it
(appending duplicates every existing observation)."""
import asyncio
from datetime import datetime

from matrx_ai.memory import (
    InMemoryStorage, Message, MessageRole, ObservationalMemory,
    ObservationalMemoryConfig, ObservationConfig, ReflectionConfig,
)

EXISTING = "Date: Dec 4, 2025\n* 🔴 (14:30) User stated they prefer Python"
seen_existing: list[str] = []


async def llm(*, mandate_key, messages=None, model=None, variables=None):
    """Behaves like the new Observer: echoes the existing list plus one new line."""
    if mandate_key != "memory.observer":
        return "<observations>\nreflected\n</observations>"
    existing = (variables or {}).get("existing_observations", "")
    seen_existing.append(existing)
    new = f"* 🟡 (14:4{len(seen_existing)}) fact number {len(seen_existing)}"
    block = (existing or EXISTING) + "\n" + new
    return f"<observations>\n{block}\n</observations>\n<current-task>t</current-task>\n<suggested-response>s</suggested-response>"


def _msg(i):
    return Message(id=str(i), thread_id="t", resource_id="r", role=MessageRole.USER,
                   content="long enough message to trigger buffering " * 3, created_at=datetime.utcnow())


async def _run():
    storage = InMemoryStorage()
    cfg = ObservationalMemoryConfig(
        observation=ObservationConfig(token_threshold=100000, buffer_tokens=20),
        reflection=ReflectionConfig(token_threshold=100000, buffer_activation=0.5),
    )
    om = ObservationalMemory(config=cfg, storage=storage, count_tokens_fn=lambda t: len(t) // 4, llm_call_fn=llm)
    rec = await om.get_or_create_record("t", "r")
    rec.active_observations = EXISTING
    await storage.upsert_record(rec)
    await om.buffer("t", "r", [_msg(1)])
    await om.buffer("t", "r", [_msg(1), _msg(2)])  # second buffered pass builds on the first
    await om.activate("t", "r")
    return (await storage.get_record("r", "t", cfg.scope)).active_observations


def test_buffered_activation_does_not_duplicate_existing_observations():
    seen_existing.clear()
    active = asyncio.run(_run())
    assert active.count("User stated they prefer Python") == 1, active
    assert active.count("fact number 1") == 1 and active.count("fact number 2") == 1, active
    assert "fact number 1" in seen_existing[1]  # 2nd pass built on the 1st chunk's list
