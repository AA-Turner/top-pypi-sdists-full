import importlib
import inspect
import pkgutil
from collections.abc import Iterable
from types import ModuleType


def find_classes(packages, target: type):
    # Handle string module names (lazy import)
    if isinstance(packages, str):
        packages = (packages,)
    elif isinstance(packages, ModuleType):
        packages = (packages,)
    elif not isinstance(packages, Iterable):
        raise TypeError(
            "packages must be a module, string module name, or iterable of modules/strings"
        )

    classes = set()

    for package in packages:
        # If package is a string, import it lazily
        if isinstance(package, str):
            package = importlib.import_module(package)

        for _, module_name, _ in pkgutil.walk_packages(
            package.__path__,
            package.__name__ + ".",
        ):
            module = importlib.import_module(module_name)

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    obj.__module__ == module.__name__
                    and issubclass(obj, target)
                    and obj is not target
                ):
                    classes.add(obj)

    return classes
