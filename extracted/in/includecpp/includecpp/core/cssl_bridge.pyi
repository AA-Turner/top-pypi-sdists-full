"""
CSSL Bridge - Type Stubs for Python API

CSSL (C-Style Scripting Language) is a scripting language that bridges Python and C++ style syntax.
This module provides the Python API for executing CSSL code and sharing objects between Python and CSSL.

Quick Start:
    from includecpp import CSSL

    # Execute CSSL code directly
    CSSL.run('printl("Hello from CSSL!");')

    # Execute a CSSL file
    CSSL.run("script.cssl", arg1, arg2)

    # Share Python objects with CSSL (live reference)
    my_data = {"count": 0}
    CSSL.share(my_data, "data")
    CSSL.run('$data.count = $data.count + 1;')
    print(my_data["count"])  # 1

    # Create reusable modules
    math_mod = CSSL.makemodule('''
        int add(int a, int b) { return a + b; }
    ''')
    result = math_mod.add(2, 3)  # 5
"""

import threading
from typing import Any, List, Optional, Callable, Dict, Union


class CSSLScript:
    """
    A typed CSSL script object.

    Created via CSSL.script() - represents a bundle of CSSL code that can be
    executed multiple times or combined into modules.

    Script Types:
        - "cssl": Main script - the primary entry point
        - "cssl-pl": Payload - helper code loaded via payload()

    Usage:
        from includecpp import CSSL

        # Create a main script
        main = CSSL.script("cssl", '''
            printl("Running main script");
            helper();
        ''')

        # Create a payload (helper functions)
        helpers = CSSL.script("cssl-pl", '''
            void helper() {
                printl("Helper called!");
            }
        ''')

        # Execute the script
        main.run()

        # Or combine into a module
        mod = CSSL.makemodule(main, helpers, "mymodule")
    """

    def __init__(self, cssl_instance: 'CsslLang', script_type: str, code: str, *params: Any) -> None: ...

    @property
    def code(self) -> str:
        """Get the script's CSSL source code."""
        ...

    @property
    def is_payload(self) -> bool:
        """Check if this script is a payload (cssl-pl) type."""
        ...

    def run(self, *args: Any) -> Any:
        """
        Execute this script with optional arguments.

        Args:
            *args: Arguments accessible in CSSL via parameter.get(index)

        Returns:
            Execution result
        """
        ...

    def __call__(self, *args: Any) -> Any:
        """Allow calling the script directly: script() is same as script.run()"""
        ...


class CSSLModule:
    """
    A callable CSSL module that executes code with arguments.

    Created via CSSL.module() - the code is executed each time the module is called,
    with arguments accessible via parameter.get(index).

    Usage:
        from includecpp import CSSL

        # Create a simple greeting module
        greet = CSSL.module('''
            string name = parameter.get(0);
            printl("Hello, " + name + "!");
        ''')

        greet("World")   # Prints: Hello, World!
        greet("Alice")   # Prints: Hello, Alice!

        # Module with multiple parameters
        calc = CSSL.module('''
            int a = parameter.get(0);
            int b = parameter.get(1);
            parameter.return(a + b);
        ''')
        result = calc(10, 20)  # Returns 30
    """

    def __init__(self, cssl_instance: 'CsslLang', code: str) -> None: ...

    def __call__(self, *args: Any) -> Any:
        """Execute the module code with the given arguments."""
        ...

    def __repr__(self) -> str: ...


class CSSLFunctionModule:
    """
    A CSSL module with accessible functions as methods.

    Created via CSSL.makemodule() - functions defined in the CSSL code
    become callable attributes on this module. This is the recommended way
    to create reusable CSSL libraries.

    Usage:
        from includecpp import CSSL

        # Create a math module with multiple functions
        math_mod = CSSL.makemodule('''
            int add(int a, int b) {
                return a + b;
            }

            int multiply(int a, int b) {
                return a * b;
            }

            float average(int a, int b) {
                return (a + b) / 2.0;
            }
        ''')

        # Call functions as attributes
        print(math_mod.add(2, 3))       # 5
        print(math_mod.multiply(4, 5))  # 20
        print(math_mod.average(10, 20)) # 15.0

        # List available functions
        print(dir(math_mod))  # ['add', 'average', 'multiply']
    """

    def __init__(self, cssl_instance: 'CsslLang', code: str) -> None: ...

    def __getattr__(self, name: str) -> Callable[..., Any]:
        """Get a function from the module by name."""
        ...

    def __dir__(self) -> List[str]:
        """List all available functions in this module."""
        ...

    def __repr__(self) -> str: ...


