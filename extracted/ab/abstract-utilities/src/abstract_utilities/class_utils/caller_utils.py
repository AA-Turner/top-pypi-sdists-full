from .imports import *

def get_initial_caller() -> str:
    """
    Return the TRUE original caller: the entrypoint script that launched the program.
    """
    main_mod = sys.modules.get('__main__')
    
    # interactive environments (REPL) may have no __file__
    if not main_mod or not hasattr(main_mod, '__file__'):
        return None

    return os.path.realpath(main_mod.__file__)
def get_initial_caller_dir() -> str:
    """
    Return the directory of the TRUE original entrypoint script.
    """
    caller = get_initial_caller()
    return os.path.dirname(caller) if caller else None

def get_caller(i: Optional[int] = None) -> str:
    """
    Return the filename of the calling frame.

    Args:
        i: Optional stack depth offset. 
           None = immediate caller (depth 1).

    Returns:
        Absolute path of the file for the stack frame.
    """
    depth = 1 if i is None else int(i)
    stack = inspect.stack()
    if depth >= len(stack):
        depth = len(stack) - 1
    return stack[depth].filename


def get_caller_path(i: Optional[int] = None) -> str:
    """
    Return the absolute path of the caller's file.
    """
    depth = 1 if i is None else int(i)
    file_path = get_caller(depth + 1)
    return os.path.realpath(file_path)


def get_caller_dir(i: Optional[int] = None) -> str:
    """
    Return the absolute directory of the caller's file.
    """
    depth = 1 if i is None else int(i)
    abspath = get_caller_path(depth + 1)
    return os.path.dirname(abspath)


def get_original_caller_dir(levels_up: int = None) -> Path:
    """
    Return the directory of the *original* caller in the call stack.

    levels_up:
        - None → automatically goes to the bottom-most user-level caller.
        - N    → manually walk up N frames for custom behavior.
    
    Returns:
        Path object pointing to caller's directory.
    """

    stack = inspect.stack()

    # If the user specifies an exact depth
    if levels_up is not None:
        target = min(levels_up + 1, len(stack) - 1)
        frame = stack[target]
        return Path(frame.filename).resolve().parent

    # Otherwise, auto-detect the FIRST file that isn't inside site-packages or abstract_* utilities
    for frameinfo in reversed(stack):
        file_path = Path(frameinfo.filename).resolve()

        # Skip internal interpreter/frame files
        if "site-packages" in str(file_path):
            continue
        if "abstract_" in file_path.name:
            continue
        if file_path.name.startswith("<"):
            continue

        return file_path.parent

    # Fallback: last entry in the stack
    return Path(stack[-1].filename).resolve().parent
