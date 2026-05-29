from .imports import *
import inspect
from dataclasses import fields, is_dataclass, MISSING
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

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

    return cls(**values)



class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

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

def prune_inputs(func, *args, **kwargs):
    """
    Smart argument adapter:
    - Detects if func accepts *args or **kwargs
    - Builds new positional arguments from kwargs when appropriate
    - Handles explicit {"args": [...]} convention
    """

    sig = inspect.signature(func)
    params = sig.parameters

    has_varargs = any(p.kind == inspect.Parameter.VAR_POSITIONAL for p in params.values())
    has_varkw   = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values())

    new_args = list(args)
    new_kwargs = dict(kwargs)

    # -----------------------------------------------------------
    # 1. If user provided explicit args: {"args": [...]}
    # -----------------------------------------------------------
    if "args" in new_kwargs:
        explicit_args = new_kwargs.pop("args")
        if isinstance(explicit_args, (list, tuple)):
            new_args.extend(explicit_args)
        else:
            new_args.append(explicit_args)

    # -----------------------------------------------------------
    # 2. If function has *args, infer which kwargs belong there
    # -----------------------------------------------------------
    if has_varargs:

        # Heuristic rules for upgrading kwargs to args:
        #   - if the function has NO named params, treat all scalar kwargs as positional
        #   - common param names like "file_path" also qualify
        preferred_as_args = {"path", "file", "file_path", "filename", "value"}

        positional_candidates = []

        for k in list(new_kwargs.keys()):
            v = new_kwargs[k]

            # candidate rules:
            if k in preferred_as_args:
                positional_candidates.append(v)
                del new_kwargs[k]

            # scalars but not mappings/lists (optional)
            elif isinstance(v, (str, int, float)) and len(positional_candidates) == 0:
                positional_candidates.append(v)
                del new_kwargs[k]

        new_args.extend(positional_candidates)

    # -----------------------------------------------------------
    # 3. If function does NOT accept **kwargs → strip extras
    # -----------------------------------------------------------
    if not has_varkw:
        allowed = {
            name for name, p in params.items()
            if p.kind in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY
            )
        }
        new_kwargs = {k: v for k, v in new_kwargs.items() if k in allowed}

    return tuple(new_args), new_kwargs
def run_pruned_func(func, *args, **kwargs):
   args,kwargs = prune_inputs(func, *args, **kwargs)
   return func(*args, **kwargs)

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
