from typing import Required, TypedDict


class _Root(TypedDict, total=False):
    android_api_level: int
    architecture: str
    device_classification: str
    device_locale: Required[str]
    """ Required property """

    device_manufacturer: Required[str]
    """ Required property """

    device_model: Required[str]
    """ Required property """

    device_os_build_number: str
    device_os_name: Required[str]
    """ Required property """

    device_os_version: Required[str]
    """ Required property """

    duration_ns: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    environment: str
    profile_id: Required[str]
    """ Required property """

    organization_id: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    platform: Required[str]
    """ Required property """

    project_id: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    received: Required[int]
    """ Required property """

    retention_days: Required[int]
    """ Required property """

    trace_id: Required[str]
    """ Required property """

    transaction_id: Required[str]
    """ Required property """

    transaction_name: Required[str]
    """ Required property """

    version_code: Required[str]
    """ Required property """

    version_name: Required[str]
    """ Required property """



_Uint = int
""" minimum: 0 """

