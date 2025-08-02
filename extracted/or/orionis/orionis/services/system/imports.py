from typing import List, Dict, Any
from orionis.services.system.contracts.imports import IImports

class Imports(IImports):

    def __init__(self):
        """
        Initialize the Imports instance.

        This constructor sets up the Imports object by initializing an empty list
        to store information about user-defined Python modules. The list will
        contain dictionaries, each representing a module with its name, file path,
        and defined symbols.

        Returns
        -------
        None
            This method does not return any value.
        """

        # List to hold information about imported modules
        self.imports: List[Dict[str, Any]] = []

    def collect(self) -> 'Imports':
        """
        Collect information about user-defined Python modules currently loaded.

        Iterates through all modules in `sys.modules` and gathers details for each qualifying module:
            - Module name.
            - Relative file path from the current working directory.
            - List of symbols (functions, classes, or submodules) defined in the module.

        Excludes modules that:
            - Are part of the standard library.
            - Reside in the active virtual environment (if any).
            - Are binary extension modules (e.g., `.pyd`, `.dll`, `.so`).
            - Are special modules such as `"__main__"`, `"__mp_main__"`, or those starting with `"_distutils"`.

        The collected information is stored in `self.imports` as a list of dictionaries, each containing the module's name, file path, and symbols.

        Returns
        -------
        Imports
            The current instance of `Imports` with the `imports` attribute updated to include information about the collected modules.
        """

        import sys
        import os
        import types

        # Clear any previously collected imports
        self.imports.clear()

        # Get standard library paths to exclude standard modules
        stdlib_paths = [os.path.dirname(os.__file__)]

        # Get virtual environment path if active
        venv_path = os.environ.get("VIRTUAL_ENV")
        if venv_path:
            venv_path = os.path.abspath(venv_path)

        # Iterate over all loaded modules
        for name, module in list(sys.modules.items()):
            file: str = getattr(module, '__file__', None)

            # Filter out unwanted modules based on path, type, and name
            if (
                file
                and not any(file.startswith(stdlib_path) for stdlib_path in stdlib_paths)
                and (not venv_path or not file.startswith(venv_path))
                and not file.lower().endswith(('.pyd', '.dll', '.so'))
                and name not in ("__main__", "__mp_main__")
                and not name.startswith("_distutils")
            ):

                # Get relative file path from current working directory
                rel_file = os.path.relpath(file, os.getcwd())
                symbols = []

                # Collect symbols defined in the module (functions, classes, submodules)
                try:
                    for attr in dir(module):
                        value = getattr(module, attr)
                        if isinstance(value, (types.FunctionType, type, types.ModuleType)):

                            # Ensure symbol is defined in this module
                            if getattr(value, '__module__', None) == name:
                                symbols.append(attr)
                except Exception:
                    # Ignore errors during symbol collection
                    pass

                # Only add modules that are not __init__.py and have symbols
                if not rel_file.endswith('__init__.py') and symbols:
                    self.imports.append({
                        "name": name,
                        "file": rel_file,
                        "symbols": symbols,
                    })

        # Return the current instance with updated imports
        return self

    def display(self) -> None:
        """
        Display a formatted table of collected import statements using the Rich library.

        This method presents a visual summary of all collected user-defined Python modules.
        If the imports have not been collected yet, it automatically calls `self.collect()` to gather them.
        The output is rendered as a table inside a styled panel in the console, showing each module's name,
        relative file path, and its defined symbols.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It outputs the formatted table to the console.
        """

        # Collect imports if not already done
        if not self.imports:
            self.collect()

        # Import Rich components for console output
        from rich.console import Console
        from rich.table import Table
        from rich.box import MINIMAL
        from rich.panel import Panel

        # Create a console instance for output
        console = Console()

        # Set table width to 75% of console width
        width = int(console.size.width * 0.75)

        # Create a table with minimal box style and custom formatting
        table = Table(
            box=MINIMAL,
            show_header=True,
            show_edge=False,
            pad_edge=False,
            min_width=width,
            padding=(0, 1),
            collapse_padding=True,
        )

        # Add columns for module name, file path, and symbols
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("File", style="white")
        table.add_column("Symbols", style="magenta")

        # Populate the table with sorted import data
        for imp in sorted(self.imports, key=lambda x: x["name"].lower()):
            symbols_str = ", ".join(imp["symbols"])
            table.add_row(imp["name"], imp["file"], symbols_str)

        # Render the table inside a styled panel in the console
        console.print(Panel(
            table,
            title="[bold blue]🔎 Loaded Python Modules (Orionis Imports Trace)[/bold blue]",
            border_style="blue",
            width=width
        ))

    def clear(self) -> None:
        """
        Remove all entries from the collected imports list.

        This method resets the `imports` attribute by removing all currently stored
        module information. It is useful for discarding previously collected data
        before performing a new collection or when a fresh state is required.

        Returns
        -------
        None
            This method does not return any value. The `imports` list is emptied in place.
        """

        # Remove all items from the imports list to reset its state
        self.imports.clear()