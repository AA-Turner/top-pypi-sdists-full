# https://gitlab.com/flufl/public/-/work_items/10

import os

from public import private, public


@public
def one(x: int) -> int:
    return x * 2


one(4)


@private
def two(x: int) -> int:
    return x * 3


two(4)


# The single argument call form accepts things that aren't callables, so the annotations
# can't require one.  Each name is privatized again afterwards, leaving this module's
# __all__ as it was.


class Three:
    pass


public(Three)
public(os)
public('four')

private(Three)
private(os)
private('four')
