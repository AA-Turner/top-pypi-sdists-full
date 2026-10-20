"""G4 leak 6: a rank tool's provider choices are plain tiers; the legacy ids still validate."""

import json

import pytest
from pydantic import TypeAdapter, ValidationError

from matrx_ai.tools.arg_models._provider_tiers import (
    TIER_TO_PROVIDER,
    Provider,
    ProviderWithAnswers,
)
from matrx_ai.tools.arg_models.dispatcher_args import SeoCollectRankWire

_VENDOR_IDS = ("brave", "serpapi", "dataforseo")


def test_schema_lists_tiers_only() -> None:
    assert TypeAdapter(ProviderWithAnswers).json_schema()["enum"] == ["web", "google", "ai_answers"]
    assert TypeAdapter(Provider).json_schema()["enum"] == ["web", "google"]
    schema = json.dumps(SeoCollectRankWire.model_json_schema())
    assert not any(v in schema for v in _VENDOR_IDS)


@pytest.mark.parametrize("value", ["web", "google", "ai_answers", "brave", "serpapi", "dataforseo"])
def test_new_and_legacy_values_validate(value: str) -> None:
    out = TypeAdapter(ProviderWithAnswers).validate_python(value)
    assert out in _VENDOR_IDS
    assert TIER_TO_PROVIDER.get(value, value) == out


def test_unknown_value_is_refused() -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(Provider).validate_python("bing")
    with pytest.raises(ValidationError):
        TypeAdapter(Provider).validate_python("ai_answers")


@pytest.mark.parametrize(("phrase", "expected"), [
    ("our search data service", "serpapi"),
    ("our SEO data service", "dataforseo"),
])
def test_the_two_intermediate_phrases_of_2026_10_16_still_validate(phrase: str, expected: str) -> None:
    """OTH-9: four stored `seo` versions listed these for one day; a stored call or agent config must still validate."""
    assert TypeAdapter(ProviderWithAnswers).validate_python(phrase) == expected
    if expected == "serpapi":  # the two-way rank field takes the search phrase; the SEO-data phrase is three-way only
        assert TypeAdapter(Provider).validate_python(phrase) == expected
    else:
        with pytest.raises(ValidationError):
            TypeAdapter(Provider).validate_python(phrase)


def test_an_intermediate_phrase_is_not_a_tier_the_schema_offers() -> None:
    assert "our search data service" not in json.dumps(TypeAdapter(ProviderWithAnswers).json_schema())
