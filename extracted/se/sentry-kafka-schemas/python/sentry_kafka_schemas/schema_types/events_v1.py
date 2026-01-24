from typing import Required, Union, Any, TypedDict, Literal, List, Dict, Tuple


class ClientSdkInfo(TypedDict, total=False):
    """ client_sdk_info. """

    integrations: Union[List[Any], None]
    """
    items:
      $ref: '#/definitions/Unicodify'
      used: !!set
        $ref: null
    """

    name: Any
    version: Any


class EndDeleteGroupsMessageBody(TypedDict, total=False):
    """ end_delete_groups_message_body. """

    transaction_id: str
    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    group_ids: Required[List[int]]
    """ Required property """

    datetime: Required[str]
    """ Required property """



class EndDeleteTagMessageBody(TypedDict, total=False):
    """ end_delete_tag_message_body. """

    tag: Required[str]
    """ Required property """

    datetime: Required[str]
    """ Required property """

    project_id: Required[int]
    """
    minimum: 0

    Required property
    """



class EndMergeMessageBody(TypedDict, total=False):
    """ end_merge_message_body. """

    transaction_id: str
    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    previous_group_ids: Required[List[int]]
    """ Required property """

    new_group_id: Required[int]
    """ Required property """

    new_group_first_seen: str
    datetime: Required[str]
    """ Required property """



class EndUnmergeMessageBody(TypedDict, total=False):
    """ end_unmerge_message_body. """

    transaction_id: str
    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    previous_group_id: Required[int]
    """ Required property """

    new_group_id: Required[int]
    """ Required property """

    hashes: Required[List[str]]
    """ Required property """

    datetime: Required[str]
    """ Required property """



EventStreamMessage = Union["_InsertEventMessage", Tuple[Literal[2], Literal['start_delete_groups'], "_StartDeleteGroupsMessage2"], Tuple[Literal[2], Literal['start_merge'], "StartMergeMessageBody"], Tuple[Literal[2], Literal['start_unmerge'], "_StartUnmergeMessage2"], Tuple[Literal[2], Literal['start_delete_tag'], "_StartDeleteTagMessage2"], Tuple[Literal[2], Literal['end_delete_groups'], "EndDeleteGroupsMessageBody"], Tuple[Literal[2], Literal['end_merge'], "EndMergeMessageBody"], Tuple[Literal[2], Literal['end_unmerge'], "EndUnmergeMessageBody"], Tuple[Literal[2], Literal['end_delete_tag'], "EndDeleteTagMessageBody"], Tuple[Literal[2], Literal['tombstone_events'], "TombstoneEventsMessageBody"], Tuple[Literal[2], Literal['replace_group'], "ReplaceGroupMessageBody"], Tuple[Literal[2], Literal['exclude_groups'], "ExcludeGroupsMessageBody"]]
"""
event_stream_message.

Aggregation type: anyOf
"""



class ExcludeGroupsMessageBody(TypedDict, total=False):
    """ exclude_groups_message_body. """

    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    group_ids: Required[List[int]]
    """ Required property """



class InsertEvent(TypedDict, total=False):
    """ insert_event. """

    data: Required["_ErrorData"]
    """ Required property """

    datetime: str
    event_id: Required[str]
    """ Required property """

    group_id: Required[int]
    """
    minimum: 0

    Required property
    """

    message: Required[str]
    """ Required property """

    platform: Union[str, None]
    """ default: None """

    primary_hash: Required[str]
    """ Required property """

    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    retention_days: Union[int, None]
    """
    default: None
    minimum: 0
    """



class ReplaceGroupMessageBody(TypedDict, total=False):
    """ replace_group_message_body. """

    event_ids: Required[List[str]]
    """ Required property """

    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    from_timestamp: str
    to_timestamp: str
    transaction_id: str
    datetime: str
    new_group_id: Required[int]
    """ Required property """



class SentryExceptionChain(TypedDict, total=False):
    """ sentry_exception_chain. """

    values: Union[List["_SentryExceptionChainValuesArrayItem"], None]
    """
    items:
      anyOf:
      - $ref: '#/definitions/ExceptionValue'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """



class SentryRequest(TypedDict, total=False):
    """ sentry_request. """

    headers: Union[List["_SentryRequestHeadersArrayItem"], None]
    """
    items:
      items:
      - type: string
      - $ref: '#/definitions/Unicodify'
        used: !!set
          $ref: null
      maxItems: 2
      minItems: 2
      type:
      - array
      - 'null'
    """

    method: Any


