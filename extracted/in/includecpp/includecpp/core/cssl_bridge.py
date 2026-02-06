"""
CSSL Bridge - Python API for CSSL Language
Provides CsslLang class for executing CSSL code from Python.

v3.8.0 API:
    cssl.run(code, *args)          - Execute CSSL code
    cssl.script("cssl", code)      - Create typed script
    cssl.makemodule(script, pl)    - Bundle main script + payload
    cssl.load(path, name)          - Load .cssl/.cssl-pl file
    cssl.execute(name)             - Execute loaded script
    cssl.include(path, name)       - Register for payload(name)
"""

import atexit
import os
import pickle
import random
import threading
import warnings
from pathlib import Path
from typing import Any, List, Optional, Callable, Dict, Union, Tuple


def _get_share_directory() -> Path:
    """Get the directory for shared objects."""
    # Use APPDATA on Windows, ~/.config on Unix
    if os.name == 'nt':
        base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    else:
        base = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config'))

    share_dir = base / 'IncludeCPP' / 'shared_objects'
    share_dir.mkdir(parents=True, exist_ok=True)
    return share_dir


def _cleanup_shared_objects() -> None:
    """Clean up all shared object marker files on process exit."""
    try:
        share_dir = _get_share_directory()
        if share_dir.exists():
            for f in share_dir.glob('*.shareobj*'):
                try:
                    f.unlink()
                except Exception:
                    pass
    except Exception:
        pass

# Register cleanup on process exit
atexit.register(_cleanup_shared_objects)


# Global live object registry - holds actual object references for live sharing
_live_objects: Dict[str, Any] = {}


class SharedObjectProxy:
    """
    Live proxy for accessing a shared Python object from CSSL.
    Changes made through this proxy are reflected in the original object.
    """

    def __init__(self, name: str, obj: Any = None):
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_direct_object', obj)

    def _get_object(self):
        """Get the live object reference."""
        # First check direct object (same-instance sharing)
        direct = object.__getattribute__(self, '_direct_object')
        if direct is not None:
            return direct

        # Fall back to global registry
        name = object.__getattribute__(self, '_name')
        if name in _live_objects:
            return _live_objects[name]

        return None

    def __getattr__(self, name: str):
        """Access attributes/methods on the shared object."""
        obj = self._get_object()
        if obj is None:
            obj_name = object.__getattribute__(self, '_name')
            raise AttributeError(f"Shared object '${obj_name}' not available")

        return getattr(obj, name)

    def __setattr__(self, name: str, value: Any):
        """Set attributes on the shared object (live update)."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
            return

        obj = self._get_object()
        if obj is None:
            obj_name = object.__getattribute__(self, '_name')
            raise AttributeError(f"Shared object '${obj_name}' not available")

        setattr(obj, name, value)

    def __repr__(self):
        obj = self._get_object()
        name = object.__getattribute__(self, '_name')
        return f"<SharedObject ${name} type={type(obj).__name__ if obj else 'None'}>"

    def __call__(self, *args, **kwargs):
        """Allow calling the object if it's callable."""
        obj = self._get_object()
        if obj is None:
            name = object.__getattribute__(self, '_name')
            raise TypeError(f"Shared object '${name}' not available")
        if callable(obj):
            return obj(*args, **kwargs)
        name = object.__getattribute__(self, '_name')
        raise TypeError(f"Shared object '${name}' is not callable")

    def __getitem__(self, key):
        """Allow indexing on the shared object."""
        obj = self._get_object()
        if obj is None:
            name = object.__getattribute__(self, '_name')
            raise KeyError(f"Shared object '${name}' not available")
        return obj[key]

    def __setitem__(self, key, value):
        """Allow setting items on the shared object (live update)."""
        obj = self._get_object()
        if obj is None:
            name = object.__getattribute__(self, '_name')
            raise KeyError(f"Shared object '${name}' not available")
        obj[key] = value

    def __iter__(self):
        """Allow iterating over the shared object."""
        obj = self._get_object()
        if obj is None:
            name = object.__getattribute__(self, '_name')
            raise TypeError(f"Shared object '${name}' not available")
        return iter(obj)

    def __len__(self):
        """Get length of the shared object."""
        obj = self._get_object()
        if obj is None:
            return 0
        return len(obj)


class CSSLModule:
    """
    A callable CSSL module that executes code with arguments.

    Created via CSSL.module() - the code is executed each time the module is called,
    with arguments accessible via parameter.get(index).
    """

    def __init__(self, cssl_instance: 'CsslLang', code: str):
        self._cssl = cssl_instance
        self._code = code

    def __call__(self, *args) -> Any:
        """Execute the module code with the given arguments."""
        return self._cssl.exec(self._code, *args)

    def __repr__(self) -> str:
        return f"<CSSLModule code_len={len(self._code)}>"


class CSSLScript:
    """
    A typed CSSL script object.

    Created via cssl.script("cssl", code) or cssl.script("cssl-pl", code).
    Can be executed directly or bundled into a module.

    Usage:
        main = cssl.script("cssl", '''
            printl("Main script");
            myFunc();
        ''')

        payload = cssl.script("cssl-pl", '''
            void myFunc() {
                printl("From payload!");
            }
        ''')

        # Execute directly
        main.run()

        # Or bundle into module
        mod = cssl.makemodule(main, payload, "mymod")
    """

    def __init__(self, cssl_instance: 'CsslLang', script_type: str, code: str, params: Tuple = ()):
        """
        Initialize a CSSL script.

        Args:
            cssl_instance: The parent CsslLang instance
            script_type: "cssl" for main script, "cssl-pl" for payload
            code: The CSSL code
            params: Optional parameters accessible via parameter.get(index)
        """
        if script_type not in ('cssl', 'cssl-pl'):
            raise ValueError(f"Invalid script type '{script_type}'. Must be 'cssl' or 'cssl-pl'")

        self._cssl = cssl_instance
        self._type = script_type
        self._code = code
        self._params = params
        self._name: Optional[str] = None

    @property
    def type(self) -> str:
        """Get script type ('cssl' or 'cssl-pl')."""
        return self._type

    @property
    def code(self) -> str:
        """Get the script code."""
        return self._code

    @property
    def is_payload(self) -> bool:
        """Check if this is a payload script."""
        return self._type == 'cssl-pl'

    def run(self, *args) -> Any:
        """Execute this script with optional arguments."""
        all_args = self._params + args
        return self._cssl.run(self._code, *all_args)

    def __call__(self, *args) -> Any:
        """Allow calling the script directly."""
        return self.run(*args)

    def __repr__(self) -> str:
        return f"<CSSLScript type='{self._type}' code_len={len(self._code)}>"


class CSSLFunctionModule:
    """
    A CSSL module with accessible functions as methods.

    Created via CSSL.makemodule() - functions defined in the CSSL code
    become callable attributes on this module.
    """

    def __init__(self, cssl_instance: 'CsslLang', code: str, payload_code: str = None, name: str = None):
        self._cssl = cssl_instance
        self._code = code
        self._payload_code = payload_code
        self._name = name
        self._runtime = None
        self._functions: Dict[str, Any] = {}
        self._initialized = False

    def _ensure_initialized(self):
        """Initialize the module by parsing and registering functions."""
        if self._initialized:
            return

        from .cssl import CSSLRuntime, parse_cssl_program, ASTNode

        # Create a dedicated runtime for this module, preserving output_callback
        self._runtime = CSSLRuntime(output_callback=self._cssl._output_callback)

        # If we have a payload, load it first (defines functions/globals for main)
        if self._payload_code:
            payload_ast = parse_cssl_program(self._payload_code)
            for child in payload_ast.children:
                if child.type == 'function':
                    func_info = child.value
                    func_name = func_info.get('name')
                    self._functions[func_name] = child
                    self._runtime.scope.set(func_name, child)
                else:
                    try:
                        self._runtime._execute_node(child)
                    except Exception:
                        pass

        # Parse the main code
        ast = parse_cssl_program(self._code)

        # Execute to register all function definitions
        for child in ast.children:
            if child.type == 'function':
                func_info = child.value
                func_name = func_info.get('name')
                self._functions[func_name] = child
                self._runtime.scope.set(func_name, child)
            else:
                # Execute other statements (like struct definitions)
                try:
                    self._runtime._execute_node(child)
                except Exception:
                    pass

        # If module has a name, register for payload() access
        if self._name:
            cssl_instance = self._cssl
            runtime = cssl_instance._get_runtime()
            if not hasattr(runtime, '_inline_payloads'):
                runtime._inline_payloads = {}
            # Store combined code for payload() access
            combined = (self._payload_code or '') + '\n' + self._code
            runtime._inline_payloads[self._name] = combined

        self._initialized = True

    def __getattr__(self, name: str) -> Callable:
        """Get a function from the module."""
        # Avoid recursion for internal attributes
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        self._ensure_initialized()

        if name in self._functions:
            func_node = self._functions[name]

            def wrapper(*args):
                from .cssl import Parameter
                # Set up parameter object for this call
                self._runtime.global_scope.set('parameter', Parameter(list(args)))
                self._runtime.global_scope.set('args', list(args))
                self._runtime.global_scope.set('argc', len(args))
                # Enable running flag for function execution
                self._runtime._running = True
                try:
                    return self._runtime._call_function(func_node, list(args))
                finally:
                    self._runtime._running = False

            return wrapper

        raise AttributeError(f"CSSL module has no function '{name}'")

    def __dir__(self) -> List[str]:
        """List available functions."""
        self._ensure_initialized()
        return list(self._functions.keys())

    def __repr__(self) -> str:
        self._ensure_initialized()
        funcs = ', '.join(self._functions.keys())
        return f"<CSSLFunctionModule functions=[{funcs}]>"


