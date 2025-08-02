from va.automation import Automation


class StepContextManager:
    """Hybrid context manager for workflow-level step tracking that supports both sync and async contexts."""

    def __init__(self, description: str):
        self.description = description
        self.automation = Automation.get_instance()

    def __enter__(self):
        """Synchronous context manager entry."""
        self.automation.execution.mark_step_executing(self.description)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Synchronous context manager exit."""
        self.automation.execution.mark_step_executed(self.description)
        return False  # Don't suppress exceptions

    async def __aenter__(self):
        """Asynchronous context manager entry."""
        self.automation.execution.mark_step_executing(self.description)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Asynchronous context manager exit."""
        self.automation.execution.mark_step_executed(self.description)
        return False  # Don't suppress exceptions


def step(description: str):
    """
    Create a step context manager that works with both sync and async contexts.

    This function returns a context manager that can be used with both 'with' and 'async with'.
    It tracks step execution by marking when steps start and complete.

    Parameters:
    -----------
    description (str): Description of the step being executed

    Returns:
    --------
    StepContextManager: Context manager for step tracking

    Examples:
    ---------
    # Synchronous usage
    with step("Processing data"):
        # sync code here
        pass

    # Asynchronous usage
    async with step("Processing data"):
        # async code here
        pass
    """
    return StepContextManager(description)
