import ast
import importlib
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import List, Set

from chalk.utils.log_with_context import get_logger
from chalk.utils.paths import get_directory_root

_logger = get_logger(__name__)


def py_path_to_module(path: Path, repo_root: Path) -> str:
    try:
        p = path.relative_to(repo_root)
    except ValueError:
        p = path
    ans = str(p)[: -len(".py")].replace(os.path.join(".", ""), "").replace(os.path.sep, ".")
    if ans.endswith(".__init__"):
        # Do not import __init__.py directly. Instead, import the module
        ans = ans[: -len(".__init__")]
    return ans


def import_only_type_checking_imports(file_path: str) -> List[ModuleType]:
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    # Get the directory of the file
    file_dir = os.path.dirname(os.path.abspath(file_path))
    imported_modules = []

    # Add the file's directory to sys.path temporarily
    sys.path.insert(0, file_dir)
    aliases = find_type_checking_aliases(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.If) and isinstance(node.test, ast.Name) and node.test.id in aliases:
            for stmt in node.body:
                if isinstance(stmt, ast.ImportFrom):
                    module = stmt.module if stmt.module else ""
                    level = stmt.level  # This is the number of dots in a relative import

                    if level > 0:
                        # This is a relative import
                        module_path = os.path.dirname(file_path)
                        for _ in range(level - 1):
                            module_path = os.path.dirname(module_path)
                        directory_root = get_directory_root() or Path(os.getcwd())
                        module_prefix = py_path_to_module(Path(module_path), directory_root)
                        module_name = f"{module_prefix}.{module}"
                        if module_name not in sys.modules:
                            module_path = f"{module_prefix}.{module}"
                            try:
                                imported_module = importlib.import_module(module_path)
                                imported_modules.append(imported_module)
                            except Exception as e:
                                _logger.error(
                                    f"Failed to import module {module_path} for {stmt} in {file_path}."
                                    + " Ensure all imports are rooted in the base directory. ",
                                    exc_info=e,
                                )
                    else:
                        # This is an absolute import
                        if module not in sys.modules:
                            module_path = str(module)
                            try:
                                imported_module = importlib.import_module(module_path)
                                imported_modules.append(imported_module)
                            except Exception as e:
                                _logger.error(
                                    f"Failed to import module {module_path} for {str(stmt)} in {file_path}."
                                    + " Ensure all imports are rooted in the base directory. ",
                                    exc_info=e,
                                )

    # Remove the file's directory from sys.path
    sys.path.pop(0)
    return imported_modules


def find_type_checking_aliases(tree: ast.AST) -> Set[str]:
    # Start with the default alias set
    aliases = {"TYPE_CHECKING"}

    # Walk through the tree to find TYPE_CHECKING alias assignments or imports
    for node in ast.walk(tree):
        # Handle assignment aliases
        if isinstance(node, ast.Assign):
            if (
                isinstance(node.value, ast.Attribute)
                and isinstance(node.value.value, ast.Name)
                and node.value.value.id == "typing"
                and node.value.attr == "TYPE_CHECKING"
            ):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        aliases.add(target.id)

        # Handle import aliases
        elif isinstance(node, ast.ImportFrom):
            if node.module == "typing":
                for alias in node.names:
                    if alias.name == "TYPE_CHECKING":
                        # Add the alias (if any) to the set
                        aliases.add(alias.asname or alias.name)

    return aliases
