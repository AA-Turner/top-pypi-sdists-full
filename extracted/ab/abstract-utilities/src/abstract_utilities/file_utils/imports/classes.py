from .imports import (
    imports,
    re,
    shlex,
    os,
    json,
    tempfile,
    textwrap,
    glob,
    fnmatch,
    importlib,
    shutil,
    sys,
    posixpath,
    types,
    string,
    subprocess,
    pkgutil,
    inspect,
    Callable,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Union,
    Iterable,
    Dict,
    List,
    Set,
    get_args,
    datetime,
    Path,
    ModuleType,
    dataclass,
    field,
    ezodf,
    gpd,
    PyPDF2,
    pdfplumber,
    pd,
    pytesseract,
    convert_from_path,
    load_dotenv,
    jsonify,
    secure_filename,
    FileStorage,
)
from .module_imports import (
    make_list,
    get_media_exts,
    is_media_type,
    MIME_TYPES,
    is_str,
    if_not_bool_default,
    imports,
    re,
    shlex,
    os,
    json,
    tempfile,
    textwrap,
    glob,
    fnmatch,
    importlib,
    shutil,
    sys,
    posixpath,
    types,
    string,
    subprocess,
    pkgutil,
    inspect,
    Callable,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Union,
    Iterable,
    Dict,
    List,
    Set,
    get_args,
    datetime,
    Path,
    ModuleType,
    dataclass,
    field,
    ezodf,
    gpd,
    PyPDF2,
    pdfplumber,
    pd,
    pytesseract,
    convert_from_path,
    load_dotenv,
    jsonify,
    secure_filename,
    FileStorage,
    get_from_kwargs,
    eatAll,
    eatOuter,
    get_sleep,
    get_caller,
    get_caller_path,
    get_caller_dir,
    SingletonMeta,
    run_pruned_func,
    get_pass_from_key,
    get_password,
    get_print_sudo_cmd,
    get_password_cmd,
    get_sudo_cmd,
    get_raw_password_sudo_cmd,
    get_remote_bash,
    get_remote_ssh,
    get_remote_cmd,
    execute_cmd,
    run_local_cmd,
    run_remote_cmd,
    run_cmd,
    run_ssh_cmd,
    remote_cmd,
    ssh_cmd,
    local_cmd,
    run_any_cmd,
    any_cmd,
    cmd_run,
    PathBackend,
    LocalFS,
    SSHFS,
    REMOTE_RE,
    normalize_items,
    get_output,
    get_cmd_out,
    cmd_input,
    get_output_text,
    get_env_value,
    print_cmd,
    get_sudo_password,
    cmd_run_sudo,
    pexpect_cmd_with_args,
    get_user_pass_host_key,
    execute_cmd_input,
    exec_sudo_capture,
    exec_sudo,
    exec_expect,
    is_remote_file,
    is_remote_dir,
    is_local_file,
    is_local_dir,
    is_file,
    is_dir,
    is_exists,
    check_path_type,
    abstractEnv,
    eatInner,
    safe_split,
    line_contains,
    is_list,
    is_bool,
    get_slash,
    path_join,
    if_not_last_child_join,
    get_home_folder,
    simple_path_join,
    DEFAULT_FILE_NAME,
    DEFAULT_KEY,
    find_and_read_env_file,
    search_for_env_key,
    check_env_file,
    safe_env_load,
    split_eq,
    dotenv_load,
    AbstractEnv,
    get_env_path,
    read_from_file,
    write_to_file,
    get_logFile,
    if_none_default,
    if_none_change,
    get_initial_caller_dir,
)
from .constants import (
    imports,
    re,
    shlex,
    os,
    json,
    tempfile,
    textwrap,
    glob,
    fnmatch,
    importlib,
    shutil,
    sys,
    posixpath,
    types,
    string,
    subprocess,
    pkgutil,
    inspect,
    Callable,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Union,
    Iterable,
    Dict,
    List,
    Set,
    get_args,
    datetime,
    Path,
    ModuleType,
    dataclass,
    field,
    ezodf,
    gpd,
    PyPDF2,
    pdfplumber,
    pd,
    pytesseract,
    convert_from_path,
    load_dotenv,
    jsonify,
    secure_filename,
    FileStorage,
    make_list,
    get_media_exts,
    is_media_type,
    MIME_TYPES,
    is_str,
    if_not_bool_default,
    get_from_kwargs,
    eatAll,
    eatOuter,
    get_sleep,
    get_caller,
    get_caller_path,
    get_caller_dir,
    SingletonMeta,
    run_pruned_func,
    get_pass_from_key,
    get_password,
    get_print_sudo_cmd,
    get_password_cmd,
    get_sudo_cmd,
    get_raw_password_sudo_cmd,
    get_remote_bash,
    get_remote_ssh,
    get_remote_cmd,
    execute_cmd,
    run_local_cmd,
    run_remote_cmd,
    run_cmd,
    run_ssh_cmd,
    remote_cmd,
    ssh_cmd,
    local_cmd,
    run_any_cmd,
    any_cmd,
    cmd_run,
    PathBackend,
    LocalFS,
    SSHFS,
    REMOTE_RE,
    normalize_items,
    get_output,
    get_cmd_out,
    cmd_input,
    get_output_text,
    get_env_value,
    print_cmd,
    get_sudo_password,
    cmd_run_sudo,
    pexpect_cmd_with_args,
    get_user_pass_host_key,
    execute_cmd_input,
    exec_sudo_capture,
    exec_sudo,
    exec_expect,
    is_remote_file,
    is_remote_dir,
    is_local_file,
    is_local_dir,
    is_file,
    is_dir,
    is_exists,
    check_path_type,
    abstractEnv,
    eatInner,
    safe_split,
    line_contains,
    is_list,
    is_bool,
    get_slash,
    path_join,
    if_not_last_child_join,
    get_home_folder,
    simple_path_join,
    DEFAULT_FILE_NAME,
    DEFAULT_KEY,
    find_and_read_env_file,
    search_for_env_key,
    check_env_file,
    safe_env_load,
    split_eq,
    dotenv_load,
    AbstractEnv,
    get_env_path,
    read_from_file,
    write_to_file,
    get_logFile,
    if_none_default,
    if_none_change,
    get_initial_caller_dir,
    import_tag,
    from_tag,
    DEFAULT_ALLOWED_EXTS,
    DEFAULT_EXCLUDE_TYPES,
    DEFAULT_EXCLUDE_EXTS,
    DEFAULT_EXCLUDE_DIRS,
    DEFAULT_EXCLUDE_PATTERNS,
    AllowedPredicate,
    DEFAULT_EXCLUDE_FILE_PATTERNS,
    DEFAULT_ALLOWED_PATTERNS,
    DEFAULT_ALLOWED_DIRS,
    DEFAULT_ALLOWED_TYPES,
    CANONICAL_MAP,
    DEFAULT_ALLOWED_EXCLUDE_MAP,
    DEFAULT_CANONICAL_MAP,
)

