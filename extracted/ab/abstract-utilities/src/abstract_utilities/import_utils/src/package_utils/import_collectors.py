from ..imports import *
from .import_functions import *

def ensure_import_pkg_js(import_pkg_js=None, file_path=None):
    import_pkg_js = import_pkg_js or {"context": {}}
    if "context" not in import_pkg_js:
        import_pkg_js["context"] = {}
    for key in ["nulines", "file_path", "all_data"]:
        import_pkg_js["context"].setdefault(key, [] if key != "file_path" else None)

    if file_path and file_path != import_pkg_js["context"].get("file_path"):
        found = False
        nu_data = {
            "file_path": import_pkg_js["context"]["file_path"],
            "nulines": import_pkg_js["context"]["nulines"]
        }
        for i, data in enumerate(import_pkg_js["context"]["all_data"]):
            if data.get("file_path") == import_pkg_js["context"]["file_path"]:
                import_pkg_js["context"]["all_data"][i] = nu_data
                found = True
                break
        if not found:
            import_pkg_js["context"]["all_data"].append(nu_data)
        import_pkg_js["context"]["nulines"] = []
        import_pkg_js["context"]["file_path"] = file_path
    return import_pkg_js

def add_imports_to_import_pkg_js(import_pkg, imports, import_pkg_js=None):
    import_pkg_js = ensure_import_pkg_js(import_pkg_js)
    imports = clean_imports(imports)
    if import_pkg not in import_pkg_js:
        i = len(import_pkg_js["context"]["nulines"])
        file_path = import_pkg_js["context"]["file_path"]
        file_parts = get_file_parts(file_path)
        dirname = file_parts["dirname"]
        import_pkg_js[import_pkg] = {"imports": imports, "line": i}
        import_pkg_js["context"]["nulines"].append(f"from {import_pkg} import ")
    else:
        import_pkg_js[import_pkg]["imports"] += imports
    return import_pkg_js

def update_import_pkg_js(line, import_pkg_js=None):
    import_pkg_js = ensure_import_pkg_js(import_pkg_js)
    if is_line_group_import(line):
        import_pkg = get_import_pkg(line)
        imports = get_imports_from_import_pkg(line)
        import_pkg_js = add_imports_to_import_pkg_js(import_pkg, imports, import_pkg_js=import_pkg_js)
    else:
        if import_pkg_js["context"]["nulines"] and line == "" and is_line_import(import_pkg_js["context"]["nulines"][-1]):
            pass
        else:
            import_pkg_js["context"]["nulines"].append(line)
    return import_pkg_js
