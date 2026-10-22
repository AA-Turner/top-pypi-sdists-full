from chalk._gen.buf.validate import validate_pb2 as _validate_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.quota.v1 import service_pb2 as _service_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class SignupCodeStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIGNUP_CODE_STATUS_UNSPECIFIED: _ClassVar[SignupCodeStatus]
    SIGNUP_CODE_STATUS_AVAILABLE: _ClassVar[SignupCodeStatus]
    SIGNUP_CODE_STATUS_REDEEMED: _ClassVar[SignupCodeStatus]
    SIGNUP_CODE_STATUS_CONSUMED: _ClassVar[SignupCodeStatus]
    SIGNUP_CODE_STATUS_REVOKED: _ClassVar[SignupCodeStatus]
    SIGNUP_CODE_STATUS_EXPIRED: _ClassVar[SignupCodeStatus]

class SignupCodeEmailDeliveryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIGNUP_CODE_EMAIL_DELIVERY_STATUS_UNSPECIFIED: _ClassVar[SignupCodeEmailDeliveryStatus]
    SIGNUP_CODE_EMAIL_DELIVERY_STATUS_ACCEPTED: _ClassVar[SignupCodeEmailDeliveryStatus]
    SIGNUP_CODE_EMAIL_DELIVERY_STATUS_FAILED: _ClassVar[SignupCodeEmailDeliveryStatus]

SIGNUP_CODE_STATUS_UNSPECIFIED: SignupCodeStatus
SIGNUP_CODE_STATUS_AVAILABLE: SignupCodeStatus
SIGNUP_CODE_STATUS_REDEEMED: SignupCodeStatus
SIGNUP_CODE_STATUS_CONSUMED: SignupCodeStatus
SIGNUP_CODE_STATUS_REVOKED: SignupCodeStatus
SIGNUP_CODE_STATUS_EXPIRED: SignupCodeStatus
SIGNUP_CODE_EMAIL_DELIVERY_STATUS_UNSPECIFIED: SignupCodeEmailDeliveryStatus
SIGNUP_CODE_EMAIL_DELIVERY_STATUS_ACCEPTED: SignupCodeEmailDeliveryStatus
SIGNUP_CODE_EMAIL_DELIVERY_STATUS_FAILED: SignupCodeEmailDeliveryStatus

class SignupCodeQuota(_message.Message):
    __slots__ = ("resource", "limit")
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    resource: _service_pb2.QuotaResource
    limit: _service_pb2.QuotaLimit
    def __init__(
        self,
        resource: _Optional[_Union[_service_pb2.QuotaResource, _Mapping]] = ...,
        limit: _Optional[_Union[_service_pb2.QuotaLimit, _Mapping]] = ...,
    ) -> None: ...

class SignupCodeQuotaGrant(_message.Message):
    __slots__ = ("quotas",)
    QUOTAS_FIELD_NUMBER: _ClassVar[int]
    quotas: _containers.RepeatedCompositeFieldContainer[SignupCodeQuota]
    def __init__(self, quotas: _Optional[_Iterable[_Union[SignupCodeQuota, _Mapping]]] = ...) -> None: ...

class SignupCode(_message.Message):
    __slots__ = (
        "id",
        "code_prefix",
        "note",
        "status",
        "created_by_user_id",
        "created_at",
        "expires_at",
        "revoked_at",
        "redeemed_at",
        "redeemed_by_user_id",
        "consumed_at",
        "team_id",
        "invite_message",
        "initial_quotas",
        "metadata",
        "created_by_email",
        "region",
        "recipient_email",
    )
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    CODE_PREFIX_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    REVOKED_AT_FIELD_NUMBER: _ClassVar[int]
    REDEEMED_AT_FIELD_NUMBER: _ClassVar[int]
    REDEEMED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONSUMED_AT_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    INVITE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_QUOTAS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_EMAIL_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    code_prefix: str
    note: str
    status: SignupCodeStatus
    created_by_user_id: str
    created_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    revoked_at: _timestamp_pb2.Timestamp
    redeemed_at: _timestamp_pb2.Timestamp
    redeemed_by_user_id: str
    consumed_at: _timestamp_pb2.Timestamp
    team_id: str
    invite_message: str
    initial_quotas: _containers.RepeatedCompositeFieldContainer[SignupCodeQuota]
    metadata: _containers.ScalarMap[str, str]
    created_by_email: str
    region: str
    recipient_email: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        code_prefix: _Optional[str] = ...,
        note: _Optional[str] = ...,
        status: _Optional[_Union[SignupCodeStatus, str]] = ...,
        created_by_user_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        revoked_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        redeemed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        redeemed_by_user_id: _Optional[str] = ...,
        consumed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        team_id: _Optional[str] = ...,
        invite_message: _Optional[str] = ...,
        initial_quotas: _Optional[_Iterable[_Union[SignupCodeQuota, _Mapping]]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
        created_by_email: _Optional[str] = ...,
        region: _Optional[str] = ...,
        recipient_email: _Optional[str] = ...,
    ) -> None: ...

