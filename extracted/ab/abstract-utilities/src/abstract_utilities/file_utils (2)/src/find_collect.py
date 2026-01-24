from ..imports import *

from pathlib import Path
from typing import Optional, List, Set

def get_proper_type_str(string):
    if not string:
        return None
    string_lower = string.lower()
    items = {
        "d":["dir","dirs","directory","directories","d","dirname"],
        "f":["file","filepath","file_path","files","filepaths","file_paths","f"]
     }
    for key,values in items.items():
        if string_lower in values:
            return key
    init = string_lower[0] if len(string_lower)>0 else None
    if init in items:
        return init
def check_path_type(
    path: str,
    user: Optional[str] = None,
    host: Optional[str] = None,
    user_as_host: Optional[str] = None,
    use_shell: bool = False
) -> Literal["file", "directory", "missing", "unknown"]:
    """
    Determine whether a given path is a file, directory, or missing.
    Works locally or remotely (via SSH).

    Args:
        path: The path to check.
        user, host, user_as_host: SSH parameters if remote.
        use_shell: Force shell test instead of Python os.path.
    Returns:
        One of: 'file', 'directory', 'missing', or 'unknown'
    """

    # --- remote check if user/host is given ---
    if user_as_host or (user and host):
        remote_target = user_as_host or f"{user}@{host}"
        cmd = f"if [ -f '{path}' ]; then echo file; elif [ -d '{path}' ]; then echo directory; else echo missing; fi"
        try:
            result = subprocess.check_output(
                ["ssh", remote_target, cmd],
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=5
            ).strip()
            return result if result in ("file", "directory", "missing") else "unknown"
        except Exception:
            return "unknown"

    # --- local check ---
    if not use_shell:
        if os.path.isfile(path):
            return "file"
        elif os.path.isdir(path):
            return "directory"
        elif not os.path.exists(path):
            return "missing"
        return "unknown"
    else:
        # fallback using shell tests (useful for sandboxed contexts)
        cmd = f"if [ -f '{path}' ]; then echo file; elif [ -d '{path}' ]; then echo directory; else echo missing; fi"
        try:
            output = subprocess.check_output(
                cmd, shell=True, stderr=subprocess.DEVNULL, text=True
            ).strip()
            return output if output in ("file", "directory", "missing") else "unknown"
        except Exception:
            return "unknown"




