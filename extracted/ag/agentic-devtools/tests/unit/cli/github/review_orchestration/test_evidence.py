import pytest
from pydantic import ValidationError

from agentic_devtools.cli.github.review_orchestration import Evidence


def test_complete_collection_does_not_encode_green_ci(state_data):
    evidence = Evidence.model_validate(state_data["evidence"])
    assert evidence.checks == "complete"
    assert evidence.review_id == 17


@pytest.mark.parametrize(
    "updates",
    [
        {"head_sha": "a" * 40 + "\n"},
        {"fingerprint": "b" * 64 + "\n"},
        {"checks": None},
        {"reviews": "green"},
        {"threads": False},
        {"tasks": 0},
    ],
)
def test_rejects_invalid_provider_shape(state_data, updates):
    with pytest.raises(ValidationError):
        Evidence.model_validate({**state_data["evidence"], **updates})
