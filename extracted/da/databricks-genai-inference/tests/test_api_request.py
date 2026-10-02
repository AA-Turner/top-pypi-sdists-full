from unittest.mock import AsyncMock, patch

import pytest
from constants import (CHAT_COMPLETION_MESSAGES, CHAT_COMPLETION_MODEL_NAME, COMPLETION_MODEL_NAME, COMPLETION_PROMPT_1,
                       COMPLETION_PROMPT_2, EMBEDDING_INPUT_1, EMBEDDING_INPUT_2, EMBEDDING_INSTRUCTION,
                       EMBEDDING_MODEL_NAME, TEST_API_KEY, TEST_ECHO, TEST_ERROR_BEHAVIOR, TEST_HOST_NAME,
                       TEST_MAX_RETRIES, TEST_MAX_TOKENS, TEST_N, TEST_STOP, TEST_SUFFIX, TEST_TEMPERATURE,
                       TEST_TIMEOUT, TEST_TOP_K, TEST_TOP_P, TEST_USE_RAW_PROMPT, TEST_USER)

from databricks_genai_inference import ChatCompletion, Completion, Embedding
from databricks_genai_inference.api.abstract.foundation_model_api_resource import (DATABRICKS_HOST_ENV,
                                                                                   DATABRICKS_MODEL_URL_ENV)