class CsslLang:
    """
    CSSL Language interface for Python.

    v3.8.0 API:
        from includecpp import CSSL
        cssl = CSSL.CsslLang()

        # Execute CSSL code
        result = cssl.run("script.cssl", arg1, arg2)
        result = cssl.run('''printl("Hello");''')

        # Create typed scripts
        main = cssl.script("cssl", '''printl("Main");''')
        payload = cssl.script("cssl-pl", '''void helper() {}''')

        # Bundle into module
        mod = cssl.makemodule(main, payload, "mymod")

        # Load and execute files
        cssl.load("utils.cssl-pl", "utils")
        cssl.execute("utils")

        # Register for payload() access
        cssl.include("helpers.cssl-pl", "helpers")
    """

    def __init__(self, output_callback: Optional[Callable[[str, str], None]] = None):
        """
        Initialize CSSL runtime.

        Args:
            output_callback: Optional callback for output (text, level)
        """
        self._output_callback = output_callback
        self._runtime = None
        self._threads: List[threading.Thread] = []
        self._loaded_scripts: Dict[str, Dict[str, Any]] = {}

    def _get_runtime(self):
        """Lazy load CSSL runtime."""
        if self._runtime is None:
            from .cssl import CSSLRuntime
            self._runtime = CSSLRuntime(output_callback=self._output_callback)
        return self._runtime

    def _detect_type(self, path: str) -> str:
        """Detect script type from file extension."""
        path_obj = Path(path)
        if path_obj.suffix == '.cssl-pl':
            return 'cssl-pl'
        return 'cssl'

    def run(self, path_or_code: str, *args, force_python: bool = False) -> Any:
        """
        Execute CSSL code or file.

        This is the primary method for running CSSL code in v3.8.0+.
        Uses C++ acceleration when available (375x+ faster).

        Args:
            path_or_code: Path to .cssl file or CSSL code string
            *args: Arguments to pass to the script (accessible via parameter.get())
            force_python: Force Python interpreter (for full builtin support)

        Returns:
            Execution result. If parameter.return() was called, returns
            the list of returned values (or single value if only one).

        Usage:
            cssl.run("script.cssl", "arg1", 42)
            cssl.run('''
                printl("Hello " + parameter.get(0));
            ''', "World")
        """
        # Check if it's a file path (not code)
        # Code detection: contains newlines, semicolons, or braces = definitely code
        is_likely_code = '\n' in path_or_code or ';' in path_or_code or '{' in path_or_code
        source = path_or_code
        is_file = False
        file_path = None

        if not is_likely_code:
            try:
                path = Path(path_or_code)
                if path.exists() and path.suffix in ('.cssl', '.cssl-mod', '.cssl-pl'):
                    is_file = True
                    file_path = str(path.absolute())
                    source = path.read_text(encoding='utf-8')
            except OSError:
                # Path too long or invalid - treat as code
                pass

        # v4.6.5: Check for native/unative keywords
        import re
        has_native = bool(re.search(r'\bnative\b', source))
        has_unative = bool(re.search(r'\bunative\b', source))

        # v4.8.5: Python-only builtins (not available in C++ runtime)
        # Auto-detect and use Python when these are present
        PYTHON_ONLY_BUILTINS = {
            # os/sys replacements
            'getcwd', 'chdir', 'mkdir', 'rmdir', 'rmfile', 'rename',
            'argv', 'argc', 'platform', 'version', 'exit',
            # File operations
            'listdir', 'makedirs', 'removefile', 'removedir', 'copyfile', 'movefile',
            'readfile', 'writefile', 'appendfile', 'readlines', 'filesize',
            'pathexists', 'exists', 'isfile', 'isdir',
            # Environment
            'env', 'setenv',
            # Module imports
            'pyimport', 'cppimport', 'include', 'libinclude',
            # Advanced features
            'initpy', 'initsh', 'appexec', 'createcmd',
            # Instance reflection
            'instance_getMethods', 'instance_getClasses', 'instance_getVars',
            'instance_getAll', 'instance_call', 'instance_has', 'instance_type',
            # Console/terminal functions
            'clear', 'input', 'color',
            'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'white', 'black',
            'bold', 'dim', 'italic', 'underline', 'blink', 'reverse',
            # v4.9.0: Memory introspection and snapshot (Python reflection)
            'memory', 'snapshot', 'address', 'reflect',
        }

        # Check if source uses any Python-only builtins
        needs_python = any(
            re.search(rf'\b{builtin}\s*\(', source)
            for builtin in PYTHON_ONLY_BUILTINS
        )

        # Also detect module usage that requires Python runtime
        has_python_modules = bool(re.search(r'\b(fmt|Console|Process|Config|Server)::',  source))

        # v4.9.3: Detect python:: namespace usage (parameter passing, pythonize, etc.)
        has_python_namespace = bool(re.search(r'\bpython::', source))

        # v4.9.0: Detect bit/byte/address type declarations (Python-only types)
        has_binary_types = bool(re.search(r'\b(bit|byte|address)\s+\w+', source))

        # unative forces Python execution (skip C++ entirely)
        # force_python flag also skips C++ (for full builtin support like getcwd, listdir)
        # Auto-detect Python-only builtins and use Python automatically
        # v4.9.0: Also skip C++ for bit/byte types (Python-only)
        # v4.9.3: Also skip C++ for python:: namespace usage
        if has_unative or force_python or needs_python or has_python_modules or has_binary_types or has_python_namespace:
            pass  # Skip C++ block, go directly to Python execution
        # Try C++ accelerated execution first (375x faster)
        # Only use C++ for simple scripts without parameter passing
        elif not args:
            try:
                from .cssl import run_cssl, run_cssl_file
                if is_file and file_path:
                    return run_cssl_file(file_path)
                else:
                    return run_cssl(source)
            except Exception as cpp_error:
                # native keyword forces C++ - no fallback allowed
                if has_native:
                    raise RuntimeError(f"C++ execution failed (native mode): {cpp_error}") from cpp_error

                # Fall back to Python for unsupported features
                # v4.8.5: Extended fallback triggers for advanced CSSL syntax
                error_msg = str(cpp_error).lower()
                fallback_triggers = [
                    'unsupported', 'not implemented', 'unexpected', 'expected',
                    'syntax error', 'unknown identifier', 'undefined', 'not defined'
                ]
                should_fallback = any(trigger in error_msg for trigger in fallback_triggers)
                if not should_fallback:
                    # Real error - re-raise it
                    raise RuntimeError(str(cpp_error)) from cpp_error
                # Otherwise fall through to Python

        # Python execution (for scripts with args or when C++ fails)
        runtime = self._get_runtime()

        # v4.8.5: Strip unative directive before parsing (it's just a marker)
        if has_unative:
            source = re.sub(r'\bunative\s*;?\s*', '', source, count=1)

        # Set arguments in runtime scope
        from .cssl import Parameter
        param = Parameter(list(args))
        runtime.global_scope.set('args', list(args))
        runtime.global_scope.set('argc', len(args))
        runtime.global_scope.set('parameter', param)

        # Execute as standalone program
        try:
            result = runtime.execute_program(source)

            # Check if parameter.return() was used (generator-like returns)
            if param.has_returns():
                returns = param.returns()
                # Return single value if only one, else return list
                return returns[0] if len(returns) == 1 else returns

            return result
        except UnicodeEncodeError as e:
            # v4.3.2: Catch unicode/emoji encoding errors and provide helpful message
            char = e.object[e.start:e.end] if hasattr(e, 'object') else '?'
            error_msg = (
                f"Unicode encoding error: Character '{char}' cannot be displayed.\n"
                f"  The console encoding ({e.encoding}) doesn't support this character.\n\n"
                f"  Hint: Use encode() to safely handle emojis/unicode:\n"
                f"    printl(\"Status: \" + encode(\"{char}\"));\n"
                f"    printl(encode(\"Your text with emojis\", \"[emoji]\"));"
            )
            raise RuntimeError(error_msg) from e
        except Exception as e:
            # Format error message nicely - don't add prefixes, let CLI handle that
            error_msg = str(e)
            # Strip any existing CSSL Error: prefix to avoid duplication
            if error_msg.startswith("CSSL Error:"):
                error_msg = error_msg[11:].strip()
            raise RuntimeError(error_msg) from e

    def exec(self, path_or_code: str, *args) -> Any:
        """
        Execute CSSL code or file.

        DEPRECATED: Use run() instead. This method is kept for backwards compatibility.

        Args:
            path_or_code: Path to .cssl file or CSSL code string
            *args: Arguments to pass to the script

        Returns:
            Execution result
        """
        warnings.warn(
            "exec() is deprecated, use run() instead",
            DeprecationWarning,
            stacklevel=2
        )
        return self.run(path_or_code, *args)

    def T_run(self, path_or_code: str, *args, callback: Optional[Callable[[Any], None]] = None) -> threading.Thread:
        """
        Execute CSSL code asynchronously in a thread.

        Args:
            path_or_code: Path to .cssl file or CSSL code string
            *args: Arguments to pass to the script
            callback: Optional callback when execution completes

        Returns:
            Thread object
        """
        def _run_async():
            try:
                result = self.run(path_or_code, *args)
                if callback:
                    callback(result)
            except Exception as e:
                if callback:
                    callback(e)

        thread = threading.Thread(target=_run_async, daemon=True)
        thread.start()
        self._threads.append(thread)
        return thread

    def T_exec(self, path_or_code: str, *args, callback: Optional[Callable[[Any], None]] = None) -> threading.Thread:
        """
        Execute CSSL code asynchronously in a thread.

        DEPRECATED: Use T_run() instead.
        """
        warnings.warn(
            "T_exec() is deprecated, use T_run() instead",
            DeprecationWarning,
            stacklevel=2
        )
        return self.T_run(path_or_code, *args, callback=callback)

    def wait_all(self, timeout: Optional[float] = None):
        """Wait for all async executions to complete."""
        for thread in self._threads:
            thread.join(timeout=timeout)
        self._threads.clear()

    def get_output(self) -> List[str]:
        """Get output buffer from last execution."""
        runtime = self._get_runtime()
        return list(runtime.output_buffer)

    def clear_output(self):
        """Clear output buffer."""
        runtime = self._get_runtime()
        runtime.output_buffer.clear()

    def set_global(self, name: str, value: Any):
        """Set a global variable in CSSL runtime."""
        runtime = self._get_runtime()
        runtime.global_scope.set(name, value)

    def get_global(self, name: str) -> Any:
        """Get a global variable from CSSL runtime."""
        runtime = self._get_runtime()
        return runtime.global_scope.get(name)

    def module(self, code: str) -> 'CSSLModule':
        """
        Create a callable CSSL module from code.

        The module can be called with arguments that are passed to the CSSL code.

        Usage:
            module = CSSL.module('''
                printl(parameter.get(0));
            ''')
            module("Hello")  # Prints "Hello"

        Args:
            code: CSSL code string

        Returns:
            CSSLModule - a callable module
        """
        return CSSLModule(self, code)

    def script(self, script_type: str, code: str, *params) -> 'CSSLScript':
        """
        Create a typed CSSL script.

        Args:
            script_type: "cssl" for main script, "cssl-pl" for payload
            code: The CSSL code
            *params: Optional parameters accessible via parameter.get(index)

        Returns:
            CSSLScript object that can be executed or bundled

        Usage:
            main = cssl.script("cssl", '''
                printl("Main script running");
                helper();
            ''')

            payload = cssl.script("cssl-pl", '''
                void helper() {
                    printl("Helper called!");
                }
            ''')

            # Execute directly
            main.run()

            # Or bundle into module
            mod = cssl.makemodule(main, payload, "mymod")
        """
        return CSSLScript(self, script_type, code, params)

    def makemodule(
        self,
        main_script: Union[str, 'CSSLScript'],
        payload_script: Union[str, 'CSSLScript', None] = None,
        name: str = None,
        bind: str = None
    ) -> 'CSSLFunctionModule':
        """
        Create a CSSL module with accessible functions.

        Functions defined in the code become methods on the returned module.
        Optionally registers the module for payload() access in other scripts.

        Args:
            main_script: Main CSSL code, file path, or CSSLScript
            payload_script: Optional payload code (string or CSSLScript)
            name: Optional name to register for payload(name) access
            bind: Optional payload name to auto-prepend (from makepayload)

        Returns:
            CSSLFunctionModule - module with callable function attributes

        Usage (simplified - with file path and bind):
            # First register the payload
            cssl.makepayload("api", "lib/api/einkaufsmanager.cssl-pl")

            # Then create module from file, binding to payload
            mod = cssl.makemodule("writer", "lib/writer.cssl", bind="api")
            mod.SaySomething("Hello!")  # Functions are now accessible

        Usage (v3.8.0 - with CSSLScript objects):
            main = cssl.script("cssl", '''
                printl("Main");
                helper();
            ''')
            payload = cssl.script("cssl-pl", '''
                void helper() { printl("Helper!"); }
            ''')
            mod = cssl.makemodule(main, payload, "mymod")
            mod.helper()  # Direct call

            # Also available in other scripts:
            cssl.run('''
                payload("mymod");
                helper();  // Works!
            ''')

        Usage (legacy - code string):
            module = cssl.makemodule('''
                string greet(string name) {
                    return "Hello, " + name + "!";
                }
            ''')
            module.greet("World")  # Returns "Hello, World!"
        """
        # Handle simplified API: makemodule(name, path, bind=...)
        # Check if main_script looks like a short identifier and payload_script looks like a path
        if (isinstance(main_script, str) and isinstance(payload_script, str) and
            not '\n' in main_script and not ';' in main_script and not '{' in main_script):
            # main_script is likely a name, payload_script is likely a path
            module_name = main_script
            path = payload_script

            # Check if it's actually a file path
            path_obj = Path(path)
            if path_obj.exists():
                main_code = path_obj.read_text(encoding='utf-8')

                # If bind is specified, prepend that payload's code
                payload_code = None
                if bind:
                    runtime = self._get_runtime()
                    if hasattr(runtime, '_inline_payloads') and bind in runtime._inline_payloads:
                        payload_code = runtime._inline_payloads[bind]

                return CSSLFunctionModule(self, main_code, payload_code, module_name)

        # Extract code from CSSLScript objects if provided
        if isinstance(main_script, CSSLScript):
            main_code = main_script.code
        else:
            main_code = main_script

        payload_code = None
        if payload_script is not None:
            if isinstance(payload_script, CSSLScript):
                payload_code = payload_script.code
            else:
                payload_code = payload_script

        # If bind is specified and no payload_script, use the bound payload
        if bind and payload_code is None:
            runtime = self._get_runtime()
            if hasattr(runtime, '_inline_payloads') and bind in runtime._inline_payloads:
                payload_code = runtime._inline_payloads[bind]

        return CSSLFunctionModule(self, main_code, payload_code, name)

    def load(self, path: str, name: str) -> None:
        """
        Load a .cssl or .cssl-pl file and register by name.

        The file becomes accessible for execute(name) or payload(name).

        Args:
            path: Path to the .cssl or .cssl-pl file
            name: Name to register the script under

        Usage:
            cssl.load("utils.cssl-pl", "utils")
            cssl.execute("utils")  # Run it

            # Or in CSSL code:
            cssl.run('''
                payload("utils");  // Loads the registered file
            ''')
        """
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"CSSL file not found: {path}")

        script_type = self._detect_type(path)
        code = path_obj.read_text(encoding='utf-8')

        self._loaded_scripts[name] = {
            'path': str(path_obj.absolute()),
            'type': script_type,
            'code': code
        }

        # Also register for payload() access
        runtime = self._get_runtime()
        if not hasattr(runtime, '_inline_payloads'):
            runtime._inline_payloads = {}
        runtime._inline_payloads[name] = code

    def execute(self, name: str, *args) -> Any:
        """
        Execute a previously loaded script by name.

        Args:
            name: Name of the loaded script
            *args: Arguments to pass to the script

        Returns:
            Execution result

        Usage:
            cssl.load("utils.cssl-pl", "utils")
            result = cssl.execute("utils", arg1, arg2)
        """
        if name not in self._loaded_scripts:
            raise KeyError(f"No script loaded with name '{name}'. Use load() first.")

        script_info = self._loaded_scripts[name]
        return self.run(script_info['code'], *args)

    def include(self, path: str, name: str) -> None:
        """
        Register a file to be accessible via payload(name) or include(name) in CSSL.

        Unlike load(), this doesn't store the script for execute() - it only
        makes it available for payload() calls within CSSL code.

        Args:
            path: Path to the .cssl or .cssl-pl file
            name: Name for payload() access

        Usage:
            cssl.include("helpers.cssl-pl", "helpers")
            cssl.run('''
                payload("helpers");
                // Functions from helpers are now available
            ''')
        """
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"CSSL file not found: {path}")

        code = path_obj.read_text(encoding='utf-8')

        runtime = self._get_runtime()
        if not hasattr(runtime, '_inline_payloads'):
            runtime._inline_payloads = {}
        runtime._inline_payloads[name] = code

    def code(self, name: str, code: str) -> None:
        """
        Register inline CSSL code as a payload that can be loaded via payload().

        This allows creating payloads from Python code without external files.

        Usage:
            from includecpp import CSSL
            cssl = CSSL.CsslLang()

            # Register a helper payload
            cssl.code("helpers", '''
                global version = "1.0.0";
                void log(string msg) {
                    printl("[LOG] " + msg);
                }
            ''')

            # Use it in CSSL code
            cssl.exec('''
                payload("helpers");  // Load the inline payload
                @log("Hello!");      // Call the helper function
                printl(@version);    // Access the global
            ''')

        Args:
            name: Name to register the payload under (used in payload("name"))
            code: CSSL code string
        """
        runtime = self._get_runtime()
        if not hasattr(runtime, '_inline_payloads'):
            runtime._inline_payloads = {}
        runtime._inline_payloads[name] = code

    def makepayload(self, name: str, path: str) -> str:
        """
        Register a payload from a file path.

        Reads the file and registers it as a payload accessible via payload(name) in CSSL.
        This is a convenience method that combines reading a file and calling code().

        Usage:
            from includecpp import CSSL
            cssl = CSSL.CsslLang()

            # Register a payload from file
            cssl.makepayload("api", "lib/api/myapi.cssl-pl")

            # Now use in CSSL code
            cssl.run('''
                payload("api");  // Load the payload
                myApiFunction();  // Call functions from it
            ''')

            # Or use with makemodule for automatic binding
            mod = cssl.makemodule("writer", "lib/writer.cssl", bind="api")
            mod.SaySomething("Hello!")

        Args:
            name: Name to register the payload under (used in payload(name) and bind=name)
            path: Path to the .cssl-pl or .cssl file

        Returns:
            The payload code that was registered
        """
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Payload file not found: {path}")

        code = path_obj.read_text(encoding='utf-8')
        self.code(name, code)
        return code

    def share(self, instance: Any, name: str = None) -> str:
        """
        Share a Python object instance with CSSL scripts (LIVE sharing).

        The object is stored as a LIVE reference - changes made in CSSL
        will be reflected in the original Python object immediately.
        Call share() again with the same name to update the shared object.

        Args:
            instance: The Python object to share (or name if using old API)
            name: The name to reference the object in CSSL ($name)

        Note: Arguments can be passed in either order:
            cssl.share(my_object, "name")  # Preferred
            cssl.share("name", my_object)  # Also works

        Usage in Python:
            from includecpp import CSSL
            cssl = CSSL.CsslLang()

            # Share a Python object
            class MyAPI:
                def __init__(self):
                    self.counter = 0
                def greet(self, name):
                    return f"Hello, {name}!"
                def increment(self):
                    self.counter += 1

            api = MyAPI()
            cssl.share(api, "myapi")

            # Use in CSSL - changes are LIVE!
            cssl.exec('''
                ob <== $myapi;
                printl(ob.greet("World"));
                ob.increment();
                printl(ob.counter);  // 1
            ''')

            # Changes reflect back to Python!
            print(api.counter)  # 1

        Args:
            instance: Python object to share
            name: Name for the shared object (accessed as $name in CSSL)

        Returns:
            Path to the shared object marker file
        """
        global _live_objects
        runtime = self._get_runtime()

        # Handle argument order flexibility: share(instance, name) or share(name, instance)
        if name is None:
            # Only one argument - use object type as name
            name = type(instance).__name__
        elif isinstance(instance, str) and not isinstance(name, str):
            # Arguments are swapped: share("name", instance) -> swap them
            instance, name = name, instance
        elif not isinstance(name, str):
            # name is not a string - use its type as name
            name = type(name).__name__

        # Sanitize filename: remove invalid characters for Windows
        import re
        safe_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(name))

        # Initialize shared objects registry
        if not hasattr(runtime, '_shared_objects'):
            runtime._shared_objects = {}

        # Generate unique filename: <name>.shareobj<7digits>
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        share_dir = _get_share_directory()
        filepath = share_dir / f"{safe_name}.shareobj{random_suffix}"

        # Remove old file if updating
        if name in runtime._shared_objects:
            old_path = runtime._shared_objects[name]['path']
            try:
                Path(old_path).unlink(missing_ok=True)
            except Exception:
                pass

        # Store LIVE object reference in global registry
        _live_objects[name] = instance

        # Write marker file with metadata (not the actual object)
        import json
        metadata = {
            'name': name,
            'type': type(instance).__name__,
            'live': True,
            'id': id(instance)
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f)

        # Register in runtime
        runtime._shared_objects[name] = {
            'path': str(filepath),
            'type': type(instance).__name__,
            'live': True
        }

        # Also register the live proxy in the runtime's scope for $name access
        proxy = SharedObjectProxy(name, instance)
        runtime.global_scope.set(f'${name}', proxy)

        return str(filepath)

    def unshare(self, name: str) -> bool:
        """
        Remove a shared object.

        Args:
            name: Name of the shared object to remove

        Returns:
            True if removed, False if not found
        """
        global _live_objects
        runtime = self._get_runtime()

        if not hasattr(runtime, '_shared_objects'):
            return False

        if name not in runtime._shared_objects:
            return False

        # Remove from live objects registry
        if name in _live_objects:
            del _live_objects[name]

        # Remove from runtime scope
        try:
            runtime.global_scope.delete(f'${name}')
        except Exception:
            pass

        # Remove marker file
        filepath = runtime._shared_objects[name]['path']
        try:
            Path(filepath).unlink(missing_ok=True)
        except Exception:
            pass

        del runtime._shared_objects[name]
        return True

    def get_shared(self, name: str) -> Optional[Any]:
        """
        Get a shared object by name (for Python-side access).

        Returns the actual live object reference, not a copy.

        Args:
            name: Name of the shared object

        Returns:
            The live shared object or None if not found
        """
        global _live_objects

        # Return live object if available
        if name in _live_objects:
            return _live_objects[name]

        return None

    def shared(self, name: str) -> Optional[Any]:
        """
        Get a shared object by name (alias for get_shared).

        Returns the actual live object reference, not a copy.
        Works with both Python cssl.share() and CSSL ==> $name shared objects.

        Usage:
            from includecpp import CSSL
            cssl = CSSL.CsslLang()

            # Share an object
            my_obj = {"value": 42}
            cssl.share(my_obj, "data")

            # Retrieve it later
            obj = cssl.shared("data")
            print(obj["value"])  # 42

        Args:
            name: Name of the shared object (without $ prefix)

        Returns:
            The live shared object or None if not found
        """
        return self.get_shared(name)

    def getInstance(self, name: str) -> Optional[Any]:
        """
        Get a universal instance by name (for Python-side access).

        Universal instances are shared containers accessible from CSSL, Python, and C++.
        They support dynamic member/method access and are mutable across all contexts.

        Usage:
            from includecpp import CSSL
            cssl = CSSL.CsslLang()

            # In CSSL: instance<"myContainer"> container;
            # Then in Python:
            container = cssl.getInstance("myContainer")
            container.member = "value"
            print(container.member)  # value

        Args:
            name: Name of the instance (without quotes)

        Returns:
            The UniversalInstance or None if not found
        """
        from .cssl.cssl_types import UniversalInstance
        return UniversalInstance.get(name)

    def createInstance(self, name: str) -> Any:
        """
        Create or get a universal instance by name (for Python-side creation).

        Usage:
            container = cssl.createInstance("myContainer")
            container.data = {"key": "value"}
            # Now accessible in CSSL via instance<"myContainer">

        Args:
            name: Name for the instance

        Returns:
            The UniversalInstance (new or existing)
        """
        from .cssl.cssl_types import UniversalInstance
        return UniversalInstance.get_or_create(name)

    def deleteInstance(self, name: str) -> bool:
        """
        Delete a universal instance by name.

        Args:
            name: Name of the instance to delete

        Returns:
            True if deleted, False if not found
        """
        from .cssl.cssl_types import UniversalInstance
        return UniversalInstance.delete(name)

    def listInstances(self) -> list:
        """
        List all universal instance names.

        Returns:
            List of instance names
        """
        from .cssl.cssl_types import UniversalInstance
        return UniversalInstance.list_all()


