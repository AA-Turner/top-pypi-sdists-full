"""Give an assistant long-term memory: recall before answering, remember after.

SUPERMEMORY_API_KEY=... uv run examples/chat_with_memory.py
"""

import asyncio

from supermemory import AsyncSupermemory

client = AsyncSupermemory()


async def context_for(user_id: str, message: str) -> str:
    # Profile and search are independent, so fetch them in parallel.
    profile, recall = await asyncio.gather(
        client.profile(user_id),
        client.search(user_id, query=message, limit=5),
    )
    facts = [fact.memory for fact in profile.profile.static or []]
    memories = [result.memory or result.chunk or "" for result in recall.results]
    return "\n".join(["Known facts:", *facts, "", "Relevant memories:", *memories])


async def main() -> None:
    user_id = "example_user"
    message = "Can you schedule my 1:1 with Sam?"
    print(await context_for(user_id, message))
    # ...call your model with that context, then store the exchange:
    await client.add(user_id, content=f"User asked: {message}")


asyncio.run(main())
