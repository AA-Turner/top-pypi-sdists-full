from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.kubernetes.v1 import deployments_pb2 as _deployments_pb2
from chalk._gen.chalk.kubernetes.v1 import events_pb2 as _events_pb2
from chalk._gen.chalk.kubernetes.v1 import horizontalpodautoscaler_pb2 as _horizontalpodautoscaler_pb2
from chalk._gen.chalk.kubernetes.v1 import jobs_pb2 as _jobs_pb2
from chalk._gen.chalk.kubernetes.v1 import namespaces_pb2 as _namespaces_pb2
from chalk._gen.chalk.kubernetes.v1 import persistentvolume_pb2 as _persistentvolume_pb2
from chalk._gen.chalk.kubernetes.v1 import pods_pb2 as _pods_pb2
from chalk._gen.chalk.kubernetes.v1 import scaledobject_pb2 as _scaledobject_pb2
from chalk._gen.chalk.kubernetes.v1 import serviceaccounts_pb2 as _serviceaccounts_pb2
from chalk._gen.chalk.kubernetes.v1 import statefulsets_pb2 as _statefulsets_pb2
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

class GetPodVenvSizeRequest(_message.Message):
    __slots__ = ("namespace", "pod_name", "container_name")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pod_name: str
    container_name: str
    def __init__(
        self, namespace: _Optional[str] = ..., pod_name: _Optional[str] = ..., container_name: _Optional[str] = ...
    ) -> None: ...

class GetPodVenvSizeResponse(_message.Message):
    __slots__ = ("output",)
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    output: str
    def __init__(self, output: _Optional[str] = ...) -> None: ...

class GetPodStackTraceDumpRequest(_message.Message):
    __slots__ = ("namespace", "pod_name", "container_name", "process_id", "process_name", "auto_detect_process")
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    POD_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTAINER_NAME_FIELD_NUMBER: _ClassVar[int]
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    PROCESS_NAME_FIELD_NUMBER: _ClassVar[int]
    AUTO_DETECT_PROCESS_FIELD_NUMBER: _ClassVar[int]
    namespace: str
    pod_name: str
    container_name: str
    process_id: int
    process_name: str
    auto_detect_process: bool
    def __init__(
        self,
        namespace: _Optional[str] = ...,
        pod_name: _Optional[str] = ...,
        container_name: _Optional[str] = ...,
        process_id: _Optional[int] = ...,
        process_name: _Optional[str] = ...,
        auto_detect_process: bool = ...,
    ) -> None: ...

class GetPodStackTraceDumpResponse(_message.Message):
    __slots__ = ("stack_trace",)
    STACK_TRACE_FIELD_NUMBER: _ClassVar[int]
    stack_trace: str
    def __init__(self, stack_trace: _Optional[str] = ...) -> None: ...

class GetKubernetesEventsRequest(_message.Message):
    __slots__ = ("cluster_name", "namespace", "label_selector", "field_selector")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    FIELD_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    namespace: str
    label_selector: str
    field_selector: str
    def __init__(
        self,
        cluster_name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        label_selector: _Optional[str] = ...,
        field_selector: _Optional[str] = ...,
    ) -> None: ...

class GetKubernetesEventsResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[_events_pb2.ChalkKubernetesEvent]
    def __init__(
        self, events: _Optional[_Iterable[_Union[_events_pb2.ChalkKubernetesEvent, _Mapping]]] = ...
    ) -> None: ...

class GetKubernetesNamespacesRequest(_message.Message):
    __slots__ = ("environment_id", "label_selector")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    label_selector: str
    def __init__(self, environment_id: _Optional[str] = ..., label_selector: _Optional[str] = ...) -> None: ...

class GetKubernetesNamespacesResponse(_message.Message):
    __slots__ = ("namespaces",)
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    namespaces: _containers.RepeatedCompositeFieldContainer[_namespaces_pb2.KubernetesNamespace]
    def __init__(
        self, namespaces: _Optional[_Iterable[_Union[_namespaces_pb2.KubernetesNamespace, _Mapping]]] = ...
    ) -> None: ...

class GetKubernetesPersistentVolumesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetKubernetesPersistentVolumesResponse(_message.Message):
    __slots__ = ("volumes",)
    VOLUMES_FIELD_NUMBER: _ClassVar[int]
    volumes: _containers.RepeatedCompositeFieldContainer[_persistentvolume_pb2.ChalkKubernetesPersistentVolume]
    def __init__(
        self,
        volumes: _Optional[_Iterable[_Union[_persistentvolume_pb2.ChalkKubernetesPersistentVolume, _Mapping]]] = ...,
    ) -> None: ...

class GetKubernetesServiceAccountsRequest(_message.Message):
    __slots__ = ("cluster_name", "namespace", "label_selector")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    namespace: str
    label_selector: str
    def __init__(
        self, cluster_name: _Optional[str] = ..., namespace: _Optional[str] = ..., label_selector: _Optional[str] = ...
    ) -> None: ...

class GetKubernetesServiceAccountsResponse(_message.Message):
    __slots__ = ("service_accounts",)
    SERVICE_ACCOUNTS_FIELD_NUMBER: _ClassVar[int]
    service_accounts: _containers.RepeatedCompositeFieldContainer[_serviceaccounts_pb2.KubernetesServiceAccount]
    def __init__(
        self,
        service_accounts: _Optional[_Iterable[_Union[_serviceaccounts_pb2.KubernetesServiceAccount, _Mapping]]] = ...,
    ) -> None: ...

class GetKubernetesAutoscalersRequest(_message.Message):
    __slots__ = ("cluster_name", "namespace", "label_selector")
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    cluster_name: str
    namespace: str
    label_selector: str
    def __init__(
        self, cluster_name: _Optional[str] = ..., namespace: _Optional[str] = ..., label_selector: _Optional[str] = ...
    ) -> None: ...

class GetKubernetesAutoscalersResponse(_message.Message):
    __slots__ = ("hpas", "scaledobjects")
    HPAS_FIELD_NUMBER: _ClassVar[int]
    SCALEDOBJECTS_FIELD_NUMBER: _ClassVar[int]
    hpas: _containers.RepeatedCompositeFieldContainer[_horizontalpodautoscaler_pb2.KubernetesHorizontalPodAutoscaler]
    scaledobjects: _containers.RepeatedCompositeFieldContainer[_scaledobject_pb2.KubernetesScaledObject]
    def __init__(
        self,
        hpas: _Optional[
            _Iterable[_Union[_horizontalpodautoscaler_pb2.KubernetesHorizontalPodAutoscaler, _Mapping]]
        ] = ...,
        scaledobjects: _Optional[_Iterable[_Union[_scaledobject_pb2.KubernetesScaledObject, _Mapping]]] = ...,
    ) -> None: ...

class GetKubernetesDeploymentsRequest(_message.Message):
    __slots__ = ("environment_id", "namespace", "label_selector")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    namespace: str
    label_selector: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        label_selector: _Optional[str] = ...,
    ) -> None: ...

class GetKubernetesDeploymentsResponse(_message.Message):
    __slots__ = ("deployments",)
    DEPLOYMENTS_FIELD_NUMBER: _ClassVar[int]
    deployments: _containers.RepeatedCompositeFieldContainer[_deployments_pb2.KubernetesDeployment]
    def __init__(
        self, deployments: _Optional[_Iterable[_Union[_deployments_pb2.KubernetesDeployment, _Mapping]]] = ...
    ) -> None: ...

class GetKubernetesStatefulSetsRequest(_message.Message):
    __slots__ = ("environment_id", "namespace", "label_selector")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    namespace: str
    label_selector: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        label_selector: _Optional[str] = ...,
    ) -> None: ...

class GetKubernetesStatefulSetsResponse(_message.Message):
    __slots__ = ("stateful_sets",)
    STATEFUL_SETS_FIELD_NUMBER: _ClassVar[int]
    stateful_sets: _containers.RepeatedCompositeFieldContainer[_statefulsets_pb2.KubernetesStatefulSet]
    def __init__(
        self, stateful_sets: _Optional[_Iterable[_Union[_statefulsets_pb2.KubernetesStatefulSet, _Mapping]]] = ...
    ) -> None: ...