# Global shared objects registry (for cross-instance sharing)
_global_shared_objects: Dict[str, str] = {}


def share(instance: Any, name: str = None) -> str:
    """
    Share a Python object globally for all CSSL instances (LIVE sharing).

    Changes made through CSSL will reflect back to the original object.

    Args can be passed in either order:
        share(my_object, "name")  # Preferred
        share("name", my_object)  # Also works
    """
    global _live_objects
    import re

    # Handle argument order flexibility
    if name is None:
        name = type(instance).__name__
    elif isinstance(instance, str) and not isinstance(name, str):
        instance, name = name, instance
    elif not isinstance(name, str):
        name = type(name).__name__

    # Sanitize filename
    safe_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(name))

    random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    share_dir = _get_share_directory()
    filepath = share_dir / f"{safe_name}.shareobj{random_suffix}"

    # Remove old file if updating
    if name in _global_shared_objects:
        try:
            Path(_global_shared_objects[name]).unlink(missing_ok=True)
        except Exception:
            pass

    # Store LIVE object reference
    _live_objects[name] = instance

    # Write marker file with metadata
    import json
    metadata = {
        'name': name,
        'type': type(instance).__name__,
        'live': True,
        'id': id(instance)
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(metadata, f)

    _global_shared_objects[name] = str(filepath)
    return str(filepath)


def unshare(name: str) -> bool:
    """Remove a globally shared object."""
    global _live_objects

    if name not in _global_shared_objects:
        return False

    # Remove from live objects
    if name in _live_objects:
        del _live_objects[name]

    try:
        Path(_global_shared_objects[name]).unlink(missing_ok=True)
    except Exception:
        pass

    del _global_shared_objects[name]
    return True


def get_shared(name: str) -> Optional[Any]:
    """Get a globally shared object by name."""
    global _live_objects
    return _live_objects.get(name)


def shared(name: str) -> Optional[Any]:
    """
    Get a shared object by name (alias for get_shared).

    Works with both Python share() and CSSL ==> $name shared objects.

    Usage:
        from includecpp import CSSL

        # Share an object
        my_obj = {"value": 42}
        CSSL.share(my_obj, "data")

        # Retrieve it later
        obj = CSSL.shared("data")
        print(obj["value"])  # 42

    Args:
        name: Name of the shared object (without $ prefix)

    Returns:
        The live shared object or None if not found
    """
    return get_shared(name)


def cleanup_shared() -> int:
    """
    Manually clean up all shared object marker files.

    Call this to remove stale .shareobj files from %APPDATA%/IncludeCPP/shared_objects/
    that may have accumulated from previous sessions.

    Returns:
        Number of files deleted
    """
    global _live_objects, _global_shared_objects

    count = 0
    try:
        share_dir = _get_share_directory()
        if share_dir.exists():
            for f in share_dir.glob('*.shareobj*'):
                try:
                    f.unlink()
                    count += 1
                except Exception:
                    pass
    except Exception:
        pass

    # Clear in-memory registries
    _live_objects.clear()
    _global_shared_objects.clear()

    return count


# Singleton for convenience
_default_instance: Optional[CsslLang] = None

def get_cssl() -> CsslLang:
    """Get default CSSL instance."""
    global _default_instance
    if _default_instance is None:
        _default_instance = CsslLang()
    return _default_instance


# Module-level convenience functions (v3.8.0 API)

def run(path_or_code: str, *args) -> Any:
    """
    Execute CSSL code or file.

    This is the primary method for running CSSL code in v3.8.0+.

    Usage:
        from includecpp import CSSL
        CSSL.run("script.cssl", arg1, arg2)
        CSSL.run("printl('Hello World');")

    Args:
        path_or_code: Path to .cssl file or CSSL code string
        *args: Arguments to pass to the script

    Returns:
        Execution result
    """
    return get_cssl().run(path_or_code, *args)


def exec(path_or_code: str, *args) -> Any:
    """
    Execute CSSL code or file.

    DEPRECATED: Use run() instead.
    """
    warnings.warn(
        "exec() is deprecated, use run() instead",
        DeprecationWarning,
        stacklevel=2
    )
    return get_cssl().run(path_or_code, *args)


def T_run(path_or_code: str, *args, callback: Optional[Callable[[Any], None]] = None) -> threading.Thread:
    """
    Execute CSSL code asynchronously in a thread.

    Usage:
        from includecpp import CSSL
        CSSL.T_run("async_script.cssl", arg1, callback=on_done)

    Args:
        path_or_code: Path to .cssl file or CSSL code string
        *args: Arguments to pass to the script
        callback: Optional callback when execution completes

    Returns:
        Thread object
    """
    return get_cssl().T_run(path_or_code, *args, callback=callback)


def T_exec(path_or_code: str, *args, callback: Optional[Callable[[Any], None]] = None) -> threading.Thread:
    """
    Execute CSSL code asynchronously in a thread.

    DEPRECATED: Use T_run() instead.
    """
    warnings.warn(
        "T_exec() is deprecated, use T_run() instead",
        DeprecationWarning,
        stacklevel=2
    )
    return get_cssl().T_run(path_or_code, *args, callback=callback)


def script(script_type: str, code: str, *params) -> CSSLScript:
    """
    Create a typed CSSL script.

    Usage:
        from includecpp import CSSL
        main = CSSL.script("cssl", '''printl("Main");''')
        payload = CSSL.script("cssl-pl", '''void helper() {}''')
        mod = CSSL.makemodule(main, payload, "mymod")

    Args:
        script_type: "cssl" for main script, "cssl-pl" for payload
        code: The CSSL code
        *params: Optional parameters

    Returns:
        CSSLScript object
    """
    return get_cssl().script(script_type, code, *params)


def load(path: str, name: str) -> None:
    """
    Load a .cssl or .cssl-pl file and register by name.

    Usage:
        CSSL.load("utils.cssl-pl", "utils")
        CSSL.execute("utils")
    """
    return get_cssl().load(path, name)


def execute(name: str, *args) -> Any:
    """
    Execute a previously loaded script by name.

    Usage:
        CSSL.load("utils.cssl-pl", "utils")
        result = CSSL.execute("utils", arg1, arg2)
    """
    return get_cssl().execute(name, *args)


def include(path: str, name: str) -> None:
    """
    Register a file for payload(name) access in CSSL.

    Usage:
        CSSL.include("helpers.cssl-pl", "helpers")
        CSSL.run('payload("helpers");')
    """
    return get_cssl().include(path, name)


def set_global(name: str, value: Any) -> None:
    """Set a global variable in CSSL runtime."""
    get_cssl().set_global(name, value)


def get_global(name: str) -> Any:
    """Get a global variable from CSSL runtime."""
    return get_cssl().get_global(name)


def get_output() -> List[str]:
    """Get output buffer from last execution."""
    return get_cssl().get_output()


def clear_output() -> None:
    """Clear output buffer."""
    get_cssl().clear_output()


# Aliases to avoid conflict with Python builtin exec
_run = run
_exec = exec
_T_run = T_run
_T_exec = T_exec


def module(code: str) -> CSSLModule:
    """
    Create a callable CSSL module from code.

    Usage:
        from includecpp import CSSL
        greet = CSSL.module('''
            printl("Hello, " + parameter.get(0) + "!");
        ''')
        greet("World")  # Prints "Hello, World!"

    Args:
        code: CSSL code string

    Returns:
        CSSLModule - a callable module
    """
    return get_cssl().module(code)


def makepayload(name: str, path: str) -> str:
    """
    Register a payload from a file path.

    Reads the file and registers it as a payload accessible via payload(name) in CSSL.

    Usage:
        from includecpp import CSSL

        # Register a payload from file
        CSSL.makepayload("api", "lib/api/myapi.cssl-pl")

        # Use with makemodule for automatic binding
        mod = CSSL.makemodule("writer", "lib/writer.cssl", bind="api")
        mod.SaySomething("Hello!")

    Args:
        name: Name to register the payload under (used in payload(name) and bind=name)
        path: Path to the .cssl-pl or .cssl file

    Returns:
        The payload code that was registered
    """
    return get_cssl().makepayload(name, path)


def makemodule(
    main_script: Union[str, CSSLScript],
    payload_script: Union[str, CSSLScript, None] = None,
    name: str = None,
    bind: str = None
) -> CSSLFunctionModule:
    """
    Create a CSSL module with accessible functions.

    Usage (simplified - with file path and bind):
        # First register the payload
        CSSL.makepayload("api", "lib/api/einkaufsmanager.cssl-pl")

        # Then create module from file, binding to payload
        mod = CSSL.makemodule("writer", "lib/writer.cssl", bind="api")
        mod.SaySomething("Hello!")

    Usage (v3.8.0 - with CSSLScript):
        main = CSSL.script("cssl", '''printl("Main");''')
        payload = CSSL.script("cssl-pl", '''void helper() {}''')
        mod = CSSL.makemodule(main, payload, "mymod")

    Usage (legacy - code string):
        math_mod = CSSL.makemodule('''
            int add(int a, int b) { return a + b; }
        ''')
        math_mod.add(2, 3)  # Returns 5

    Args:
        main_script: Main CSSL code, file path, or CSSLScript
        payload_script: Optional payload code (string or CSSLScript)
        name: Optional name to register for payload(name) access
        bind: Optional payload name to auto-prepend (from makepayload)

    Returns:
        CSSLFunctionModule - module with callable function attributes
    """
    return get_cssl().makemodule(main_script, payload_script, name, bind)


# =============================================================================
# v4.6.5: CsslWatcher - Live Python Instance Collection for CSSL Access
# =============================================================================

# Global registry of active watchers
_active_watchers: Dict[str, 'CsslWatcher'] = {}


class CsslWatcher:
    """
    Live Python instance watcher that collects all active instances, classes,
    and functions from the Python scope and makes them available to CSSL.

    Usage in Python:
        from includecpp.core.cssl_bridge import CsslWatcher

        cwatcher = CsslWatcher(id="MyWatcher")
        cwatcher.start()

        class Game:
            def __init__(self):
                self.score = 0
            def start(self):
                print("Game started!")

        game = Game()

        # ... later
        cwatcher.end()

    Usage in CSSL:
        # Get all instances from a watcher
        all_instances = watcher::get("MyWatcher");

        # Access Python class/instance
        pygameclass = all_instances['Game'];
        game_instance = all_instances['game'];

        # Call Python methods
        game_instance.start();

        # Bidirectional: CSSL can overwrite Python functions
        int start() : overwrites all_instances['Game.start'] {
            printl("Overwritten by CSSL!");
            return 0;
        }
    """

    def __init__(self, id: str, auto_collect: bool = True, depth: int = 1):
        """
        Initialize a new CsslWatcher.

        Args:
            id: Unique identifier for this watcher (used in watcher::get("id"))
            auto_collect: If True, automatically collect instances periodically
            depth: Stack frame depth to look for variables (1 = caller's scope)
        """
        self._id = id
        self._auto_collect = auto_collect
        self._depth = depth
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._instances: Dict[str, Any] = {}
        self._classes: Dict[str, type] = {}
        self._functions: Dict[str, Callable] = {}
        self._caller_frame = None
        self._caller_locals = {}
        self._caller_globals = {}

    @property
    def id(self) -> str:
        """Get the watcher ID."""
        return self._id

    def start(self) -> 'CsslWatcher':
        """
        Start the watcher. Collects instances from the caller's scope
        and registers this watcher globally.

        Returns:
            self for chaining
        """
        import inspect

        # Get caller's frame
        frame = inspect.currentframe()
        try:
            # Go up the stack to find the caller
            for _ in range(self._depth + 1):
                if frame.f_back:
                    frame = frame.f_back

            self._caller_frame = frame
            self._caller_locals = frame.f_locals
            self._caller_globals = frame.f_globals
        finally:
            del frame

        # Initial collection
        self._collect_instances()

        # Register globally
        with self._lock:
            _active_watchers[self._id] = self
            self._running = True

        # Start background thread if auto_collect
        if self._auto_collect:
            self._thread = threading.Thread(
                target=self._background_collect,
                daemon=True,
                name=f"CsslWatcher-{self._id}"
            )
            self._thread.start()

        return self

    def end(self) -> None:
        """Stop the watcher and unregister it."""
        with self._lock:
            self._running = False
            if self._id in _active_watchers:
                del _active_watchers[self._id]

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=1.0)

        self._caller_frame = None
        self._caller_locals = {}
        self._caller_globals = {}

    def stop(self) -> None:
        """Alias for end()."""
        self.end()

    def _collect_instances(self) -> None:
        """Collect all instances, classes, and functions from the watched scope."""
        import inspect

        with self._lock:
            # Combine locals and globals
            all_vars = {**self._caller_globals, **self._caller_locals}

            for name, obj in all_vars.items():
                # Skip private/magic names and modules
                if name.startswith('_'):
                    continue
                if inspect.ismodule(obj):
                    continue

                # Classify the object
                if inspect.isclass(obj):
                    self._classes[name] = obj
                    # Also collect class methods
                    for method_name, method in inspect.getmembers(obj, predicate=inspect.isfunction):
                        if not method_name.startswith('_'):
                            self._functions[f"{name}.{method_name}"] = method
                elif callable(obj) and not isinstance(obj, type):
                    self._functions[name] = obj
                elif hasattr(obj, '__class__') and not isinstance(obj, (int, float, str, bool, list, dict, tuple, set)):
                    # It's an instance of a custom class
                    self._instances[name] = obj
                    # Also collect instance methods
                    obj_class = obj.__class__
                    for method_name in dir(obj):
                        if not method_name.startswith('_'):
                            try:
                                method = getattr(obj, method_name)
                                if callable(method):
                                    self._functions[f"{name}.{method_name}"] = method
                            except Exception:
                                pass

    def _background_collect(self) -> None:
        """Background thread for periodic collection."""
        import time
        while self._running:
            time.sleep(0.5)  # Collect every 500ms
            if self._running:
                try:
                    self._collect_instances()
                except Exception:
                    pass

    def refresh(self) -> None:
        """Manually refresh the collected instances."""
        self._collect_instances()

    def get_all(self) -> Dict[str, Any]:
        """
        Get all collected items as a dictionary.

        Returns:
            Dict with all instances, classes, and functions
        """
        with self._lock:
            result = {}
            result.update(self._classes)
            result.update(self._instances)
            result.update(self._functions)
            return result

    def get(self, path: str) -> Any:
        """
        Get a specific item by path.

        Args:
            path: Name or dotted path like 'Game' or 'game.start'

        Returns:
            The requested object or None
        """
        with self._lock:
            # Check direct matches first
            if path in self._classes:
                return self._classes[path]
            if path in self._instances:
                return self._instances[path]
            if path in self._functions:
                return self._functions[path]

            # Handle dotted paths
            if '.' in path:
                parts = path.split('.', 1)
                base = parts[0]
                rest = parts[1]

                # Get the base object
                obj = self._instances.get(base) or self._classes.get(base)
                if obj:
                    try:
                        # Navigate the path
                        for part in rest.split('.'):
                            obj = getattr(obj, part)
                        return obj
                    except AttributeError:
                        pass

            return None

    def set(self, path: str, value: Any) -> bool:
        """
        Set/overwrite a value at the given path (bidirectional).

        Args:
            path: Name or dotted path like 'Game.start'
            value: New value (function, class, or instance)

        Returns:
            True if successful
        """
        with self._lock:
            if '.' in path:
                parts = path.rsplit('.', 1)
                base_path = parts[0]
                attr_name = parts[1]

                # Get the base object
                obj = self.get(base_path)
                if obj:
                    try:
                        setattr(obj, attr_name, value)
                        # Update our registry
                        self._functions[path] = value
                        return True
                    except Exception:
                        pass
            else:
                # Direct assignment to scope
                if callable(value) and not isinstance(value, type):
                    self._functions[path] = value
                elif isinstance(value, type):
                    self._classes[path] = value
                else:
                    self._instances[path] = value

                # Also update caller's scope
                if path in self._caller_locals:
                    self._caller_locals[path] = value
                elif path in self._caller_globals:
                    self._caller_globals[path] = value

                return True

        return False

    def __getitem__(self, key: str) -> Any:
        """Dict-like access: watcher['Game']"""
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Dict-like assignment: watcher['Game.start'] = new_func"""
        self.set(key, value)

    def __contains__(self, key: str) -> bool:
        """Check if key exists: 'Game' in watcher"""
        return self.get(key) is not None

    def __repr__(self) -> str:
        with self._lock:
            return (f"CsslWatcher(id='{self._id}', "
                    f"classes={len(self._classes)}, "
                    f"instances={len(self._instances)}, "
                    f"functions={len(self._functions)}, "
                    f"running={self._running})")


def watcher_get(watcher_id: str) -> Optional[Dict[str, Any]]:
    """
    Get all instances from a watcher by ID.
    This is the Python-side implementation for watcher::get("id").

    Args:
        watcher_id: The watcher's unique ID

    Returns:
        Dict of all collected instances, classes, and functions
    """
    if watcher_id in _active_watchers:
        return _active_watchers[watcher_id].get_all()
    return None


def watcher_set(watcher_id: str, path: str, value: Any) -> bool:
    """
    Set a value in a watcher (bidirectional overwrite).

    Args:
        watcher_id: The watcher's unique ID
        path: Path to the item (e.g., 'Game.start')
        value: New value

    Returns:
        True if successful
    """
    if watcher_id in _active_watchers:
        return _active_watchers[watcher_id].set(path, value)
    return False


def get_watcher(watcher_id: str) -> Optional[CsslWatcher]:
    """Get a watcher instance by ID."""
    return _active_watchers.get(watcher_id)


def list_watchers() -> List[str]:
    """List all active watcher IDs."""
    return list(_active_watchers.keys())


# =============================================================================
# v4.9.12: Extended CsslLang API - 20 New Professional Features
# =============================================================================

import asyncio
import time
import sys
import signal
import json
import io
import re
import traceback
import contextlib
from dataclasses import dataclass, field
from typing import Iterator, Set
from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError as FuturesTimeoutError


# -----------------------------------------------------------------------------
# Data Classes for Result Types
# -----------------------------------------------------------------------------

@dataclass
class ValidationResult:
    """Result of code validation."""
    valid: bool
    errors: List[dict] = field(default_factory=list)
    warnings: List[dict] = field(default_factory=list)

    def __bool__(self) -> bool:
        return self.valid


@dataclass
class ProfileResult:
    """Result of code profiling."""
    total_time_ms: float
    calls: Dict[str, int] = field(default_factory=dict)
    time_per_function: Dict[str, float] = field(default_factory=dict)
    hotspots: List[dict] = field(default_factory=list)
    call_tree: List[dict] = field(default_factory=list)


@dataclass
class BenchmarkResult:
    """Result of code benchmarking."""
    iterations: int
    avg_ms: float
    min_ms: float
    max_ms: float
    std_dev: float
    total_ms: float
    times: List[float] = field(default_factory=list)


@dataclass
class MemoryStats:
    """Memory statistics from CSSL runtime."""
    objects: int
    addresses: int
    shared: int
    bytes_used: int
    top_allocations: List[dict] = field(default_factory=list)
    scope_depth: int = 0
    global_count: int = 0


# -----------------------------------------------------------------------------
# 1. async_console() - Live Debugging GUI (Tkinter)
# -----------------------------------------------------------------------------

class CSSLDevConsole:
    """
    Tkinter-based CSSL developer console for live debugging.

    Features:
    - Multi-line CSSL code editor with syntax highlighting
    - Output panel with colored output (green=output, red=error, cyan=return)
    - API Tree showing all shared instances (dynamically introspected)
    - Double-click API tree items to insert into code editor
    - Ctrl+Enter to execute, history navigation

    Usage:
        from includecpp import CSSL

        # Share some objects
        CSSL.share(player, "player")
        CSSL.share(world, "world")

        # Launch console (non-blocking)
        await CSSL.async_console()

        # Or blocking:
        CSSL.async_console_sync()
    """

    def __init__(self, cssl_instance: 'CsslLang', shared_instances: list = None):
        self.cssl = cssl_instance
        self._thread: Optional[threading.Thread] = None
        self._root = None
        self._running = False
        self._history: list = []
        self._history_index = 0
        self._output_queue: 'queue.Queue' = None

        # Auto-share instances if provided
        if shared_instances:
            for obj in shared_instances:
                name = obj.__class__.__name__.lower()
                self.cssl.share(obj, name)

        # Install output callback
        self._original_callback = getattr(self.cssl, '_output_callback', None)
        self.cssl._output_callback = self._cssl_output_callback

    def _cssl_output_callback(self, text: str, level: str = "info"):
        """Route CSSL output to the output queue."""
        if self._output_queue:
            self._output_queue.put(("output", str(text)))
        if self._original_callback:
            self._original_callback(text, level)

    def launch(self, block: bool = False):
        """
        Start the console.

        Args:
            block: If True, runs on calling thread (blocks).
                   If False, runs in daemon thread.
        """
        if self._running:
            return
        self._running = True

        import queue
        self._output_queue = queue.Queue()

        if block:
            self._run_tkinter()
        else:
            self._thread = threading.Thread(target=self._run_tkinter, daemon=True)
            self._thread.start()

    def stop(self):
        """Close the console window."""
        self._running = False
        if self._root:
            try:
                self._root.after(0, self._root.destroy)
            except Exception:
                pass

    def _run_tkinter(self):
        """Main Tkinter loop."""
        try:
            import tkinter as tk
            from tkinter import ttk
            from tkinter.scrolledtext import ScrolledText
        except ImportError:
            print("[CSSLDevConsole] Tkinter not available", file=sys.stderr)
            return

        self._root = tk.Tk()
        self._root.title("CSSL Developer Console")
        self._root.geometry("1200x700")
        self._root.configure(bg="#1a1a2e")
        self._root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Dark theme
        style = ttk.Style(self._root)
        style.theme_use("clam")
        style.configure("Dark.TFrame", background="#1a1a2e")
        style.configure("Dark.TLabel", background="#1a1a2e", foreground="#e0e0e0", font=("Consolas", 10))
        style.configure("Dark.TButton", background="#2d2d44", foreground="#e0e0e0", font=("Consolas", 9))
        style.configure("Run.TButton", background="#1a4a1a", foreground="#44ff44", font=("Consolas", 10, "bold"))
        style.configure("API.Treeview", background="#12121e", foreground="#c0c0c0",
                        fieldbackground="#12121e", font=("Consolas", 9))
        style.configure("API.Treeview.Heading", background="#2d2d44",
                        foreground="#e0e0e0", font=("Consolas", 9, "bold"))
        style.map("API.Treeview", background=[("selected", "#3a3a5c")])

        self._build_ui(tk, ttk, ScrolledText)
        self._poll_output()
        self._root.mainloop()

    def _build_ui(self, tk, ttk, ScrolledText):
        """Build the three-panel UI layout."""
        root = self._root

        # Main horizontal paned window
        main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, bg="#1a1a2e",
                                    sashwidth=4, sashrelief=tk.FLAT)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Left panel: API Tree
        left_frame = ttk.Frame(main_pane, style="Dark.TFrame")
        main_pane.add(left_frame, width=320, minsize=200)

        header_frame = ttk.Frame(left_frame, style="Dark.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 4))

        ttk.Label(header_frame, text="Shared Objects", style="Dark.TLabel",
                  font=("Consolas", 11, "bold")).pack(side=tk.LEFT)

        btn_frame = ttk.Frame(header_frame, style="Dark.TFrame")
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text="Refresh", style="Dark.TButton",
                   command=self._refresh_api_tree).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Expand", style="Dark.TButton",
                   command=self._expand_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Collapse", style="Dark.TButton",
                   command=self._collapse_all).pack(side=tk.LEFT, padx=2)

        tree_container = ttk.Frame(left_frame, style="Dark.TFrame")
        tree_container.pack(fill=tk.BOTH, expand=True)

        tree_scroll = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self._tree = ttk.Treeview(tree_container, style="API.Treeview",
                                   yscrollcommand=tree_scroll.set, show="tree")
        self._tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self._tree.yview)
        self._tree.bind("<Double-1>", self._on_tree_double_click)

        # Right panel: Output + Code Editor
        right_frame = ttk.Frame(main_pane, style="Dark.TFrame")
        main_pane.add(right_frame, minsize=400)

        right_pane = tk.PanedWindow(right_frame, orient=tk.VERTICAL, bg="#1a1a2e",
                                     sashwidth=4, sashrelief=tk.FLAT)
        right_pane.pack(fill=tk.BOTH, expand=True)

        # Output area (top)
        output_frame = ttk.Frame(right_pane, style="Dark.TFrame")
        right_pane.add(output_frame, height=350, minsize=100)

        output_header = ttk.Frame(output_frame, style="Dark.TFrame")
        output_header.pack(fill=tk.X)

        ttk.Label(output_header, text="Output", style="Dark.TLabel",
                  font=("Consolas", 11, "bold")).pack(side=tk.LEFT)
        ttk.Button(output_header, text="Clear", style="Dark.TButton",
                   command=self._clear_output).pack(side=tk.RIGHT, padx=2)

        self._output = ScrolledText(output_frame, wrap=tk.WORD, font=("Consolas", 10),
                                    bg="#0d0d1a", fg="#44ff44", insertbackground="#44ff44",
                                    selectbackground="#3a3a5c", state=tk.DISABLED,
                                    relief=tk.FLAT, borderwidth=2)
        self._output.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        self._output.tag_configure("output", foreground="#44ff44")
        self._output.tag_configure("error", foreground="#ff4444")
        self._output.tag_configure("return_val", foreground="#44ddff")
        self._output.tag_configure("command", foreground="#888888")
        self._output.tag_configure("system", foreground="#ffaa00")

        # Code editor area (bottom)
        editor_frame = ttk.Frame(right_pane, style="Dark.TFrame")
        right_pane.add(editor_frame, height=250, minsize=120)

        editor_header = ttk.Frame(editor_frame, style="Dark.TFrame")
        editor_header.pack(fill=tk.X)

        ttk.Label(editor_header, text="CSSL Code", style="Dark.TLabel",
                  font=("Consolas", 11, "bold")).pack(side=tk.LEFT)

        ttk.Button(editor_header, text="Run (Ctrl+Enter)", style="Run.TButton",
                   command=self._run_code).pack(side=tk.RIGHT, padx=2)
        ttk.Button(editor_header, text="Clear", style="Dark.TButton",
                   command=self._clear_editor).pack(side=tk.RIGHT, padx=2)

        hist_frame = ttk.Frame(editor_header, style="Dark.TFrame")
        hist_frame.pack(side=tk.RIGHT, padx=8)
        ttk.Button(hist_frame, text="<", style="Dark.TButton",
                   command=self._history_prev).pack(side=tk.LEFT, padx=1)
        self._hist_label = ttk.Label(hist_frame, text="History", style="Dark.TLabel",
                                      font=("Consolas", 8), foreground="#666688")
        self._hist_label.pack(side=tk.LEFT, padx=4)
        ttk.Button(hist_frame, text=">", style="Dark.TButton",
                   command=self._history_next).pack(side=tk.LEFT, padx=1)

        # Code editor with line numbers
        code_container = ttk.Frame(editor_frame, style="Dark.TFrame")
        code_container.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

        self._line_numbers = tk.Text(code_container, width=4, font=("Consolas", 11),
                                     bg="#12121e", fg="#555566", relief=tk.FLAT, borderwidth=0,
                                     state=tk.DISABLED, takefocus=0, padx=4)
        self._line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        code_scroll = ttk.Scrollbar(code_container, orient=tk.VERTICAL)
        code_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self._editor = tk.Text(code_container, font=("Consolas", 11),
                               bg="#0a0a18", fg="#e0e0e0", insertbackground="#44ff44",
                               selectbackground="#3a3a5c", relief=tk.FLAT, borderwidth=2,
                               undo=True, wrap=tk.NONE, tabs="    ", padx=6, pady=4)
        self._editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        code_scroll.config(command=self._on_editor_scroll)
        self._editor.config(yscrollcommand=self._on_editor_yscroll)

        # Bindings
        self._editor.bind("<Control-Return>", self._on_ctrl_enter)
        self._editor.bind("<Control-Key-a>", self._on_select_all)
        self._editor.bind("<Tab>", self._on_tab)
        self._editor.bind("<Shift-Tab>", self._on_shift_tab)
        self._editor.bind("<KeyRelease>", self._on_editor_change)
        self._editor.bind("<ButtonRelease-1>", self._on_editor_change)

        # Syntax highlighting tags
        self._editor.tag_configure("keyword", foreground="#cc77ff")
        self._editor.tag_configure("type_kw", foreground="#44aaff")
        self._editor.tag_configure("string_lit", foreground="#ffaa44")
        self._editor.tag_configure("comment", foreground="#556655")
        self._editor.tag_configure("shared_obj", foreground="#44ffaa")
        self._editor.tag_configure("number", foreground="#ff7777")
        self._editor.tag_configure("builtin", foreground="#ffdd44")

        self._editor.focus_set()

        # Hint bar
        hint = ttk.Label(editor_frame, style="Dark.TLabel",
                         text="Ctrl+Enter = Execute | Tab = Indent | < > = History | Dbl-Click Tree = Insert",
                         font=("Consolas", 8), foreground="#555566")
        hint.pack(fill=tk.X, pady=(2, 0))

        # Initial state
        self._append_output("CSSL Developer Console v4.9.12", "system")
        self._append_output("Use $name to access shared objects (e.g. $player.health = 100;)", "system")
        self._append_output("", "output")

        self._refresh_api_tree()
        self._update_line_numbers()

    def _on_editor_scroll(self, *args):
        self._editor.yview(*args)
        self._line_numbers.yview(*args)

    def _on_editor_yscroll(self, *args):
        self._line_numbers.yview_moveto(args[0])

    def _update_line_numbers(self):
        import tkinter as tk
        self._line_numbers.configure(state=tk.NORMAL)
        self._line_numbers.delete("1.0", tk.END)
        content = self._editor.get("1.0", tk.END)
        line_count = max(1, content.count("\n"))
        numbers = "\n".join(str(i) for i in range(1, line_count + 1))
        self._line_numbers.insert("1.0", numbers)
        self._line_numbers.configure(state=tk.DISABLED)

    def _on_editor_change(self, event=None):
        self._update_line_numbers()
        self._highlight_syntax()

    def _highlight_syntax(self):
        """Basic CSSL syntax highlighting."""
        editor = self._editor
        content = editor.get("1.0", "end-1c")

        for tag in ("keyword", "type_kw", "string_lit", "comment", "shared_obj", "number", "builtin"):
            editor.tag_remove(tag, "1.0", "end")

        import re
        keywords = r'\b(define|if|else|elif|for|while|foreach|return|global|true|false|null|void|payload|import|pyimport|new|break|continue|const|class|constr|enum|throw|try|catch|finally|switch|case|default|private|public|closed|async|await)\b'
        type_keywords = r'\b(int|float|string|bool|dynamic|ob|list|dict|vector|stack|queue|set|map|ptr|pointer|address|bit|byte|instance)\b'
        builtins = r'\b(printl|print|str|int|float|len|abs|encode|decode|typeof|sizeof|reflect|address|memory|snapshot|randint|input|format|range)\b'
        shared_refs = r'\$\w+'
        strings = r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''
        comments = r'//.*$|/\*[\s\S]*?\*/|/d\s.*$'
        numbers = r'\b0x[0-9A-Fa-f]+\b|\b\d+\.?\d*\b'

        patterns = [
            (comments, "comment"),
            (strings, "string_lit"),
            (keywords, "keyword"),
            (type_keywords, "type_kw"),
            (builtins, "builtin"),
            (shared_refs, "shared_obj"),
            (numbers, "number"),
        ]

        for pattern, tag in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                editor.tag_add(tag, start_idx, end_idx)

    def _on_tab(self, event=None):
        self._editor.insert("insert", "    ")
        return "break"

    def _on_shift_tab(self, event=None):
        line = self._editor.get("insert linestart", "insert lineend")
        if line.startswith("    "):
            self._editor.delete("insert linestart", "insert linestart+4c")
        return "break"

    def _on_select_all(self, event=None):
        import tkinter as tk
        self._editor.tag_add(tk.SEL, "1.0", tk.END)
        return "break"

    def _on_ctrl_enter(self, event=None):
        self._run_code()
        return "break"

    def _run_code(self):
        import tkinter as tk
        code = self._editor.get("1.0", tk.END).strip()
        if not code:
            return

        if not self._history or self._history[-1] != code:
            self._history.append(code)
        self._history_index = len(self._history)
        self._update_hist_label()

        lines = code.split("\n")
        if len(lines) == 1:
            self._append_output(f"> {code}", "command")
        else:
            self._append_output(f"> ({len(lines)} lines)", "command")
            for line in lines[:5]:
                self._append_output(f"  {line}", "command")
            if len(lines) > 5:
                self._append_output(f"  ... ({len(lines) - 5} more lines)", "command")

        self._execute(code)

    def _execute(self, code: str):
        try:
            result = self.cssl.run(code)
            if result is not None:
                self._append_output(f"=> {result}", "return_val")
        except Exception as e:
            error_msg = str(e)
            if len(error_msg) > 500:
                error_msg = error_msg[:500] + "..."
            self._append_output(f"[ERROR] {error_msg}", "error")

    def _clear_editor(self):
        import tkinter as tk
        self._editor.delete("1.0", tk.END)
        self._update_line_numbers()

    def _history_prev(self):
        import tkinter as tk
        if self._history and self._history_index > 0:
            self._history_index -= 1
            self._editor.delete("1.0", tk.END)
            self._editor.insert("1.0", self._history[self._history_index])
            self._on_editor_change()
        self._update_hist_label()

    def _history_next(self):
        import tkinter as tk
        if self._history_index < len(self._history) - 1:
            self._history_index += 1
            self._editor.delete("1.0", tk.END)
            self._editor.insert("1.0", self._history[self._history_index])
            self._on_editor_change()
        else:
            self._history_index = len(self._history)
            self._editor.delete("1.0", tk.END)
            self._on_editor_change()
        self._update_hist_label()

    def _update_hist_label(self):
        total = len(self._history)
        if total == 0:
            self._hist_label.configure(text="No history")
        elif self._history_index >= total:
            self._hist_label.configure(text=f"New ({total})")
        else:
            self._hist_label.configure(text=f"{self._history_index + 1}/{total}")

    def _append_output(self, text: str, tag: str = "output"):
        import tkinter as tk
        self._output.configure(state=tk.NORMAL)
        self._output.insert(tk.END, text + "\n", tag)
        self._output.configure(state=tk.DISABLED)
        self._output.see(tk.END)

    def _poll_output(self):
        import queue
        try:
            while True:
                tag, text = self._output_queue.get_nowait()
                self._append_output(text, tag)
        except queue.Empty:
            pass
        if self._running and self._root:
            self._root.after(50, self._poll_output)

    def _clear_output(self):
        import tkinter as tk
        self._output.configure(state=tk.NORMAL)
        self._output.delete("1.0", tk.END)
        self._output.configure(state=tk.DISABLED)

    def _refresh_api_tree(self):
        import tkinter as tk
        import inspect
        tree = self._tree

        for item in tree.get_children():
            tree.delete(item)

        for name in sorted(_live_objects.keys()):
            obj = _live_objects[name]
            type_name = type(obj).__name__

            node_id = tree.insert("", tk.END, text=f"${name}  ({type_name})", open=False)
            self._populate_object_node(tree, node_id, name, obj, tk, inspect)

    def _populate_object_node(self, tree, parent_id: str, obj_name: str, obj, tk, inspect, depth: int = 0):
        if depth > 2:
            return

        methods = []
        properties = []

        for attr_name in sorted(dir(obj)):
            if attr_name.startswith("_"):
                continue
            try:
                val = getattr(obj, attr_name)
            except Exception:
                continue

            if callable(val):
                try:
                    sig = inspect.signature(val)
                    methods.append((attr_name, str(sig)))
                except (ValueError, TypeError):
                    methods.append((attr_name, "(...)"))
            else:
                val_type = type(val).__name__
                val_repr = repr(val)
                if len(val_repr) > 50:
                    val_repr = val_repr[:47] + "..."
                properties.append((attr_name, val_type, val_repr))

        for attr_name, val_type, val_repr in properties:
            tree.insert(parent_id, tk.END, text=f"  {attr_name}: {val_type} = {val_repr}", tags=("property",))

        for attr_name, sig in methods:
            tree.insert(parent_id, tk.END, text=f"  {attr_name}{sig}", tags=("method",))

    def _on_tree_double_click(self, event=None):
        import tkinter as tk
        selection = self._tree.selection()
        if not selection:
            return

        item_id = selection[0]
        item_text = self._tree.item(item_id, "text").strip()
        parent_id = self._tree.parent(item_id)

        if parent_id:
            parent_text = self._tree.item(parent_id, "text").strip()
            obj_ref = parent_text.split("  ")[0]
            attr_part = item_text.split(":")[0].split("(")[0].strip()
            insert_text = f"{obj_ref}.{attr_part}"
        else:
            insert_text = item_text.split("  ")[0]

        self._editor.insert(tk.INSERT, insert_text)
        self._editor.focus_set()
        self._on_editor_change()

    def _expand_all(self):
        for item in self._tree.get_children():
            self._tree.item(item, open=True)

    def _collapse_all(self):
        for item in self._tree.get_children():
            self._tree.item(item, open=False)

    def _on_close(self):
        self._running = False
        try:
            if self._root:
                self._root.quit()
                self._root.destroy()
        except Exception:
            pass
        self._root = None


async def async_console(shared_instances: list = None) -> None:
    """
    Launch the CSSL Developer Console asynchronously.

    Opens a Tkinter-based multi-line editor with:
    - CSSL syntax highlighting
    - API Tree showing all share()'d objects
    - Output panel with colored output
    - History navigation
    - Ctrl+Enter to execute

    Args:
        shared_instances: Optional list of objects to auto-share

    Usage:
        import asyncio
        from includecpp import CSSL

        CSSL.share(player, "player")
        asyncio.run(CSSL.async_console())
    """
    cssl = get_cssl()
    console = CSSLDevConsole(cssl, shared_instances=shared_instances)
    console.launch()

    while console._running:
        await asyncio.sleep(0.1)


def async_console_sync(shared_instances: list = None, block: bool = True) -> CSSLDevConsole:
    """
    Launch the CSSL Developer Console synchronously.

    Args:
        shared_instances: Optional list of objects to auto-share
        block: If True, blocks until console is closed

    Returns:
        CSSLDevConsole instance
    """
    cssl = get_cssl()
    console = CSSLDevConsole(cssl, shared_instances=shared_instances)
    console.launch(block=block)
    return console


# -----------------------------------------------------------------------------
# 2. async_run() / await_result() - Async/Await Support
# -----------------------------------------------------------------------------

_async_futures: Dict[str, Future] = {}
_async_executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="CSSLAsync")


async def async_run(code: str, *args, timeout: float = None) -> Any:
    """
    Execute CSSL code asynchronously with native asyncio support.

    Args:
        code: CSSL code string or file path
        *args: Arguments to pass to the script
        timeout: Optional timeout in seconds

    Returns:
        Execution result

    Usage:
        import asyncio
        from includecpp import CSSL

        async def main():
            result = await CSSL.async_run('return 42;')
            print(result)

        asyncio.run(main())
    """
    loop = asyncio.get_event_loop()
    cssl = get_cssl()

    def _run():
        return cssl.run(code, *args)

    if timeout:
        try:
            return await asyncio.wait_for(
                loop.run_in_executor(_async_executor, _run),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            raise TimeoutError(f"CSSL execution timed out after {timeout}s")
    else:
        return await loop.run_in_executor(_async_executor, _run)


def start_async(code: str, *args) -> str:
    """
    Start CSSL code execution asynchronously and return a future ID.

    Args:
        code: CSSL code string or file path
        *args: Arguments to pass to the script

    Returns:
        Future ID string for later retrieval

    Usage:
        future_id = CSSL.start_async('long_running_task();')
        # ... do other work ...
        result = CSSL.await_result(future_id)
    """
    import uuid
    future_id = str(uuid.uuid4())
    cssl = get_cssl()

    def _run():
        return cssl.run(code, *args)

    future = _async_executor.submit(_run)
    _async_futures[future_id] = future
    return future_id


def await_result(future_id: str, timeout: float = None) -> Any:
    """
    Wait for and retrieve the result of an async execution.

    Args:
        future_id: Future ID from start_async()
        timeout: Optional timeout in seconds

    Returns:
        Execution result

    Raises:
        KeyError: If future_id not found
        TimeoutError: If timeout exceeded
    """
    if future_id not in _async_futures:
        raise KeyError(f"Future ID not found: {future_id}")

    future = _async_futures[future_id]
    try:
        result = future.result(timeout=timeout)
        del _async_futures[future_id]
        return result
    except FuturesTimeoutError:
        raise TimeoutError(f"Async execution timed out after {timeout}s")


def is_async_done(future_id: str) -> bool:
    """Check if an async execution is complete."""
    if future_id not in _async_futures:
        return True
    return _async_futures[future_id].done()


def cancel_async(future_id: str) -> bool:
    """Cancel an async execution."""
    if future_id not in _async_futures:
        return False
    future = _async_futures[future_id]
    result = future.cancel()
    if result or future.done():
        del _async_futures[future_id]
    return result


# -----------------------------------------------------------------------------
# 3. watch() / unwatch() - Live Variable Monitoring
# -----------------------------------------------------------------------------

_watches: Dict[str, dict] = {}
_watch_thread: Optional[threading.Thread] = None
_watch_lock = threading.Lock()
_watch_running = False


def watch(target: str, callback: Callable[[Any, Any], None], interval: float = 0.1) -> str:
    """
    Watch a CSSL variable or shared object for changes.

    Args:
        target: Variable name or $shared_name to watch
        callback: Function called with (old_value, new_value) on change
        interval: Check interval in seconds

    Returns:
        Watch ID for unwatch()

    Usage:
        def on_change(old, new):
            print(f"Changed: {old} -> {new}")

        watch_id = CSSL.watch("$player.health", on_change)
        # ... later ...
        CSSL.unwatch(watch_id)
    """
    global _watch_thread, _watch_running
    import uuid

    watch_id = str(uuid.uuid4())

    # Get initial value
    initial_value = _get_watch_value(target)

    with _watch_lock:
        _watches[watch_id] = {
            'target': target,
            'callback': callback,
            'interval': interval,
            'last_value': initial_value,
            'last_check': time.time()
        }

    # Start watch thread if not running
    if not _watch_running:
        _watch_running = True
        _watch_thread = threading.Thread(target=_watch_loop, daemon=True, name="CSSLWatch")
        _watch_thread.start()

    return watch_id


def unwatch(watch_id: str) -> bool:
    """
    Stop watching a variable.

    Args:
        watch_id: Watch ID from watch()

    Returns:
        True if watch was removed
    """
    global _watch_running

    with _watch_lock:
        if watch_id in _watches:
            del _watches[watch_id]
            if not _watches:
                _watch_running = False
            return True
    return False


def unwatch_all() -> int:
    """Stop all watches. Returns count of removed watches."""
    global _watch_running

    with _watch_lock:
        count = len(_watches)
        _watches.clear()
        _watch_running = False
    return count


def _get_watch_value(target: str) -> Any:
    """Get the current value of a watch target."""
    if target.startswith('$'):
        name = target[1:]
        parts = name.split('.', 1)
        obj = _live_objects.get(parts[0])
        if obj and len(parts) > 1:
            try:
                for attr in parts[1].split('.'):
                    obj = getattr(obj, attr)
            except AttributeError:
                return None
        return obj
    else:
        cssl = get_cssl()
        return cssl.get_global(target)


def _watch_loop():
    """Background thread for watching variables."""
    global _watch_running

    while _watch_running:
        current_time = time.time()

        with _watch_lock:
            watches_copy = dict(_watches)

        for watch_id, watch_info in watches_copy.items():
            if current_time - watch_info['last_check'] >= watch_info['interval']:
                try:
                    new_value = _get_watch_value(watch_info['target'])
                    old_value = watch_info['last_value']

                    if new_value != old_value:
                        watch_info['callback'](old_value, new_value)
                        with _watch_lock:
                            if watch_id in _watches:
                                _watches[watch_id]['last_value'] = new_value

                    with _watch_lock:
                        if watch_id in _watches:
                            _watches[watch_id]['last_check'] = current_time
                except Exception:
                    pass

        time.sleep(0.01)


# -----------------------------------------------------------------------------
# 4. breakpoint() / step() / continue_() - Debug Stepping
# -----------------------------------------------------------------------------

_debug_breakpoints: Dict[str, Set[int]] = {}
_debug_state: Dict[str, Any] = {
    'paused': False,
    'current_line': 0,
    'current_file': None,
    'scope_snapshot': {},
    'call_stack': [],
    'step_mode': False
}
_debug_event = threading.Event()
_debug_lock = threading.Lock()


def breakpoint_add(file_or_code: str, line: int) -> str:
    """
    Add a breakpoint at a specific line.

    Args:
        file_or_code: File path or code identifier
        line: Line number (1-based)

    Returns:
        Breakpoint ID
    """
    import hashlib

    bp_key = hashlib.md5(file_or_code.encode()).hexdigest()[:8]

    with _debug_lock:
        if bp_key not in _debug_breakpoints:
            _debug_breakpoints[bp_key] = set()
        _debug_breakpoints[bp_key].add(line)

    return f"{bp_key}:{line}"


def breakpoint_remove(bp_id: str) -> bool:
    """Remove a breakpoint by ID."""
    try:
        bp_key, line_str = bp_id.split(':')
        line = int(line_str)

        with _debug_lock:
            if bp_key in _debug_breakpoints:
                _debug_breakpoints[bp_key].discard(line)
                if not _debug_breakpoints[bp_key]:
                    del _debug_breakpoints[bp_key]
                return True
    except ValueError:
        pass
    return False


def breakpoint_clear() -> int:
    """Clear all breakpoints. Returns count removed."""
    with _debug_lock:
        count = sum(len(lines) for lines in _debug_breakpoints.values())
        _debug_breakpoints.clear()
        return count


def step() -> dict:
    """
    Execute one step and return current debug state.

    Returns:
        Dict with: line, file, scope, call_stack
    """
    with _debug_lock:
        _debug_state['step_mode'] = True
    _debug_event.set()
    _debug_event.clear()

    time.sleep(0.01)

    with _debug_lock:
        return {
            'line': _debug_state['current_line'],
            'file': _debug_state['current_file'],
            'scope': dict(_debug_state['scope_snapshot']),
            'call_stack': list(_debug_state['call_stack'])
        }


def continue_debug() -> Any:
    """Continue execution after breakpoint."""
    with _debug_lock:
        _debug_state['step_mode'] = False
        _debug_state['paused'] = False
    _debug_event.set()
    return None


def get_stack() -> List[dict]:
    """Get current call stack."""
    with _debug_lock:
        return list(_debug_state['call_stack'])


def is_paused() -> bool:
    """Check if debugger is paused."""
    with _debug_lock:
        return _debug_state['paused']


# -----------------------------------------------------------------------------
# 5. profile() - Performance Analysis
# -----------------------------------------------------------------------------

def profile(code: str, *args) -> ProfileResult:
    """
    Profile CSSL code execution and return detailed performance data.

    Args:
        code: CSSL code string or file path
        *args: Arguments to pass to the script

    Returns:
        ProfileResult with timing data per function

    Usage:
        result = CSSL.profile('''
            define slow() { for(i=0;i<1000;i++){} }
            slow();
            slow();
        ''')
        print(result.time_per_function)
        print(result.hotspots)
    """
    cssl = get_cssl()
    runtime = cssl._get_runtime()

    # Enable profiling
    call_counts: Dict[str, int] = {}
    call_times: Dict[str, float] = {}
    call_tree: List[dict] = []
    call_stack: List[str] = []

    original_call_function = None
    if hasattr(runtime, '_call_function'):
        original_call_function = runtime._call_function

    def profiled_call_function(func_info, args_list, kwargs_dict=None):
        func_name = func_info.get('name', '<anonymous>') if isinstance(func_info, dict) else str(func_info)

        call_counts[func_name] = call_counts.get(func_name, 0) + 1
        call_stack.append(func_name)

        start = time.perf_counter()
        try:
            if original_call_function:
                return original_call_function(func_info, args_list, kwargs_dict or {})
        finally:
            elapsed = (time.perf_counter() - start) * 1000
            call_times[func_name] = call_times.get(func_name, 0) + elapsed
            call_stack.pop()

            call_tree.append({
                'function': func_name,
                'time_ms': elapsed,
                'depth': len(call_stack)
            })

    # Patch and run
    if original_call_function:
        runtime._call_function = profiled_call_function

    start_time = time.perf_counter()
    try:
        cssl.run(code, *args)
    finally:
        if original_call_function:
            runtime._call_function = original_call_function
    total_time = (time.perf_counter() - start_time) * 1000

    # Generate hotspots (functions sorted by time)
    hotspots = sorted(
        [{'function': fn, 'time_ms': tm, 'calls': call_counts.get(fn, 0),
          'avg_ms': tm / call_counts.get(fn, 1)}
         for fn, tm in call_times.items()],
        key=lambda x: x['time_ms'],
        reverse=True
    )[:10]

    return ProfileResult(
        total_time_ms=total_time,
        calls=call_counts,
        time_per_function=call_times,
        hotspots=hotspots,
        call_tree=call_tree
    )


# -----------------------------------------------------------------------------
# 6. validate() - Code Syntax Checking
# -----------------------------------------------------------------------------

def validate(code: str) -> ValidationResult:
    """
    Validate CSSL code without executing it.

    Args:
        code: CSSL code string

    Returns:
        ValidationResult with errors and warnings

    Usage:
        result = CSSL.validate('printl("Hello"')  # Missing )
        if not result.valid:
            for error in result.errors:
                print(f"Line {error['line']}: {error['message']}")
    """
    errors = []
    warnings_list = []

    try:
        from .cssl.cssl_parser import CSSLParser, CSSLSyntaxError

        parser = CSSLParser(code)
        try:
            ast = parser.parse()

            # Check for warnings
            if hasattr(parser, 'warnings'):
                for w in parser.warnings:
                    warnings_list.append({
                        'line': getattr(w, 'line', 0),
                        'column': getattr(w, 'column', 0),
                        'message': str(w)
                    })

            # Basic semantic checks
            _validate_semantics(ast, warnings_list)

        except CSSLSyntaxError as e:
            errors.append({
                'line': getattr(e, 'line', 0),
                'column': getattr(e, 'column', 0),
                'message': str(e)
            })
    except ImportError:
        errors.append({
            'line': 0,
            'column': 0,
            'message': "CSSL parser not available"
        })
    except Exception as e:
        errors.append({
            'line': 0,
            'column': 0,
            'message': f"Validation error: {str(e)}"
        })

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings_list
    )


def _validate_semantics(ast, warnings: list):
    """Perform basic semantic validation on AST."""
    if ast is None:
        return

    defined_functions = set()
    defined_variables = set()

    def visit(node):
        if node is None:
            return

        node_type = getattr(node, 'type', None)

        if node_type == 'function':
            func_info = node.value if hasattr(node, 'value') else {}
            name = func_info.get('name') if isinstance(func_info, dict) else None
            if name:
                if name in defined_functions:
                    warnings.append({
                        'line': getattr(node, 'line', 0),
                        'column': 0,
                        'message': f"Function '{name}' is defined multiple times"
                    })
                defined_functions.add(name)

        if hasattr(node, 'children'):
            for child in node.children:
                visit(child)

    visit(ast)


# -----------------------------------------------------------------------------
# 7. transpile() - Code Transpilation
# -----------------------------------------------------------------------------

def transpile(code: str, target: str = "python") -> str:
    """
    Transpile CSSL code to another language.

    Args:
        code: CSSL code string
        target: Target language ("python", "cpp", "js")

    Returns:
        Transpiled code string

    Usage:
        py_code = CSSL.transpile('int x = 5; printl(x * 2);', 'python')
        print(py_code)
    """
    if target not in ("python", "cpp", "js", "javascript"):
        raise ValueError(f"Unsupported target: {target}. Use 'python', 'cpp', or 'js'")

    try:
        from .cssl.cssl_parser import CSSLParser
        parser = CSSLParser(code)
        ast = parser.parse()

        if target == "python":
            return _transpile_to_python(ast)
        elif target == "cpp":
            return _transpile_to_cpp(ast)
        else:
            return _transpile_to_js(ast)
    except Exception as e:
        raise ValueError(f"Transpilation failed: {str(e)}")


def _transpile_to_python(ast, indent: int = 0) -> str:
    """Transpile AST to Python code."""
    lines = []
    prefix = "    " * indent

    if ast is None:
        return ""

    def visit(node, ind=0):
        pre = "    " * ind

        if node is None:
            return ""

        node_type = getattr(node, 'type', None)
        value = getattr(node, 'value', None)

        if node_type == 'program':
            return "\n".join(visit(c, ind) for c in getattr(node, 'children', []))

        elif node_type == 'function':
            func_info = value if isinstance(value, dict) else {}
            name = func_info.get('name', 'anonymous')
            params = func_info.get('params', [])
            param_str = ", ".join(p.get('name', str(p)) if isinstance(p, dict) else str(p) for p in params)
            body = "\n".join(visit(c, ind + 1) for c in getattr(node, 'children', []))
            if not body.strip():
                body = f"{'    ' * (ind + 1)}pass"
            return f"{pre}def {name}({param_str}):\n{body}"

        elif node_type == 'typed_declaration':
            decl = value if isinstance(value, dict) else {}
            name = decl.get('name', 'var')
            val_node = decl.get('value')
            val = visit(val_node, 0) if val_node else "None"
            return f"{pre}{name} = {val}"

        elif node_type == 'assignment':
            target = visit(value.get('target'), 0) if isinstance(value, dict) else "x"
            val = visit(value.get('value'), 0) if isinstance(value, dict) else "None"
            return f"{pre}{target} = {val}"

        elif node_type == 'call':
            call_info = value if isinstance(value, dict) else {}
            callee = visit(call_info.get('callee'), 0)
            args = call_info.get('args', [])
            args_str = ", ".join(visit(a, 0) for a in args)
            # Map CSSL builtins to Python
            if callee == 'printl':
                callee = 'print'
            return f"{pre}{callee}({args_str})" if ind > 0 else f"{callee}({args_str})"

        elif node_type == 'identifier':
            return str(value)

        elif node_type == 'literal':
            if isinstance(value, str):
                return f'"{value}"'
            return str(value)

        elif node_type == 'number':
            return str(value)

        elif node_type == 'binary':
            op_info = value if isinstance(value, dict) else {}
            left = visit(op_info.get('left'), 0)
            right = visit(op_info.get('right'), 0)
            op = op_info.get('op', '+')
            return f"({left} {op} {right})"

        elif node_type == 'if':
            cond_info = value if isinstance(value, dict) else {}
            cond = visit(cond_info.get('condition'), 0)
            then_body = "\n".join(visit(c, ind + 1) for c in getattr(node, 'children', []))
            if not then_body.strip():
                then_body = f"{'    ' * (ind + 1)}pass"
            return f"{pre}if {cond}:\n{then_body}"

        elif node_type == 'for':
            for_info = value if isinstance(value, dict) else {}
            init = visit(for_info.get('init'), 0)
            cond = visit(for_info.get('condition'), 0)
            update = visit(for_info.get('update'), 0)
            body = "\n".join(visit(c, ind + 1) for c in getattr(node, 'children', []))
            if not body.strip():
                body = f"{'    ' * (ind + 1)}pass"
            return f"{pre}# for({init}; {cond}; {update})\n{pre}while {cond}:\n{body}\n{'    ' * (ind + 1)}{update}"

        elif node_type == 'while':
            while_info = value if isinstance(value, dict) else {}
            cond = visit(while_info.get('condition'), 0)
            body = "\n".join(visit(c, ind + 1) for c in getattr(node, 'children', []))
            if not body.strip():
                body = f"{'    ' * (ind + 1)}pass"
            return f"{pre}while {cond}:\n{body}"

        elif node_type == 'return':
            val = visit(value, 0) if value else ""
            return f"{pre}return {val}"

        elif node_type == 'expression':
            return f"{pre}{visit(value, 0)}"

        else:
            return f"{pre}# Unknown: {node_type}"

    return visit(ast, indent)


def _transpile_to_cpp(ast, indent: int = 0) -> str:
    """Transpile AST to C++ code."""
    lines = ["#include <iostream>", "#include <string>", "#include <vector>", ""]

    def visit(node, ind=0):
        pre = "    " * ind

        if node is None:
            return ""

        node_type = getattr(node, 'type', None)
        value = getattr(node, 'value', None)

        if node_type == 'program':
            body = "\n".join(visit(c, ind) for c in getattr(node, 'children', []))
            return body

        elif node_type == 'function':
            func_info = value if isinstance(value, dict) else {}
            name = func_info.get('name', 'anonymous')
            ret_type = func_info.get('return_type', 'auto')
            params = func_info.get('params', [])
            param_str = ", ".join(f"auto {p.get('name', str(p))}" if isinstance(p, dict) else f"auto {p}" for p in params)
            body = "\n".join(visit(c, ind + 1) for c in getattr(node, 'children', []))
            return f"{pre}{ret_type} {name}({param_str}) {{\n{body}\n{pre}}}"

        elif node_type == 'typed_declaration':
            decl = value if isinstance(value, dict) else {}
            type_name = decl.get('type', 'auto')
            name = decl.get('name', 'var')
            val_node = decl.get('value')
            val = visit(val_node, 0) if val_node else ""
            cpp_type = {'int': 'int', 'float': 'double', 'string': 'std::string', 'bool': 'bool'}.get(type_name, 'auto')
            if val:
                return f"{pre}{cpp_type} {name} = {val};"
            return f"{pre}{cpp_type} {name};"

        elif node_type == 'assignment':
            target = visit(value.get('target'), 0) if isinstance(value, dict) else "x"
            val = visit(value.get('value'), 0) if isinstance(value, dict) else "0"
            return f"{pre}{target} = {val};"

        elif node_type == 'call':
            call_info = value if isinstance(value, dict) else {}
            callee = visit(call_info.get('callee'), 0)
            args = call_info.get('args', [])
            args_str = ", ".join(visit(a, 0) for a in args)
            if callee == 'printl':
                return f"{pre}std::cout << {args_str} << std::endl;" if ind > 0 else f"std::cout << {args_str} << std::endl"
            return f"{pre}{callee}({args_str});" if ind > 0 else f"{callee}({args_str})"

        elif node_type == 'identifier':
            return str(value)

        elif node_type == 'literal':
            if isinstance(value, str):
                return f'"{value}"'
            return str(value)

        elif node_type == 'return':
            val = visit(value, 0) if value else ""
            return f"{pre}return {val};"

        elif node_type == 'expression':
            return f"{pre}{visit(value, 0)};"

        else:
            return f"{pre}// Unknown: {node_type}"

    main_body = visit(ast, 0)
    return "\n".join(lines) + main_body


def _transpile_to_js(ast, indent: int = 0) -> str:
    """Transpile AST to JavaScript code."""

    def visit(node, ind=0):
        pre = "    " * ind

        if node is None:
            return ""

        node_type = getattr(node, 'type', None)
        value = getattr(node, 'value', None)

        if node_type == 'program':
            return "\n".join(visit(c, ind) for c in getattr(node, 'children', []))

        elif node_type == 'function':
            func_info = value if isinstance(value, dict) else {}
            name = func_info.get('name', 'anonymous')
            params = func_info.get('params', [])
            param_str = ", ".join(p.get('name', str(p)) if isinstance(p, dict) else str(p) for p in params)
            body = "\n".join(visit(c, ind + 1) for c in getattr(node, 'children', []))
            return f"{pre}function {name}({param_str}) {{\n{body}\n{pre}}}"

        elif node_type == 'typed_declaration':
            decl = value if isinstance(value, dict) else {}
            name = decl.get('name', 'var')
            val_node = decl.get('value')
            val = visit(val_node, 0) if val_node else "null"
            return f"{pre}let {name} = {val};"

        elif node_type == 'assignment':
            target = visit(value.get('target'), 0) if isinstance(value, dict) else "x"
            val = visit(value.get('value'), 0) if isinstance(value, dict) else "null"
            return f"{pre}{target} = {val};"

        elif node_type == 'call':
            call_info = value if isinstance(value, dict) else {}
            callee = visit(call_info.get('callee'), 0)
            args = call_info.get('args', [])
            args_str = ", ".join(visit(a, 0) for a in args)
            if callee == 'printl':
                callee = 'console.log'
            return f"{pre}{callee}({args_str});" if ind > 0 else f"{callee}({args_str})"

        elif node_type == 'identifier':
            return str(value)

        elif node_type == 'literal':
            if isinstance(value, str):
                return f'"{value}"'
            elif value is None:
                return "null"
            elif isinstance(value, bool):
                return "true" if value else "false"
            return str(value)

        elif node_type == 'return':
            val = visit(value, 0) if value else ""
            return f"{pre}return {val};"

        elif node_type == 'expression':
            return f"{pre}{visit(value, 0)};"

        else:
            return f"{pre}// Unknown: {node_type}"

    return visit(ast, indent)


# -----------------------------------------------------------------------------
# 8. serialize() / deserialize() - Runtime State Persistence
# -----------------------------------------------------------------------------

def serialize(name: str = None) -> bytes:
    """
    Serialize CSSL runtime state to bytes.

    Args:
        name: Optional specific variable/object to serialize (None = all globals)

    Returns:
        Pickled bytes of the runtime state

    Usage:
        state = CSSL.serialize()
        # ... later or in another process ...
        CSSL.deserialize(state)
    """
    cssl = get_cssl()
    runtime = cssl._get_runtime()

    state = {}

    if name:
        value = runtime.global_scope.get(name) if hasattr(runtime, 'global_scope') else None
        if value is None:
            value = _live_objects.get(name)
        state[name] = _serialize_value(value)
    else:
        # Serialize all globals
        if hasattr(runtime, 'global_scope') and hasattr(runtime.global_scope, 'variables'):
            for k, v in runtime.global_scope.variables.items():
                try:
                    state[k] = _serialize_value(v)
                except Exception:
                    pass

        # Serialize shared objects
        for k, v in _live_objects.items():
            try:
                state[f"$shared${k}"] = _serialize_value(v)
            except Exception:
                pass

    return pickle.dumps(state, protocol=pickle.HIGHEST_PROTOCOL)


def deserialize(data: bytes) -> None:
    """
    Deserialize and restore CSSL runtime state.

    Args:
        data: Pickled bytes from serialize()
    """
    cssl = get_cssl()
    runtime = cssl._get_runtime()

    state = pickle.loads(data)

    for k, v in state.items():
        if k.startswith('$shared$'):
            name = k[8:]
            _live_objects[name] = _deserialize_value(v)
        else:
            if hasattr(runtime, 'global_scope'):
                runtime.global_scope.set(k, _deserialize_value(v))


def save_state(path: str) -> None:
    """
    Save CSSL runtime state to a file.

    Args:
        path: File path to save state to
    """
    data = serialize()
    with open(path, 'wb') as f:
        f.write(data)


def load_state(path: str) -> None:
    """
    Load CSSL runtime state from a file.

    Args:
        path: File path to load state from
    """
    with open(path, 'rb') as f:
        data = f.read()
    deserialize(data)


def _serialize_value(value: Any) -> Any:
    """Serialize a single value, handling CSSL types."""
    if value is None or isinstance(value, (int, float, str, bool, bytes)):
        return value
    elif isinstance(value, (list, tuple)):
        return type(value)(_serialize_value(v) for v in value)
    elif isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items()}
    elif hasattr(value, '__dict__'):
        return {'__class__': type(value).__name__, '__dict__': _serialize_value(value.__dict__)}
    else:
        return str(value)


def _deserialize_value(value: Any) -> Any:
    """Deserialize a single value."""
    if value is None or isinstance(value, (int, float, str, bool, bytes)):
        return value
    elif isinstance(value, list):
        return [_deserialize_value(v) for v in value]
    elif isinstance(value, tuple):
        return tuple(_deserialize_value(v) for v in value)
    elif isinstance(value, dict):
        if '__class__' in value and '__dict__' in value:
            # Restore as dict with class info
            return {'__restored_class__': value['__class__'], **_deserialize_value(value['__dict__'])}
        return {k: _deserialize_value(v) for k, v in value.items()}
    return value


# -----------------------------------------------------------------------------
# 9. hot_reload() - Live Code Updates
# -----------------------------------------------------------------------------

_hot_reload_watchers: Dict[str, dict] = {}
_hot_reload_thread: Optional[threading.Thread] = None
_hot_reload_running = False


def hot_reload(name: str) -> bool:
    """
    Reload a previously loaded script by name.

    Args:
        name: Name of the loaded script (from load())

    Returns:
        True if reloaded successfully
    """
    cssl = get_cssl()

    if not hasattr(cssl, '_loaded_scripts') or name not in cssl._loaded_scripts:
        return False

    script_info = cssl._loaded_scripts[name]
    path = script_info.get('path')

    if path and os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                new_code = f.read()
            script_info['code'] = new_code
            return True
        except Exception:
            pass
    return False


def enable_hot_reload(watch_dir: str, extensions: list = None) -> str:
    """
    Enable hot reload for a directory, watching for file changes.

    Args:
        watch_dir: Directory to watch for changes
        extensions: File extensions to watch (default: ['.cssl', '.cssl-pl'])

    Returns:
        Watcher ID
    """
    global _hot_reload_thread, _hot_reload_running
    import uuid

    if extensions is None:
        extensions = ['.cssl', '.cssl-pl']

    watcher_id = str(uuid.uuid4())

    _hot_reload_watchers[watcher_id] = {
        'dir': os.path.abspath(watch_dir),
        'extensions': extensions,
        'mtimes': {}
    }

    # Scan initial mtimes
    _scan_directory(watcher_id)

    if not _hot_reload_running:
        _hot_reload_running = True
        _hot_reload_thread = threading.Thread(target=_hot_reload_loop, daemon=True, name="CSSLHotReload")
        _hot_reload_thread.start()

    return watcher_id


def disable_hot_reload(watcher_id: str = None) -> int:
    """
    Disable hot reload watcher(s).

    Args:
        watcher_id: Specific watcher to disable (None = all)

    Returns:
        Count of watchers disabled
    """
    global _hot_reload_running

    if watcher_id:
        if watcher_id in _hot_reload_watchers:
            del _hot_reload_watchers[watcher_id]
            return 1
        return 0
    else:
        count = len(_hot_reload_watchers)
        _hot_reload_watchers.clear()
        _hot_reload_running = False
        return count


def _scan_directory(watcher_id: str):
    """Scan directory and update mtimes."""
    info = _hot_reload_watchers.get(watcher_id)
    if not info:
        return

    watch_dir = info['dir']
    extensions = info['extensions']

    for root, dirs, files in os.walk(watch_dir):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(filepath)
                    info['mtimes'][filepath] = mtime
                except OSError:
                    pass


def _hot_reload_loop():
    """Background thread for hot reload file watching."""
    global _hot_reload_running

    while _hot_reload_running:
        for watcher_id, info in list(_hot_reload_watchers.items()):
            watch_dir = info['dir']
            extensions = info['extensions']
            mtimes = info['mtimes']

            for root, dirs, files in os.walk(watch_dir):
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        filepath = os.path.join(root, file)
                        try:
                            current_mtime = os.path.getmtime(filepath)
                            if filepath in mtimes and current_mtime > mtimes[filepath]:
                                # File changed - reload
                                name = os.path.splitext(file)[0]
                                hot_reload(name)
                            mtimes[filepath] = current_mtime
                        except OSError:
                            pass

        time.sleep(1.0)


# -----------------------------------------------------------------------------
# 10. on() / emit() / off() - Event System
# -----------------------------------------------------------------------------

_event_listeners: Dict[str, Dict[str, Callable]] = {}
_event_lock = threading.Lock()


def on(event: str, callback: Callable, once: bool = False) -> str:
    """
    Register an event listener.

    Args:
        event: Event name
        callback: Function to call when event is emitted
        once: If True, listener is removed after first trigger

    Returns:
        Listener ID for off()

    Usage:
        def on_damage(amount, source):
            print(f"Took {amount} damage from {source}")

        CSSL.on("player_damage", on_damage)
        CSSL.emit("player_damage", 10, "enemy")
    """
    import uuid
    listener_id = str(uuid.uuid4())

    with _event_lock:
        if event not in _event_listeners:
            _event_listeners[event] = {}

        _event_listeners[event][listener_id] = {
            'callback': callback,
            'once': once
        }

    return listener_id


def once(event: str, callback: Callable) -> str:
    """
    Register a one-time event listener.

    Args:
        event: Event name
        callback: Function to call once when event is emitted

    Returns:
        Listener ID
    """
    return on(event, callback, once=True)


def emit(event: str, *args, **kwargs) -> int:
    """
    Emit an event to all listeners.

    Args:
        event: Event name
        *args: Positional arguments to pass to listeners
        **kwargs: Keyword arguments to pass to listeners

    Returns:
        Number of listeners called
    """
    to_remove = []
    called = 0

    with _event_lock:
        if event not in _event_listeners:
            return 0
        listeners = dict(_event_listeners[event])

    for listener_id, info in listeners.items():
        try:
            info['callback'](*args, **kwargs)
            called += 1
            if info['once']:
                to_remove.append(listener_id)
        except Exception:
            pass

    with _event_lock:
        if event in _event_listeners:
            for lid in to_remove:
                _event_listeners[event].pop(lid, None)

    return called


def off(listener_id: str) -> bool:
    """
    Remove an event listener.

    Args:
        listener_id: Listener ID from on()

    Returns:
        True if listener was removed
    """
    with _event_lock:
        for event, listeners in _event_listeners.items():
            if listener_id in listeners:
                del listeners[listener_id]
                return True
    return False


def off_all(event: str = None) -> int:
    """
    Remove all listeners for an event (or all events).

    Args:
        event: Event name (None = all events)

    Returns:
        Count of listeners removed
    """
    with _event_lock:
        if event:
            if event in _event_listeners:
                count = len(_event_listeners[event])
                del _event_listeners[event]
                return count
            return 0
        else:
            count = sum(len(l) for l in _event_listeners.values())
            _event_listeners.clear()
            return count


# -----------------------------------------------------------------------------
# 11. pipe() - Function Chaining
# -----------------------------------------------------------------------------

class CSSLPipeline:
    """
    Pipeline for chaining CSSL function calls.

    Usage:
        pipeline = CSSL.pipe("parse", "validate", "transform")
        result = pipeline(input_data)
    """

    def __init__(self, *function_names: str):
        self.functions = list(function_names)
        self._cssl = get_cssl()

    def __call__(self, initial_value: Any) -> Any:
        """Execute the pipeline with an initial value."""
        result = initial_value

        for func_name in self.functions:
            if '.' in func_name:
                # Method call on result
                parts = func_name.rsplit('.', 1)
                if len(parts) == 2:
                    obj_name, method_name = parts
                    obj = self._cssl.get_global(obj_name)
                    if obj and hasattr(obj, method_name):
                        result = getattr(obj, method_name)(result)
                        continue

            # CSSL function call
            code = f"{func_name}(parameter.get(0))"
            result = self._cssl.run(code, result)

        return result

    def add(self, *function_names: str) -> 'CSSLPipeline':
        """Add more functions to the pipeline."""
        self.functions.extend(function_names)
        return self

    def then(self, func: Callable) -> 'CSSLPipeline':
        """Add a Python function to the pipeline."""
        self.functions.append(func)
        return self


def pipe(*function_names: str) -> CSSLPipeline:
    """
    Create a function pipeline.

    Args:
        *function_names: Names of CSSL functions to chain

    Returns:
        CSSLPipeline callable

    Usage:
        # Define functions in CSSL
        CSSL.run('''
            define double(x) { return x * 2; }
            define addTen(x) { return x + 10; }
        ''')

        # Create and use pipeline
        pipeline = CSSL.pipe("double", "addTen", "double")
        result = pipeline(5)  # (5 * 2 + 10) * 2 = 40
    """
    return CSSLPipeline(*function_names)


# -----------------------------------------------------------------------------
# 12. sandbox() - Secure Execution
# -----------------------------------------------------------------------------

def sandbox(code: str, restrictions: dict = None, **kwargs) -> Any:
    """
    Execute CSSL code in a sandboxed environment.

    Args:
        code: CSSL code to execute
        restrictions: Dict of restrictions:
            - no_io: Disable file I/O (default: True)
            - no_network: Disable network (default: True)
            - no_exec: Disable exec/system calls (default: True)
            - max_time: Max execution time in seconds (default: 5.0)
            - max_memory: Max memory in MB (default: 100)
            - allowed_builtins: List of allowed builtin functions

    Returns:
        Execution result

    Raises:
        SecurityError: If code violates restrictions
        TimeoutError: If execution exceeds max_time
    """
    if restrictions is None:
        restrictions = {}

    no_io = restrictions.get('no_io', True)
    no_network = restrictions.get('no_network', True)
    no_exec = restrictions.get('no_exec', True)
    max_time = restrictions.get('max_time', kwargs.get('timeout', 5.0))
    allowed_builtins = restrictions.get('allowed_builtins', None)

    # Check for dangerous patterns
    dangerous_patterns = []

    if no_io:
        dangerous_patterns.extend([
            r'\breadfile\b', r'\bwritefile\b', r'\bappendfile\b',
            r'\bmkdir\b', r'\brmdir\b', r'\brmfile\b', r'\brename\b',
            r'\blistdir\b', r'\bpathexists\b', r'\bfilesize\b'
        ])

    if no_network:
        dangerous_patterns.extend([
            r'\bfetch\b', r'\bhttprequest\b', r'\bsocket\b',
            r'\bdownload\b', r'\bupload\b'
        ])

    if no_exec:
        dangerous_patterns.extend([
            r'\bexec\b', r'\bsystem\b', r'\bappexec\b',
            r'\bpyimport\b', r'\binitpy\b', r'\binitsh\b',
            r'\bcreatecmd\b'
        ])

    # Check code against patterns
    for pattern in dangerous_patterns:
        if re.search(pattern, code, re.IGNORECASE):
            raise SecurityError(f"Sandboxed code contains forbidden pattern: {pattern}")

    # Run with timeout
    cssl = get_cssl()

    result_container = {'result': None, 'error': None}

    def run_sandboxed():
        try:
            result_container['result'] = cssl.run(code)
        except Exception as e:
            result_container['error'] = e

    thread = threading.Thread(target=run_sandboxed, daemon=True)
    thread.start()
    thread.join(timeout=max_time)

    if thread.is_alive():
        raise TimeoutError(f"Sandboxed execution timed out after {max_time}s")

    if result_container['error']:
        raise result_container['error']

    return result_container['result']


class SecurityError(Exception):
    """Raised when sandboxed code violates security restrictions."""
    pass


# -----------------------------------------------------------------------------
# 13. run() with timeout - Add timeout parameter
# -----------------------------------------------------------------------------

def run_with_timeout(code: str, *args, timeout: float = None, **kwargs) -> Any:
    """
    Execute CSSL code with an optional timeout.

    Args:
        code: CSSL code string or file path
        *args: Arguments to pass to the script
        timeout: Maximum execution time in seconds (None = no timeout)

    Returns:
        Execution result

    Raises:
        TimeoutError: If execution exceeds timeout
    """
    if timeout is None:
        return get_cssl().run(code, *args)

    result_container = {'result': None, 'error': None}

    def _run():
        try:
            result_container['result'] = get_cssl().run(code, *args)
        except Exception as e:
            result_container['error'] = e

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    if thread.is_alive():
        raise TimeoutError(f"CSSL execution timed out after {timeout}s")

    if result_container['error']:
        raise result_container['error']

    return result_container['result']


# -----------------------------------------------------------------------------
# 14. memory_stats() - Heap Analysis
# -----------------------------------------------------------------------------

def memory_stats() -> MemoryStats:
    """
    Get memory statistics from the CSSL runtime.

    Returns:
        MemoryStats with object counts and allocations

    Usage:
        stats = CSSL.memory_stats()
        print(f"Objects: {stats.objects}")
        print(f"Addresses: {stats.addresses}")
        for alloc in stats.top_allocations:
            print(f"  {alloc['type']}: {alloc['count']}")
    """
    cssl = get_cssl()
    runtime = cssl._get_runtime()

    objects = 0
    addresses = 0
    shared = len(_live_objects)
    scope_depth = 0
    global_count = 0
    type_counts: Dict[str, int] = {}

    # Count globals
    if hasattr(runtime, 'global_scope'):
        gs = runtime.global_scope
        if hasattr(gs, 'variables'):
            global_count = len(gs.variables)
            for name, value in gs.variables.items():
                objects += 1
                type_name = type(value).__name__
                type_counts[type_name] = type_counts.get(type_name, 0) + 1

    # Count scope chain depth
    if hasattr(runtime, 'scope'):
        scope = runtime.scope
        while scope:
            scope_depth += 1
            if hasattr(scope, 'variables'):
                objects += len(scope.variables)
            scope = getattr(scope, 'parent', None)

    # Count addresses
    try:
        from .cssl.cssl_types import Address
        if hasattr(Address, '_registry'):
            addresses = len(Address._registry)
    except ImportError:
        pass

    # Estimate memory (rough)
    bytes_used = objects * 100 + addresses * 64 + shared * 200

    # Top allocations by type
    top_allocations = sorted(
        [{'type': t, 'count': c} for t, c in type_counts.items()],
        key=lambda x: x['count'],
        reverse=True
    )[:10]

    return MemoryStats(
        objects=objects,
        addresses=addresses,
        shared=shared,
        bytes_used=bytes_used,
        top_allocations=top_allocations,
        scope_depth=scope_depth,
        global_count=global_count
    )


# -----------------------------------------------------------------------------
# 15. export_symbols() - Symbol Inspection
# -----------------------------------------------------------------------------

def export_symbols(code: str = None) -> dict:
    """
    Extract all defined symbols from CSSL code or current runtime.

    Args:
        code: Optional CSSL code to analyze (None = current runtime)

    Returns:
        Dict with: functions, classes, variables, enums, constants

    Usage:
        symbols = CSSL.export_symbols('''
            int x = 5;
            define greet(name) { printl("Hello " + name); }
            class Person { string name; }
            enum Color { RED, GREEN, BLUE }
        ''')
        print(symbols['functions'])  # ['greet']
        print(symbols['classes'])    # ['Person']
    """
    result = {
        'functions': [],
        'classes': [],
        'variables': [],
        'enums': [],
        'constants': []
    }

    if code:
        try:
            from .cssl.cssl_parser import CSSLParser
            parser = CSSLParser(code)
            ast = parser.parse()
            _extract_symbols(ast, result)
        except Exception:
            pass
    else:
        cssl = get_cssl()
        runtime = cssl._get_runtime()

        if hasattr(runtime, 'global_scope') and hasattr(runtime.global_scope, 'variables'):
            for name, value in runtime.global_scope.variables.items():
                if name.startswith('_'):
                    continue

                if hasattr(value, 'type') and value.type == 'function':
                    result['functions'].append(name)
                elif hasattr(value, '__class__') and value.__class__.__name__ == 'CSSLClass':
                    result['classes'].append(name)
                elif hasattr(value, '__class__') and value.__class__.__name__ == 'CSSLEnum':
                    result['enums'].append(name)
                else:
                    result['variables'].append(name)

    return result


def _extract_symbols(ast, result: dict):
    """Extract symbols from AST recursively."""
    if ast is None:
        return

    node_type = getattr(ast, 'type', None)
    value = getattr(ast, 'value', None)

    if node_type == 'function':
        func_info = value if isinstance(value, dict) else {}
        name = func_info.get('name')
        if name and not name.startswith('_'):
            if func_info.get('is_const'):
                result['constants'].append(name)
            else:
                result['functions'].append(name)

    elif node_type == 'class':
        class_info = value if isinstance(value, dict) else {}
        name = class_info.get('name')
        if name and not name.startswith('_'):
            result['classes'].append(name)

    elif node_type == 'enum':
        enum_info = value if isinstance(value, dict) else {}
        name = enum_info.get('name')
        if name and not name.startswith('_'):
            result['enums'].append(name)

    elif node_type == 'typed_declaration':
        decl = value if isinstance(value, dict) else {}
        name = decl.get('name')
        if name and not name.startswith('_'):
            modifiers = decl.get('modifiers', [])
            if 'const' in modifiers:
                result['constants'].append(name)
            else:
                result['variables'].append(name)

    if hasattr(ast, 'children'):
        for child in ast.children:
            _extract_symbols(child, result)


# -----------------------------------------------------------------------------
# 16. hook() / unhook() - Function Interception
# -----------------------------------------------------------------------------

_function_hooks: Dict[str, dict] = {}


def hook(func_name: str, before: Callable = None, after: Callable = None) -> str:
    """
    Add hooks before/after a CSSL function.

    Args:
        func_name: Name of the CSSL function to hook
        before: Callable(args, kwargs) called before function
        after: Callable(result, args, kwargs) called after function

    Returns:
        Hook ID for unhook()

    Usage:
        def log_before(args, kwargs):
            print(f"Calling with: {args}")

        def log_after(result, args, kwargs):
            print(f"Returned: {result}")

        hook_id = CSSL.hook("myFunction", before=log_before, after=log_after)
    """
    import uuid
    hook_id = str(uuid.uuid4())

    _function_hooks[hook_id] = {
        'func_name': func_name,
        'before': before,
        'after': after
    }

    # Install hooks into runtime
    cssl = get_cssl()
    runtime = cssl._get_runtime()

    if hasattr(runtime, '_hooks'):
        if func_name not in runtime._hooks:
            runtime._hooks[func_name] = []
        runtime._hooks[func_name].append({
            'id': hook_id,
            'before': before,
            'after': after
        })

    return hook_id


def unhook(hook_id: str) -> bool:
    """
    Remove a function hook.

    Args:
        hook_id: Hook ID from hook()

    Returns:
        True if hook was removed
    """
    if hook_id not in _function_hooks:
        return False

    info = _function_hooks[hook_id]
    func_name = info['func_name']

    cssl = get_cssl()
    runtime = cssl._get_runtime()

    if hasattr(runtime, '_hooks') and func_name in runtime._hooks:
        runtime._hooks[func_name] = [
            h for h in runtime._hooks[func_name] if h.get('id') != hook_id
        ]

    del _function_hooks[hook_id]
    return True


def unhook_all(func_name: str = None) -> int:
    """
    Remove all hooks for a function (or all hooks).

    Args:
        func_name: Function name (None = all hooks)

    Returns:
        Count of hooks removed
    """
    count = 0
    to_remove = []

    for hook_id, info in _function_hooks.items():
        if func_name is None or info['func_name'] == func_name:
            to_remove.append(hook_id)

    for hook_id in to_remove:
        if unhook(hook_id):
            count += 1

    return count


# -----------------------------------------------------------------------------
# 17. inject() - Code Injection
# -----------------------------------------------------------------------------

def inject(target_func: str, code: str, position: str = "before") -> bool:
    """
    Inject CSSL code into an existing function.

    Args:
        target_func: Name of the target CSSL function
        code: CSSL code to inject
        position: "before", "after", or "replace"

    Returns:
        True if injection was successful

    Usage:
        CSSL.run('define greet() { printl("Hello"); }')
        CSSL.inject("greet", 'printl("Before!");', "before")
        CSSL.run('greet();')  # Prints: Before! Hello
    """
    if position not in ("before", "after", "replace"):
        raise ValueError(f"Invalid position: {position}. Use 'before', 'after', or 'replace'")

    cssl = get_cssl()
    runtime = cssl._get_runtime()

    # Find the target function
    target = None
    if hasattr(runtime, 'global_scope'):
        target = runtime.global_scope.get(target_func)
    if target is None and hasattr(runtime, 'scope'):
        target = runtime.scope.get(target_func)

    if target is None or not hasattr(target, 'children'):
        return False

    try:
        from .cssl.cssl_parser import CSSLParser
        parser = CSSLParser(code)
        inject_ast = parser.parse()

        if position == "before":
            # Prepend children
            new_children = list(inject_ast.children) + list(target.children)
            target.children = new_children
        elif position == "after":
            # Append children
            target.children = list(target.children) + list(inject_ast.children)
        else:  # replace
            target.children = list(inject_ast.children)

        return True
    except Exception:
        return False


# -----------------------------------------------------------------------------
# 18. format() - Code Formatting
# -----------------------------------------------------------------------------

def format_code(code: str, style: dict = None) -> str:
    """
    Format CSSL code according to style rules.

    Args:
        code: CSSL code string to format
        style: Formatting options:
            - indent: Spaces per indent level (default: 4)
            - line_width: Max line width (default: 100)
            - brace_style: "allman" or "k&r" (default: "k&r")
            - space_around_ops: Add spaces around operators (default: True)

    Returns:
        Formatted code string
    """
    if style is None:
        style = {}

    indent_size = style.get('indent', 4)
    line_width = style.get('line_width', 100)
    brace_style = style.get('brace_style', 'k&r')
    space_around_ops = style.get('space_around_ops', True)

    lines = code.split('\n')
    result_lines = []
    current_indent = 0
    in_string = False
    in_multiline_comment = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            result_lines.append('')
            continue

        # Handle multiline comments
        if '/*' in stripped and '*/' not in stripped:
            in_multiline_comment = True
        if '*/' in stripped:
            in_multiline_comment = False

        # Adjust indent for closing braces
        if stripped.startswith('}') or stripped.startswith(')'):
            current_indent = max(0, current_indent - 1)

        # Format line
        formatted = ' ' * (indent_size * current_indent) + stripped

        # Adjust indent for opening braces
        if stripped.endswith('{') or (stripped.endswith('(') and not stripped.endswith('()')):
            current_indent += 1

        # Handle K&R vs Allman brace style
        if brace_style == 'allman':
            # Move opening brace to next line
            if formatted.rstrip().endswith('{') and not formatted.strip().startswith('{'):
                base = formatted.rstrip()[:-1].rstrip()
                result_lines.append(base)
                result_lines.append(' ' * (indent_size * (current_indent - 1)) + '{')
                continue

        # Add spaces around operators
        if space_around_ops and not in_string and not in_multiline_comment:
            # Simple operator spacing
            for op in ['==', '!=', '<=', '>=', '&&', '||', '+=', '-=', '*=', '/=']:
                formatted = formatted.replace(op, f' {op} ')
            for op in ['=', '+', '-', '*', '/', '<', '>']:
                # Avoid double-spacing
                if f' {op} ' not in formatted and f'{op}{op}' not in formatted:
                    formatted = re.sub(rf'(?<=[^\s{op}]){re.escape(op)}(?=[^\s{op}=])', f' {op} ', formatted)

        # Clean up multiple spaces
        while '  ' in formatted and not formatted.strip().startswith('//'):
            formatted = formatted.replace('  ', ' ')

        result_lines.append(formatted)

    return '\n'.join(result_lines)


# Alias without conflicting with potential future 'format' builtin
cssl_format = format_code


# -----------------------------------------------------------------------------
# 19. benchmark() - Performance Testing
# -----------------------------------------------------------------------------

def benchmark(code: str, iterations: int = 1000, warmup: int = 10) -> BenchmarkResult:
    """
    Benchmark CSSL code execution over multiple iterations.

    Args:
        code: CSSL code to benchmark
        iterations: Number of iterations to run
        warmup: Number of warmup iterations (not counted)

    Returns:
        BenchmarkResult with timing statistics

    Usage:
        result = CSSL.benchmark('x = 1 + 2 * 3;', iterations=10000)
        print(f"Average: {result.avg_ms:.4f}ms")
        print(f"Min: {result.min_ms:.4f}ms")
        print(f"Max: {result.max_ms:.4f}ms")
    """
    import statistics

    cssl = get_cssl()
    times = []

    # Warmup runs
    for _ in range(warmup):
        cssl.run(code)

    # Timed runs
    for _ in range(iterations):
        start = time.perf_counter()
        cssl.run(code)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        times.append(elapsed)

    avg_ms = statistics.mean(times)
    min_ms = min(times)
    max_ms = max(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0.0
    total_ms = sum(times)

    return BenchmarkResult(
        iterations=iterations,
        avg_ms=avg_ms,
        min_ms=min_ms,
        max_ms=max_ms,
        std_dev=std_dev,
        total_ms=total_ms,
        times=times
    )


# -----------------------------------------------------------------------------
# 20. context() - Context Manager for Temporary Scope
# -----------------------------------------------------------------------------

@contextlib.contextmanager
def context(globals_dict: dict = None, **options) -> Iterator['CSSLContext']:
    """
    Create a temporary CSSL execution context.

    Args:
        globals_dict: Variables to add to the context
        **options: Context options (timeout, sandbox, etc.)

    Yields:
        CSSLContext object for executing code

    Usage:
        with CSSL.context(player=my_player, debug=True) as ctx:
            ctx.run("$player.health = 100")
            result = ctx.run("return $player.health")
    """
    ctx = CSSLContext(globals_dict, **options)
    try:
        yield ctx
    finally:
        ctx._cleanup()


class CSSLContext:
    """
    Temporary CSSL execution context with isolated scope.
    """

    def __init__(self, globals_dict: dict = None, **options):
        self._cssl = get_cssl()
        self._options = options
        self._shared_names: List[str] = []
        self._original_globals: Dict[str, Any] = {}

        # Share globals
        if globals_dict:
            for name, value in globals_dict.items():
                self._shared_names.append(name)
                share(value, name)

        # Set up options
        for name, value in options.items():
            if name not in ('timeout', 'sandbox'):
                self._shared_names.append(name)
                share(value, name)

    def run(self, code: str, *args) -> Any:
        """Execute code in this context."""
        timeout = self._options.get('timeout')
        is_sandbox = self._options.get('sandbox', False)

        if is_sandbox:
            return sandbox(code, {'max_time': timeout or 5.0})
        elif timeout:
            return run_with_timeout(code, *args, timeout=timeout)
        else:
            return self._cssl.run(code, *args)

    def set(self, name: str, value: Any):
        """Set a variable in this context."""
        share(value, name)
        if name not in self._shared_names:
            self._shared_names.append(name)

    def get(self, name: str) -> Any:
        """Get a variable from this context."""
        return get_shared(name)

    def _cleanup(self):
        """Clean up context resources."""
        for name in self._shared_names:
            unshare(name)


# Export all
__all__ = [
    # Core classes
    'CsslLang',
    'CSSLModule',
    'CSSLScript',
    'CSSLFunctionModule',
    'get_cssl',

    # v3.8.0 primary API
    'run',
    '_run',
    'T_run',
    '_T_run',
    'script',
    'load',
    'execute',
    'include',

    # Legacy (deprecated)
    'exec',
    '_exec',
    'T_exec',
    '_T_exec',

    # Global/Output
    'set_global',
    'get_global',
    'get_output',
    'clear_output',
    'module',
    'makepayload',
    'makemodule',

    # Sharing
    'share',
    'unshare',
    'shared',
    'get_shared',
    'cleanup_shared',

    # v4.6.5: CsslWatcher for live Python instance access
    'CsslWatcher',
    'watcher_get',
    'watcher_set',
    'get_watcher',
    'list_watchers',

    # v4.9.12: Extended API - 20 New Features
    # 1. Developer Console
    'CSSLDevConsole',
    'async_console',
    'async_console_sync',

    # 2. Async/Await Support
    'async_run',
    'start_async',
    'await_result',
    'is_async_done',
    'cancel_async',

    # 3. Variable Watching
    'watch',
    'unwatch',
    'unwatch_all',

    # 4. Debug Stepping
    'breakpoint_add',
    'breakpoint_remove',
    'breakpoint_clear',
    'step',
    'continue_debug',
    'get_stack',
    'is_paused',

    # 5. Performance Profiling
    'profile',
    'ProfileResult',

    # 6. Code Validation
    'validate',
    'ValidationResult',

    # 7. Code Transpilation
    'transpile',

    # 8. State Serialization
    'serialize',
    'deserialize',
    'save_state',
    'load_state',

    # 9. Hot Reload
    'hot_reload',
    'enable_hot_reload',
    'disable_hot_reload',

    # 10. Event System
    'on',
    'once',
    'emit',
    'off',
    'off_all',

    # 11. Pipeline Chaining
    'pipe',
    'CSSLPipeline',

    # 12. Sandbox Execution
    'sandbox',
    'SecurityError',

    # 13. Timeout Execution
    'run_with_timeout',

    # 14. Memory Statistics
    'memory_stats',
    'MemoryStats',

    # 15. Symbol Export
    'export_symbols',

    # 16. Function Hooks
    'hook',
    'unhook',
    'unhook_all',

    # 17. Code Injection
    'inject',

    # 18. Code Formatting
    'format_code',
    'cssl_format',

    # 19. Benchmarking
    'benchmark',
    'BenchmarkResult',

    # 20. Context Manager
    'context',
    'CSSLContext',
]
