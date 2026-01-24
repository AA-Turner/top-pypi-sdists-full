"""
read_write_utils.py
-------------------
Unified read/write utility for safe file operations.
Supports:
- Writing content to a file
- Reading content from a file
- Creating and reading if missing
- Detecting file/content params via positional args or kwargs

Usage:
    from abstract_utilities.read_write_utils import *
"""

from .imports import *
_FILE_PATH_KEYS = ['file', 'filepath', 'file_path', 'path', 'directory', 'f', 'dst', 'dest']
_CONTENTS_KEYS = ['cont', 'content', 'contents', 'data', 'datas', 'dat', 'src', 'source']
from pathlib import Path
import uuid
import shlex

_STAGE_ROOT = Path("/var/tmp/abstract_stage")


def _stage_file(contents: str, suffix=".tmp") -> Path:
    """
    Write contents to a local staging file.
    """
    _STAGE_ROOT.mkdir(parents=True, exist_ok=True)
    path = _STAGE_ROOT / f"{uuid.uuid4().hex}{suffix}"
    path.write_text(str(contents), encoding="utf-8")
    return path


def _install_file(staged: Path, dest: str, **kwargs) -> str:
    """
    Atomically install a staged file to destination using sudo install.
    """
    cmd = (
        f"sudo install -D -m 0644 "
        f"{shlex.quote(str(staged))} "
        f"{shlex.quote(dest)}"
    )
    return run_local_cmd(
        cmd=cmd,
        password=kwargs.get("password"),
        key=kwargs.get("key"),
        env_path=kwargs.get("env_path"),
    )

            
# --- Helper utilities --------------------------------------------------------
def string_in_keys(strings, kwargs):
    """Find a matching keyword in kwargs that contains any of the given substrings."""
    for key in kwargs:
        for s in strings:
            if s.lower() in key.lower():
                return key
    return None
def make_dirs(path, exist_ok=True, **kwargs):
    remote = get_user_pass_host_key(**kwargs)
 
    if remote:
        kwargs['cmd'] = f"mkdir -p {path}"
       
        resp = run_pruned_func(run_cmd, **kwargs)
       
    else:
        os.makedirs(path, exist_ok=exist_ok)
    return path
def make_path(path, home_dir=None, file=None, **kwargs):
    if not path:
        return None

    basename = os.path.basename(path)
    parts = [p for p in path.split('/') if p]

    # Detect whether this is a file or a folder
    is_file = file if file is not None else ('.' in basename)
    pieces = parts[:-1] if is_file else parts
  
    full_dir = home_dir or '/'
    for piece in pieces:
        full_dir = os.path.join(full_dir, piece)
        make_dirs(full_dir, exist_ok=True, **kwargs)
       
    if is_file:
        full_dir = os.path.join(full_dir, basename)

    return full_dir
def get_rel_path(src,src_rel,dst,**kwargs):
    if src.startswith(src_rel):
        nu_src = src[len(src_rel):]
        nu_src= eatAll(nu_src,'/')
        directory= eatOuter(dst,'/')
        rel_path = os.path.join(dst,nu_src)
        return rel_path
def make_relative_path(src,src_rel,dst,**kwargs):

    if src.startswith(src_rel):
        rel_path = get_rel_path(src,src_rel,dst)
      
        path = make_path(rel_path,**kwargs)
      
        return path

def path_join(*args):
    path = None
    for i,arg in enumerate(args):
        if arg:
            if i == 0:
                path = arg
            else:
                path = os.path.join(path,arg)
    return path

def get_path(paths,**kwargs):
    """Return the first valid path among given paths."""
    for path in paths:
        if isinstance(path, str):
            if is_file(path,**kwargs):
                return path
            dirname = os.path.dirname(path)
            if is_exists(dirname,**kwargs):
                return path
    return None


def break_down_find_existing(path,**kwargs):
    """Return the first non-existent subpath within a path chain."""
    test_path = ''
    for part in path.split(os.sep):
        test_path = os.path.join(test_path, part)
        if not is_exists(test_path,**kwargs):
            return test_path if test_path else None
    return test_path


