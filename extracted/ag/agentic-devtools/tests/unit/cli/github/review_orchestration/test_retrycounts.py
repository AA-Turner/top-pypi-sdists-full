import pytest
from pydantic import ValidationError

from agentic_devtools.cli.github.review_orchestration import RetryCounts


def test_retry_classes_are_independent(state_data):
    failures = {**state_data["failures"], "throttling": 1, "repair": 1}
    assert RetryCounts.model_validate(failures).transport == 0


@pytest.mark.parametrize("updates", [{"transport": -1}, {"repair": True}, {"all": 0}])
def test_invalid_retry_counts_fail(state_data, updates):
    with pytest.raises(ValidationError):
        RetryCounts.model_validate({**state_data["failures"], **updates})
