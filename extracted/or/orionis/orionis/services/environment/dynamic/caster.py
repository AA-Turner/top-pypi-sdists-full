from typing import Any
from orionis.services.environment.contracts.caster import IEnvironmentCaster
from orionis.services.environment.enums.value_type import EnvironmentValueType
from orionis.services.environment.exceptions import OrionisEnvironmentValueError, OrionisEnvironmentValueException

class EnvironmentCaster(IEnvironmentCaster):

    # Type class to handle different types of environment variables
    OPTIONS = {e.value for e in EnvironmentValueType}

    @staticmethod
    def options() -> set:
        """
        Get the set of valid type hints supported by this class.

        Returns
        -------
        set
            Set of valid type hint strings that can be used for environment value casting.
        """
        return EnvironmentCaster.OPTIONS

    def __init__(
        self,
        raw: str | Any
    ) -> None:
        """
        Parse the input `raw` to extract a type hint and value for environment variable casting.

        Parameters
        ----------
        raw : str or Any
            The input value to be parsed. If a string, it may contain a type hint and value
            separated by a colon (e.g., "int: 42"). If a colon is present, the part before
            the colon is treated as the type hint and the part after as the value. If no colon
            is present, the entire string is treated as the value with no type hint. If not a
            string, the input is treated as the value with no type hint.

        Attributes
        ----------
        __type_hint : str or None
            The extracted type hint in lowercase, or None if not provided or invalid.
        __value_raw : str or Any
            The extracted value string if input is a string, or the raw value otherwise.

        Notes
        -----
        This constructor does not return a value. It initializes the instance attributes
        for type hint and raw value, which are used for subsequent type casting operations.
        """

        # Initialize type hint and value to default None
        self.__type_hint: str = None
        self.__value_raw: str | Any = None

        # If the input is a string, attempt to parse type hint and value
        if isinstance(raw, str):

            # Remove leading whitespace from the input
            self.__value_raw = raw.lstrip()

            # Check if the string contains a colon, indicating a type hint
            if ':' in self.__value_raw:

                # Split at the first colon to separate type hint and value
                type_hint, value_str = raw.split(':', 1)

                # Validate the extracted type hint and set attributes if valid
                if type_hint.strip().lower() in self.OPTIONS:
                    self.__type_hint = type_hint.strip().lower()
                    # Remove leading whitespace from the value part
                    self.__value_raw = value_str.lstrip() if value_str else None
        else:

            # If input is not a string, treat it as the value with no type hint
            self.__value_raw = raw

    def get(self):
        """
        Returns the processed value based on the specified type hint.

        If a valid type hint is present, this method dispatches to the corresponding
        internal parsing method for that type. Supported type hints include: 'path',
        'str', 'int', 'float', 'bool', 'list', 'dict', 'tuple', 'set', and 'base64'.
        If no type hint is set, the raw value is returned as is.

        Returns
        -------
        Any
            The value converted or processed according to the specified type hint.
            If no type hint is set, returns the raw value.

        Raises
        ------
        OrionisEnvironmentValueError
            If an error occurs during type conversion or processing.
        """

        # Attempt to process the value based on the type hint
        try:

            # If a type hint is set, dispatch to the appropriate parsing method
            if self.__type_hint:

                # Handle 'path' type hint
                if self.__type_hint == EnvironmentValueType.PATH.value:
                    return self.__parsePath()

                # Handle 'str' type hint
                if self.__type_hint == EnvironmentValueType.STR.value:
                    return self.__parseStr()

                # Handle 'int' type hint
                if self.__type_hint == EnvironmentValueType.INT.value:
                    return self.__parseInt()

                # Handle 'float' type hint
                if self.__type_hint == EnvironmentValueType.FLOAT.value:
                    return self.__parseFloat()

                # Handle 'bool' type hint
                if self.__type_hint == EnvironmentValueType.BOOL.value:
                    return self.__parseBool()

                # Handle 'list' type hint
                if self.__type_hint == EnvironmentValueType.LIST.value:
                    return self.__parseList()

                # Handle 'dict' type hint
                if self.__type_hint == EnvironmentValueType.DICT.value:
                    return self.__parseDict()

                # Handle 'tuple' type hint
                if self.__type_hint == EnvironmentValueType.TUPLE.value:
                    return self.__parseTuple()

                # Handle 'set' type hint
                if self.__type_hint == EnvironmentValueType.SET.value:
                    return self.__parseSet()

                # Handle 'base64' type hint
                if self.__type_hint == EnvironmentValueType.BASE64.value:
                    return self.__parseBase64()

            else:

                # If no type hint is set, return the raw value
                return self.__value_raw

        except OrionisEnvironmentValueError:

            # Propagate specific type conversion errors
            raise

        except Exception as e:

            # Catch any other unexpected errors and wrap them in an environment value error
            raise OrionisEnvironmentValueError(
                f"Error processing value '{self.__value_raw}' with type hint '{self.__type_hint}': {str(e)}"
            ) from e

    def to(self, type_hint: str | EnvironmentValueType) -> Any:
        """
        Convert the internal value to the specified type and return its string representation
        with the type hint prefix.

        Parameters
        ----------
        type_hint : str or EnvironmentValueType
            The type to which the internal value should be converted. Can be a string or an
            EnvironmentValueType enum member. Must be one of the valid options in `OPTIONS`.

        Returns
        -------
        Any
            The string representation of the value with the type hint prefix, according to the
            specified type. For example, "int:42", "list:[1, 2, 3]", etc.

        Raises
        ------
        OrionisEnvironmentValueError
            If the provided type hint is not valid or if the value cannot be converted to the
            specified type.
        """

        # Validate the type hint and ensure it is one of the defined options
        try:

            # If type_hint is an enum, convert it to its value string
            if isinstance(type_hint, EnvironmentValueType):
                type_hint = type_hint.value

            # Validate the type hint against the defined options
            if type_hint not in self.OPTIONS:
                raise OrionisEnvironmentValueError(
                    f"Invalid type hint: {type_hint}. Must be one of {self.OPTIONS}."
                )

            # Set the type hint for the instance
            self.__type_hint = type_hint

            # Dispatch to the appropriate conversion method based on the type hint
            if self.__type_hint == EnvironmentValueType.PATH.value:
                return self.__toPath()

            # If the type hint is 'str', convert to string
            if self.__type_hint == EnvironmentValueType.STR.value:
                return self.__toStr()

            # If the type hint is 'int', convert to integer
            if self.__type_hint == EnvironmentValueType.INT.value:
                return self.__toInt()

            # If the type hint is 'float', convert to float
            if self.__type_hint == EnvironmentValueType.FLOAT.value:
                return self.__toFloat()

            # If the type hint is 'bool', convert to boolean
            if self.__type_hint == EnvironmentValueType.BOOL.value:
                return self.__toBool()

            # If the type hint is 'list', convert to list
            if self.__type_hint == EnvironmentValueType.LIST.value:
                return self.__toList()

            # If the type hint is 'dict', convert to dictionary
            if self.__type_hint == EnvironmentValueType.DICT.value:
                return self.__toDict()

            # If the type hint is 'tuple', convert to tuple
            if self.__type_hint == EnvironmentValueType.TUPLE.value:
                return self.__toTuple()

            # If the type hint is 'set', convert to set
            if self.__type_hint == EnvironmentValueType.SET.value:
                return self.__toSet()

            # If the type hint is 'base64', convert to Base64 encoded string
            if self.__type_hint == EnvironmentValueType.BASE64.value:
                return self.__toBase64()

        except OrionisEnvironmentValueError:

            # Propagate specific type conversion errors
            raise

        except Exception as e:

            # Catch any other unexpected errors and wrap them in an environment value error
            raise OrionisEnvironmentValueError(
                f"Error converting value '{self.__value_raw}' to type '{type_hint}': {str(e)}"
            ) from e

    def __toBase64(self) -> str:
        """
        Convert the internal value to a Base64 encoded string with the type hint prefix.

        - If the value is already valid base64, leave it as-is.
        - Otherwise, encode it to base64.

        Returns
        -------
        str
            A string in the format "<type_hint>:<base64_value>".
        """
        import base64

        if not isinstance(self.__value_raw, (str, bytes)):
            raise OrionisEnvironmentValueError(
                f"Value must be a string or bytes to convert to Base64, got {type(self.__value_raw).__name__} instead."
            )

        # Normalizar a str
        if isinstance(self.__value_raw, bytes):
            candidate = self.__value_raw.decode("utf-8", errors="ignore")
        else:
            candidate = self.__value_raw

        try:
            # Validar si ya es base64 válido
            base64.b64decode(candidate, validate=True)
            encoded_value = candidate
        except Exception:
            # No era base64, entonces convertirlo
            raw_bytes = (
                self.__value_raw.encode() if isinstance(self.__value_raw, str) else self.__value_raw
            )
            encoded_value = base64.b64encode(raw_bytes).decode("utf-8")

        return f"{self.__type_hint}:{encoded_value}"

    def __parseBase64(self) -> bytes:
        """
        Decode the internal raw value from Base64 encoding.

        Returns
        -------
        bytes
            The decoded raw bytes from the Base64-encoded internal value.

        Raises
        ------
        OrionisEnvironmentValueException
            If the internal value cannot be decoded from Base64.
        """
        import base64

        try:
            raw_value = self.__value_raw
            if isinstance(raw_value, bytes):
                raw_value = raw_value.decode("utf-8", errors="ignore")

            decoded = base64.b64decode(raw_value, validate=True)

            try:
                return decoded.decode("utf-8")
            except UnicodeDecodeError:
                return decoded

        except Exception as e:
            raise OrionisEnvironmentValueException(
                f"Cannot decode Base64 value '{self.__value_raw}': {str(e)}"
            )

    def __parsePath(self):
        """
        Convert the internal raw value to a normalized POSIX path string.

        This method processes the internal value as a file system path. If the value is already
        a `Path` object, it returns its POSIX representation. If the value is a string, it replaces
        backslashes with forward slashes for normalization and returns the POSIX path string.

        Returns
        -------
        str
            The normalized POSIX path string representing the file system path.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be processed as a valid path.
        """

        # Import the Path class from pathlib for path manipulation
        from pathlib import Path

        # If the value is already a Path object, return its POSIX representation
        if isinstance(self.__value_raw, Path):
            return self.__value_raw.as_posix()

        # Normalize the path by replacing backslashes with forward slashes
        normalized_path = str(self.__value_raw).replace('\\', '/')

        # Convert the normalized string to a Path object and return its POSIX representation
        return Path(normalized_path).as_posix()

    def __toPath(self) -> str:
        """
        Convert the internal value to an absolute POSIX path string with type hint prefix.

        Returns
        -------
        str
            A string in the format "<type_hint>:<absolute_path>", where <absolute_path> is the
            normalized, absolute POSIX path representation of the internal value.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a string or a pathlib.Path object.
        """

        # Import the Path class from pathlib for path manipulation
        from pathlib import Path

        # Ensure the internal value is a string or Path object
        if not isinstance(self.__value_raw, (str, Path)):
            raise OrionisEnvironmentValueError(
                f"Value must be a string or Path to convert to path, got {type(self.__value_raw).__name__} instead."
            )

        # Normalize slashes and strip whitespace from the path string
        raw_path = str(self.__value_raw).replace('\\', '/').strip()

        # Create a Path object from the normalized path string
        path_obj = Path(raw_path)

        # If the path is not absolute, resolve it relative to the current working directory
        if not path_obj.is_absolute():

            # Remove any leading slash to avoid creating an absolute path when joining
            raw_path_no_leading = raw_path.lstrip('/\\')

            # Combine with the current working directory to form an absolute path
            path_obj = Path(Path.cwd()) / raw_path_no_leading

        # Expand user home and convert to POSIX format for consistency
        abs_path = path_obj.expanduser().as_posix()

        # Return the absolute path as a string with the type hint prefix
        return f"{self.__type_hint}:{str(abs_path)}"

    def __parseStr(self):
        """
        Returns the internal raw value as a string, removing leading whitespace.

        Parameters
        ----------
        self : EnvironmentCaster
            Instance of the EnvironmentCaster class.

        Returns
        -------
        str
            The internal value as a string with leading whitespace removed.

        Notes
        -----
        No type conversion is performed; the value is returned as a string after
        stripping leading whitespace. This method assumes the type hint is 'str:'.
        No exceptions are raised by this method.
        """

        # Remove leading whitespace from the internal value
        # This ensures that any accidental spaces before the value are ignored
        return self.__value_raw.lstrip()

    def __toStr(self):
        """
        Returns the internal value as a string representation with the type hint prefix.

        Returns
        -------
        str
            The string representation of the internal value, prefixed by the type hint and separated by a colon.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a string.
        """

        # Ensure the internal value is a string before conversion
        if not isinstance(self.__value_raw, str):

            # Raise an error if the value is not a string
            raise OrionisEnvironmentValueError(
                f"Value must be a string to convert to str, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and value
        return f"{self.__type_hint}:{self.__value_raw}"

    def __parseInt(self):
        """
        Convert the internal raw value to an integer.

        Strips leading and trailing whitespace from the internal raw value and attempts to convert it to an integer.
        Raises an OrionisEnvironmentValueException if the conversion fails due to invalid format or type.

        Returns
        -------
        int
            The internal value converted to an integer.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to an integer due to invalid format or type.
        """

        # Remove leading and trailing whitespace from the raw value
        value = self.__value_raw.strip()

        # Attempt to convert the value to an integer
        try:
            return int(value)
        # Raise a custom exception if conversion fails
        except ValueError as e:
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to int: {str(e)}")

    def __toInt(self):
        """
        Converts the internal value to a string representation with the integer type hint prefix.

        Returns
        -------
        str
            String in the format "<type_hint>:<value>", where <type_hint> is the current type hint
            and <value> is the integer value.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not an integer.
        """

        # Check if the internal value is an integer before conversion
        if not isinstance(self.__value_raw, int):

            # Raise an error if the value is not an integer
            raise OrionisEnvironmentValueError(
                f"Value must be an integer to convert to int, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and integer value
        return f"{self.__type_hint}:{str(self.__value_raw)}"

    def __parseFloat(self):
        """
        Convert the internal raw value to a float.

        Strips leading and trailing whitespace from the internal raw value and attempts to convert it to a float.
        Raises an OrionisEnvironmentValueException if the conversion fails due to invalid format or type.

        Returns
        -------
        float
            The internal value converted to a float.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a float due to invalid format or type.
        """

        # Remove leading and trailing whitespace from the raw value to ensure clean input
        value = self.__value_raw.strip()

        # Attempt to convert the value to a float
        try:
            return float(value)

        # Raise a custom exception if conversion fails
        except ValueError as e:
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to float: {str(e)}")

    def __toFloat(self):
        """
        Converts the internal value to a string representation with the float type hint prefix.

        Returns
        -------
        str
            A string in the format "<type_hint>:<value>", where <type_hint> is the current type hint
            and <value> is the float value.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a float.
        """

        # Ensure the internal value is a float before conversion
        if not isinstance(self.__value_raw, float):

            # Raise an error if the value is not a float
            raise OrionisEnvironmentValueError(
                f"Value must be a float to convert to float, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and float value
        return f"{self.__type_hint}:{str(self.__value_raw)}"

    def __parseBool(self):
        """
        Convert the internal raw value to a boolean.

        This method strips leading and trailing whitespace from the internal raw value,
        converts it to lowercase, and checks if it matches 'true' or 'false'. If the value
        is 'true', it returns True. If the value is 'false', it returns False. If the value
        does not match either, an OrionisEnvironmentValueException is raised.

        Returns
        -------
        bool
            True if the value is 'true' (case-insensitive), False if the value is 'false' (case-insensitive).

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a boolean because it does not match 'true' or 'false'.
        """

        # Remove leading and trailing whitespace, then convert to lowercase for comparison
        value = self.__value_raw.strip().lower()

        # If the value is 'true', return True
        if value == 'true':
            return True

        # If the value is 'false', return False
        elif value == 'false':
            return False

        # If the value is neither 'true' nor 'false', raise an exception
        else:
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to bool.")

    def __toBool(self):
        """
        Convert the internal value to a string representation with the boolean type hint prefix.

        Returns
        -------
        str
            A string in the format "<type_hint>:<value>", where <type_hint> is the current type hint
            and <value> is the lowercase string representation of the boolean value ('true' or 'false').

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a boolean.
        """

        # Ensure the internal value is a boolean before conversion
        if not isinstance(self.__value_raw, bool):

            # Raise an error if the value is not a boolean
            raise OrionisEnvironmentValueError(
                f"Value must be a boolean to convert to bool, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and boolean value in lowercase
        return f"{self.__type_hint}:{str(self.__value_raw).lower()}"

    def __parseList(self):
        """
        Parses the internal raw value and converts it to a Python list.

        The method strips leading and trailing whitespace from the internal raw value,
        then attempts to safely evaluate the string as a Python list using `ast.literal_eval`.
        If the conversion is successful and the result is a list, it is returned.
        If the conversion fails or the evaluated value is not a list, an
        `OrionisEnvironmentValueException` is raised.

        Returns
        -------
        list
            The internal value converted to a list.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a list due to invalid format or type.
        """

        # Import the ast module for safe evaluation of string literals
        import ast

        # Remove leading and trailing whitespace from the raw value to ensure clean input
        value = self.__value_raw.strip()

        try:

            # Safely evaluate the string to a Python object using ast.literal_eval
            parsed = ast.literal_eval(value)

            # Ensure the evaluated object is a list
            if not isinstance(parsed, list):
                raise ValueError("Value is not a list")

            # Return the parsed list if successful
            return parsed

        except (ValueError, SyntaxError) as e:

            # Raise a custom exception if conversion fails
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to list: {str(e)}")

    def __toList(self):
        """
        Converts the internal value to its string representation with the list type hint prefix.

        Parameters
        ----------
        self : EnvironmentCaster
            Instance of the EnvironmentCaster class.

        Returns
        -------
        str
            A string in the format "<type_hint>:<value>", where <type_hint> is the current type hint
            and <value> is the string representation of the list.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a list.
        """

        # Ensure the internal value is a list before conversion
        if not isinstance(self.__value_raw, list):

            # Raise an error if the value is not a list
            raise OrionisEnvironmentValueError(
                f"Value must be a list to convert to list, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and list value
        return f"{self.__type_hint}:{repr(self.__value_raw)}"

    def __parseDict(self):
        """
        Parses the internal raw value and converts it to a Python dictionary.

        The method strips leading and trailing whitespace from the internal raw value,
        then attempts to safely evaluate the string as a Python dictionary using
        `ast.literal_eval`. If the conversion is successful and the result is a dictionary,
        it is returned. If the conversion fails or the evaluated value is not a dictionary,
        an OrionisEnvironmentValueException is raised.

        Returns
        -------
        dict
            The internal value converted to a dictionary.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a dictionary due to invalid format or type.
        """

        # Import the ast module for safe evaluation of string literals
        import ast

        # Remove leading and trailing whitespace from the raw value to ensure clean input
        value = self.__value_raw.strip()

        # Attempt to parse the string as a dictionary
        try:

            # Safely evaluate the string to a Python object using ast.literal_eval
            parsed = ast.literal_eval(value)

            # Ensure the evaluated object is a dictionary
            if not isinstance(parsed, dict):
                raise ValueError("Value is not a dict")

            # Return the parsed dictionary if successful
            return parsed

        except (ValueError, SyntaxError) as e:

            # Raise a custom exception if conversion fails
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to dict: {str(e)}")

    def __toDict(self):
        """
        Converts the internal value to a string representation with the dictionary type hint prefix.

        Returns
        -------
        str
            A string in the format "<type_hint>:<value>", where <type_hint> is the current type hint
            and <value> is the string representation of the dictionary.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a dictionary.
        """

        # Ensure the internal value is a dictionary before conversion
        if not isinstance(self.__value_raw, dict):

            # Raise an error if the value is not a dictionary
            raise OrionisEnvironmentValueError(
                f"Value must be a dict to convert to dict, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and dictionary value
        return f"{self.__type_hint}:{repr(self.__value_raw)}"

    def __parseTuple(self):
        """
        Parse the internal raw value and convert it to a Python tuple.

        The method removes leading and trailing whitespace from the internal raw value,
        then attempts to safely evaluate the string as a Python tuple using `ast.literal_eval`.
        If the conversion is successful and the result is a tuple, it is returned.
        If the conversion fails or the evaluated value is not a tuple, an
        OrionisEnvironmentValueException is raised.

        Returns
        -------
        tuple
            The internal value converted to a tuple.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a tuple due to invalid format or type.
        """

        # Import the ast module for safe evaluation of string literals
        import ast

        # Remove leading and trailing whitespace from the raw value to ensure clean input
        value = self.__value_raw.strip()

        try:

            # Safely evaluate the string to a Python object using ast.literal_eval
            parsed = ast.literal_eval(value)

            # Ensure the evaluated object is a tuple
            if not isinstance(parsed, tuple):
                raise ValueError("Value is not a tuple")

            # Return the parsed tuple if successful
            return parsed

        except (ValueError, SyntaxError) as e:

            # Raise a custom exception if conversion fails
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to tuple: {str(e)}")

    def __toTuple(self):
        """
        Convert the internal value to a string representation with the tuple type hint prefix.

        Returns
        -------
        str
            A string in the format "<type_hint>:<value>", where <type_hint> is the current type hint
            and <value> is the string representation of the tuple.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a tuple.
        """

        # Ensure the internal value is a tuple before conversion
        if not isinstance(self.__value_raw, tuple):

            # Raise an error if the value is not a tuple
            raise OrionisEnvironmentValueError(
                f"Value must be a tuple to convert to tuple, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and tuple value
        return f"{self.__type_hint}:{repr(self.__value_raw)}"

    def __parseSet(self):
        """
        Parse the internal raw value and convert it to a Python set.

        This method removes leading and trailing whitespace from the internal raw value,
        then attempts to safely evaluate the string as a Python set using `ast.literal_eval`.
        If the conversion is successful and the result is a set, it is returned.
        If the conversion fails or the evaluated value is not a set, an
        OrionisEnvironmentValueException is raised.

        Returns
        -------
        set
            The internal value converted to a set.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a set due to invalid format or type.
        """

        # Import the ast module for safe evaluation of string literals
        import ast

        # Remove leading and trailing whitespace from the raw value to ensure clean input
        value = self.__value_raw.strip()

        try:

            # Safely evaluate the string to a Python object using ast.literal_eval
            parsed = ast.literal_eval(value)

            # Ensure the evaluated object is a set
            if not isinstance(parsed, set):
                raise ValueError("Value is not a set")

            # Return the parsed set if successful
            return parsed

        except (ValueError, SyntaxError) as e:

            # Raise a custom exception if conversion fails
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to set: {str(e)}")

    def __toSet(self):
        """
        Convert the internal value to a string representation with the set type hint prefix.

        Returns
        -------
        str
            A string in the format "<type_hint>:<value>", where <type_hint> is the current type hint
            and <value> is the string representation of the set.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a set.
        """

        # Ensure the internal value is a set before conversion
        if not isinstance(self.__value_raw, set):
            # Raise an error if the value is not a set
            raise OrionisEnvironmentValueError(
            f"Value must be a set to convert to set, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and set value
        return f"{self.__type_hint}:{repr(self.__value_raw)}"
