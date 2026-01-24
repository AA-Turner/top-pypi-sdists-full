from abstract_utilities import *
from collections import defaultdict
def clean_line(line):
    return eatAll(line,[' ','','\t','\n'])
def is_from_line_group(line):
    if line and line.startswith(FROM_TAG) and IMPORT_TAG in line and '(' in line:
        import_spl = line.split(IMPORT_TAG)[-1]
        import_spl_clean = clean_line(line)
        if not import_spl_clean.endswith(')'):
            return True
    return False
def clean_imports(text=None,file_path=None,import_pkg_js=None,fill_nulines=False):
    if text and os.path.isfile(text):
        file_path = text
        input(file_path)
        text = read_from_file(file_path)    
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
def get_all_imports(text=None,file_path=None,import_pkg_js=None):
    if text and os.path.isfile(text):
        
        try:
            text = read_from_file(text)    
        except:
            pass
        file_path = text
    text = get_text_or_read(text=text,file_path=file_path)
    lines = text.split('\n')
    cleaned_import_list=[]
    nu_lines = []
    is_from_group = False
    import_pkg_js = ensure_import_pkg_js(import_pkg_js,file_path=file_path)
    for line in lines:
        if line.startswith(IMPORT_TAG) and ' from ' not in line:
            cleaned_import_list = get_cleaned_import_list(line)
            import_pkg_js = add_imports_to_import_pkg_js("import",cleaned_import_list,import_pkg_js=import_pkg_js)
        else:
            if is_from_group:
                import_pkg=is_from_group
                line = clean_line(line)
                if line.endswith(')'):
                   is_from_group=False
                   line=line[:-1]
                imports_from_import_pkg = clean_imports(line)
                import_pkg_js = add_imports_to_import_pkg_js(import_pkg,imports_from_import_pkg,import_pkg_js=import_pkg_js)
                
            else:
                import_pkg_js=update_import_pkg_js(line,import_pkg_js=import_pkg_js)
            if is_from_line_group(line) and is_from_group == False:
                is_from_group=get_import_pkg(line)
    return import_pkg_js
def get_path_or_init(pkg_info):
    root_dirname = pkg_info.get("root_dirname")
    pkg = pkg_info.get("pkg")
    rel_path = pkg.replace('.','/')
    dirname = os.path.dirname(root_dirname)
    pkg_path = os.path.join(dirname,rel_path)
    pkg_py_path = f"{pkg_path}.py"
    if os.path.isfile(pkg_py_path):
        return pkg_py_path
    pkg_init_path = os.path.join(pkg_path,'__init__.py')
    if os.path.isdir(pkg_path):
        if os.path.isfile(pkg_init_path):
            return pkg_init_path
    #input(f"nnot found == {pkg_info}")
def get_dot_fro_line(line,dirname=None,file_path=None,get_info=False):
    info_js = {"nuline":line,"og_line":line,"pkg":line,"dirname":dirname,"file_path":file_path,"root_dirname":None,"local":False}
    if dirname and is_file(dirname):
        file_path=dirname
        dirname = os.path.dirname(dirname)
        info_js["file_path"]=file_path
        info_js["dirname"]=dirname
    from_line = line.split(FROM_TAG)[-1]
    dot_fro = ""
    for char in from_line:
        if  char != '.':
            pkg = f"{dot_fro}{eatAll(from_line,'.')}"
            nuline=f"from {pkg}"
            info_js["nuline"]=nuline
            info_js["pkg"]=pkg
            break
        if dirname:
            info_js["root_dirname"]=dirname
            dirbase = os.path.basename(dirname)
            dirname = os.path.dirname(dirname)
            
            dot_fro = f"{dirbase}.{dot_fro}"
    if get_info:
        if dot_fro and os.path.isdir(info_js["root_dirname"]):
            info_js["local"]=True
            info_js["pkg_path"]=get_path_or_init(info_js)
        return info_js
    return line
def get_top_level_imp(line,dirname=None):
    imp = get_dot_fro_line(line,dirname)
    return imp.split('.')[0]
def return_local_imps(file_path):
    local_imps = []
    dirname = os.path.dirname(file_path)
    imports_js = get_all_imports(file_path)
    for pkg,imps in imports_js.items():
        if pkg not in ['context','nulines']:
           full_imp_info = get_dot_fro_line(pkg,dirname,file_path=file_path,get_info=True)
           if full_imp_info.get("local") == True:
               local_imps.append(full_imp_info)
    return local_imps
def get_all_pkg_paths(file_path):
    pkg_paths = []
    local_imps = return_local_imps(file_path)
    for local_imp in local_imps:
        curr_file_path = local_imp.get('file_path')
        pkg_path = local_imp.get('pkg_path')
        if pkg_path != None:
            pkg_paths.append(pkg_path)
    return pkg_paths
def get_cir_dir(pkg_path):
    dirname = os.path.dirname(pkg_path)
    dirbase = os.path.basename(dirname)
    while True:
        if dirname == "/home/flerb/Documents/pythonTools/modules/src/modules/abstract_utilities/src/abstract_utilities":
            break
        dirbase = os.path.basename(dirname)
        dirname = os.path.dirname(dirname)
    #input(f"{dirbase} is circular")
    return dirbase 
def is_circular(pkg_path):
    pkg_paths = get_all_pkg_paths(pkg_path)
    if pkg_path in pkg_paths:
        return pkg_path
def are_circular(pkg_path,cir_dirs = None):
    cir_dirs = cir_dirs or []
    pkg_path = is_circular(pkg_path)
    if pkg_path:
        if pkg_path not in cir_dirs:
            cir_dirs.append(pkg_path)
    return cir_dirs


def build_dependency_graph(main_directory):
    """Map each file to all local imports (by resolved pkg_path)."""
    graph = defaultdict(list)
    dirs, all_local_scripts = get_files_and_dirs(
        main_directory,
        allowed_exts='.py',
        exclude_dirs=['depriciate', 'junk'],
        files_only=True
    )
    for file_path in all_local_scripts:
        deps = get_all_pkg_paths(file_path)
        for dep in deps:
            if dep and os.path.isfile(dep):
                graph[file_path].append(dep)
    return graph


def find_circular_chains(graph):
    """Detect circular imports and return their full dependency paths."""
    visited, cycles = set(), []

    def dfs(node, path):
        visited.add(node)
        path.append(node)
        for dep in graph.get(node, []):
            if dep not in path:
                dfs(dep, path.copy())
            else:
                # Found a circular import
                cycle_start = path.index(dep)
                cycle = path[cycle_start:] + [dep]
                if cycle not in cycles:
                    cycles.append(cycle)
        return

    for start in graph:
        dfs(start, [])
    return cycles


def explain_circular_imports(cycles):
    """Pretty-print circular import chains with file names and import lines."""
    for i, cycle in enumerate(cycles, 1):
        print(f"\n🔁 Circular import {i}:")
        for j in range(len(cycle) - 1):
            src, dst = cycle[j], cycle[j + 1]
            print(f"  {os.path.basename(src)}  →  {os.path.basename(dst)}")
        print(f"  ^ back to {os.path.basename(cycle[0])}")
main_directory = "/home/flerb/Documents/pythonTools/modules/src/modules/abstract_utilities/src/abstract_utilities"

graph = build_dependency_graph(main_directory)
cycles = find_circular_chains(graph)

if not cycles:
    print("✅ No circular imports found.")
else:
    print(f"❌ Found {len(cycles)} circular import(s).")
    explain_circular_imports(cycles)
