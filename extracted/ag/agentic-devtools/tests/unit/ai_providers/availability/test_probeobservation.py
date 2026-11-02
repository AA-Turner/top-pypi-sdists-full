import pytest

from agentic_devtools.ai_providers.availability import ProbeObservation
from agentic_devtools.ai_providers.errors import ProviderError


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        (
            {"model": "", "surface": "model", "status_code": 200, "classification": "ACCEPTED"},
            "model must be a non-empty string",
        ),
        (
            {"model": "model-a", "surface": "unknown", "status_code": 200, "classification": "ACCEPTED"},
            "surface must be one of",
        ),
        (
            {"model": "model-a", "surface": "model", "status_code": True, "classification": "ACCEPTED"},
            "status_code must be an integer",
        ),
        (
            {"model": "model-a", "surface": [], "status_code": 200, "classification": "ACCEPTED"},
            "surface must be one of",
        ),
        (
            {"model": "model-a", "surface": "model", "status_code": 200, "classification": []},
            "classification must be a valid",
        ),
        (
            {"model": "model-a", "surface": "model", "status_code": 200, "classification": "OTHER"},
            "classification must be a valid",
        ),
        (
            {
                "model": "model-a",
                "surface": "model",
                "status_code": 200,
                "classification": "ACCEPTED",
                "body_excerpt": 123,
            },
            "body_excerpt must be a string",
        ),
    ],
)
def test_probe_observation_validates_fields(kwargs: dict[str, object], match: str) -> None:
    with pytest.raises(ProviderError, match=match):
        ProbeObservation(**kwargs)  # type: ignore[arg-type]


def test_probe_observation_accepts_valid_payload() -> None:
    observation = ProbeObservation(
        model="model-a",
        surface="base_ref",
        status_code=412,
        classification="ACCEPTED",
        body_excerpt="base_ref missing",
    )

    assert observation.body_excerpt == "base_ref missing"
    assert observation.surface == "base_ref"
