"""Tests for CallLogger."""

import logging

from agentic_devtools.orchestration.llm.call_logger import CallLogger, LogLevel, log_llm_call
from agentic_devtools.orchestration.llm.types import LLMMessage, LLMResponse, ProviderType, TokenUsage


class TestCallLogger:
    """Tests for CallLogger."""

    def test_none_level_does_not_log(self, caplog):
        logger = CallLogger(level=LogLevel.NONE)
        logger.log_call(model="gpt-4o", node_type="test")
        assert len(caplog.records) == 0

    def test_level_property(self):
        logger = CallLogger(level=LogLevel.VERBOSE)
        assert logger.level == LogLevel.VERBOSE

    def test_minimal_level_logs_basic_info(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.MINIMAL)
            response = LLMResponse(
                text="Hello",
                model="gpt-4o",
                provider_type=ProviderType.AZURE_OPENAI,
                usage=TokenUsage(input_tokens=10, output_tokens=5, total_tokens=15),
                latency_ms=100,
            )
            logger.log_call(model="gpt-4o", node_type="analysis", response=response, latency_ms=100)
        assert len(caplog.records) == 1
        assert "gpt-4o" in caplog.records[0].message

    def test_minimal_level_with_cost(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.MINIMAL)
            response = LLMResponse(
                text="Hello",
                model="gpt-4o",
                provider_type=ProviderType.AZURE_OPENAI,
                usage=TokenUsage(input_tokens=10, output_tokens=5, total_tokens=15, estimated_cost_usd=0.001),
            )
            logger.log_call(model="gpt-4o", response=response)
        assert len(caplog.records) == 1
        assert "cost_usd" in caplog.records[0].message

    def test_standard_level_includes_prompt_preview(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            messages = [LLMMessage(role="user", content="Tell me about Python programming language")]
            logger.log_call(model="gpt-4o", messages=messages)
        assert len(caplog.records) == 1
        assert "Tell me about" in caplog.records[0].message

    def test_standard_level_skips_system_message_for_preview(self, caplog):
        """STANDARD level must preview the first non-system message, not the system message."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            messages = [
                LLMMessage(role="system", content="You are a helpful assistant with internal instructions"),
                LLMMessage(role="user", content="Summarise this document"),
            ]
            logger.log_call(model="gpt-4o", messages=messages)
        assert len(caplog.records) == 1
        assert "Summarise this document" in caplog.records[0].message
        assert "internal instructions" not in caplog.records[0].message

    def test_standard_level_skips_system_message_case_insensitively(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            messages = [
                LLMMessage(role="SYSTEM", content="Internal instructions"),
                LLMMessage(role="user", content="Visible prompt"),
            ]
            logger.log_call(model="gpt-4o", messages=messages)
        assert len(caplog.records) == 1
        assert "Visible prompt" in caplog.records[0].message
        assert "Internal instructions" not in caplog.records[0].message

    def test_standard_level_omits_preview_when_all_system(self, caplog):
        """When all messages are system role, preview must be omitted to avoid prompt leakage."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            messages = [
                LLMMessage(role="system", content="Only system message here"),
            ]
            logger.log_call(model="gpt-4o", messages=messages)
        assert len(caplog.records) == 1
        assert "Only system message here" not in caplog.records[0].message
        assert "prompt_preview" not in caplog.records[0].message

    def test_error_logs_at_warning_level(self, caplog):
        with caplog.at_level(logging.WARNING, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.MINIMAL)
            logger.log_call(model="gpt-4o", error=Exception("API error"))
        assert len(caplog.records) == 1
        assert caplog.records[0].levelname == "WARNING"

    def test_verbose_includes_full_content(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.VERBOSE)
            messages = [LLMMessage(role="user", content="Full content here")]
            response = LLMResponse(text="Full response", model="gpt-4o", provider_type=ProviderType.AZURE_OPENAI)
            logger.log_call(model="gpt-4o", messages=messages, response=response)
        assert "Full content here" in caplog.records[0].message

    def test_verbose_without_response(self, caplog):
        """Verbose level with messages but no response covers the falsy-response branch."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.VERBOSE)
            messages = [LLMMessage(role="user", content="Only messages")]
            logger.log_call(model="gpt-4o", messages=messages)
        assert "Only messages" in caplog.records[0].message
        assert "response_text" not in caplog.records[0].message

    def test_verbose_without_messages(self, caplog):
        """Verbose level without messages covers the falsy-messages branch."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.VERBOSE)
            response = LLMResponse(text="Resp", model="gpt-4o", provider_type=ProviderType.AZURE_OPENAI)
            logger.log_call(model="gpt-4o", response=response)
        assert "response_text" in caplog.records[0].message


