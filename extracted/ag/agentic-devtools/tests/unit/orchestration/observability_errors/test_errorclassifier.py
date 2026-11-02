"""Tests for ErrorClassifier."""

import errno

from agentic_devtools.orchestration.observability_errors import ErrorClassifier


class TestErrorClassifier:
    """Tests for ErrorClassifier.classify()."""

    def setup_method(self) -> None:
        self.classifier = ErrorClassifier()

    # --- Transient errors ---

    def test_connection_error_is_transient(self) -> None:
        result = self.classifier.classify(ConnectionError("Connection refused"))
        assert result.error_class == "transient"
        assert result.retryable is True

    def test_timeout_error_is_transient(self) -> None:
        result = self.classifier.classify(TimeoutError("Timed out"))
        assert result.error_class == "transient"
        assert result.retryable is True

    def test_http_429_is_transient(self) -> None:
        result = self.classifier.classify(RuntimeError("Rate limited"), context={"status_code": 429})
        assert result.error_class == "transient"
        assert result.retryable is True

    def test_http_500_is_transient(self) -> None:
        result = self.classifier.classify(RuntimeError("Server error"), context={"status_code": 500})
        assert result.error_class == "transient"
        assert result.retryable is True

    def test_http_503_is_transient(self) -> None:
        result = self.classifier.classify(RuntimeError("Unavailable"), context={"status_code": 503})
        assert result.error_class == "transient"
        assert result.retryable is True

    # --- Permanent errors ---

    def test_http_401_is_permanent(self) -> None:
        result = self.classifier.classify(RuntimeError("Unauthorized"), context={"status_code": 401})
        assert result.error_class == "permanent"
        assert result.retryable is False

    def test_http_403_is_permanent(self) -> None:
        result = self.classifier.classify(RuntimeError("Forbidden"), context={"status_code": 403})
        assert result.error_class == "permanent"
        assert result.retryable is False

    def test_http_400_is_permanent(self) -> None:
        result = self.classifier.classify(RuntimeError("Bad request"), context={"status_code": 400})
        assert result.error_class == "permanent"
        assert result.retryable is False

    def test_value_error_is_permanent(self) -> None:
        result = self.classifier.classify(ValueError("Invalid input"))
        assert result.error_class == "permanent"
        assert result.retryable is False

    def test_key_error_is_permanent(self) -> None:
        result = self.classifier.classify(KeyError("missing_key"))
        assert result.error_class == "permanent"
        assert result.retryable is False

    def test_unmapped_exception_defaults_to_permanent(self) -> None:
        result = self.classifier.classify(RuntimeError("Unknown issue"))
        assert result.error_class == "permanent"
        assert result.retryable is False

    # --- LLM errors ---

    def test_llm_context_validation_failure(self) -> None:
        result = self.classifier.classify(
            ValueError("Output validation failed"),
            context={"source": "llm"},
        )
        assert result.error_class == "llm"
        assert result.retryable is True

    def test_llm_context_model_refusal(self) -> None:
        result = self.classifier.classify(
            RuntimeError("Model refused to respond"),
            context={"source": "llm"},
        )
        assert result.error_class == "llm"
        assert result.retryable is True

    def test_llm_context_transient_still_transient(self) -> None:
        """Transient errors within LLM context are still classified transient."""
        result = self.classifier.classify(
            ConnectionError("Network failure"),
            context={"source": "llm"},
        )
        assert result.error_class == "transient"
        assert result.retryable is True

    def test_llm_context_http_401_is_llm_non_retryable(self) -> None:
        result = self.classifier.classify(
            RuntimeError("Unauthorized"),
            context={"source": "llm", "status_code": 401},
        )
        assert result.error_class == "llm"
        assert result.retryable is False

    # --- Tool errors ---

    def test_tool_context_api_failure(self) -> None:
        result = self.classifier.classify(
            RuntimeError("API returned error"),
            context={"source": "tool"},
        )
        assert result.error_class == "tool"
        assert result.retryable is True

    def test_tool_context_timeout(self) -> None:
        """TimeoutError in tool context is still transient."""
        result = self.classifier.classify(
            TimeoutError("Tool timed out"),
            context={"source": "tool"},
        )
        assert result.error_class == "transient"
        assert result.retryable is True

    def test_tool_context_generic_error(self) -> None:
        result = self.classifier.classify(
            ValueError("Bad tool input"),
            context={"source": "tool"},
        )
        assert result.error_class == "tool"
        assert result.retryable is True

    def test_tool_context_http_403_is_tool_non_retryable(self) -> None:
        result = self.classifier.classify(
            RuntimeError("Forbidden"),
            context={"source": "tool", "status_code": 403},
        )
        assert result.error_class == "tool"
        assert result.retryable is False

    # --- Default fallback ---

    def test_default_fallback_no_context(self) -> None:
        """Exception without context defaults to permanent."""
        result = self.classifier.classify(Exception("Something went wrong"))
        assert result.error_class == "permanent"
        assert result.retryable is False

    def test_classification_message_contains_exception_info(self) -> None:
        result = self.classifier.classify(ValueError("Bad value"))
        assert "ValueError" in result.message
        assert "Bad value" in result.message

    def test_os_error_with_network_errno_is_transient(self) -> None:
        """OSError with a network errno that is not auto-promoted is classified as transient.

        Python 3.3+ auto-promotes certain OSError codes to ConnectionError/TimeoutError
        subclasses (ECONNRESET → ConnectionResetError, ETIMEDOUT → TimeoutError, etc.),
        which are caught by the first isinstance check before reaching the errno branch.
        ENETUNREACH and EHOSTUNREACH are *not* auto-promoted, so they exercise the
        plain-OSError + errno path.
        """
        err = OSError(errno.ENETUNREACH, "Network unreachable")
        result = self.classifier.classify(err)
        assert result.error_class == "transient"
        assert result.retryable is True

    def test_os_error_with_no_errno_is_not_transient(self) -> None:
        """OSError with no errno (e.g. a path that contains 'connection') is NOT transient.

        This guards against substring-matching false positives such as
        FileNotFoundError('connection.txt').
        """
        err = OSError("connection.txt not found")
        result = self.classifier.classify(err)
        assert result.error_class == "permanent"
        assert result.retryable is False

    def test_file_not_found_with_connection_in_path_is_not_transient(self) -> None:
        """FileNotFoundError whose path contains 'connection' is NOT a network error."""
        err = FileNotFoundError("No such file or directory: 'connection.txt'")
        result = self.classifier.classify(err)
        assert result.error_class == "permanent"
        assert result.retryable is False
