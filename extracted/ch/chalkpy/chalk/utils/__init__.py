from typing import Any

from typing_extensions import TypeAlias

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
