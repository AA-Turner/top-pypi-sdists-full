"""
Aetheris Headless Runner Module

Provides non-interactive, programmatic execution of Aetheris tasks.

Usage:
    from src.runner import TaskRunner, TaskFile, ExecutionResult

    # Parse and validate task file
    task_file = TaskFile.from_file("task.json")

    # Execute task
    runner = TaskRunner(task_file)
    result = await runner.execute()

    # Output as JSON
    print(result.to_json())
"""

from src.runner.executor import TaskRunner
from src.runner.output_formatter import ExecutionResult, OutputFormatter
from src.runner.task_parser import TaskFile, TaskFileParser, TaskFileValidationError

__all__ = [
    "TaskRunner",
    "TaskFile",
    "TaskFileParser",
    "TaskFileValidationError",
    "ExecutionResult",
    "OutputFormatter",
]
