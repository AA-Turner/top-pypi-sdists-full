import pytest
from connector.oai.capabilities.errors import CapabilityError
from pytest_cases import parametrize_with_cases

from .test_executor_cases import (
    CaseCapabilityExecutorFailureMode,
    CaseCapabilityExecutorSuccessMode,
    ExecutorFailureModeCases,
    ExecutorSuccessModeCases,
)


class TestCapabilityExecutor:
    @parametrize_with_cases(
        "case",
        cases=ExecutorSuccessModeCases,
    )
    async def test_executor(self, case: CaseCapabilityExecutorSuccessMode) -> None:
        actual_response = await case.executor.execute(case.serialized_request)
        assert case.expected_response == actual_response

    @parametrize_with_cases(
        "case",
        cases=ExecutorFailureModeCases,
    )
    async def test_executor_failure_mode(self, case: CaseCapabilityExecutorFailureMode) -> None:
        with pytest.raises(CapabilityError) as excinfo:
            await case.executor.execute(case.serialized_request)

        actual_exception_type = type(excinfo.value)
        assert actual_exception_type == case.expected_exception_type, "Unexpected exception type."

        if case.expected_exception_contains:
            assert case.expected_exception_contains in excinfo.value._message
