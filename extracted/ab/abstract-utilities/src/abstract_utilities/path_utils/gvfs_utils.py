from .imports import (
    imports,
    os,
    sys,
    get_args,
    Path,
    load_dotenv,
    jsonify,
    secure_filename,
    eatAll,
    make_list,
    get_media_exts,
    is_media_type,
    MIME_TYPES,
    safe_join,
    get_slash,
    get_caller_path,
    get_caller_dir,
    get_initial_caller,
    get_initial_caller_dir,
    is_file,
    is_dir,
    is_exists,
    split_text,
    get_ext,
    get_current_path,
    get_home_folder,
    simple_path_join,
    path_join,
    update_global_variable,
    trunc,
    get_shortest_path,
    get_common_root,
    get_dirs,
    get_directory,
    if_not_last_child_join,
    createFolds,
    list_directory_contents,
    is_string_in_dir,
    raw_create_dirs,
    mkdirs,
    makedirs,
    make_dirs,
    makeAllDirs,
    get_file_name,
    get_abs_name_of_this,
    sanitize_filename,
    get_base_name,
    get_os_info,
    mkGb,
    mkGbTrunk,
    mkGbTrunFroPathTot,
)
def find_gvfs_sftp(host: str, user: str) -> Path | None:
    gvfs_root = Path("/run/user") / str(os.getuid()) / "gvfs"
    if not gvfs_root.exists():
        return None

    for p in gvfs_root.iterdir():
        if p.name.startswith(f"sftp:host={host},user={user}"):
            return p

    return None
def resolve_solcatcher_root() -> Path:
    gvfs = find_gvfs_sftp("192.168.0.100", "solcatcher")

    if not gvfs:
        raise RuntimeError(
            "GVFS SFTP mount not available. "
            "Open Nautilus → click the server first."
        )

    root = gvfs / "mnt/24T/ABSTRACT_ENDEAVORS"
    if not root.exists():
        raise RuntimeError("Solcatcher root missing inside GVFS mount")

    return root
def ensure_solcatcher_importable():
    root = resolve_solcatcher_root()
    src = root / "scripts/RABBIT/aggregator/src"

    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