def get_find_cmd(*args,
    mindepth: Optional[int] = None,
    maxdepth: Optional[int] = None,
    depth: Optional[int] = None,
    file_type: Optional[str] = None,  # 'f' or 'd'
    name: Optional[str] = None,
    size: Optional[str] = None,
    mtime: Optional[str] = None,
    perm: Optional[str] = None,
    user: Optional[str] = None,
    **kwargs
) -> str:
    """
    Construct a Unix `find` command string from cfg and explicit keyword args.

    - Honors allowed/excluded patterns, dirs, and extensions from ScanConfig.
    - Automatically applies mindepth/maxdepth/depth/file_type filters.
    """

    params = define_all_params(*args,**kwargs)
    cmd = [f"find {shlex.quote(params.directories[0])}"]

    # --- depth ---
    if depth is not None:
        cmd += [f"-mindepth {depth}", f"-maxdepth {depth}"]
    else:
        if mindepth is not None:
            cmd.append(f"-mindepth {mindepth}")
        if maxdepth is not None:
            cmd.append(f"-maxdepth {maxdepth}")

    # --- file type ---
    if file_type in ("f", "d"):
        cmd.append(f"-type {file_type}")

    # --- base attributes ---
    if name:
        cmd.append(f"-name {shlex.quote(name)}")
    if size:
        cmd.append(f"-size {shlex.quote(size)}")
    if mtime:
        cmd.append(f"-mtime {shlex.quote(mtime)}")
    if perm:
        cmd.append(f"-perm {shlex.quote(perm)}")
    if user:
        cmd.append(f"-user {shlex.quote(user)}")
    cfg = params.cfg
    # --- cfg-based filters ---
    if cfg:
        # allowed extensions
        if cfg.allowed_exts and cfg.allowed_exts != {"*"}:
            ext_expr = " -o ".join(
                [f"-name '*{e}'" for e in cfg.allowed_exts if e]
            )
            cmd.append(f"\\( {ext_expr} \\)")

        # disallowed extensions
        if cfg.exclude_exts:
            for e in cfg.exclude_exts:
                cmd.append(f"! -name '*{e}'")

        # allowed directories (match any path)
        if cfg.allowed_dirs and cfg.allowed_dirs != ["*"]:
            dir_expr = " -o ".join(
                [f"-path '*{d}*'" for d in cfg.allowed_dirs if d]
            )
            cmd.append(f"\\( {dir_expr} \\)")

        # exclude directories
        if cfg.exclude_dirs:
            for d in cfg.exclude_dirs:
                cmd.append(f"! -path '*{d}*'")

        # allowed patterns
        if cfg.allowed_patterns and cfg.allowed_patterns != ["*"]:
            pat_expr = " -o ".join(
                [f"-name '{p}'" for p in cfg.allowed_patterns if p]
            )
            cmd.append(f"\\( {pat_expr} \\)")

        # exclude patterns
        if cfg.exclude_patterns:
            for p in cfg.exclude_patterns:
                cmd.append(f"! -name '{p}'")

        # allowed types
        if cfg.allowed_types and cfg.allowed_types != {"*"}:
            type_expr = " -o ".join(
                [f"-path '*{t}*'" for t in cfg.allowed_types if t]
            )
            cmd.append(f"\\( {type_expr} \\)")

        # excluded types
        if cfg.exclude_types:
            for t in cfg.exclude_types:
                cmd.append(f"! -path '*{t}*'")

    return " ".join(cmd)



def collect_globs(*args,
    patterns: Optional[List[str]] = None,
    mindepth: Optional[int] = None,
    maxdepth: Optional[int] = None,
    depth: Optional[int] = None,
    file_type: Optional[str] = None,   # "f", "d", or None
    **kwargs
) -> List[str] | dict:
    """
    Collect file or directory paths recursively.

    - If file_type is None → returns {"f": [...], "d": [...]}
    - If file_type is "f" or "d" → returns a list of that type
    - Supports SSH mode via `user_at_host`
    """
    directories,cfg,allowed,include_files,recursive = get_file_filters(*args,**kwargs)

    type_strs = {"f":"files","d":"dirs"}
    file_type = get_proper_type_str(file_type)
    file_types = make_list(file_type)
    if file_type == None:
        file_types = ["f","d"]
    return_results = {}
    return_result=[]
    for file_type in file_types:
        type_str = type_strs.get(file_type)
        # Remote path (SSH)
        for directory in directories:
            find_cmd = get_find_cmd(
                    directory,
                    cfg=cfg,
                    mindepth=mindepth,
                    maxdepth=maxdepth,
                    depth=depth,
                    file_type=file_type,
                    **{k: v for k, v in kwargs.items() if v},
                )
            result = run_pruned_func(run_cmd,find_cmd,
                **kwargs
                
                )
            return_result = [res for res in result.split('\n') if res]
            if type_str not in return_results:
                return_results[type_str]=[]
            return_results[type_str]+=return_result
    if len(file_types) == 1:
        return return_result
    return return_results

##    # Local path (Python-native walk)
##    root = Path(directory)
##    
##    results_js = {"f": [], "d": []}
##
##    for p in root.rglob("*"):
##        if p.is_file():
##            kind = "f"
##        elif p.is_dir():
##            kind = "d"
##        else:
##            continue
##
##        # If file_type is specified, skip the other kind
##        if file_type and kind != file_type:
##            continue
##
##        if exts and kind == "f" and p.suffix.lower() not in exts:
##            continue
##
##        if patterns and not any(p.match(pat) for pat in patterns):
##            continue
##
##        results_js[kind].append(str(p))
##
##    # Return based on selection
##    if file_type is None:
##        return results_js
##    else:
##        return results_js[file_type]


