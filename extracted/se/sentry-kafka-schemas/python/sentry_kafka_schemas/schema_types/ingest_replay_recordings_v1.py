from typing import Required, Union, Any, TypedDict, Literal, List, Dict


class ReplayRecording(TypedDict, total=False):
    """
    replay_recording.

    A replay recording, or a chunk thereof
    """

    type: Required[Literal['replay_recording_not_chunked']]
    """ Required property """

    replay_id: Required[str]
    """ Required property """

    key_id: Union[None, int]
    org_id: Required[int]
    """
    minimum: 0

    Required property
    """

    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    received: Required[int]
    """
    minimum: 0

    Required property
    """

    retention_days: Required[int]
    """ Required property """

    payload: Required[Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]]
    """
    msgpack bytes

    Required property
    """

    replay_event: Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
    """ JSON bytes """

    replay_video: Union[str, Union[int, float], Dict[str, Any], List[Any], bool, None]
    """ JSON bytes """

    version: int
    """ default: 0 """



_REPLAY_RECORDING_VERSION_DEFAULT = 0
""" Default value of the field path 'replay_recording version' """

