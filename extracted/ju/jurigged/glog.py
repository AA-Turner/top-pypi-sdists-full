class Brock:
    pass


# stuff = {
#     i: Brock()
#     for i in range(10000000)
# }


def foo(x):
    print("hey!")
    print("hey!")
    print("hey!")
    print("hey!")
    print("hey!")
    print("hey!")
    print("hey!")
    print("hey!")
    print("hey!")
    return x * x * x * x


def wow(x):
    def aye(y, z=3):
        return x + y + z + 12

    return aye


def fab():
    return 1 / 0


def rox():
    return 556


a = wow(4)


# from ovld import ovld

# @ovld.dispatch
# def f(self, x):
#     return self.call(x)

# @ovld
# def f(self, x: int):
#     return x * x

# @ovld
# def f(self, x: str):
#     return x + x

# @ovld
# def f(self, xs: list):
#     return [self(x) for x in xs]


# import sys
# sys.audit("rabbit", 123, 34)


# import types
# oi = object()

# foo2 = types.FunctionType(
#     foo.__code__,
#     globals()
# )

# foo3 = types.FunctionType(
#     foo.__code__.replace(co_name="foopy"),
#     globals()
# )
# # setattr(foo3, "elcode", foo.__code__)
# foo3.elcode = foo.__code__
# foo3.xxx = oi


# class Bork:
#     pass


# b = Bork()
# b.lala = foo.__code__
# b.lalax = [foo.__code__]


# class Slim:
#     __slots__ = ("a", "b", "c")
#     def __init__(self, a, b, c):
#         self.a = a
#         self.b = b
#         self.c = c


# sl = Slim(foo.__code__, oi, 33)


# import gc
# def refs(z=foo.__code__):
#     return gc.get_referrers(z)


# def trefs(z=foo.__code__):
#     return [type(x) for x in refs(z)]


# print(trefs())
# print(trefs(oi))
