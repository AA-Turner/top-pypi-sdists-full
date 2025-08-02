import logging
from typing import Type, TypeVar, Union, overload
from pydantic import BaseModel
from .agent.agent import Agent

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


@overload
async def prompt(
    prompt_text: str, response_model: Type[T], max_retries: int = 3
) -> T: ...


@overload
async def prompt(
    prompt_text: str, response_model: Type[str] = str, max_retries: int = 3
) -> str: ...


async def prompt(
    prompt_text: str,
    response_model: Union[Type[T], Type[str]] = str,
    max_retries: int = 3,
) -> Union[T, str]:
    """
    Sends a prompt to the LLM and returns a response.

    Args:
        prompt_text: The text prompt to send to the LLM.
        response_model: If a Pydantic model is provided, the response will be a validated JSON object.
                        If not provided or set to str, it will be a string.
        max_retries: The maximum number of times to retry if the LLM response is not valid.

    Returns:
        If response_model is a Pydantic model, an instance of that model.
        Otherwise, the response from the LLM as a string.
    """
    agent = Agent()

    if response_model is str:
        response = agent.client.messages.create(
            model=agent.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt_text}],
        )
        if response.content and len(response.content) > 0:
            return response.content[0].text
        return ""
    else:
        response = agent.instructor_client.messages.create(
            model=agent.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt_text}],
            response_model=response_model,
            max_retries=max_retries,
        )
        return response
