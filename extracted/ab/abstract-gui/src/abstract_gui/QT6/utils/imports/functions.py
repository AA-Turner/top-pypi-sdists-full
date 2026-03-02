from .imports import *

# -----------------------------------------------------------------------------
#  helper heuristics -----------------------------------------------------------
# -----------------------------------------------------------------------------

def _which(prog: str) -> str | None:
    return shutil.which(prog)

def _is_python_script(path: str) -> bool:
    low = path.lower()
    return low.endswith(".py") or (os.path.isfile(path) and open(path, 'rb').read(2) == b'#!' and b'python' in open(path, 'rb').read(64))

def _split_command(cmd: str | List[str]) -> Tuple[str, List[str]]:
    """
    Returns (program, args) ready for QProcess.start(program, args),
    handling quoted paths with spaces safely.
    """
    if isinstance(cmd, list):
        parts = cmd[:]  # assume already tokenized correctly by caller
    else:
        parts = shlex.split(cmd)  # keeps quoted paths intact

    if not parts:
        raise ValueError("Empty command")

    # If a single token is an existing .py file with spaces (quoted), run via python
    if len(parts) == 1 and _is_python_script(parts[0]) and os.path.exists(parts[0]):
        py = _which("python3") or sys.executable
        return py, ["-u", parts[0]]

    prog = parts[0]
    args = parts[1:]

    # If first token is a .py script, prefer python -u script.py args...
    if _is_python_script(prog) and os.path.exists(prog):
        py = _which("python3") or sys.executable
        return py, ["-u", prog, *args]

    # Otherwise, ensure program exists in PATH or as an absolute path
    resolved = _which(prog) if not os.path.isabs(prog) else prog
    if not resolved or (os.path.isabs(resolved) and not os.path.exists(resolved)):
        raise FileNotFoundError(f"Executable not found: {prog}")

    return resolved, args

def _wrap_stdbuf(program: str, args: List[str]) -> Tuple[str, List[str]]:
    """Wrap non-python programs with stdbuf if available to force line-buffered output."""
    base = os.path.basename(program)
    if base.startswith(("python", "python3")):
        return program, args
    sb = _which("stdbuf")
    if not sb:
        return program, args
    # We return stdbuf as the program, and shift the original as an arg
    return sb, ["-oL", "-eL", program, *args]
def log_path(): return LOG_FILE

