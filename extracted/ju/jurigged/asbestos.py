# def deco(f):
#     def wrap(x):
#         return f(x) + 7
#     return wrap


# @deco
# def f1(x):
#     return x * x


# @deco
# def f2(x):
#     return x * x


# from jurigged.goodies import develop

# @develop
# def f(x):
#     return x * x * x


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


module_code = compile(
    """
def foo():
    def bar():
        pass
    return bar
""",
    "<string>",
    "exec",
)

codes = list(find_subcodes(module_code))

# exec(module_code)
