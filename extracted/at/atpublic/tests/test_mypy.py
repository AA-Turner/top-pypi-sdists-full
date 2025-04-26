# https://gitlab.com/warsaw/public/-/issues/10

from public import private, public


@public
def one(x: int) -> int:
    return x * 2


one(4)


@private
def two(x: int) -> int:
    return x * 3


two(4)