class SentryThreadChain(TypedDict, total=False):
    """ sentry_thread_chain. """

    values: Union[List["_SentryThreadChainValuesArrayItem"], None]
    """
    items:
      anyOf:
      - $ref: '#/definitions/ThreadValue'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """



class SentryUser(TypedDict, total=False):
    """ sentry_user. """

    email: Any
    geo: Union[Dict[str, Any], None]
    """
    additionalProperties:
      $ref: '#/definitions/ContextStringify'
      used: !!set
        $ref: null
    """

    id: Any
    ip_address: Union[str, None]
    """ default: None """

    username: Any


class StartMergeMessageBody(TypedDict, total=False):
    """ start_merge_message_body. """

    transaction_id: str
    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    previous_group_ids: Required[List[int]]
    """ Required property """

    new_group_id: Required[int]
    """ Required property """

    new_group_first_seen: str
    datetime: Required[str]
    """ Required property """



class TombstoneEventsMessageBody(TypedDict, total=False):
    """ tombstone_events_message_body. """

    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    event_ids: Required[List[str]]
    """ Required property """

    old_primary_hash: Union[str, None]
    from_timestamp: str
    to_timestamp: str
    datetime: str


class _Contexts(TypedDict, total=False):
    replay: "_ContextsReplay"
    """ Aggregation type: anyOf """

    trace: "_ContextsTrace"
    """ Aggregation type: anyOf """



_ContextsReplay = Union["_ReplayContext", None]
""" Aggregation type: anyOf """



_ContextsTrace = Union["_TraceContext", None]
""" Aggregation type: anyOf """



_ERROR_DATA_ERRORS_DEFAULT = None
""" Default value of the field path 'error data errors' """



_ERROR_DATA_LOCATION_DEFAULT = None
""" Default value of the field path 'error data location' """



_ERROR_DATA_MODULES_DEFAULT = None
""" Default value of the field path 'error data modules' """



_ERROR_DATA_SAMPLE_RATE_DEFAULT = None
""" Default value of the field path 'error data sample_rate' """



_ERROR_DATA_SYMBOLICATED_IN_APP_DEFAULT = None
""" Default value of the field path 'error data symbolicated_in_app' """



_ERROR_DATA_VERSION_DEFAULT = None
""" Default value of the field path 'error data version' """



class _ErrorData(TypedDict, total=False):
    contexts: "_ErrorDataContexts"
    """ Aggregation type: anyOf """

    culprit: Any
    errors: Union[List[Any], None]
    """
    default: None
    items: True
    """

    exception: "_ErrorDataException"
    """ Aggregation type: anyOf """

    location: Union[str, None]
    """ default: None """

    modules: Union[Dict[str, Union[str, None]], None]
    """
    default: None
    additionalProperties:
      type:
      - string
      - 'null'
    """

    received: Required[Union[int, float]]
    """ Required property """

    request: "_ErrorDataRequest"
    """ Aggregation type: anyOf """

    sdk: "_ErrorDataSdk"
    """ Aggregation type: anyOf """

    tags: Union[List["_ErrorDataTagsArrayItem"], None]
    """
    items:
      items:
      - $ref: '#/definitions/Unicodify'
        used: !!set
          $ref: null
      - $ref: '#/definitions/Unicodify'
        used: !!set
          $ref: null
      maxItems: 2
      minItems: 2
      type:
      - array
      - 'null'
    """

    threads: "_ErrorDataThreads"
    """ Aggregation type: anyOf """

    title: Any
    type: Any
    user: "_ErrorDataUser"
    """ Aggregation type: anyOf """

    version: Union[str, None]
    """ default: None """

    symbolicated_in_app: Union[bool, None]
    """ default: None """

    sample_rate: Union[Union[int, float], None]
    """ default: None """



_ErrorDataContexts = Union["_Contexts", None]
""" Aggregation type: anyOf """



_ErrorDataException = Union["SentryExceptionChain", None]
""" Aggregation type: anyOf """



_ErrorDataRequest = Union["SentryRequest", None]
""" Aggregation type: anyOf """



_ErrorDataSdk = Union["ClientSdkInfo", None]
""" Aggregation type: anyOf """



_ErrorDataTagsArrayItem = Union[Tuple[Any, Any], None]
"""
items:
  - $ref: '#/definitions/Unicodify'
    used: !!set
      $ref: null
  - $ref: '#/definitions/Unicodify'
    used: !!set
      $ref: null
maxItems: 2
minItems: 2
"""



_ErrorDataThreads = Union["SentryThreadChain", None]
""" Aggregation type: anyOf """



_ErrorDataUser = Union["SentryUser", None]
""" Aggregation type: anyOf """



class _ExceptionMechanism(TypedDict, total=False):
    handled: Any
    type: Any


