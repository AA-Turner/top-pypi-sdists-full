from src.abstract_utilities import *
import ast,re
import importlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
import ast
import importlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Core Helpers
# ---------------------------------------------------------------------------
def is_local_import(line):
    return clean_imports(line)

def try_is_file(file_path):
    try:
        return os.path.isfile(file_path)
    except:
        return False

def try_is_dir(file_path):
    try:
        return os.path.isdir(file_path)
    except:
        return False

def try_join(*args):
    try:
        return safe_join(*args)
    except:
        return False

def get_pkg_or_init(pkg_path):
    if pkg_path:
        if try_is_file(pkg_path):
            return pkg_path
        pkg_py_path = f"{pkg_path}.py"
        if try_is_file(pkg_py_path):
            return pkg_py_path
        pkg_init_path = try_join(pkg_path,'__init__.py')
        if try_is_dir(pkg_path):
            if os.path.isfile(pkg_init_path):
                return pkg_init_path

def get_text_and_file_and_js(text=None,file_path=None,import_pkg_js=None):
    inputs = {"text":text,"file_path":file_path,"import_pkg_js":import_pkg_js}
    for key,value in inputs.items():
        if value:
            if isinstance(value,str):
                _file_path = get_pkg_or_init(file_path)
                if _file_path:
                    file_path=_file_path
                    if key == "text" or text == None:
                        text=read_from_file(file_path)
                if isinstance(value,dict):
                    if key in ["text","file_path"]:
                        if key == "text":
                            text = None
                        if key == "file_path":
                            file_path = None
                    import_pkg_js=value
    import_pkg_js = ensure_import_pkg_js(import_pkg_js,file_path=file_path)
    return text,file_path,import_pkg_js

def get_text_or_read(text=None,file_path=None):
    file_path = get_pkg_or_init(file_path)
    if not text and file_path:
        text=read_from_file(file_path)
    if text and not file_path:
        file_path=get_pkg_or_init(text)
        if file_path:
            text = None
    return text,file_path 

def is_line_import(line):
    if line and (line.startswith(FROM_TAG) or line.startswith(IMPORT_TAG)):
        return True
    return False

def is_line_group_import(line):
    if line and (line.startswith(FROM_TAG) and IMPORT_TAG in line):
        return True
    return False

def is_from_line_group(line):
    if line and line.startswith(FROM_TAG) and IMPORT_TAG in line and '(' in line:
        import_spl = line.split(IMPORT_TAG)[-1]
        import_spl_clean = clean_line(line)
        if not import_spl_clean.endswith(')'):
            return True
    return False

# ---------------------------------------------------------------------------
# Star Import & Function Call Derivation Engine
# ---------------------------------------------------------------------------
_EXPORTS_CACHE: Dict[str, Set[str]] = {}

def get_module_star_exports(target_file_path: str, visited: Optional[Set[str]] = None) -> Set[str]:
    """Extracts public symbols or __all__ entries from a target file recursively."""
    if not target_file_path or not os.path.isfile(target_file_path):
        return set()

    if target_file_path in _EXPORTS_CACHE:
        return _EXPORTS_CACHE[target_file_path]

    visited = visited or set()
    if target_file_path in visited:
        return set()
    visited.add(target_file_path)

    try:
        with open(target_file_path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=target_file_path)
    except Exception:
        return set()

    exports = set()
    has_explicit_all = False

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "__all__":
                    if isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                exports.add(elt.value)
                        has_explicit_all = True
                        break

    if has_explicit_all:
        _EXPORTS_CACHE[target_file_path] = exports
        return exports

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not node.name.startswith("_"):
                exports.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    exports.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if not node.target.id.startswith("_"):
                exports.add(node.target.id)
        elif isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" for alias in node.names):
                sub_path = get_pkg_or_init(os.path.join(os.path.dirname(target_file_path), node.module or ""))
                if sub_path and sub_path != target_file_path:
                    exports.update(get_module_star_exports(sub_path, visited))

    _EXPORTS_CACHE[target_file_path] = exports
    return exports

def find_utilized_star_calls(file_path: str) -> Set[str]:
    """Parses a file, unpacks its star imports, and identifies which imported symbols are called as functions."""
    file_path = get_pkg_or_init(file_path)
    if not file_path or not os.path.isfile(file_path):
        return set()

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            tree = ast.parse(f.read(), filename=file_path)
    except Exception:
        return set()

    star_symbols = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and any(alias.name == "*" for alias in node.names):
            cur_dir = os.path.dirname(os.path.abspath(file_path))
            for _ in range(node.level - 1):
                cur_dir = os.path.dirname(cur_dir)
            target_base = os.path.join(cur_dir, node.module.replace(".", os.sep) if node.module else "")
            target_file = get_pkg_or_init(target_base)
            if target_file:
                star_symbols.update(get_module_star_exports(target_file))

    called_identifiers = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                called_identifiers.add(func.id)
            elif isinstance(func, ast.Attribute):
                called_identifiers.add(func.attr)

    return star_symbols.intersection(called_identifiers)

