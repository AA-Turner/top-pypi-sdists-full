"""Global constants for Eve Universe."""

from enum import IntEnum


class EveCategoryId(IntEnum):
    """An Eve category ID."""

    BLUEPRINT = 9
    CELESTIAL = 2
    OWNER = 1
    SHIP = 6
    SKIN = 91
    STRUCTURE = 65


class EveGroupId(IntEnum):
    """An Eve group ID."""

    ALLIANCE = 32
    ASTEROID_BELT = 9
    CHARACTER = 1
    CITADEL = 1657
    CORPORATION = 2
    FRIGATE = 25
    MOON = 8
    PERMANENT_SKIN = 1950
    PLANET = 7
    SOLAR_SYSTEM = 5
    STAR = 6
    STARGATE = 10
    STATION = 15


class EveRegionId(IntEnum):
    """An Eve region ID."""

    POCHVEN = 10000070


class EveTypeId(IntEnum):
    """An Eve type ID."""

    ASTEROID_BELT = 15
    MOON = 14
    SOLAR_SYSTEM = 5


# ESI
POST_UNIVERSE_NAMES_MAX_ITEMS = 1000
