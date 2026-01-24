from ..imports import *
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
                nu_values += make_list(value)
    return nu_values


   
def make_allowed_predicate(cfg: ScanConfig) -> Callable[[str], bool]:
    """
    Build a predicate that returns True if a given path is considered allowed
    under the given ScanConfig. Applies allowed_* and exclude_* logic symmetrically.
    """
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

        if cfg.allowed_dirs and cfg.allowed_dirs != ["*"]:
            # must be in at least one allowed dir
            if not any(
                fnmatch.fnmatch(path_str, f"*{dpat.lower()}*") for dpat in cfg.allowed_dirs
            ):
                return False

        # --------------------
        # B) pattern filters
        # --------------------
        if cfg.allowed_patterns and cfg.allowed_patterns != ["*"]:
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
        if cfg.allowed_types and cfg.allowed_types != {"*"}:
            if not any(t in path_str for t in cfg.allowed_types):
                return False
        if cfg.exclude_types and cfg.exclude_types != {"*"}:
            if any(t in path_str for t in cfg.exclude_types):
                return False

        return True

    return allowed
# -------------------------
# Utility functions
# -------------------------

def _normalize_listlike(value, typ=list, sep=','):
    """Normalize comma-separated or iterable values into the desired type."""
    if value in [True, None, False]:
        return value
    if isinstance(value, str):
        value = [v.strip() for v in value.split(sep) if v.strip()]
    return typ(value)

def ensure_exts(exts):
    if exts in [True, None, False]:
        return exts
    out = []
    for ext in _normalize_listlike(exts, list):
        if not ext.startswith('.'):
            ext = f".{ext}"
        out.append(ext)
    return set(out)
def ensure_directories(*args,**kwargs):
    directories = []
    for arg in args:
        arg_str = str(arg)
        if is_dir(arg_str,**kwargs):
            directories.append(arg_str)
        elif is_file(arg_str,**kwargs):
            dirname = os.path.dirname(arg_str)
            directories.append(dirname)
    safe_directories = get_dir_filter_kwargs(**kwargs)
    directories+= make_list(safe_directories.get('directories',[]))
    return list(set([r for r in directories if r]))
def ensure_patterns(patterns):
    """Normalize pattern list and ensure they are valid globs."""
    if patterns in [True, None, False]:
        return patterns
    patterns = _normalize_listlike(patterns, list)
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
def get_replace_strings(string,strings_js):
    for string_key,string_values in strings_js.items():
        string_parts = string.split('_')
        for i,string_part in enumerate(string_parts):
            if string_part in string_values:
                string_parts[i] = string_key
    return '-'.join(string_parts)
    
import re
def get_safe_kwargs(canonical_map,**kwargs):
    # Lowercase all keys for safety
    norm_kwargs = {k.lower(): v for k, v in kwargs.items() if v is not None}
    
    # Inverse lookup: alias → canonical key
    alias_lookup = {alias: canon for canon, aliases in canonical_map.items() for alias in aliases}

    safe_kwargs = {k: v for k, v in norm_kwargs.items() if k in canonical_map}  # preserve correctly named keys

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
    print(f"canonicl_map == {canonical_map}\n\nkwrgs={kwargs}\n\nsafe_kwargs=={safe_kwargs}")
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
def derive_file_defaults(**kwargs):
    kwargs = get_file_filter_kwargs(**kwargs)
    add = kwargs.get("add",False)
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
            input_value = _normalize_listlike(key_value, typ)
        nu_defaults[key] = _get_default_modular(input_value, default, add, typ)
    return nu_defaults
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
                input_value = _normalize_listlike(key_value, typ)
            nu_defaults[key] = _get_default_modular(input_value, default, add, typ)
        else:
            value = default if key_value is None else key_value
            if typ == list:
                value = make_list(value)
            elif typ == bool:
                value = bool(value)
            nu_defaults[key] = value
   
    return nu_defaults

def define_defaults(**kwargs):
    defaults = derive_file_defaults(**kwargs)
    return ScanConfig(**defaults)

# ============================================================
# Unified param definition funnel -> AllParams
# ============================================================

def define_search_params(*args, **kwargs) -> SearchParams:
    """
    Legacy-compatible constructor that upgrades to SearchParams.
    Uses ScanConfig defaults under the hood.
    """
    directories = ensure_directories(*args, **kwargs)
    cfg = kwargs.get('cfg') or define_defaults(**kwargs)

    return SearchParams(
        directories=directories,
        add=kwargs.get('add', False),
        recursive=kwargs.get('recursive', True),
        strings=_normalize_listlike(kwargs.get('strings', []), list),
        total_strings=kwargs.get('total_strings', False),
        parse_lines=kwargs.get('parse_lines', False),
        spec_line=kwargs.get('spec_line', False),
        get_lines=kwargs.get('get_lines', False),
        allowed_exts=cfg.allowed_exts,
        exclude_exts=cfg.exclude_exts,
        allowed_types=cfg.allowed_types,
        exclude_types=cfg.exclude_types,
        allowed_dirs=cfg.allowed_dirs,
        exclude_dirs=cfg.exclude_dirs,
        allowed_patterns=cfg.allowed_patterns,
        exclude_patterns=cfg.exclude_patterns,
    )


def define_all_params(*args, **kwargs) -> AllParams:
    """
    Master param definition entrypoint.
    Accepts any legacy kwargs or args and returns a fully built AllParams.
    """
    # Step 1: normalize any alias/legacy key names
    kwargs = get_safe_canonical_kwargs(**kwargs)
    
    # Step 2: get SearchParams base
    search_params = define_search_params(*args, **kwargs)

    # Step 3: create ScanConfig from SearchParams
    cfg = ScanConfig(
        allowed_exts=search_params.allowed_exts,
        exclude_exts=search_params.exclude_exts,
        allowed_types=search_params.allowed_types,
        exclude_types=search_params.exclude_types,
        allowed_dirs=search_params.allowed_dirs,
        exclude_dirs=search_params.exclude_dirs,
        allowed_patterns=search_params.allowed_patterns,
        exclude_patterns=search_params.exclude_patterns,
    )

    # Step 4: build allowed predicate + merge new flags
    directories = ensure_directories(*args, **kwargs)
    allowed = kwargs.get("allowed") or make_allowed_predicate(cfg)
    
    include_files = kwargs.get("include_files", True)
    recursive = kwargs.get("recursive", search_params.recursive)

    # Step 5: convert search_params to dict and safely update
    merged = asdict(search_params)
     
    merged.update({
        "directories":directories,
        "allowed": allowed,
        "include_files": include_files,
        "recursive": recursive,  # override existing value safely
    })
    input(merged)   
    # Step 6: instantiate AllParams
    return AllParams(**merged)
def get_file_filters(*args, **kwargs) -> AllParams:
    """
    Unified modern entrypoint:
    Returns a single AllParams dataclass, fully populated and key-accessible.
    """
    return define_all_params(*args, **kwargs)




