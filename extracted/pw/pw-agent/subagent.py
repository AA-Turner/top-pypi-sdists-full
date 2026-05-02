"""Subagents — spawn focused sub-conversations from the main agent.

A subagent is a fresh ReAct loop with its own conversation history,
running on the same LLM client. It's used for tasks where the parent
agent wants to:
  - delegate a focused exploration ("find all places where X is used")
  - parallelize independent work ("run tests on these 3 files in parallel")
  - keep its main context clean of large intermediate results

The subagent receives a self-contained task description, runs to
completion in quiet mode, and returns just its final answer.

Subagents do NOT have access to spawn more subagents (no recursion).
Subagents share the same LLM client + memory store as the parent.
"""

import threading
from typing import Optional


def run_subagent(parent_agent, task: str, max_iterations: int = 20) -> str:
    """Run a focused subagent task synchronously and return its final answer.

    The subagent inherits the parent's LLM client, memory, and skills,
    but starts with a fresh conversation. It cannot spawn its own
    subagents (the spawn_agent tool is removed from its tool list).
    """
    # Lazy import to avoid circular dep
    from agent import Agent

    if getattr(parent_agent, "is_subagent", False):
        return "Error: subagents cannot spawn other subagents"

    sub = Agent(
        client=parent_agent.client,
        stream=False,  # No streaming for subagents — we want clean final answer
        plan_mode=parent_agent.plan_mode,
        thinking=False,  # No thinking — keep it fast
        quiet=True,  # Suppress all UI
        memory_store=parent_agent.memory,
    )
    sub.is_subagent = True
    sub.skills = parent_agent.skills  # Inherit skills

    try:
        sub.run(task)
    except Exception as e:
        return f"Error: subagent crashed — {e}"

    # Extract the final assistant message
    for msg in reversed(sub.conversation):
        if msg.get("role") == "assistant":
            content = msg.get("content", "").strip()
            # Skip pure tool_call messages
            if "<tool_call>" in content or "ACTION:" in content:
                continue
            return content or "(subagent returned empty response)"

    return "(subagent did not produce a final answer)"


def run_subagents_parallel(parent_agent, tasks: list[str], max_iterations: int = 20) -> list[str]:
    """Run multiple subagent tasks in parallel threads. Returns answers in order."""
    results: list[Optional[str]] = [None] * len(tasks)

    def _worker(idx: int, task: str):
        try:
            results[idx] = run_subagent(parent_agent, task, max_iterations)
        except Exception as e:
            results[idx] = f"Error: {e}"

    threads = [threading.Thread(target=_worker, args=(i, t)) for i, t in enumerate(tasks)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=300)  # 5 min cap per subagent

    return [r if r is not None else "(subagent timed out)" for r in results]
