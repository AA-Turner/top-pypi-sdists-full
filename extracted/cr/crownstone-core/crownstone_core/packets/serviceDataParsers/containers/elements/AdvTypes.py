from enum import Enum


class AdvType(Enum):
    CROWNSTONE_STATE   = 0
    CROWNSTONE_ERROR   = 1
    EXTERNAL_STATE     = 2
    EXTERNAL_ERROR     = 3
    ALTERNATIVE_STATE  = 4
    HUB_STATE          = 5
    MICROAPP_DATA      = 6

    SETUP_STATE        = 100

    UNKNOWN_DATA       = 200

    CROWNSTONE_FLAGS   = 300
    HUB_FLAGS          = 301
    MICROAPP_FLAGS     = 302

    CROWNSTONE_ERRORS  = 500