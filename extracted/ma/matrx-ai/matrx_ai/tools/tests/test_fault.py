from matrx_ai.tools.executor import _is_expected_domain_failure
from matrx_ai.tools.fault import MODEL_ERROR, TOOL_DEFECT, classify_fault


def test_validation_is_model_fault_and_remains_capture_suppressed() -> None:
    assert classify_fault("validation") == MODEL_ERROR
    assert _is_expected_domain_failure(tool_name="data", error_type="validation")


def test_unexpected_tool_execution_remains_tool_defect() -> None:
    assert classify_fault("execution") == TOOL_DEFECT
    assert not _is_expected_domain_failure(tool_name="data", error_type="execution")
