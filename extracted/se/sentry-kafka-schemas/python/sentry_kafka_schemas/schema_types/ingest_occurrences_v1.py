from typing import Required, Union, List, TypedDict


class _Root(TypedDict, total=False):
    """ Issue occurrence """

    id: Required[str]
    """ Required property """

    project_id: Required[int]
    """ Required property """

    fingerprint: Required[List[str]]
    """ Required property """

    issue_title: Union[str, None]
    subtitle: Union[str, None]
    type: Union[int, None]
    initial_issue_priority: Union[int, None]
    payload_type: Union[str, None]
