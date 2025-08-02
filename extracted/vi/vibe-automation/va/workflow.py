import inspect
import logging
import os
import uuid
import warnings
from typing import get_type_hints

from pydantic import BaseModel, ValidationError

from va.automation import Automation
from va.store import get_store
from va.logging_handlers import ExecutionLogHandler
from va.utils import is_test_execution, TEST_EXECUTION_PREFIX
from va.protos.orby.va.public.execution_messages_pb2 import ExecutionStatus


def _process_function_arguments(func, args, kwargs, automation, is_managed_execution):
    """
    Process function arguments to handle input replacement and logger injection.

    Args:
        func: The decorated function
        args: Original positional arguments
        kwargs: Original keyword arguments
        automation: Automation instance
        is_managed_execution: Whether this is a managed execution

    Returns:
        Tuple of (modified_args, modified_kwargs)
    """
    # Get function signature and type hints
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)
    param_names = list(sig.parameters.keys())

    # Convert args to kwargs for easier processing
    bound_args = sig.bind_partial(*args, **kwargs)
    bound_args.apply_defaults()
    all_kwargs = dict(bound_args.arguments)

    # Handle input replacement
    if param_names and param_names[0] == "input":
        input_param_name = param_names[0]
        input_type = type_hints.get(input_param_name)

        # Check if we're in managed execution environment
        if is_managed_execution:
            try:
                # Get execution input from automation
                execution_input = automation.execution.get_input()

                # Validate and convert input if type hint is a Pydantic model
                if input_type and _is_pydantic_model(input_type):
                    try:
                        validated_input = input_type(**execution_input)
                        all_kwargs[input_param_name] = validated_input
                    except ValidationError as e:
                        raise ValueError(
                            f"Input validation failed for parameter '{input_param_name}': {e}"
                        )
                else:
                    # No validation, use raw input
                    all_kwargs[input_param_name] = execution_input

            except ValueError:
                # Re-raise validation errors
                raise
            except Exception as e:
                warnings.warn(
                    f"Failed to get execution input: {e}. Using original argument.",
                    UserWarning,
                )
    elif is_managed_execution and param_names:
        # First parameter is not named "input" but we have managed execution
        warnings.warn(
            f"Execution input provided but first parameter is named '{param_names[0]}' instead of 'input'. "
            "To activate input replacement behavior, rename the first parameter to 'input'.",
            UserWarning,
        )

    # Handle logger injection
    logger_params = [
        name
        for name, param in sig.parameters.items()
        if param.annotation == logging.Logger
        or (
            hasattr(param.annotation, "__origin__")
            and param.annotation.__origin__ is logging.Logger
        )
    ]

    for logger_param in logger_params:
        if logger_param not in all_kwargs or all_kwargs[logger_param] is None:
            # Create managed logger for this execution
            managed_logger = _create_managed_logger(automation.execution_id)
            all_kwargs[logger_param] = managed_logger

    # Convert back to args and kwargs
    new_args = []
    new_kwargs = {}

    for i, param_name in enumerate(param_names):
        if i < len(args):
            # This was originally a positional argument
            new_args.append(all_kwargs[param_name])
        else:
            # This was a keyword argument, default, or injected
            if param_name in all_kwargs:
                new_kwargs[param_name] = all_kwargs[param_name]

    return tuple(new_args), new_kwargs


def _is_pydantic_model(type_hint):
    """Check if a type hint is a Pydantic model."""
    try:
        return isinstance(type_hint, type) and issubclass(type_hint, BaseModel)
    except (TypeError, AttributeError):
        return False


def _create_managed_logger(execution_id: str):
    """Create (or fetch) a managed logger instance for the execution.

    The logger is equipped with a A StreamHandler so that logs still appear on stdout/stderr
    """

    logger = logging.getLogger(f"va.execution.{execution_id}")

    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(
            logging.Formatter(
                f"[{execution_id[:8]}] %(asctime)s - %(levelname)s - %(message)s"
            )
        )
        logger.addHandler(stream_handler)

    logger.setLevel(logging.INFO)
    return logger