# ---------------------------------------------------------------------------
# Import Processing & Rewriting
# ---------------------------------------------------------------------------
def get_all_imports(text=None,file_path=None,import_pkg_js=None):
    text,file_path = get_text_or_read(text=text,file_path=file_path)
    lines = text.split('\n')
    is_from_group = False
    import_pkg_js = ensure_import_pkg_js(import_pkg_js,file_path=file_path)
    for line in lines:
        if line.startswith(IMPORT_TAG) and ' from ' not in line:
            cleaned_import_list = get_cleaned_import_list(line)
            import_pkg_js = add_imports_to_import_pkg_js("import",cleaned_import_list,import_pkg_js=import_pkg_js,file_path=file_path)
        else:
            if is_from_group:
                import_pkg=is_from_group
                line = clean_line(line)
                if line.endswith(')'):
                   is_from_group=False
                   line=line[:-1]
                imports_from_import_pkg = clean_imports(line)
                import_pkg_js = add_imports_to_import_pkg_js(import_pkg,imports_from_import_pkg,import_pkg_js=import_pkg_js,file_path=file_path)
            else:
                import_pkg_js=update_import_pkg_js(line,import_pkg_js=import_pkg_js,file_path=file_path)
            if is_from_line_group(line) and is_from_group == False:
                is_from_group=get_import_pkg(line)
    return import_pkg_js

def get_clean_imports(text=None,file_path=None,import_pkg_js=None,fill_nulines=False):
    text,file_path,_ = get_text_and_file_and_js(text=text,file_path=file_path,import_pkg_js=import_pkg_js)    
    if not import_pkg_js:
        import_pkg_js = get_all_imports(text=text,file_path=file_path)
    import_pkg_js = ensure_import_pkg_js(import_pkg_js,file_path=file_path)
    nu_lines = import_pkg_js["context"]["nulines"]
    for pkg,values in import_pkg_js.items():
        comments = []
        if pkg not in ["context"]: 
            imports = values.get('imports', [])
            for i,imp in enumerate(imports):
                if '#' in imp:
                    imp_spl = imp.split('#')
                    comments.append(imp_spl[-1])
                    imports[i] = clean_line(imp_spl[0])
            imports = list(set(imports))    
            if '*' in imports:
                if file_path:
                    utilized = find_utilized_star_calls(file_path)
                    if utilized:
                        imports = sorted(list(utilized))
                    else:
                        imports = "*"
                else:
                    imports = "*"
            else:
                imports=','.join(imports)
                if comments:
                    comments=','.join(comments)
                    imports+=f" #{comments}"
            import_pkg_js[pkg]["imports"]=imports
            if fill_nulines:
                line = values.get('line')
                if line is not None and len(nu_lines) >= line:
                    nu_lines[line] += str(imports)
    return import_pkg_js

def clean_all_imports(text=None,file_path=None,import_pkg_js=None,fill_nulines=False):
    import_pkg_js = get_clean_imports(text=text,file_path=file_path,import_pkg_js=import_pkg_js,fill_nulines=fill_nulines)
    import_pkg_js["context"]["nulines"]=import_pkg_js["context"]["nulines"]
    return import_pkg_js

def get_clean_import_string(import_pkg_js,fill_nulines=False,get_locals=False):
    import_pkg_js = get_clean_imports(import_pkg_js=import_pkg_js,fill_nulines=fill_nulines)
    import_ls = []
    for key,values in import_pkg_js.items():
        if key not in ['context','nulines']:
            imports = None
            imp_values= values.get('imports')
            if key == 'import':
                imports = f'import {imp_values}'
            elif get_locals or not key.startswith('.'):
                imports = f'from {key} import {imp_values}'
            if imports:
                import_ls.append(imports)
    return '\n'.join(import_ls)