@dataclass
class ScanConfig:
    allowed_exts: Set[str]
    exclude_exts: Set[str]
    allowed_types: Set[str]
    exclude_types: Set[str]
    allowed_dirs: List[str] = field(default_factory=list)
    exclude_dirs: List[str] = field(default_factory=list)
    allowed_patterns: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)

@dataclass
class SearchParams(ScanConfig):
    directories: List[str] = field(default_factory=list)
    add: bool = False
    recursive: bool = True
    strings: List[str] = field(default_factory=list)
    total_strings: bool = False
    parse_lines: bool = False
    spec_line: Union[bool, int] = False
    get_lines: bool = False

@dataclass
class AllParams(SearchParams):
    cfg = None
    allowed: Optional[Callable[[str], bool]] = None
    include_files: bool = True
    recursive: bool = True
def get_item_check_cmd(path, file=True, directory=False, exists=False):
    if (directory and file) or exists:
        typ = "e"
    elif file:
        typ = "f"
    elif directory:
        typ = "d"
    elif isinstance(file, str):
        if "f" in file:
            typ = "f"
        elif "d" in file:
            typ = "d"
        else:
            typ = "e"
    else:
        typ = "e"
    return f"test -{typ} {shlex.quote(path)} && echo __OK__ || true"


def get_all_item_check_cmd(path, file=True, directory=True, exists=True):
    collects = []
    out_js = {}

    if file:
        collects.append("file")
    if directory:
        collects.append("dir")
    if exists:
        collects.append("exists")

    if not collects:
        return out_js

    path = shlex.quote(path)
    for typ in collects:
        t = typ[0]  # f, d, or e
        out_js[typ] = f"test -{t} {path} && echo __OK__ || true"

    return out_js
        

