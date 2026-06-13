"""Tests for structured JSON:API error detail surfacing in SDK exceptions."""

from __future__ import annotations

import json
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest

from smplkit.errors import (
    ApiErrorDetail,
    ConflictError,
    Error,
    NotFoundError,
    PaymentRequiredError,
    ValidationError,
    _derive_message,
    _parse_error_body,
    _raise_for_status,
)


# ---------------------------------------------------------------------------
# _parse_error_body
# ---------------------------------------------------------------------------


class TestParseErrorBody:
    def test_single_error(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'id' field is required.",
                        "source": {"pointer": "/data/id"},
                    }
                ]
            }
        ).encode()
        errors = _parse_error_body(body)
        assert len(errors) == 1
        assert errors[0].status == "400"
        assert errors[0].title == "Validation Error"
        assert errors[0].detail == "The 'id' field is required."
        assert errors[0].source == {"pointer": "/data/id"}

    def test_multiple_errors(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'name' field is required.",
                        "source": {"pointer": "/data/attributes/name"},
                    },
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'id' field is required.",
                        "source": {"pointer": "/data/id"},
                    },
                ]
            }
        ).encode()
        errors = _parse_error_body(body)
        assert len(errors) == 2

    def test_invalid_json(self):
        assert _parse_error_body(b"<html>Bad Gateway</html>") == []

    def test_empty_body(self):
        assert _parse_error_body(b"") == []

    def test_no_errors_key(self):
        assert _parse_error_body(json.dumps({"data": {}}).encode()) == []

    def test_partial_fields(self):
        body = json.dumps({"errors": [{"detail": "oops"}]}).encode()
        errors = _parse_error_body(body)
        assert len(errors) == 1
        assert errors[0].detail == "oops"
        assert errors[0].status is None
        assert errors[0].title is None
        assert errors[0].source == {}

    def test_non_dict_items_skipped(self):
        body = json.dumps({"errors": ["not-a-dict", {"detail": "real"}]}).encode()
        errors = _parse_error_body(body)
        assert len(errors) == 1
        assert errors[0].detail == "real"

    def test_extracts_code_and_meta(self):
        # Regression: ``code`` and ``meta`` were dropped by the parser,
        # so callers couldn't branch on machine-readable codes like
        # ``environment_unmanaged`` without string-matching the human
        # ``detail``. Both must round-trip.
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "400",
                        "code": "environment_unmanaged",
                        "title": "Environment is unmanaged",
                        "detail": "Promote it first.",
                        "meta": {"environment": "staging", "count": 2},
                    }
                ]
            }
        ).encode()
        errors = _parse_error_body(body)
        assert len(errors) == 1
        assert errors[0].code == "environment_unmanaged"
        assert errors[0].meta == {"environment": "staging", "count": 2}
        # to_dict should round-trip the new fields too.
        d = errors[0].to_dict()
        assert d["code"] == "environment_unmanaged"
        assert d["meta"] == {"environment": "staging", "count": 2}

    def test_ignores_non_dict_meta_and_source(self):
        # The parser must defensively coerce malformed meta/source
        # (e.g. a string where the spec expects an object) to empty
        # rather than blowing up.
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "400",
                        "title": "Bad",
                        "source": "not-an-object",
                        "meta": "also-not-an-object",
                    }
                ]
            }
        ).encode()
        errors = _parse_error_body(body)
        assert errors[0].source == {}
        assert errors[0].meta == {}


# ---------------------------------------------------------------------------
# _derive_message
# ---------------------------------------------------------------------------


class TestDeriveMessage:
    def test_empty_list(self):
        assert _derive_message([]) == "An API error occurred"

    def test_detail_first(self):
        err = ApiErrorDetail(status="400", title="Bad Request", detail="Name is required.")
        assert _derive_message([err]) == "Name is required."

    def test_title_fallback(self):
        err = ApiErrorDetail(status="400", title="Bad Request")
        assert _derive_message([err]) == "Bad Request"

    def test_status_fallback(self):
        err = ApiErrorDetail(status="400")
        assert _derive_message([err]) == "400"

    def test_all_empty(self):
        err = ApiErrorDetail()
        assert _derive_message([err]) == "An API error occurred"

    def test_multiple_errors_suffix(self):
        errs = [ApiErrorDetail(detail="first"), ApiErrorDetail(detail="second")]
        assert _derive_message(errs) == "first (and 1 more error)"

    def test_three_errors_suffix(self):
        errs = [
            ApiErrorDetail(detail="a"),
            ApiErrorDetail(detail="b"),
            ApiErrorDetail(detail="c"),
        ]
        assert _derive_message(errs) == "a (and 2 more errors)"


