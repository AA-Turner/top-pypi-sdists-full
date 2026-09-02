import pytest

from agentic_devtools.ai_providers.availability import canonicalize_matrix
from agentic_devtools.ai_providers.errors import ProviderError


def test_canonicalize_matrix_normalizes_statuses_and_sorts_models() -> None:
    assert canonicalize_matrix({"gemini-3.1-pro-preview": "REJECTED", "claude-opus-5": "available"}) == {
        "claude-opus-5": "available",
        "gemini-3.1-pro-preview": "rejected",
    }


def test_canonicalize_matrix_rejects_invalid_model_names_and_statuses() -> None:
    with pytest.raises(ProviderError, match="Model names must be non-empty strings"):
        canonicalize_matrix({"": "available"})

    with pytest.raises(ProviderError, match="Unsupported availability status"):
        canonicalize_matrix({"claude-opus-5": "maybe"})


def test_canonicalize_matrix_rejects_non_string_model_names_before_sorting() -> None:
    with pytest.raises(ProviderError, match="Model names must be non-empty strings"):
        canonicalize_matrix({1: "available", "claude-opus-5": "available"})  # type: ignore[dict-item]


def test_canonicalize_matrix_rejects_non_string_status_values() -> None:
    with pytest.raises(ProviderError, match="must be a string"):
        canonicalize_matrix({"claude-opus-5": 1})  # type: ignore[dict-item]

    with pytest.raises(ProviderError, match="must be a string"):
        canonicalize_matrix({"claude-opus-5": None})  # type: ignore[dict-item]


def test_canonicalize_matrix_normalizes_model_names() -> None:
    assert canonicalize_matrix({" claude-opus-5 ": "available"}) == {"claude-opus-5": "available"}


def test_canonicalize_matrix_rejects_model_name_collisions_after_normalization() -> None:
    with pytest.raises(ProviderError, match="Model name collision after normalization"):
        canonicalize_matrix({"claude-opus-5": "available", " claude-opus-5 ": "rejected"})
