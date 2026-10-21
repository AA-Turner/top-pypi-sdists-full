from chalk._gen.buf.validate import validate_pb2 as _validate_pb2
from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import signup_code_pb2 as _signup_code_pb2
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

class SignupLinkStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SIGNUP_LINK_STATUS_UNSPECIFIED: _ClassVar[SignupLinkStatus]
    SIGNUP_LINK_STATUS_ACTIVE: _ClassVar[SignupLinkStatus]
    SIGNUP_LINK_STATUS_EXHAUSTED: _ClassVar[SignupLinkStatus]
    SIGNUP_LINK_STATUS_EXPIRED: _ClassVar[SignupLinkStatus]
    SIGNUP_LINK_STATUS_REVOKED: _ClassVar[SignupLinkStatus]

SIGNUP_LINK_STATUS_UNSPECIFIED: SignupLinkStatus
SIGNUP_LINK_STATUS_ACTIVE: SignupLinkStatus
SIGNUP_LINK_STATUS_EXHAUSTED: SignupLinkStatus
SIGNUP_LINK_STATUS_EXPIRED: SignupLinkStatus
SIGNUP_LINK_STATUS_REVOKED: SignupLinkStatus

class SignupLink(_message.Message):
    __slots__ = (
        "id",
        "public_id",
        "name",
        "note",
        "metadata",
        "onboarding_profile",
        "initial_quotas",
        "max_signups",
        "completed_signups",
        "status",
        "created_by_user_id",
        "created_by_email",
        "created_at",
        "expires_at",
        "revoked_at",
        "email_suffix",
        "environment_feature_flags",
        "region",
    )
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ONBOARDING_PROFILE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_QUOTAS_FIELD_NUMBER: _ClassVar[int]
    MAX_SIGNUPS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_SIGNUPS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_EMAIL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    REVOKED_AT_FIELD_NUMBER: _ClassVar[int]
    EMAIL_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    id: str
    public_id: str
    name: str
    note: str
    metadata: _containers.ScalarMap[str, str]
    onboarding_profile: str
    initial_quotas: _containers.RepeatedCompositeFieldContainer[_signup_code_pb2.SignupCodeQuota]
    max_signups: int
    completed_signups: int
    status: SignupLinkStatus
    created_by_user_id: str
    created_by_email: str
    created_at: _timestamp_pb2.Timestamp
    expires_at: _timestamp_pb2.Timestamp
    revoked_at: _timestamp_pb2.Timestamp
    email_suffix: str
    environment_feature_flags: _containers.RepeatedScalarFieldContainer[str]
    region: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        public_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        note: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
        onboarding_profile: _Optional[str] = ...,
        initial_quotas: _Optional[_Iterable[_Union[_signup_code_pb2.SignupCodeQuota, _Mapping]]] = ...,
        max_signups: _Optional[int] = ...,
        completed_signups: _Optional[int] = ...,
        status: _Optional[_Union[SignupLinkStatus, str]] = ...,
        created_by_user_id: _Optional[str] = ...,
        created_by_email: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        revoked_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        email_suffix: _Optional[str] = ...,
        environment_feature_flags: _Optional[_Iterable[str]] = ...,
        region: _Optional[str] = ...,
    ) -> None: ...

class CreateSignupLinkRequest(_message.Message):
    __slots__ = (
        "name",
        "note",
        "metadata",
        "onboarding_profile",
        "initial_quotas",
        "max_signups",
        "expires_in_seconds",
        "email_suffix",
        "environment_feature_flags",
        "region",
    )
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ONBOARDING_PROFILE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_QUOTAS_FIELD_NUMBER: _ClassVar[int]
    MAX_SIGNUPS_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    EMAIL_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    REGION_FIELD_NUMBER: _ClassVar[int]
    name: str
    note: str
    metadata: _containers.ScalarMap[str, str]
    onboarding_profile: str
    initial_quotas: _containers.RepeatedCompositeFieldContainer[_signup_code_pb2.SignupCodeQuota]
    max_signups: int
    expires_in_seconds: int
    email_suffix: str
    environment_feature_flags: _containers.RepeatedScalarFieldContainer[str]
    region: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        note: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
        onboarding_profile: _Optional[str] = ...,
        initial_quotas: _Optional[_Iterable[_Union[_signup_code_pb2.SignupCodeQuota, _Mapping]]] = ...,
        max_signups: _Optional[int] = ...,
        expires_in_seconds: _Optional[int] = ...,
        email_suffix: _Optional[str] = ...,
        environment_feature_flags: _Optional[_Iterable[str]] = ...,
        region: _Optional[str] = ...,
    ) -> None: ...

class SignupLinkFeatureFlagGrant(_message.Message):
    __slots__ = ("flags",)
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, flags: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateSignupLinkResponse(_message.Message):
    __slots__ = ("signup_link",)
    SIGNUP_LINK_FIELD_NUMBER: _ClassVar[int]
    signup_link: SignupLink
    def __init__(self, signup_link: _Optional[_Union[SignupLink, _Mapping]] = ...) -> None: ...

class ListSignupLinksRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSignupLinksResponse(_message.Message):
    __slots__ = ("signup_links",)
    SIGNUP_LINKS_FIELD_NUMBER: _ClassVar[int]
    signup_links: _containers.RepeatedCompositeFieldContainer[SignupLink]
    def __init__(self, signup_links: _Optional[_Iterable[_Union[SignupLink, _Mapping]]] = ...) -> None: ...

class UpdateSignupLinkRequest(_message.Message):
    __slots__ = ("signup_link_id", "max_signups", "expires_at", "quota_grant", "feature_flag_grant")
    SIGNUP_LINK_ID_FIELD_NUMBER: _ClassVar[int]
    MAX_SIGNUPS_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    QUOTA_GRANT_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FLAG_GRANT_FIELD_NUMBER: _ClassVar[int]
    signup_link_id: str
    max_signups: int
    expires_at: _timestamp_pb2.Timestamp
    quota_grant: _signup_code_pb2.SignupCodeQuotaGrant
    feature_flag_grant: SignupLinkFeatureFlagGrant
    def __init__(
        self,
        signup_link_id: _Optional[str] = ...,
        max_signups: _Optional[int] = ...,
        expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        quota_grant: _Optional[_Union[_signup_code_pb2.SignupCodeQuotaGrant, _Mapping]] = ...,
        feature_flag_grant: _Optional[_Union[SignupLinkFeatureFlagGrant, _Mapping]] = ...,
    ) -> None: ...

class UpdateSignupLinkResponse(_message.Message):
    __slots__ = ("signup_link",)
    SIGNUP_LINK_FIELD_NUMBER: _ClassVar[int]
    signup_link: SignupLink
    def __init__(self, signup_link: _Optional[_Union[SignupLink, _Mapping]] = ...) -> None: ...

class RevokeSignupLinkRequest(_message.Message):
    __slots__ = ("signup_link_id",)
    SIGNUP_LINK_ID_FIELD_NUMBER: _ClassVar[int]
    signup_link_id: str
    def __init__(self, signup_link_id: _Optional[str] = ...) -> None: ...

class RevokeSignupLinkResponse(_message.Message):
    __slots__ = ("signup_link",)
    SIGNUP_LINK_FIELD_NUMBER: _ClassVar[int]
    signup_link: SignupLink
    def __init__(self, signup_link: _Optional[_Union[SignupLink, _Mapping]] = ...) -> None: ...

class SignupLinkRedemption(_message.Message):
    __slots__ = ("id", "user_id", "team_id", "project_id", "team_name", "team_exists", "created_at", "user_email")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    TEAM_EXISTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    team_id: str
    project_id: str
    team_name: str
    team_exists: bool
    created_at: _timestamp_pb2.Timestamp
    user_email: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        user_id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        project_id: _Optional[str] = ...,
        team_name: _Optional[str] = ...,
        team_exists: bool = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        user_email: _Optional[str] = ...,
    ) -> None: ...

class ListSignupLinkRedemptionsFilters(_message.Message):
    __slots__ = ("signup_link_id",)
    SIGNUP_LINK_ID_FIELD_NUMBER: _ClassVar[int]
    signup_link_id: str
    def __init__(self, signup_link_id: _Optional[str] = ...) -> None: ...

class ListSignupLinkRedemptionsRequest(_message.Message):
    __slots__ = ("filters",)
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: ListSignupLinkRedemptionsFilters
    def __init__(self, filters: _Optional[_Union[ListSignupLinkRedemptionsFilters, _Mapping]] = ...) -> None: ...

class ListSignupLinkRedemptionsResponse(_message.Message):
    __slots__ = ("redemptions",)
    REDEMPTIONS_FIELD_NUMBER: _ClassVar[int]
    redemptions: _containers.RepeatedCompositeFieldContainer[SignupLinkRedemption]
    def __init__(self, redemptions: _Optional[_Iterable[_Union[SignupLinkRedemption, _Mapping]]] = ...) -> None: ...

class PreviewSignupLinkRequest(_message.Message):
    __slots__ = ("public_id",)
    PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    public_id: str
    def __init__(self, public_id: _Optional[str] = ...) -> None: ...

class PreviewSignupLinkResponse(_message.Message):
    __slots__ = ("available", "name", "signup_slug")
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_SLUG_FIELD_NUMBER: _ClassVar[int]
    available: bool
    name: str
    signup_slug: str
    def __init__(
        self, available: bool = ..., name: _Optional[str] = ..., signup_slug: _Optional[str] = ...
    ) -> None: ...

class StartSignupLinkAttemptRequest(_message.Message):
    __slots__ = ("public_id", "signup_slug")
    PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_SLUG_FIELD_NUMBER: _ClassVar[int]
    public_id: str
    signup_slug: str
    def __init__(self, public_id: _Optional[str] = ..., signup_slug: _Optional[str] = ...) -> None: ...

class StartSignupLinkAttemptResponse(_message.Message):
    __slots__ = ("token", "signup_slug")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_SLUG_FIELD_NUMBER: _ClassVar[int]
    token: str
    signup_slug: str
    def __init__(self, token: _Optional[str] = ..., signup_slug: _Optional[str] = ...) -> None: ...

