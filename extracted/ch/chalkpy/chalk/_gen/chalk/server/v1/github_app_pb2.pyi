from chalk._gen.chalk.auth.v1 import audit_pb2 as _audit_pb2
from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.utils.v1 import sensitive_pb2 as _sensitive_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
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

class GitHubAppConfig(_message.Message):
    __slots__ = (
        "id",
        "team_id",
        "app_id",
        "app_slug",
        "client_id",
        "private_key_secret_id",
        "webhook_secret_id",
        "client_secret_id",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SLUG_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    app_id: int
    app_slug: str
    client_id: str
    private_key_secret_id: str
    webhook_secret_id: str
    client_secret_id: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        app_id: _Optional[int] = ...,
        app_slug: _Optional[str] = ...,
        client_id: _Optional[str] = ...,
        private_key_secret_id: _Optional[str] = ...,
        webhook_secret_id: _Optional[str] = ...,
        client_secret_id: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GitHubAppInstallation(_message.Message):
    __slots__ = (
        "id",
        "team_id",
        "installation_id",
        "account_login",
        "account_type",
        "repository_selection",
        "avatar_url",
        "installed_by_user_id",
        "suspended_at",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_LOGIN_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_TYPE_FIELD_NUMBER: _ClassVar[int]
    REPOSITORY_SELECTION_FIELD_NUMBER: _ClassVar[int]
    AVATAR_URL_FIELD_NUMBER: _ClassVar[int]
    INSTALLED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    installation_id: int
    account_login: str
    account_type: str
    repository_selection: str
    avatar_url: str
    installed_by_user_id: str
    suspended_at: _timestamp_pb2.Timestamp
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        installation_id: _Optional[int] = ...,
        account_login: _Optional[str] = ...,
        account_type: _Optional[str] = ...,
        repository_selection: _Optional[str] = ...,
        avatar_url: _Optional[str] = ...,
        installed_by_user_id: _Optional[str] = ...,
        suspended_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GitHubRepository(_message.Message):
    __slots__ = ("id", "name", "full_name", "owner", "private", "default_branch", "html_url")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BRANCH_FIELD_NUMBER: _ClassVar[int]
    HTML_URL_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    full_name: str
    owner: str
    private: bool
    default_branch: str
    html_url: str
    def __init__(
        self,
        id: _Optional[int] = ...,
        name: _Optional[str] = ...,
        full_name: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        private: bool = ...,
        default_branch: _Optional[str] = ...,
        html_url: _Optional[str] = ...,
    ) -> None: ...

class GitHubPullRequest(_message.Message):
    __slots__ = (
        "id",
        "number",
        "title",
        "state",
        "html_url",
        "user_login",
        "head_ref",
        "base_ref",
        "created_at",
        "updated_at",
        "merged_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    HTML_URL_FIELD_NUMBER: _ClassVar[int]
    USER_LOGIN_FIELD_NUMBER: _ClassVar[int]
    HEAD_REF_FIELD_NUMBER: _ClassVar[int]
    BASE_REF_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    MERGED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    number: int
    title: str
    state: str
    html_url: str
    user_login: str
    head_ref: str
    base_ref: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    merged_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[int] = ...,
        number: _Optional[int] = ...,
        title: _Optional[str] = ...,
        state: _Optional[str] = ...,
        html_url: _Optional[str] = ...,
        user_login: _Optional[str] = ...,
        head_ref: _Optional[str] = ...,
        base_ref: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        merged_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class UpsertGitHubAppConfigRequest(_message.Message):
    __slots__ = ("app_id", "app_slug", "client_id", "private_key", "webhook_secret", "client_secret")
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    APP_SLUG_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    PRIVATE_KEY_FIELD_NUMBER: _ClassVar[int]
    WEBHOOK_SECRET_FIELD_NUMBER: _ClassVar[int]
    CLIENT_SECRET_FIELD_NUMBER: _ClassVar[int]
    app_id: int
    app_slug: str
    client_id: str
    private_key: str
    webhook_secret: str
    client_secret: str
    def __init__(
        self,
        app_id: _Optional[int] = ...,
        app_slug: _Optional[str] = ...,
        client_id: _Optional[str] = ...,
        private_key: _Optional[str] = ...,
        webhook_secret: _Optional[str] = ...,
        client_secret: _Optional[str] = ...,
    ) -> None: ...

class UpsertGitHubAppConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: GitHubAppConfig
    def __init__(self, config: _Optional[_Union[GitHubAppConfig, _Mapping]] = ...) -> None: ...

class GetGitHubAppConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetGitHubAppConfigResponse(_message.Message):
    __slots__ = ("config",)
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    config: GitHubAppConfig
    def __init__(self, config: _Optional[_Union[GitHubAppConfig, _Mapping]] = ...) -> None: ...

class DeleteGitHubAppConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeleteGitHubAppConfigResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetGitHubAppInstallUrlRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetGitHubAppInstallUrlResponse(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class CompleteGitHubAppInstallationRequest(_message.Message):
    __slots__ = ("installation_id", "setup_action")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    SETUP_ACTION_FIELD_NUMBER: _ClassVar[int]
    installation_id: int
    setup_action: str
    def __init__(self, installation_id: _Optional[int] = ..., setup_action: _Optional[str] = ...) -> None: ...

class CompleteGitHubAppInstallationResponse(_message.Message):
    __slots__ = ("installation",)
    INSTALLATION_FIELD_NUMBER: _ClassVar[int]
    installation: GitHubAppInstallation
    def __init__(self, installation: _Optional[_Union[GitHubAppInstallation, _Mapping]] = ...) -> None: ...

class ListGitHubAppInstallationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListGitHubAppInstallationsResponse(_message.Message):
    __slots__ = ("installations",)
    INSTALLATIONS_FIELD_NUMBER: _ClassVar[int]
    installations: _containers.RepeatedCompositeFieldContainer[GitHubAppInstallation]
    def __init__(self, installations: _Optional[_Iterable[_Union[GitHubAppInstallation, _Mapping]]] = ...) -> None: ...

class DeleteGitHubAppInstallationRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeleteGitHubAppInstallationResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SyncGitHubAppInstallationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SyncGitHubAppInstallationsResponse(_message.Message):
    __slots__ = ("installations",)
    INSTALLATIONS_FIELD_NUMBER: _ClassVar[int]
    installations: _containers.RepeatedCompositeFieldContainer[GitHubAppInstallation]
    def __init__(self, installations: _Optional[_Iterable[_Union[GitHubAppInstallation, _Mapping]]] = ...) -> None: ...

class ListGitHubRepositoriesRequest(_message.Message):
    __slots__ = ("installation_id", "page", "per_page")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    installation_id: str
    page: int
    per_page: int
    def __init__(
        self, installation_id: _Optional[str] = ..., page: _Optional[int] = ..., per_page: _Optional[int] = ...
    ) -> None: ...

class ListGitHubRepositoriesResponse(_message.Message):
    __slots__ = ("repositories",)
    REPOSITORIES_FIELD_NUMBER: _ClassVar[int]
    repositories: _containers.RepeatedCompositeFieldContainer[GitHubRepository]
    def __init__(self, repositories: _Optional[_Iterable[_Union[GitHubRepository, _Mapping]]] = ...) -> None: ...

class ListGitHubPullRequestsRequest(_message.Message):
    __slots__ = ("installation_id", "owner", "repo", "state", "page", "per_page")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    installation_id: str
    owner: str
    repo: str
    state: str
    page: int
    per_page: int
    def __init__(
        self,
        installation_id: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        repo: _Optional[str] = ...,
        state: _Optional[str] = ...,
        page: _Optional[int] = ...,
        per_page: _Optional[int] = ...,
    ) -> None: ...

class ListGitHubPullRequestsResponse(_message.Message):
    __slots__ = ("pull_requests",)
    PULL_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    pull_requests: _containers.RepeatedCompositeFieldContainer[GitHubPullRequest]
    def __init__(self, pull_requests: _Optional[_Iterable[_Union[GitHubPullRequest, _Mapping]]] = ...) -> None: ...