def is_file(
    path,
    user_at_host=None,
    password=None,
    key=None,
    env_path=None,
    **kwargs
    ):
    if path:
        contingencies = list(set([user_at_host,password,key,env_path]))
        len_contingencies = len(contingencies)
        is_potential = (len_contingencies >1 or (None not in contingencies))
        if not is_potential:
            return os.path.isfile(path)
        cmd = get_item_check_cmd(path,file=True)
        return run_cmd(cmd=cmd,
                user_at_host=user_at_host,
                password=password,
                key=key,
                env_path=env_path,
                **kwargs
                )
def is_dir(
    path,
    user_at_host=None,
    password=None,
    key=None,
    env_path=None,
    **kwargs
    ):
    if path:
        contingencies = list(set([user_at_host,password,key,env_path]))
        len_contingencies = len(contingencies)
        is_potential = (len_contingencies >1 or (None not in contingencies))
        if not is_potential:
            return os.path.isdir(path)
        cmd = get_item_check_cmd(path,file=False,directory=True)
        return run_cmd(cmd=cmd,
                user_at_host=user_at_host,
                password=password,
                key=key,
                env_path=env_path,
                **kwargs
                )
def is_exists(
    path,
    user_at_host=None,
    password=None,
    key=None,
    env_path=None,
    **kwargs
    ):
    if path:
        contingencies = list(set([user_at_host,password,key,env_path]))
        len_contingencies = len(contingencies)
        is_potential = (len_contingencies >1 or (None not in contingencies))
        if not is_potential:
            return os.path.exists(path)
        if is_potential == True:
            cmd = get_item_check_cmd(path,exists=True)
            return run_cmd(cmd=cmd,
                    user_at_host=user_at_host,
                    password=password,
                    key=key,
                    env_path=env_path,
                    **kwargs
                    )
def is_any(
    path,
    user_at_host=None,
    password=None,
    key=None,
    env_path=None,
    **kwargs
    ):
    if path:
        contingencies = list(set([user_at_host,password,key,env_path]))
        len_contingencies = len(contingencies)
        is_potential = (len_contingencies >1 or (None not in contingencies))
        if not is_potential:
            return os.path.exists(path)
        if is_potential == True:
            out_js = get_all_item_check_cmd(path,file=True,directory=True,exists=True)
            for typ,cmd in out_js.items():
                response = run_cmd(cmd=cmd,
                        user_at_host=user_at_host,
                        password=password,
                        key=key,
                        env_path=env_path,
                        **kwargs
                        )
                result = "__OK__" in (response or "")
                if result:
                    return typ

class PathBackend(Protocol):
    def join(self, *parts: str) -> str: ...
    def isfile(self, path: str) -> bool: ...
    def isdir(self, path: str) -> bool: ...
    def glob_recursive(self, base: str, **opts) -> List[str]: ...
    def listdir(self, base: str) -> List[str]: ...

