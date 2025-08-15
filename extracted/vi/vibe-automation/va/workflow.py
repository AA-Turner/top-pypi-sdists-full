import inspect
import logging
import os
import uuid
import warnings
from typing import get_type_hints

from pydantic import BaseModel, ValidationError

from va.automation import Automation
from va.playwright.page import Page
from va.store import get_store
from va.configure_structlog import configure_structlog, bind_execution_id_to_root_logger
from va.execution_log_handler import ExecutionLogHandler
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
        provided_logger = all_kwargs.get(logger_param)

        # If the caller did not supply a logger, create one tied to this execution.
        if provided_logger is None:
            provided_logger = _create_managed_logger(automation.execution_id)

        all_kwargs[logger_param] = provided_logger

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
    """Create (or fetch) a managed logger instance for the execution."""
    logger = logging.getLogger(f"va.execution.{execution_id}")
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

            # Configure JSON output immediately so that **all** subsequent logs (even those coming
            # from libraries imported later) benefit from the formatter.
            configure_structlog()

            # Ensure *every* log record generated in this process carries the execution_id
            bind_execution_id_to_root_logger(execution_id)

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
                    logging.getLogger().exception("Workflow execution failed")
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
                    logging.getLogger().exception("Workflow execution failed")
                    # Failure – update status then re-raise.
                    automation.execution.mark_stop(status=ExecutionStatus.FAILED)
                    raise

                finally:
                    # Print workflow mutation diffs before marking execution as stopped
                    automation.mutation.print_all_diffs()

            return wrapper

    return decorator


class WorkflowCompletionResult(BaseModel):
    """Result model for workflow completion verification."""

    completed: bool
    message: str


async def assert_workflow_completion(page: Page):
    """
    Assert that the workflow has been completed successfully based on the current page state.

    This function extracts the workflow goal from the containing function's docstring
    and uses the page's extract method to verify if the workflow can be considered complete.

    Args:
        page: The Page instance to check for completion

    Raises:
        Exception: If the workflow is not complete with details from the verification
    """
    # Get the calling frame to extract the workflow goal from the docstring
    frame = inspect.currentframe()
    try:
        # Go up the call stack to find the calling function
        calling_frame = frame.f_back
        if calling_frame is None:
            raise Exception(
                "Could not determine calling function for workflow goal extraction"
            )

        # Get the calling function's code object
        calling_function_name = calling_frame.f_code.co_name

        # Get the module where the calling function is defined
        calling_module = inspect.getmodule(calling_frame)

        # First try: Get from frame's globals (most reliable for dynamically loaded modules)
        calling_function = calling_frame.f_globals.get(calling_function_name)

        # Second try: Get from module if available
        if calling_function is None and calling_module is not None:
            calling_function = getattr(calling_module, calling_function_name, None)

        # Extract the docstring which contains the workflow goal
        workflow_goal = None

        if calling_function is not None:
            workflow_goal = inspect.getdoc(calling_function)

        # If we still don't have a docstring, try to get it from the code object
        if not workflow_goal:
            code_obj = calling_frame.f_code
            # Get the first constant which is typically the docstring
            if code_obj.co_consts and isinstance(code_obj.co_consts[0], str):
                # Check if the first constant looks like a docstring
                potential_docstring = code_obj.co_consts[0]
                if len(potential_docstring) > 10:  # Basic heuristic for docstring
                    workflow_goal = potential_docstring

        if not workflow_goal:
            raise Exception(
                f"No docstring found for function '{calling_function_name}' - workflow goal cannot be determined"
            )

    finally:
        del frame

    verification_prompt = f"""
    Based on the current page state, determine if the following workflow goal has been completed:
    
    WORKFLOW GOAL: {workflow_goal}
    
    Analyze the page content and determine:
    1. Whether the workflow goal has been fully achieved
    2. Provide a clear explanation of your assessment
    """

    result = await page.extract(verification_prompt, schema=WorkflowCompletionResult)
    completion_result = result.extraction

    # Raise exception if workflow is not complete
    if not completion_result.completed:
        raise Exception(f"Workflow not complete: {completion_result.message}")