class _ExceptionValue(TypedDict, total=False):
    mechanism: "_ExceptionValueMechanism"
    """ Aggregation type: anyOf """

    stacktrace: "_ExceptionValueStacktrace"
    """ Aggregation type: anyOf """

    thread_id: "_ExceptionValueThreadId"
    """ Aggregation type: anyOf """

    type: Any
    value: Any


_ExceptionValueMechanism = Union["_ExceptionMechanism", None]
""" Aggregation type: anyOf """



_ExceptionValueStacktrace = Union["_StackTrace", None]
""" Aggregation type: anyOf """



_ExceptionValueThreadId = Union["_ThreadId", None]
""" Aggregation type: anyOf """



_INSERT_EVENT_PLATFORM_DEFAULT = None
""" Default value of the field path 'insert_event platform' """



_INSERT_EVENT_RETENTION_DAYS_DEFAULT = None
""" Default value of the field path 'insert_event retention_days' """



_InsertEventMessage = Tuple["_InsertEventMessage0", str, "InsertEvent", Any]
"""
maxItems: 4
minItems: 4
"""



_InsertEventMessage0 = int
""" minimum: 0 """



class _ReplayContext(TypedDict, total=False):
    replay_id: Union[str, None]


_SENTRY_USER_IP_ADDRESS_DEFAULT = None
""" Default value of the field path 'sentry_user ip_address' """



_STACK_FRAME_COLNO_DEFAULT = None
""" Default value of the field path 'stack frame colno' """



_STACK_FRAME_IN_APP_DEFAULT = None
""" Default value of the field path 'stack frame in_app' """



_STACK_FRAME_LINENO_DEFAULT = None
""" Default value of the field path 'stack frame lineno' """



_SentryExceptionChainValuesArrayItem = Union["_ExceptionValue", None]
""" Aggregation type: anyOf """



_SentryRequestHeadersArrayItem = Union[Tuple[str, Any], None]
"""
items:
  - type: string
  - $ref: '#/definitions/Unicodify'
    used: !!set
      $ref: null
maxItems: 2
minItems: 2
"""



_SentryThreadChainValuesArrayItem = Union["_ThreadValue", None]
""" Aggregation type: anyOf """



class _StackFrame(TypedDict, total=False):
    abs_path: Any
    colno: Union[int, None]
    """
    default: None
    minimum: 0
    """

    filename: Any
    function: Any
    in_app: Union[bool, None]
    """ default: None """

    lineno: Union[int, None]
    """
    default: None
    minimum: 0
    """

    module: Any
    package: Any


class _StackTrace(TypedDict, total=False):
    frames: Union[List["_StackTraceFramesArrayItem"], None]
    """
    items:
      anyOf:
      - $ref: '#/definitions/StackFrame'
      - type: 'null'
      used: !!set
        $ref: null
        anyOf: null
    """



_StackTraceFramesArrayItem = Union["_StackFrame", None]
""" Aggregation type: anyOf """



class _StartDeleteGroupsMessage2(TypedDict, total=False):
    transaction_id: str
    project_id: Required[int]
    """
    minimum: 0

    Required property
    """

    group_ids: Required[List[int]]
    """ Required property """

    datetime: Required[str]
    """ Required property """



class _StartDeleteTagMessage2(TypedDict, total=False):
    project_id: Required[int]
    """
    minimum: 0

    Required property
    """



class _StartUnmergeMessage2(TypedDict, total=False):
    project_id: Required[int]
    """
    minimum: 0

    Required property
    """



_THREAD_VALUE_MAIN_DEFAULT = None
""" Default value of the field path 'thread value main' """



_TRACE_CONTEXT_SAMPLED_DEFAULT = None
""" Default value of the field path 'trace context sampled' """



_TRACE_CONTEXT_SPAN_ID_DEFAULT = None
""" Default value of the field path 'trace context span_id' """



_TRACE_CONTEXT_TRACE_ID_DEFAULT = None
""" Default value of the field path 'trace context trace_id' """



_ThreadId = Union["_ThreadIdAnyof0", str]
""" Aggregation type: anyOf """



_ThreadIdAnyof0 = int
""" minimum: 0 """



class _ThreadValue(TypedDict, total=False):
    id: "_ThreadValueId"
    """ Aggregation type: anyOf """

    main: Union[bool, None]
    """ default: None """



_ThreadValueId = Union["_ThreadId", None]
""" Aggregation type: anyOf """



class _TraceContext(TypedDict, total=False):
    sampled: Union[bool, None]
    """ default: None """

    span_id: Union[str, None]
    """ default: None """

    trace_id: Union[str, None]
    """ default: None """

