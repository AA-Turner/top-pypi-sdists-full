from unittest.mock import patch

import pytest
from constants import (CHAT_COMPLETION_MESSAGES, CHAT_COMPLETION_MODEL_NAME, COMPLETION_MODEL_NAME, COMPLETION_PROMPT_1,
                       COMPLETION_PROMPT_2, EMBEDDING_INPUT_1, EMBEDDING_INPUT_2, EMBEDDING_INSTRUCTION,
                       EMBEDDING_MODEL_NAME, FAKE_ARG_VALUE, TEST_ECHO, TEST_ERROR_BEHAVIOR, TEST_MAX_TOKENS, TEST_N,
                       TEST_STOP, TEST_SUFFIX, TEST_TEMPERATURE, TEST_TIMEOUT, TEST_TOP_K, TEST_TOP_P,
                       TEST_USE_RAW_PROMPT, TEST_USER)

from databricks_genai_inference import ChatCompletion, Completion, Embedding
from databricks_genai_inference.api.chat_completion import ChatCompletionAPIInput
from databricks_genai_inference.api.completion import CompletionAPIInput
from databricks_genai_inference.api.embedding import EmbeddingAPIInput
from databricks_genai_inference.api.exception import FoundationModelAPIException


class TestInputValidation:

    @patch('databricks_genai_inference.ChatCompletion._make_query')
    def test_chat_completion_correct_input(self, mocked_request):
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
        }
        expected_model_input = ChatCompletionAPIInput(
            model=CHAT_COMPLETION_MODEL_NAME,
            messages=CHAT_COMPLETION_MESSAGES,
            temperature=TEST_TEMPERATURE,
            stop=TEST_STOP,
            max_tokens=TEST_MAX_TOKENS,
            top_p=TEST_TOP_P,
            top_k=TEST_TOP_K,
            user=TEST_USER,
            timeout=TEST_TIMEOUT,
            n=TEST_N,
        )
        ChatCompletion.create(**kwargs)
        mocked_request.assert_called_once_with(None, expected_model_input, f"databricks-{CHAT_COMPLETION_MODEL_NAME}")

    @patch('databricks_genai_inference.ChatCompletion._make_query')
    def test_chat_completion_correct_input_required(self, mocked_request):
        kwargs = {
            "model": CHAT_COMPLETION_MODEL_NAME,
            "messages": CHAT_COMPLETION_MESSAGES,
        }
        expected_model_input = ChatCompletionAPIInput(
            model=CHAT_COMPLETION_MODEL_NAME,
            messages=CHAT_COMPLETION_MESSAGES,
        )
        ChatCompletion.create(**kwargs)
        mocked_request.assert_called_once_with(None, expected_model_input, f"databricks-{CHAT_COMPLETION_MODEL_NAME}")

    @patch('databricks_genai_inference.ChatCompletion._make_query')
    def test_chat_completion_custom_endpoint(self, mocked_request):
        CUSTOM_MODEL_NAME = "finetuned-dbrx-instruct"
        kwargs = {
            "model": CUSTOM_MODEL_NAME,
            "messages": CHAT_COMPLETION_MESSAGES,
        }
        expected_model_input = ChatCompletionAPIInput(
            model=CUSTOM_MODEL_NAME,
            messages=CHAT_COMPLETION_MESSAGES,
        )
        ChatCompletion.create(**kwargs)
        mocked_request.assert_called_once_with(None, expected_model_input, CUSTOM_MODEL_NAME)

    @patch('databricks_genai_inference.ChatCompletion._make_query')
    def test_chat_completion_wrong_input(self, mocked_request):
        with pytest.raises(FoundationModelAPIException) as error:
            ChatCompletion.create(messages=CHAT_COMPLETION_MESSAGES)
        assert "validation error" in str(error.value), "missing model name should raise validation error"

        with pytest.raises(FoundationModelAPIException) as error:
            ChatCompletion.create(FAKE_ARG_NAME=FAKE_ARG_VALUE)
        assert "validation error" in str(error.value), "unrecognized should raise validation error"

    @patch('databricks_genai_inference.Completion._make_query')
    def test_completion_correct_input(self, mocked_request):
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
        }
        expected_model_input = CompletionAPIInput(
            model=COMPLETION_MODEL_NAME,
            prompt=[COMPLETION_PROMPT_1, COMPLETION_PROMPT_2],
            temperature=TEST_TEMPERATURE,
            stop=TEST_STOP,
            max_tokens=TEST_MAX_TOKENS,
            top_p=TEST_TOP_P,
            top_k=TEST_TOP_K,
            user=TEST_USER,
            timeout=TEST_TIMEOUT,
            n=TEST_N,
            suffix=TEST_SUFFIX,
            echo=TEST_ECHO,
            error_behavior=TEST_ERROR_BEHAVIOR,
            use_raw_prompt=TEST_USE_RAW_PROMPT,
        )
        Completion.create(**kwargs)
        mocked_request.assert_called_once_with(None, expected_model_input, f"databricks-{COMPLETION_MODEL_NAME}")

    @patch('databricks_genai_inference.Completion._make_query')
    def test_completion_correct_input_required(self, mocked_request):
        kwargs = {
            "model": COMPLETION_MODEL_NAME,
            "prompt": [COMPLETION_PROMPT_1, COMPLETION_PROMPT_2],
        }
        expected_model_input = CompletionAPIInput(
            model=COMPLETION_MODEL_NAME,
            prompt=[COMPLETION_PROMPT_1, COMPLETION_PROMPT_2],
        )
        Completion.create(**kwargs)
        mocked_request.assert_called_once_with(None, expected_model_input, f"databricks-{COMPLETION_MODEL_NAME}")

    @patch('databricks_genai_inference.Completion._make_query')
    def test_completion_wrong_input(self, mocked_request):
        with pytest.raises(FoundationModelAPIException) as error:
            Completion.create(prompt=[COMPLETION_PROMPT_1, COMPLETION_PROMPT_2])
        assert "validation error" in str(error.value), "missing model name should raise validation error"

        with pytest.raises(FoundationModelAPIException) as error:
            Completion.create(FAKE_ARG_NAME=FAKE_ARG_VALUE)
        assert "validation error" in str(error.value), "unrecognized should raise validation error"

    @patch('databricks_genai_inference.Embedding._make_query')
    def test_embedding_correct_input(self, mocked_request):
        kwargs = {
            "model": EMBEDDING_MODEL_NAME,
            "instruction": EMBEDDING_INSTRUCTION,
            "input": [EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
            "user": TEST_USER,
            "timeout": TEST_TIMEOUT,
        }
        expected_model_input = EmbeddingAPIInput(
            model=EMBEDDING_MODEL_NAME,
            instruction=EMBEDDING_INSTRUCTION,
            input=[EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
            user=TEST_USER,
            timeout=TEST_TIMEOUT,
        )
        Embedding.create(**kwargs)
        mocked_request.assert_called_once_with(None, expected_model_input, f"databricks-{EMBEDDING_MODEL_NAME}")

    @patch('databricks_genai_inference.Embedding._make_query')
    def test_embedding_correct_input_required(self, mocked_request):
        kwargs = {
            "model": EMBEDDING_MODEL_NAME,
            "input": [EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
        }
        expected_model_input = EmbeddingAPIInput(
            model=EMBEDDING_MODEL_NAME,
            input=[EMBEDDING_INPUT_1, EMBEDDING_INPUT_2],
        )
        Embedding.create(**kwargs)
        mocked_request.assert_called_once_with(None, expected_model_input, f"databricks-{EMBEDDING_MODEL_NAME}")

    @patch('databricks_genai_inference.Embedding._make_query')
    def test_embedding_wrong_input(self, mocked_request):
        with pytest.raises(FoundationModelAPIException) as error:
            Embedding.create(input=[EMBEDDING_INPUT_1, EMBEDDING_INPUT_2])
        assert "validation error" in str(error.value), "missing model name should raise validation error"

        with pytest.raises(FoundationModelAPIException) as error:
            Embedding.create(FAKE_ARG_NAME=FAKE_ARG_VALUE)
        assert "validation error" in str(error.value), "unrecognized should raise validation error"

        with pytest.raises(FoundationModelAPIException) as error:
            Embedding.create(model=EMBEDDING_MODEL_NAME, input=EMBEDDING_INPUT_1, stream=True)
        assert "validation error" in str(error.value), "embedding model does not support streaming"
