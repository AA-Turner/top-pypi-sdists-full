import gc
import types


def find_subcodes(code):
    """
    Yields all code objects descended from this code object.
    e.g. given a module code object, will yield all codes defined in that module.
    """
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            yield const
            yield from find_subcodes(const)


def get_functions(code):
    """
    Returns functions that use the given code.
    """
    return [
        ref
        for ref in gc.get_referrers(code)
        if isinstance(ref, types.FunctionType) and ref.__code__ == code
    ]


module_code = compile(
    """
def foo():
    def bar():
        pass
    return bar

class Bonk:
    pass
""",
    "<string>",
    "exec",
)


print("AYE")


# breakpoint()
# codes = list(find_subcodes(module_code))

# exec(module_code)

# bars = [foo(), foo()]

# code_to_functions = {code: set(get_functions(code)) for code in codes}

# print(code_to_functions)

# assert code_to_functions == {foo.__code__: {foo}, bars[0].__code__: set(bars)}