class CsslLang:
    """
    CSSL Language runtime interface for Python.

    This is the main class for interacting with CSSL from Python. It provides
    methods for executing code, sharing objects, creating modules, and more.

    Basic Usage:
        from includecpp import CSSL

        # Get default instance
        cssl = CSSL.CsslLang()

        # Or use module-level functions directly
        CSSL.run("printl('Hello');")

    Execution Methods:
        - run(): Execute CSSL code or file (recommended)
        - exec(): Alias for run() (deprecated)
        - T_run(): Execute asynchronously in a thread

    Object Sharing:
        - share(): Share Python object with CSSL (live reference)
        - unshare(): Remove shared object
        - shared(): Get a shared object by name

    Module Creation:
        - module(): Create callable code block
        - makemodule(): Create module with callable functions
        - script(): Create typed script (cssl or cssl-pl)
        - code(): Register inline payload

    Globals:
        - set_global(): Set CSSL global variable
        - get_global(): Get CSSL global variable
    """

    def __init__(self, output_callback: Optional[Callable[[str, str], None]] = ...) -> None:
        """
        Initialize CSSL runtime.

        Args:
            output_callback: Optional callback for capturing output.
                             Called with (text, level) where level is
                             'normal', 'debug', 'warning', or 'error'.

        Usage:
            def my_output(text, level):
                if level == 'error':
                    log_error(text)
                else:
                    print(text)

            cssl = CSSL.CsslLang(output_callback=my_output)
        """
        ...

    def run(self, path_or_code: str, *args: Any) -> Any:
        """
        Execute CSSL code or file. This is the primary execution method.

        Args:
            path_or_code: Either a path to a .cssl file or CSSL code string.
                          File paths must end in .cssl, .cssl-pl, or .cssl-mod
            *args: Arguments passed to the script, accessible via parameter.get(index)

        Returns:
            Execution result. If parameter.return() was called in CSSL,
            returns those values. Single value if one, list if multiple.

        Usage:
            # Execute a file
            result = cssl.run("script.cssl", "arg1", 42)

            # Execute inline code
            cssl.run('printl("Hello World!");')

            # Get return value
            result = cssl.run('''
                int x = parameter.get(0);
                parameter.return(x * 2);
            ''', 21)
            print(result)  # 42
        """
        ...

    def T_run(
        self,
        path_or_code: str,
        *args: Any,
        callback: Optional[Callable[[Any], None]] = ...
    ) -> threading.Thread:
        """
        Execute CSSL code asynchronously in a background thread.

        Args:
            path_or_code: Path to .cssl file or CSSL code string
            *args: Arguments to pass to the script
            callback: Optional callback invoked with result when execution completes

        Returns:
            Thread object that can be joined or monitored

        Usage:
            def on_complete(result):
                print(f"Script finished with: {result}")

            thread = cssl.T_run("long_running.cssl", callback=on_complete)
            # ... do other work ...
            thread.join()  # Wait for completion if needed
        """
        ...

    def exec(self, path_or_code: str, *args: Any) -> Any:
        """
        Execute CSSL code or file (DEPRECATED - use run() instead).

        This method is kept for backwards compatibility.
        See run() for documentation.
        """
        ...

    def T_exec(
        self,
        path_or_code: str,
        *args: Any,
        callback: Optional[Callable[[Any], None]] = ...
    ) -> threading.Thread:
        """
        Execute CSSL asynchronously (DEPRECATED - use T_run() instead).

        This method is kept for backwards compatibility.
        See T_run() for documentation.
        """
        ...

    def script(self, script_type: str, code: str, *params: Any) -> CSSLScript:
        """
        Create a typed CSSL script object.

        Scripts can be executed multiple times or combined into modules.
        This is useful for organizing complex CSSL projects.

        Args:
            script_type: "cssl" for main script, "cssl-pl" for payload
            code: The CSSL source code
            *params: Optional default parameters

        Returns:
            CSSLScript object

        Usage:
            # Create main script and payload
            main = cssl.script("cssl", '''
                printl("Main running");
                @helper.greet("World");
            ''')

            payload = cssl.script("cssl-pl", '''
                void greet(string name) {
                    printl("Hello, " + name + "!");
                }
            ''')

            # Bundle into a .cssl-mod file
            cssl.makemodule(main, payload, "mymodule")
        """
        ...

    def code(self, name: str, code: str) -> None:
        """
        Register inline CSSL code as a named payload.

        Registered payloads can be loaded in CSSL using payload("name").
        This allows creating helper libraries from Python without external files.

        Args:
            name: Unique name for the payload
            code: CSSL code string

        Usage:
            # Register helper functions
            cssl.code("utils", '''
                global version = "1.0.0";

                void log(string msg) {
                    printl("[LOG] " + msg);
                }

                int double(int x) {
                    return x * 2;
                }
            ''')

            # Use in CSSL code
            cssl.run('''
                payload("utils");
                @log("Starting...");
                printl(@double(21));  // 42
            ''')
        """
        ...

    def module(self, code: str) -> CSSLModule:
        """
        Create a callable CSSL module from code.

        The module executes the code each time it's called.
        Arguments are accessible via parameter.get(index).

        Args:
            code: CSSL code string

        Returns:
            CSSLModule - callable that executes the code

        Usage:
            # Simple greeting
            greet = cssl.module('''
                string name = parameter.get(0);
                printl("Hello, " + name + "!");
            ''')
            greet("World")  # Prints: Hello, World!

            # With return value
            calc = cssl.module('''
                int a = parameter.get(0);
                int b = parameter.get(1);
                parameter.return(a * b);
            ''')
            result = calc(6, 7)  # Returns 42
        """
        ...

    def makepayload(self, name: str, path: str) -> str:
        """
        Register a payload from a file path.

        Reads the file and registers it as a payload accessible via payload(name) in CSSL.
        This is a convenience method for loading payload files.

        Args:
            name: Name to register the payload under (used in payload(name) and bind=name)
            path: Path to the .cssl-pl or .cssl file

        Returns:
            The payload code that was registered

        Usage:
            # Register a payload from file
            cssl.makepayload("api", "lib/api/myapi.cssl-pl")

            # Use with makemodule for automatic binding
            mod = cssl.makemodule("writer", "lib/writer.cssl", bind="api")
            mod.SaySomething("Hello!")
        """
        ...

    def makemodule(
        self,
        main_script: Union[str, CSSLScript],
        payload_script: Union[str, CSSLScript, None] = ...,
        name: str = ...,
        bind: str = ...
    ) -> CSSLFunctionModule:
        """
        Create a CSSL module with accessible functions as methods.

        This is the recommended way to create reusable CSSL libraries.
        Functions defined in the code become callable Python methods.

        Args:
            main_script: CSSL code string, file path, or CSSLScript object
            payload_script: Optional payload code (string or CSSLScript)
            name: Optional name to register for payload(name) access
            bind: Optional payload name to auto-prepend (from makepayload)

        Returns:
            CSSLFunctionModule with callable function attributes

        Usage (simplified - with file path and bind):
            # First register the payload
            cssl.makepayload("api", "lib/api/einkaufsmanager.cssl-pl")

            # Then create module from file, binding to payload
            mod = cssl.makemodule("writer", "lib/writer.cssl", bind="api")
            mod.SaySomething("Hello!")  # Functions are now accessible

        Usage (from code string):
            math = cssl.makemodule('''
                int add(int a, int b) { return a + b; }
                int sub(int a, int b) { return a - b; }
            ''')
            print(math.add(10, 5))  # 15
            print(math.sub(10, 5))  # 5

        Usage (from script objects):
            main = cssl.script("cssl", "...")
            helpers = cssl.script("cssl-pl", "...")
            mod = cssl.makemodule(main, helpers, "mymodule")
        """
        ...

    def share(self, instance: Any, name: str = ...) -> str:
        """
        Share a Python object with CSSL (LIVE sharing).

        Changes made in CSSL immediately reflect in the Python object.
        This enables true bidirectional communication between Python and CSSL.

        Args can be passed in either order (for convenience):
            cssl.share(my_object, "name")  # Preferred
            cssl.share("name", my_object)  # Also works

        Args:
            instance: Python object to share (can be any object)
            name: Name to reference in CSSL as $name

        Returns:
            Path to the shared object marker file

        Usage:
            # Share a simple object
            counter = {"value": 0}
            cssl.share(counter, "cnt")
            cssl.run('$cnt.value = $cnt.value + 1;')
            print(counter["value"])  # 1

            # Share a class instance
            class Player:
                def __init__(self):
                    self.health = 100
                    self.name = "Hero"

                def take_damage(self, amount):
                    self.health -= amount

            player = Player()
            cssl.share(player, "player")
            cssl.run('''
                $player.take_damage(25);
                printl($player.name + " has " + $player.health + " HP");
            ''')
            # Prints: Hero has 75 HP
        """
        ...

    def unshare(self, name: str) -> bool:
        """
        Remove a shared object by name.

        Args:
            name: Name of the shared object to remove

        Returns:
            True if object was found and removed, False otherwise

        Usage:
            cssl.share(my_obj, "temp")
            cssl.run("...")  # Use $temp
            cssl.unshare("temp")  # Clean up
        """
        ...

    def get_shared(self, name: str) -> Optional[Any]:
        """
        Get a shared object by name (Python-side access).

        Returns the actual live object reference, not a copy.

        Args:
            name: Name of the shared object (without $ prefix)

        Returns:
            The live shared object, or None if not found
        """
        ...

    def shared(self, name: str) -> Optional[Any]:
        """
        Get a shared object by name (alias for get_shared).

        Works with both Python cssl.share() and CSSL ==> $name exports.

        Args:
            name: Name of the shared object (without $ prefix)

        Returns:
            The live shared object, or None if not found

        Usage:
            # Share from Python
            data = {"x": 1}
            cssl.share(data, "mydata")

            # Later retrieve it
            same_data = cssl.shared("mydata")
            same_data["x"] = 2
            print(data["x"])  # 2 (same object)
        """
        ...

    def getInstance(self, name: str) -> Optional[Any]:
        """
        Get a universal instance by name (for Python-side access).

        Universal instances are shared containers accessible from CSSL, Python, and C++.
        They support dynamic member/method access and are mutable across all contexts.

        Args:
            name: Name of the instance (without quotes)

        Returns:
            The UniversalInstance or None if not found

        Usage:
            # In CSSL: instance<"myContainer"> container;
            # Then in Python:
            container = cssl.getInstance("myContainer")
            container.member = "value"
            print(container.member)  # value
        """
        ...

    def createInstance(self, name: str) -> Any:
        """
        Create or get a universal instance by name (for Python-side creation).

        Args:
            name: Name for the instance

        Returns:
            The UniversalInstance (new or existing)

        Usage:
            container = cssl.createInstance("myContainer")
            container.data = {"key": "value"}
            # Now accessible in CSSL via instance<"myContainer">
        """
        ...

    def deleteInstance(self, name: str) -> bool:
        """
        Delete a universal instance by name.

        Args:
            name: Name of the instance to delete

        Returns:
            True if deleted, False if not found
        """
        ...

    def listInstances(self) -> List[str]:
        """
        List all universal instance names.

        Returns:
            List of instance names
        """
        ...

    def set_global(self, name: str, value: Any) -> None:
        """
        Set a global variable in the CSSL runtime.

        These globals persist across multiple run() calls on the same instance.

        Args:
            name: Variable name (accessible as @name in CSSL)
            value: Value to set

        Usage:
            cssl.set_global("config_path", "/etc/myapp.conf")
            cssl.run('printl(@config_path);')
        """
        ...

    def get_global(self, name: str) -> Any:
        """
        Get a global variable from the CSSL runtime.

        Args:
            name: Variable name

        Returns:
            The variable's value, or None if not found
        """
        ...

    def wait_all(self, timeout: Optional[float] = ...) -> None:
        """
        Wait for all async executions (T_run) to complete.

        Args:
            timeout: Maximum seconds to wait (None = wait forever)

        Usage:
            cssl.T_run("script1.cssl")
            cssl.T_run("script2.cssl")
            cssl.wait_all()  # Wait for both to finish
        """
        ...

    def get_output(self) -> List[str]:
        """
        Get the output buffer from the last execution.

        Returns:
            List of output lines
        """
        ...

    def clear_output(self) -> None:
        """Clear the output buffer."""
        ...


