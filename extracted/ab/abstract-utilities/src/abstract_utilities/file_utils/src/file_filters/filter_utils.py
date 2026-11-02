from ...imports import (
    CANONICAL_MAP,
    combine_params,
    get_safe_kwargs,
    create_canonical_map,
    get_safe_canonical_kwargs,
    get_dir_filter_kwargs,
)
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
