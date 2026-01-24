from ...imports import *
import re
def combine_params(*values,typ=None):
    nu_values = None
    for value in values:
        if value is not None:
            typ = typ or type(value)
            if nu_values is None:
                nu_values = typ()
            
            if typ is set:
                nu_values = nu_values | typ(value)
            if typ is list:
                nu_values += typ(value)
    return nu_values
def get_safe_kwargs(canonical_map, **kwargs):
    # Lowercase all keys for safety
    canonical_map = canonical_map or CANONICAL_MAP
    norm_kwargs = {k.lower(): v for k, v in kwargs.items() if v is not None}

    # Inverse lookup: alias → canonical key
    alias_lookup = {
        alias: canon
        for canon, aliases in canonical_map.items()
        if aliases
        for alias in aliases
    }

    # Preserve correctly named keys
    safe_kwargs = {k: v for k, v in norm_kwargs.items() if k in canonical_map}

    for k, v in norm_kwargs.items():
        if k in alias_lookup:
            canonical_key = alias_lookup[k]
            prev = safe_kwargs.get(canonical_key)
            if prev is None:
                safe_kwargs[canonical_key] = v
            else:
                # merge intelligently if both exist
                if isinstance(prev, (set, list)) and isinstance(v, (set, list)):
                    safe_kwargs[canonical_key] = list(set(prev) | set(v))
                else:
                    safe_kwargs[canonical_key] = v  # overwrite for non-iterables

    # fill defaults if missing
    for canon in canonical_map:
        safe_kwargs.setdefault(canon, None)

    return safe_kwargs

def create_canonical_map(*args,canonical_map=None):
    keys = [arg for arg in args if arg]
    if not keys:
        return CANONICAL_MAP
    canonical_map = canonical_map or CANONICAL_MAP

    return {key:canonical_map.get(key) for key in keys}
def get_safe_canonical_kwargs(*args,canonical_map=None,**kwargs):
    canonical_map = canonical_map or create_canonical_map(*args)
    
    return get_safe_kwargs(canonical_map=canonical_map,**kwargs)    
def get_dir_filter_kwargs(**kwargs):
    canonical_map = create_canonical_map("directories")
    return get_safe_kwargs(canonical_map=canonical_map,**kwargs)
def get_file_filter_kwargs(**kwargs):
    """
    Normalize arbitrary keyword arguments for file scanning configuration.
    
    Examples:
      - 'excluded_ext' or 'unallowed_exts' → 'exclude_exts'
      - 'include_dirs' or 'allow_dir' → 'allowed_dirs'
      - 'excludePattern' or 'excluded_patterns' → 'exclude_patterns'
      - 'allowed_type' or 'include_types' → 'allowed_types'
    """
    # Canonical keys and aliases
    canonical_keys =["allowed_exts","exclude_exts","allowed_types","exclude_types","allowed_dirs","exclude_dirs","allowed_patterns","exclude_patterns"]
   
    return get_safe_canonical_kwargs(*canonical_keys,**kwargs)

def normalize_listlike(value, typ=list, sep=','):
    """Normalize comma-separated or iterable values into the desired type."""
    if value in [True, None, False]:
        return value
    if isinstance(value, str):
        value = [v.strip() for v in value.split(sep) if v.strip()]
    return typ(value)

def ensure_exts(exts):
    if exts in [True, None, False]:
        return exts
    cleaned = set()
    for ext in normalize_listlike(exts, list):
        ext = ext.strip().lower()
        ext = ext.lstrip(".")      # remove ALL leading dots
        cleaned.add("." + ext)     # add exactly one
    return cleaned

def ensure_patterns(patterns):
    """Normalize pattern list and ensure they are valid globs."""
    if patterns in [True, None, False]:
        return patterns
    patterns = normalize_listlike(patterns, list)
    out = []
    for pattern in patterns:
        if not pattern:
            continue
        if '*' not in pattern and '?' not in pattern:
            # Implicitly make it a prefix match
            if pattern.startswith('.') or pattern.startswith('~'):
                pattern = f"*{pattern}"
            else:
                pattern = f"{pattern}*"
        out.append(pattern)
    return out
def ensure_directories(*args,**kwargs):
    directories = []
    for arg in args:
        arg_str = str(arg)
        
        if run_pruned_func(is_dir,arg_str,**kwargs):
            directories.append(arg_str)
            
        elif run_pruned_func(is_file,arg_str,**kwargs):
            dirname = os.path.dirname(arg_str)
            directories.append(dirname)
    if not directories:    
        safe_directories = get_dir_filter_kwargs(**kwargs)
        safe_dirs = safe_directories.get('directories')
        safe_dirs = if_none_change(safe_dirs or None,get_initial_caller_dir())
        directories+= make_list(safe_dirs)
    return list(set([r for r in directories if r]))

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
def get_allowed_predicate(allowed=None,cfg=None,**kwargs):
    if allowed != False:
        if allowed == True:
            allowed = None
        allowed = allowed or make_allowed_predicate(cfg=cfg,**kwargs)
    else:
        def allowed(*args):
            return True
        allowed = allowed
    return allowed