# =============================================================================
# Module-Level Functions (Convenience API)
# =============================================================================
# These functions operate on a default global CSSL instance.
# For most use cases, you can use these directly instead of creating a CsslLang.

def get_cssl() -> CsslLang:
    """Get the default global CSSL instance."""
    ...


def run(path_or_code: str, *args: Any) -> Any:
    """
    Execute CSSL code or file using the default instance.

    This is the primary way to run CSSL code. Supports both file paths
    and inline code strings.

    Args:
        path_or_code: Path to .cssl file or CSSL code string
        *args: Arguments accessible via parameter.get(index)

    Returns:
        Execution result

    Usage:
        from includecpp import CSSL

        # Run inline code
        CSSL.run('printl("Hello World!");')

        # Run a file with arguments
        CSSL.run("process.cssl", input_data, output_path)

        # Get return value
        result = CSSL.run('''
            parameter.return(42);
        ''')
    """
    ...


def T_run(
    path_or_code: str,
    *args: Any,
    callback: Optional[Callable[[Any], None]] = ...
) -> threading.Thread:
    """
    Execute CSSL code asynchronously in a background thread.

    Args:
        path_or_code: Path to .cssl file or CSSL code string
        *args: Arguments to pass to the script
        callback: Optional callback when execution completes

    Returns:
        Thread object

    Usage:
        from includecpp import CSSL

        def on_done(result):
            print(f"Finished: {result}")

        CSSL.T_run("background_task.cssl", callback=on_done)
    """
    ...


