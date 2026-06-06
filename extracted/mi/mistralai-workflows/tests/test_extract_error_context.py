import httpx

from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.worker_client.errors import SDKDefaultError


class TestExtractErrorContext:
    def test_base_exception(self) -> None:
        exc = ValueError("boom")
        ctx = extract_error_context(exc)
        assert ctx["error_type"] == "ValueError"
        assert ctx["error_message"] == "boom"
        assert "http_status" not in ctx
        assert "error" not in ctx

    def test_sdk_error_via_cause(self) -> None:
        mock_response = httpx.Response(403, content=b"")
        sdk_err = SDKDefaultError("API error", mock_response, body='{"code":"WF_1104","message":"Unauthorized"}')
        wrapper = RuntimeError("wrapped")
        wrapper.__cause__ = sdk_err
        ctx = extract_error_context(wrapper)
        assert ctx["error_type"] == "RuntimeError"
        assert ctx["http_status"] == 403
        assert ctx["api_error_body"] == '{"code":"WF_1104","message":"Unauthorized"}'
        assert ctx["api_error_code"] == "WF_1104"
        assert ctx["api_error_message"] == "Unauthorized"

    def test_sdk_error_non_json_body_does_not_raise(self) -> None:
        mock_response = httpx.Response(500, content=b"")
        sdk_err = SDKDefaultError("API error", mock_response, body="internal server error")
        ctx = extract_error_context(sdk_err)
        assert ctx["http_status"] == 500
        assert ctx["api_error_body"] == "internal server error"
        assert "api_error_code" not in ctx
        assert "api_error_message" not in ctx

    def test_sdk_error_via_context(self) -> None:
        mock_response = httpx.Response(500, content=b"")
        sdk_err = SDKDefaultError("API error", mock_response, body="internal")

        # Simulate implicit chaining: exception raised inside an except block
        wrapper = RuntimeError("wrapped")
        wrapper.__context__ = sdk_err
        wrapper.__suppress_context__ = False
        ctx = extract_error_context(wrapper)
        assert ctx["error_type"] == "RuntimeError"
        assert ctx["http_status"] == 500

    def test_suppressed_context_is_not_traversed(self) -> None:
        mock_response = httpx.Response(500, content=b"")
        sdk_err = SDKDefaultError("API error", mock_response, body="internal")

        # raise WrapperException() from None sets __suppress_context__ = True
        wrapper = RuntimeError("wrapped")
        wrapper.__context__ = sdk_err
        wrapper.__suppress_context__ = True
        ctx = extract_error_context(wrapper)
        assert ctx["error_type"] == "RuntimeError"
        assert "http_status" not in ctx
