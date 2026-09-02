from __future__ import annotations

import errno


def ls_no_access(path: str) -> str:
    return f"ls: cannot access '{path}': No such file or directory\n"


def ls_perm_denied_dir(path: str) -> str:
    return f"ls: cannot open directory '{path}': Permission denied\n"


def cat_no_file(path: str) -> str:
    return f"cat: {path}: No such file or directory\n"


def cat_is_dir(path: str) -> str:
    return f"cat: {path}: Is a directory\n"


def cat_perm(path: str) -> str:
    return f"cat: {path}: Permission denied\n"


def mkdir_exists(path: str) -> str:
    return f"mkdir: cannot create directory '{path}': File exists\n"


def mkdir_no_parent(path: str) -> str:
    return f"mkdir: cannot create directory '{path}': No such file or directory\n"


def mv_no_src(path: str) -> str:
    return f"mv: cannot stat '{path}': No such file or directory\n"


def cp_no_src(path: str) -> str:
    return f"cp: cannot stat '{path}': No such file or directory\n"


def cp_omit_dir(path: str) -> str:
    return f"cp: -r not specified; omitting directory '{path}'\n"


def rm_no_file(path: str) -> str:
    return f"rm: cannot remove '{path}': No such file or directory\n"


def rm_is_dir(path: str) -> str:
    return f"rm: cannot remove '{path}': Is a directory\n"


def rmdir_not_empty(path: str) -> str:
    return f"rmdir: failed to remove '{path}': Directory not empty\n"


def grep_no_file(path: str) -> str:
    return f"grep: {path}: No such file or directory\n"


def grep_is_dir(path: str) -> str:
    return f"grep: {path}: Is a directory\n"


def find_no_file(path: str) -> str:
    return f"find: '{path}': No such file or directory\n"


def chmod_no_access(path: str) -> str:
    return f"chmod: cannot access '{path}': No such file or directory\n"


def head_no_file(path: str) -> str:
    return f"head: cannot open '{path}' for reading: No such file or directory\n"


def tail_no_file(path: str) -> str:
    return f"tail: cannot open '{path}' for reading: No such file or directory\n"


def sed_no_file(path: str) -> str:
    return f"sed: can't read {path}: No such file or directory\n"


def cmd_not_found(cmd: str) -> str:
    return f"bash: {cmd}: command not found\n"


def cd_no_dir(path: str) -> str:
    return f"bash: cd: {path}: No such file or directory\n"


def cd_not_dir(path: str) -> str:
    return f"bash: cd: {path}: Not a directory\n"


def ln_exists(link: str) -> str:
    return f"ln: failed to create symbolic link '{link}': File exists\n"


# Single-quoted command set (per GNU coreutils 9.x quoting style).
_SINGLE_QUOTE_CMDS = frozenset(
    {
        "ls",
        "mv",
        "cp",
        "mkdir",
        "rm",
        "rmdir",
        "find",
        "chmod",
        "touch",
    }
)

# Bare path command set.
_BARE_PATH_CMDS = frozenset({"cat", "grep", "sed", "head", "tail"})


# Mapping of (cmd, errno) -> emitter.
_DISPATCH: dict[tuple[str, int], object] = {
    ("ls", errno.ENOENT): ls_no_access,
    ("ls", errno.EACCES): ls_perm_denied_dir,
    ("cat", errno.ENOENT): cat_no_file,
    ("cat", errno.EISDIR): cat_is_dir,
    ("cat", errno.EACCES): cat_perm,
    ("mkdir", errno.EEXIST): mkdir_exists,
    ("mkdir", errno.ENOENT): mkdir_no_parent,
    ("mv", errno.ENOENT): mv_no_src,
    ("cp", errno.ENOENT): cp_no_src,
    ("rm", errno.ENOENT): rm_no_file,
    ("rm", errno.EISDIR): rm_is_dir,
    ("rmdir", errno.ENOTEMPTY): rmdir_not_empty,
    ("grep", errno.ENOENT): grep_no_file,
    ("grep", errno.EISDIR): grep_is_dir,
    ("find", errno.ENOENT): find_no_file,
    ("chmod", errno.ENOENT): chmod_no_access,
    ("head", errno.ENOENT): head_no_file,
    ("tail", errno.ENOENT): tail_no_file,
    ("sed", errno.ENOENT): sed_no_file,
    ("cd", errno.ENOENT): cd_no_dir,
    ("cd", errno.ENOTDIR): cd_not_dir,
    ("ln", errno.EEXIST): ln_exists,
}


def from_oserror(cmd: str, path: str, err: OSError) -> str:
    code = err.errno
    if code is None:
        # Best-effort fallback: derive a reasonable message from the cmd's quoting.
        quoted = f"'{path}'" if cmd in _SINGLE_QUOTE_CMDS else path
        return f"{cmd}: {quoted}: {err.strerror or 'I/O error'}\n"
    handler = _DISPATCH.get((cmd, code))
    if handler is not None:
        return handler(path)  # type: ignore[operator]
    # Fallback when no specific mapping is registered.
    quoted = f"'{path}'" if cmd in _SINGLE_QUOTE_CMDS else path
    strerr = err.strerror or "I/O error"
    return f"{cmd}: {quoted}: {strerr}\n"
