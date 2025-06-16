"""
    Helper class for utility parameters
"""

from typing import List, Dict, Literal, Optional

DYNAMIC_PARAMETER_TYPES = [
    "ScenariosList",
    "ScenariosMultiselectList",
    "MapsList",
    "AnalyticsList",
    "TablesList",
    "InputTablesList",
    "InputTablesMultiselectList",
    "OutputTablesList",
    "CustomTablesList",
    "ModelList",
    "TechnologyList",
]

DYNAMIC_ATTRIBUTES_PARAMETER_TYPES = [
    'TableColumnsList',
    'TableColumnUniqueValuesList'
]

POSSIBLE_TYPES = [
    "int",
    "double",
    "string",
] + DYNAMIC_PARAMETER_TYPES + DYNAMIC_ATTRIBUTES_PARAMETER_TYPES

# Note: Type can also be list of strings: [Option1, Option2] which requires the user to select

# Define a Literal type for param_type, which is restricted to all possible values
ParamType = Literal[
    "int", "double", "string",
    "ScenariosList", "MapsList", "AnalyticsList", "TablesList", "ScenariosMultiselectList",
    "InputTablesList", "OutputTablesList", "CustomTablesList", "InputTablesMultiselectList",
    "ModelList", "TechnologyList", "TableColumnsList", "TableColumnUniqueValuesList"
]

class Params:
    """
    A helper class to represent a set of parameters for a CF Model Function.

    Attributes
    ----------
    None

    Methods
    -------
    add - Adds a new parameter
    result - Returns all added parameters
    """

    def __init__(self, params: List | Dict = None):
        self.__params = []
        self.app_key = None

        # Note: No validation on params passed here, is responsibility of the running script to validate
        if params is not None:
            # Old utilities (list of values) - TO REMOVE WHEN UNUSED
            if isinstance(params, list):
                self.__loaded_params = params
                self.model_name = self.__loaded_params.pop(0)

            # New utilities (dict of values)
            if isinstance(params, dict):
                self.__loaded_params = params
                self.model_name = self.__loaded_params["model_name"]
                self.__loaded_params.remove("model_name")

    def __getitem__(self, index):
        return self.__loaded_params[index]

    def __is_valid_param_type(self, param_type: str) -> bool:
        if param_type in POSSIBLE_TYPES:
            return True

        if param_type.startswith("[") and param_type.endswith("]"):
            return True

        return False

    def add(self, name: str, description: str, default: any, param_type: str, dynamic_attributes: Optional[Dict[str, str]] = None) -> None:
        """Add a new parameter.

        Args:
            name: the name of the parameter to add.
            description: a user-friendly description of the parameter.
            default: default value of the parameter.
            param_type: the type of the parameter.
            dynamic_attributes: optional, required when param_type is in DYNAMIC_ATTRIBUTES_PARAMETER_TYPES.
                For "TableColumnsList", it must include "table".
                For "TableColumnUniqueValuesList", it must include "table" and "column".
        Returns:
            None.
        Raises:
            ValueError if the type does not validate as a type or if dynamic_attributes are missing or incomplete.
        """

        name = name.strip()
        description = description.strip()
        param_type = param_type.strip()

        if param_type not in DYNAMIC_PARAMETER_TYPES and param_type not in DYNAMIC_ATTRIBUTES_PARAMETER_TYPES and not param_type.startswith("["):
            param_type = param_type.lower()

        if not self.__is_valid_param_type(param_type):
            raise ValueError(f"Invalid param type: {param_type}")

        if param_type == "TableColumnsList":
            if not dynamic_attributes or "table" not in dynamic_attributes:
                raise ValueError(f"Missing required 'table' attribute for param type: {param_type}")
        elif param_type == "TableColumnUniqueValuesList":
            if not dynamic_attributes or "table" not in dynamic_attributes or "column" not in dynamic_attributes:
                raise ValueError(f"Missing required 'table' and 'column' attributes for param type: {param_type}")

        self.__params.append(
            {
                "Name": name,
                "Description": description,
                "Value": default,
                "Type": param_type,
                "Attributes": dynamic_attributes if dynamic_attributes else {},
            }
        )

    def result(self):
        """Returns the parameter list.

        Args:
            None.
        Returns:
            List of added parameters.
        """
        return self.__params
