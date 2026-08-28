from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import flag_pb2 as _flag_pb2
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

class FlagPredicate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FLAG_PREDICATE_UNSPECIFIED: _ClassVar[FlagPredicate]
    FLAG_PREDICATE_IS_TRUE: _ClassVar[FlagPredicate]
    FLAG_PREDICATE_IS_TRUE_OR_UNSET: _ClassVar[FlagPredicate]
    FLAG_PREDICATE_IS_FALSE_OR_UNSET: _ClassVar[FlagPredicate]

class EnvVarPredicate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENV_VAR_PREDICATE_UNSPECIFIED: _ClassVar[EnvVarPredicate]
    ENV_VAR_PREDICATE_IS_TRUTHY: _ClassVar[EnvVarPredicate]
    ENV_VAR_PREDICATE_IS_FALSY_OR_UNSET: _ClassVar[EnvVarPredicate]
    ENV_VAR_PREDICATE_IS_SET: _ClassVar[EnvVarPredicate]
    ENV_VAR_PREDICATE_IS_UNSET: _ClassVar[EnvVarPredicate]
    ENV_VAR_PREDICATE_EQUALS_ANY: _ClassVar[EnvVarPredicate]
    ENV_VAR_PREDICATE_IS_TRUTHY_OR_UNSET: _ClassVar[EnvVarPredicate]

class RuntimePredicate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RUNTIME_PREDICATE_UNSPECIFIED: _ClassVar[RuntimePredicate]
    RUNTIME_PREDICATE_EQUALS_ANY: _ClassVar[RuntimePredicate]
    RUNTIME_PREDICATE_NOT_EQUALS_ANY: _ClassVar[RuntimePredicate]

class EnvironmentMigrationState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ENVIRONMENT_MIGRATION_STATE_UNSPECIFIED: _ClassVar[EnvironmentMigrationState]
    ENVIRONMENT_MIGRATION_STATE_MIGRATED: _ClassVar[EnvironmentMigrationState]
    ENVIRONMENT_MIGRATION_STATE_UNMIGRATED: _ClassVar[EnvironmentMigrationState]

FLAG_PREDICATE_UNSPECIFIED: FlagPredicate
FLAG_PREDICATE_IS_TRUE: FlagPredicate
FLAG_PREDICATE_IS_TRUE_OR_UNSET: FlagPredicate
FLAG_PREDICATE_IS_FALSE_OR_UNSET: FlagPredicate
ENV_VAR_PREDICATE_UNSPECIFIED: EnvVarPredicate
ENV_VAR_PREDICATE_IS_TRUTHY: EnvVarPredicate
ENV_VAR_PREDICATE_IS_FALSY_OR_UNSET: EnvVarPredicate
ENV_VAR_PREDICATE_IS_SET: EnvVarPredicate
ENV_VAR_PREDICATE_IS_UNSET: EnvVarPredicate
ENV_VAR_PREDICATE_EQUALS_ANY: EnvVarPredicate
ENV_VAR_PREDICATE_IS_TRUTHY_OR_UNSET: EnvVarPredicate
RUNTIME_PREDICATE_UNSPECIFIED: RuntimePredicate
RUNTIME_PREDICATE_EQUALS_ANY: RuntimePredicate
RUNTIME_PREDICATE_NOT_EQUALS_ANY: RuntimePredicate
ENVIRONMENT_MIGRATION_STATE_UNSPECIFIED: EnvironmentMigrationState
ENVIRONMENT_MIGRATION_STATE_MIGRATED: EnvironmentMigrationState
ENVIRONMENT_MIGRATION_STATE_UNMIGRATED: EnvironmentMigrationState

class FlagCriterion(_message.Message):
    __slots__ = ("flag", "predicate")
    FLAG_FIELD_NUMBER: _ClassVar[int]
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    flag: str
    predicate: FlagPredicate
    def __init__(self, flag: _Optional[str] = ..., predicate: _Optional[_Union[FlagPredicate, str]] = ...) -> None: ...

class EnvVarCriterion(_message.Message):
    __slots__ = ("key", "predicate", "values")
    KEY_FIELD_NUMBER: _ClassVar[int]
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    key: str
    predicate: EnvVarPredicate
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        key: _Optional[str] = ...,
        predicate: _Optional[_Union[EnvVarPredicate, str]] = ...,
        values: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class RuntimeCriterion(_message.Message):
    __slots__ = ("predicate", "values")
    PREDICATE_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    predicate: RuntimePredicate
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, predicate: _Optional[_Union[RuntimePredicate, str]] = ..., values: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class MigrationCriterion(_message.Message):
    __slots__ = ("description", "flag", "env_var", "runtime")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FLAG_FIELD_NUMBER: _ClassVar[int]
    ENV_VAR_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    description: str
    flag: FlagCriterion
    env_var: EnvVarCriterion
    runtime: RuntimeCriterion
    def __init__(
        self,
        description: _Optional[str] = ...,
        flag: _Optional[_Union[FlagCriterion, _Mapping]] = ...,
        env_var: _Optional[_Union[EnvVarCriterion, _Mapping]] = ...,
        runtime: _Optional[_Union[RuntimeCriterion, _Mapping]] = ...,
    ) -> None: ...

class Migration(_message.Message):
    __slots__ = ("id", "name", "description", "owner", "ticket", "criteria")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    CRITERIA_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    owner: str
    ticket: str
    criteria: _containers.RepeatedCompositeFieldContainer[MigrationCriterion]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        ticket: _Optional[str] = ...,
        criteria: _Optional[_Iterable[_Union[MigrationCriterion, _Mapping]]] = ...,
    ) -> None: ...

