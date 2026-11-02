"""Exercise a virtual RobotAdapter offline, without physical hardware.

    python -m dreamscale.examples.llm_counter

With --live, makes billable managed LLM calls using saved login credentials.
The gateway must first qualify the virtual-counter/v1 profile.
Pass --max-cost to set a credit cap for live runs.
"""

from __future__ import annotations

import argparse
import asyncio
import time
from uuid import uuid4

from dreamscale import agents


class Counter:
    """Minimal adapter: describe, observe, execute, stop and close."""

    def __init__(self):
        self.value = 0
        self.stopped = False

    def describe(self) -> agents.RobotProfile:
        return agents.RobotProfile(
            id="virtual-counter/v1",
            description="A virtual counter. Read its value and increment it toward the goal.",
            tools=[
                agents.ToolSpec(
                    name="increment",
                    description="Increase the counter by one; cannot increase beyond three.",
                    parameters={"type": "object", "properties": {}, "additionalProperties": False},
                )
            ],
        )

    async def observe(self) -> agents.Observation:
        return agents.Observation(
            id=str(uuid4()),
            captured_at=time.time(),
            state={"value": self.value},
        )

    async def execute(self, call: agents.ToolCall) -> agents.ToolReceipt:
        # Every adapter validates calls locally, independently of the model.
        if self.stopped or call.name != "increment" or call.arguments or self.value >= 3:
            return agents.ToolReceipt(
                call_id=call.id,
                status="rejected",
                requested=call.arguments,
                measured={"value": self.value},
                detail="Only increments up to three are allowed.",
            )
        self.value += 1
        return agents.ToolReceipt(
            call_id=call.id,
            status="completed",
            requested=call.arguments,
            applied={"increment": 1},
            measured={"value": self.value},
        )

    async def stop(self) -> None:
        self.stopped = True

    async def close(self) -> None:
        pass


async def offline() -> None:
    counter = Counter()
    try:
        for index in range(3):
            receipt = await counter.execute(
                agents.ToolCall(id=f"offline-{index}", name="increment", arguments={})
            )
            print(f"Counter: {receipt.measured['value']} ({receipt.status})")
    finally:
        await counter.stop()
        await counter.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Use a qualified managed gateway")
    parser.add_argument("--model", default="gpt-6-astra")
    parser.add_argument("--max-cost", type=float, default=None, help="Optional cap in credits")
    args = parser.parse_args()
    if not args.live:
        asyncio.run(offline())
        return
    agents.run(
        Counter(),
        model=args.model,
        instruction="Increment the counter to exactly three, then finish.",
        max_cost=args.max_cost,
    )


if __name__ == "__main__":
    main()