class TestAPIRequest:

    def _get_expected_header(self, test_api_key: str):
        return {
            'Authorization': "Bearer " + test_api_key,
            'Content-Type': 'application/json',
            'X-Databricks-Endpoints-API-Client': 'Generative AI Inference (Mosaic) SDK'
        }

    # Fixture to change an environment variable temporarily
    @pytest.fixture(autouse=True)
    def mock_env_var(self, monkeypatch):
        monkeypatch.setenv(DATABRICKS_HOST_ENV, TEST_HOST_NAME)
        monkeypatch.setenv('DATABRICKS_TOKEN', TEST_API_KEY)
        monkeypatch.setenv(DATABRICKS_MODEL_URL_ENV, "")

    @patch('databricks_genai_inference.ChatCompletion._get_non_streaming_response')
    def test_chat_completion_request_non_streaming(self, mocked_request):
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
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{CHAT_COMPLETION_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "messages": CHAT_COMPLETION_MESSAGES,
                "temperature": TEST_TEMPERATURE,
                "stop": TEST_STOP,
                "max_tokens": TEST_MAX_TOKENS,
                "top_p": TEST_TOP_P,
                "top_k": TEST_TOP_K,
                "user": TEST_USER,
                "n": TEST_N,
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        ChatCompletion.create(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @pytest.mark.asyncio
    @patch('databricks_genai_inference.ChatCompletion._aget_non_streaming_response', new_callable=AsyncMock)
    async def test_chat_completion_async_request_non_streaming(self, mocked_request):
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
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{CHAT_COMPLETION_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "messages": CHAT_COMPLETION_MESSAGES,
                "temperature": TEST_TEMPERATURE,
                "stop": TEST_STOP,
                "max_tokens": TEST_MAX_TOKENS,
                "top_p": TEST_TOP_P,
                "top_k": TEST_TOP_K,
                "user": TEST_USER,
                "n": TEST_N,
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }

        await ChatCompletion.acreate(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @patch('databricks_genai_inference.ChatCompletion._get_streaming_response')
    def test_chat_completion_request_streaming(self, mocked_request):
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
            "stream": True,
            "max_retries": TEST_MAX_RETRIES,
        }
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{CHAT_COMPLETION_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "messages": CHAT_COMPLETION_MESSAGES,
                "temperature": TEST_TEMPERATURE,
                "stop": TEST_STOP,
                "max_tokens": TEST_MAX_TOKENS,
                "top_p": TEST_TOP_P,
                "top_k": TEST_TOP_K,
                "user": TEST_USER,
                "n": TEST_N,
                "stream": True
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        ChatCompletion.create(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @pytest.mark.asyncio
    @patch('databricks_genai_inference.ChatCompletion._aget_streaming_response', new_callable=AsyncMock)
    async def test_chat_completion_async_request_streaming(self, mocked_request):
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
            "stream": True,
            "max_retries": TEST_MAX_RETRIES,
        }
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{CHAT_COMPLETION_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "messages": CHAT_COMPLETION_MESSAGES,
                "temperature": TEST_TEMPERATURE,
                "stop": TEST_STOP,
                "max_tokens": TEST_MAX_TOKENS,
                "top_p": TEST_TOP_P,
                "top_k": TEST_TOP_K,
                "user": TEST_USER,
                "n": TEST_N,
                "stream": True
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        await ChatCompletion.acreate(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @patch('databricks_genai_inference.Completion._get_non_streaming_response')
    def test_completion_request_non_streaming(self, mocked_request):
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
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{COMPLETION_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "prompt": [COMPLETION_PROMPT_1, COMPLETION_PROMPT_2],
                "temperature": TEST_TEMPERATURE,
                "stop": TEST_STOP,
                "max_tokens": TEST_MAX_TOKENS,
                "top_p": TEST_TOP_P,
                "top_k": TEST_TOP_K,
                "user": TEST_USER,
                "n": TEST_N,
                "suffix": TEST_SUFFIX,
                "echo": TEST_ECHO,
                "error_behavior": TEST_ERROR_BEHAVIOR,
                "use_raw_prompt": TEST_USE_RAW_PROMPT,
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        Completion.create(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @pytest.mark.asyncio
    @patch('databricks_genai_inference.Completion._aget_non_streaming_response', new_callable=AsyncMock)
    async def test_completion_async_request_non_streaming(self, mocked_request):
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
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{COMPLETION_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "prompt": [COMPLETION_PROMPT_1, COMPLETION_PROMPT_2],
                "temperature": TEST_TEMPERATURE,
                "stop": TEST_STOP,
                "max_tokens": TEST_MAX_TOKENS,
                "top_p": TEST_TOP_P,
                "top_k": TEST_TOP_K,
                "user": TEST_USER,
                "n": TEST_N,
                "suffix": TEST_SUFFIX,
                "echo": TEST_ECHO,
                "error_behavior": TEST_ERROR_BEHAVIOR,
                "use_raw_prompt": TEST_USE_RAW_PROMPT,
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        await Completion.acreate(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @patch('databricks_genai_inference.Completion._get_streaming_response')
    def test_completion_request_streaming(self, mocked_request):
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
            "stream": True,
            "max_retries": TEST_MAX_RETRIES,
        }
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{COMPLETION_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "prompt": [COMPLETION_PROMPT_1, COMPLETION_PROMPT_2],
                "temperature": TEST_TEMPERATURE,
                "stop": TEST_STOP,
                "max_tokens": TEST_MAX_TOKENS,
                "top_p": TEST_TOP_P,
                "top_k": TEST_TOP_K,
                "user": TEST_USER,
                "n": TEST_N,
                "suffix": TEST_SUFFIX,
                "echo": TEST_ECHO,
                "error_behavior": TEST_ERROR_BEHAVIOR,
                "use_raw_prompt": TEST_USE_RAW_PROMPT,
                "stream": True
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        Completion.create(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @pytest.mark.asyncio
    @patch('databricks_genai_inference.Completion._aget_streaming_response', new_callable=AsyncMock)
    async def test_completion_async_request_streaming(self, mocked_request):
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
            "stream": True,
            "max_retries": TEST_MAX_RETRIES,
        }
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{COMPLETION_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "prompt": [COMPLETION_PROMPT_1, COMPLETION_PROMPT_2],
                "temperature": TEST_TEMPERATURE,
                "stop": TEST_STOP,
                "max_tokens": TEST_MAX_TOKENS,
                "top_p": TEST_TOP_P,
                "top_k": TEST_TOP_K,
                "user": TEST_USER,
                "n": TEST_N,
                "suffix": TEST_SUFFIX,
                "echo": TEST_ECHO,
                "error_behavior": TEST_ERROR_BEHAVIOR,
                "use_raw_prompt": TEST_USE_RAW_PROMPT,
                "stream": True
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        await Completion.acreate(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @patch('databricks_genai_inference.Embedding._get_non_streaming_response')
    def test_embedding_request_non_streaming(self, mocked_request):
        kwargs = {
            "model": EMBEDDING_MODEL_NAME,
            "instruction": EMBEDDING_INSTRUCTION,
            "input": [EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
            "user": TEST_USER,
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{EMBEDDING_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "input": [EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
                "instruction": EMBEDDING_INSTRUCTION,
                "user": TEST_USER,
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        Embedding.create(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)

    @pytest.mark.asyncio
    @patch('databricks_genai_inference.Embedding._aget_non_streaming_response', new_callable=AsyncMock)
    async def test_embedding_async_request_non_streaming(self, mocked_request):
        kwargs = {
            "model": EMBEDDING_MODEL_NAME,
            "instruction": EMBEDDING_INSTRUCTION,
            "input": [EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
            "user": TEST_USER,
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        expected_request = {
            "client": None,
            "url": f'{TEST_HOST_NAME}/serving-endpoints/databricks-{EMBEDDING_MODEL_NAME}/invocations',
            "headers": self._get_expected_header(TEST_API_KEY),
            "json": {
                "input": [EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
                "instruction": EMBEDDING_INSTRUCTION,
                "user": TEST_USER,
            },
            "timeout": TEST_TIMEOUT,
            "max_retries": TEST_MAX_RETRIES,
        }
        await Embedding.acreate(**kwargs)
        mocked_request.assert_called_once_with(**expected_request)
