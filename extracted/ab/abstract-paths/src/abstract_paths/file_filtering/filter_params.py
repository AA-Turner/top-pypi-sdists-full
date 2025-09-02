from typing import *
from abstract_utilities import make_list,get_media_exts, is_media_type,eatAll
from dataclasses import dataclass, field
@dataclass
class ScanConfig:
    allowed_exts: Set[str]
    unallowed_exts: Set[str]
    exclude_types: Set[str]
    exclude_dirs: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)
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
_unallowed = set(get_media_exts(DEFAULT_EXCLUDE_TYPES)) | {'.bak', '.shp', '.cpg', '.dbf', '.shx','.geojson',".pyc",'.shx','.geojson','.prj','.sbn','.sbx'}
DEFAULT_UNALLOWED_EXTS = {e for e in _unallowed if e not in DEFAULT_ALLOWED_EXTS}

DEFAULT_EXCLUDE_DIRS: Set[str] = {
    "node_modules", "__pycache__", "backups", "backup", "backs", "trash", "depriciated", "old", "__init__"
}

DEFAULT_EXCLUDE_PATTERNS: Set[str] = {
    "__init__*", "*.tmp", "*.log", "*.lock", "*.zip","*~"
}
def get_default_modular(obj,default=None,add=False,typ=set):
    if obj in [False,True,None]:
        if obj in [True,None]:
            obj = default
        if obj == False:
            obj =None
    elif add == True:
        if typ == set:
            obj = typ(typ(obj) | typ(default))
        elif typ == list:
            obj = make_list(obj) + make_list(default)
    return obj
def ensure_exts(exts):
    if exts in [True,None,False]:
        return exts
    if isinstance(exts,str):
        exts = exts.split(',')
    exts = make_list(exts)
    for i,ext in enumerate(exts):
        ext = eatAll(ext,' ')
        if ext and isinstance(ext,str) and not ext.startswith('.'):
            ext = f".{ext}"
        exts[i] = ext
    return set(exts)
def ensure_patterns(patterns):
    if patterns in [True,None,False]:
        return patterns
    if isinstance(patterns,str):
        patterns = patterns.split(',')
    patterns = make_list(patterns)
    for i,pattern in enumerate(patterns):
        if pattern and isinstance(pattern,str) and '*' not in pattern:
            if pattern.startswith('.') or pattern.startswith('~'):
                pattern = f"*{pattern}"
            else:
                pattern = f"{pattern}*"
        patterns[i] = pattern
    return patterns
def ensure_dirtypes(obj):
    if obj in [True,None,False]:
        return obj
    if isinstance(obj,str):
        obj = obj.split(',')
    obj = make_list(obj)
    return obj
def define_defaults(
    allowed_exts: Optional[Set[str]] = False,
    unallowed_exts: Optional[Set[str]] = False,
    exclude_types: Optional[Set[str]] = False,
    exclude_dirs: Optional[List[str]] = False,
    exclude_patterns: Optional[List[str]] = False,
    add = False
    ):
    defaults = derive_file_defaults(
            allowed_exts = allowed_exts,
            unallowed_exts = unallowed_exts,
            exclude_types = exclude_types,
            exclude_dirs = exclude_dirs,
            exclude_patterns = exclude_patterns,
            add = add
        )
    DEFAULT_CFG = ScanConfig(**defaults)
    return DEFAULT_CFG
def derive_file_defaults(
    allowed_exts: Optional[Set[str]] = False,
    unallowed_exts: Optional[Set[str]] = False,
    exclude_types: Optional[Set[str]] = False,
    exclude_dirs: Optional[List[str]] = False,
    exclude_patterns: Optional[List[str]] = False,
    add = False
    ):
    allowed_exts=ensure_exts(allowed_exts)
    unallowed_exts=ensure_exts(unallowed_exts)
    exclude_types = ensure_dirtypes(exclude_types)
    exclude_dirs = ensure_dirtypes(exclude_dirs)
    exclude_patterns = ensure_patterns(exclude_patterns)
    allowed_exts = get_default_modular(allowed_exts,default=DEFAULT_ALLOWED_EXTS,add=add,typ=set)
    unallowed_exts = get_default_modular(unallowed_exts,default=DEFAULT_UNALLOWED_EXTS,add=add,typ=set)
    exclude_types = get_default_modular(exclude_types,default=DEFAULT_EXCLUDE_TYPES,add=add,typ=set)
    exclude_dirs = get_default_modular(exclude_dirs,default=DEFAULT_EXCLUDE_DIRS,add=add,typ=list)
    exclude_patterns = get_default_modular(exclude_patterns,default=DEFAULT_EXCLUDE_PATTERNS,add=add,typ=list)
    return {
        "allowed_exts":allowed_exts,
        "unallowed_exts":unallowed_exts,
        "exclude_types":exclude_types,
        "exclude_dirs":exclude_dirs,
        "exclude_patterns":exclude_patterns
        }