def get_globs(items,recursive: bool = True,allowed=None,cfg=None,**kwargs):
    glob_paths = []
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    items = [item for item in make_list(items) if item]
    for item in items:
        pattern = os.path.join(item, "**/*")  # include all files recursively\n
        nuItems = glob.glob(pattern, recursive=recursive)
        if allowed:
            nuItems = [nuItem for nuItem in nuItems if nuItem and allowed(nuItem)]
        glob_paths += nuItems
    return glob_paths
def get_allowed_files(items,allowed=True,cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    return [item for item in items if item and os.path.isfile(item) and allowed(item)]
def get_allowed_dirs(items,allowed=False,cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    return [item for item in items if item and os.path.isdir(item) and allowed(item)]

def get_filtered_files(items,allowed=None,files = [],cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    glob_paths = get_globs(items,allowed=allowed,cfg=cfg,**kwargs)
    return [glob_path for glob_path in glob_paths if glob_path and os.path.isfile(glob_path) and glob_path not in files and allowed(glob_path)]
def get_filtered_dirs(items,allowed=None,dirs = [],cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    glob_paths = get_globs(items,allowed=allowed,cfg=cfg,**kwargs)
    return [glob_path for glob_path in glob_paths if glob_path and os.path.isdir(glob_path) and glob_path not in dirs and allowed(glob_path)]

def get_all_allowed_files(items,allowed=None,cfg=None,**kwargs):
    dirs = get_all_allowed_dirs(items,allowed=allowed,cfg=cfg,**kwargs)
    files = get_allowed_files(items,allowed=allowed,cfg=cfg,**kwargs)
    nu_files = []
    for directory in dirs:
        files += get_filtered_files(directory,allowed=allowed,files=files,cfg=cfg,**kwargs)
    return files
def get_all_allowed_dirs(items,allowed=None,cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    dirs = get_allowed_dirs(items,allowed=allowed,cfg=cfg,**kwargs)
    nu_dirs=[]
    for directory in dirs:
        nu_dirs += get_filtered_dirs(directory,allowed=allowed,dirs=nu_dirs,cfg=cfg,**kwargs)
    return nu_dirs

def make_allowed_predicate(cfg: ScanConfig=None,**kwargs) -> Callable[[str], bool]:
    """
    Build a predicate that returns True if a given path is considered allowed
    under the given ScanConfig. Applies allowed_* and exclude_* logic symmetrically.
    """
    cfg=cfg or define_defaults(**kwargs)
    def allowed(path: str=None,p=None) -> bool:
        p = p or Path(path)
        name = p.name.lower()
        path_str = str(p).lower()

        # --------------------
        # A) directory filters
        # --------------------
        if cfg.exclude_dirs:
            for dpat in cfg.exclude_dirs:
                dpat_l = dpat.lower()
                if dpat_l in path_str or fnmatch.fnmatch(name, dpat_l):
                    if p.is_dir() or dpat_l in path_str:
                        return False

        if cfg.allowed_dirs and "*" not in cfg.allowed_dirs:
            # must be in at least one allowed dir
            if not any(
                fnmatch.fnmatch(path_str, f"*{dpat.lower()}*") for dpat in cfg.allowed_dirs
            ):
                return False

        # --------------------
        # B) pattern filters
        # --------------------
        if cfg.allowed_patterns and "*" not in cfg.allowed_patterns:
            if not any(fnmatch.fnmatch(name, pat.lower()) for pat in cfg.allowed_patterns):
                return False

        if cfg.exclude_patterns:
            for pat in cfg.exclude_patterns:
                if fnmatch.fnmatch(name, pat.lower()):
                    return False

        # --------------------
        # C) extension filters
        # --------------------
        if p.is_file():
            ext = p.suffix.lower()
            if cfg.allowed_exts and ext not in cfg.allowed_exts:
                return False
            if cfg.exclude_exts and ext in cfg.exclude_exts:
                return False

        # --------------------
        # D) type filters (optional)
        # --------------------
        if cfg.allowed_types and "*" not in cfg.allowed_types:
            if not any(t in path_str for t in cfg.allowed_types):
                return False
        if cfg.exclude_types:
            if any(t in path_str for t in cfg.exclude_types):
                return False

        return True

    return allowed
def _get_default_modular(value, default, add=False, typ=set):
    """Merge user and default values intelligently."""
    if value == None:
        value = add
    if value in [True]:
        return default
    if value is False:
        return value
    if add:
        return combine_params(value,default,typ=None)

    return typ(value)

# -------------------------
# Default derivation logic
# -------------------------
def _get_default_modular(value, default, add=None, typ=set):
    """Merge user and default values intelligently."""
    add = add or False
    if value == None:
        value = add
    if value in [True]:
        return default
    if value is False:
        return value
    if add:
        return combine_params(value,default,typ=None)
    return typ(value)
def make_allowed_predicate(cfg: ScanConfig = None, **kwargs) -> Callable[[str], bool]:
    """
    Build and return a function `allowed(path)` that evaluates the given ScanConfig.
    Unlike substring-based matching, this version avoids accidental matches inside
    unrelated names (e.g., 'abstract' matching 'archive').
    """

    cfg = cfg or define_defaults(**kwargs)

    def allowed(path: str) -> bool:
        p = Path(path)
        name = p.name.lower()
        path_str = str(p).lower()

        # --------------------
        # A) directory filters
        # --------------------
        # Excluded dirs: reject if any directory in the path matches exactly
        if cfg.exclude_dirs:
            parts = path_str.split("/")
            if any(d.lower() in parts for d in cfg.exclude_dirs):
                print(f"[exclude_dirs] → {path}")
                return False

        # Allowed dirs: require at least one match (unless "*")
        if cfg.allowed_dirs and cfg.allowed_dirs != ["*"]:
            parts = path_str.split("/")
            if not any(d.lower() in parts for d in cfg.allowed_dirs):
                print(f"[allowed_dirs] → {path}")
                return False

        # --------------------
        # B) pattern filters
        # --------------------
        if cfg.allowed_patterns and cfg.allowed_patterns != ["*"]:
            if not any(fnmatch.fnmatch(name, pat.lower()) for pat in cfg.allowed_patterns):
                print(f"[allowed_patterns] → {path}")
                return False

        if cfg.exclude_patterns:
            if any(fnmatch.fnmatch(name, pat.lower()) for pat in cfg.exclude_patterns):
                print(f"[exclude_patterns] → {path}")
                return False

        # --------------------
        # C) extension filters
        # --------------------
        if p.is_file():
            ext = p.suffix.lower()

            if cfg.allowed_exts and ext not in cfg.allowed_exts:
                print(f"[allowed_exts] → {path}")
                return False

            if cfg.exclude_exts and ext in cfg.exclude_exts:
                print(f"[exclude_exts] → {path}")
                return False

        # --------------------
        # D) type filters (SAFE SEMANTIC MATCHING)
        # --------------------
        if cfg.allowed_types and "*" not in cfg.allowed_types:
            if not any(t.lower() in path_str.split("/") for t in cfg.allowed_types):
                print(f"[allowed_types] → {path}")
                return False

        if cfg.exclude_types:
            if any(t.lower() in path_str.split("/") for t in cfg.exclude_types):
                print(f"[exclude_types] → {path}")
                return False

        return True

    # Preserve real name for debugging and repr
    allowed.__name__ = "allowed"
    return allowed

def filter_allowed_items(items, cfg=None, **kwargs):
    """
    Apply ScanConfig allow/exclude rules to a flat list of file or directory paths.
    No recursion. No globs. No shell calls.
    Just pure deterministic filtering.
    """
    allowed_items = []
    allowed = make_allowed_predicate(cfg=cfg, **kwargs)
    for item in items:
        if allowed(item):    
            allowed_items.append(item)

    return allowed_items

def derive_all_defaults(**kwargs):
    kwargs = get_safe_canonical_kwargs(**kwargs)
    add = kwargs.get("add",False)
    nu_defaults = {}
    for key,values in DEFAULT_CANONICAL_MAP.items():
        default = values.get("default")
        typ = values.get("type")
        key_value = kwargs.get(key)
        if key in DEFAULT_ALLOWED_EXCLUDE_MAP:

            if key.endswith('exts'):
                input_value = ensure_exts(key_value)
            if key.endswith('patterns'):
                input_value = ensure_patterns(key_value)
            else:
                input_value = normalize_listlike(key_value, typ)
            nu_defaults[key] = _get_default_modular(input_value, default, add, typ)
        else:
            value = default if key_value is None else key_value
            if typ == list:
                value = make_list(value)
            elif typ == bool:
                value = bool(value)
            nu_defaults[key] = value
   
    return nu_defaults
# -------------------------
# Default derivation logic
# -------------------------
def derive_file_defaults(**kwargs):
    kwargs = derive_all_defaults(**kwargs)
    add = kwargs.get("add",True)
    nu_defaults = {}
    for key,values in DEFAULT_ALLOWED_EXCLUDE_MAP.items():
        default = values.get("default")
        typ = values.get("type")
        key_value = kwargs.get(key)
        if key.endswith('exts'):
            input_value = ensure_exts(key_value)
        if key.endswith('patterns'):
            input_value = ensure_patterns(key_value)
        else:
            input_value = normalize_listlike(key_value, typ)
        nu_defaults[key] = _get_default_modular(input_value, default, add, typ)
    return nu_defaults

def define_defaults(**kwargs):
    defaults = derive_file_defaults(**kwargs)
    return ScanConfig(**defaults)

def get_file_filters(*args,**kwargs):
    directories = ensure_directories(*args,**kwargs)
    recursive = kwargs.get('recursive',True)
    include_files = kwargs.get('include_files',True)
    cfg = define_defaults(**kwargs)
    allowed = kwargs.get("allowed") or make_allowed_predicate(cfg)
    return directories,cfg,allowed,include_files,recursive
