from .file_filters import (
    imports,
    re,
    os,
    get_args,
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
from .reader_utils import (
    imports,
    re,
    os,
    get_args,
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
    if_none_return,
    write_pdf,
    read_pdf,
    is_pdf_path,
    get_pdf_obj,
    get_separate_pages,
    get_pdf_pages,
    save_pdf,
    split_pdf,
    pdf_to_img_list,
    img_to_txt_list,
    open_pdf_file,
    get_pdfs_in_directory,
    get_all_pdf_in_directory,
    collate_pdfs,
    convert_date_string,
    source_engine_for_ext,
    is_valid_file_path,
    is_dataframe,
    create_dataframe,
    read_ods_file,
    read_ods_as_excel,
    filter_df,
    read_shape_file,
    pdf_to_text,
    get_df,
    read_any_file,
    read_file_as_text,
    read_files,
    read_directory,
    shoudSkipManager,
    SKIP_MGR,
    should_skip,
    re_initialize_skip_mgr,
)
from .find_collect import (
    imports,
    re,
    os,
    get_args,
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
    get_find_cmd,
    collect_globs,
    get_files_and_dirs,
    collect_filepaths,
    get_filename,
    find_files,
)
STOP_SEARCH = False

def request_find_console_stop():
    global STOP_SEARCH
    STOP_SEARCH = True

def reset_find_console_stop():
    global STOP_SEARCH
    STOP_SEARCH = False

def get_contents(
    full_path=None,
    parse_lines=False,
    content=None
    ):
    if full_path:
        content = content or read_any_file(full_path)
    if content:
        if parse_lines:
            content = str(content).split('\n')
        return make_list(content,commaparse=False)
    return []

def _normalize(s: str, strip_comments=True, collapse_ws=True, lower=True):
    if s is None:
        return ""
    if strip_comments:
        s = s.split('//', 1)[0]
    if collapse_ws:
        s = re.sub(r'\s+', ' ', s)
    if lower:
        s = s.lower()
    return s.strip()

def stringInContent(content, strings, total_strings=False, normalize=False):
    if not content:
        return False
    if normalize:
        c = _normalize(str(content))
        
        found = [s for s in strings if _normalize(s) and _normalize(s) in c]
    else:
        c = str(content)
        found = [s for s in strings if s and s in c]
    if not found:
        return False
    return len(found) == len(strings) if total_strings else True
def find_file(content, spec_line, strings, total_strings=False):
    lines = content.split('\n')
    if 1 <= spec_line <= len(lines):
        return stringInContent(lines[spec_line - 1], strings, total_strings=total_strings)
    return False
def find_lines(content, strings, total_strings=False, normalize=True, any_per_line=True):
    lines = content.split('\n')
    hits = []
    for i, line in enumerate(lines):
        # match one line either if ANY string matches or if ALL match (configurable)
        if any_per_line:
            match = stringInContent(line, strings, total_strings=False, normalize=normalize)
        else:
            match = stringInContent(line, strings, total_strings=True,  normalize=normalize)
        if match:
            hits.append({"line": i+1, "content": line})
    return hits
def getPaths(files, strings):
    tot_strings = strings
    nu_files, found_paths = [], []
    if isinstance(strings,list):
        if len(strings) >1:
            tot_strings = '\n'.join(strings)
        else:
            if len(strings) == 0:
                return nu_files, found_paths
            tot_strings = strings[0]
    
    
    for file_path in files:
        try:
            og_content = read_any_file(file_path)
            if tot_strings not in og_content:
                continue
            if file_path not in nu_files:
                nu_files.append(file_path)
            ogLines = og_content.split('\n')
            # find all occurrences of the block
            for m in re.finditer(re.escape(tot_strings), og_content):
                start_line = og_content[:m.start()].count('\n') + 1  # 1-based
                curr = {'file_path': file_path, 'lines': []}
                for j in range(len(strings)):
                    ln = start_line + j
                    curr['lines'].append({'line': ln, 'content': ogLines[ln - 1]})
                found_paths.append(curr)
        except Exception as e:
            print(f"{e}")
    return nu_files, found_paths

def findContent(
    *args,
    strings: list=[],
    total_strings=True,
    parse_lines=False,
    spec_line=False,
    get_lines=True,
    diffs=False,
    **kwargs
):
    global STOP_SEARCH
    kwargs["directories"] = ensure_directories(*args,**kwargs)

    found_paths = []

    dirs, files = get_files_and_dirs(
        **kwargs
    )
    nu_files, found_paths = getPaths(files, strings)

    if diffs and found_paths:
        return found_paths

    for file_path in nu_files:
        if STOP_SEARCH:
            return found_paths   # early exit

        if file_path:
            og_content = read_any_file(file_path)
            contents = get_contents(
                file_path,
                parse_lines=parse_lines,
                content=og_content
            )
            found = False
            for content in contents:
                if STOP_SEARCH:
                    return found_paths  # bail out cleanly

                if stringInContent(content, strings, total_strings=True, normalize=True):
                    found = True
                    if spec_line:
                        found = find_file(og_content, spec_line, strings, total_strings=True)
                    if found:
                        if get_lines:
                            lines = find_lines(
                                og_content,
                                strings=strings,
                                total_strings=False,
                                normalize=True,
                                any_per_line=True
                            )
                            if lines:
                                file_path = {"file_path": file_path, "lines": lines}
                        found_paths.append(file_path)
                        break
    return found_paths
def return_function(start_dir=None,preferred_dir=None,basenames=None,functionName=None):
    if basenames:
        basenames = make_list(basenames,commaparse=False)
        abstract_file_finder = AbstractFileFinderImporter(start_dir=start_dir,preferred_dir=preferred_dir)
        paths = abstract_file_finder.find_paths(basenames)
        func = abstract_file_finder.import_function_from_path(paths[0], functionName)
        return func
def getLineNums(file_path):
    lines=[]
    if file_path and isinstance(file_path,dict):
        lines = file_path.get('lines')
        file_path = file_path.get('file_path')
    return file_path,lines
def get_line_content(obj):
    line,content=None,None
    if obj and isinstance(obj,dict):
        line=obj.get('line')
        content = obj.get('content')
    #print(f"line: {line}\ncontent: {content}")
    return line,content
def get_edit(file_path):
    if file_path and os.path.isfile(file_path):
        os.system(f"code {file_path}")
def editLines(file_paths):
    for file_path in file_paths:
        file_path,lines = getLineNums(file_path)
        for obj in lines:
            line,content = get_line_content(obj)
        get_edit(file_path)
def findContentAndEdit(*args,
    strings: list=[],
    total_strings=True,
    parse_lines=False,
    spec_line=False,
    get_lines=True,
    edit_lines=False,
    diffs=False,
    **kwargs
    ):
    file_paths = findContent(
        *args,
        strings=strings,
        total_strings=total_strings,
        parse_lines=parse_lines,
        spec_line=spec_line,
        get_lines=get_lines,
        diffs=diffs,
        **kwargs
        )
    if edit_lines:
        editLines(file_paths)
    return file_paths

