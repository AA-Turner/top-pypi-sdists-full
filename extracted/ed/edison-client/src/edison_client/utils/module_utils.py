import ast
import importlib.util
import logging
import types
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_docstring_from_file(
    file_path: Path,
    class_name: str,
    function_name: str,
) -> str | None:
    """Extract the docstring for a specific function in a class without importing the module.

    Args:
        file_path (Path): Path to the Python file.
        class_name (str): Name of the class containing the function.
        function_name (str): Name of the function.

    Returns:
        str: The docstring of the function, or None if not found.

    """
    with file_path.open(encoding="utf-8") as file:
        source = file.read()

    tree = ast.parse(source)

    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for class_node in node.body:
                if (
                    isinstance(class_node, ast.FunctionDef)
                    and class_node.name == function_name
                ):
                    return ast.get_docstring(class_node)
    return None


def load_module(file_path: Path, package_name: str) -> types.ModuleType | None:
    """Load a Python file as part of a package.

    Args:
        file_path (Path): Path to the Python file.
        package_name (str): Full package name (e.g., "envs.dummy_env.env").

    Returns:
        Module: The loaded module.

    """
    spec = importlib.util.spec_from_file_location(package_name, file_path)
    if not spec:
        return None
    return importlib.util.module_from_spec(spec)


def fetch_environment_function_docstring(
    environment_name: str,
    directory: Path,
    function_name: str,
) -> str | None:
    """Retrieve the docstring for a specific function within a class, identified by an environment-style module path.

    The function attempts the following:
    1. Parse the file inferred from the environment name (e.g., environment "my_env.module.MyClass"
       attempts to find `directory/my_env/module.py`).
    2. If not found there, recursively searches all `.py` files under `directory` for a class
       with the given name containing the specified function.

    Args:
        environment_name (str): The environment name in dot notation
                                (e.g., "package.module.ClassName").
        directory (Path): The base directory containing the environment files.
        function_name (str): The name of the function to retrieve the docstring for.

    Returns:
        str | None: The docstring of the specified function, or None if not found.

    Raises:
        ValueError: If multiple classes with the same name are found in different files
                    (making the intended class ambiguous), an error is raised requiring
                    disambiguation.

    """
    parts = environment_name.split(".")
    class_name = parts[-1]

    guessed_file_path = directory / ("/".join(parts[1:-1]) + ".py")
    if guessed_file_path.exists():
        doc = extract_docstring_from_file(guessed_file_path, class_name, function_name)
        if doc:
            return doc

    matches = []
    for py_file in directory.rglob("*.py"):
        doc = extract_docstring_from_file(py_file, class_name, function_name)
        if doc:
            matches.append((py_file, doc))

    if not matches:
        return None
    if len(matches) == 1:
        return matches[0][1]
    match_paths = [str(m[0]) for m in matches]
    raise ValueError(
        f"Multiple classes named '{class_name}' found in:\n"
        + "\n".join(match_paths)
        + "\nPlease specify a more explicit path or ensure unique class names.",
    )


class OrganizationSelector:
    @staticmethod
    def select_organization(organizations: list[str]) -> str | None:
        """Prompts the user to select an organization from a list.

        Args:
            organizations: List of organization names/IDs

        Returns:
            Selected organization name/ID or None if selection was cancelled

        """
        if not organizations:
            raise ValueError("User does not belong to any organizations")

        if len(organizations) == 1:
            logger.debug(f"Only one organization available: {organizations[0]}")
            return organizations[0]

        print("\nAvailable organizations:")
        for idx, org in enumerate(organizations, 1):
            print(f"[{idx}]. {org}")

        while True:
            try:
                selection = input("\nSelect an organization number (or 'q' to quit): ")

                if selection.lower().strip() == "q":
                    return None

                idx = int(selection)
                if 1 <= idx <= len(organizations):
                    return organizations[idx - 1]
                print(f"Please enter a number between 1 and {len(organizations)}")
            except ValueError:
                print("Please enter a valid number or 'q' to quit")