# --- Parameter parsing --------------------------------------------------------
def check_read_write_params(*args, **kwargs):
    """
    Determine file_path and contents from arguments.
    Returns a tuple: (file_path, contents)
    """
    file_key = string_in_keys(_FILE_PATH_KEYS, kwargs)
    content_key = string_in_keys(_CONTENTS_KEYS, kwargs)

    file_path = kwargs.get(file_key) if file_key else None
    contents = kwargs.get(content_key) if content_key else None

    # Handle positional args (fallback)
    if file_path is None and len(args) > 0:
        file_path = args[0]
    if contents is None and len(args) > 1:
        contents = args[1]

    if file_path is None:
        raise ValueError("Missing file_path argument.")
    return file_path, contents

def write_to_path(
        file_path: str,
        contents: str,
        *,
        user_at_host: str = None,
        cwd: str | None = None,
        password=None,
        key=None,
        env_path=None,
        **kwargs
    ) -> str:
    """
    Completely overwrite a file (locally or remotely).
    Supports sudo and password-based remote execution.
    """

    # sanitize for shell safety
    quoted_path = shlex.quote(file_path)
    quoted_data = shlex.quote(str(contents))

    # shell command that fully overwrites
    # (no append, replaces contents entirely)
    base_cmd = f'sudo sh -c "echo {quoted_data} > {quoted_path}"'

    # optional sudo password injection
    full_cmd = get_print_sudo_cmd(
        cmd=base_cmd,
        password=password,
        key=key,
        env_path=env_path
    )

    # local or remote dispatch
    if user_at_host:
        return run_remote_cmd(
            user_at_host=user_at_host,
            cmd=full_cmd,
            cwd=cwd,
            password=password,
            key=key,
            env_path=env_path,
            **kwargs
        )
    else:
        return run_local_cmd(
            cmd=full_cmd,
            cwd=cwd,
            password=password,
            key=key,
            env_path=env_path,
            **kwargs
        )
### --- Core functionality -------------------------------------------------------
##def write_to_file(*args, **kwargs):
##    """
##    Write contents to a file (create if missing).
##
##    Returns the file_path written.
##    """
##    file_path, contents = check_read_write_params(*args, **kwargs)
##    if contents is None:
##        raise ValueError("Missing contents to write.")
##
##    os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
##    with open(file_path, "w", encoding="utf-8") as f:
##        f.write(str(contents))
##    return file_path
# --- Core functionality -------------------------------------------------------
##def write_to_file(*args, **kwargs):
##    """
##    Write contents to a file (create if missing).
##
##    Returns the file_path written.
##    """
##    file_path, contents = check_read_write_params(*args, **kwargs)
##    values,kwargs = get_from_kwargs(['file_path','contents'],del_kwarg=True,**kwargs)
##    dirname = os.path.dirname(file_path)
##    
##    if contents is None:
##        raise ValueError("Missing contents to write.")
##    user_at_host = kwargs.get("user_at_host")
##    if get_user_pass_host_key(**kwargs):
##        make_dirs(dirname, exist_ok=True,**kwargs)
##        kwargs["cwd"] = kwargs.get('cwd') or os.path.dirname(file_path)
##        # sanitize for shell safety
##        quoted_path = shlex.quote(file_path)
##        quoted_data = shlex.quote(str(contents))
##        # shell command that fully overwrites
##        # (no append, replaces contents entirely)
##        kwargs["cmd"] = f'sh -c "echo {quoted_data} > {quoted_path}"'
##        if not kwargs.get('password') and not kwargs.get('key'):
##            kwargs["cmd"]=f'sudo {kwargs["cmd"]}'
##        result = run_pruned_func(run_cmd,**kwargs)
##        if 'file_path' in kwargs:
##            del kwargs['file_path']
##        if not is_file(file_path,**kwargs) or str(contents) != read_from_file(file_path,**kwargs):
##            kwargs["cmd"]=f'sudo {kwargs["cmd"]}'
##            result = run_pruned_func(run_cmd,**kwargs)
##        return result
##
##    make_dirs(dirname or ".", exist_ok=True)
##    with open(file_path, "w", encoding="utf-8") as f:
##        f.write(str(contents))
##    return file_path

def _should_use_remote(**kwargs) -> bool:
    """
    Only use remote mode IF:
    - user_at_host is provided
    - AND password/key is provided
    Otherwise: local write.
    """
    user = kwargs.get("user_at_host")
    if not user:
        return False  # not remote

    # If user_at_host is provided, then password or key MUST be present
    if kwargs.get("password") or kwargs.get("key"):
        return True

    return False  # user provided but no auth → treat as local


