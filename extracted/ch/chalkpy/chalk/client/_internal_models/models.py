from enum import IntEnum


class OfflineQueryGivensVersion(IntEnum):
    """Version in which inputs to offline query is stored as a ChalkTable"""

    NATIVE_TS_FEATURE_FOR_ROOT_NS = 1
    """Replace '__chalk__.CHALK_TS' with the 'native' TS feature for the root output namespace"""

    SINGLE_TS_COL_NAME = 2
    """Replace '__chalk__.CHALK_TS' with the single column name '__ts__' (TS_COL_NAME)"""

    SINGLE_TS_COL_NAME_WITH_URI_PREFIX = 3
    """
    Replace '__chalk__.CHALK_TS' with the single column name '__ts__' (TS_COL_NAME)
    Also, this is now a prefix instead of a single file
    """


TS_COL_NAME = "__ts__"
INDEX_COL_NAME = "__index__"
PKEY_COL_NAME = "__id__"
OBSERVED_AT_COL_NAME = "__oat__"
