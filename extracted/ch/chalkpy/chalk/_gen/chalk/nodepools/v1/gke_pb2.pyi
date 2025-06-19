from google.protobuf import duration_pb2 as _duration_pb2
from google.rpc import code_pb2 as _code_pb2
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

class NodePoolUpdateStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NODE_POOL_UPDATE_STRATEGY_UNSPECIFIED: _ClassVar[NodePoolUpdateStrategy]
    NODE_POOL_UPDATE_STRATEGY_BLUE_GREEN: _ClassVar[NodePoolUpdateStrategy]
    NODE_POOL_UPDATE_STRATEGY_SURGE: _ClassVar[NodePoolUpdateStrategy]

NODE_POOL_UPDATE_STRATEGY_UNSPECIFIED: NodePoolUpdateStrategy
NODE_POOL_UPDATE_STRATEGY_BLUE_GREEN: NodePoolUpdateStrategy
NODE_POOL_UPDATE_STRATEGY_SURGE: NodePoolUpdateStrategy

class StatusCondition(_message.Message):
    __slots__ = ("code", "message", "canonical_code")
    class Code(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        CODE_UNSPECIFIED: _ClassVar[StatusCondition.Code]
        CODE_GCE_STOCKOUT: _ClassVar[StatusCondition.Code]
        CODE_GKE_SERVICE_ACCOUNT_DELETED: _ClassVar[StatusCondition.Code]
        CODE_GCE_QUOTA_EXCEEDED: _ClassVar[StatusCondition.Code]
        CODE_SET_BY_OPERATOR: _ClassVar[StatusCondition.Code]
        CODE_CLOUD_KMS_KEY_ERROR: _ClassVar[StatusCondition.Code]
        CODE_CA_EXPIRING: _ClassVar[StatusCondition.Code]
        CODE_NODE_SERVICE_ACCOUNT_MISSING_PERMISSIONS: _ClassVar[StatusCondition.Code]

    CODE_UNSPECIFIED: StatusCondition.Code
    CODE_GCE_STOCKOUT: StatusCondition.Code
    CODE_GKE_SERVICE_ACCOUNT_DELETED: StatusCondition.Code
    CODE_GCE_QUOTA_EXCEEDED: StatusCondition.Code
    CODE_SET_BY_OPERATOR: StatusCondition.Code
    CODE_CLOUD_KMS_KEY_ERROR: StatusCondition.Code
    CODE_CA_EXPIRING: StatusCondition.Code
    CODE_NODE_SERVICE_ACCOUNT_MISSING_PERMISSIONS: StatusCondition.Code
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_CODE_FIELD_NUMBER: _ClassVar[int]
    code: StatusCondition.Code
    message: str
    canonical_code: _code_pb2.Code
    def __init__(
        self,
        code: _Optional[_Union[StatusCondition.Code, str]] = ...,
        message: _Optional[str] = ...,
        canonical_code: _Optional[_Union[_code_pb2.Code, str]] = ...,
    ) -> None: ...

class NodePoolAutoscaling(_message.Message):
    __slots__ = (
        "enabled",
        "min_node_count",
        "max_node_count",
        "autoprovisioned",
        "location_policy",
        "total_min_node_count",
        "total_max_node_count",
    )
    class LocationPolicy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOCATION_POLICY_UNSPECIFIED: _ClassVar[NodePoolAutoscaling.LocationPolicy]
        LOCATION_POLICY_BALANCED: _ClassVar[NodePoolAutoscaling.LocationPolicy]
        LOCATION_POLICY_ANY: _ClassVar[NodePoolAutoscaling.LocationPolicy]

    LOCATION_POLICY_UNSPECIFIED: NodePoolAutoscaling.LocationPolicy
    LOCATION_POLICY_BALANCED: NodePoolAutoscaling.LocationPolicy
    LOCATION_POLICY_ANY: NodePoolAutoscaling.LocationPolicy
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MIN_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    MAX_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    AUTOPROVISIONED_FIELD_NUMBER: _ClassVar[int]
    LOCATION_POLICY_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MIN_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MAX_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    min_node_count: int
    max_node_count: int
    autoprovisioned: bool
    location_policy: NodePoolAutoscaling.LocationPolicy
    total_min_node_count: int
    total_max_node_count: int
    def __init__(
        self,
        enabled: bool = ...,
        min_node_count: _Optional[int] = ...,
        max_node_count: _Optional[int] = ...,
        autoprovisioned: bool = ...,
        location_policy: _Optional[_Union[NodePoolAutoscaling.LocationPolicy, str]] = ...,
        total_min_node_count: _Optional[int] = ...,
        total_max_node_count: _Optional[int] = ...,
    ) -> None: ...

class NodeTaint(_message.Message):
    __slots__ = ("key", "value", "effect")
    class Effect(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EFFECT_UNSPECIFIED: _ClassVar[NodeTaint.Effect]
        EFFECT_NO_SCHEDULE: _ClassVar[NodeTaint.Effect]
        EFFECT_PREFER_NO_SCHEDULE: _ClassVar[NodeTaint.Effect]
        EFFECT_NO_EXECUTE: _ClassVar[NodeTaint.Effect]

    EFFECT_UNSPECIFIED: NodeTaint.Effect
    EFFECT_NO_SCHEDULE: NodeTaint.Effect
    EFFECT_PREFER_NO_SCHEDULE: NodeTaint.Effect
    EFFECT_NO_EXECUTE: NodeTaint.Effect
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    EFFECT_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    effect: NodeTaint.Effect
    def __init__(
        self,
        key: _Optional[str] = ...,
        value: _Optional[str] = ...,
        effect: _Optional[_Union[NodeTaint.Effect, str]] = ...,
    ) -> None: ...

class MaxPodsConstraint(_message.Message):
    __slots__ = ("max_pods_per_node",)
    MAX_PODS_PER_NODE_FIELD_NUMBER: _ClassVar[int]
    max_pods_per_node: int
    def __init__(self, max_pods_per_node: _Optional[int] = ...) -> None: ...

class BestEffortProvisioning(_message.Message):
    __slots__ = ("enabled", "min_provision_nodes")
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MIN_PROVISION_NODES_FIELD_NUMBER: _ClassVar[int]
    enabled: bool
    min_provision_nodes: int
    def __init__(self, enabled: bool = ..., min_provision_nodes: _Optional[int] = ...) -> None: ...

class NodeManagement(_message.Message):
    __slots__ = ("auto_upgrade", "auto_repair", "upgrade_options")
    AUTO_UPGRADE_FIELD_NUMBER: _ClassVar[int]
    AUTO_REPAIR_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_OPTIONS_FIELD_NUMBER: _ClassVar[int]
    auto_upgrade: bool
    auto_repair: bool
    upgrade_options: AutoUpgradeOptions
    def __init__(
        self,
        auto_upgrade: bool = ...,
        auto_repair: bool = ...,
        upgrade_options: _Optional[_Union[AutoUpgradeOptions, _Mapping]] = ...,
    ) -> None: ...

class AutoUpgradeOptions(_message.Message):
    __slots__ = ("auto_upgrade_start_time", "description")
    AUTO_UPGRADE_START_TIME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    auto_upgrade_start_time: str
    description: str
    def __init__(self, auto_upgrade_start_time: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class NodeConfig(_message.Message):
    __slots__ = (
        "machine_type",
        "disk_size_gb",
        "oauth_scopes",
        "service_account",
        "metadata",
        "image_type",
        "labels",
        "local_ssd_count",
        "tags",
        "preemptible",
        "disk_type",
        "min_cpu_platform",
        "taints",
        "node_group",
        "boot_disk_kms_key",
        "spot",
        "resource_labels",
        "local_ssd_encryption_mode",
        "effective_cgroup_mode",
    )
    class LocalSsdEncryptionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        LOCAL_SSD_ENCRYPTION_MODE_UNSPECIFIED: _ClassVar[NodeConfig.LocalSsdEncryptionMode]
        LOCAL_SSD_ENCRYPTION_MODE_STANDARD_ENCRYPTION: _ClassVar[NodeConfig.LocalSsdEncryptionMode]
        LOCAL_SSD_ENCRYPTION_MODE_EPHEMERAL_KEY_ENCRYPTION: _ClassVar[NodeConfig.LocalSsdEncryptionMode]

    LOCAL_SSD_ENCRYPTION_MODE_UNSPECIFIED: NodeConfig.LocalSsdEncryptionMode
    LOCAL_SSD_ENCRYPTION_MODE_STANDARD_ENCRYPTION: NodeConfig.LocalSsdEncryptionMode
    LOCAL_SSD_ENCRYPTION_MODE_EPHEMERAL_KEY_ENCRYPTION: NodeConfig.LocalSsdEncryptionMode
    class EffectiveCgroupMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        EFFECTIVE_CGROUP_MODE_UNSPECIFIED: _ClassVar[NodeConfig.EffectiveCgroupMode]
        EFFECTIVE_CGROUP_MODE_V1: _ClassVar[NodeConfig.EffectiveCgroupMode]
        EFFECTIVE_CGROUP_MODE_V2: _ClassVar[NodeConfig.EffectiveCgroupMode]

    EFFECTIVE_CGROUP_MODE_UNSPECIFIED: NodeConfig.EffectiveCgroupMode
    EFFECTIVE_CGROUP_MODE_V1: NodeConfig.EffectiveCgroupMode
    EFFECTIVE_CGROUP_MODE_V2: NodeConfig.EffectiveCgroupMode
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class ResourceLabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    DISK_SIZE_GB_FIELD_NUMBER: _ClassVar[int]
    OAUTH_SCOPES_FIELD_NUMBER: _ClassVar[int]
    SERVICE_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    IMAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_SSD_COUNT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    PREEMPTIBLE_FIELD_NUMBER: _ClassVar[int]
    DISK_TYPE_FIELD_NUMBER: _ClassVar[int]
    MIN_CPU_PLATFORM_FIELD_NUMBER: _ClassVar[int]
    TAINTS_FIELD_NUMBER: _ClassVar[int]
    NODE_GROUP_FIELD_NUMBER: _ClassVar[int]
    BOOT_DISK_KMS_KEY_FIELD_NUMBER: _ClassVar[int]
    SPOT_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_LABELS_FIELD_NUMBER: _ClassVar[int]
    LOCAL_SSD_ENCRYPTION_MODE_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_CGROUP_MODE_FIELD_NUMBER: _ClassVar[int]
    machine_type: str
    disk_size_gb: int
    oauth_scopes: _containers.RepeatedScalarFieldContainer[str]
    service_account: str
    metadata: _containers.ScalarMap[str, str]
    image_type: str
    labels: _containers.ScalarMap[str, str]
    local_ssd_count: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    preemptible: bool
    disk_type: str
    min_cpu_platform: str
    taints: _containers.RepeatedCompositeFieldContainer[NodeTaint]
    node_group: str
    boot_disk_kms_key: str
    spot: bool
    resource_labels: _containers.ScalarMap[str, str]
    local_ssd_encryption_mode: NodeConfig.LocalSsdEncryptionMode
    effective_cgroup_mode: NodeConfig.EffectiveCgroupMode
    def __init__(
        self,
        machine_type: _Optional[str] = ...,
        disk_size_gb: _Optional[int] = ...,
        oauth_scopes: _Optional[_Iterable[str]] = ...,
        service_account: _Optional[str] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
        image_type: _Optional[str] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        local_ssd_count: _Optional[int] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        preemptible: bool = ...,
        disk_type: _Optional[str] = ...,
        min_cpu_platform: _Optional[str] = ...,
        taints: _Optional[_Iterable[_Union[NodeTaint, _Mapping]]] = ...,
        node_group: _Optional[str] = ...,
        boot_disk_kms_key: _Optional[str] = ...,
        spot: bool = ...,
        resource_labels: _Optional[_Mapping[str, str]] = ...,
        local_ssd_encryption_mode: _Optional[_Union[NodeConfig.LocalSsdEncryptionMode, str]] = ...,
        effective_cgroup_mode: _Optional[_Union[NodeConfig.EffectiveCgroupMode, str]] = ...,
    ) -> None: ...

class BlueGreenSettings(_message.Message):
    __slots__ = ("standard_rollout_policy", "node_pool_soak_duration")
    class StandardRolloutPolicy(_message.Message):
        __slots__ = ("batch_percentage", "batch_node_count", "batch_soak_duration")
        BATCH_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
        BATCH_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
        BATCH_SOAK_DURATION_FIELD_NUMBER: _ClassVar[int]
        batch_percentage: float
        batch_node_count: int
        batch_soak_duration: _duration_pb2.Duration
        def __init__(
            self,
            batch_percentage: _Optional[float] = ...,
            batch_node_count: _Optional[int] = ...,
            batch_soak_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        ) -> None: ...

    STANDARD_ROLLOUT_POLICY_FIELD_NUMBER: _ClassVar[int]
    NODE_POOL_SOAK_DURATION_FIELD_NUMBER: _ClassVar[int]
    standard_rollout_policy: BlueGreenSettings.StandardRolloutPolicy
    node_pool_soak_duration: _duration_pb2.Duration
    def __init__(
        self,
        standard_rollout_policy: _Optional[_Union[BlueGreenSettings.StandardRolloutPolicy, _Mapping]] = ...,
        node_pool_soak_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
    ) -> None: ...

class GKENodePool(_message.Message):
    __slots__ = (
        "name",
        "config",
        "initial_node_count",
        "locations",
        "self_link",
        "version",
        "instance_group_urls",
        "status",
        "status_message",
        "autoscaling",
        "management",
        "max_pods_constraint",
        "conditions",
        "pod_ipv4_cidr_size",
        "upgrade_settings",
        "placement_policy",
        "update_info",
        "etag",
        "queued_provisioning",
        "best_effort_provisioning",
    )
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        STATUS_UNSPECIFIED: _ClassVar[GKENodePool.Status]
        STATUS_PROVISIONING: _ClassVar[GKENodePool.Status]
        STATUS_RUNNING: _ClassVar[GKENodePool.Status]
        STATUS_RUNNING_WITH_ERROR: _ClassVar[GKENodePool.Status]
        STATUS_RECONCILING: _ClassVar[GKENodePool.Status]
        STATUS_STOPPING: _ClassVar[GKENodePool.Status]
        STATUS_ERROR: _ClassVar[GKENodePool.Status]

    STATUS_UNSPECIFIED: GKENodePool.Status
    STATUS_PROVISIONING: GKENodePool.Status
    STATUS_RUNNING: GKENodePool.Status
    STATUS_RUNNING_WITH_ERROR: GKENodePool.Status
    STATUS_RECONCILING: GKENodePool.Status
    STATUS_STOPPING: GKENodePool.Status
    STATUS_ERROR: GKENodePool.Status
    class UpgradeSettings(_message.Message):
        __slots__ = ("max_surge", "max_unavailable", "strategy", "blue_green_settings")
        MAX_SURGE_FIELD_NUMBER: _ClassVar[int]
        MAX_UNAVAILABLE_FIELD_NUMBER: _ClassVar[int]
        STRATEGY_FIELD_NUMBER: _ClassVar[int]
        BLUE_GREEN_SETTINGS_FIELD_NUMBER: _ClassVar[int]
        max_surge: int
        max_unavailable: int
        strategy: NodePoolUpdateStrategy
        blue_green_settings: BlueGreenSettings
        def __init__(
            self,
            max_surge: _Optional[int] = ...,
            max_unavailable: _Optional[int] = ...,
            strategy: _Optional[_Union[NodePoolUpdateStrategy, str]] = ...,
            blue_green_settings: _Optional[_Union[BlueGreenSettings, _Mapping]] = ...,
        ) -> None: ...

    class UpdateInfo(_message.Message):
        __slots__ = ("blue_green_info",)
        class BlueGreenInfo(_message.Message):
            __slots__ = (
                "phase",
                "blue_instance_group_urls",
                "green_instance_group_urls",
                "blue_pool_deletion_start_time",
                "green_pool_version",
            )
            class Phase(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
                __slots__ = ()
                PHASE_UNSPECIFIED: _ClassVar[GKENodePool.UpdateInfo.BlueGreenInfo.Phase]
                PHASE_UPDATE_STARTED: _ClassVar[GKENodePool.UpdateInfo.BlueGreenInfo.Phase]
                PHASE_CREATING_GREEN_POOL: _ClassVar[GKENodePool.UpdateInfo.BlueGreenInfo.Phase]
                PHASE_CORDONING_BLUE_POOL: _ClassVar[GKENodePool.UpdateInfo.BlueGreenInfo.Phase]
                PHASE_DRAINING_BLUE_POOL: _ClassVar[GKENodePool.UpdateInfo.BlueGreenInfo.Phase]
                PHASE_NODE_POOL_SOAKING: _ClassVar[GKENodePool.UpdateInfo.BlueGreenInfo.Phase]
                PHASE_DELETING_BLUE_POOL: _ClassVar[GKENodePool.UpdateInfo.BlueGreenInfo.Phase]
                PHASE_ROLLBACK_STARTED: _ClassVar[GKENodePool.UpdateInfo.BlueGreenInfo.Phase]

            PHASE_UNSPECIFIED: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            PHASE_UPDATE_STARTED: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            PHASE_CREATING_GREEN_POOL: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            PHASE_CORDONING_BLUE_POOL: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            PHASE_DRAINING_BLUE_POOL: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            PHASE_NODE_POOL_SOAKING: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            PHASE_DELETING_BLUE_POOL: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            PHASE_ROLLBACK_STARTED: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            PHASE_FIELD_NUMBER: _ClassVar[int]
            BLUE_INSTANCE_GROUP_URLS_FIELD_NUMBER: _ClassVar[int]
            GREEN_INSTANCE_GROUP_URLS_FIELD_NUMBER: _ClassVar[int]
            BLUE_POOL_DELETION_START_TIME_FIELD_NUMBER: _ClassVar[int]
            GREEN_POOL_VERSION_FIELD_NUMBER: _ClassVar[int]
            phase: GKENodePool.UpdateInfo.BlueGreenInfo.Phase
            blue_instance_group_urls: _containers.RepeatedScalarFieldContainer[str]
            green_instance_group_urls: _containers.RepeatedScalarFieldContainer[str]
            blue_pool_deletion_start_time: str
            green_pool_version: str
            def __init__(
                self,
                phase: _Optional[_Union[GKENodePool.UpdateInfo.BlueGreenInfo.Phase, str]] = ...,
                blue_instance_group_urls: _Optional[_Iterable[str]] = ...,
                green_instance_group_urls: _Optional[_Iterable[str]] = ...,
                blue_pool_deletion_start_time: _Optional[str] = ...,
                green_pool_version: _Optional[str] = ...,
            ) -> None: ...

        BLUE_GREEN_INFO_FIELD_NUMBER: _ClassVar[int]
        blue_green_info: GKENodePool.UpdateInfo.BlueGreenInfo
        def __init__(
            self, blue_green_info: _Optional[_Union[GKENodePool.UpdateInfo.BlueGreenInfo, _Mapping]] = ...
        ) -> None: ...

    class PlacementPolicy(_message.Message):
        __slots__ = ("type", "tpu_topology", "policy_name")
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = ()
            TYPE_UNSPECIFIED: _ClassVar[GKENodePool.PlacementPolicy.Type]
            TYPE_COMPACT: _ClassVar[GKENodePool.PlacementPolicy.Type]

        TYPE_UNSPECIFIED: GKENodePool.PlacementPolicy.Type
        TYPE_COMPACT: GKENodePool.PlacementPolicy.Type
        TYPE_FIELD_NUMBER: _ClassVar[int]
        TPU_TOPOLOGY_FIELD_NUMBER: _ClassVar[int]
        POLICY_NAME_FIELD_NUMBER: _ClassVar[int]
        type: GKENodePool.PlacementPolicy.Type
        tpu_topology: str
        policy_name: str
        def __init__(
            self,
            type: _Optional[_Union[GKENodePool.PlacementPolicy.Type, str]] = ...,
            tpu_topology: _Optional[str] = ...,
            policy_name: _Optional[str] = ...,
        ) -> None: ...

    class QueuedProvisioning(_message.Message):
        __slots__ = ("enabled",)
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        enabled: bool
        def __init__(self, enabled: bool = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    INITIAL_NODE_COUNT_FIELD_NUMBER: _ClassVar[int]
    LOCATIONS_FIELD_NUMBER: _ClassVar[int]
    SELF_LINK_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_GROUP_URLS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    AUTOSCALING_FIELD_NUMBER: _ClassVar[int]
    MANAGEMENT_FIELD_NUMBER: _ClassVar[int]
    MAX_PODS_CONSTRAINT_FIELD_NUMBER: _ClassVar[int]
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    POD_IPV4_CIDR_SIZE_FIELD_NUMBER: _ClassVar[int]
    UPGRADE_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    PLACEMENT_POLICY_FIELD_NUMBER: _ClassVar[int]
    UPDATE_INFO_FIELD_NUMBER: _ClassVar[int]
    ETAG_FIELD_NUMBER: _ClassVar[int]
    QUEUED_PROVISIONING_FIELD_NUMBER: _ClassVar[int]
    BEST_EFFORT_PROVISIONING_FIELD_NUMBER: _ClassVar[int]
    name: str
    config: NodeConfig
    initial_node_count: int
    locations: _containers.RepeatedScalarFieldContainer[str]
    self_link: str
    version: str
    instance_group_urls: _containers.RepeatedScalarFieldContainer[str]
    status: GKENodePool.Status
    status_message: str
    autoscaling: NodePoolAutoscaling
    management: NodeManagement
    max_pods_constraint: MaxPodsConstraint
    conditions: _containers.RepeatedCompositeFieldContainer[StatusCondition]
    pod_ipv4_cidr_size: int
    upgrade_settings: GKENodePool.UpgradeSettings
    placement_policy: GKENodePool.PlacementPolicy
    update_info: GKENodePool.UpdateInfo
    etag: str
    queued_provisioning: GKENodePool.QueuedProvisioning
    best_effort_provisioning: BestEffortProvisioning
    def __init__(
        self,
        name: _Optional[str] = ...,
        config: _Optional[_Union[NodeConfig, _Mapping]] = ...,
        initial_node_count: _Optional[int] = ...,
        locations: _Optional[_Iterable[str]] = ...,
        self_link: _Optional[str] = ...,
        version: _Optional[str] = ...,
        instance_group_urls: _Optional[_Iterable[str]] = ...,
        status: _Optional[_Union[GKENodePool.Status, str]] = ...,
        status_message: _Optional[str] = ...,
        autoscaling: _Optional[_Union[NodePoolAutoscaling, _Mapping]] = ...,
        management: _Optional[_Union[NodeManagement, _Mapping]] = ...,
        max_pods_constraint: _Optional[_Union[MaxPodsConstraint, _Mapping]] = ...,
        conditions: _Optional[_Iterable[_Union[StatusCondition, _Mapping]]] = ...,
        pod_ipv4_cidr_size: _Optional[int] = ...,
        upgrade_settings: _Optional[_Union[GKENodePool.UpgradeSettings, _Mapping]] = ...,
        placement_policy: _Optional[_Union[GKENodePool.PlacementPolicy, _Mapping]] = ...,
        update_info: _Optional[_Union[GKENodePool.UpdateInfo, _Mapping]] = ...,
        etag: _Optional[str] = ...,
        queued_provisioning: _Optional[_Union[GKENodePool.QueuedProvisioning, _Mapping]] = ...,
        best_effort_provisioning: _Optional[_Union[BestEffortProvisioning, _Mapping]] = ...,
    ) -> None: ...
