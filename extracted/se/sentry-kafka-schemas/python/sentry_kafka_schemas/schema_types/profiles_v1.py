from typing import TypedDict, Dict, Required, List, Any, Union


class Profile(TypedDict, total=False):
    """
    profile.

    profile data from relay
    """

    type: Required[str]
    """ Required property """

    organization_id: Required[int]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    key_id: Required[int]
    """ Required property """

    received: int
    payload: Required[Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]]
    """
    bytes

    Required property
    """

