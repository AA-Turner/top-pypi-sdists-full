# flake8: noqa: I003

import importlib

class module_factory:
    
    modules = {}

    def __init__(self):
        pass

    def load_module(self, module_name:str):
        if module_name in module_factory.modules:
            return module_factory.modules[module_name]
        else:
            try:
                module_factory.modules[module_name] = importlib.import_module(module_name)
                return module_factory.modules[module_name]
            except ImportError as e:
                raise ImportError(f"Module {module_name} not found") from e