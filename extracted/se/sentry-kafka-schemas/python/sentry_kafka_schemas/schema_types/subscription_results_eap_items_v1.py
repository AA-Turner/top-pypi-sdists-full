from typing import Required, Any, TypedDict, Literal, List, Dict


class PayloadV3(TypedDict, total=False):
    """ payload_v3. """

    subscription_id: Required[str]
    """
    minLength: 1

    Required property
    """

    request: Required[Dict[str, Any]]
    """ Required property """

    result: Required["_PayloadV3Result"]
    """ Required property """

    timestamp: Required[str]
    """ Required property """

    entity: Required[str]
    """
    minLength: 1

    Required property
    """



class SubscriptionResult(TypedDict, total=False):
    """ subscription_result. """

    version: Required[Literal[3]]
    """ Required property """

    payload: Required["PayloadV3"]
    """
    payload_v3.

    Required property
    """



class _PayloadV3Result(TypedDict, total=False):
    data: Required[List[Dict[str, Any]]]
    """ Required property """

    meta: Required[List["_PayloadV3ResultMetaItem"]]
    """ Required property """



class _PayloadV3ResultMetaItem(TypedDict, total=False):
    name: str
    type: str
