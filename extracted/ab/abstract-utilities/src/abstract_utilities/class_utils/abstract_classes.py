from .imports import (
    get_args,
    SingletonMeta,
    prune_inputs,
    run_pruned_func,
)
import inspect
from dataclasses import fields, is_dataclass, MISSING
def get_inputs(cls, *args, **kwargs):
    """
    Dynamically construct a dataclass instance from args and kwargs,
    filling missing values from defaults in the dataclass.
    """
    fields = list(cls.__annotations__.keys())
    values = {}

    args = list(args)
    for field in fields:
        if field in kwargs:
            values[field] = kwargs[field]
        elif args:
            values[field] = args.pop(0)
        else:
            values[field] = getattr(cls(), field)  # default from dataclass

    return cls(*args,**values)
def get_input_params(func):
    sig = inspect.signature(func)
    return sig.parameters
def get_args(func, *args,**kwargs):
    parameters = get_input_params(func)
    parameters = dict(parameters)
    for key,value in parameters.items():
        value = str(value)
        if value.startswith('**'):
            kwargs_key = key
        elif value.startswith('*'):
            args_key = key
            kwargs_copy = kwargs.copy()
            for k_key,k_value in kwargs.items():
                if args_key == k_key and  isinstance(k_value,list or tuple or set):
                    args = args | tuple(k_value)
                    del kwargs[k_key]
    return args,kwargs

def safe_construct(cls, *args, **kwargs):
    """Build cls from whatever's given. Missing fields -> their default
    (or None if none). Unknown keys -> dropped (or stashed in `extra` if
    the class has one). Never raises on arg mismatch."""
    flds = {f.name: f for f in fields(cls)} if is_dataclass(cls) else {}

    out = {}
    leftover = dict(kwargs)
    arglist = list(args)

    for name, f in flds.items():
        if name in leftover:
            out[name] = leftover.pop(name)
        elif arglist:
            out[name] = arglist.pop(0)
        elif f.default is not MISSING:
            out[name] = f.default
        elif f.default_factory is not MISSING:
            out[name] = f.default_factory()
        else:
            out[name] = None              # required but absent -> None, no crash

    # unknown keys: keep them if the class has an `extra` field, else drop
    if "extra" in flds:
        out.setdefault("extra", {})
        out["extra"].update(leftover)

    return cls(**out)