def script(script_type: str, code: str, *params: Any) -> CSSLScript:
    """
    Create a typed CSSL script.

    Args:
        script_type: "cssl" for main script, "cssl-pl" for payload
        code: The CSSL code
        *params: Optional parameters

    Returns:
        CSSLScript object

    Usage:
        from includecpp import CSSL

        main = CSSL.script("cssl", '''printl("Main");''')
        payload = CSSL.script("cssl-pl", '''void helper() {}''')
    """
    ...


def code(name: str, code: str) -> None:
    """
    Register inline CSSL code as a named payload.

    Payloads can be loaded in CSSL using payload("name").

    Args:
        name: Unique name for the payload
        code: CSSL code string

    Usage:
        from includecpp import CSSL

        CSSL.code("utils", '''
            void log(string msg) { printl("[LOG] " + msg); }
        ''')

        CSSL.run('''
            payload("utils");
            @log("Hello!");
        ''')
    """
    ...


def module(code: str) -> CSSLModule:
    """
    Create a callable CSSL module from code.

    Args:
        code: CSSL code string

    Returns:
        CSSLModule - callable that executes the code

    Usage:
        from includecpp import CSSL

        greet = CSSL.module('''
            printl("Hello, " + parameter.get(0) + "!");
        ''')
        greet("World")  # Prints: Hello, World!
    """
    ...


