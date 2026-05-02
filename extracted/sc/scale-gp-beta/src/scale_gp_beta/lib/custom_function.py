import inspect
import textwrap
from typing import Any, Dict, List, Callable, Optional

from scale_gp_beta import SGPClient
from scale_gp_beta.types.evaluation_task_param import (
    CustomFunctionEvaluationTask,
    CustomFunctionEvaluationTaskConfiguration,
)
from scale_gp_beta.types.evaluation_schema_response import Field


def _extract_function_source(func: Callable[..., Any]) -> str:
    """Extract the source code of a function.

    Only the function source is captured; module-level code is not. Any imports
    the function depends on must be placed inside the function body so they are
    included in the serialized source sent to the API::

        def my_func(x):
            import math          # included
            return math.sqrt(x)

    Decorators are also captured by ``inspect.getsource``, so any decorator
    that references a module-level import will fail at remote execution time
    with a ``NameError``::

        # also incorrect — @my_decorator references an external symbol remotely
        import my_decorator

        @my_decorator
        def my_func(x):
            return x

    Args:
        func: The callable to extract source from.

    Returns:
        The dedented function source string.

    Raises:
        ValueError: If the source code cannot be extracted (e.g. lambdas, builtins).
    """
    if getattr(func, "__name__", "") == "<lambda>":
        raise ValueError(
            "Cannot use a lambda as a custom function. "
            "Please define a named function instead."
        )

    try:
        source = inspect.getsource(func)
    except (OSError, TypeError) as e:
        raise ValueError(
            f"Cannot extract source code from {func!r}. "
            "Ensure the function is defined in a regular .py file "
            "(lambdas and built-in functions are not supported)."
        ) from e

    return textwrap.dedent(source)


def get_evaluation_columns(client: SGPClient, evaluation_id: str) -> List[Field]:
    """Return the data columns available on an evaluation's items.

    Useful for discovering which column names to use in ``arg_mapping``
    before defining a :class:`CustomFunction`.

    Args:
        client: An authenticated SGPClient instance.
        evaluation_id: The ID of the evaluation to inspect.

    Returns:
        List of :class:`~scale_gp_beta.types.evaluation_schema_response.Field`
        objects, each with ``field_name`` and ``data_type``. Only fields from
        the ``data`` source are returned (task result fields are excluded).

    Example::

        columns = get_evaluation_columns(client, "eval_abc123")
        for col in columns:
            print(col.field_name, col.data_type)
    """
    schema = client.evaluations.retrieve_schema(evaluation_id)
    return [f for f in schema.fields if f.source == "data"]


class CustomFunction:
    """Wraps a Python callable for use as a custom function evaluation task.

    Extracts the function source code and provides serialization for the
    evaluation API and a dry-run method for testing against sample data.

    Any imports the function depends on must be placed **inside the function
    body**. Module-level imports are not captured and will not be available
    at remote execution time::

        # correct
        def my_func(x):
            import math
            return math.sqrt(x)

        # incorrect — math will not be available remotely
        import math
        def my_func(x):
            return math.sqrt(x)

    Args:
        func: The Python callable to wrap.
        alias: Display name for the task. Defaults to func.__name__.
        arg_mapping: Optional mapping from function parameter names to
            dataset column names.
    """

    TASK_TYPE = "custom_function"

    def __init__(
        self,
        func: Callable[..., Any],
        alias: Optional[str] = None,
        arg_mapping: Optional[Dict[str, str]] = None,
    ):
        self.func = func
        self.alias = alias or getattr(func, "__name__", None) or repr(func)
        self.arg_mapping = arg_mapping
        self.function_source = _extract_function_source(func)

    @staticmethod
    def _normalize_locator(value: str) -> str:
        """Normalize an arg_mapping value to a item locator.

        Plain column names are prefixed with ``item.``; values that already
        start with ``item.`` are passed through unchanged to support nested
        locators (e.g. ``item.nested.field``).
        """
        if not value:
            raise ValueError("arg_mapping values must be non-empty strings.")
        return value if value.startswith("item.") else f"item.{value}"

    def _build_configuration(self) -> CustomFunctionEvaluationTaskConfiguration:
        configuration = CustomFunctionEvaluationTaskConfiguration(
            function_source=self.function_source,
        )
        if self.arg_mapping:
            configuration["arg_mapping"] = {
                k: self._normalize_locator(v) for k, v in self.arg_mapping.items()
            }
        return configuration

    def serialize(self) -> CustomFunctionEvaluationTask:
        """Return a task config dict ready for the evaluation tasks array.

        Returns:
            A dictionary with task_type, alias, and configuration suitable
            for inclusion in an evaluation creation request.
        """
        return CustomFunctionEvaluationTask(
            task_type="custom_function",
            alias=self.alias,
            configuration=self._build_configuration(),
        )

    def dry_run(
        self,
        client: SGPClient,
        sample_data: List[Dict[str, Any]],
    ) -> Any:
        """Execute a dry run of this custom function against sample data.

        Calls the evaluation dry-run endpoint to validate the function
        source and preview results without creating a full evaluation.

        Args:
            client: An authenticated SGPClient instance.
            sample_data: A list of row dicts to run the function against.

        Returns:
            The parsed API response.
        """
        response = client.post(
            "/v5/evaluations/tasks/dry-run",
            body={
                "task_type": self.TASK_TYPE,
                "configuration": self._build_configuration(),
                "sample_data": sample_data,
            },
            cast_to=object,
        )
        return response
