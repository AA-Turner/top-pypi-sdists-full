"""Global constants for Eve Universe."""

from enum import IntEnum


class EveCategoryId(IntEnum):
    """An Eve category ID."""

    SHIP = 6
    BLUEPRINT = 9
    STRUCTURE = 65
    SKIN = 91


class EveGroupId(IntEnum):
    """An Eve group ID."""

    CHARACTER = 1
    CORPORATION = 2
    SOLAR_SYSTEM = 5
    STAR = 6
    PLANET = 7
    MOON = 8
    ASTEROID_BELT = 9
    STARGATE = 10
    STATION = 15
    ALLIANCE = 32


class EveRegionId(IntEnum):
    """An Eve region ID."""

    POCHVEN = 10000070


# ESI
POST_UNIVERSE_NAMES_MAX_ITEMS = 1000
