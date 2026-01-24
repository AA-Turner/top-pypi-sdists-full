import logging
from typing import Any, Callable, Generic, TypeVar

from celery import shared_task
from django.db import models
from django.db.models.signals import ModelSignal
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from wbcore.workers import Queue

from ..exceptions import APIStatusErrors, BadRequestErrors
from .utils import run_llm

logger = logging.getLogger("llm")


@shared_task(
    queue=Queue.BACKGROUND.value,
    autoretry_for=tuple(APIStatusErrors),
    retry_backoff=10,
    max_retries=5,  # retry 5 times maximum
    default_retry_delay=60,  # retry in 60s
    retry_jitter=False,
)
def invoke_as_task(
    instance,
    prompt: str,
    chat_model: type[BaseChatModel],
    chat_model_name: str,
    max_tokens: int,
    model_field: str | None,
    output_model: "type[BaseModel] | None",
    tools: list[dict[str, Any]],
    query: Callable | dict[str, Any] | None,
    extra_query: dict[str, Any] | None,
    llm_kwargs: dict[str, Any] | None,
    result_parser: Callable | None,
):
    try:
        if callable(query):
            query = query(instance)
        if not query:
            query = dict()
        if extra_query:
            query.update(extra_query)

        output_result, ai_msg = run_llm(
            prompt, output_model, chat_model, chat_model_name, max_tokens, query=query, extra_tools=tools, **llm_kwargs
        )
        # if a result parser is provided, we use this to parse the results into the instance
        if result_parser:
            instance = result_parser(instance, output_result, ai_msg)
        elif output_result and isinstance(output_result, BaseModel):
            for field, value in output_result.model_dump().items():
                setattr(instance, field, value)
    except tuple(BadRequestErrors) as e:  # we silent bad request error because there is nothing we can do about it
        logger.warning(str(e))
    except tuple(APIStatusErrors) as e:  # for APIStatusError, we let celery retry it
        raise e
    except Exception as e:  # otherwise we log the error and silently fail
        logger.warning(str(e))
    return instance


T = TypeVar("T", bound=models.Model)


add_llm_prompt = ModelSignal()


class LLMConfig(Generic[T]):
    def __init__(
        self,
        key: str,
        prompt: Callable | str | list[BaseMessage],
        field: str | None = None,
        output_model: "type[BaseModel] | None" = None,
        on_save: bool = True,
        on_condition: Callable | bool | None = None,
        chat_model: Callable | tuple[type[BaseChatModel], str] = (ChatOpenAI, "gpt-4o-mini"),
        max_tokens: int = 16000,
        tools: Callable | list[dict[str, str]] | None = None,
        query: Callable | dict[str, Any] | None = None,
        llm_kwargs_callback: Callable | None = None,
        result_parser: Callable | None = None,
        **llm_kwargs,
    ):
        self.key = key
        self.on_save = on_save
        self.field = field
        self.on_condition = on_condition
        self.prompt = prompt
        self.output_model = output_model
        self.chat_model = chat_model
        self.max_tokens = max_tokens
        self.tools = tools
        self.query = query
        self.llm_kwargs_callback = llm_kwargs_callback
        self.llm_kwargs = llm_kwargs
        self.result_parser = result_parser

    def check_condition(self, instance: T) -> bool:
        if self.on_condition is None:
            return True
        if callable(self.on_condition):
            return self.on_condition(instance)
        return bool(self.on_condition)

    def _get_prompt(self, instance: T):
        prompt = self.prompt
        extra_query = dict()
        if callable(prompt):
            prompt = prompt(instance)
        for _, response in add_llm_prompt.send(sender=instance.__class__, instance=instance, key=self.key):
            remote_prompts, remote_query = response
            prompt.extend(remote_prompts)
            extra_query.update(remote_query)

        return prompt, extra_query

    def _get_chat_model(self, instance: T) -> tuple[type[BaseChatModel], str]:
        if callable(self.chat_model):
            return self.chat_model(instance)
        return self.chat_model

    def _get_tools(self, instance: T) -> list[dict[str, Any]]:
        if callable(self.tools):
            return self.tools(instance)
        return self.tools

    def _get_llm_kwargs(self, instance: T) -> dict[str, Any]:
        llm_kwargs = self.llm_kwargs
        if callable(self.llm_kwargs_callback):
            llm_kwargs = self.llm_kwargs_callback(instance)
        return llm_kwargs

    def schedule(self, instance: T, initial: bool = True):
        prompt, extra_query = self._get_prompt(instance)
        args = []
        if initial:
            args.append(instance)
        chat_model, chat_model_name = self._get_chat_model(instance)
        tools = self._get_tools(instance)
        llm_kwargs = self._get_llm_kwargs(instance)
        args.extend(
            [
                prompt,
                chat_model,
                chat_model_name,
                self.max_tokens,
                self.field,
                self.output_model,
                tools,
                self.query,
                extra_query,
                llm_kwargs,
                self.result_parser,
            ]
        )
        return invoke_as_task.s(*args)

    def invoke(self, instance: T):
        self.schedule(instance)()
