"""Workflows for testing handler input validation.

These workflows are used by integration tests to verify that workflow handlers
(signals, queries, updates, entrypoints) properly validate inputs at runtime.
"""

import mistralai.workflows as workflows


@workflows.workflow.define(name="test-validation-workflow")
class ValidationTestWorkflow:
    """Workflow for testing basic handler validation.

    This workflow stays running until the 'complete' signal is sent,
    allowing tests to send signals, queries, and updates before completion.
    """

    def __init__(self) -> None:
        self.received_signals: list[tuple[str, int]] = []
        self.received_updates: list[int] = []
        self.query_calls: int = 0
        self._should_complete: bool = False

    @workflows.workflow.entrypoint
    async def run(self, initial_value: int) -> str:
        await workflows.workflow.wait_condition(lambda: self._should_complete)
        return f"Workflow completed with {initial_value}"

    @workflows.workflow.signal()
    async def process_signal(self, name: str, count: int) -> None:
        self.received_signals.append((name, count))

    @workflows.workflow.signal()
    async def complete(self) -> None:
        """Signal to mark the workflow as complete."""
        self._should_complete = True

    @workflows.workflow.query()
    def get_state(self, include_details: bool = False) -> dict:
        self.query_calls += 1
        return {"signals": len(self.received_signals), "details": include_details}

    @workflows.workflow.update()
    async def update_config(self, new_value: int) -> str:
        self.received_updates.append(new_value)
        return f"Updated to {new_value}"


@workflows.workflow.define(name="test-complex-validation")
class ComplexValidationWorkflow:
    """Workflow for testing complex type validation."""

    @workflows.workflow.entrypoint
    async def run(self, config: dict) -> str:
        return f"Received config with {len(config)} items"

    @workflows.workflow.signal()
    async def process_items(self, items: list) -> None:
        pass