# ---------------------------------------------------------------------------
# Error enhanced constructor and __str__
# ---------------------------------------------------------------------------


class TestSmplErrorStr:
    def test_single_error_str(self):
        err = ValidationError(
            "The 'id' field is required.",
            errors=[
                ApiErrorDetail(
                    status="400",
                    title="Validation Error",
                    detail="The 'id' field is required.",
                    source={"pointer": "/data/id"},
                )
            ],
            status_code=400,
        )
        s = str(err)
        assert "The 'id' field is required." in s
        assert "Error:" in s
        assert '"/data/id"' in s

    def test_multi_error_str(self):
        err = ValidationError(
            "The 'name' field is required. (and 1 more error)",
            errors=[
                ApiErrorDetail(
                    status="400",
                    title="Validation Error",
                    detail="The 'name' field is required.",
                    source={"pointer": "/data/attributes/name"},
                ),
                ApiErrorDetail(
                    status="400",
                    title="Validation Error",
                    detail="The 'id' field is required.",
                    source={"pointer": "/data/id"},
                ),
            ],
            status_code=400,
        )
        s = str(err)
        assert "Errors:" in s
        assert "[0]" in s
        assert "[1]" in s
        assert "The 'name' field is required." in s
        assert "The 'id' field is required." in s

    def test_no_errors_str(self):
        err = Error("plain message")
        assert str(err) == "plain message"
        assert err.errors == []
        assert err.status_code is None

    def test_backwards_compat_positional_message(self):
        err = NotFoundError("Config abc not found")
        assert str(err) == "Config abc not found"
        assert err.errors == []

    def test_message_derived_when_none(self):
        err = Error(errors=[ApiErrorDetail(detail="auto-derived")])
        assert "auto-derived" in str(err)


# ---------------------------------------------------------------------------
# _raise_for_status
# ---------------------------------------------------------------------------


class TestRaiseForStatus:
    def test_2xx_no_raise(self):
        _raise_for_status(200, b"")
        _raise_for_status(201, b"")
        _raise_for_status(204, b"")

    def test_400_validation_error(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'id' field is required.",
                        "source": {"pointer": "/data/id"},
                    }
                ]
            }
        ).encode()
        with pytest.raises(ValidationError) as exc_info:
            _raise_for_status(400, body)
        exc = exc_info.value
        assert exc.status_code == 400
        assert len(exc.errors) == 1
        assert exc.errors[0].detail == "The 'id' field is required."
        assert exc.errors[0].source == {"pointer": "/data/id"}
        assert "The 'id' field is required." in str(exc)
        assert '"/data/id"' in str(exc)

    def test_400_multi_error(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'name' field is required.",
                        "source": {"pointer": "/data/attributes/name"},
                    },
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'id' field is required.",
                        "source": {"pointer": "/data/id"},
                    },
                ]
            }
        ).encode()
        with pytest.raises(ValidationError) as exc_info:
            _raise_for_status(400, body)
        exc = exc_info.value
        assert "(and 1 more error)" in str(exc)
        assert len(exc.errors) == 2
        assert "Errors:" in str(exc)
        assert "[0]" in str(exc)
        assert "[1]" in str(exc)

    def test_402_payment_required(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "402",
                        "title": "Payment Required",
                        "detail": "Plan does not include this capability.",
                    }
                ]
            }
        ).encode()
        with pytest.raises(PaymentRequiredError) as exc_info:
            _raise_for_status(402, body)
        exc = exc_info.value
        assert exc.status_code == 402
        assert "Plan does not include this capability." in str(exc)

    def test_404_not_found(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "404",
                        "title": "Not Found",
                        "detail": "Config 'abc' does not exist.",
                    }
                ]
            }
        ).encode()
        with pytest.raises(NotFoundError) as exc_info:
            _raise_for_status(404, body)
        exc = exc_info.value
        assert exc.status_code == 404
        assert "Config 'abc' does not exist." in str(exc)

    def test_409_conflict(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "409",
                        "title": "Conflict",
                        "detail": "Config has children and cannot be deleted.",
                    }
                ]
            }
        ).encode()
        with pytest.raises(ConflictError) as exc_info:
            _raise_for_status(409, body)
        exc = exc_info.value
        assert exc.status_code == 409
        assert "Config has children" in str(exc)

    def test_422_validation(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "422",
                        "title": "Unprocessable Entity",
                        "detail": "Invalid key format.",
                    }
                ]
            }
        ).encode()
        with pytest.raises(ValidationError) as exc_info:
            _raise_for_status(422, body)
        assert exc_info.value.status_code == 422

    def test_500_server_error(self):
        body = json.dumps(
            {
                "errors": [
                    {
                        "status": "500",
                        "title": "Internal Server Error",
                        "detail": "Something went wrong.",
                    }
                ]
            }
        ).encode()
        with pytest.raises(Error) as exc_info:
            _raise_for_status(500, body)
        exc = exc_info.value
        assert exc.status_code == 500
        assert "Something went wrong." in str(exc)

    def test_non_json_response(self):
        with pytest.raises(Error) as exc_info:
            _raise_for_status(502, b"<html>Bad Gateway</html>")
        exc = exc_info.value
        assert exc.status_code == 502
        assert "HTTP 502" in str(exc)
        assert exc.errors == []

    def test_empty_body(self):
        with pytest.raises(Error) as exc_info:
            _raise_for_status(502, b"")
        assert exc_info.value.status_code == 502
        assert exc_info.value.errors == []


