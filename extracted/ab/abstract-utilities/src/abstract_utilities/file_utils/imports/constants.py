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
# -------------------------
# Config dataclass
# -------------------------
# ============================================================
# Constants
# ============================================================
import_tag = 'import '
from_tag = 'from '

# -------------------------
# Default sets
# -------------------------
DEFAULT_ALLOWED_EXTS: Set[str] = {
    ".py", ".pyw",                             # python
    ".js", ".jsx", ".ts", ".tsx", ".mjs",      # JS/TS
    ".html", ".htm", ".xml",                   # markup
    ".css", ".scss", ".sass", ".less",         # styles
    ".json", ".yaml", ".yml", ".toml", ".ini",  # configs
    ".cfg", ".md", ".markdown", ".rst",        # docs
    ".sh", ".bash", ".env",                    # scripts/env
    ".txt"                                     # plain text
}

DEFAULT_EXCLUDE_TYPES: Set[str] = {
    "image", "video", "audio", "presentation",
    "spreadsheet", "archive", "executable"
}

# never want these—even if they sneak into ALLOWED
_unallowed = set(get_media_exts(DEFAULT_EXCLUDE_TYPES)) | {
    ".bak", ".shp", ".cpg", ".dbf", ".shx", ".geojson",
    ".pyc", ".prj", ".sbn", ".sbx"
}
DEFAULT_EXCLUDE_EXTS = {e.split('.')[-1] for e in _unallowed if e not in DEFAULT_ALLOWED_EXTS}

DEFAULT_EXCLUDE_DIRS: Set[str] = {
    "node_modules", "old","__pycache__", "backups", "backup",
    "backs", "trash", "depriciated", "old", "__init__"
}

DEFAULT_EXCLUDE_PATTERNS: Set[str] = {
    "__init__*", "*.tmp", "*.log", "*.lock", "*.zip","*~"
}
REMOTE_RE = re.compile(r"^(?P<host>[^:\s]+@[^:\s]+):(?P<path>/.*)$")
AllowedPredicate = Optional[Callable[[str], bool]]
DEFAULT_EXCLUDE_FILE_PATTERNS=DEFAULT_EXCLUDE_PATTERNS
DEFAULT_ALLOWED_PATTERNS: List[str] = ["*"]
DEFAULT_ALLOWED_DIRS: List[str] = ["*"]
DEFAULT_ALLOWED_TYPES: List[str] = ["*"]
CANONICAL_MAP = {
    "directories": ["directory", "directories", "dir","dirs","directory","directories","d","dirname", "paths", "path","roots","root"],
    "files":["file","filepath","file_path","files","filepaths","file_paths","paths", "path","f"],
    "allowed_exts": ["allow_ext", "allowed_ext", "include_ext", "include_exts", "exts_allowed"],
    "exclude_exts": ["exclude_ext", "excluded_ext", "excluded_exts", "unallowed_ext", "unallowed_exts"],
    "allowed_types": ["allow_type", "allowed_type", "include_type", "include_types", "types_allowed"],
    "exclude_types": ["exclude_type", "excluded_type", "excluded_types", "unallowed_type", "unallowed_types"],
    "allowed_dirs": ["allow_dir", "allowed_dir", "include_dir", "include_dirs", "dirs_allowed"],
    "exclude_dirs": ["exclude_dir", "excluded_dir", "excluded_dirs", "unallowed_dir", "unallowed_dirs"],
    "allowed_patterns": ["allow_pattern", "allowed_pattern", "include_pattern", "include_patterns", "patterns_allowed"],
    "exclude_patterns": ["exclude_pattern", "excluded_pattern", "excluded_patterns", "unallowed_pattern", "unallowed_patterns"],
    "add":["add"],
    "cfg":["cfg"],
    "recursive":["recursive"],
    "strings":["strings"],
    "total_strings":["total_strings"],
    "parse_lines":["parse_lines"],
    "spec_line":["spec_line"],
    "get_lines":["get_lines"]
}
DEFAULT_ALLOWED_EXCLUDE_MAP={
    "allowed_exts": {"default":DEFAULT_ALLOWED_EXTS,"type":type(DEFAULT_ALLOWED_EXTS),"canonical":CANONICAL_MAP.get("allowed_exts")},
    "exclude_exts": {"default":DEFAULT_EXCLUDE_EXTS,"type":type(DEFAULT_EXCLUDE_EXTS),"canonical":CANONICAL_MAP.get("exclude_exts")},
    "allowed_types": {"default":DEFAULT_ALLOWED_TYPES,"type":type(DEFAULT_ALLOWED_TYPES),"canonical":CANONICAL_MAP.get("allowed_types")},
    "exclude_types": {"default":DEFAULT_EXCLUDE_TYPES,"type":type(DEFAULT_EXCLUDE_TYPES),"canonical":CANONICAL_MAP.get("exclude_types")},
    "allowed_dirs": {"default":DEFAULT_ALLOWED_DIRS,"type":type(DEFAULT_ALLOWED_DIRS),"canonical":CANONICAL_MAP.get("allowed_dirs")},
    "exclude_dirs": {"default":DEFAULT_EXCLUDE_DIRS,"type":type(DEFAULT_EXCLUDE_DIRS),"canonical":CANONICAL_MAP.get("exclude_dirs")},
    "allowed_patterns": {"default":DEFAULT_ALLOWED_PATTERNS,"type":type(DEFAULT_ALLOWED_PATTERNS),"canonical":CANONICAL_MAP.get("allowed_patterns")},
    "exclude_patterns": {"default":DEFAULT_EXCLUDE_PATTERNS,"type":type(DEFAULT_EXCLUDE_PATTERNS),"canonical":CANONICAL_MAP.get("exclude_patterns")},
}
DEFAULT_CANONICAL_MAP={
    "directories":{"default":[],"type":list,"canonical":CANONICAL_MAP.get("directories")},
    "files":{"default":[],"type":list,"canonical":CANONICAL_MAP.get("files")},
    **DEFAULT_ALLOWED_EXCLUDE_MAP,
    "allowed":{"default":None,"type":bool,"canonical":CANONICAL_MAP.get("allowed")},
    "add":{"default":False,"type":bool,"canonical":CANONICAL_MAP.get("add")},
    "recursive":{"default":True,"type":bool,"canonical":CANONICAL_MAP.get("recursive")},
    "strings":{"default":None,"type":list,"canonical":CANONICAL_MAP.get("strings")},
    "total_strings":{"default":False,"type":bool,"canonical":CANONICAL_MAP.get("total_strings")},
    "parse_lines":{"default":False,"type":bool,"canonical":CANONICAL_MAP.get("parse_lines")},
    "spec_line":{"default":False,"type":bool,"canonical":CANONICAL_MAP.get("spec_line")},
    "get_lines":{"default":False,"type":bool,"canonical":CANONICAL_MAP.get("get_lines")},
}