class LocalFS:
    def __init__(self, get_type=False, get_is_dir=False, get_is_file=False, get_is_exists=False, **kwargs):
        self.get_type = get_type
        self.get_is_dir = get_is_dir
        self.get_is_file = get_is_file
        self.get_is_exists = get_is_exists

    def join(self, *parts: str) -> str:
        return os.path.join(*parts)

    def isfile(self, path: str) -> bool:
        return os.path.isfile(path)

    def isdir(self, path: str) -> bool:
        return os.path.isdir(path)

    def isexists(self, path: str) -> bool:
        return os.path.exists(path)

    def istype(self, path: str) -> str | None:
        funcs_js = {"file": os.path.isfile, "dir": os.path.isdir, "exists": os.path.exists}
        for key, func in funcs_js.items():
            if func(path):
                return key
        return None

    def is_included(self, path, **kwargs):
        include_js = {}
        if self.get_type:
            include_js["typ"] = self.istype(path)
        if self.get_is_dir:
            include_js["dir"] = self.isdir(path)
        if self.get_is_file:
            include_js["file"] = self.isfile(path)
        if self.get_is_exists:
            include_js["exists"] = self.isexists(path)
        return include_js
    def glob_recursive(self, base: str, **opts) -> List[str]:
        """
        opts:
          - maxdepth: int | None
          - mindepth: int (default 1)
          - follow_symlinks: bool
          - include_dirs: bool
          - include_files: bool
          - exclude_hidden: bool
        """
        maxdepth = opts.get("maxdepth")
        mindepth = opts.get("mindepth", 1)
        follow   = opts.get("follow_symlinks", False)
        want_d   = opts.get("include_dirs", True)
        want_f   = opts.get("include_files", True)
        hide     = opts.get("exclude_hidden", False)

        results: List[str] = []
        base_depth = os.path.normpath(base).count(os.sep)

        for root, dirs, files in os.walk(base, followlinks=follow):
            depth = os.path.normpath(root).count(os.sep) - base_depth
            if maxdepth is not None and depth > maxdepth:
                dirs[:] = []
                continue
            if want_d and depth >= mindepth:
                for d in dirs:
                    if hide and d.startswith("."): continue
                    results.append(os.path.join(root, d))
            if want_f and depth >= mindepth:
                for f in files:
                    if hide and f.startswith("."): continue
                    results.append(os.path.join(root, f))
        return results

    def listdir(self, base: str) -> List[str]:
        try:
            return [os.path.join(base, name) for name in os.listdir(base)]
        except Exception:
            return []
def get_spec_kwargs(
    user_at_host=None,
    password=None,
    key=None,
    env_path=None,
    kwargs=None
):
    kwargs = kwargs or {}
    kwargs["user_at_host"] = kwargs.get("user_at_host") or user_at_host
    kwargs["password"] = kwargs.get("password") or password
    kwargs["key"] = kwargs.get("key") or key
    kwargs["env_path"] = kwargs.get("env_path") or env_path
    return kwargs
