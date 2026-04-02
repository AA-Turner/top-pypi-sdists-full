import ast
import inspect


def _check_func(cls, method, func_expr):
    method_str = method.__name__
    if inspect.isfunction(method):
        return method.__name__ == func_expr

    if func_expr in [
        f"self.{method_str}",
        f"cls.{method_str}",
    ]:
        return issubclass(cls, method.__self__.__class__)

    return f"{method.__self__.__class__.__name__}().{method_str}" == func_expr


def _find_args_and_kwargs(node, method):
    pos_args = [ast.unparse(arg) for arg in node.args]
    # Add kwargs
    call_params = {kw.arg: ast.unparse(kw.value) for kw in node.keywords}

    # Fill with args
    params = [
        p for p in inspect.signature(method).parameters if p not in ["self", "cls"]
    ]
    for i, arg in enumerate(pos_args):
        call_params[params[i]] = arg

    return call_params


def analyze_method_calls(cls, methods_to_track):
    calls = {method: [] for method in methods_to_track}
    # Loop over all parents except object
    for base in cls.__mro__:
        if base is object:
            continue
        source = inspect.getsource(base)
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func_expr = ast.unparse(node.func)
            for method in calls:
                if _check_func(cls, method, func_expr):
                    calls[method].append(_find_args_and_kwargs(node, method))

    return calls
