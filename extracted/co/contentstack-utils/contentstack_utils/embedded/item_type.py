"""
ItemType is Enumeration class that conatains two options for ItemType:

ASSET

ENTRY
"""

import enum


class ItemType(enum.Enum):
    """Contains Two option for ItemsType => ENTRY and ASSET """
    ENTRY = 'entry'
    ASSET = 'asset'
