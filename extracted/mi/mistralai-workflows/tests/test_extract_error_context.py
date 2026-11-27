import httpx
from pydantic import BaseModel, ValidationError

from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.worker_client.errors import SDKDefaultError


class TestExtractErrorContext:
    def test_base_exception_excludes_message(self) -> None:
        secret = "SYNTHETIC_SECRET"

        ctx = extract_error_context(ValueError(secret))

        assert ctx == {"error_type": "ValueError"}
        assert secret not in str(ctx)

    def test_validation_error_exposes_types_but_not_input(self) -> None:
        class Input(BaseModel):
            count: int

        secret = "SYNTHETIC_SECRET"
        try:
            Input.model_validate({"count": secret})
        except ValidationError as exc:
            ctx = extract_error_context(exc)
        else:
            raise AssertionError("Expected validation to fail")

        assert ctx == {
            "error_type": "ValidationError",
            "validation_error_count": 1,
            "validation_error_types": ["int_parsing"],
        }
        assert secret not in str(ctx)

    def test_chained_sdk_error_exposes_status_and_code_but_not_messages(self) -> None:
        secret = "SYNTHETIC_SECRET"
        response = httpx.Response(403, content=b"")
        sdk_error = SDKDefaultError(
            f"API error: {secret}",
            response,
            body=f'{{"code":"WF_1104","message":"{secret}"}}',
        )
        wrapper = RuntimeError(f"wrapped: {secret}")
        wrapper.__cause__ = sdk_error

        ctx = extract_error_context(wrapper)

        assert ctx == {
            "error_type": "RuntimeError",
            "error_chain": ["RuntimeError", "SDKDefaultError"],
            "http_status": 403,
            "api_error_code": "WF_1104",
        }
        assert secret not in str(ctx)

    def test_outermost_sdk_error_owns_http_diagnostics(self) -> None:
        inner = SDKDefaultError(
            "fallback",
            httpx.Response(500, content=b""),
            body='{"code":"WF_1500"}',
        )
        outer = SDKDefaultError(
            "registration refused",
            httpx.Response(403, content=b""),
            body='{"code":"WF_1104"}',
        )
        outer.__context__ = inner

        ctx = extract_error_context(outer)

        assert ctx == {
            "error_type": "SDKDefaultError",
            "error_chain": ["SDKDefaultError", "SDKDefaultError"],
            "http_status": 403,
            "api_error_code": "WF_1104",
        }

    def test_http_status_error_does_not_take_inner_sdk_code(self) -> None:
        request = httpx.Request("POST", "https://example.test/register")
        response = httpx.Response(403, request=request)
        outer = httpx.HTTPStatusError("registration refused", request=request, response=response)
        inner = SDKDefaultError(
            "fallback",
            httpx.Response(500, content=b""),
            body='{"code":"WF_1500"}',
        )
        outer.__context__ = inner

        ctx = extract_error_context(outer)

        assert ctx == {
            "error_type": "HTTPStatusError",
            "error_chain": ["HTTPStatusError", "SDKDefaultError"],
            "http_status": 403,
        }

    def test_non_json_sdk_error_exposes_status_but_not_body(self) -> None:
        secret = "SYNTHETIC_SECRET"
        response = httpx.Response(500, content=b"")
        sdk_error = SDKDefaultError(secret, response, body=secret)

        ctx = extract_error_context(sdk_error)

        assert ctx == {"error_type": "SDKDefaultError", "http_status": 500}
        assert secret not in str(ctx)

    def test_module_not_found_exposes_module_but_not_message(self) -> None:
        secret = "SYNTHETIC_SECRET"
        exc = ModuleNotFoundError(secret, name="workflow_dependency")

        ctx = extract_error_context(exc)

        assert ctx == {
            "error_type": "ModuleNotFoundError",
            "missing_module": "workflow_dependency",
        }
        assert secret not in str(ctx)