def workflow(workflow_name: str):
    """
    Decorator for defining a workflow execution entrypoint.

    This decorator should be applied to the main function that implements your workflow
    logic. It sets up the execution environment, manages execution, and handles workflow
    lifecycle events.

    Args:
        workflow_name (str): Unique identifier for the workflow. Used to identify and
            categorize workflow executions in the store.

    Returns:
        A decorator function that wraps the workflow main function.

    Execution Management:
        - If VA_EXECUTION_ID environment variable is set, reuses that execution
        - Otherwise creates a new execution with a unique ID

    Usage:
        @workflow("data_processing_pipeline")
        def main():
            # Your workflow implementation here
            step = Step("process_data")
            # ... workflow logic

    Example:
        # Reuse existing execution
        import os
        os.environ['VA_EXECUTION_ID'] = 'existing_execution_123'

        @workflow("user_onboarding")
        def onboard_user():
            # This execution will be part of execution 'existing_execution_123'
            pass

        # Create new execution (default behavior)
        @workflow("report_generation")
        def generate_report():
            # This creates a new execution automatically
            pass
    """

    def decorator(func):
        def _setup_execution():
            """Setup execution environment - common logic for sync and async."""
            # create VA_EXECUTION_ID if it is not set
            if "VA_EXECUTION_ID" in os.environ:
                execution_id = os.environ["VA_EXECUTION_ID"]
                is_managed_execution = True
            else:
                execution_id = TEST_EXECUTION_PREFIX + "-" + str(uuid.uuid4())
                is_managed_execution = False

            store = get_store(is_managed_execution)

            # Attach a single root-level ExecutionLogHandler bound to this execution
            # (if not a local test execution) so all relevant logs are forwarded to the backend
            if not is_test_execution(execution_id):
                root_logger = logging.getLogger()
                root_logger.addHandler(ExecutionLogHandler(execution_id))

            automation = Automation(store, workflow_name, execution_id)
            Automation.set_instance(automation)
            automation.execution.mark_start()

            return automation, is_managed_execution

        def _execute_function(
            target_func, args, kwargs, automation, is_managed_execution
        ):
            """Execute function with proper argument processing - common logic."""
            if is_managed_execution:
                modified_args, modified_kwargs = _process_function_arguments(
                    target_func, args, kwargs, automation, is_managed_execution
                )
                return target_func(*modified_args, **modified_kwargs)
            else:
                return target_func(*args, **kwargs)

        if inspect.iscoroutinefunction(func):
            # Handle async functions
            async def async_wrapper(*args, **kwargs):
                automation, is_managed_execution = _setup_execution()

                try:
                    result = await _execute_function(
                        func, args, kwargs, automation, is_managed_execution
                    )

                    # Completed successfully – update status.
                    automation.execution.mark_stop(status=ExecutionStatus.COMPLETED)
                    return result

                except Exception:
                    automation.execution.mark_stop(status=ExecutionStatus.FAILED)
                    raise
                finally:
                    # Print workflow mutation diffs before marking execution as stopped
                    automation.mutation.print_all_diffs()

            return async_wrapper
        else:
            # Handle sync functions
            def wrapper(*args, **kwargs):
                automation, is_managed_execution = _setup_execution()

                try:
                    result = _execute_function(
                        func, args, kwargs, automation, is_managed_execution
                    )
                    # Completed successfully – update status.
                    automation.execution.mark_stop(status=ExecutionStatus.COMPLETED)
                    return result

                except Exception:
                    # Failure – update status then re-raise.
                    automation.execution.mark_stop(status=ExecutionStatus.FAILED)
                    raise

                finally:
                    # Print workflow mutation diffs before marking execution as stopped
                    automation.mutation.print_all_diffs()

            return wrapper

    return decorator
