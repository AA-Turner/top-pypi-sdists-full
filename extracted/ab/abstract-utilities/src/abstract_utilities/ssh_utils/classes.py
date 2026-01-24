from .imports import *

class PathBackend(Protocol):
    def join(self, *parts: str) -> str: ...
    def isfile(self, path: str) -> bool: ...
    def isdir(self, path: str) -> bool: ...
    def glob_recursive(self, base: str, **opts) -> List[str]: ...
    def listdir(self, base: str) -> List[str]: ...

class LocalFS:
    def join(self, *parts: str) -> str:
        return os.path.join(*parts)
    def isfile(self, path: str) -> bool:
        return os.path.isfile(path)
    def isdir(self, path: str) -> bool:
        return os.path.isdir(path)
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

class SSHFS:
    """Remote POSIX backend via your run_remote_cmd."""
    def __init__(self, user_at_host: str):
        self.user_at_host = user_at_host

    def join(self, *parts: str) -> str:
        return posixpath.join(*parts)

    def isfile(self, path: str) -> bool:
        cmd = f"test -f {shlex.quote(path)} && echo __OK__ || true"
        out = run_remote_cmd(self.user_at_host, cmd)
        return "__OK__" in (out or "")

    def isdir(self, path: str) -> bool:
        cmd = f"test -d {shlex.quote(path)} && echo __OK__ || true"
        out = run_remote_cmd(self.user_at_host, cmd)
        return "__OK__" in (out or "")

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

# ---- auto-detect "user@host:/abs/path" ----
REMOTE_RE = re.compile(r"^(?P<host>[^:\s]+@[^:\s]+):(?P<path>/.*)$")

def normalize_items(paths: Iterable[str],user_at_host=None,**kwargs) -> List[tuple[PathBackend, str]]:
    pairs: List[tuple[PathBackend, str]] = []
    host = user_at_host or kwargs.get('host')
    
    for item in paths:
        if not item: continue
        m = REMOTE_RE.match(item)
        if m:
            pairs.append((SSHFS(m.group("host") or user_at_host), m.group("path")))
        else:
            pairs.append((LocalFS(), item))
    return pairs