# ---------------------------------------------------------------------------
# Integration: wrapper method raises structured errors
# ---------------------------------------------------------------------------


def _make_error_response(status_code: int, errors_body: dict) -> MagicMock:
    """Build a mock response matching the generated client's Response pattern."""
    resp = MagicMock()
    resp.status_code = HTTPStatus(status_code)
    resp.content = json.dumps(errors_body).encode()
    resp.parsed = None
    return resp


class TestConfigClientErrors:
    @patch("smplkit.config.clients.update_config.sync_detailed")
    def test_update_config_400_surfaces_detail(self, mock_update):
        mock_update.return_value = _make_error_response(
            400,
            {
                "errors": [
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'id' field is required.",
                        "source": {"pointer": "/data/id"},
                    }
                ]
            },
        )
        from smplkit.config.models import Config

        import datetime

        from smplkit import SmplClient

        config = SmplClient(api_key="sk_test", base_domain="example.test").config
        cfg = Config(
            config,
            id="test",
            name="test",
            created_at=datetime.datetime(2025, 1, 1),
        )
        with pytest.raises(ValidationError) as exc_info:
            cfg.save()
        exc = exc_info.value
        assert exc.status_code == 400
        assert "The 'id' field is required." in str(exc)
        assert len(exc.errors) == 1
        assert exc.errors[0].source == {"pointer": "/data/id"}

    @patch("smplkit.config.clients.create_config.sync_detailed")
    def test_create_config_multi_error(self, mock_create):
        mock_create.return_value = _make_error_response(
            400,
            {
                "errors": [
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'name' field is required.",
                        "source": {"pointer": "/data/attributes/name"},
                    },
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'id' field is required.",
                        "source": {"pointer": "/data/id"},
                    },
                ]
            },
        )

        from smplkit import SmplClient

        config = SmplClient(api_key="sk_test", base_domain="example.test").config
        cfg = config.new("test-key", name="test")
        with pytest.raises(ValidationError) as exc_info:
            cfg.save()
        exc = exc_info.value
        assert len(exc.errors) == 2
        assert "(and 1 more error)" in str(exc)

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_get_config_404_surfaces_detail(self, mock_get):
        mock_get.return_value = _make_error_response(
            404,
            {
                "errors": [
                    {
                        "status": "404",
                        "title": "Not Found",
                        "detail": "Config 'abc' does not exist.",
                    }
                ]
            },
        )

        from smplkit import SmplClient

        config = SmplClient(api_key="sk_test", base_domain="example.test").config
        with pytest.raises(NotFoundError) as exc_info:
            config.get("abc")
        exc = exc_info.value
        assert exc.status_code == 404
        assert "Config 'abc' does not exist." in str(exc)

    @patch("smplkit.config.clients.delete_config.sync_detailed")
    def test_delete_config_409_surfaces_detail(self, mock_delete):
        mock_delete.return_value = _make_error_response(
            409,
            {
                "errors": [
                    {
                        "status": "409",
                        "title": "Conflict",
                        "detail": "Config has children and cannot be deleted.",
                    }
                ]
            },
        )

        from smplkit import SmplClient

        config = SmplClient(api_key="sk_test", base_domain="example.test").config
        with pytest.raises(ConflictError) as exc_info:
            config.delete("test-config")
        exc = exc_info.value
        assert exc.status_code == 409
        assert "Config has children" in str(exc)

    @patch("smplkit.config.clients.create_config.sync_detailed")
    def test_non_json_error_response(self, mock_create):
        resp = MagicMock()
        resp.status_code = HTTPStatus(502)
        resp.content = b"<html>Bad Gateway</html>"
        resp.parsed = None
        mock_create.return_value = resp

        from smplkit import SmplClient

        config = SmplClient(api_key="sk_test", base_domain="example.test").config
        cfg = config.new("test-key", name="test")
        with pytest.raises(Error) as exc_info:
            cfg.save()
        exc = exc_info.value
        assert exc.status_code == 502
        assert "HTTP 502" in str(exc)
        assert exc.errors == []