class GetKubernetesJobsRequest(_message.Message):
    __slots__ = ("environment_id", "namespace", "label_selector")
    ENVIRONMENT_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    LABEL_SELECTOR_FIELD_NUMBER: _ClassVar[int]
    environment_id: str
    namespace: str
    label_selector: str
    def __init__(
        self,
        environment_id: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        label_selector: _Optional[str] = ...,
    ) -> None: ...

class GetKubernetesJobsResponse(_message.Message):
    __slots__ = ("jobs",)
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[_jobs_pb2.KubernetesJob]
    def __init__(self, jobs: _Optional[_Iterable[_Union[_jobs_pb2.KubernetesJob, _Mapping]]] = ...) -> None: ...

class GetKubernetesStatefulSetWithPodsRequest(_message.Message):
    __slots__ = ("stateful_set_name", "namespace", "cluster_name")
    STATEFUL_SET_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    stateful_set_name: str
    namespace: str
    cluster_name: str
    def __init__(
        self,
        stateful_set_name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        cluster_name: _Optional[str] = ...,
    ) -> None: ...

class GetKubernetesStatefulSetWithPodsResponse(_message.Message):
    __slots__ = ("stateful_set", "pods")
    STATEFUL_SET_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    stateful_set: _statefulsets_pb2.KubernetesStatefulSet
    pods: _containers.RepeatedCompositeFieldContainer[_pods_pb2.KubernetesPodData]
    def __init__(
        self,
        stateful_set: _Optional[_Union[_statefulsets_pb2.KubernetesStatefulSet, _Mapping]] = ...,
        pods: _Optional[_Iterable[_Union[_pods_pb2.KubernetesPodData, _Mapping]]] = ...,
    ) -> None: ...

class GetKubernetesJobWithPodsRequest(_message.Message):
    __slots__ = ("job_name", "namespace", "cluster_name")
    JOB_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    job_name: str
    namespace: str
    cluster_name: str
    def __init__(
        self, job_name: _Optional[str] = ..., namespace: _Optional[str] = ..., cluster_name: _Optional[str] = ...
    ) -> None: ...

class GetKubernetesJobWithPodsResponse(_message.Message):
    __slots__ = ("job", "pods")
    JOB_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    job: _jobs_pb2.KubernetesJob
    pods: _containers.RepeatedCompositeFieldContainer[_pods_pb2.KubernetesPodData]
    def __init__(
        self,
        job: _Optional[_Union[_jobs_pb2.KubernetesJob, _Mapping]] = ...,
        pods: _Optional[_Iterable[_Union[_pods_pb2.KubernetesPodData, _Mapping]]] = ...,
    ) -> None: ...

class GetKubernetesDeploymentWithPodsRequest(_message.Message):
    __slots__ = ("deployment_name", "namespace", "cluster_name")
    DEPLOYMENT_NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_NAME_FIELD_NUMBER: _ClassVar[int]
    deployment_name: str
    namespace: str
    cluster_name: str
    def __init__(
        self, deployment_name: _Optional[str] = ..., namespace: _Optional[str] = ..., cluster_name: _Optional[str] = ...
    ) -> None: ...

class GetKubernetesDeploymentWithPodsResponse(_message.Message):
    __slots__ = ("deployment", "pods")
    DEPLOYMENT_FIELD_NUMBER: _ClassVar[int]
    PODS_FIELD_NUMBER: _ClassVar[int]
    deployment: _deployments_pb2.KubernetesDeployment
    pods: _containers.RepeatedCompositeFieldContainer[_pods_pb2.KubernetesPodData]
    def __init__(
        self,
        deployment: _Optional[_Union[_deployments_pb2.KubernetesDeployment, _Mapping]] = ...,
        pods: _Optional[_Iterable[_Union[_pods_pb2.KubernetesPodData, _Mapping]]] = ...,
    ) -> None: ...
