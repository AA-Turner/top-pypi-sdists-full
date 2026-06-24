from typing import Required, Dict, TypedDict, List, Union, Any


class _Root(TypedDict, total=False):
    """ Transactions message from Relay """

    type: Required[str]
    """ Required property """

    payload: Required[Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]]
    """
    bytes

    Required property
    """

    event_id: Required[str]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    start_time: Required[int]
    """ Required property """

