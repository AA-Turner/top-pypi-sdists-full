from typing import TypedDict, Required, Union, Dict, List, Any


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

    attachments: List["_ProfileAttachmentsItem"]
    """ files related to the profile chunk (e.g. a raw profile), stored in the object store """



class _ProfileAttachmentsItem(TypedDict, total=False):
    name: Required[str]
    """ Required property """

    content_type: str
    stored_id: Required[str]
    """ Required property """

