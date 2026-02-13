from typing import Union, TypedDict, Required


class Outcome(TypedDict, total=False):
    """ outcome. """

    timestamp: Required[str]
    """ Required property """

    org_id: Union[int, None]
    project_id: Union[int, None]
    key_id: Union[int, None]
    outcome: Required[int]
    """ Required property """

    reason: Union[str, None]
    event_id: Union[str, None]
    category: Union[int, None]
    quantity: Union[int, None]
