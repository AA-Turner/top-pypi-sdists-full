from typing import List, Any, TypedDict, Dict, Required, Union


class Attachments(TypedDict, total=False):
    """
    attachments.

    User feedback event from Relay

    oneOf:
      - required:
        - attachment
      - required:
        - attachment_id
        - chunk_index
        - payload
    """

    type: Required[str]
    """ Required property """

    event_id: Required[str]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    payload: Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
    """ bytes """

    attachment_id: str
    chunk_index: int
    attachment: Dict[str, Any]
