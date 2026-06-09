from typing import TypedDict, List, Required


class _FunctionItem(TypedDict, total=False):
    fingerprint: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    function: Required[str]
    """ Required property """

    in_app: Required[bool]
    """ Required property """

    package: Required[str]
    """ Required property """

    self_times_ns: Required[List["_Uint"]]
    """ Required property """



class _Root(TypedDict, total=False):
    functions: Required[List["_FunctionItem"]]
    """ Required property """

    environment: str
    profile_id: Required[str]
    """ Required property """

    platform: Required[str]
    """ Required property """

    project_id: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    received: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    release: str
    retention_days: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    timestamp: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    transaction_name: Required[str]
    """ Required property """



_Uint = int
""" minimum: 0 """

