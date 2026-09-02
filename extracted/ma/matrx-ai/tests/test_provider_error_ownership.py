from __future__ import annotations

from pathlib import Path

import httpx

from matrx_ai.catalog.errors import CatalogRoutingError
from matrx_ai.providers.errors import (
    classify_anthropic_error,
    classify_google_error,
    classify_provider_error,
)


def test_empty_httpx_read_error_keeps_typed_transport_classification() -> None:
    error = httpx.ReadError("")

    for classified in (
        classify_anthropic_error(error),
        classify_google_error(error),
        classify_provider_error("anthropic", error),
    ):
        assert classified.error_type == "connection_error"
        assert classified.message == "ReadError"
        assert classified.is_retryable is True
        assert classified.details["transport_exception"] == "httpx.ReadError"


def test_internal_defect_type_is_consistent_across_entry_points() -> None:
    error = AttributeError("missing emitter method")

    assert classify_anthropic_error(error).error_type == "matrx_internal_error"
    assert classify_provider_error("anthropic", error).error_type == "matrx_internal_error"
    assert classify_provider_error("unknown", error).is_retryable is False


def test_catalog_routing_failure_is_explicit_and_never_retried() -> None:
    error = CatalogRoutingError(
        "resolve_call_profile: model 'retired-model' has no available ai.offering"
    )

    classified = classify_provider_error("unknown", error)

    assert classified.error_type == "matrx_catalog_error"
    assert classified.is_retryable is False
    assert "retired-model" in classified.message
    assert "retired-model" in classified.user_message


def test_database_failure_is_never_laundered_as_a_provider_error() -> None:
    """A DB/ORM failure inside a provider's broad ``except Exception`` must keep
    its own identity. The 2026-08 outage (history.row_versions ran out of
    partitions) surfaced to users as "An unexpected Google error occurred.
    Retrying..." on five different providers at once, and burned paid retries on
    a condition no retry could fix.
    """

    class _FakeOrmIntegrityError(Exception):
        __module__ = "matrx_orm.exceptions"

    error = _FakeOrmIntegrityError('no partition of relation "row_versions" found for row')

    for classified in (
        classify_anthropic_error(error),
        classify_google_error(error),
        classify_provider_error("together", error),
    ):
        assert classified.error_type == "matrx_infrastructure_error"
        assert classified.is_retryable is False
        # The real message is the only diagnosable thing — never drop it.
        assert "row_versions" in classified.message
        assert "row_versions" in classified.user_message
        assert classified.details["infrastructure"] == "matrx_orm"


def test_infrastructure_classification_matches_on_base_classes() -> None:
    """Subclasses of a driver/ORM exception are ours too — match on the MRO."""

    class _AsyncpgBase(Exception):
        __module__ = "asyncpg.exceptions"

    class _AppSubclass(_AsyncpgBase):
        __module__ = "some_app.errors"

    assert (
        classify_provider_error("openai", _AppSubclass("connection refused")).error_type
        == "matrx_infrastructure_error"
    )


def test_ordinary_provider_exceptions_are_still_provider_errors() -> None:
    """The infrastructure guard must not swallow genuine provider failures."""
    assert classify_provider_error("openai", Exception("429 rate limit")).error_type != (
        "matrx_infrastructure_error"
    )


def test_provider_adapters_do_not_log_tracebacks_or_emit_terminal_errors() -> None:
    providers_root = Path(__file__).parents[1] / "matrx_ai" / "providers"
    adapter_paths = (
        "anthropic/anthropic_api.py",
        "openai/openai_api.py",
        "google/google_api.py",
        "xai/xai_api.py",
        "groq/groq_api.py",
        "together/together_api.py",
        "cerebras/cerebras_api.py",
        "eleven_labs/elevenlabs_api.py",
    )

    for relative_path in adapter_paths:
        source = (providers_root / relative_path).read_text()
        assert "traceback.print_exc" not in source, relative_path
        assert (
            "error_type=error_info.error_type" not in source
        ), f"{relative_path} emits a classified exception instead of rethrowing it"
