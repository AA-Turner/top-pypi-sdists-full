import asyncio
import time
from typing import TYPE_CHECKING, Optional, Union, List
from abc import ABC, abstractmethod

from fireworks._literals import ReasoningEffort
from fireworks.client.error import InvalidRequestError, RateLimitError, BadGatewayError, ServiceUnavailableError
from fireworks._logger import logger
from fireworks.llm._types import ResponseFormat

# Type checking imports to avoid circular imports
if TYPE_CHECKING:
    from fireworks.llm.llm import LLM

DEFAULT_MAX_RETRIES = 10
DEFAULT_DELAY = 0.5


class BaseCompletion(ABC):
    """Base class for completion wrappers that provides common functionality."""

    def __init__(self, llm: "LLM"):
        self._llm = llm

    def _create_setup(self):
        """
        Setup for .create() and .acreate()
        """
        self._llm._ensure_deployment_ready()
        model_id = self._llm.model_id()
        return model_id

    def _should_retry_error(self, e: Exception) -> bool:
        """Check if an error should trigger a retry."""
        if isinstance(e, InvalidRequestError):
            error_msg = str(e).lower()
            return any(
                msg in error_msg
                for msg in ["model not found, inaccessible, and/or not deployed", "model does not exist"]
            )
        return isinstance(e, (BadGatewayError, ServiceUnavailableError, RateLimitError))

    def _execute_with_retry(self, params: dict, stream: bool, operation_name: str):
        """Execute a request with retry logic for synchronous calls."""
        retries = 0
        delay = DEFAULT_DELAY
        while retries < self._llm.max_retries:
            try:
                if self._llm.enable_metrics and not stream:
                    start_time = time.time()

                result = self._client.create(**params)  # type: ignore

                if self._llm.enable_metrics and not stream:
                    end_time = time.time()
                    self._llm._metrics.add_metric("time_to_last_token", end_time - start_time)

                return result
            except Exception as e:
                if not self._should_retry_error(e):
                    raise e
                logger.debug(f"{type(e).__name__}: {e}. operation: {operation_name}")
                time.sleep(delay)
                retries += 1
                delay *= 2
        raise Exception(f"Failed to create {operation_name} after {self._llm.max_retries} retries")

    async def _execute_with_retry_async(self, params: dict, stream: bool, operation_name: str):
        """Execute a request with retry logic for asynchronous calls."""
        retries = 0
        delay = DEFAULT_DELAY
        while retries < self._llm.max_retries:
            try:
                resp_or_generator = self._client.acreate(**params)  # type: ignore
                if stream:
                    return resp_or_generator  # type: ignore
                else:
                    if self._llm.enable_metrics:
                        start_time = time.time()
                    resp = await resp_or_generator  # type: ignore
                    if self._llm.enable_metrics:
                        end_time = time.time()
                        self._llm._metrics.add_metric("time_to_last_token", end_time - start_time)
                    return resp
            except Exception as e:
                if not self._should_retry_error(e):
                    raise e
                logger.debug(f"{type(e).__name__}: {e}. operation: {operation_name}")
                await asyncio.sleep(delay)
                retries += 1
                delay *= 2
        raise Exception(f"Failed to create {operation_name} after {self._llm.max_retries} retries")

    def _build_common_request_params(
        self,
        model_id: str,
        stream: bool = False,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        repetition_penalty: Optional[float] = None,
        reasoning_effort: Optional[ReasoningEffort] = None,
        mirostat_lr: Optional[float] = None,
        mirostat_target: Optional[float] = None,
        n: Optional[int] = None,
        ignore_eos: Optional[bool] = None,
        stop: Optional[Union[str, List[str]]] = None,
        response_format: Optional[ResponseFormat] = None,
        context_length_exceeded_behavior: Optional[str] = None,
        user: Optional[str] = None,
        extra_headers=None,
        **kwargs,
    ) -> dict:
        """Build common request parameters shared by both completion types."""
        # Start with required parameters and those that have default handling
        params = {
            "model": model_id,
            "stream": stream,
            "temperature": temperature if temperature is not None else self._llm.temperature,
            **kwargs,
        }

        # Only add optional parameters if they are not None
        optional_params = {
            "extra_headers": extra_headers,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "top_k": top_k,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "repetition_penalty": repetition_penalty,
            "reasoning_effort": reasoning_effort,
            "mirostat_lr": mirostat_lr,
            "mirostat_target": mirostat_target,
            "n": n,
            "ignore_eos": ignore_eos,
            "stop": stop,
            "response_format": response_format,
            "context_length_exceeded_behavior": context_length_exceeded_behavior,
            "user": user,
        }

        # Add only non-None optional parameters
        for key, value in optional_params.items():
            if value is not None:
                params[key] = value

        return params

    @abstractmethod
    def _build_request_params(self, model_id: str, *args, **kwargs) -> dict:
        """Build request parameters - must be implemented by subclasses."""
        pass
