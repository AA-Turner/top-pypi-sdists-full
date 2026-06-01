"""Source code reader module."""

import inspect
from bacore.domain.source_code import (
    ClassModel,
    DirectoryModel,
    FunctionModel,
    ModuleModel,
)
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import Any, Literal, Optional


class ExternalModule:
    """External module.

    Attributes:
        external_dir: Directory where external module is fetched from.
        module_name: Name of module file (without ".py")
    """

    def __init__(self, external_dir: str, module_name: str):
        self.external_dir = Path(external_dir)
        self.module_name = module_name

    def load(self) -> ModuleType:
        """Loading external module into path.

        Returns:
            External module loaded into sys.path.

        Raises:
            ImportError: If the module cannot be loaded.
        """
        # sys.path.append(str(self.external_dir))
        module_path = self.external_dir / f"{self.module_name}.py"

        try:
            spec = spec_from_file_location(self.module_name, module_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load spec or spec.loader for module {self.module_name}")
            external_module = module_from_spec(spec)
            spec.loader.exec_module(external_module)
            return external_module
        except ImportError as e:
            raise ImportError(f"Failed to load module {self.module_name} with error: {e}")

    def execute_func(self, function_name: str, accept_return_value: bool) -> Any:
        """Execute a function from from an external module and return the values from what the function executed.

        Parameters:
            external_module: External module type.
            function_name: Name of the function to execute in the external module.

        Returns:
            Return value of externally defined function.

        Raises:
            ValueError: If the function is not callable.
        """
        # ext_module = external_module.load()
        func = getattr(self.load(), function_name, None)
        if callable(func):
            if accept_return_value:
                return func()
            else:
                func()
        else:
            raise ValueError(f"Function is not callable {function_name}")


def get_objects(
    object_holder: ModuleType | type,
    object_holder_uri: str,
    match_object_type: Literal["class", "function", "class_and_function"],
) -> list[ClassModel | FunctionModel]:
    """Get members of a python object which are either functions or classes or both.

    Parameters
        object_holder: A module or a class.
        object_holder_module_path: Path to the object holding the with dot notation.
        match_object_type: The type of object type wished to be returned. Can be function, class or both.

    Returns
        SrcClass and/or SrcFunc.
    """
    match match_object_type:
        case "class":

            def member_filter(member):
                return inspect.isclass(member)

        case "function":

            def member_filter(member):
                return inspect.isfunction(member) or inspect.ismethod(member)

        case "class_and_function":

            def member_filter(member):
                return inspect.isclass(member) or inspect.isfunction(member) or inspect.ismethod(member)

        case _:
            raise ValueError(f"wrong value for match_object_type: {match_object_type}")

    return [
        (ClassModel(klass=member) if inspect.isclass(member) else FunctionModel(func=member))
        for _, member in inspect.getmembers(object_holder)
        if member_filter(member) and member.__module__.startswith(object_holder_uri)
    ]


def get_package_init_file(package_path: Path, package_root: Optional[str] = None) -> ModuleModel:
    """Return a file from a list of files if it meets the condition of having the name '__init__.py."""
    package = DirectoryModel(path=package_path, package_root=package_root)
    for module in package.modules:
        if module.name == "bacore":
            return module
    raise FileNotFoundError("No '__init__.py' file found in the package.")
