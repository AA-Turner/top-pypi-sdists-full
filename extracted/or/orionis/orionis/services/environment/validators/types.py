from typing import Union
from orionis.services.environment.enums.value_type import EnvironmentValueType
from orionis.services.environment.exceptions import OrionisEnvironmentValueError

class __ValidateTypes:

    def __call__(self, value: Union[str, int, float, bool, list, dict, tuple, set], type_hint: str | EnvironmentValueType = None) -> str:
        """
        Validates and determines the type of a given value, optionally using a provided type hint.

        Parameters
        ----------
        value : str, int, float, bool, list, dict, tuple, or set
            The value whose type is to be validated and determined.
        type_hint : str or EnvironmentValueType, optional
            An optional type hint specifying the expected type. Can be a string or an EnvironmentValueType.

        Returns
        -------
        str
            The determined type as a string, either from the type hint or inferred from the value.

        Raises
        ------
        OrionisEnvironmentValueError
            If the value is not of a supported type or if the type hint is invalid.
        """
        # Ensure the value is a valid type.
        if not isinstance(value, (str, int, float, bool, list, dict, tuple, set)):
            raise OrionisEnvironmentValueError(
                f"Unsupported value type: {type(value).__name__}. Allowed types are str, int, float, bool, list, dict, tuple, set."
            )

        # If a type hint is provided, ensure it is valid.
        if type_hint and not isinstance(type_hint, (str, EnvironmentValueType)):
            raise OrionisEnvironmentValueError(
                f"Type hint must be a string or EnvironmentValueType, got {type(type_hint).__name__}."
            )

        # If type_hint is provided, convert it to a string if it's an EnvironmentValueType.
        if type_hint:

            # If type_hint is a string, convert it to EnvironmentValueType if valid.
            try:
                if isinstance(type_hint, str):
                    type_hint = EnvironmentValueType[type_hint.upper()].value
                elif isinstance(type_hint, EnvironmentValueType):
                    type_hint = type_hint.value

            # If type_hint is not a valid EnvironmentValueType, raise an error.
            except KeyError:
                raise OrionisEnvironmentValueError(
                    f"Invalid type hint: {type_hint}. Allowed types are: {[e.value for e in EnvironmentValueType]}"
                )

        # If no type hint is provided, use the type of the value.
        else:
            type_hint = type(value).__name__.lower()

        # Return the type hint as a string.
        return type_hint


# Instance to be used for key name validation
ValidateTypes = __ValidateTypes()