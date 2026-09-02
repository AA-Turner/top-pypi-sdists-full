import pytest

from agentic_devtools.ai_providers.priors import PriorSet, PriorValidationError


def test_prior_set_rejects_bad_version_and_bad_mapping() -> None:
    with pytest.raises(PriorValidationError):
        PriorSet(version="")
    with pytest.raises(PriorValidationError):
        PriorSet(model_overrides=[])  # type: ignore[arg-type]
