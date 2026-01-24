from .imports import *

def get_user_pass_host_key(**kwargs):
    args = ['password','user_at_host','host','key','user']
    kwargs['del_kwarg']=kwargs.get('del_kwarg',False)
    values,kwargs = get_from_kwargs(*args,**kwargs)
    return values

# --- Base remote checker -----------------------------------------------------
def _remote_test(path: str, test_flag: str, timeout: int = 5,*args, **kwargs) -> bool:
    """
    Run a remote shell test (e.g. -f, -d) via SSH.
    Returns True if test succeeds, False otherwise.
    """
    try:
        kwargs['cmd']=f"[ {test_flag} {shlex.quote(path)} ] && echo 1 || echo 0"
        kwargs['text']=True
        kwargs['timeout']=timeout
        kwargs['stderr']=subprocess.DEVNULL
        result = run_pruned_func(run_cmd,**kwargs)
        return result.strip() == "1"
    except Exception:
        return False


# --- Individual path checks --------------------------------------------------
def is_remote_file(path: str,*args, **kwargs) -> bool:
    """True if remote path is a file."""
    return _remote_test(path, "-f", **kwargs)


def is_remote_dir(path: str,*args, **kwargs) -> bool:
    """True if remote path is a directory."""
    return _remote_test(path, "-d", **kwargs)


def is_local_file(path: str) -> bool:
    """True if local path is a file."""
    return os.path.isfile(path)


def is_local_dir(path: str) -> bool:
    """True if local path is a directory."""
    return os.path.isdir(path)


# --- Unified interface -------------------------------------------------------

def is_file(path: str,*args,**kwargs) -> bool:
    """Determine if path is a file (works local or remote)."""
    if get_user_pass_host_key(**kwargs):
        return is_remote_file(path, **kwargs)
    return is_local_file(path)


def is_dir(path: str, *args,**kwargs) -> bool:
    """Determine if path is a directory (works local or remote)."""
    if get_user_pass_host_key(**kwargs):
        return is_remote_dir(path, **kwargs)
    return is_local_dir(path)

def is_exists(path: str, *args,**kwargs) -> bool:
    if is_file(path,**kwargs):
        return True
    if is_dir(path,**kwargs):
        return True
    return False
# --- Optional: keep your original all-in-one wrapper ------------------------
def check_path_type(
    path: str,
    *args,
    **kwargs
) -> str:
    """
    Return 'file', 'directory', 'missing', or 'unknown'.
    Uses isolated is_file/is_dir functions.
    """
    if get_user_pass_host_key(**kwargs):
        if is_remote_file(path,**kwargs):
            return "file"
        elif is_remote_dir(path,**kwargs):
            return "directory"
        else:
            return "missing"
    else:
        if os.path.isfile(path):
            return "file"
        elif os.path.isdir(path):
            return "directory"
        elif not os.path.exists(path):
            return "missing"
        return "unknown"
