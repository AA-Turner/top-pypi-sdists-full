from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
ONBOARDING_STATUS_COMPLETED: OnboardingStatusEnum
ONBOARDING_STATUS_INCOMPLETE: OnboardingStatusEnum
ONBOARDING_STATUS_UNSPECIFIED: OnboardingStatusEnum
TASK_STATUS_FAILED: DataPlatformSetupTaskStatusEnum
TASK_STATUS_NOT_STARTED: DataPlatformSetupTaskStatusEnum
TASK_STATUS_RUNNING: DataPlatformSetupTaskStatusEnum
TASK_STATUS_SUCCEEDED: DataPlatformSetupTaskStatusEnum
TASK_STATUS_UNKNOWN: DataPlatformSetupTaskStatusEnum

class DataPlatformSetupTaskStatus(_message.Message):
    __slots__ = ["details", "error_message", "task_display_name", "task_status"]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TASK_DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    TASK_STATUS_FIELD_NUMBER: _ClassVar[int]
    details: str
    error_message: str
    task_display_name: str
    task_status: DataPlatformSetupTaskStatusEnum
    def __init__(self, task_display_name: _Optional[str] = ..., task_status: _Optional[_Union[DataPlatformSetupTaskStatusEnum, str]] = ..., error_message: _Optional[str] = ..., details: _Optional[str] = ...) -> None: ...

class OnboardingStatus(_message.Message):
    __slots__ = ["status", "user_id"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    status: OnboardingStatusEnum
    user_id: str
    def __init__(self, user_id: _Optional[str] = ..., status: _Optional[_Union[OnboardingStatusEnum, str]] = ...) -> None: ...

class OnboardingStatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DataPlatformSetupTaskStatusEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