class CreateSignupCodeRequest(_message.Message):
    __slots__ = (
        "note",
        "expires_in_seconds",
        "invite_message",
        "initial_quotas",
        "metadata",
        "region",
        "recipient_email",
    )
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NOTE_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    INVITE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_QUOTAS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    note: str
    expires_in_seconds: int
    invite_message: str
    initial_quotas: _containers.RepeatedCompositeFieldContainer[SignupCodeQuota]
    metadata: _containers.ScalarMap[str, str]
    region: str
    recipient_email: str
    def __init__(
        self,
        note: _Optional[str] = ...,
        expires_in_seconds: _Optional[int] = ...,
        invite_message: _Optional[str] = ...,
        initial_quotas: _Optional[_Iterable[_Union[SignupCodeQuota, _Mapping]]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
        region: _Optional[str] = ...,
        recipient_email: _Optional[str] = ...,
    ) -> None: ...

class CreateSignupCodeResponse(_message.Message):
    __slots__ = ("signup_code", "code", "email_delivery_status")
    SIGNUP_CODE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_DELIVERY_STATUS_FIELD_NUMBER: _ClassVar[int]
    signup_code: SignupCode
    code: str
    email_delivery_status: SignupCodeEmailDeliveryStatus
    def __init__(
        self,
        signup_code: _Optional[_Union[SignupCode, _Mapping]] = ...,
        code: _Optional[str] = ...,
        email_delivery_status: _Optional[_Union[SignupCodeEmailDeliveryStatus, str]] = ...,
    ) -> None: ...

class ListSignupCodesFilters(_message.Message):
    __slots__ = ("created_by_user_id", "created_by_email", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_EMAIL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    created_by_user_id: str
    created_by_email: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        created_by_user_id: _Optional[str] = ...,
        created_by_email: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class ListSignupCodesRequest(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: ListSignupCodesFilters
    def __init__(self, filters: _Optional[_Union[ListSignupCodesFilters, _Mapping]] = ...) -> None: ...

class ListSignupCodesResponse(_message.Message):
    __slots__ = ("signup_codes",)
    SIGNUP_CODES_FIELD_NUMBER: _ClassVar[int]
    signup_codes: _containers.RepeatedCompositeFieldContainer[SignupCode]
    def __init__(self, signup_codes: _Optional[_Iterable[_Union[SignupCode, _Mapping]]] = ...) -> None: ...

class RevokeSignupCodeRequest(_message.Message):
    __slots__ = ("signup_code_id",)
    SIGNUP_CODE_ID_FIELD_NUMBER: _ClassVar[int]
    signup_code_id: str
    def __init__(self, signup_code_id: _Optional[str] = ...) -> None: ...

class RevokeSignupCodeResponse(_message.Message):
    __slots__ = ("signup_code",)
    SIGNUP_CODE_FIELD_NUMBER: _ClassVar[int]
    signup_code: SignupCode
    def __init__(self, signup_code: _Optional[_Union[SignupCode, _Mapping]] = ...) -> None: ...

class RedeemSignupCodeRequest(_message.Message):
    __slots__ = ("user_id", "code")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    code: str
    def __init__(self, user_id: _Optional[str] = ..., code: _Optional[str] = ...) -> None: ...

class RedeemSignupCodeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PreviewSignupCodeRequest(_message.Message):
    __slots__ = ("code",)
    CODE_FIELD_NUMBER: _ClassVar[int]
    code: str
    def __init__(self, code: _Optional[str] = ...) -> None: ...

class PreviewSignupCodeResponse(_message.Message):
    __slots__ = ("redeemable", "invite_message")
    REDEEMABLE_FIELD_NUMBER: _ClassVar[int]
    INVITE_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    redeemable: bool
    invite_message: str
    def __init__(self, redeemable: bool = ..., invite_message: _Optional[str] = ...) -> None: ...

class GetSignupCodeRedemptionStatusRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetSignupCodeRedemptionStatusResponse(_message.Message):
    __slots__ = ("has_live_clearance",)
    HAS_LIVE_CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    has_live_clearance: bool
    def __init__(self, has_live_clearance: bool = ...) -> None: ...
