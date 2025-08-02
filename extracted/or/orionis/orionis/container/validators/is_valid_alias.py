from typing import Any
from orionis.container.exceptions import OrionisContainerTypeError

class __IsValidAlias:
    """
    Validator that checks if a value is a valid alias string.
    """

    _INVALID_CHARS = set(' \t\n\r\x0b\x0c!@#$%^&*()[]{};:,/<>?\\|`~"\'')

    def __call__(self, value: Any) -> None:
        """
        Ensures that the provided value is a valid alias of type str and does not contain invalid characters.

        Parameters
        ----------
        value : Any
            The value to check.

        Raises
        ------
        OrionisContainerTypeError
            If the value is not of type str or contains invalid characters.
        """
        if value is None or value == "" or str(value).isspace():
            raise OrionisContainerTypeError(
                "Alias cannot be None, empty, or whitespace only."
            )

        if not isinstance(value, str):
            raise OrionisContainerTypeError(
                f"Expected a string type for alias, but got {type(value).__name__} instead."
            )

        if any(char in self._INVALID_CHARS for char in value):
            raise OrionisContainerTypeError(
                f"Alias '{value}' contains invalid characters. "
                "Aliases must not contain whitespace or special symbols."
            )

# Exported singleton instance
IsValidAlias = __IsValidAlias()