class ObservedFlagState(_message.Message):
    __slots__ = ("is_set", "value", "scope", "updated_at")
    IS_SET_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SCOPE_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    is_set: bool
    value: bool
    scope: _flag_pb2.FlagScope
    updated_at: _timestamp_pb2.Timestamp
    def __init__(
        self,
        is_set: bool = ...,
        value: bool = ...,
        scope: _Optional[_Union[_flag_pb2.FlagScope, str]] = ...,
        updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class ObservedEnvVarState(_message.Message):
    __slots__ = ("is_set", "value", "redacted")
    IS_SET_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    REDACTED_FIELD_NUMBER: _ClassVar[int]
    is_set: bool
    value: str
    redacted: bool
    def __init__(self, is_set: bool = ..., value: _Optional[str] = ..., redacted: bool = ...) -> None: ...

class ObservedRuntimeState(_message.Message):
    __slots__ = ("has_active_deployment", "value")
    HAS_ACTIVE_DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    has_active_deployment: bool
    value: str
    def __init__(self, has_active_deployment: bool = ..., value: _Optional[str] = ...) -> None: ...

class CriterionResult(_message.Message):
    __slots__ = ("criterion", "satisfied", "flag_state", "env_var_state", "runtime_state")
    CRITERION_FIELD_NUMBER: _ClassVar[int]
    SATISFIED_FIELD_NUMBER: _ClassVar[int]
    FLAG_STATE_FIELD_NUMBER: _ClassVar[int]
    ENV_VAR_STATE_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_STATE_FIELD_NUMBER: _ClassVar[int]
    criterion: MigrationCriterion
    satisfied: bool
    flag_state: ObservedFlagState
    env_var_state: ObservedEnvVarState
    runtime_state: ObservedRuntimeState
    def __init__(
        self,
        criterion: _Optional[_Union[MigrationCriterion, _Mapping]] = ...,
        satisfied: bool = ...,
        flag_state: _Optional[_Union[ObservedFlagState, _Mapping]] = ...,
        env_var_state: _Optional[_Union[ObservedEnvVarState, _Mapping]] = ...,
        runtime_state: _Optional[_Union[ObservedRuntimeState, _Mapping]] = ...,
    ) -> None: ...

class EnvironmentMigrationStatus(_message.Message):
    __slots__ = ("team_id", "team_name", "project_id", "environment_id", "environment_name", "state", "criteria")
    TEAM_ID_FIELD_NUMBER: _ClassVar[int]
    TEAM_NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CRITERIA_FIELD_NUMBER: _ClassVar[int]
    team_id: str
    team_name: str
    project_id: str
    environment_id: str
    environment_name: str
    state: EnvironmentMigrationState
    criteria: _containers.RepeatedCompositeFieldContainer[CriterionResult]
    def __init__(
        self,
        team_id: _Optional[str] = ...,
        team_name: _Optional[str] = ...,
        project_id: _Optional[str] = ...,
        environment_id: _Optional[str] = ...,
        environment_name: _Optional[str] = ...,
        state: _Optional[_Union[EnvironmentMigrationState, str]] = ...,
        criteria: _Optional[_Iterable[_Union[CriterionResult, _Mapping]]] = ...,
    ) -> None: ...

class MigrationCounts(_message.Message):
    __slots__ = ("migrated", "unmigrated")
    MIGRATED_FIELD_NUMBER: _ClassVar[int]
    UNMIGRATED_FIELD_NUMBER: _ClassVar[int]
    migrated: int
    unmigrated: int
    def __init__(self, migrated: _Optional[int] = ..., unmigrated: _Optional[int] = ...) -> None: ...

class ListMigrationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListMigrationsResponse(_message.Message):
    __slots__ = ("migrations",)
    class MigrationWithCounts(_message.Message):
        __slots__ = ("migration", "counts")
        MIGRATION_FIELD_NUMBER: _ClassVar[int]
        COUNTS_FIELD_NUMBER: _ClassVar[int]
        migration: Migration
        counts: MigrationCounts
        def __init__(
            self,
            migration: _Optional[_Union[Migration, _Mapping]] = ...,
            counts: _Optional[_Union[MigrationCounts, _Mapping]] = ...,
        ) -> None: ...

    MIGRATIONS_FIELD_NUMBER: _ClassVar[int]
    migrations: _containers.RepeatedCompositeFieldContainer[ListMigrationsResponse.MigrationWithCounts]
    def __init__(
        self, migrations: _Optional[_Iterable[_Union[ListMigrationsResponse.MigrationWithCounts, _Mapping]]] = ...
    ) -> None: ...

class GetMigrationStatusRequest(_message.Message):
    __slots__ = ("migration_id", "include_archived")
    MIGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_ARCHIVED_FIELD_NUMBER: _ClassVar[int]
    migration_id: str
    include_archived: bool
    def __init__(self, migration_id: _Optional[str] = ..., include_archived: bool = ...) -> None: ...

class GetMigrationStatusResponse(_message.Message):
    __slots__ = ("migration", "counts", "environments")
    MIGRATION_FIELD_NUMBER: _ClassVar[int]
    COUNTS_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    migration: Migration
    counts: MigrationCounts
    environments: _containers.RepeatedCompositeFieldContainer[EnvironmentMigrationStatus]
    def __init__(
        self,
        migration: _Optional[_Union[Migration, _Mapping]] = ...,
        counts: _Optional[_Union[MigrationCounts, _Mapping]] = ...,
        environments: _Optional[_Iterable[_Union[EnvironmentMigrationStatus, _Mapping]]] = ...,
    ) -> None: ...
