from typing import List, TypedDict, Union, Any, Required, Dict


class FeedbackEvent(TypedDict, total=False):
    """
    feedback_event.

    User feedback event from Relay
    """

    type: Required[str]
    """ Required property """

    payload: Required[Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]]
    """
    bytes. JSON string of the wrapped feedback event

    Required property
    """

    event_id: Required[str]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    start_time: Required[int]
    """ Required property """