class TestFlagsClientErrors:
    @patch("smplkit.flags.clients.create_flag.sync_detailed")
    def test_create_flag_400_surfaces_detail(self, mock_create):
        mock_create.return_value = _make_error_response(
            400,
            {
                "errors": [
                    {
                        "status": "400",
                        "title": "Validation Error",
                        "detail": "The 'id' field is required.",
                        "source": {"pointer": "/data/attributes/id"},
                    }
                ]
            },
        )
        from smplkit.flags.models import Flag

        from smplkit import SmplClient

        client = SmplClient(api_key="sk_test", base_domain="example.test")
        flag = Flag(
            client.flags,
            id="test",
            name="Test",
            type="boolean",
            default=True,
        )
        with pytest.raises(ValidationError) as exc_info:
            flag.save()
        exc = exc_info.value
        assert exc.status_code == 400
        assert "The 'id' field is required." in str(exc)

    @patch("smplkit.flags.clients.get_flag.sync_detailed")
    def test_get_flag_404_surfaces_detail(self, mock_get):
        mock_get.return_value = _make_error_response(
            404,
            {
                "errors": [
                    {
                        "status": "404",
                        "title": "Not Found",
                        "detail": "Flag does not exist.",
                    }
                ]
            },
        )

        from smplkit import SmplClient

        client = SmplClient(api_key="sk_test", base_domain="example.test")
        with pytest.raises(NotFoundError) as exc_info:
            client.flags.get("test-flag")
        exc = exc_info.value
        assert exc.status_code == 404
        assert "Flag does not exist." in str(exc)


class TestLoggingClientErrors:
    @patch("smplkit.logging.clients.update_logger.sync_detailed")
    def test_save_new_logger_upserts_via_put(self, mock_update):
        from smplkit.errors import ConnectionError
        import httpx

        # Simulate PUT failing with a network error to verify a single
        # HTTP call is made (upsert — no bulk pre-step).
        mock_update.side_effect = httpx.ConnectError("refused")
        from smplkit import SmplClient

        mgmt = SmplClient(api_key="sk_test", base_domain="example.test").logging
        lg = mgmt.loggers.new("test-key")
        with pytest.raises(ConnectionError):
            lg.save()
        mock_update.assert_called_once()

    @patch("smplkit.logging.clients.get_logger.sync_detailed")
    def test_get_logger_404_surfaces_detail(self, mock_get):
        mock_get.return_value = _make_error_response(
            404,
            {
                "errors": [
                    {
                        "status": "404",
                        "title": "Not Found",
                        "detail": "Logger does not exist.",
                    }
                ]
            },
        )

        from smplkit import SmplClient

        mgmt = SmplClient(api_key="sk_test", base_domain="example.test").logging
        with pytest.raises(NotFoundError) as exc_info:
            mgmt.loggers.get("test-key")
        exc = exc_info.value
        assert exc.status_code == 404
        assert "Logger does not exist." in str(exc)


class TestApiErrorDetailSerialization:
    def test_to_dict_full(self):
        err = ApiErrorDetail(
            status="400",
            title="Validation Error",
            detail="Bad field.",
            source={"pointer": "/data/id"},
        )
        d = err.to_dict()
        assert d == {
            "status": "400",
            "title": "Validation Error",
            "detail": "Bad field.",
            "source": {"pointer": "/data/id"},
        }

    def test_to_dict_minimal(self):
        err = ApiErrorDetail(detail="oops")
        d = err.to_dict()
        assert d == {"detail": "oops"}

    def test_to_json(self):
        err = ApiErrorDetail(status="400", detail="oops")
        j = err.to_json()
        parsed = json.loads(j)
        assert parsed["status"] == "400"
        assert parsed["detail"] == "oops"
