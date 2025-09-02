import os
import glob
from typing import *
from collections import defaultdict
from ..file_filtering.file_filters import get_files_and_dirs, define_defaults
#!/usr/bin/env python3
from pathlib import PurePosixPath
def normalize_paths(paths: Optional[Union[bool, str]] = True) -> str:
    """
    Normalize the paths parameter for glob pattern.
    
    - If True, returns '**' for recursive search.
    - If False or None, returns '_' (non-recursive placeholder).
    - If str, returns the provided string.
    
    Args:
        paths: The paths specification.
    
    Returns:
        Normalized paths string.
    """
    if paths is True:
        return '**'
    elif paths in (False, None):
        return '_'
    elif isinstance(paths, str):
        return paths
    raise ValueError(f"Invalid paths value: {paths}")

def normalize_extensions(exts: Optional[Union[bool, str, List[str]]] = True) -> str:
    """
    Normalize the extensions parameter for glob pattern.
    
    - If True, returns '*' for all files.
    - If False or None, returns '_' (no extension filter).
    - If str starting with '.', returns '*{exts}'.
    - If str without '.', assumes it's the extension and adds '.'.
    - If list of str, returns '*.' + '{ext1,ext2,...}' for multiple extensions.
    
    Args:
        exts: The extensions specification.
    
    Returns:
        Normalized extensions string.
    """
    if exts is True:
        return '*'
    elif exts in (False, None):
        return '_'
    elif isinstance(exts, str):
        if exts.startswith('.'):
            return f"*{exts}"
        else:
            return f"*.{exts}"
    elif isinstance(exts, list):
        if not exts:
            return '*'
        normalized = [e.lstrip('.') for e in exts]
        return "*." + "{" + ",".join(normalized) + "}"
    raise ValueError(f"Invalid exts value: {exts}")

def build_glob_pattern(
    directory: str,
    paths: Optional[Union[bool, str]] = True,
    exts: Optional[Union[bool, str, List[str]]] = True
) -> str:
    """
    Build the full glob search pattern by joining directory, paths, and extensions.
    
    Args:
        directory: The base directory to search in.
        paths: The paths specification (see normalize_paths).
        exts: The extensions specification (see normalize_extensions).
    
    Returns:
        The complete glob pattern string.
    """
    norm_paths = normalize_paths(paths)
    norm_exts = normalize_extensions(exts)
    return os.path.join(directory, norm_paths, norm_exts)

def findGlobFiles(
    directory: str,
    paths: Optional[Union[bool, str]] = True,
    exts: Optional[Union[bool, str, List[str]]] = True,
    recursive: bool = True
) -> List[str]:
    """
    Find files in the directory using glob based on the provided patterns.
    
    This is the main entry point for file searching. It builds the glob pattern
    and performs the search.
    
    Args:
        directory: The base directory to search in.
        paths: The paths specification (see normalize_paths).
        exts: The extensions specification (see normalize_extensions).
        recursive: Whether to search recursively (affects glob behavior).
    
    Returns:
        List of matching file paths.
    """
    search_pattern = build_glob_pattern(directory, paths, exts)
    return glob.glob(search_pattern, recursive=recursive)
def get_e_normalized(f,exts):
    norm_exts = normalize_extensions(exts)
    if norm_exts == '_':
        return True
    norm_exts_spl = norm_exts.lstrip('*').split(',')
    lstrip_exts = [norm_exts.lstrip('*.')]
    brak_in_exts = '{' in norm_exts
    def get_strip(f,e,norm_exts_spl,lstrip_exts,brak_in_exts):
        if brak_in_exts:
            f.endswith(e.lstrip('*.'))
        return lstrip_exts
    if any(get_strip(f,e,norm_exts_spl,lstrip_exts,brak_in_exts) for e in norm_exts_spl):
         return True
    return False

