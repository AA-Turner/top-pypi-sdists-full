from .predicate_utils import *
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