def makepayload(name: str, path: str) -> str:
    """
    Register a payload from a file path.

    Reads the file and registers it as a payload accessible via payload(name) in CSSL.

    Args:
        name: Name to register the payload under (used in payload(name) and bind=name)
        path: Path to the .cssl-pl or .cssl file

    Returns:
        The payload code that was registered

    Usage:
        from includecpp import CSSL

        # Register a payload from file
        CSSL.makepayload("api", "lib/api/myapi.cssl-pl")

        # Use with makemodule for automatic binding
        mod = CSSL.makemodule("writer", "lib/writer.cssl", bind="api")
        mod.SaySomething("Hello!")
    """
    ...


def makemodule(
    main_script: Union[str, CSSLScript],
    payload_script: Union[str, CSSLScript, None] = ...,
    name: str = ...,
    bind: str = ...
) -> CSSLFunctionModule:
    """
    Create a CSSL module with accessible functions.

    Args:
        main_script: CSSL code string, file path, or CSSLScript object
        payload_script: Optional payload code (string or CSSLScript)
        name: Optional name to register for payload(name) access
        bind: Optional payload name to auto-prepend (from makepayload)

    Returns:
        CSSLFunctionModule with callable function attributes

    Usage (simplified):
        from includecpp import CSSL

        # Register payload and create module
        CSSL.makepayload("api", "lib/api/myapi.cssl-pl")
        mod = CSSL.makemodule("writer", "lib/writer.cssl", bind="api")
        mod.SaySomething("Hello!")

    Usage (code string):
        math = CSSL.makemodule('''
            int add(int a, int b) { return a + b; }
        ''')
        result = math.add(2, 3)  # 5
    """
    ...


