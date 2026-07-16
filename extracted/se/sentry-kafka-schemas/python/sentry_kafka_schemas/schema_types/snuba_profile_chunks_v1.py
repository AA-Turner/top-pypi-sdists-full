from typing import Union, Required, TypedDict


class ProfileChunk(TypedDict, total=False):
    """ profile_chunk. """

    project_id: Required["_Uint64"]
    """
    minimum: 0

    Required property
    """

    profiler_id: Required["_Uuid"]
    """
    minLength: 32
    maxLength: 36

    Required property
    """

    chunk_id: Required["_Uuid"]
    """
    minLength: 32
    maxLength: 36

    Required property
    """

    start_timestamp: Required["_PositiveFloat"]
    """
    minimum: 0

    Required property
    """

    end_timestamp: Required["_PositiveFloat"]
    """
    minimum: 0

    Required property
    """

    retention_days: Required["_Uint16"]
    """
    minimum: 0
    maximum: 65535

    Required property
    """

    received: Required["_Uint64"]
    """
    minimum: 0

    Required property
    """



_PositiveFloat = Union[int, float]
""" minimum: 0 """



_Uint16 = int
"""
minimum: 0
maximum: 65535
"""



_Uint64 = int
""" minimum: 0 """



_Uuid = str
"""
minLength: 32
maxLength: 36
"""

