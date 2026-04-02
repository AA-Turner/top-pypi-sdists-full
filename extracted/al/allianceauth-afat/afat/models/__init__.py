"""
Initialization of the afat.models package.
"""

# flake8: noqa

# Alliance Auth AFAT
from afat.models.afat import (
    Doctrine,
    Duration,
    Fat,
    FatLink,
    FleetType,
    General,
    Log,
    Setting,
    get_hash_on_save,
    get_sentinel_user,
)
from afat.models.smart_filter import FatsInTimeFilter
