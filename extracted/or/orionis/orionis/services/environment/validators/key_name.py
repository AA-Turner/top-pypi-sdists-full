import re
from orionis.services.environment.exceptions.value import OrionisEnvironmentValueError

class __ValidateKeyName:

    # Regular expression pattern to match valid environment variable names
    _pattern = re.compile(r'^[A-Z][A-Z0-9_]*$')

    def __call__(self, key: object) -> str:
        """
        Validates that the provided environment variable name meets the required format.

        Parameters
        ----------
        key : object
            The environment variable name to validate.

        Returns
        -------
        str
            The validated environment variable name if it meets the format requirements.

        Raises
        ------
        OrionisEnvironmentValueError
            If the provided key is not a string or does not match the required format.
        """

        # Check if the key is a string
        if not isinstance(key, str):
            raise OrionisEnvironmentValueError(
                f"Environment variable name must be a string, got {type(key).__name__}."
            )

        # Validate the key against the pattern
        if not self._pattern.fullmatch(key):
            raise OrionisEnvironmentValueError(
                f"Invalid environment variable name '{key}'. It must start with an uppercase letter, "
                "contain only uppercase letters, numbers, or underscores. Example: 'MY_ENV_VAR'."
            )

        # Return the validated key
        return key

# Instance to be used for key name validation
ValidateKeyName = __ValidateKeyName()