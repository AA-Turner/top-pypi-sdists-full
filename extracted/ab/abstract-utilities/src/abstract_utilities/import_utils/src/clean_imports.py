from ..imports import *
from .pkg_utils import *
from ...safe_utils import *
def is_local_import(line):
    print(line)
    imports_from_import_pkg = clean_imports(line)
    input(imports_from_import_pkg)
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

def get_all_imports(text=None,file_path=None,import_pkg_js=None):
    text,file_path = get_text_or_read(text=text,file_path=file_path)
    lines = text.split('\n')
    cleaned_import_list=[]
    nu_lines = []
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
            
            imports = values.get('imports')
            for i,imp in enumerate(imports):
                if '#' in imp:
                    imp_spl = imp.split('#')
                    comments.append(imp_spl[-1])
                    imports[i] = clean_line(imp_spl[0])
            imports = list(set(imports))   
            if '*' in imports:
                imports="*"
            else:
                imports=','.join(imports)
                if comments:
                    comments=','.join(comments)
                    imports+=f" #{comments}"
            import_pkg_js[pkg]["imports"]=imports
            if fill_nulines:
                line = values.get('line')
                if len(nu_lines) >= line:
                    nu_lines[line] += imports
    return import_pkg_js
def clean_all_imports(text=None,file_path=None,import_pkg_js=None,fill_nulines=False):
    import_pkg_js = get_clean_imports(text=text,file_path=file_path,import_pkg_js=import_pkg_js,fill_nulines=import_pkg_js)
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
def get_clean_imports_from_files(files):
    import_pkg_js={}
    for file in files:
        import_pkg_js = get_all_imports(file,import_pkg_js=import_pkg_js)
    return get_clean_import_string(import_pkg_js)
def get_dot_fro_line(line,dirname):
    from_line = line.split(FROM_TAG)[-1]
    dot_fro = ""
    for char in from_line:
        if  char != '.':
            line = f"from {dot_fro}{eatAll(from_line,'.')}"
            break
        dirname = os.path.dirname(dirname)
        dirbase = os.path.basename(dirname)
        dot_fro = f"{dirbase}.{dot_fro}"
    return line
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
def convert_to_sysroot_relative(import_pkg, file_path, sysroot):
    """
    Convert an absolute package import into a dotted relative import based on
    the file's depth inside sysroot.
    """

    if not sysroot:
        return import_pkg  # no conversion

    file_path = os.path.abspath(file_path)
    sysroot = os.path.abspath(sysroot)

    # Ignore imports outside sysroot
    file_dir = os.path.dirname(file_path)
    if not file_dir.startswith(sysroot):
        return import_pkg

    # Compute how many directories deep the file is
    rel = os.path.relpath(file_dir, sysroot)
    depth = 0 if rel == "." else len(rel.split(os.sep))

    # Depth N means N dots (i.e. N relative levels)
    dots = "." * depth

    return f"{dots}{import_pkg}"

import os

def rewrite_import_with_sysroot(line, file_path, sysroot):
    """
    Rewrite imports like:
        from imports.constants import *
    into:
        from <relative_path>.imports.constants import *
    Where <relative_path> is computed relative to sysroot.
    """

    line = line.rstrip()
    if not line.startswith("from "):
        return line

    # Split import structure
    try:
        after_from = line[len("from "):]
        pkg, after_import = after_from.split(" import ", 1)
    except ValueError:
        return line  # Not a normal from X import Y

    # Absolute paths
    file_dir = os.path.dirname(os.path.abspath(file_path))
    sysroot = os.path.abspath(sysroot)

    # Compute relative path
    relpath = os.path.relpath(file_dir, sysroot)

    # Turn filesystem path into dotted python path
    if relpath == ".":
        dotted = ""
    else:
        dotted = ".".join(part for part in relpath.split(os.sep) if part)

    # Import path you want to append the old import to
    new_pkg = f"{dotted}.{pkg}".lstrip('.')

    # Build final rewritten import
    return f"from {new_pkg} import {after_import}"

def trace_all_imports(file_path, sysroot=None):
    import_pkg_js = {}
    files = collect_filepaths(file_path, allowed_exts='.py', add=True)

    for file in files:
        text = get_all_real_imps(file_path=file)
        lines = text.split("\n")

        if sysroot:
            new_lines = []
            for line in lines:
                new_lines.append(rewrite_import_with_sysroot(line, file, sysroot))
            text = "\n".join(new_lines)

        import_pkg_js = get_all_imports(text=text, file_path=file, import_pkg_js=import_pkg_js)

    return get_clean_import_string(import_pkg_js)
