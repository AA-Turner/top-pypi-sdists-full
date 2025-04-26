import pytest

# These will be set by gather_cases
missing_capabilities: set[str] = set()
integration_name: str = ""


def case_coverage_check():
    pytest.fail(
        f"Integration {integration_name} does not have full coverage. "
        f"Missing tests for capabilities: {', '.join(missing_capabilities)}"
    )
