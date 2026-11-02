import importlib.util
import inspect
import os

from rock.cli.command.command import Command


class CommandLoader:
    @staticmethod
    async def load(directories: list[str], base_class: type = Command):
        subclasses = []
        for directory in directories:
            subclasses.extend(await CommandLoader.load_one_directory(directory, base_class))
        return subclasses

    @staticmethod
    async def load_one_directory(directory: str, base_class: type = Command):
        subclasses = []

        # scan all .py files in the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == "__init__.py" or not file.endswith(".py"):
                    continue

                filepath = os.path.join(root, file)

                # get the module full name
                rel_path = os.path.relpath(filepath, directory)
                module_full_name = rel_path.replace("/", ".").replace("\\", ".").replace(".py", "")

                # import the module
                spec = importlib.util.spec_from_file_location(module_full_name, filepath)
                if spec is None:
                    continue
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"Failed to load {filepath}: {e}")
                    continue

                # get all classes in the module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, base_class) and obj is not base_class:
                        if obj.__module__ == module_full_name or obj.__module__.startswith(module_full_name):
                            subclasses.append(obj)

        return subclasses
