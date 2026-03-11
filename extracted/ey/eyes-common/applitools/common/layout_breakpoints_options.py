from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING

import attr

if TYPE_CHECKING:
    from typing import List, Optional, Union


@attr.s
class LayoutBreakpointsOptions(object):
    breakpoints = attr.ib()  # type: Union[bool, List[int]]
    reload = attr.ib(default=None)  # type: Optional[bool]
    height_breakpoints = attr.ib(default=None)  # type: Optional[bool]
