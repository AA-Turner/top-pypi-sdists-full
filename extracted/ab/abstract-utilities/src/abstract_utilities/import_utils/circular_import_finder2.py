from abstract_utilities import *
import os
from collections import defaultdict

def get_path_or_init(pkg_info):
    root_dirname = pkg_info.get("root_dirname")
    pkg = pkg_info.get("pkg")
    rel_path = pkg.replace('.', '/')
    dirname = os.path.dirname(root_dirname)
    pkg_path = os.path.join(dirname, rel_path)
    pkg_py_path = f"{pkg_path}.py"
    if os.path.isfile(pkg_py_path):
        return pkg_py_path
    pkg_init_path = os.path.join(pkg_path, '__init__.py')
    if os.path.isdir(pkg_path) and os.path.isfile(pkg_init_path):
        return pkg_init_path
    # optional: silence instead of blocking input()
    print(f"⚠️ not found == {pkg_info}")
    return None


def get_dot_fro_line(line, dirname=None, file_path=None, get_info=False):
    info_js = {"nuline": line, "og_line": line, "pkg": line, "dirname": dirname,
               "file_path": file_path, "root_dirname": None, "local": False}
    if dirname and is_file(dirname):
        file_path = dirname
        dirname = os.path.dirname(dirname)
        info_js["file_path"] = file_path
        info_js["dirname"] = dirname

    from_line = line.split(FROM_TAG)[-1]
    dot_fro = ""
    for char in from_line:
        if char != '.':
            pkg = f"{dot_fro}{eatAll(from_line, '.')}"
            nuline = f"from {pkg}"
            info_js["nuline"] = nuline
            info_js["pkg"] = pkg
            break
        if dirname:
            info_js["root_dirname"] = dirname
            dirbase = os.path.basename(dirname)
            dirname = os.path.dirname(dirname)
            dot_fro = f"{dirbase}.{dot_fro}"

    if get_info:
        if dot_fro and os.path.isdir(info_js.get("root_dirname") or ""):
            info_js["local"] = True
            info_js["pkg_path"] = get_path_or_init(info_js)
        return info_js
    return line


def return_local_imps(file_path):
    local_imps = []
    dirname = os.path.dirname(file_path)
    imports_js = get_all_imports(file_path)
    for pkg, imps in imports_js.items():
        if pkg not in ['context', 'nulines']:
            full_imp_info = get_dot_fro_line(pkg, dirname, file_path=file_path, get_info=True)
            if full_imp_info.get("local"):
                local_imps.append(full_imp_info)
    return local_imps


def get_all_pkg_paths(file_path):
    pkg_paths = []
    local_imps = return_local_imps(file_path)
    for local_imp in local_imps:
        pkg_path = local_imp.get('pkg_path')
        if pkg_path:
            pkg_paths.append(pkg_path)
    return pkg_paths


# --- NEW: Build dependency graph and detect circular imports ---

def build_graph(main_directory):
    dirs, all_local_scripts = get_files_and_dirs(main_directory, allowd_exts='.py', files_only=True)
    graph = defaultdict(set)
    for file_path in all_local_scripts:
        deps = get_all_pkg_paths(file_path)
        for dep in deps:
            if dep:  # only valid files
                graph[file_path].add(dep)
    return graph


def find_cycles(graph):
    visited, stack, cycles = set(), [], []

    def dfs(node, path):
        visited.add(node)
        path.append(node)
        for dep in graph.get(node, []):
            if dep not in visited:
                dfs(dep, path.copy())
            elif dep in path:
                cycle_start = path.index(dep)
                cycles.append(path[cycle_start:] + [dep])

    for node in graph:
        if node not in visited:
            dfs(node, [])
    return cycles


if __name__ == "__main__":
    main_directory = "/home/flerb/Documents/pythonTools/modules/src/modules/abstract_utilities/src/abstract_utilities"
    graph = build_graph(main_directory)
    cycles = find_cycles(graph)

    if not cycles:
        print("✅ No circular imports found.")
    else:
        print("❌ Circular imports detected:")
        for cycle in cycles:
            print(" → ".join(cycle))
