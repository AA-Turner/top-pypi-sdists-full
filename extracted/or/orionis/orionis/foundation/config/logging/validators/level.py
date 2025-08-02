from typing import Any
from orionis.foundation.config.logging.enums import Level
from orionis.foundation.exceptions import OrionisIntegrityException

class _IsValidLevel:
    """
    Validator that checks if a value is a valid logging level.
    Accepts int, str, or Level enum.
    """

    _level_names = {level.name for level in Level}
    _level_values = {level.value for level in Level}

    def __call__(self, value: Any) -> None:
        """
        Validate the provided logging level value.
        Parameters
        ----------
        value : Any
            The value to validate as a logging level. Can be an integer, string, or Level enum instance.
        Raises
        ------
        OrionisIntegrityException
            If the value is not a valid logging level or not of an accepted type (int, str, or Level).
        Notes
        -----
        - If `value` is an integer, it must be present in `self._level_values`.
        - If `value` is a string, it is stripped, uppercased, and must be present in `self._level_names`.
        - If `value` is a Level enum instance, it is accepted as valid.
        """
        if isinstance(value, Level):
            return

        if isinstance(value, int):
            if value not in self._level_values:
                raise OrionisIntegrityException(
                    f"'level' must be one of {sorted(self._level_values)}, got {value}."
                )
            return

        if isinstance(value, str):
            name = value.strip().upper()
            if name not in self._level_names:
                raise OrionisIntegrityException(
                    f"'level' must be one of {sorted(self._level_names)}, got '{value}'."
                )
            return

        raise OrionisIntegrityException(
            f"'level' must be int, str, or Level enum, got {type(value).__name__}."
        )

# Exported singleton instance
IsValidLevel = _IsValidLevel()
