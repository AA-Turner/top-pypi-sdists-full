from ..imports import *
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
    return None
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


