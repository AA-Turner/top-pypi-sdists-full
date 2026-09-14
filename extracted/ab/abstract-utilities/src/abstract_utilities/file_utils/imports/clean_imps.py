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
    types,
    string,
    subprocess,
    pkgutil,
    inspect,
    Callable,
    Literal,
    Optional,
    Tuple,
    Union,
    Dict,
    List,
    Set,
    get_args,
    datetime,
    Path,
    ModuleType,
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
from .module_imports import read_from_file, eatAll,make_list
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
    types,
    string,
    subprocess,
    pkgutil,
    inspect,
    Callable,
    Literal,
    Optional,
    Tuple,
    Union,
    Dict,
    List,
    Set,
    get_args,
    datetime,
    Path,
    ModuleType,
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

# ============================================================
# Helpers
# ============================================================
def get_caller_path(i=None):
    i = i or 1
    frame = inspect.stack()[i]
    return os.path.abspath(frame.filename)



def eatElse(stringObj, chars=None):
    chars = make_list(chars or []) + list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
    while stringObj:
        if stringObj and stringObj[0] not in chars:
            stringObj = stringObj[1:]
            continue
        if stringObj and stringObj[-1] not in chars:
            stringObj = stringObj[:-1]
            continue
        break
    return stringObj

def clean_line(line):
    return eatAll(line, [' ', '', '\t', '\n'])

def is_line_import(line):
    return bool(line and line.startswith(import_tag) and 'from ' not in line)

def is_line_from_import(line):
    return bool(line and line.startswith(from_tag) and ' import ' in line)

def is_from_group_start(line):
    return bool(line and line.startswith(from_tag) and 'import' in line and '(' in line and not line.rstrip().endswith(')'))

def is_from_group_end(line):
    return bool(line and ')' in line)

def clean_imports(imports):
    if isinstance(imports, str):
        imports = imports.split(',')
    return [eatElse(imp.strip()) for imp in imports if imp.strip()]

# ============================================================
# Combine lone import statements
# ============================================================
def combine_lone_imports(text=None, file_path=None):
    text = text or ''
    if file_path and os.path.isfile(file_path):
        text += read_from_file(file_path)
    lines = text.split('\n')

    cleaned_import_list = []
    nu_lines = []
    j = None

    for i, line in enumerate(lines):
        if is_line_import(line):
            if j is None:
                nu_lines.append(import_tag)
                j = i
            cleaned_import_list += clean_imports(line.split(import_tag)[1])
        else:
            nu_lines.append(line)

    if j is None:
        return '\n'.join(nu_lines)
    cleaned_import_list = sorted(set(cleaned_import_list))
    nu_lines[j] += ', '.join(cleaned_import_list)
    return '\n'.join(nu_lines)

# ============================================================
# Merge repeated 'from pkg import ...' (1-line only)
# Preserve multi-line grouped imports
# ============================================================
def merge_from_import_groups(text=None, file_path=None):
    if file_path and os.path.isfile(file_path):
        text = read_from_file(file_path)
    text = text or ''
    lines = text.split('\n')

    pkg_to_imports: Dict[str, Set[str]] = {}
    pkg_to_line_index: Dict[str, int] = {}
    nu_lines: List[str] = []

    in_group = False
    for i, line in enumerate(lines):
        stripped = line.strip()

        # preserve multi-line grouped blocks intact
        if in_group:
            nu_lines.append(line)
            if is_from_group_end(line):
                in_group = False
            continue

        if is_from_group_start(line):
            in_group = True
            nu_lines.append(line)
            continue

        if is_line_from_import(line):
            try:
                pkg_part, imps_part = line.split(' import ', 1)
                pkg_name = pkg_part.replace('from ', '').strip()
                imps = clean_imports(imps_part)
            except Exception:
                nu_lines.append(line)
                continue

            if pkg_name not in pkg_to_imports:
                pkg_to_imports[pkg_name] = set(imps)
                pkg_to_line_index[pkg_name] = len(nu_lines)
                nu_lines.append(line)
            else:
                pkg_to_imports[pkg_name].update(imps)
        else:
            nu_lines.append(line)

    # Rewrite first occurrences
    for pkg, idx in pkg_to_line_index.items():
        all_imps = sorted(pkg_to_imports[pkg])
        nu_lines[idx] = f"from {pkg} import {', '.join(all_imps)}"

    return '\n'.join(nu_lines)

# ============================================================
# Pipeline
# ============================================================
def clean_imports_pipeline(path: str):
    raw = read_from_file(path)
    step1 = combine_lone_imports(text=raw)
    step2 = merge_from_import_groups(text=step1)
    return step2

# ============================================================
# Standalone Run
# ============================================================
if __name__ == "__main__":
    abs_path = "/home/flerb/Documents/pythonTools/modules/src/modules/abstract_utilities/src/abstract_utilities/file_utils/imports/imports.py"
    cleaned = clean_imports_pipeline(abs_path)
    print(cleaned)
