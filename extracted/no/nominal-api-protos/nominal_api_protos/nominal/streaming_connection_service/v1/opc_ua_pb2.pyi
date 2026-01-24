import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from nominal.gen.v1 import alias_pb2 as _alias_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OpcSecurityPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPC_SECURITY_POLICY_UNSPECIFIED: _ClassVar[OpcSecurityPolicy]
    NONE: _ClassVar[OpcSecurityPolicy]

class OpcUaReferenceExplorationType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPC_UA_REFERENCE_EXPLORATION_TYPE_UNSPECIFIED: _ClassVar[OpcUaReferenceExplorationType]
    OPC_UA_REFERENCE_EXPLORATION_TYPE_ORGANIZES: _ClassVar[OpcUaReferenceExplorationType]
    OPC_UA_REFERENCE_EXPLORATION_TYPE_HIERARCHICAL_REFERENCES: _ClassVar[OpcUaReferenceExplorationType]

class OpcUaUnknownDataTypeHandling(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPC_UA_UNKNOWN_DATA_TYPE_HANDLING_UNSPECIFIED: _ClassVar[OpcUaUnknownDataTypeHandling]
    OPC_UA_UNKNOWN_DATA_TYPE_HANDLING_ERROR: _ClassVar[OpcUaUnknownDataTypeHandling]
    OPC_UA_UNKNOWN_DATA_TYPE_HANDLING_TREAT_AS_DOUBLE: _ClassVar[OpcUaUnknownDataTypeHandling]
    OPC_UA_UNKNOWN_DATA_TYPE_HANDLING_TREAT_AS_STRING: _ClassVar[OpcUaUnknownDataTypeHandling]

class OpcUaFailedMonitorHandling(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPC_UA_FAILED_MONITOR_HANDLING_UNSPECIFIED: _ClassVar[OpcUaFailedMonitorHandling]
    OPC_UA_FAILED_MONITOR_HANDLING_ERROR: _ClassVar[OpcUaFailedMonitorHandling]
    OPC_UA_FAILED_MONITOR_HANDLING_IGNORE: _ClassVar[OpcUaFailedMonitorHandling]

class OpcUaDataChangeTrigger(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPC_UA_DATA_CHANGE_TRIGGER_UNSPECIFIED: _ClassVar[OpcUaDataChangeTrigger]
    OPC_UA_DATA_CHANGE_TRIGGER_STATUS_ONLY: _ClassVar[OpcUaDataChangeTrigger]
    OPC_UA_DATA_CHANGE_TRIGGER_STATUS_VALUE: _ClassVar[OpcUaDataChangeTrigger]
    OPC_UA_DATA_CHANGE_TRIGGER_STATUS_VALUE_TIMESTAMP: _ClassVar[OpcUaDataChangeTrigger]

class OpcUaDeadbandType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPC_UA_DEADBAND_TYPE_UNSPECIFIED: _ClassVar[OpcUaDeadbandType]
    OPC_UA_DEADBAND_TYPE_NONE: _ClassVar[OpcUaDeadbandType]
    OPC_UA_DEADBAND_TYPE_ABSOLUTE: _ClassVar[OpcUaDeadbandType]
    OPC_UA_DEADBAND_TYPE_PERCENT: _ClassVar[OpcUaDeadbandType]
OPC_SECURITY_POLICY_UNSPECIFIED: OpcSecurityPolicy
NONE: OpcSecurityPolicy
OPC_UA_REFERENCE_EXPLORATION_TYPE_UNSPECIFIED: OpcUaReferenceExplorationType
OPC_UA_REFERENCE_EXPLORATION_TYPE_ORGANIZES: OpcUaReferenceExplorationType
OPC_UA_REFERENCE_EXPLORATION_TYPE_HIERARCHICAL_REFERENCES: OpcUaReferenceExplorationType
OPC_UA_UNKNOWN_DATA_TYPE_HANDLING_UNSPECIFIED: OpcUaUnknownDataTypeHandling
OPC_UA_UNKNOWN_DATA_TYPE_HANDLING_ERROR: OpcUaUnknownDataTypeHandling
OPC_UA_UNKNOWN_DATA_TYPE_HANDLING_TREAT_AS_DOUBLE: OpcUaUnknownDataTypeHandling
OPC_UA_UNKNOWN_DATA_TYPE_HANDLING_TREAT_AS_STRING: OpcUaUnknownDataTypeHandling
OPC_UA_FAILED_MONITOR_HANDLING_UNSPECIFIED: OpcUaFailedMonitorHandling
OPC_UA_FAILED_MONITOR_HANDLING_ERROR: OpcUaFailedMonitorHandling
OPC_UA_FAILED_MONITOR_HANDLING_IGNORE: OpcUaFailedMonitorHandling
OPC_UA_DATA_CHANGE_TRIGGER_UNSPECIFIED: OpcUaDataChangeTrigger
OPC_UA_DATA_CHANGE_TRIGGER_STATUS_ONLY: OpcUaDataChangeTrigger
OPC_UA_DATA_CHANGE_TRIGGER_STATUS_VALUE: OpcUaDataChangeTrigger
OPC_UA_DATA_CHANGE_TRIGGER_STATUS_VALUE_TIMESTAMP: OpcUaDataChangeTrigger
OPC_UA_DEADBAND_TYPE_UNSPECIFIED: OpcUaDeadbandType
OPC_UA_DEADBAND_TYPE_NONE: OpcUaDeadbandType
OPC_UA_DEADBAND_TYPE_ABSOLUTE: OpcUaDeadbandType
OPC_UA_DEADBAND_TYPE_PERCENT: OpcUaDeadbandType

class OpcAuthenticationConfig(_message.Message):
    __slots__ = ("anonymous", "username_password", "token")
    ANONYMOUS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    anonymous: _empty_pb2.Empty
    username_password: OpcUsernamePasswordAuthentication
    token: OpcTokenAuthentication
    def __init__(self, anonymous: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ..., username_password: _Optional[_Union[OpcUsernamePasswordAuthentication, _Mapping]] = ..., token: _Optional[_Union[OpcTokenAuthentication, _Mapping]] = ...) -> None: ...

class OpcAuthenticationConfigSecret(_message.Message):
    __slots__ = ("anonymous", "username_password", "token")
    ANONYMOUS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    anonymous: _empty_pb2.Empty
    username_password: OpcUsernamePasswordAuthenticationSecret
    token: OpcTokenAuthenticationSecret
    def __init__(self, anonymous: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ..., username_password: _Optional[_Union[OpcUsernamePasswordAuthenticationSecret, _Mapping]] = ..., token: _Optional[_Union[OpcTokenAuthenticationSecret, _Mapping]] = ...) -> None: ...

class OpcUsernamePasswordAuthentication(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class OpcUsernamePasswordAuthenticationSecret(_message.Message):
    __slots__ = ("username", "password")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username: str
    password: str
    def __init__(self, username: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class OpcTokenAuthentication(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class OpcTokenAuthenticationSecret(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class OpcIdentifierValue(_message.Message):
    __slots__ = ("numeric", "string")
    NUMERIC_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    numeric: int
    string: str
    def __init__(self, numeric: _Optional[int] = ..., string: _Optional[str] = ...) -> None: ...

class OpcNode(_message.Message):
    __slots__ = ("namespace", "identifier")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    namespace: int
    identifier: OpcIdentifierValue
    def __init__(self, namespace: _Optional[int] = ..., identifier: _Optional[_Union[OpcIdentifierValue, _Mapping]] = ...) -> None: ...

class OpcUaChannelNamingConvention(_message.Message):
    __slots__ = ("node_id", "browse_name", "display_name", "full_path")
    class OpcUaNodeId(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class OpcUaBrowseName(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class OpcUaDisplayName(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class OpcUaFullPath(_message.Message):
        __slots__ = ("root_nodes", "delimiter")
        ROOT_NODES_FIELD_NUMBER: _ClassVar[int]
        DELIMITER_FIELD_NUMBER: _ClassVar[int]
        root_nodes: _containers.RepeatedCompositeFieldContainer[OpcNode]
        delimiter: str
        def __init__(self, root_nodes: _Optional[_Iterable[_Union[OpcNode, _Mapping]]] = ..., delimiter: _Optional[str] = ...) -> None: ...
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    BROWSE_NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    FULL_PATH_FIELD_NUMBER: _ClassVar[int]
    node_id: OpcUaChannelNamingConvention.OpcUaNodeId
    browse_name: OpcUaChannelNamingConvention.OpcUaBrowseName
    display_name: OpcUaChannelNamingConvention.OpcUaDisplayName
    full_path: OpcUaChannelNamingConvention.OpcUaFullPath
    def __init__(self, node_id: _Optional[_Union[OpcUaChannelNamingConvention.OpcUaNodeId, _Mapping]] = ..., browse_name: _Optional[_Union[OpcUaChannelNamingConvention.OpcUaBrowseName, _Mapping]] = ..., display_name: _Optional[_Union[OpcUaChannelNamingConvention.OpcUaDisplayName, _Mapping]] = ..., full_path: _Optional[_Union[OpcUaChannelNamingConvention.OpcUaFullPath, _Mapping]] = ...) -> None: ...

class OpcUaConnectionDetails(_message.Message):
    __slots__ = ("uri", "security_policy", "authentication_config")
    URI_FIELD_NUMBER: _ClassVar[int]
    SECURITY_POLICY_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    uri: str
    security_policy: OpcSecurityPolicy
    authentication_config: OpcAuthenticationConfig
    def __init__(self, uri: _Optional[str] = ..., security_policy: _Optional[_Union[OpcSecurityPolicy, str]] = ..., authentication_config: _Optional[_Union[OpcAuthenticationConfig, _Mapping]] = ...) -> None: ...

class OpcUaConnectionDetailsSecret(_message.Message):
    __slots__ = ("uri", "security_policy", "authentication_config")
    URI_FIELD_NUMBER: _ClassVar[int]
    SECURITY_POLICY_FIELD_NUMBER: _ClassVar[int]
    AUTHENTICATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    uri: str
    security_policy: OpcSecurityPolicy
    authentication_config: OpcAuthenticationConfigSecret
    def __init__(self, uri: _Optional[str] = ..., security_policy: _Optional[_Union[OpcSecurityPolicy, str]] = ..., authentication_config: _Optional[_Union[OpcAuthenticationConfigSecret, _Mapping]] = ...) -> None: ...

class OpcUaTraversalConfig(_message.Message):
    __slots__ = ("root_nodes", "skip_nodes", "reference_exploration_type")
    ROOT_NODES_FIELD_NUMBER: _ClassVar[int]
    SKIP_NODES_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_EXPLORATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    root_nodes: _containers.RepeatedCompositeFieldContainer[OpcNode]
    skip_nodes: _containers.RepeatedCompositeFieldContainer[OpcNode]
    reference_exploration_type: OpcUaReferenceExplorationType
    def __init__(self, root_nodes: _Optional[_Iterable[_Union[OpcNode, _Mapping]]] = ..., skip_nodes: _Optional[_Iterable[_Union[OpcNode, _Mapping]]] = ..., reference_exploration_type: _Optional[_Union[OpcUaReferenceExplorationType, str]] = ...) -> None: ...

class OpcUaDirectNodeSubscription(_message.Message):
    __slots__ = ("nodes",)
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[OpcNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[OpcNode, _Mapping]]] = ...) -> None: ...

class OpcUaNodeExplorationConfig(_message.Message):
    __slots__ = ("opc_ua_traversal_config", "opc_ua_direct_node_subscription")
    OPC_UA_TRAVERSAL_CONFIG_FIELD_NUMBER: _ClassVar[int]
    OPC_UA_DIRECT_NODE_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    opc_ua_traversal_config: OpcUaTraversalConfig
    opc_ua_direct_node_subscription: OpcUaDirectNodeSubscription
    def __init__(self, opc_ua_traversal_config: _Optional[_Union[OpcUaTraversalConfig, _Mapping]] = ..., opc_ua_direct_node_subscription: _Optional[_Union[OpcUaDirectNodeSubscription, _Mapping]] = ...) -> None: ...

class OpcUaTimestampHandling(_message.Message):
    __slots__ = ("server", "source", "relative")
    class OpcUaServerTime(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class OpcUaSourceTime(_message.Message):
        __slots__ = ()
        def __init__(self) -> None: ...
    class OpcUaRelativeTimestamp(_message.Message):
        __slots__ = ("offset",)
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        offset: _timestamp_pb2.Timestamp
        def __init__(self, offset: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
    SERVER_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_FIELD_NUMBER: _ClassVar[int]
    server: OpcUaTimestampHandling.OpcUaServerTime
    source: OpcUaTimestampHandling.OpcUaSourceTime
    relative: OpcUaTimestampHandling.OpcUaRelativeTimestamp
    def __init__(self, server: _Optional[_Union[OpcUaTimestampHandling.OpcUaServerTime, _Mapping]] = ..., source: _Optional[_Union[OpcUaTimestampHandling.OpcUaSourceTime, _Mapping]] = ..., relative: _Optional[_Union[OpcUaTimestampHandling.OpcUaRelativeTimestamp, _Mapping]] = ...) -> None: ...

class OpcUaDataChangeFilter(_message.Message):
    __slots__ = ("trigger", "deadband_type", "deadband_value")
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    DEADBAND_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEADBAND_VALUE_FIELD_NUMBER: _ClassVar[int]
    trigger: OpcUaDataChangeTrigger
    deadband_type: OpcUaDeadbandType
    deadband_value: float
    def __init__(self, trigger: _Optional[_Union[OpcUaDataChangeTrigger, str]] = ..., deadband_type: _Optional[_Union[OpcUaDeadbandType, str]] = ..., deadband_value: _Optional[float] = ...) -> None: ...

class OpcUaScrapingConfig(_message.Message):
    __slots__ = ("node_exploration_config", "unit_node_name", "channel_naming_convention", "override_host", "unknown_data_type_handling", "failed_monitor_handling", "timestamp_handling", "data_change_filter")
    NODE_EXPLORATION_CONFIG_FIELD_NUMBER: _ClassVar[int]
    UNIT_NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NAMING_CONVENTION_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_HOST_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_DATA_TYPE_HANDLING_FIELD_NUMBER: _ClassVar[int]
    FAILED_MONITOR_HANDLING_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_HANDLING_FIELD_NUMBER: _ClassVar[int]
    DATA_CHANGE_FILTER_FIELD_NUMBER: _ClassVar[int]
    node_exploration_config: OpcUaNodeExplorationConfig
    unit_node_name: str
    channel_naming_convention: OpcUaChannelNamingConvention
    override_host: bool
    unknown_data_type_handling: OpcUaUnknownDataTypeHandling
    failed_monitor_handling: OpcUaFailedMonitorHandling
    timestamp_handling: OpcUaTimestampHandling
    data_change_filter: OpcUaDataChangeFilter
    def __init__(self, node_exploration_config: _Optional[_Union[OpcUaNodeExplorationConfig, _Mapping]] = ..., unit_node_name: _Optional[str] = ..., channel_naming_convention: _Optional[_Union[OpcUaChannelNamingConvention, _Mapping]] = ..., override_host: bool = ..., unknown_data_type_handling: _Optional[_Union[OpcUaUnknownDataTypeHandling, str]] = ..., failed_monitor_handling: _Optional[_Union[OpcUaFailedMonitorHandling, str]] = ..., timestamp_handling: _Optional[_Union[OpcUaTimestampHandling, _Mapping]] = ..., data_change_filter: _Optional[_Union[OpcUaDataChangeFilter, _Mapping]] = ...) -> None: ...