class BindSignupLinkAttemptRequest(_message.Message):
    __slots__ = ("token", "user_id", "authentication_provider")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_PROVIDER_FIELD_NUMBER: _ClassVar[int]
    token: str
    user_id: str
    authentication_provider: str
    def __init__(
        self, token: _Optional[str] = ..., user_id: _Optional[str] = ..., authentication_provider: _Optional[str] = ...
    ) -> None: ...

class BindSignupLinkAttemptResponse(_message.Message):
    __slots__ = ("context", "required_email_suffix")
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_EMAIL_SUFFIX_FIELD_NUMBER: _ClassVar[int]
    context: SignupLinkContext
    required_email_suffix: str
    def __init__(
        self, context: _Optional[_Union[SignupLinkContext, _Mapping]] = ..., required_email_suffix: _Optional[str] = ...
    ) -> None: ...

class SignupLinkContext(_message.Message):
    __slots__ = (
        "signup_link_id",
        "name",
        "onboarding_profile",
        "attempt_id",
        "can_create_team",
        "public_id",
        "signup_slug",
    )
    SIGNUP_LINK_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ONBOARDING_PROFILE_FIELD_NUMBER: _ClassVar[int]
    ATTEMPT_ID_FIELD_NUMBER: _ClassVar[int]
    CAN_CREATE_TEAM_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    SIGNUP_SLUG_FIELD_NUMBER: _ClassVar[int]
    signup_link_id: str
    name: str
    onboarding_profile: str
    attempt_id: str
    can_create_team: bool
    public_id: str
    signup_slug: str
    def __init__(
        self,
        signup_link_id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        onboarding_profile: _Optional[str] = ...,
        attempt_id: _Optional[str] = ...,
        can_create_team: bool = ...,
        public_id: _Optional[str] = ...,
        signup_slug: _Optional[str] = ...,
    ) -> None: ...

class GetSignupLinkContextRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class GetSignupLinkContextResponse(_message.Message):
    __slots__ = ("context",)
    CONTEXT_FIELD_NUMBER: _ClassVar[int]
    context: SignupLinkContext
    def __init__(self, context: _Optional[_Union[SignupLinkContext, _Mapping]] = ...) -> None: ...

class SignupLinkSlug(_message.Message):
    __slots__ = ("slug", "public_id", "created_by_user_id", "created_by_email", "created_at")
    SLUG_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_BY_EMAIL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    slug: str
    public_id: str
    created_by_user_id: str
    created_by_email: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        slug: _Optional[str] = ...,
        public_id: _Optional[str] = ...,
        created_by_user_id: _Optional[str] = ...,
        created_by_email: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class CreateSignupLinkSlugRequest(_message.Message):
    __slots__ = ("slug", "public_id")
    SLUG_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    slug: str
    public_id: str
    def __init__(self, slug: _Optional[str] = ..., public_id: _Optional[str] = ...) -> None: ...

class CreateSignupLinkSlugResponse(_message.Message):
    __slots__ = ("association",)
    ASSOCIATION_FIELD_NUMBER: _ClassVar[int]
    association: SignupLinkSlug
    def __init__(self, association: _Optional[_Union[SignupLinkSlug, _Mapping]] = ...) -> None: ...

class UpdateSignupLinkSlugRequest(_message.Message):
    __slots__ = ("slug", "public_id")
    SLUG_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    slug: str
    public_id: str
    def __init__(self, slug: _Optional[str] = ..., public_id: _Optional[str] = ...) -> None: ...

class UpdateSignupLinkSlugResponse(_message.Message):
    __slots__ = ("association",)
    ASSOCIATION_FIELD_NUMBER: _ClassVar[int]
    association: SignupLinkSlug
    def __init__(self, association: _Optional[_Union[SignupLinkSlug, _Mapping]] = ...) -> None: ...

class DeleteSignupLinkSlugRequest(_message.Message):
    __slots__ = ("slug",)
    SLUG_FIELD_NUMBER: _ClassVar[int]
    slug: str
    def __init__(self, slug: _Optional[str] = ...) -> None: ...

class DeleteSignupLinkSlugResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSignupLinkSlugsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListSignupLinkSlugsResponse(_message.Message):
    __slots__ = ("associations",)
    ASSOCIATIONS_FIELD_NUMBER: _ClassVar[int]
    associations: _containers.RepeatedCompositeFieldContainer[SignupLinkSlug]
    def __init__(self, associations: _Optional[_Iterable[_Union[SignupLinkSlug, _Mapping]]] = ...) -> None: ...

class ResolveSignupLinkSlugRequest(_message.Message):
    __slots__ = ("slug",)
    SLUG_FIELD_NUMBER: _ClassVar[int]
    slug: str
    def __init__(self, slug: _Optional[str] = ...) -> None: ...

class ResolveSignupLinkSlugResponse(_message.Message):
    __slots__ = ("public_id",)
    PUBLIC_ID_FIELD_NUMBER: _ClassVar[int]
    public_id: str
    def __init__(self, public_id: _Optional[str] = ...) -> None: ...
