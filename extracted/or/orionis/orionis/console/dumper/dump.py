import inspect
import json
import os
from dataclasses import is_dataclass
from datetime import datetime
from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.traceback import install
from orionis.console.dumper.contracts.dump import IDebug

class Debug(IDebug):

    def __init__(self, line:str = None) -> None:
        """
        Initializes the dump class.

        Parameters
        ----------
        line : str, optional
            The line text callback to use for output, default is None
        Returns
        -------
        None
        Notes
        -----
        This constructor performs the following setup:
        - Installs required dependencies via `install()`
        - Initializes a console instance for output handling
        - Sets the default indentation size to 4 spaces
        - Creates a set to prevent recursion during operations
        - Stores the provided line callback if specified
        """
        install()
        self.console = Console()
        self.indent_size = 4
        self._recursion_guard = set()
        self.line_tcbk = line

    def dd(self, *args: Any) -> None:
        """
        Dumps the provided arguments to the output and exits the program.

        Parameters
        ----------
        *args : Any
            Variable length argument list to be processed and output.
        Returns
        -------
        Notes
        -----
        This method will terminate the program execution after dumping the arguments.
        """
        self.__processOutput(*args, exit_after=True)

    def dump(self, *args: Any) -> None:
        """
        Dumps the provided arguments to the output without exiting the program.

        Parameters
        ----------
        *args : Any
            Variable length argument list to be processed and output.

        Returns
        -------
        None

        Notes
        -----
        This method displays the arguments in an appropriate format based on their type
        but allows the program execution to continue.
        """
        self.__processOutput(*args, exit_after=False)

    def __processOutput(self, *args: Any, exit_after: bool) -> None:
        """
        Processes the output based on the provided arguments and determines the appropriate
        format for displaying the data.

        Parameters
        ----------
        *args : Any
            Variable-length arguments representing the data to be processed.
        exit_after : bool
            If True, the program will exit after processing the output.

        Raises
        ------
        Exception
            Catches and logs any exception that occurs during processing.

        Notes
        -----
        If `exit_after` is True, the program will terminate with an exit code of 1.
        Determines whether to display data as a table, JSON, or raw dump based on its structure.
        """

        # Try to process the output and handle any exceptions that may occur
        try:

            # Check if any arguments were provided
            if not args:
                raise ValueError("No arguments were provided, or the arguments are null or invalid")

            # If only one argument is provided, determine its type and print accordingly
            elif len(args) == 1:
                arg = args[0]
                if self.__isJsonSerializable(arg) and self.__isTabular(arg) and isinstance(arg, (list)):
                    self.__printTable(arg)
                elif self.__isJsonSerializable(arg):
                    self.__printJson(arg)
                else:
                    self.__printDump(args)

            # If multiple arguments are provided, determine the type of each and print accordingly
            else:
                self.__printDump(args)

        except Exception as e:

            # If an error occurs, print the error message in a standard panel format
            self.__printStandardPanel(
                f"[bold red]An error occurred while processing the debug output: {str(e)}[/]",
                border_style="red",
            )
        finally:

            # If exit_after is True, exit the program with a non-zero status code
            if exit_after:
                os._exit(1)

    def __printDump(self, args: tuple) -> None:
        """
        Prints a formatted dump of the provided arguments to the console.

        Parameters
        ----------
        args : tuple
            A tuple containing the objects to be dumped and displayed.

        Returns
        -------
            This method doesn't return anything.

        Notes
        -----
        This method processes each argument in the tuple, clears the recursion guard
        for each iteration, renders the argument using the __render method, and then
        prints all rendered content in a formatted panel with syntax highlighting.
        """

        # Clear the recursion guard before processing the arguments
        content = []
        for arg in args:
            self._recursion_guard.clear()
            content.append(self.__render(arg))

        # Print the rendered content in a standard panel with syntax highlighting
        self.__printStandardPanel(
            Syntax(
                "\n".join(content),
                "python",
                line_numbers=False,
                background_color="default",
                word_wrap=True
            ),
            border_style="cyan bold",
        )

    def __printJson(self, data: Any) -> None:
        """
        Print a JSON representation of the given data to the console using a styled panel.

        Parameters
        ----------
        data : Any
            The data to be serialized and displayed as JSON.
            Must be a dictionary or list for proper JSON serialization.

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the data cannot be serialized to JSON, falls back to a generic dump method.

        Notes
        -----
        Uses the `rich` library to format and display the JSON output with syntax highlighting.
        Retrieves and displays the caller's line information for context.
        Handles non-serializable objects using a custom JSON serializer.
        If serialization fails, falls back to the `__printDump` method.
        """
        try:

            # Check if the data is JSON serializable
            if not isinstance(data, (dict, list)):
                raise TypeError("Data must be a dictionary or a list for JSON serialization.")

            # Serialize the data to JSON format with custom serializer
            json_str = json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
                default=self.__jsonSerializer
            )

            # Print the JSON string in a standard panel with syntax highlighting
            self.__printStandardPanel(
                Syntax(
                    json_str,
                    "json",
                    line_numbers=True,
                    background_color="default",
                    word_wrap=True
                ),
                border_style="green",
            )

        except TypeError as e:

            # If serialization fails, print a dump of the data instead
            self.__printDump((data,))

    def __printTable(self, data: Any) -> None:
        """
        Prints a formatted table representation of the given data.

        Parameters
        ----------
        data : Any
            The data to be displayed in a tabular format.
            Can be a list of dictionaries, list of objects, or a dictionary.

        Returns
        -------
        None
            This method doesn't return anything, it prints output to the console.

        Notes
        -----
        - For lists of dictionaries: Uses dictionary keys as column headers
        - For lists of objects: Uses object attribute names as column headers
        - For simple lists: Shows index and value columns
        - For dictionaries: Shows key-value pairs as two columns
        - Falls back to __printDump if table rendering fails
        """
        try:

            # Create a table with specified styles and minimum width
            table = Table(
                show_header=True,
                header_style="bold white on blue",
                min_width=(self.console.width // 4) * 3
            )

            # Check if the data is in a tabular format (list or dict)
            if isinstance(data, list):

                # If the list is empty, print a message and return
                if not data:
                    self.console.print("[yellow]Empty list[/]")
                    return

                # Determine the columns based on the first item in the list
                first = data[0]
                if isinstance(first, dict):
                    columns = list(first.keys())
                elif hasattr(first, '__dict__'):
                    columns = list(vars(first).keys())
                else:
                    columns = ["Index", "Value"]

                # Add columns to the table
                for col in columns:
                    table.add_column(str(col))

                # Populate the table with data
                for i, item in enumerate(data):
                    if isinstance(item, dict):
                        table.add_row(*[str(item.get(col, '')) for col in columns])
                    elif hasattr(item, '__dict__'):
                        item_dict = vars(item)
                        table.add_row(*[str(item_dict.get(col, '')) for col in columns])
                    else:
                        table.add_row(str(i), str(item))

            # If the data is a dictionary, create a key-value table
            elif isinstance(data, dict):
                table.add_column("Key", style="magenta")
                table.add_column("Value")

                for k, v in data.items():
                    table.add_row(str(k), str(v))

            # If the data is not in a recognized format, print a dump
            self.__printStandardPanel(
                table,
                border_style="blue",
            )

        except Exception as e:

            # If an error occurs while creating the table, print a dump of the data
            self.__printDump((data,))

    def __printStandardPanel(self, renderable, border_style: str, padding=(0, 1)) -> None:
        """
        Renders a standard panel with the given content and styling options.

        Parameters
        ----------
        renderable : Any
            The content to be displayed inside the panel. This can be any renderable object
            supported by the Rich library.
        border_style : str
            The style of the border for the panel (e.g., "green", "red bold").
        padding : tuple, optional
            A tuple specifying the padding inside the panel as (vertical, horizontal).
            Default is (0, 1).

        Returns
        -------
        None
            This method prints to the console but does not return a value.

        Notes
        -----
        This method uses the Rich library to create and display a panel with the specified
        content and styling. It includes line information from the call stack and a timestamp.
        """

        # Get the line information from the call stack or use the provided callback
        if self.line_tcbk is None:
            frame = inspect.currentframe()
            caller_frame = frame.f_back.f_back.f_back.f_back if frame else None
            line_info = f"[blue underline]{self.__getLineInfo(caller_frame) if caller_frame else 'Unknown location'}[/]"

        # If a line callback is provided, use it to get the line information
        else:
            line_info = f"[blue underline]{self.line_tcbk}[/]"

        # Get the current timestamp for the subtitle
        subtitle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print a blank line before the panel for better readability
        self.console.print()
        self.console.print(Panel(
            renderable,
            title=f"Debugger - {line_info}",
            title_align='left',
            subtitle=subtitle,
            subtitle_align='right',
            border_style=border_style,
            highlight=True,
            padding=padding,
            width=(self.console.width // 4) * 3,
        ))
        self.console.print()

    def __isTabular(self, data: Any) -> bool:
        """
        Determines if the given data is in a tabular format.

        Parameters
        ----------
        data : Any
            The data to be checked for tabular structure.

        Returns
        -------
        bool
            True if the data is in a tabular format, False otherwise.

        Notes
        -----
        A data structure is considered tabular if it is:
        - A list of dictionaries with identical keys
        - A list of objects with attributes
        - A dictionary
        """

        # Check if the data is a list or a dictionary
        if isinstance(data, list):

            # If the list is empty, it is not considered tabular
            if all(isinstance(item, dict) for item in data):
                keys = set(data[0].keys())
                return all(set(item.keys()) == keys for item in data)

            # If the list contains objects, check if they have a __dict__ attribute
            if len(data) > 0 and hasattr(data[0], '__dict__'):
                return True

        # If the data is a tuple, set, or any other iterable, it is not considered tabular
        elif isinstance(data, dict):
            return True

        # If the data is not a list or dictionary, it is not considered tabular
        return False

    def __isJsonSerializable(self, data: Any) -> bool:
        """
        Determines if the given data is JSON serializable.

        Parameters
        ----------
        data : Any
            The data to check for JSON serializability.

        Returns
        -------
        bool
            True if the data is JSON serializable, False otherwise.

        Notes
        -----
        This method attempts to serialize the provided data into a JSON string
        using a custom serializer. If the serialization succeeds, the data is
        considered JSON serializable.
        """
        try:

            # Attempt to serialize the data to JSON format
            json.dumps(
                data,
                default=self.__jsonSerializer
            )

            # If serialization succeeds, return True
            return True

        except (TypeError, OverflowError):

            # If serialization fails due to unsupported types or overflow,
            # return False indicating the data is not JSON serializable
            return False

    def __render(self, value: Any, indent: int = 0, key: Any = None, depth: int = 0) -> str:
        """
        Recursively renders a string representation of a given value.

        Parameters
        ----------
        value : Any
            The value to render. Can be of any type, including dict, list, tuple, set,
            dataclass, or objects with a `__dict__` attribute.
        indent : int, optional
            The current indentation level. Default is 0.
        key : Any, optional
            The key or index associated with the value, if applicable. Default is None.
        depth : int, optional
            The current recursion depth. Default is 0.

        Returns
        -------
        str
            A string representation of the value, formatted with indentation and type information.

        Notes
        -----
        - Limits recursion depth to 10 to prevent infinite loops.
        - Detects and handles recursive references to avoid infinite recursion.
        - Supports rendering of common Python data structures, dataclasses, and objects with attributes.
        - Formats datetime objects and callable objects with additional details.
        """

        # Check for maximum recursion depth to prevent infinite loops
        if depth > 10:
            return "... (max depth)"

        # Check for recursion guard to prevent infinite recursion
        obj_id = id(value)

        # If the object ID is already in the recursion guard, return a placeholder
        if obj_id in self._recursion_guard:
            return "... (recursive)"

        # Add the object ID to the recursion guard to track it
        self._recursion_guard.add(obj_id)

        # Prepare the prefix for the rendered output
        space = ' ' * indent
        prefix = f"{space}"

        # If a key is provided, format it and add it to the prefix
        if key is not None:
            prefix += f"{self.__formatKey(key)} => "

        # If the value is None, return a formatted string indicating None
        if value is None:
            result = f"{prefix}None"

        # Handle different types of values and format them accordingly
        elif isinstance(value, dict):
            result = f"{prefix}dict({len(value)})"
            for k, v in value.items():
                result += "\n" + self.__render(v, indent + self.indent_size, k, depth + 1)

        # If the value is a list, tuple, or set, format it with its type and length
        elif isinstance(value, (list, tuple, set)):
            type_name = type(value).__name__
            result = f"{prefix}{type_name}({len(value)})"
            for i, item in enumerate(value):
                result += "\n" + self.__render(
                    item,
                    indent + self.indent_size,
                    i if isinstance(value, (list, tuple)) else None,
                    depth + 1
                )

        # If the value is a string, format it with its type and length
        elif is_dataclass(value):
            result = f"{prefix}{value.__class__.__name__}"
            for k, v in vars(value).items():
                result += "\n" + self.__render(v, indent + self.indent_size, k, depth + 1)

        # If the value is an object with a __dict__ attribute, format it with its class name
        elif hasattr(value, "__dict__"):
            result = f"{prefix}{value.__class__.__name__}"
            for k, v in vars(value).items():
                result += "\n" + self.__render(v, indent + self.indent_size, k, depth + 1)

        # If the value is a datetime object, format it with its ISO 8601 string representation
        elif isinstance(value, datetime):
            result = f"{prefix}datetime({value.isoformat()})"

        # If the value is a callable (function or method), format it with its name
        elif callable(value):
            result = f"{prefix}callable({value.__name__ if hasattr(value, '__name__') else repr(value)})"

        # If the value is a simple type (int, float, str, etc.), format it with its type and value
        else:
            result = f"{prefix}{type(value).__name__}({repr(value)})"

        # Remove the object ID from the recursion guard after processing
        self._recursion_guard.discard(obj_id)

        # Return the formatted result
        return result

    @staticmethod
    def __jsonSerializer(obj):
        """
        Serialize an object into a JSON-compatible format.

        Parameters
        ----------
        obj : object
            The object to serialize. Supported types include:

        Returns
        -------
        object

        Raises
        ------
        TypeError
            If the object type is not supported for JSON serialization.
        """

        # Check if the object is a datetime instance and return its ISO format
        if isinstance(obj, datetime):
            return obj.isoformat()

        # Check if the object is a dataclass and return its dictionary representation
        elif hasattr(obj, '__dict__'):
            return vars(obj)

        # Check if the object is a dataclass instance and return its dictionary representation
        elif isinstance(obj, (set, tuple)):
            return list(obj)

        # If the object is a list, convert it to a list of JSON-serializable items
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    @staticmethod
    def __formatKey(key: Any) -> str:
        """
        Formats a given key into a string representation.

        Parameters
        ----------
        key : Any
            The key to be formatted. It can be of any type.
        Returns
        -------
        str
            A string representation of the key. If the key is a string, it is
        """

        # If the key is a string, return it wrapped in quotes; otherwise, convert it to a string
        if isinstance(key, str):
            return f'"{key}"'

        # If the key is not a string, convert it to a string representation
        return str(key)

    @staticmethod
    def __getLineInfo(frame: inspect.FrameInfo) -> str:
        """
        Extracts and formats line information from a given frame.

        Parameters
        ----------
        frame : inspect.FrameInfo
            The frame object containing code context.

        Returns
        -------
        str
            A string in the format "filename:line_no", where `filename` is the
            name of the file (excluding the path) and `line_no` is the line number
            in the file where the frame is located.
        """

        # Extract the filename and line number from the frame
        filename = frame.f_code.co_filename.split('/')[-1]
        line_no = frame.f_lineno

        # Return the formatted string with filename and line number
        return f"{filename}:{line_no}"