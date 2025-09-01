import re
from orionis.services.environment.exceptions import OrionisEnvironmentValueError

class __ValidateKeyName:

    # Regular expression pattern to match valid environment variable names
    _pattern = re.compile(r'^[A-Z][A-Z0-9_]*$')

    def __call__(self, key: object) -> str:
        """
        Validates that the provided environment variable name is a string and matches the required format.

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

        # Ensure the key is of type string
        if not isinstance(key, str):
            raise OrionisEnvironmentValueError(
                f"Environment variable name must be a string, got {type(key).__name__}."
            )

        # Check if the key matches the required pattern for environment variable names
        if not self._pattern.fullmatch(key):
            raise OrionisEnvironmentValueError(
                f"Invalid environment variable name '{key}'. It must start with an uppercase letter, "
                "contain only uppercase letters, numbers, or underscores. Example: 'MY_ENV_VAR'."
            )

        # Return the validated key if all checks pass
        return key

# Instance to be used for key name validation
ValidateKeyName = __ValidateKeyName()
