import os
from pathlib import Path
from orionis.services.introspection.modules.reflection import ReflectionModule


class Reactor:

    def __init__(
        self
    ):
        self.__reactors = {}
        self.__command_path = str((Path.cwd() / 'app' / 'console' / 'commands').resolve())
        self.__loadCommands()

    def __loadCommands(self):

        # Base path of the project
        root_path = str(Path.cwd())

        # Iterate through the command path and load command modules
        for current_directory, _, files in os.walk(self.__command_path):
            for file in files:
                if file.endswith('.py'):
                    pre_module = current_directory.replace(root_path, '').replace(os.sep, '.').lstrip('.')
                    file_name = file[:-3]
                    print(f"{pre_module}.{file_name}")
                    rf_module = ReflectionModule(f"{pre_module}.{file_name}")
                    print(rf_module.getClasses())