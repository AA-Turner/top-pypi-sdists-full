from typing import List, Any, Required, TypedDict, Dict


class _Root(TypedDict, total=False):
    version: Required[int]
    """ Required property """

    payload: Required["_RootPayload"]
    """ Required property """



class _RootPayload(TypedDict, total=False):
    subscription_id: Required[str]
    """ Required property """

    request: Required[Dict[str, Any]]
    """ Required property """

    result: Required["_RootPayloadResult"]
    """ Required property """

    timestamp: Required[str]
    """ Required property """

    entity: Required[str]
    """ Required property """



class _RootPayloadResult(TypedDict, total=False):
    data: Required[List[Dict[str, Any]]]
    """ Required property """

    meta: Required[List[Any]]
    """ Required property """