def build_directory_tree(
    dirs: List[str],
    files: List[str],
    directory: str,
    recursive: bool = True,
    include_files: bool = True,
    prefix: str = ""
) -> str:
    """
    Build a text-based tree map from pre-filtered lists of directories and files.

    Args:
        dirs: List of full paths to allowed directories.
        files: List of full paths to allowed files.
        directory: The base directory (root) for relative paths.
        recursive: Whether to build a recursive tree (True) or flat immediate contents (False).
        include_files: Whether to include files in the tree.
        prefix: Internal prefix for indentation in recursive calls.

    Returns:
        A string representation of the directory tree.
    """
    tree_str = []
    directory = os.path.abspath(directory)
    base_name = os.path.basename(directory)
    tree_str.append(f"{prefix}{base_name}/")

    # Normalize to relative paths
    rel_dirs = [os.path.relpath(d, directory) for d in dirs if d != directory]
    rel_files = [(os.path.relpath(os.path.dirname(f), directory), os.path.basename(f)) for f in files]
    str_tree = None
    if not recursive:
        # Non-recursive: only immediate subdirs and files under root
        immediate_dirs = sorted([os.path.basename(rd) + '/' for rd in rel_dirs if os.path.dirname(rd) == '.'])
        immediate_files = sorted([fname for rel_dir, fname in rel_files if rel_dir == '.']) if include_files else []

        contents = immediate_dirs + immediate_files
        for i, item in enumerate(contents):
            is_last = (i == len(contents) - 1)
            connector = '└── ' if is_last else '├── '
            tree_str.append(f"{prefix}{connector}{item.rstrip('/')}" if not item.endswith('/') else f"{prefix}{connector}{item}")
    else:
        # Recursive: build dir_structure mapping
        dir_structure = defaultdict(list)

        # Add subdirs to their parents
        for rel in rel_dirs:
            parent = os.path.dirname(rel)
            child = os.path.basename(rel) + '/'
            if child not in dir_structure[parent]:
                dir_structure[parent].append(child)
        
        # Add files to their dirs
        if include_files:
            for rel_dir, fname in rel_files:
                if fname not in dir_structure[rel_dir]:
                    dir_structure[rel_dir].append(fname)

        # Sort all contents
        for key in dir_structure:
            dir_structure[key] = sorted(dir_structure[key])
        
        # Recursive builder

        Tree = Dict[str, Union[dict, None]]


        def build_tree_from_map(dirmap: Dict[str, List[str]]) -> Tree:
            root: Tree = {}

            def ensure_dir(node: Tree, path: str) -> Tree:
                """Ensure that path exists as a directory under node; create/promote as needed."""
                if not path or path in (".",):
                    return node
                cur = node
                for part in PurePosixPath(path.strip("/")).parts:
                    child = cur.get(part)
                    if child is None:          # was a file -> promote to dir
                        cur[part] = {}
                        child = cur[part]
                    elif child is None or not isinstance(child, dict):
                        cur[part] = {}
                        child = cur[part]
                    else:
                        # already a dir
                        pass
                    cur = child
                return cur

            for parent, entries in dirmap.items():
                parent_dir = ensure_dir(root, parent)
                for entry in entries:
                    is_dir = entry.endswith("/")
                    name = entry.rstrip("/")
                    existing = parent_dir.get(name)
                    if is_dir:
                        # directory: create or promote
                        if existing is None or not isinstance(existing, dict):
                            parent_dir[name] = {}
                    else:
                        # file: only set if not already a dir
                        if not isinstance(existing, dict):
                            parent_dir[name] = None
                        # if it’s already a dir, keep it as dir (promotion wins)
            return root

        def render_tree(tree: Tree, prefix: str = "") -> List[str]:
            lines: List[str] = []
            for i, name in enumerate(sorted(tree.keys())):
                child = tree[name]
                is_last = (i == len(tree) - 1)
                connector = "└── " if is_last else "├── "
                display = f"{name}/" if isinstance(child, dict) else name
                lines.append(f"{prefix}{connector}{display}")
                if isinstance(child, dict) and child:
                    lines.extend(render_tree(child, prefix + ("    " if is_last else "│   ")))
            return lines

        tree = build_tree_from_map(dir_structure)
        rendered_tree = render_tree(tree)
        str_tree = '\n'.join(rendered_tree)
    return str_tree

def get_directory_map(
    directory: str,
    cfg:Optional[List[str]] = None,
    allowed_exts: Optional[Set[str]] = False,
    unallowed_exts: Optional[Set[str]] = False,
    exclude_types: Optional[Set[str]] = False,
    exclude_dirs: Optional[List[str]] = False,
    exclude_patterns: Optional[List[str]] = False,
    add = False,
    recursive: bool = True,
    include_files: bool = True,
    prefix: str = "",
    **kwargs
) -> str:
    """
    Public entry point to get a copyable directory map string.
    
    This wraps build_directory_trees to provide a simple API for generating
    and returning the tree string, which can be printed or copied to clipboard.
    
    Example usage:
    map_str = get_directory_maps('/path/to/dir')
    print(map_str)  # Or copy to clipboard via pyperclip or similar
    
    Args:
        directory: The base directory to map.
        allowed_exts: Allowed file extensions (e.g., {'.py', '.txt'}).
        unallowed_exts: Unallowed file extensions to exclude.
        exclude_types: Types to exclude (e.g., {'image', 'video'}).
        exclude_dirs: Directory names/patterns to exclude.
        exclude_patterns: Filename patterns to exclude.
        add: Whether to add to defaults (True) or override (False).
        recursive: Whether to map recursively.
        include_files: Whether to include files in the map.
        prefix: Starting prefix for the tree string.
    
    Returns:
        The directory tree as a string.
    """
    cfg = cfg or define_defaults(
        allowed_exts=allowed_exts,
        unallowed_exts=unallowed_exts,
        exclude_types=exclude_types,
        exclude_dirs=exclude_dirs,
        exclude_patterns=exclude_patterns,
        add=add
        )
    dirs,files = get_files_and_dirs(
        directory=directory,
        cfg=cfg,
        recursive=recursive,
        include_files=include_files
        )
    return build_directory_tree(dirs=dirs, files=files, directory=directory, recursive=recursive, include_files=include_files, prefix=prefix)
