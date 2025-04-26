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

class KubernetesPodData(_message.Message):
    __slots__ = (
        "team",
        "app",
        "component",
        "datadog_service",
        "datadog_version",
        "pod_template_hash",
        "status",
        "spec",
        "creation_timestamp",
        "deletion_timestamp",
        "observed_timestamp",
        "labels",
        "annotations",
        "cluster",
        "uid",
        "name",
        "namespace",
    )
    class Volume(_message.Message):
        __slots__ = ("name",)
        NAME_FIELD_NUMBER: _ClassVar[int]
        name: str
        def __init__(self, name: _Optional[str] = ...) -> None: ...

    class ClaimSource(_message.Message):
        __slots__ = ("resource_claim_name", "resource_claim_template_name")
        RESOURCE_CLAIM_NAME_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_CLAIM_TEMPLATE_NAME_FIELD_NUMBER: _ClassVar[int]
        resource_claim_name: str
        resource_claim_template_name: str
        def __init__(
            self, resource_claim_name: _Optional[str] = ..., resource_claim_template_name: _Optional[str] = ...
        ) -> None: ...

    class PodResourceClaim(_message.Message):
        __slots__ = ("name", "source")
        NAME_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        name: str
        source: KubernetesPodData.ClaimSource
        def __init__(
            self, name: _Optional[str] = ..., source: _Optional[_Union[KubernetesPodData.ClaimSource, _Mapping]] = ...
        ) -> None: ...

    class PodSpec(_message.Message):
        __slots__ = (
            "volumes",
            "init_containers",
            "containers",
            "restart_policy",
            "termination_grace_period_seconds",
            "active_deadline_seconds",
            "dns_policy",
            "node_selector",
            "service_account_name",
            "automount_service_account_token",
            "node_name",
            "host_network",
            "host_pid",
            "host_ipc",
            "share_process_namespace",
            "hostname",
            "subdomain",
            "scheduler_name",
            "priority_class_name",
            "priority",
            "runtime_class_name",
            "enable_service_links",
            "preemption_policy",
            "host_users",
            "resource_claims",
        )
        class NodeSelectorEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

        VOLUMES_FIELD_NUMBER: _ClassVar[int]
        INIT_CONTAINERS_FIELD_NUMBER: _ClassVar[int]
        CONTAINERS_FIELD_NUMBER: _ClassVar[int]
        RESTART_POLICY_FIELD_NUMBER: _ClassVar[int]
        TERMINATION_GRACE_PERIOD_SECONDS_FIELD_NUMBER: _ClassVar[int]
        ACTIVE_DEADLINE_SECONDS_FIELD_NUMBER: _ClassVar[int]
        DNS_POLICY_FIELD_NUMBER: _ClassVar[int]
        NODE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
        SERVICE_ACCOUNT_NAME_FIELD_NUMBER: _ClassVar[int]
        AUTOMOUNT_SERVICE_ACCOUNT_TOKEN_FIELD_NUMBER: _ClassVar[int]
        NODE_NAME_FIELD_NUMBER: _ClassVar[int]
        HOST_NETWORK_FIELD_NUMBER: _ClassVar[int]
        HOST_PID_FIELD_NUMBER: _ClassVar[int]
        HOST_IPC_FIELD_NUMBER: _ClassVar[int]
        SHARE_PROCESS_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
        HOSTNAME_FIELD_NUMBER: _ClassVar[int]
        SUBDOMAIN_FIELD_NUMBER: _ClassVar[int]
        SCHEDULER_NAME_FIELD_NUMBER: _ClassVar[int]
        PRIORITY_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
        PRIORITY_FIELD_NUMBER: _ClassVar[int]
        RUNTIME_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
        ENABLE_SERVICE_LINKS_FIELD_NUMBER: _ClassVar[int]
        PREEMPTION_POLICY_FIELD_NUMBER: _ClassVar[int]
        HOST_USERS_FIELD_NUMBER: _ClassVar[int]
        RESOURCE_CLAIMS_FIELD_NUMBER: _ClassVar[int]
        volumes: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.Volume]
        init_containers: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.Container]
        containers: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.Container]
        restart_policy: str
        termination_grace_period_seconds: int
        active_deadline_seconds: int
        dns_policy: str
        node_selector: _containers.ScalarMap[str, str]
        service_account_name: str
        automount_service_account_token: bool
        node_name: str
        host_network: bool
        host_pid: bool
        host_ipc: bool
        share_process_namespace: bool
        hostname: str
        subdomain: str
        scheduler_name: str
        priority_class_name: str
        priority: int
        runtime_class_name: str
        enable_service_links: bool
        preemption_policy: str
        host_users: bool
        resource_claims: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.PodResourceClaim]
        def __init__(
            self,
            volumes: _Optional[_Iterable[_Union[KubernetesPodData.Volume, _Mapping]]] = ...,
            init_containers: _Optional[_Iterable[_Union[KubernetesPodData.Container, _Mapping]]] = ...,
            containers: _Optional[_Iterable[_Union[KubernetesPodData.Container, _Mapping]]] = ...,
            restart_policy: _Optional[str] = ...,
            termination_grace_period_seconds: _Optional[int] = ...,
            active_deadline_seconds: _Optional[int] = ...,
            dns_policy: _Optional[str] = ...,
            node_selector: _Optional[_Mapping[str, str]] = ...,
            service_account_name: _Optional[str] = ...,
            automount_service_account_token: bool = ...,
            node_name: _Optional[str] = ...,
            host_network: bool = ...,
            host_pid: bool = ...,
            host_ipc: bool = ...,
            share_process_namespace: bool = ...,
            hostname: _Optional[str] = ...,
            subdomain: _Optional[str] = ...,
            scheduler_name: _Optional[str] = ...,
            priority_class_name: _Optional[str] = ...,
            priority: _Optional[int] = ...,
            runtime_class_name: _Optional[str] = ...,
            enable_service_links: bool = ...,
            preemption_policy: _Optional[str] = ...,
            host_users: bool = ...,
            resource_claims: _Optional[_Iterable[_Union[KubernetesPodData.PodResourceClaim, _Mapping]]] = ...,
        ) -> None: ...

    class ContainerState(_message.Message):
        __slots__ = ("waiting", "running", "terminated")
        WAITING_FIELD_NUMBER: _ClassVar[int]
        RUNNING_FIELD_NUMBER: _ClassVar[int]
        TERMINATED_FIELD_NUMBER: _ClassVar[int]
        waiting: KubernetesPodData.ContainerStateWaiting
        running: KubernetesPodData.ContainerStateRunning
        terminated: KubernetesPodData.ContainerStateTerminated
        def __init__(
            self,
            waiting: _Optional[_Union[KubernetesPodData.ContainerStateWaiting, _Mapping]] = ...,
            running: _Optional[_Union[KubernetesPodData.ContainerStateRunning, _Mapping]] = ...,
            terminated: _Optional[_Union[KubernetesPodData.ContainerStateTerminated, _Mapping]] = ...,
        ) -> None: ...

    class ContainerStateRunning(_message.Message):
        __slots__ = ("started_at",)
        STARTED_AT_FIELD_NUMBER: _ClassVar[int]
        started_at: int
        def __init__(self, started_at: _Optional[int] = ...) -> None: ...

    class ContainerStateTerminated(_message.Message):
        __slots__ = ("exit_code", "signal", "reason", "message", "started_at", "finished_at", "container_id")
        EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
        SIGNAL_FIELD_NUMBER: _ClassVar[int]
        REASON_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        STARTED_AT_FIELD_NUMBER: _ClassVar[int]
        FINISHED_AT_FIELD_NUMBER: _ClassVar[int]
        CONTAINER_ID_FIELD_NUMBER: _ClassVar[int]
        exit_code: int
        signal: int
        reason: str
        message: str
        started_at: int
        finished_at: int
        container_id: str
        def __init__(
            self,
            exit_code: _Optional[int] = ...,
            signal: _Optional[int] = ...,
            reason: _Optional[str] = ...,
            message: _Optional[str] = ...,
            started_at: _Optional[int] = ...,
            finished_at: _Optional[int] = ...,
            container_id: _Optional[str] = ...,
        ) -> None: ...

    class EnvVar(_message.Message):
        __slots__ = ("name", "value")
        NAME_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        name: str
        value: str
        def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class Container(_message.Message):
        __slots__ = (
            "name",
            "image",
            "command",
            "args",
            "working_dir",
            "env",
            "resources",
            "restart_policy",
            "termination_message_path",
            "termination_message_policy",
            "image_pull_policy",
            "stdin",
            "stdin_once",
            "tty",
        )
        NAME_FIELD_NUMBER: _ClassVar[int]
        IMAGE_FIELD_NUMBER: _ClassVar[int]
        COMMAND_FIELD_NUMBER: _ClassVar[int]
        ARGS_FIELD_NUMBER: _ClassVar[int]
        WORKING_DIR_FIELD_NUMBER: _ClassVar[int]
        ENV_FIELD_NUMBER: _ClassVar[int]
        RESOURCES_FIELD_NUMBER: _ClassVar[int]
        RESTART_POLICY_FIELD_NUMBER: _ClassVar[int]
        TERMINATION_MESSAGE_PATH_FIELD_NUMBER: _ClassVar[int]
        TERMINATION_MESSAGE_POLICY_FIELD_NUMBER: _ClassVar[int]
        IMAGE_PULL_POLICY_FIELD_NUMBER: _ClassVar[int]
        STDIN_FIELD_NUMBER: _ClassVar[int]
        STDIN_ONCE_FIELD_NUMBER: _ClassVar[int]
        TTY_FIELD_NUMBER: _ClassVar[int]
        name: str
        image: str
        command: _containers.RepeatedScalarFieldContainer[str]
        args: _containers.RepeatedScalarFieldContainer[str]
        working_dir: str
        env: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.EnvVar]
        resources: KubernetesPodData.ResourceRequirements
        restart_policy: str
        termination_message_path: str
        termination_message_policy: str
        image_pull_policy: str
        stdin: bool
        stdin_once: bool
        tty: bool
        def __init__(
            self,
            name: _Optional[str] = ...,
            image: _Optional[str] = ...,
            command: _Optional[_Iterable[str]] = ...,
            args: _Optional[_Iterable[str]] = ...,
            working_dir: _Optional[str] = ...,
            env: _Optional[_Iterable[_Union[KubernetesPodData.EnvVar, _Mapping]]] = ...,
            resources: _Optional[_Union[KubernetesPodData.ResourceRequirements, _Mapping]] = ...,
            restart_policy: _Optional[str] = ...,
            termination_message_path: _Optional[str] = ...,
            termination_message_policy: _Optional[str] = ...,
            image_pull_policy: _Optional[str] = ...,
            stdin: bool = ...,
            stdin_once: bool = ...,
            tty: bool = ...,
        ) -> None: ...

    class ContainerStateWaiting(_message.Message):
        __slots__ = ("reason", "message")
        REASON_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        reason: str
        message: str
        def __init__(self, reason: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

    class ContainerStatus(_message.Message):
        __slots__ = (
            "name",
            "state",
            "last_state",
            "ready",
            "restart_count",
            "image",
            "image_id",
            "container_id",
            "started",
        )
        NAME_FIELD_NUMBER: _ClassVar[int]
        STATE_FIELD_NUMBER: _ClassVar[int]
        LAST_STATE_FIELD_NUMBER: _ClassVar[int]
        READY_FIELD_NUMBER: _ClassVar[int]
        RESTART_COUNT_FIELD_NUMBER: _ClassVar[int]
        IMAGE_FIELD_NUMBER: _ClassVar[int]
        IMAGE_ID_FIELD_NUMBER: _ClassVar[int]
        CONTAINER_ID_FIELD_NUMBER: _ClassVar[int]
        STARTED_FIELD_NUMBER: _ClassVar[int]
        name: str
        state: KubernetesPodData.ContainerState
        last_state: KubernetesPodData.ContainerState
        ready: bool
        restart_count: int
        image: str
        image_id: str
        container_id: str
        started: bool
        def __init__(
            self,
            name: _Optional[str] = ...,
            state: _Optional[_Union[KubernetesPodData.ContainerState, _Mapping]] = ...,
            last_state: _Optional[_Union[KubernetesPodData.ContainerState, _Mapping]] = ...,
            ready: bool = ...,
            restart_count: _Optional[int] = ...,
            image: _Optional[str] = ...,
            image_id: _Optional[str] = ...,
            container_id: _Optional[str] = ...,
            started: bool = ...,
        ) -> None: ...

    class Quantity(_message.Message):
        __slots__ = ("string",)
        STRING_FIELD_NUMBER: _ClassVar[int]
        string: str
        def __init__(self, string: _Optional[str] = ...) -> None: ...

    class ResourceRequirements(_message.Message):
        __slots__ = ("limits", "requests")
        class LimitsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: KubernetesPodData.Quantity
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[_Union[KubernetesPodData.Quantity, _Mapping]] = ...
            ) -> None: ...

        class RequestsEntry(_message.Message):
            __slots__ = ("key", "value")
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: KubernetesPodData.Quantity
            def __init__(
                self, key: _Optional[str] = ..., value: _Optional[_Union[KubernetesPodData.Quantity, _Mapping]] = ...
            ) -> None: ...

        LIMITS_FIELD_NUMBER: _ClassVar[int]
        REQUESTS_FIELD_NUMBER: _ClassVar[int]
        limits: _containers.MessageMap[str, KubernetesPodData.Quantity]
        requests: _containers.MessageMap[str, KubernetesPodData.Quantity]
        def __init__(
            self,
            limits: _Optional[_Mapping[str, KubernetesPodData.Quantity]] = ...,
            requests: _Optional[_Mapping[str, KubernetesPodData.Quantity]] = ...,
        ) -> None: ...

    class PodCondition(_message.Message):
        __slots__ = ("type", "status", "last_probe_time", "last_transition_time", "reason", "message")
        TYPE_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        LAST_PROBE_TIME_FIELD_NUMBER: _ClassVar[int]
        LAST_TRANSITION_TIME_FIELD_NUMBER: _ClassVar[int]
        REASON_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        type: str
        status: str
        last_probe_time: int
        last_transition_time: int
        reason: str
        message: str
        def __init__(
            self,
            type: _Optional[str] = ...,
            status: _Optional[str] = ...,
            last_probe_time: _Optional[int] = ...,
            last_transition_time: _Optional[int] = ...,
            reason: _Optional[str] = ...,
            message: _Optional[str] = ...,
        ) -> None: ...

    class HostIP(_message.Message):
        __slots__ = ("ip",)
        IP_FIELD_NUMBER: _ClassVar[int]
        ip: str
        def __init__(self, ip: _Optional[str] = ...) -> None: ...

    class PodStatus(_message.Message):
        __slots__ = (
            "phase",
            "conditions",
            "message",
            "reason",
            "nominated_node_name",
            "host_ip",
            "host_ips",
            "pod_ip",
            "start_time",
            "init_container_statuses",
            "container_statuses",
            "qos_class",
            "ephemeral_container_statuses",
            "resize",
        )
        PHASE_FIELD_NUMBER: _ClassVar[int]
        CONDITIONS_FIELD_NUMBER: _ClassVar[int]
        MESSAGE_FIELD_NUMBER: _ClassVar[int]
        REASON_FIELD_NUMBER: _ClassVar[int]
        NOMINATED_NODE_NAME_FIELD_NUMBER: _ClassVar[int]
        HOST_IP_FIELD_NUMBER: _ClassVar[int]
        HOST_IPS_FIELD_NUMBER: _ClassVar[int]
        POD_IP_FIELD_NUMBER: _ClassVar[int]
        START_TIME_FIELD_NUMBER: _ClassVar[int]
        INIT_CONTAINER_STATUSES_FIELD_NUMBER: _ClassVar[int]
        CONTAINER_STATUSES_FIELD_NUMBER: _ClassVar[int]
        QOS_CLASS_FIELD_NUMBER: _ClassVar[int]
        EPHEMERAL_CONTAINER_STATUSES_FIELD_NUMBER: _ClassVar[int]
        RESIZE_FIELD_NUMBER: _ClassVar[int]
        phase: str
        conditions: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.PodCondition]
        message: str
        reason: str
        nominated_node_name: str
        host_ip: str
        host_ips: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.HostIP]
        pod_ip: str
        start_time: int
        init_container_statuses: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.ContainerStatus]
        container_statuses: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.ContainerStatus]
        qos_class: str
        ephemeral_container_statuses: _containers.RepeatedCompositeFieldContainer[KubernetesPodData.ContainerStatus]
        resize: str
        def __init__(
            self,
            phase: _Optional[str] = ...,
            conditions: _Optional[_Iterable[_Union[KubernetesPodData.PodCondition, _Mapping]]] = ...,
            message: _Optional[str] = ...,
            reason: _Optional[str] = ...,
            nominated_node_name: _Optional[str] = ...,
            host_ip: _Optional[str] = ...,
            host_ips: _Optional[_Iterable[_Union[KubernetesPodData.HostIP, _Mapping]]] = ...,
            pod_ip: _Optional[str] = ...,
            start_time: _Optional[int] = ...,
            init_container_statuses: _Optional[_Iterable[_Union[KubernetesPodData.ContainerStatus, _Mapping]]] = ...,
            container_statuses: _Optional[_Iterable[_Union[KubernetesPodData.ContainerStatus, _Mapping]]] = ...,
            qos_class: _Optional[str] = ...,
            ephemeral_container_statuses: _Optional[
                _Iterable[_Union[KubernetesPodData.ContainerStatus, _Mapping]]
            ] = ...,
            resize: _Optional[str] = ...,
        ) -> None: ...

    class LabelsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    class AnnotationsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    TEAM_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    DATADOG_SERVICE_FIELD_NUMBER: _ClassVar[int]
    DATADOG_VERSION_FIELD_NUMBER: _ClassVar[int]
    POD_TEMPLATE_HASH_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SPEC_FIELD_NUMBER: _ClassVar[int]
    CREATION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DELETION_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    team: str
    app: str
    component: str
    datadog_service: str
    datadog_version: str
    pod_template_hash: str
    status: KubernetesPodData.PodStatus
    spec: KubernetesPodData.PodSpec
    creation_timestamp: int
    deletion_timestamp: int
    observed_timestamp: int
    labels: _containers.ScalarMap[str, str]
    annotations: _containers.ScalarMap[str, str]
    cluster: str
    uid: str
    name: str
    namespace: str
    def __init__(
        self,
        team: _Optional[str] = ...,
        app: _Optional[str] = ...,
        component: _Optional[str] = ...,
        datadog_service: _Optional[str] = ...,
        datadog_version: _Optional[str] = ...,
        pod_template_hash: _Optional[str] = ...,
        status: _Optional[_Union[KubernetesPodData.PodStatus, _Mapping]] = ...,
        spec: _Optional[_Union[KubernetesPodData.PodSpec, _Mapping]] = ...,
        creation_timestamp: _Optional[int] = ...,
        deletion_timestamp: _Optional[int] = ...,
        observed_timestamp: _Optional[int] = ...,
        labels: _Optional[_Mapping[str, str]] = ...,
        annotations: _Optional[_Mapping[str, str]] = ...,
        cluster: _Optional[str] = ...,
        uid: _Optional[str] = ...,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
    ) -> None: ...
