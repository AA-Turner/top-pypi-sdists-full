from collections.abc import Callable
from jsonpath_ng import parse
import asyncio
import pandas as pd
from ..exceptions import (
    ComponentError,
)
from .BaseLoop import BaseLoop


class Switch(BaseLoop):
    """
    Switch Component

    Routes execution to a specific component based on user-defined conditions.

    cases: Defines a list of conditions and their corresponding components.
        Each condition is a Python-style logical expression evaluated against self.data.
    default: Specifies the fallback component if none of the conditions match.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Switch:
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
        self._cases = kwargs.get("cases", [])
        super(Switch, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """
        start.

            Initialize (if needed) a task
        """
        await super(Switch, self).start(**kwargs)
        # Add all case components to the tracker
        self._define_tracking_components(*self._cases)
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
            # Parse the condition: split JSONPath and comparison
            try:
                # Split the condition into JSONPath and comparison
                jsonpath_expr, operator, expected_value = self._parse_condition(condition)

                # Evaluate the JSONPath
                jsonpath = parse(jsonpath_expr)
                matches = jsonpath.find(self.data)

                # Get the first match (if any)
                actual_value = matches[0].value if matches else None

                # Evaluate the operator
                return self._evaluate_operator(actual_value, operator, expected_value)

            except Exception as err:
                raise ComponentError(f"Error evaluating condition '{condition}': {err}")

        elif isinstance(self.data, pd.DataFrame):
            # For DataFrame, condition should be a valid query string
            try:
                filtered = self.data.query(condition)
                return not filtered.empty
            except Exception as err:
                raise ComponentError(
                    f"Error evaluating DataFrame condition '{condition}': {err}"
                ) from err

        elif isinstance(self.data, str):
            # For string data, check if condition is a substring
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
                    raise ValueError(f"Invalid condition format: {condition}")
                jsonpath_expr, expected_value = parts
                expected_value = expected_value.strip().strip("'\"")  # Remove quotes
                return jsonpath_expr.strip(), op, expected_value
        raise ValueError(f"No valid operator found in condition: {condition}")

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
            raise ValueError(f"Unsupported operator: {operator}")

    async def run(self):
        """
        Executes the appropriate component based on the conditions.
        """
        # Determine the component to execute
        selected_component = None
        for case in self._cases:
            if self._evaluate_condition(case["condition"]):
                selected_component = case["component"]
                break

        if not selected_component:
            # Use the default component if no case matches
            if not self._default:
                raise ComponentError(
                    "No matching case and no default component provided."
                )
            selected_component = self._default

        # Execute the selected component
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
        self._result = await self.exec_component(component_instance, step.name)
        # at the end, remove all tracked components from TaskPile to prevent future execution
        for component_name in self._tracked_components:
            self._TaskPile.delStepByName(component_name)
        return self._result
