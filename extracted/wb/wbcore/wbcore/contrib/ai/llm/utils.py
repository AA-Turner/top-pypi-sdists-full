from contextlib import suppress
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage
from langchain_core.messages.base import BaseMessage
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, ValidationError

from wbcore.contrib.ai.exceptions import LLMCallError, is_bad_request

type Prompt = str | list[BaseMessage] | BaseMessage


def _convert_prompt_to_chat_prompt_template(prompt: Prompt, format_instructions=None) -> ChatPromptTemplate:
    if isinstance(prompt, BaseMessage):
        prompt = [prompt]
    if isinstance(prompt, str):
        prompt = SystemMessage(content=prompt)
    messages = []
    for index, msg in enumerate(prompt):
        content = msg.content
        if index == 0 and format_instructions:
            if "{format_instructions}" not in content:
                content += "\n{format_instructions}"
        messages.append((msg.type, content))
    return ChatPromptTemplate.from_messages(messages).partial(format_instructions=format_instructions)


def run_llm(
    prompt: Prompt,
    output_model: "type[BaseModel] | None" = None,
    chat_model: type[BaseChatModel] = ChatOpenAI,
    chat_model_name: str = "gpt-4o-mini",
    max_tokens: int = 16000,
    extra_tools: list[dict[str, str]] | None = None,
    query: dict[str, Any] | None = None,
    **llm_kwargs,
) -> tuple[BaseModel | None, BaseMessage]:
    llm = chat_model(model=chat_model_name, max_tokens=max_tokens, **llm_kwargs)  # type: ignore
    tools = []
    if not query:
        query = {}

    if extra_tools:
        tools.extend(extra_tools)
    if output_model:
        tools.append(output_model)
    if tools:
        llm = llm.bind_tools(tools)

    # Set up a parser
    if output_model:
        parser = PydanticOutputParser(pydantic_object=output_model)
    else:
        parser = StrOutputParser()
    try:
        format_instructions = parser.get_format_instructions()
    except NotImplementedError:
        format_instructions = None
    chat_prompt_template = _convert_prompt_to_chat_prompt_template(prompt, format_instructions=format_instructions)

    chain = chat_prompt_template | llm
    try:
        response = chain.invoke(query)
    except Exception as e:
        if is_bad_request(e):
            return None, SystemMessage(content=str(e))
        raise LLMCallError(
            e,
            llm_name=chat_model.__name__,
            model=chat_model_name,
        ) from e
    if output_model:
        with suppress(ValidationError, IndexError):
            return output_model.model_validate(response.tool_calls[0]["args"]), response
    return None, response
