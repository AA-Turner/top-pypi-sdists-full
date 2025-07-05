import json
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Callable

def key_builder(
    func: Callable,
    *args,
    **kwargs
) -> str:
    arg_values = []
    for arg in args:
        try:
            if isinstance(arg, BaseModel) and hasattr(arg, "model_dump"):
                arg_values.append(arg.model_dump(mode="json"))
            else:
                arg_values.append(jsonable_encoder(arg))
        except Exception:
            arg_values.append(str(arg))

    kwarg_values = {}
    for k, v in kwargs.items():
        try:
            if isinstance(v, BaseModel) and hasattr(arg, "model_dump"):
                kwarg_values[k] = v.model_dump(mode="json")
            else:
                kwarg_values[k] = jsonable_encoder(v)
        except Exception:
            kwarg_values[k] = str(v)

    serialized_args = json.dumps(arg_values, sort_keys=True)
    serialized_kwargs = json.dumps(kwarg_values, sort_keys=True)
    
    return f"{func.__module__}:{func.__qualname__}({serialized_args}|{serialized_kwargs})"

def build_key(
    *ext: str,
    namespace: str
):
    return ":".join([namespace, *ext])