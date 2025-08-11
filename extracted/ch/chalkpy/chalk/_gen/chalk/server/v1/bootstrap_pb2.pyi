from chalk._gen.chalk.server.v1 import environment_pb2 as _environment_pb2
from chalk._gen.chalk.server.v1 import team_pb2 as _team_pb2
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

class BootstrapExtraSettingsEnvironment(_message.Message):
    __slots__ = ("settings",)
    class SettingsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...

    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    settings: _containers.ScalarMap[str, bool]
    def __init__(self, settings: _Optional[_Mapping[str, bool]] = ...) -> None: ...

class BootstrapExtraSettings(_message.Message):
    __slots__ = ("environments",)
    class GlobalEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bool
        def __init__(self, key: _Optional[str] = ..., value: bool = ...) -> None: ...

    class EnvironmentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: BootstrapExtraSettingsEnvironment
        def __init__(
            self, key: _Optional[str] = ..., value: _Optional[_Union[BootstrapExtraSettingsEnvironment, _Mapping]] = ...
        ) -> None: ...

    GLOBAL_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    environments: _containers.MessageMap[str, BootstrapExtraSettingsEnvironment]
    def __init__(
        self, environments: _Optional[_Mapping[str, BootstrapExtraSettingsEnvironment]] = ..., **kwargs
    ) -> None: ...

class ParsedBootstrapConfigs(_message.Message):
    __slots__ = ("teams", "projects", "environments", "team_invites", "extra_settings", "global_pinned_base_image")
    TEAMS_FIELD_NUMBER: _ClassVar[int]
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    TEAM_INVITES_FIELD_NUMBER: _ClassVar[int]
    EXTRA_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_PINNED_BASE_IMAGE_FIELD_NUMBER: _ClassVar[int]
    teams: _containers.RepeatedCompositeFieldContainer[_team_pb2.Team]
    projects: _containers.RepeatedCompositeFieldContainer[_team_pb2.Project]
    environments: _containers.RepeatedCompositeFieldContainer[_environment_pb2.Environment]
    team_invites: _containers.RepeatedCompositeFieldContainer[_team_pb2.TeamInvite]
    extra_settings: BootstrapExtraSettings
    global_pinned_base_image: str
    def __init__(
        self,
        teams: _Optional[_Iterable[_Union[_team_pb2.Team, _Mapping]]] = ...,
        projects: _Optional[_Iterable[_Union[_team_pb2.Project, _Mapping]]] = ...,
        environments: _Optional[_Iterable[_Union[_environment_pb2.Environment, _Mapping]]] = ...,
        team_invites: _Optional[_Iterable[_Union[_team_pb2.TeamInvite, _Mapping]]] = ...,
        extra_settings: _Optional[_Union[BootstrapExtraSettings, _Mapping]] = ...,
        global_pinned_base_image: _Optional[str] = ...,
    ) -> None: ...
