import temporalio.workflow

from mistralai.workflows import workflow


class TestUnsafeImportsPassedThrough:
    def test_imports_passed_through(self) -> None:
        assert not temporalio.workflow.unsafe.is_imports_passed_through()
        with workflow.unsafe.imports_passed_through():
            assert temporalio.workflow.unsafe.is_imports_passed_through()
        assert not temporalio.workflow.unsafe.is_imports_passed_through()


class TestUnsafeSkipDeterminismEnforcement:
    def test_skip_determinism_enforcement(self) -> None:
        assert not temporalio.workflow.unsafe.is_sandbox_unrestricted()
        with workflow.unsafe.skip_determinism_enforcement():
            assert temporalio.workflow.unsafe.is_sandbox_unrestricted()
        assert not temporalio.workflow.unsafe.is_sandbox_unrestricted()
