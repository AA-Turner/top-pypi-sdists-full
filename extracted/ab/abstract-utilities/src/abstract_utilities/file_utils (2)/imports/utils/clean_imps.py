from ..imports import *
# ============================================================
# Constants
# ============================================================
import_tag = 'import '
from_tag = 'from '

# ============================================================
# Helpers
# ============================================================
def get_caller_path(i=None):
    i = i or 1
    frame = inspect.stack()[i]
    return os.path.abspath(frame.filename)

def make_list(obj: any) -> list:
    if isinstance(obj, str) and ',' in obj:
        obj = obj.split(',')
    if isinstance(obj, (set, tuple)):
        return list(obj)
    if isinstance(obj, list):
        return obj
    return [obj]

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