def share(instance: Any, name: str = ...) -> str:
    """
    Share a Python object globally for all CSSL instances (LIVE sharing).

    Changes made in CSSL immediately reflect in the Python object.

    Args:
        instance: Python object to share
        name: Name to reference in CSSL as $name

    Returns:
        Path to the shared object marker file

    Usage:
        from includecpp import CSSL

        data = {"count": 0}
        CSSL.share(data, "data")
        CSSL.run('$data.count = 10;')
        print(data["count"])  # 10
    """
    ...


def unshare(name: str) -> bool:
    """
    Remove a globally shared object.

    Args:
        name: Name of the shared object to remove

    Returns:
        True if removed, False if not found
    """
    ...


def get_shared(name: str) -> Optional[Any]:
    """
    Get a globally shared object by name.

    Args:
        name: Name of the shared object

    Returns:
        The live shared object or None if not found
    """
    ...


def shared(name: str) -> Optional[Any]:
    """
    Get a shared object by name (alias for get_shared).

    Args:
        name: Name of the shared object (without $ prefix)

    Returns:
        The live shared object or None if not found
    """
    ...


def set_global(name: str, value: Any) -> None:
    """Set a global variable in CSSL runtime."""
    ...


def get_global(name: str) -> Any:
    """Get a global variable from CSSL runtime."""
    ...


def get_output() -> List[str]:
    """Get output buffer from last execution."""
    ...


def clear_output() -> None:
    """Clear output buffer."""
    ...


# =============================================================================
# Deprecated Aliases (for backwards compatibility)
# =============================================================================

def exec(path_or_code: str, *args: Any) -> Any:
    """DEPRECATED: Use run() instead."""
    ...


def T_exec(
    path_or_code: str,
    *args: Any,
    callback: Optional[Callable[[Any], None]] = ...
) -> threading.Thread:
    """DEPRECATED: Use T_run() instead."""
    ...


def _exec(code: str, *args: Any) -> Any:
    """
    Execute CSSL code directly (alias to avoid conflict with Python builtin exec).

    Usage:
        from includecpp import CSSL
        CSSL._exec('''
            printl("Hello from CSSL!");
        ''')
    """
    ...


def _T_exec(
    code: str,
    *args: Any,
    callback: Optional[Callable[[Any], None]] = ...
) -> threading.Thread:
    """Execute CSSL code asynchronously (alias for T_exec)."""
    ...


__all__: List[str]
