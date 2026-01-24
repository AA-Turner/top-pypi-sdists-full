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
        }

        # Check if source uses any Python-only builtins
        needs_python = any(
            re.search(rf'\b{builtin}\s*\(', source)
            for builtin in PYTHON_ONLY_BUILTINS
        )

        # unative forces Python execution (skip C++ entirely)
        # force_python flag also skips C++ (for full builtin support like getcwd, listdir)
        # Auto-detect Python-only builtins and use Python automatically
        if has_unative or force_python or needs_python:
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


# Export all
__all__ = [
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
    # Other
    'set_global',
    'get_global',
    'get_output',
    'clear_output',
    'module',
    'makepayload',
    'makemodule',
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
]