class SSHFS:
    """Remote POSIX backend via run_remote_cmd."""
    def __init__(self, password=None, key=None, env_path=None,
                 get_type=False, get_is_dir=False, get_is_file=False, get_is_exists=False, **kwargs):
        self.user_at_host = kwargs.get('user_at_host') or kwargs.get('user') or kwargs.get('host')
        self.password = password
        self.key = key
        self.env_path = env_path
        self.get_type = get_type
        self.get_is_dir = get_is_dir
        self.get_is_file = get_is_file
        self.get_is_exists = get_is_exists

    def cell_spec_kwargs(self, func, path, **kwargs):
        kwargs = get_spec_kwargs(
            user_at_host=self.user_at_host,
            password=self.password,
            key=self.key,
            env_path=self.env_path,
            kwargs=kwargs
        )
        return func(path, **kwargs)

    def is_included(self, path, **kwargs):
        include_js = {}
        if self.get_type:
            include_js["typ"] = self.istype(path, **kwargs)
        if self.get_is_dir:
            include_js["dir"] = self.isdir(path, **kwargs)
        if self.get_is_file:
            include_js["file"] = self.isfile(path, **kwargs)
        if self.get_is_exists:
            include_js["exists"] = self.isexists(path, **kwargs)
        return include_js

    def join(self, *parts: str) -> str:
        return posixpath.join(*parts)

    def isfile(self, path: str, **kwargs) -> bool:
        out = self.cell_spec_kwargs(is_file, path, **kwargs)
        return "__OK__" in (out or "")

    def isdir(self, path: str, **kwargs) -> bool:
        out = self.cell_spec_kwargs(is_dir, path, **kwargs)
        return "__OK__" in (out or "")

    def isexists(self, path: str, **kwargs) -> bool:
        out = self.cell_spec_kwargs(is_exists, path, **kwargs)
        return "__OK__" in (out or "")

    def istype(self, path: str, **kwargs) -> str | None:
        out = self.cell_spec_kwargs(is_any, path, **kwargs)
        return out

    def glob_recursive(self, base: str, **opts) -> List[str]:
        maxdepth = opts.get("maxdepth")
        mindepth = opts.get("mindepth", 1)
        follow   = opts.get("follow_symlinks", False)
        want_d   = opts.get("include_dirs", True)
        want_f   = opts.get("include_files", True)
        hide     = opts.get("exclude_hidden", False)

        parts = []
        if follow:
            parts.append("-L")
        parts += ["find", shlex.quote(base)]
        if mindepth is not None:
            parts += ["-mindepth", str(mindepth)]
        if maxdepth is not None:
            parts += ["-maxdepth", str(maxdepth)]

        type_filters = []
        if want_d and not want_f:
            type_filters = ["-type", "d"]
        elif want_f and not want_d:
            type_filters = ["-type", "f"]

        hidden_filter = []
        if hide:
            hidden_filter = ["!", "-regex", r".*/\..*"]

        cmd = " ".join(parts + type_filters + hidden_filter + ["-printf", r"'%p\n'"]) + " 2>/dev/null"
        out = run_remote_cmd(self.user_at_host, cmd)
        return [line.strip().strip("'") for line in (out or "").splitlines() if line.strip()]

    def listdir(self, base: str) -> List[str]:
        cmd = f"find {shlex.quote(base)} -maxdepth 1 -mindepth 1 -printf '%p\\n' 2>/dev/null"
        out = run_remote_cmd(self.user_at_host, cmd)
        return [line.strip() for line in (out or "").splitlines() if line.strip()]



def try_group(pre,item,strings):
    
    try:
        m = pre.match(item)
        for i,string in enumerate(strings):
            strings[i] = m.group(string)
        
    except:
        return None
    return strings
def normalize_items(
    paths: Iterable[str],
    user_at_host=None,
    get_type=True,
    get_is_dir=False,
    get_is_file=False,
    get_is_exists=False,
    **kwargs
) -> List[tuple[PathBackend, str, dict]]:
    pairs: List[tuple[PathBackend, str, dict]] = []
    host = user_at_host or kwargs.get("host") or kwargs.get("user")
    paths = make_list(paths)
    for item in paths:
        if not item:
            continue

        strings = try_group(REMOTE_RE, item, ["host", "path"])
        fs_host = None
        nuhost = None

        if (strings and None not in strings) or host:
            if strings and None not in strings:
                nuhost = strings[0]
                item = strings[1] or item
            nuhost = nuhost or host
            fs_host = SSHFS(
                nuhost,
                user_at_host=user_at_host,
                get_type=get_type,
                get_is_dir=get_is_dir,
                get_is_file=get_is_file,
                get_is_exists=get_is_exists,
                **kwargs
            )
        else:
            fs_host = LocalFS(
                get_type=get_type,
                get_is_dir=get_is_dir,
                get_is_file=get_is_file,
                get_is_exists=get_is_exists
            )

        includes = fs_host.is_included(item)
        pairs.append((fs_host, item, includes))
    return pairs


