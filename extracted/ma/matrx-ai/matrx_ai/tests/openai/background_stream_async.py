import asyncio
from typing import List

import rich
from pydantic import BaseModel
from openai.types.shared_params import Reasoning

from openai import AsyncOpenAI


class Step(BaseModel):
    explanation: str
    output: str


class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str


async def main() -> None:
    client = AsyncOpenAI()
    id = None
    async with client.responses.stream(
        input="solve 8x + 31 = 2",
        model="gpt-5-mini",
        include=["reasoning.encrypted_content"],
        reasoning=Reasoning(effort="medium", summary="detailed"),
        text_format=MathResponse,
        background=True,
    ) as stream:
        async for event in stream:
            if event.type == "response.created":
                id = event.response.id
            if "output_text" in event.type:
                rich.print(event)
            if event.sequence_number == 125:
                break

    print("Interrupted. Continuing...")

    assert id is not None
    async with client.responses.stream(
        response_id=id,
        starting_after=125,
        text_format=MathResponse,
    ) as stream:
        async for event in stream:
            if "output_text" in event.type:
                rich.print(event)

        rich.print(await stream.get_final_response())


if __name__ == "__main__":
    asyncio.run(main())
