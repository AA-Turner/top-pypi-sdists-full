import ast
import importlib
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Optional, Set, Tuple, Union

from chalk.utils.cached_type_hints import cached_get_type_hints
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


def import_only_type_checking_imports(file_path: str) -> ast.Module:
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
    return tree


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


def gather_all_imports_and_local_classes(tree: ast.Module) -> Tuple[list[str], list[str], list[str]]:
    # Lists to store the different types of imports
    regular_from_imports: list[str] = []
    type_checking_imports: list[str] = []
    local_classes: list[str] = []

    # Get all TYPE_CHECKING aliases
    aliases = find_type_checking_aliases(tree)

    # Track if we're inside a TYPE_CHECKING conditional
    def is_type_checking_if(node: ast.AST) -> bool:
        if not isinstance(node, ast.If):
            return False
        # Check if the condition is any of the known TYPE_CHECKING aliases
        if isinstance(node.test, ast.Name) and node.test.id in aliases:
            return True
        return False

    def process_node(node: ast.AST, is_in_type_checking: bool = False) -> None:
        # Only process actual AST nodes, not strings or other types
        if not isinstance(node, ast.AST):  # pyright: ignore[reportUnnecessaryIsInstance]
            return

        # Handle class definitions
        if isinstance(node, ast.ClassDef):
            local_classes.append(node.name)

        # Handle import statements
        elif isinstance(node, ast.Import):
            for name in node.names:
                if is_in_type_checking:
                    type_checking_imports.append(name.name)
        elif isinstance(node, ast.ImportFrom):
            for name in node.names:
                if is_in_type_checking:
                    type_checking_imports.append(name.name)
                else:
                    regular_from_imports.append(name.name)

        # Check for TYPE_CHECKING conditionals
        elif isinstance(node, ast.If) and is_type_checking_if(node):
            # Process the body of the TYPE_CHECKING if statement
            for child in node.body:
                process_node(child, True)
            return  # Skip normal child processing, we've already handled this if's body

        # Process all child nodes
        for child_node in ast.iter_child_nodes(node):
            process_node(child_node, is_in_type_checking)

    # Process the entire AST starting from the root
    process_node(tree)

    return regular_from_imports, type_checking_imports, local_classes


def get_detailed_type_hint_errors(
    cls: Any, include_extras: bool, globalns: Optional[Dict[str, Any]]
) -> Dict[str, Exception]:
    errors = {}

    # Get all annotations (even unevaluated ones)
    annotations = getattr(cls, "__annotations__", {})

    for attr_name, annotation in annotations.items():
        # Create a mini class with just this one annotation
        try:

            class SingleAttr:
                pass

            # Add just this one annotation to the class
            SingleAttr.__annotations__ = {attr_name: annotation}

            # Try to get type hints for just this attribute
            cached_get_type_hints(SingleAttr, include_extras=include_extras, globalns=globalns)

        except Exception as e:
            errors[attr_name] = e

    return errors


def get_type_checking_imports(file_path: str) -> list[str]:
    """
    Extract all imported objects from TYPE_CHECKING blocks in a Python file.

    Args:
        file_path: Path to the Python file to analyze

    Returns:
        List of imported object names from TYPE_CHECKING blocks
    """
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    _, type_checking_imports, _ = gather_all_imports_and_local_classes(tree)
    return type_checking_imports


def check_if_subpackage(base_package: Union[ModuleType, str], submodule_name: str) -> bool:
    if isinstance(base_package, str):
        try:
            base_package = importlib.import_module(base_package)
        except ImportError:
            return False
    assert isinstance(base_package, ModuleType)

    base_package_name = base_package.__name__
    if base_package_name == submodule_name:
        return True
    if not submodule_name.startswith(base_package_name):
        return False
    try:
        importlib.import_module(submodule_name.removeprefix(base_package_name), package=base_package_name)
    except ImportError:
        return False
    return True
