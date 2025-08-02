from typing import Any, Union
from orionis.container.enums.lifetimes import Lifetime
from orionis.container.exceptions import OrionisContainerTypeError

class __LifetimeValidator:
    """
    Validator that checks if a value is a valid lifetime and converts string representations
    to Lifetime enum values.
    """

    def __call__(self, lifetime: Union[str, Lifetime, Any]) -> Lifetime:
        """
        Validates and normalizes the provided lifetime value.

        Parameters
        ----------
        lifetime : Union[str, Lifetime, Any]
            The lifetime value to validate. Can be a Lifetime enum or a string
            representing a valid lifetime.

        Returns
        -------
        Lifetime
            The validated Lifetime enum value.

        Raises
        ------
        OrionisContainerTypeError
            If the value is not a valid Lifetime enum or string representation,
            or if the string doesn't match any valid Lifetime value.
        """
        # Already a Lifetime enum
        if isinstance(lifetime, Lifetime):
            return lifetime

        # String that might represent a Lifetime
        if isinstance(lifetime, str):
            lifetime_key = lifetime.strip().upper()
            if lifetime_key in Lifetime.__members__:
                return Lifetime[lifetime_key]

            valid_options = ', '.join(Lifetime.__members__.keys())
            raise OrionisContainerTypeError(
                f"Invalid lifetime '{lifetime}'. Valid options are: {valid_options}."
            )

        # Invalid type
        raise OrionisContainerTypeError(
            f"Lifetime must be of type str or Lifetime enum, got {type(lifetime).__name__}."
        )

# Exported singleton instance
LifetimeValidator = __LifetimeValidator()