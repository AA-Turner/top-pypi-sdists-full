import json
from typing import Callable
from fastapi.encoders import jsonable_encoder

class BaseCacheConfigurations:
    @staticmethod
    def key_builder(
        func: Callable,
        *args,
        **kwargs
    ) -> str:
        arg_values = []
        for arg in args:
            try:
                arg_values.append(jsonable_encoder(arg))
            except Exception:
                arg_values.append(str(arg))

        kwarg_values = {}
        for k, v in kwargs.items():
            try:
                kwarg_values[k] = jsonable_encoder(v)
            except Exception:
                kwarg_values[k] = str(v)

        serialized_args = json.dumps(arg_values, sort_keys=True)
        serialized_kwargs = json.dumps(kwarg_values, sort_keys=True)
        
        return f"{func.__module__}:{func.__qualname__}({serialized_args}|{serialized_kwargs})"