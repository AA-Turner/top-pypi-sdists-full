import os
import ast
import threading
from pathlib import Path
from typing import Any, Optional, Union
from dotenv import dotenv_values, load_dotenv, set_key, unset_key
from orionis.services.environment.enums import EnvironmentValueType
from orionis.services.environment.exceptions.environment import OrionisEnvironmentException, OrionisOperatingSystemError
from orionis.services.environment.validators import ValidateKeyName, ValidateTypes
from orionis.support.patterns.singleton import Singleton
from orionis.services.environment.dynamic.caster import EnvironmentCaster

class DotEnv(metaclass=Singleton):

    # Thread-safe singleton instance lock
    _lock = threading.RLock()

    def __init__(
        self,
        path: str = None
    ) -> None:
        """
        Initialize the DotEnv service and prepare the `.env` file for environment variable management.

        Parameters
        ----------
        path : str, optional
            Path to the `.env` file. If not provided, defaults to `.env` in the current working directory.

        Raises
        ------
        OSError
            If the `.env` file cannot be created or accessed.

        Notes
        -----
        Ensures thread safety during initialization. If the specified `.env` file does not exist, it is created.
        Loads environment variables from the `.env` file into the process environment.
        """

        try:

            # Ensure thread-safe initialization to avoid race conditions
            with self._lock:

                # Set the default .env file path to the current working directory
                self.__resolved_path = Path(os.getcwd()) / ".env"

                # If a custom path is provided, resolve and use it
                if path:
                    self.__resolved_path = Path(path).expanduser().resolve()

                # Create the .env file if it does not exist
                if not self.__resolved_path.exists():
                    self.__resolved_path.touch()

                # Load environment variables from the .env file into the process environment
                load_dotenv(self.__resolved_path)

        except OSError as e:

            # Raise an error if the .env file cannot be created or accessed
            raise OrionisOperatingSystemError(f"Failed to create or access the .env file at {self.__resolved_path}: {e}")

        except Exception as e:

            # Raise a general error for any other exceptions during initialization
            raise OrionisEnvironmentException(f"An unexpected error occurred while initializing DotEnv: {e}")

    def set(
        self,
        key: str,
        value: Union[str, int, float, bool, list, dict, tuple, set],
        type_hint: str | EnvironmentValueType = None
    ) -> bool:
        """
        Set an environment variable in both the `.env` file and the current process environment.

        Parameters
        ----------
        key : str
            The name of the environment variable to set. Must be a valid environment variable name.
        value : str, int, float, bool, list, dict, tuple, or set
            The value to assign to the environment variable.
        type_hint : str or EnvironmentValueType, optional
            An explicit type hint to guide the serialization of the value.

        Returns
        -------
        bool
            True if the environment variable was successfully set.

        Raises
        ------
        OrionisEnvironmentValueError
            If the provided key is not a valid environment variable name.

        Notes
        -----
        This method ensures thread safety during the set operation. It validates the key name,
        serializes the value (optionally using a type hint), writes the variable to the `.env` file,
        and updates the variable in the current process environment.
        """

        # Ensure thread-safe operation during the set process.
        with self._lock:

            # Validate the environment variable key name.
            __key = ValidateKeyName(key)

            # If a type hint is provided, validate and serialize the value accordingly.
            if type_hint is not None:

                # Validate the value against the provided type hint.
                __type = ValidateTypes(value, type_hint)

                # Serialize the value using the validated type.
                __value = self.__serializeValue(value, __type)

            else:

                # Serialize the value without a type hint.
                __value = self.__serializeValue(value)

            # Set the environment variable in the .env file.
            set_key(self.__resolved_path, __key, __value)

            # Update the environment variable in the current process environment.
            os.environ[__key] = __value

            # Indicate successful operation.
            return True

    def get(
        self,
        key: str,
        default: Optional[Any] = None
    ) -> Any:
        """
        Retrieve the value of an environment variable.

        Parameters
        ----------
        key : str
            Name of the environment variable to retrieve.
        default : Any, optional
            Value to return if the key is not found. Default is None.

        Returns
        -------
        Any
            Parsed value of the environment variable, or `default` if not found.

        Raises
        ------
        OrionisEnvironmentValueError
            If `key` is not a string.
        """

        # Ensure thread-safe operation while retrieving the environment variable.
        with self._lock:

            # Ensure the key is a string.
            __key = ValidateKeyName(key)

            # Get the value from the .env file or the current environment.
            value = dotenv_values(self.__resolved_path).get(__key)

            # If the value is not found in the .env file, check the current environment variables.
            if value is None:
                value = os.getenv(__key)

            # Parse the value using the internal __parseValue method and return it
            return self.__parseValue(value) if value is not None else default

    def unset(self, key: str) -> bool:
        """
        Remove an environment variable from both the `.env` file and the current process environment.

        Parameters
        ----------
        key : str
            Name of the environment variable to remove.

        Returns
        -------
        bool
            True if the environment variable was successfully removed.

        Raises
        ------
        OrionisEnvironmentValueError
            If the provided key is not a valid environment variable name.

        Notes
        -----
        If the environment variable does not exist, the method has no effect and returns True.
        """

        # Ensure thread-safe operation during the unset process.
        with self._lock:

            # Validate the environment variable key name.
            validated_key = ValidateKeyName(key)

            # Remove the key from the .env file.
            unset_key(self.__resolved_path, validated_key)

            # Remove the key from the current process environment, if present.
            os.environ.pop(validated_key, None)

            # Indicate successful operation.
            return True

    def all(self) -> dict:
        """
        Retrieve all environment variables from the resolved `.env` file as a dictionary.

        Returns
        -------
        dict
            Dictionary where each key is an environment variable name (str) and each value
            is the parsed Python representation of the variable.

        Notes
        -----
        Only variables present in the `.env` file are returned; variables set only in the
        process environment are not included.
        """

        # Ensure thread-safe operation while reading and parsing environment variables.
        with self._lock:

            # Read all raw key-value pairs from the .env file
            raw_values = dotenv_values(self.__resolved_path)

            # Parse each value and return as a dictionary
            return {k: self.__parseValue(v) for k, v in raw_values.items()}

    def __serializeValue(
        self,
        value: Any,
        type_hint: str | EnvironmentValueType = None
    ) -> str:
        """
        Serialize a Python value into a string suitable for storage in a .env file.

        Parameters
        ----------
        value : Any
            Value to serialize. Supported types include None, str, int, float, bool,
            list, dict, tuple, and set.
        type_hint : str or EnvironmentValueType, optional
            Explicit type hint to guide serialization.

        Returns
        -------
        str
            Serialized string representation of the input value, suitable for storage
            in a .env file. Returns "null" for None values.
        """

        # Handle None values explicitly
        if value is None:
            return "null"

        # If a type hint is provided, use EnvTypes for serialization
        if type_hint:

            # Use EnvironmentCaster to handle type hints
            return EnvironmentCaster(value).to(type_hint)

        else:

            # Serialize strings by stripping whitespace
            if isinstance(value, str):
                return value.strip()

            # Serialize booleans as lowercase strings ("true" or "false")
            if isinstance(value, bool):
                return str(value).lower()

            # Serialize integers and floats as strings
            if isinstance(value, (int, float)):
                return str(value)

            # Serialize collections (list, dict, tuple, set) using repr
            if isinstance(value, (list, dict, tuple, set)):
                return repr(value)

        # Fallback: convert any other type to string
        return str(value)

    def __parseValue(
        self,
        value: Any
    ) -> Any:
        """
        Parse a string or raw value from the .env file into its appropriate Python type.

        Parameters
        ----------
        value : Any
            Value to parse, typically a string read from the .env file, but may also be a Python object.

        Returns
        -------
        Any
            Parsed Python value. Returns `None` for recognized null representations, a boolean for
            "true"/"false" strings, a Python literal (list, dict, int, etc.) if possible, or the original
            string if no conversion is possible.

        Notes
        -----
        Recognizes 'none', 'null', 'nan', 'nil' (case-insensitive) as null values.
        Attempts to use `EnvironmentCaster` for advanced type parsing.
        Falls back to `ast.literal_eval` for literal evaluation.
        Returns the original string if all parsing attempts fail.
        """

        # Early return for None values
        if value is None:
            return None

        # Return immediately if already a basic Python type
        if isinstance(value, (bool, int, float, dict, list, tuple, set)):
            return value

        # Convert the value to string for further processing
        value_str = str(value)

        # Handle empty strings and common null representations
        # This includes 'none', 'null', 'nan', 'nil' (case-insensitive)
        if not value_str or value_str.lower().strip() in {'none', 'null', 'nan', 'nil'}:
            return None

        # Boolean detection for string values (case-insensitive)
        lower_val = value_str.lower().strip()
        if lower_val in ('true', 'false'):
            return lower_val == 'true'

        # Attempt to parse using EnvironmentCaster for advanced types
        # Try to detect if the value string starts with a known EnvironmentValueType prefix
        env_type_prefixes = {str(e.value) for e in EnvironmentValueType}
        if any(value_str.startswith(prefix) for prefix in env_type_prefixes):
            return EnvironmentCaster(value_str).get()

        # Attempt to parse using ast.literal_eval for Python literals
        try:
            return ast.literal_eval(value_str)

        # Return the original string if parsing fails
        except (ValueError, SyntaxError):
            return value_str