def _write_to_file(contents: str, file_path: str, **kwargs) -> str:
    """
    Unified writer using stage → install model.
    """

    remote = _should_use_remote(**kwargs)

    # --- Remote path (unchanged conceptually) ---
    if remote:
        tmp_path = _stage_file(contents)

        user_at_host = kwargs["user_at_host"]
        password = kwargs.get("password")
        key = kwargs.get("key")

        # copy staged file
        scp_cmd = (
            f"scp {shlex.quote(str(tmp_path))} "
            f"{shlex.quote(user_at_host)}:{shlex.quote(file_path)}"
        )
        return run_pruned_func(
            run_local_cmd,
            cmd=scp_cmd,
            password=password,
            key=key,
            **kwargs
        )

    # --- Local path ---
    try:
        # Attempt direct write for non-privileged paths
        os.makedirs(os.path.dirname(file_path) or ".", exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(str(contents))
        return file_path

    except (PermissionError, FileNotFoundError):
        # Privileged path → stage + install
        staged = _stage_file(contents)
        return _install_file(staged, file_path, **kwargs)



def write_to_file(*, contents: str, file_path: str, **kwargs):
    """
    Error-handled public writer.
    """
    try:
        return _write_to_file(contents=contents, file_path=file_path, **kwargs)
    except Exception as e:
        print("WRITE ERROR:", e)
        raise RuntimeError(f"Failed writing: {file_path}")
def read_from_file(file_path=None,**kwargs):
    if get_user_pass_host_key(**kwargs):
        kwargs["cwd"] = kwargs.get('cwd') or os.path.dirname(file_path)
        basename = os.path.basename(file_path)
        kwargs["cmd"] = f'cat {basename}'
        return run_pruned_func(run_cmd,**kwargs)
    """Read text content from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def copy_dirs(dirs, dst_root, src_rel=None, **kwargs):
    """
    Recursively copy directory structures (without files) from dirs → dst_root.
    """
    for src in dirs:
        # build destination path preserving relative structure
        dst_path = make_relative_path(src, src_rel, dst_root, **kwargs) if src_rel else dst_root
        make_path(dst_path, **kwargs)  # ensures directory exists
     


def copy_file(src, dst_root, src_rel=None, **kwargs):
    """
    Copy a single file to dst_root, preserving relative structure if src_rel provided.
    Supports remote copy via read/write.
    """
    # derive destination file path
    dst_path = make_relative_path(src, src_rel, dst_root, **kwargs) if src_rel else os.path.join(dst_root, os.path.basename(src))
    make_path(dst_path, **kwargs)

    if get_user_pass_host_key(**kwargs):  # remote mode
        contents = read_from_file(src, **kwargs)
        write_to_file(contents=contents, file_path=dst_path, **kwargs)
    else:  # local
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src, dst_path)


    return dst_path


def copy_files(files, dst_root, src_rel=None, **kwargs):
    """
    Copy a list of files to dst_root.
    """
    for src in files:
        copy_file(src=src, dst_root=dst_root, src_rel=src_rel, **kwargs)

def create_and_read_file(*args, **kwargs):
    """
    Create the file (if missing) and read contents from it.
    """
    file_path, contents = check_read_write_params(*args, **kwargs)
    if not os.path.isfile(file_path):
        write_to_file(file_path, contents or "")
    return read_from_file(file_path)


def is_file_extension(obj: str) -> bool:
    """Return True if obj looks like a filename with extension."""
    if not isinstance(obj, str):
        return False
    root, ext = os.path.splitext(obj)
    return bool(root and ext)


def delete_file(file_path: str):
    """Safely delete a file if it exists."""
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    return False


def get_content_lines(*args, **kwargs):
    """Return a list of lines from string or file path."""
    file_path, contents = check_read_write_params(*args, **kwargs)
    if os.path.isfile(file_path):
        contents = read_from_file(filepath)

    if isinstance(contents, str):
        return contents.splitlines()
    elif isinstance(contents, list):
        return contents
    return []
def collate_text_docs(directory=None):
    return [read_from_file(item) for item in get_all_files(directory=directory)]
def get_content(*paths):
    item_path = os.path.join(*paths)
    if os.path.isfile(item_path):
        try:
            content = read_from_file(item_path)
            return content
        except:
            pass
    return None
def get_text_or_read(text=None,file_path=None):
    text = text or ''
    imports_js = {}
    if not text and file_path and os.path.isfile(file_path):
        text=read_from_file(file_path)
    return text
##
