from collections.abc import Callable
from jsonpath_ng import parse
import asyncio
import pandas as pd
from ..exceptions import ComponentError
from .BaseLoop import BaseLoop


class IF(BaseLoop):
    """
    IF Component

    Executes one of two components based on a condition.

    true_component: The component to execute if the condition evaluates to True.
    false_component: The component to execute if the condition evaluates to False.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          IF:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._condition = kwargs.get("condition", None)
        self._true_component = kwargs.get("true_component", None)
        self._false_component = kwargs.get("false_component", None)
        super(IF, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """
        Initialize the component.
        """
        await super(IF, self).start(**kwargs)
        # Ensure the condition and components are defined
        if not self._condition:
            raise ComponentError(
                "The 'condition' argument must be provided."
            )
        if not self._true_component or not self._false_component:
            raise ComponentError(
                "Both 'true_component' and 'false_component' must be specified."
            )
        return True

    def _evaluate_condition(self, condition: str) -> bool:
        """
        Evaluate a condition based on the type of self.data.

        Args:
            condition (str): A condition in the format "<jsonpath> <operator> <value>".

        Returns:
            bool: True if the condition is satisfied, else False.
        """
        if isinstance(self.data, dict):
            try:
                jsonpath_expr, operator, expected_value = self._parse_condition(condition)
                jsonpath = parse(jsonpath_expr)
                matches = jsonpath.find(self.data)
                actual_value = matches[0].value if matches else None
                return self._evaluate_operator(
                    actual_value,
                    operator,
                    expected_value
                )
            except Exception as err:
                raise ComponentError(
                    f"Error evaluating condition '{condition}': {err}"
                )

        elif isinstance(self.data, pd.DataFrame):
            try:
                filtered = self.data.query(condition)
                return not filtered.empty
            except Exception as err:
                raise ComponentError(
                    f"Error evaluating DataFrame condition '{condition}': {err}"
                )

        elif isinstance(self.data, str):
            return condition in self.data

        else:
            raise ComponentError(
                f"Unsupported data type for condition evaluation: {type(self.data)}"
            )

    def _parse_condition(self, condition: str):
        """
        Parse the condition into JSONPath, operator, and expected value.

        Args:
            condition (str): A condition string, e.g., "$.metadata.type == 'recapDefinition'".

        Returns:
            tuple: (jsonpath_expr, operator, expected_value)
        """
        operators = ["==", "!=", ">", "<", ">=", "<="]
        for op in operators:
            if op in condition:
                parts = condition.split(op)
                if len(parts) != 2:
                    raise ValueError(
                        f"Invalid condition format: {condition}"
                    )
                jsonpath_expr, expected_value = parts
                expected_value = expected_value.strip().strip("'\"")  # Remove quotes
                return jsonpath_expr.strip(), op, expected_value
        raise ValueError(
            f"No valid operator found in condition: {condition}"
        )

    def _evaluate_operator(self, actual_value, operator, expected_value):
        """
        Evaluate the comparison operator.

        Args:
            actual_value: The value extracted from JSONPath.
            operator: The comparison operator as a string.
            expected_value: The value to compare against.

        Returns:
            bool: True if the comparison is satisfied, else False.
        """
        if operator == "==":
            return actual_value == expected_value
        elif operator == "!=":
            return actual_value != expected_value
        elif operator == ">":
            return actual_value > expected_value
        elif operator == "<":
            return actual_value < expected_value
        elif operator == ">=":
            return actual_value >= expected_value
        elif operator == "<=":
            return actual_value <= expected_value
        else:
            raise ValueError(
                f"Unsupported operator: {operator}"
            )

    async def run(self):
        """
        Executes the appropriate component based on the condition.
        """
        try:
            condition_result = self._evaluate_condition(self._condition)
        except ComponentError as e:
            raise ComponentError(
                f"Error evaluating condition '{self._condition}': {e}"
            )

        selected_component = (
            self._true_component if condition_result else self._false_component
        )

        step, idx = self._TaskPile.getStepByName(selected_component)
        if step is None:
            raise ComponentError(
                f"Component '{selected_component}' not found in Task Definition."
            )

        target, params, stat = self.get_component(step)
        component_instance = self.create_component(
            target,
            value=self.data,
            stat=stat,
            **params
        )
        self._result = await self.exec_component(
            component_instance,
            step.name
        )
        # Remove executed components
        self._TaskPile.delStepByName(self._true_component)
        self._TaskPile.delStepByName(self._false_component)
        return self._result
