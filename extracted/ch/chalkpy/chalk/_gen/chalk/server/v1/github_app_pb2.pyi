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

class GitHubProjectRepoLink(_message.Message):
    __slots__ = (
        "id",
        "team_id",
        "project_id",
        "installation_id",
        "repo_owner",
        "repo_name",
        "default_branch",
        "created_at",
        "updated_at",
    )
    ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    REPO_OWNER_FIELD_NUMBER: _ClassVar[int]
    REPO_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BRANCH_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    team_id: str
    project_id: str
    installation_id: str
    repo_owner: str
    repo_name: str
    default_branch: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        id: _Optional[str] = ...,
        team_id: _Optional[str] = ...,
        project_id: _Optional[str] = ...,
        installation_id: _Optional[str] = ...,
        repo_owner: _Optional[str] = ...,
        repo_name: _Optional[str] = ...,
        default_branch: _Optional[str] = ...,
        created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GitHubBranch(_message.Message):
    __slots__ = ("name", "commit_sha", "protected")
    NAME_FIELD_NUMBER: _ClassVar[int]
    COMMIT_SHA_FIELD_NUMBER: _ClassVar[int]
    PROTECTED_FIELD_NUMBER: _ClassVar[int]
    name: str
    commit_sha: str
    protected: bool
    def __init__(self, name: _Optional[str] = ..., commit_sha: _Optional[str] = ..., protected: bool = ...) -> None: ...

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
    __slots__ = ("project_id", "environment_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    environment_id: str
    def __init__(self, project_id: _Optional[str] = ..., environment_id: _Optional[str] = ...) -> None: ...

class GetGitHubAppInstallUrlResponse(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class CompleteGitHubAppInstallationRequest(_message.Message):
    __slots__ = ("installation_id", "setup_action", "state")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    SETUP_ACTION_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    installation_id: int
    setup_action: str
    state: str
    def __init__(
        self, installation_id: _Optional[int] = ..., setup_action: _Optional[str] = ..., state: _Optional[str] = ...
    ) -> None: ...

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
    __slots__ = ("installations", "removed_account_logins")
    INSTALLATIONS_FIELD_NUMBER: _ClassVar[int]
    REMOVED_ACCOUNT_LOGINS_FIELD_NUMBER: _ClassVar[int]
    installations: _containers.RepeatedCompositeFieldContainer[GitHubAppInstallation]
    removed_account_logins: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        installations: _Optional[_Iterable[_Union[GitHubAppInstallation, _Mapping]]] = ...,
        removed_account_logins: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

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

class LinkProjectToGitHubRepositoryRequest(_message.Message):
    __slots__ = ("project_id", "installation_id", "repo_owner", "repo_name", "default_branch")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    REPO_OWNER_FIELD_NUMBER: _ClassVar[int]
    REPO_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_BRANCH_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    installation_id: str
    repo_owner: str
    repo_name: str
    default_branch: str
    def __init__(
        self,
        project_id: _Optional[str] = ...,
        installation_id: _Optional[str] = ...,
        repo_owner: _Optional[str] = ...,
        repo_name: _Optional[str] = ...,
        default_branch: _Optional[str] = ...,
    ) -> None: ...

class LinkProjectToGitHubRepositoryResponse(_message.Message):
    __slots__ = ("link",)
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: GitHubProjectRepoLink
    def __init__(self, link: _Optional[_Union[GitHubProjectRepoLink, _Mapping]] = ...) -> None: ...

class UnlinkProjectFromGitHubRepositoryRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class UnlinkProjectFromGitHubRepositoryResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetProjectGitHubRepoLinkRequest(_message.Message):
    __slots__ = ("project_id",)
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    def __init__(self, project_id: _Optional[str] = ...) -> None: ...

class GetProjectGitHubRepoLinkResponse(_message.Message):
    __slots__ = ("link",)
    LINK_FIELD_NUMBER: _ClassVar[int]
    link: GitHubProjectRepoLink
    def __init__(self, link: _Optional[_Union[GitHubProjectRepoLink, _Mapping]] = ...) -> None: ...

class ListProjectGitHubRepoLinksRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListProjectGitHubRepoLinksResponse(_message.Message):
    __slots__ = ("links",)
    LINKS_FIELD_NUMBER: _ClassVar[int]
    links: _containers.RepeatedCompositeFieldContainer[GitHubProjectRepoLink]
    def __init__(self, links: _Optional[_Iterable[_Union[GitHubProjectRepoLink, _Mapping]]] = ...) -> None: ...

class ListGitHubBranchesRequest(_message.Message):
    __slots__ = ("installation_id", "owner", "repo", "page", "per_page")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PER_PAGE_FIELD_NUMBER: _ClassVar[int]
    installation_id: str
    owner: str
    repo: str
    page: int
    per_page: int
    def __init__(
        self,
        installation_id: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        repo: _Optional[str] = ...,
        page: _Optional[int] = ...,
        per_page: _Optional[int] = ...,
    ) -> None: ...

class ListGitHubBranchesResponse(_message.Message):
    __slots__ = ("branches",)
    BRANCHES_FIELD_NUMBER: _ClassVar[int]
    branches: _containers.RepeatedCompositeFieldContainer[GitHubBranch]
    def __init__(self, branches: _Optional[_Iterable[_Union[GitHubBranch, _Mapping]]] = ...) -> None: ...

class GetGitHubRepositoryArchiveRequest(_message.Message):
    __slots__ = ("installation_id", "owner", "repo", "ref")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    installation_id: str
    owner: str
    repo: str
    ref: str
    def __init__(
        self,
        installation_id: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        repo: _Optional[str] = ...,
        ref: _Optional[str] = ...,
    ) -> None: ...

class GetGitHubRepositoryArchiveResponse(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class RepoFileChangeInput(_message.Message):
    __slots__ = ("path", "content", "delete", "mode")
    PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    DELETE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    path: str
    content: bytes
    delete: bool
    mode: str
    def __init__(
        self,
        path: _Optional[str] = ...,
        content: _Optional[bytes] = ...,
        delete: bool = ...,
        mode: _Optional[str] = ...,
    ) -> None: ...

class CreatePullRequestFromChangesRequest(_message.Message):
    __slots__ = ("installation_id", "owner", "repo", "base_branch", "head_branch", "title", "body", "draft", "changes")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    BASE_BRANCH_FIELD_NUMBER: _ClassVar[int]
    HEAD_BRANCH_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    BODY_FIELD_NUMBER: _ClassVar[int]
    DRAFT_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    installation_id: str
    owner: str
    repo: str
    base_branch: str
    head_branch: str
    title: str
    body: str
    draft: bool
    changes: _containers.RepeatedCompositeFieldContainer[RepoFileChangeInput]
    def __init__(
        self,
        installation_id: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        repo: _Optional[str] = ...,
        base_branch: _Optional[str] = ...,
        head_branch: _Optional[str] = ...,
        title: _Optional[str] = ...,
        body: _Optional[str] = ...,
        draft: bool = ...,
        changes: _Optional[_Iterable[_Union[RepoFileChangeInput, _Mapping]]] = ...,
    ) -> None: ...

class CreatePullRequestFromChangesResponse(_message.Message):
    __slots__ = ("html_url", "number", "head_branch")
    HTML_URL_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    HEAD_BRANCH_FIELD_NUMBER: _ClassVar[int]
    html_url: str
    number: int
    head_branch: str
    def __init__(
        self, html_url: _Optional[str] = ..., number: _Optional[int] = ..., head_branch: _Optional[str] = ...
    ) -> None: ...

class CreateVolumeFromGitHubRepoRequest(_message.Message):
    __slots__ = ("installation_id", "owner", "repo", "ref", "volume_name")
    INSTALLATION_ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    VOLUME_NAME_FIELD_NUMBER: _ClassVar[int]
    installation_id: str
    owner: str
    repo: str
    ref: str
    volume_name: str
    def __init__(
        self,
        installation_id: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        repo: _Optional[str] = ...,
        ref: _Optional[str] = ...,
        volume_name: _Optional[str] = ...,
    ) -> None: ...

class CreateVolumeFromGitHubRepoResponse(_message.Message):
    __slots__ = ("volume_name", "volume_id", "files", "bytes")
    VOLUME_NAME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_ID_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    volume_name: str
    volume_id: str
    files: int
    bytes: int
    def __init__(
        self,
        volume_name: _Optional[str] = ...,
        volume_id: _Optional[str] = ...,
        files: _Optional[int] = ...,
        bytes: _Optional[int] = ...,
    ) -> None: ...
