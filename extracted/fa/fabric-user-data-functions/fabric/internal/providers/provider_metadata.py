# flake8: noqa: I003

class ProviderMetadata:

    _functions = {}

    def __init__(self):
        pass

    def add_kwargs(self, funcName: str, argName: str, **kwargs):
        if funcName not in self._functions:
            self._functions[funcName] = {}
        self._functions[funcName][argName] = kwargs

    def get_kwargs(self, funcName: str, argName: str) -> dict:
        return self._functions.get(funcName, {}).get(argName, {})
    
