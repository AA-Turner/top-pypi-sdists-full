from typing import Required, Union, Any, TypedDict, Literal, List, Dict


class _Root(TypedDict, total=False):
    type: "_RootType"
    start_time: Required[Union[int, float]]
    """ Required property """

    replay_id: Required[str]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    retention_days: Required[int]
    """ Required property """

    payload: Required[Union[List[int], Dict[str, Any]]]
    """
    Aggregation type: oneOf

    Required property
    """



_RootType = Union[Literal['replay_event']]
_ROOTTYPE_REPLAY_EVENT: Literal['replay_event'] = "replay_event"
"""The values for the '_RootType' enum"""

