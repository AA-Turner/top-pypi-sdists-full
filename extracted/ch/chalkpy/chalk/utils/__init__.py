import sys
from typing import Any, TypeAlias

from chalk.utils.secret import Secret

HAS_PEP_649 = sys.version_info >= (3, 14)
"""PEP 649 (deferred evaluation of annotations) is enabled by default in Python 3.14+.
Annotations are no longer eagerly stored in cls.__dict__['__annotations__']."""

MachineType: TypeAlias = str
"""The type of machine to use.

You can optionally specify that resolvers need to run
on a machine other than the default. Must be configured
in your deployment.
"""

AnyDataclass: TypeAlias = Any
"""Any class decorated by `@dataclass`.

There isn't a base class for `dataclass`, so we use this
`TypeAlias` to refer to indicate any class decorated with
`@dataclass`.
"""

__all__ = (
    "AnyDataclass",
    "HAS_PEP_649",
    "MachineType",
    "Secret",
)