class TestLogLlmCall:
    """Tests for log_llm_call convenience function."""

    def test_logs_without_error(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            log_llm_call(model="gpt-4o", level=LogLevel.MINIMAL)
        assert len(caplog.records) == 1


class TestCallLoggerBestEffort:
    """Tests that log_call never raises due to unexpected message shapes."""

    def test_dict_messages_do_not_raise_at_standard_level(self, caplog):
        """Dict-form messages (not LLMMessage objects) must not cause log_call to raise."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            dict_messages = [{"role": "user", "content": "Hello"}]
            logger.log_call(model="gpt-4o", messages=dict_messages)
        # Must not raise; a log record should still be produced
        assert len(caplog.records) == 1
        assert "Hello" in caplog.records[0].message

    def test_dict_messages_skip_system_for_preview(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            dict_messages = [
                {"role": "system", "content": "Internal instructions"},
                {"role": "user", "content": "Visible prompt"},
            ]
            logger.log_call(model="gpt-4o", messages=dict_messages)
        assert len(caplog.records) == 1
        assert "Visible prompt" in caplog.records[0].message
        assert "Internal instructions" not in caplog.records[0].message

    def test_dict_messages_all_system_omits_preview(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            dict_messages = [{"role": "system", "content": "Internal instructions"}]
            logger.log_call(model="gpt-4o", messages=dict_messages)
        assert len(caplog.records) == 1
        assert "Internal instructions" not in caplog.records[0].message
        assert "prompt_preview" not in caplog.records[0].message

    def test_dict_messages_preview_truncates_long_content(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            long_content = "x" * 120
            logger.log_call(model="gpt-4o", messages=[{"role": "user", "content": long_content}])
        assert len(caplog.records) == 1
        assert ("x" * 100 + "...") in caplog.records[0].message

    def test_nonstring_content_does_not_raise_at_standard_level(self, caplog):
        """Non-string content (e.g. integer) triggers TypeError on slicing; must be silently swallowed."""

        class BadMessage:
            role = "user"
            content = 42  # int is not subscriptable → TypeError on [:100]

        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            logger.log_call(model="gpt-4o", messages=[BadMessage()])
        # Must not raise; a log record should still be produced
        assert len(caplog.records) == 1

    def test_nonstring_role_omits_preview(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            logger.log_call(model="gpt-4o", messages=[{"role": object(), "content": "Internal instructions"}])
        assert len(caplog.records) == 1
        assert "Internal instructions" not in caplog.records[0].message
        assert "prompt_preview" not in caplog.records[0].message

    def test_empty_messages_list_does_not_raise_at_standard_level(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.STANDARD)
            logger.log_call(model="gpt-4o", messages=[])
        assert len(caplog.records) == 1
        assert "prompt_preview" not in caplog.records[0].message

    def test_dict_messages_do_not_raise_at_verbose_level(self, caplog):
        """Dict-form messages at VERBOSE level must not cause log_call to raise."""
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.VERBOSE)
            dict_messages = [{"role": "user", "content": "Hello"}]
            logger.log_call(model="gpt-4o", messages=dict_messages)
        assert len(caplog.records) == 1

    def test_verbose_message_serialization_errors_are_swallowed(self, caplog):
        class BadVerboseMessage:
            role = "user"

            @property
            def content(self):
                raise TypeError("not serializable")

        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.VERBOSE)
            logger.log_call(model="gpt-4o", messages=[BadVerboseMessage()])
        assert len(caplog.records) == 1

    def test_verbose_handles_none_fields_in_message(self, caplog):
        with caplog.at_level(logging.INFO, logger="agentic_devtools.orchestration.llm"):
            logger = CallLogger(level=LogLevel.VERBOSE)
            logger.log_call(model="gpt-4o", messages=[{"role": None, "content": None}])
        assert len(caplog.records) == 1