def get_dot_fro_line(line: str, file_path: str) -> str:
    if not line.startswith("from ."):
        return line

    match = re.match(r"^from\s+(\.+)([\w\.]*)\s+import\s+(.*)$", line.strip())
    if not match:
        return line

    dots, remainder, after_import = match.groups()
    num_dots = len(dots)

    target_dir = os.path.dirname(os.path.abspath(file_path))
    for _ in range(num_dots - 1):
        target_dir = os.path.dirname(target_dir)

    if remainder:
        rel_subpath = os.path.join(*remainder.split("."))
        target_path = os.path.join(target_dir, rel_subpath)
    else:
        target_path = target_dir

    cursor = target_dir
    pkg_parts = []
    while os.path.isfile(os.path.join(cursor, "__init__.py")):
        pkg_parts.insert(0, os.path.basename(cursor))
        parent = os.path.dirname(cursor)
        if parent == cursor:
            break
        cursor = parent

    if remainder:
        pkg_parts.append(remainder)

    resolved_dotted = ".".join(pkg_parts)
    return f"from {resolved_dotted} import {after_import}"

def get_dot_fro_lines(lines,file_path,all_imps):
    for line in lines:
        if line.startswith(FROM_TAG):
            line = get_dot_fro_line(line,file_path)
            if line in all_imps:
                line = ""
        if line:
            all_imps.append(line)
    return all_imps

def get_all_real_imps(text=None,file_path=None,all_imps=None):
    all_imps = all_imps or []
    text,file_path = get_text_or_read(text=text,file_path=file_path)
    lines = text.split('\n')
    all_imps = get_dot_fro_lines(lines,file_path,all_imps)
    return '\n'.join(all_imps)

def save_cleaned_imports(text=None,file_path=None,write=False,import_pkg_js=None):
    text,file_path,import_pkg_js = get_text_and_file_and_js(text=text,file_path=file_path,import_pkg_js=import_pkg_js)
    import_pkg_js = clean_all_imports(text=text,file_path=file_path,import_pkg_js=import_pkg_js)
    contents = '\n'.join(import_pkg_js["context"]["nulines"])
    if file_path and write:
        write_to_file(contents=contents,file_path=file_path)
    return contents

def trace_all_imports(file_path, sysroot=None):
    import_pkg_js = {}
    files = collect_filepaths(file_path, allowed_exts='.py', add=True)

    for file in files:
        text = get_all_real_imps(file_path=file)
        import_pkg_js = get_all_imports(text=text, file_path=file, import_pkg_js=import_pkg_js)

    return get_clean_import_string(import_pkg_js)
import os
from pathlib import Path
from typing import List, Dict

def convert_sysroot_imports_to_paths(trace_output_string: str, sysroot: str) -> Dict[str, str]:
    """
    Takes the output of trace_all_imports (where each line is a sysroot import statement)
    and maps every dotted module back to its absolute physical .py or __init__.py path.
    
    Returns: {dotted_module_name: absolute_file_path}
    """
    sysroot_path = Path(sysroot).resolve()
    resolved_paths: Dict[str, str] = {}

    for line in trace_output_string.splitlines():
        line = line.strip()
        if not line.startswith("from "):
            continue

        try:
            # Extract the module path between 'from ' and ' import'
            # e.g., 'abstract_hugpy_dev.comms.model_physical'
            module_name = line.split("from ")[1].split(" import ")[0].strip()
        except IndexError:
            continue

        # Convert dotted module path to file system parts
        parts = module_name.split(".")
        
        # Check candidate locations:
        # 1. <sysroot>/path/to/module.py
        py_target = sysroot_path.joinpath(*parts).with_suffix(".py")
        if py_target.is_file():
            resolved_paths[module_name] = str(py_target.resolve())
            continue

        # 2. <sysroot>/path/to/module/__init__.py
        init_target = sysroot_path.joinpath(*parts, "__init__.py")
        if init_target.is_file():
            resolved_paths[module_name] = str(init_target.resolve())

    return resolved_paths

from pathlib import Path

def get_sysroot_from_file(file_path: str) -> str:
    """
    Takes any starting file path, climbs up past all __init__.py package directories,
    and returns the sysroot directory (the folder *above* the top-level package root).
    """
    p = Path(file_path).resolve()
    if p.is_file():
        p = p.parent

    top = p
    while (top / "__init__.py").exists():
        if top.parent == top:
            break
        top = top.parent

    # The sysroot is the directory containing the top-level package
    return str(top.parent)
file = "/run/user/1000/gvfs/sftp:host=192.168.1.100,user=solcatcher/srv/hugpy/src/abstract_hugpy_dev/src/abstract_hugpy_dev/__init__.py"
sysroot = get_sysroot_from_file(file)
all_imports = trace_all_imports(file)
all_stars = []
for line in all_imports.split('\n'):
    if line.endswith('*'):
        all_stars.append(line)
        print(line)
