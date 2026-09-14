from ..imports import (
    imports,
    re,
    shlex,
    os,
    textwrap,
    importlib,
    sys,
    types,
    pkgutil,
    inspect,
    Callable,
    Optional,
    Tuple,
    Dict,
    List,
    get_args,
    ModuleType,
    load_dotenv,
    jsonify,
    secure_filename,
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
    ScanConfig,
    SearchParams,
    AllParams,
    get_item_check_cmd,
    get_all_item_check_cmd,
    is_any,
    get_spec_kwargs,
    try_group,
    eatElse,
    clean_line,
    is_line_import,
    is_line_from_import,
    is_from_group_start,
    is_from_group_end,
    clean_imports,
    combine_lone_imports,
    merge_from_import_groups,
    clean_imports_pipeline,
)
from .file_filters import (
    imports,
    re,
    shlex,
    os,
    textwrap,
    importlib,
    sys,
    types,
    pkgutil,
    inspect,
    Callable,
    Optional,
    Tuple,
    Dict,
    List,
    get_args,
    ModuleType,
    load_dotenv,
    jsonify,
    secure_filename,
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
    ScanConfig,
    SearchParams,
    AllParams,
    get_item_check_cmd,
    get_all_item_check_cmd,
    is_any,
    get_spec_kwargs,
    try_group,
    eatElse,
    clean_line,
    is_line_import,
    is_line_from_import,
    is_from_group_start,
    is_from_group_end,
    clean_imports,
    combine_lone_imports,
    merge_from_import_groups,
    clean_imports_pipeline,
    combine_params,
    get_safe_kwargs,
    create_canonical_map,
    get_safe_canonical_kwargs,
    get_dir_filter_kwargs,
    get_file_filter_kwargs,
    normalize_listlike,
    ensure_exts,
    ensure_patterns,
    ensure_directories,
    get_proper_type_str,
    get_allowed_predicate,
    get_globs,
    get_allowed_files,
    get_allowed_dirs,
    get_filtered_files,
    get_filtered_dirs,
    get_all_allowed_files,
    get_all_allowed_dirs,
    make_allowed_predicate,
    filter_allowed_items,
    derive_all_defaults,
    derive_file_defaults,
    define_defaults,
    get_file_filters,
)
from typing import (
    Optional,
    List,
)






def get_find_cmd(
    *args,
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
    Construct a Unix `find` command string that supports multiple directories.
    Accepts filtering via ScanConfig-compatible kwargs.
    """
    # Normalize inputs into canonical form
    kwargs = get_safe_canonical_kwargs(*args, **kwargs)
    cfg = kwargs.get('cfg') or define_defaults(**kwargs)

    # Get directory list (may come from args or kwargs)
    kwargs["directories"] = ensure_directories(*args, **kwargs)
    if not kwargs["directories"]:
        return []

    # Build base command for all directories
    dir_expr = " ".join(shlex.quote(d) for d in kwargs["directories"])
    cmd = [f"find {dir_expr}"]

    # --- depth filters ---
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

    # --- basic attributes ---
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

    # --- cfg-based filters ---
    if cfg:
        # Allowed extensions
        if cfg.allowed_exts and cfg.allowed_exts != {"*"}:
            ext_expr = " -o ".join(
                [f"-name '*{e}'" for e in cfg.allowed_exts if e]
            )
            cmd.append(f"\\( {ext_expr} \\)")

        # Excluded extensions
        if cfg.exclude_exts:
            for e in cfg.exclude_exts:
                cmd.append(f"! -name '*{e}'")

        # Allowed directories
        if cfg.allowed_dirs and cfg.allowed_dirs != ["*"]:
            dir_expr = " -o ".join(
                [f"-path '*{d}*'" for d in cfg.allowed_dirs if d]
            )
            cmd.append(f"\\( {dir_expr} \\)")

        # Excluded directories
        if cfg.exclude_dirs:
            for d in cfg.exclude_dirs:
                cmd.append(f"! -path '*{d}*'")

        # Allowed patterns
        if cfg.allowed_patterns and cfg.allowed_patterns != ["*"]:
            pat_expr = " -o ".join(
                [f"-name '{p}'" for p in cfg.allowed_patterns if p]
            )
            cmd.append(f"\\( {pat_expr} \\)")

        # Excluded patterns
        if cfg.exclude_patterns:
            for p in cfg.exclude_patterns:
                cmd.append(f"! -name '{p}'")

        # Allowed types (semantic, not `-type`)
        if cfg.allowed_types and cfg.allowed_types != {"*"}:
            type_expr = " -o ".join(
                [f"-path '*{t}*'" for t in cfg.allowed_types if t]
            )
            cmd.append(f"\\( {type_expr} \\)")

        # Excluded types
        if cfg.exclude_types:
            for t in cfg.exclude_types:
                cmd.append(f"! -path '*{t}*'")

    return " ".join(cmd)



def collect_globs(
    *args,
    mindepth: Optional[int] = None,
    maxdepth: Optional[int] = None,
    depth: Optional[int] = None,
    file_type: Optional[str] = None,   # "f", "d", or None
    allowed: Optional[Callable[[str], bool]] = None,
    **kwargs
) -> List[str] | dict:
    """
    Collect file or directory paths recursively.

    - If file_type is None → returns {"f": [...], "d": [...]}
    - If file_type is "f" or "d" → returns a list of that type
    - Supports SSH mode via `user_at_host`
    """
    user_pass_host_key = get_user_pass_host_key(**kwargs)
    kwargs["directories"] = ensure_directories(*args, **kwargs)
    kwargs= get_safe_canonical_kwargs(**kwargs)
    kwargs["cfg"] = kwargs.get('cfg') or define_defaults(**kwargs)
    
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
        find_cmd = get_find_cmd(
            directories=kwargs.get("directories"),
            cfg=kwargs.get('cfg'),
                mindepth=mindepth,
                maxdepth=maxdepth,
                depth=depth,
                file_type=file_type,
                **user_pass_host_key,
            )
        result = run_pruned_func(run_cmd,find_cmd,
            **kwargs
            
            )
        return_result = [res for res in result.split('\n') if res]
        return_results[type_str]=return_result
    if len(file_types) == 1:
        return return_result
    return return_results
def get_files_and_dirs(
    *args,
    recursive: bool = True,
    include_files: bool = True,
    **kwargs
    ):
    if recursive == False:
        kwargs['maxdepth']=1
    if include_files == False:
        kwargs['file_type']='d'
    result = collect_globs(*args,**kwargs)
    if include_files == False:
        return result,[]
    dirs = result.get("dirs")
    files = result.get("files")
    return dirs,files
def collect_filepaths(
    *args,
    **kwargs
    ) -> List[str]:
    kwargs['file_type']='f'
    return collect_globs(*args,**kwargs)

def get_filename(path):
    basename = os.path.basename(path)
    filename,ext = os.path.splitext(basename)
    return filename
def find_files(filename,directory=None,add=None):
    add = if_not_bool_default(add,default=True)
    directory = directory or os.getcwd()
    dirs,files = get_files_and_dirs(directory,add=add)
    return [file for file in files if get_filename(file) == filename]
