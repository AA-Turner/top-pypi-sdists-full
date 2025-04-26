"""
Tecton's sdk currently relies on the pendulum package for datetime functionality. In order for the sdk to support python
3.12, we must upgrade pendulum to 3.X. However, Tecton must also support python 3.7 at this time, which pendulum 3.X
does not support.

To make the sdk support python 3.7 - 3.12, this compat module mediates access to pendulum functionality: pendulum 3.0.X
for python>=3.12, and pendulum 2.1.2 for python<3.12 (as specified in sdk/pypi/pyproject.toml). The eventual goal is
removing the pendulum dependency entirely.
"""

import re

import pendulum as _pendulum  # noqa: TID251


_VERSION_3_0_PATTERN = r"^3\.0\.\d+$"
_IS_PENDULUM_3 = hasattr(_pendulum, "__version__") and re.match(_VERSION_3_0_PATTERN, getattr(_pendulum, "__version__"))

# classes
Duration = _pendulum.Duration

# modules
tz = _pendulum.tz

# functions
now = _pendulum.now
from_timestamp = _pendulum.from_timestamp
datetime = _pendulum.datetime
duration = _pendulum.duration
instance = _pendulum.instance
parse = _pendulum.parse
today = _pendulum.today
timezone = _pendulum.timezone

if _IS_PENDULUM_3:
    """
    In pendulum 2, DateTime.__str__ returned iso8601 based timestamps e.g. '1975-05-21T22:00:00'. However,
    in pendulum 3, DateTime.__str__ returns timestamps without the 'T' to match the native python datetime behavior.
    tecton_athena sql templates like sdk/tecton_athena/templates/time_limit.sql explicitly expect iso8601 timestamps
    and tests assert the 'T' is present. In order to maintain compatibility with our code, we override __str__ here.
    """

    def pendulum_V2_str(self):
        return self.isoformat("T")

    DateTime = _pendulum.DateTime
    DateTime.__str__ = pendulum_V2_str

    """
    In pendulum 3, the Period class and period method have been renamed to Interval and interval, respectively.
    Rename them to Period for compatibility.
    """
    Period = _pendulum.Interval
    period = _pendulum.interval

else:
    DateTime = _pendulum.DateTime
    Period = _pendulum.Period
    period = _pendulum.period
