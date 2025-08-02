from typing import Any
from orionis.container.exceptions import OrionisContainerTypeError

class __IsCallable:
    """
    Validator that checks if a value is callable.
    Can be used directly like a function: `IsCallable(value)`
    """

    def __call__(self, value: Any) -> None:
        """
        Ensures that the provided value is callable.

        Parameters
        ----------
        value : Any
            The value to check.

        Raises
        ------
        OrionisContainerTypeError
            If the value is not callable.
        """
        if not callable(value):
            raise OrionisContainerTypeError(
                f"Expected a callable type, but got {type(value).__name__} instead."
            )

# Exported singleton instance
IsCallable = __IsCallable()
