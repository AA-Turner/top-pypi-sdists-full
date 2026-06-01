"""Tests for error models and SerializerMixin."""

from csrd.models.errors import APIErrorResponse, APIVersion, Error, ErrorMeta


class TestAPIVersion:
    def test_defaults(self):
        v = APIVersion()
        assert v.requested is None
        assert v.served is None

    def test_camel_case_serialization(self):
        from pydantic import TypeAdapter

        v = APIVersion(requested="2025-06-20", served="2025-06-20")
        dumped = TypeAdapter(APIVersion).dump_python(v, by_alias=True)
        assert dumped["requested"] == "2025-06-20"
        assert dumped["served"] == "2025-06-20"


class TestErrorMeta:
    def test_required_fields(self):
        meta = ErrorMeta(
            status=404,
            error="Not Found",
            path="/api/test",
            api_version=APIVersion(),
        )
        assert meta.status == 404
        assert meta.error == "Not Found"
        assert meta.timestamp is not None

    def test_optional_fields(self):
        meta = ErrorMeta(
            status=500,
            error="Internal Server Error",
            path="/api/test",
            api_version=APIVersion(),
            method="GET",
            request_id="abc-123",
        )
        assert meta.method == "GET"
        assert meta.request_id == "abc-123"


class TestError:
    def test_minimal(self):
        err = Error(title="Something went wrong")
        assert err.title == "Something went wrong"
        assert err.detail is None
        assert err.code is None

    def test_full(self):
        err = Error(title="Validation", detail="Field required", code="FIELD_REQUIRED")
        assert err.code == "FIELD_REQUIRED"


class TestAPIErrorResponse:
    def test_as_dict(self):
        resp = APIErrorResponse(
            meta=ErrorMeta(
                status=400,
                error="Bad Request",
                path="/api/test",
                api_version=APIVersion(requested="v1", served="v1"),
            ),
            errors=[Error(title="Invalid input")],
        )
        d = resp.as_dict(by_alias=True, mode="json")
        assert d["meta"]["status"] == 400
        assert d["meta"]["error"] == "Bad Request"
        assert d["meta"]["apiVersion"]["requested"] == "v1"
        assert len(d["errors"]) == 1
        assert d["errors"][0]["title"] == "Invalid input"

    def test_empty_errors(self):
        resp = APIErrorResponse(
            meta=ErrorMeta(
                status=500,
                error="Internal Server Error",
                path="/",
                api_version=APIVersion(),
            ),
            errors=[],
        )
        d = resp.as_dict(by_alias=True)
        assert d["errors"] == []
