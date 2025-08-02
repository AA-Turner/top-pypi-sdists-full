
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
        Returns the set of valid type hints that can be used with this Type class.

        Returns
        -------
        set
            A set containing the valid type hints.
        """
        return EnvironmentCaster.OPTIONS

    def __init__(
        self,
        raw: str | Any
    ) -> None:
        """
        Initializes an EnvTypes instance by parsing a raw input into a type hint and value.

        Parameters
        ----------
        raw : str or Any
            The input to be parsed. If a string, it may contain a type hint and value separated by a colon
            (e.g., "int: 42"). If a colon is present, the part before the colon is treated as the type hint
            and the part after as the value. If no colon is present, the entire string is treated as the value
            with no type hint. If not a string, the input is treated as the value with no type hint.

        Attributes
        ----------
        __type_hint : str or None
            The extracted type hint in lowercase, or None if not provided or invalid.
        __value_raw : str or Any
            The extracted value string if input is a string, or the raw value otherwise.

        Returns
        -------
        None
            This constructor does not return a value. It initializes the instance attributes.
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
        Retrieves the value processed according to the specified type hint.

        This method checks if a valid type hint is present and dispatches the call to the
        corresponding internal parsing method for that type. Supported type hints include:
        'path', 'str', 'int', 'float', 'bool', 'list', 'dict', 'tuple', and 'set'.
        If no type hint is set, the raw value is returned as is.

        Returns
        -------
        Any
            The value converted or processed according to the specified type hint. If no type hint
            is set, returns the raw value.

        Raises
        ------
        OrionisEnvironmentValueError
            If the type hint is not one of the supported options.
        """

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
        Converts the internal value to the specified type and returns its string representation with the type hint prefix.

        This method sets the type hint for the instance and attempts to convert the internal value to the specified type.
        The type hint must be one of the valid options defined in `OPTIONS`. If the conversion is successful, a string
        representation of the value prefixed with the type hint is returned. If the type hint is invalid or the conversion
        fails, an exception is raised.

        Parameters
        ----------
        type_hint : str or EnvironmentValueType
            The type hint to set. Can be a string or an `EnvironmentValueType` enum member. Must be one of the valid options.

        Returns
        -------
        Any
            The string representation of the value with the type hint prefix, according to the specified type.
            For example, "int:42", "list:[1, 2, 3]", etc.

        Raises
        ------
        OrionisEnvironmentValueError
            If the provided type hint is not valid or if the value cannot be converted to the specified type.
        """
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
            if self.__type_hint == EnvironmentValueType.STR.value:
                return self.__toStr()
            if self.__type_hint == EnvironmentValueType.INT.value:
                return self.__toInt()
            if self.__type_hint == EnvironmentValueType.FLOAT.value:
                return self.__toFloat()
            if self.__type_hint == EnvironmentValueType.BOOL.value:
                return self.__toBool()
            if self.__type_hint == EnvironmentValueType.LIST.value:
                return self.__toList()
            if self.__type_hint == EnvironmentValueType.DICT.value:
                return self.__toDict()
            if self.__type_hint == EnvironmentValueType.TUPLE.value:
                return self.__toTuple()
            if self.__type_hint == EnvironmentValueType.SET.value:
                return self.__toSet()
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
        Converts the internal value to a Base64 encoded string with the type hint prefix.

        This method checks if the internal value is a string or bytes. If so, it encodes the value in Base64
        and returns a string in the format "<type_hint>:<base64_value>". If the internal value is not a string
        or bytes, an exception is raised.

        Returns
        -------
        str
            A Base64 encoded string combining the type hint and the internal value, separated by a colon.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a string or bytes.
        """
        import base64

        if not isinstance(self.__value_raw, (str, bytes)):
            raise OrionisEnvironmentValueError(
                f"Value must be a string or bytes to convert to Base64, got {type(self.__value_raw).__name__} instead."
            )

        # Encode the value in Base64
        encoded_value = base64.b64encode(str(self.__value_raw).encode()).decode()

        # Return the formatted string with type hint and Base64 encoded value
        return f"{self.__type_hint}:{encoded_value}"

    def __parseBase64(self) -> str:
        """
        Decodes the Base64 encoded value, assuming the type hint is 'base64:'.

        This method decodes the internal raw value from Base64 and returns it as a string.
        If the value cannot be decoded, an `OrionisEnvironmentValueException` is raised.

        Returns
        -------
        str
            The decoded Base64 value as a string.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be decoded from Base64.
        """
        import base64

        try:
            # Decode the Base64 encoded value
            decoded_value = base64.b64decode(self.__value_raw).decode()
            return decoded_value
        except Exception as e:
            raise OrionisEnvironmentValueException(f"Cannot decode Base64 value '{self.__value_raw}': {str(e)}")

    def __parsePath(self):
        """
        Converts the internal raw value to a `Path` object, assuming the type hint is 'path:'.

        This method processes the internal value as a file system path. It replaces backslashes
        with forward slashes for normalization and returns a `Path` object representing the path.

        Parameters
        ----------
        self : EnvironmentCaster
            The instance of the EnvironmentCaster class.

        Returns
        -------
        pathlib.Path
            A `Path` object representing the normalized file system path.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be processed as a valid path.
        """
        from pathlib import Path

        # If the value is already a Path object, return it directly
        if isinstance(self.__value_raw, Path):
            return self.__value_raw.as_posix()

        # Normalize the path by replacing backslashes with forward slashes
        normalized_path = str(self.__value_raw).replace('\\', '/')

        # Avoid redundant wrapping: if normalized_path is already absolute, just return Path(normalized_path)
        return Path(normalized_path).as_posix()

    def __toPath(self) -> str:
        """
        Converts the internal value to an absolute path string.

        Returns
        -------
        str
            A string representing the type hint and the absolute path value.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a string or Path.
        """
        from pathlib import Path
        import os

        if not isinstance(self.__value_raw, (str, Path)):
            raise OrionisEnvironmentValueError(
            f"Value must be a string or Path to convert to path, got {type(self.__value_raw).__name__} instead."
            )

        # Normalize slashes and strip whitespace
        raw_path = str(self.__value_raw).replace('\\', '/').strip()

        # If the path is relative, resolve it from the current working directory
        path_obj = Path(raw_path)

        # If the path is not absolute, make it absolute by combining with the current working directory
        if not path_obj.is_absolute():

            # Remove leading slash if present to avoid absolute path when joining
            raw_path_no_leading = raw_path.lstrip('/\\')
            path_obj = Path(Path.cwd()) / raw_path_no_leading

        # Resolve the path to get the absolute path
        abs_path = path_obj.expanduser().as_posix()

        # Return the absolute path as a string with the type hint
        return f"{self.__type_hint}:{str(abs_path)}"

    def __parseStr(self):
        """
        Returns the value as a string, assuming the type hint is 'str:'.

        This method processes the internal raw value and returns it as a string,
        provided the type hint is 'str:'. Leading whitespace is removed from the value
        before returning. No type conversion is performed; the value is returned as-is
        after stripping leading whitespace.

        Returns
        -------
        str
            The internal value as a string with leading whitespace removed.

        Raises
        ------
        None
            This method does not raise any exceptions.
        """

        # Return the internal value as a string, removing leading whitespace
        return self.__value_raw.lstrip()

    def __toStr(self):
        """
        Converts the internal value to a string representation with the type hint prefix.

        This method checks if the internal value is a string. If so, it returns a string
        in the format "<type_hint>:<value>", where <type_hint> is the current type hint
        and <value> is the internal string value. If the internal value is not a string,
        an exception is raised.

        Returns
        -------
        str
            A string combining the type hint and the internal value, separated by a colon.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a string.
        """

        # Ensure the internal value is a string before conversion
        if not isinstance(self.__value_raw, str):
            raise OrionisEnvironmentValueError(
                f"Value must be a string to convert to str, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and value
        return f"{self.__value_raw}"

    def __parseInt(self):
        """
        Converts the internal raw value to an integer, assuming the type hint is 'int:'.

        This method attempts to strip leading and trailing whitespace from the internal
        raw value and convert it to an integer. If the conversion fails due to an invalid
        format or non-integer input, an `OrionisEnvironmentValueException` is raised.

        Parameters
        ----------
        self : EnvironmentCaster
            The instance of the EnvironmentCaster class.

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

        This method checks if the internal value is an integer. If so, it returns a string
        in the format "<type_hint>:<value>", where <type_hint> is the current type hint
        and <value> is the integer value. If the internal value is not an integer, an exception is raised.

        Returns
        -------
        str
            A string combining the type hint and the internal integer value, separated by a colon.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not an integer.
        """

        # Ensure the internal value is an integer before conversion
        if not isinstance(self.__value_raw, int):
            raise OrionisEnvironmentValueError(
                f"Value must be an integer to convert to int, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and integer value
        return f"{self.__type_hint}:{str(self.__value_raw)}"

    def __parseFloat(self):
        """
        Converts the internal raw value to a float, assuming the type hint is 'float:'.

        This method attempts to strip leading and trailing whitespace from the internal
        raw value and convert it to a float. If the conversion fails due to an invalid
        format or non-numeric input, an `OrionisEnvironmentValueException` is raised.

        Parameters
        ----------
        self : EnvironmentCaster
            The instance of the EnvironmentCaster class.

        Returns
        -------
        float
            The internal value converted to a float.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a float due to invalid format or type.
        """
        # Remove leading and trailing whitespace from the raw value
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

        This method checks if the internal value is a float. If so, it returns a string
        in the format "<type_hint>:<value>", where <type_hint> is the current type hint
        and <value> is the float value. If the internal value is not a float, an exception is raised.

        Returns
        -------
        str
            A string combining the type hint and the internal float value, separated by a colon.
            For example, "float:3.14".

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a float.
        """

        # Ensure the internal value is a float before conversion
        if not isinstance(self.__value_raw, float):
            raise OrionisEnvironmentValueError(
                f"Value must be a float to convert to float, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and float value
        return f"{self.__type_hint}:{str(self.__value_raw)}"

    def __parseBool(self):
        """
        Converts the internal raw value to a boolean, assuming the type hint is 'bool:'.

        This method processes the internal raw value by stripping leading and trailing whitespace,
        converting it to lowercase, and then checking if it matches the string 'true' or 'false'.
        If the value is 'true', it returns the boolean value True. If the value is 'false', it returns
        the boolean value False. If the value does not match either, an `OrionisEnvironmentValueException`
        is raised.

        Parameters
        ----------
        self : EnvironmentCaster
            The instance of the EnvironmentCaster class.

        Returns
        -------
        bool
            Returns True if the value is 'true' (case-insensitive), False if the value is 'false' (case-insensitive).

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a boolean because it does not match 'true' or 'false'.
        """

        # Strip whitespace and convert the value to lowercase for comparison
        value = self.__value_raw.strip().lower()

        # Check for 'true' and return True
        if value == 'true':
            return True

        # Check for 'false' and return False
        elif value == 'false':
            return False

        # Raise an exception if the value cannot be interpreted as a boolean
        else:
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to bool.")

    def __toBool(self):
        """
        Converts the internal value to a string representation with the boolean type hint prefix.

        This method checks if the internal value is a boolean. If so, it returns a string
        in the format "<type_hint>:<value>", where <type_hint> is the current type hint
        and <value> is the lowercase string representation of the boolean value.
        If the internal value is not a boolean, an exception is raised.

        Returns
        -------
        str
            A string combining the type hint and the internal boolean value, separated by a colon.
            The boolean value is represented as 'true' or 'false' in lowercase.

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a boolean.
        """

        # Ensure the internal value is a boolean before conversion
        if not isinstance(self.__value_raw, bool):
            raise OrionisEnvironmentValueError(
                f"Value must be a boolean to convert to bool, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and boolean value in lowercase
        return f"{self.__type_hint}:{str(self.__value_raw).lower()}"

    def __parseList(self):
        """
        Converts the internal raw value to a list, assuming the type hint is 'list:'.

        This method attempts to strip leading and trailing whitespace from the internal
        raw value and convert it to a Python list using `ast.literal_eval`. If the conversion
        fails due to an invalid format or if the evaluated value is not a list, an
        `OrionisEnvironmentValueException` is raised.

        Parameters
        ----------
        self : EnvironmentCaster
            The instance of the EnvironmentCaster class.

        Returns
        -------
        list
            The internal value converted to a list if the type hint is 'list:'.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a list due to invalid format or type.
        """
        import ast

        # Remove leading and trailing whitespace from the raw value
        value = self.__value_raw.strip()

        try:

            # Safely evaluate the string to a Python object
            parsed = ast.literal_eval(value)

            # Ensure the evaluated object is a list
            if not isinstance(parsed, list):
                raise ValueError("Value is not a list")

            # Return the parsed list
            return parsed

        except (ValueError, SyntaxError) as e:

            # Raise a custom exception if conversion fails
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to list: {str(e)}")

    def __toList(self):
        """
        Converts the internal value to a string representation with the list type hint prefix.

        This method checks if the internal value is a list. If so, it returns a string
        in the format "<type_hint>:<value>", where <type_hint> is the current type hint
        and <value> is the string representation of the list. If the internal value is not a list,
        an exception is raised.

        Returns
        -------
        str
            A string combining the type hint and the internal list value, separated by a colon.
            For example, "list:[1, 2, 3]".

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a list.
        """

        # Ensure the internal value is a list before conversion
        if not isinstance(self.__value_raw, list):
            raise OrionisEnvironmentValueError(
                f"Value must be a list to convert to list, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and list value
        return f"{self.__type_hint}:{repr(self.__value_raw)}"

    def __parseDict(self):
        """
        Converts the internal raw value to a dictionary, assuming the type hint is 'dict:'.

        This method attempts to strip leading and trailing whitespace from the internal
        raw value and safely evaluate it as a Python dictionary using `ast.literal_eval`.
        If the conversion fails due to an invalid format or if the evaluated value is not
        a dictionary, an `OrionisEnvironmentValueException` is raised.

        Parameters
        ----------
        self : EnvironmentCaster
            The instance of the EnvironmentCaster class.

        Returns
        -------
        dict
            The internal value converted to a dictionary if the type hint is 'dict:'.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a dictionary due to invalid format or type.
        """
        import ast

        # Remove leading and trailing whitespace from the raw value
        value = self.__value_raw.strip()

        try:

            # Safely evaluate the string to a Python object
            parsed = ast.literal_eval(value)

            # Ensure the evaluated object is a dictionary
            if not isinstance(parsed, dict):
                raise ValueError("Value is not a dict")

            # Return the parsed dictionary
            return parsed

        except (ValueError, SyntaxError) as e:

            # Raise a custom exception if conversion fails
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to dict: {str(e)}")

    def __toDict(self):
        """
        Converts the internal value to a string representation with the dictionary type hint prefix.

        This method checks if the internal value is a dictionary. If so, it returns a string
        in the format "<type_hint>:<value>", where <type_hint> is the current type hint
        and <value> is the string representation of the dictionary. If the internal value is not a dictionary,
        an exception is raised.

        Returns
        -------
        str
            A string combining the type hint and the internal dictionary value, separated by a colon.
            For example, "dict:{'key': 'value'}".

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a dictionary.
        """

        # Ensure the internal value is a dictionary before conversion
        if not isinstance(self.__value_raw, dict):
            raise OrionisEnvironmentValueError(
                f"Value must be a dict to convert to dict, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and dictionary value
        return f"{self.__type_hint}:{repr(self.__value_raw)}"

    def __parseTuple(self):
        """
        Converts the internal raw value to a tuple, assuming the type hint is 'tuple:'.

        This method strips leading and trailing whitespace from the internal raw value,
        then attempts to safely evaluate the string as a Python tuple using `ast.literal_eval`.
        If the conversion is successful and the result is a tuple, it is returned.
        If the conversion fails or the evaluated value is not a tuple, an
        `OrionisEnvironmentValueException` is raised.

        Parameters
        ----------
        self : EnvironmentCaster
            The instance of the EnvironmentCaster class.

        Returns
        -------
        tuple
            The internal value converted to a tuple if the type hint is 'tuple:'.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a tuple due to invalid format or type.
        """
        import ast

        # Remove leading and trailing whitespace from the raw value
        value = self.__value_raw.strip()

        try:

            # Safely evaluate the string to a Python object
            parsed = ast.literal_eval(value)

            # Ensure the evaluated object is a tuple
            if not isinstance(parsed, tuple):
                raise ValueError("Value is not a tuple")

            # Return the parsed tuple
            return parsed

        except (ValueError, SyntaxError) as e:

            # Raise a custom exception if conversion fails
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to tuple: {str(e)}")

    def __toTuple(self):
        """
        Converts the internal value to a string representation with the tuple type hint prefix.

        This method checks if the internal value is a tuple. If so, it returns a string
        in the format "<type_hint>:<value>", where <type_hint> is the current type hint
        and <value> is the string representation of the tuple. If the internal value is not a tuple,
        an exception is raised.

        Returns
        -------
        str
            A string combining the type hint and the internal tuple value, separated by a colon.
            For example, "tuple:(1, 2, 3)".

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a tuple.
        """

        # Ensure the internal value is a tuple before conversion
        if not isinstance(self.__value_raw, tuple):
            raise OrionisEnvironmentValueError(
                f"Value must be a tuple to convert to tuple, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and tuple value
        return f"{self.__type_hint}:{repr(self.__value_raw)}"

    def __parseSet(self):
        """
        Converts the internal raw value to a set, assuming the type hint is 'set:'.

        This method strips leading and trailing whitespace from the internal raw value,
        then attempts to safely evaluate the string as a Python set using `ast.literal_eval`.
        If the conversion is successful and the result is a set, it is returned.
        If the conversion fails or the evaluated value is not a set, an
        `OrionisEnvironmentValueException` is raised.

        Returns
        -------
        set
            The internal value converted to a set if the type hint is 'set:'.

        Raises
        ------
        OrionisEnvironmentValueException
            If the value cannot be converted to a set due to invalid format or type.
        """
        import ast

        # Remove leading and trailing whitespace from the raw value
        value = self.__value_raw.strip()

        try:

            # Safely evaluate the string to a Python object
            parsed = ast.literal_eval(value)

            # Ensure the evaluated object is a set
            if not isinstance(parsed, set):
                raise ValueError("Value is not a set")

            # Return the parsed set
            return parsed

        except (ValueError, SyntaxError) as e:

            # Raise a custom exception if conversion fails
            raise OrionisEnvironmentValueException(f"Cannot convert '{value}' to set: {str(e)}")

    def __toSet(self):
        """
        Converts the internal value to a string representation with the set type hint prefix.

        This method checks if the internal value is a set. If so, it returns a string
        in the format "<type_hint>:<value>", where <type_hint> is the current type hint
        and <value> is the string representation of the set. If the internal value is not a set,
        an exception is raised.

        Returns
        -------
        str
            A string combining the type hint and the internal set value, separated by a colon.
            For example, "set:{1, 2, 3}".

        Raises
        ------
        OrionisEnvironmentValueError
            If the internal value is not a set.
        """

        # Ensure the internal value is a set before conversion
        if not isinstance(self.__value_raw, set):
            raise OrionisEnvironmentValueError(
                f"Value must be a set to convert to set, got {type(self.__value_raw).__name__} instead."
            )

        # Return the formatted string with type hint and set value
        return f"{self.__type_hint}:{repr(self.__value_raw)}"
