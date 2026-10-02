# Import the necessary modules
import types

import httpx
import pytest
from constants import (CHAT_COMPLETION_MESSAGES, CHAT_COMPLETION_MODEL_NAME, COMPLETION_MODEL_NAME, COMPLETION_PROMPT_1,
                       COMPLETION_PROMPT_2, EMBEDDING_INPUT_1, EMBEDDING_INPUT_2, EMBEDDING_INSTRUCTION,
                       EMBEDDING_MODEL_NAME, TEST_ECHO, TEST_ERROR_BEHAVIOR, TEST_MAX_RETRIES, TEST_MAX_TOKENS, TEST_N,
                       TEST_STOP, TEST_SUFFIX, TEST_TEMPERATURE, TEST_TIMEOUT, TEST_TOP_K, TEST_TOP_P,
                       TEST_USE_RAW_PROMPT, TEST_USER)

from databricks_genai_inference import (ChatCompletion, ChatCompletionChunkObject, ChatCompletionObject, Completion,
                                        CompletionChunkObject, CompletionObject, Embedding, EmbeddingObject)
from databricks_genai_inference.api.abstract.foundation_model_api_resource import AsyncStreamResponse


def test_embedding():
    kwargs = {
        "model": EMBEDDING_MODEL_NAME,
        "instruction": EMBEDDING_INSTRUCTION,
        "input": [EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
        "user": TEST_USER,
        "timeout": TEST_TIMEOUT,
        "max_retries": TEST_MAX_RETRIES,
    }
    try:
        response = Embedding.create(**kwargs)
        assert isinstance(response, EmbeddingObject)
    except Exception as e:
        assert False, f"Test failed due to an exception"


@pytest.mark.asyncio
async def test_async_embedding():
    kwargs = {
        "model": EMBEDDING_MODEL_NAME,
        "instruction": EMBEDDING_INSTRUCTION,
        "input": [EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
        "user": TEST_USER,
        "timeout": TEST_TIMEOUT,
        "max_retries": TEST_MAX_RETRIES,
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await Embedding.acreate(client, **kwargs)

        assert isinstance(response, EmbeddingObject)
    except Exception as e:
        assert False, f"Test failed due to an exception: {e}"


def test_completion():
    kwargs = {
        "model": COMPLETION_MODEL_NAME,
        "prompt": [COMPLETION_PROMPT_1, COMPLETION_PROMPT_2],
        "temperature": TEST_TEMPERATURE,
        "stop": TEST_STOP,
        "max_tokens": TEST_MAX_TOKENS,
        "top_p": TEST_TOP_P,
        "top_k": TEST_TOP_K,
        "user": TEST_USER,
        "timeout": TEST_TIMEOUT,
        "n": TEST_N,
        "suffix": TEST_SUFFIX,
        "echo": TEST_ECHO,
        "error_behavior": TEST_ERROR_BEHAVIOR,
        "use_raw_prompt": TEST_USE_RAW_PROMPT,
        "max_retries": TEST_MAX_RETRIES,
    }
    try:
        response = Completion.create(**kwargs)
        assert isinstance(response, CompletionObject)
        response = Completion.create(stream=True, **kwargs)
        assert isinstance(response, types.GeneratorType)
    except Exception as e:
        assert False, f"Test failed due to an exception"


@pytest.mark.asyncio
async def test_async_completion():
    kwargs = {
        "model": COMPLETION_MODEL_NAME,
        "prompt": COMPLETION_PROMPT_1,
        "temperature": TEST_TEMPERATURE,
        "stop": TEST_STOP,
        "max_tokens": TEST_MAX_TOKENS,
        "top_p": TEST_TOP_P,
        "top_k": TEST_TOP_K,
        "user": TEST_USER,
        "timeout": TEST_TIMEOUT,
        "n": TEST_N,
        "suffix": TEST_SUFFIX,
        "echo": TEST_ECHO,
        "error_behavior": TEST_ERROR_BEHAVIOR,
        "use_raw_prompt": TEST_USE_RAW_PROMPT,
        "max_retries": TEST_MAX_RETRIES,
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await Completion.acreate(client, **kwargs)
            assert isinstance(response, CompletionObject)
            response = await Completion.acreate(client, stream=True, **kwargs)
            assert isinstance(response, AsyncStreamResponse)
            async for data in response:
                assert isinstance(data, CompletionChunkObject)
    except Exception as e:
        assert False, f"Test failed due to an exception: {e}"


def test_chat_completion():
    kwargs = {
        "model": CHAT_COMPLETION_MODEL_NAME,
        "messages": CHAT_COMPLETION_MESSAGES,
        "temperature": TEST_TEMPERATURE,
        "stop": TEST_STOP,
        "max_tokens": TEST_MAX_TOKENS,
        "top_p": TEST_TOP_P,
        "top_k": TEST_TOP_K,
        "user": TEST_USER,
        "timeout": TEST_TIMEOUT,
        "n": TEST_N,
        "max_retries": TEST_MAX_RETRIES,
    }
    try:
        response = ChatCompletion.create(**kwargs)
        assert isinstance(response, ChatCompletionObject)
        response = ChatCompletion.create(stream=True, **kwargs)
        assert isinstance(response, types.GeneratorType)
    except Exception as e:
        assert False, f"Test failed due to an exception"


@pytest.mark.asyncio
async def test_async_chat_completion():
    kwargs = {
        "model": CHAT_COMPLETION_MODEL_NAME,
        "messages": CHAT_COMPLETION_MESSAGES,
        "temperature": TEST_TEMPERATURE,
        "stop": TEST_STOP,
        "max_tokens": TEST_MAX_TOKENS,
        "top_p": TEST_TOP_P,
        "top_k": TEST_TOP_K,
        "user": TEST_USER,
        "timeout": TEST_TIMEOUT,
        "n": TEST_N,
        "max_retries": TEST_MAX_RETRIES,
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await ChatCompletion.acreate(client, **kwargs)
            assert isinstance(response, ChatCompletionObject)
            response = await ChatCompletion.acreate(client, stream=True, **kwargs)
            assert isinstance(response, AsyncStreamResponse)
            async for data in response:
                assert isinstance(data, ChatCompletionChunkObject)
    except Exception as e:
        assert False, f"Test failed due to an exception: {e}"


if __name__ == "__main__":
    pytest.main()
