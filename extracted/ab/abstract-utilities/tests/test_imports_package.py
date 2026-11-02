import ast
import builtins
import importlib
from pathlib import Path

import abstract_essentials
imports = importlib.import_module("abstract_utilities.imports")
from abstract_utilities.imports import functions


def test_imports_package_exports_shared_names():
    assert imports.make_list is abstract_essentials.make_list
    assert importlib.import_module("abstract_utilities").imports is imports
    assert not hasattr(imports, "imports")
    assert callable(imports.load_dotenv)
    assert callable(imports.jsonify)
    assert callable(imports.secure_filename)


def test_fallback_helpers_load_when_optional_packages_are_missing(monkeypatch, tmp_path):
    original_import = builtins.__import__

    def without_optional_packages(name, *args, **kwargs):
        if name in {"dotenv", "werkzeug.utils", "flask"}:
            raise ImportError(name)
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", without_optional_packages)
    env_file = tmp_path / ".env"
    env_file.write_text("IMPORTS_PACKAGE_TEST=works\n")
    assert functions.load_dotenv(env_file)
    assert imports.os.environ["IMPORTS_PACKAGE_TEST"] == "works"
    monkeypatch.delenv("IMPORTS_PACKAGE_TEST")
    assert functions.secure_filename("../my file.txt") == "my_file.txt"
    assert functions.jsonify(value=1) == '{"value":1}\n'
    assert functions.jsonify(value=2) == '{"value":2}\n'


def test_list_helpers_share_essentials_implementations():
    names = (
        "combineList", "compare_lists", "ensure_nested_list",
        "filter_json_list_values", "find_original_case", "get_actual_number",
        "get_highest_value_obj", "get_single_from_list", "get_sort",
        "get_symetric_difference", "list_set", "make_list", "make_list_add",
        "make_list_it", "recursive_json_list", "remove_from_list",
        "safe_list_return",
    )
    for name in names:
        assert getattr(imports, name) is getattr(abstract_essentials, name)


def test_public_root_exports_resolve():
    utilities = importlib.import_module("abstract_utilities")
    assert all(hasattr(utilities, name) for name in utilities.__all__)
    assert all(hasattr(abstract_essentials, name) for name in abstract_essentials.__all__)
    assert callable(utilities.read_xlsx)
    assert callable(utilities.get_current_year)
    assert callable(abstract_essentials.get_safe_kwargs)
    assert utilities.make_list is abstract_essentials.make_list


def test_essentials_imports_live_in_imports_layer_and_replace_local_copies():
    """Every name abstract_utilities takes from abstract_essentials is imported
    inside a subpackage's ``imports/`` layer (never mid-module), and no module
    still defines its own copy of a name it imports from the core."""
    root = Path(importlib.import_module("abstract_utilities").__file__).parent
    misplaced, shadowed = [], []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text())
        defined = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}
        for node in tree.body:
            if not (isinstance(node, ast.ImportFrom) and node.module and node.module.split(".")[0] == "abstract_essentials"):
                continue
            rel = path.relative_to(root)
            if rel.parent.name != "imports":
                misplaced.append(f"{rel}:{node.lineno}")
            for alias in node.names:
                if (alias.asname or alias.name) in defined:
                    shadowed.append(f"{rel}:{alias.name}")
    assert not misplaced, f"abstract_essentials imported outside an imports/ layer: {misplaced}"
    assert not shadowed, f"module both imports and redefines: {shadowed}"
