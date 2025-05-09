# autogenerated module
from typing import List, Optional, TYPE_CHECKING

from ._schema import dataclass, field, DictMixin

if TYPE_CHECKING:   # Fix for pycharm autocompletion https://youtrack.jetbrains.com/issue/PY-54560
    from dataclasses import dataclass, field

from . import meta_v1


@dataclass
class CrossVersionObjectReference(DictMixin):
    r"""CrossVersionObjectReference contains enough information to let you identify
      the referred resource.

      **parameters**

      * **kind** ``str`` - kind is the kind of the referent; More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **name** ``str`` - name is the name of the referent; More info:
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
      * **apiVersion** ``Optional[str]`` - apiVersion is the API version of the referent
    """
    kind: 'str'
    name: 'str'
    apiVersion: 'Optional[str]' = None


@dataclass
class HorizontalPodAutoscaler(DictMixin):
    r"""configuration of a horizontal pod autoscaler.

      **parameters**

      * **apiVersion** ``Optional[str]`` - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``Optional[str]`` - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``Optional[meta_v1.ObjectMeta]`` - Standard object metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
      * **spec** ``Optional[HorizontalPodAutoscalerSpec]`` - spec defines the behaviour of autoscaler. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.
      * **status** ``Optional[HorizontalPodAutoscalerStatus]`` - status is the current information about the autoscaler.
    """
    apiVersion: 'Optional[str]' = None
    kind: 'Optional[str]' = None
    metadata: 'Optional[meta_v1.ObjectMeta]' = None
    spec: 'Optional[HorizontalPodAutoscalerSpec]' = None
    status: 'Optional[HorizontalPodAutoscalerStatus]' = None


@dataclass
class HorizontalPodAutoscalerList(DictMixin):
    r"""list of horizontal pod autoscaler objects.

      **parameters**

      * **items** ``List[HorizontalPodAutoscaler]`` - items is the list of horizontal pod autoscaler objects.
      * **apiVersion** ``Optional[str]`` - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``Optional[str]`` - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``Optional[meta_v1.ListMeta]`` - Standard list metadata.
    """
    items: 'List[HorizontalPodAutoscaler]'
    apiVersion: 'Optional[str]' = None
    kind: 'Optional[str]' = None
    metadata: 'Optional[meta_v1.ListMeta]' = None


@dataclass
class HorizontalPodAutoscalerSpec(DictMixin):
    r"""specification of a horizontal pod autoscaler.

      **parameters**

      * **maxReplicas** ``int`` - maxReplicas is the upper limit for the number of pods that can be set by the
        autoscaler; cannot be smaller than MinReplicas.
      * **scaleTargetRef** ``CrossVersionObjectReference`` - reference to scaled resource; horizontal pod autoscaler will learn the current
        resource consumption and will set the desired number of pods by using its
        Scale subresource.
      * **minReplicas** ``Optional[int]`` - minReplicas is the lower limit for the number of replicas to which the
        autoscaler can scale down.  It defaults to 1 pod.  minReplicas is allowed to
        be 0 if the alpha feature gate HPAScaleToZero is enabled and at least one
        Object or External metric is configured.  Scaling is active as long as at
        least one metric value is available.
      * **targetCPUUtilizationPercentage** ``Optional[int]`` - targetCPUUtilizationPercentage is the target average CPU utilization
        (represented as a percentage of requested CPU) over all the pods; if not
        specified the default autoscaling policy will be used.
    """
    maxReplicas: 'int'
    scaleTargetRef: 'CrossVersionObjectReference'
    minReplicas: 'Optional[int]' = None
    targetCPUUtilizationPercentage: 'Optional[int]' = None


@dataclass
class HorizontalPodAutoscalerStatus(DictMixin):
    r"""current status of a horizontal pod autoscaler

      **parameters**

      * **currentReplicas** ``int`` - currentReplicas is the current number of replicas of pods managed by this
        autoscaler.
      * **desiredReplicas** ``int`` - desiredReplicas is the  desired number of replicas of pods managed by this
        autoscaler.
      * **currentCPUUtilizationPercentage** ``Optional[int]`` - currentCPUUtilizationPercentage is the current average CPU utilization over
        all pods, represented as a percentage of requested CPU, e.g. 70 means that an
        average pod is using now 70% of its requested CPU.
      * **lastScaleTime** ``Optional[meta_v1.Time]`` - lastScaleTime is the last time the HorizontalPodAutoscaler scaled the number
        of pods; used by the autoscaler to control how often the number of pods is
        changed.
      * **observedGeneration** ``Optional[int]`` - observedGeneration is the most recent generation observed by this autoscaler.
    """
    currentReplicas: 'int'
    desiredReplicas: 'int'
    currentCPUUtilizationPercentage: 'Optional[int]' = None
    lastScaleTime: 'Optional[meta_v1.Time]' = None
    observedGeneration: 'Optional[int]' = None


@dataclass
class Scale(DictMixin):
    r"""Scale represents a scaling request for a resource.

      **parameters**

      * **apiVersion** ``Optional[str]`` - APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``Optional[str]`` - Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``Optional[meta_v1.ObjectMeta]`` - Standard object metadata; More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.
      * **spec** ``Optional[ScaleSpec]`` - spec defines the behavior of the scale. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.
      * **status** ``Optional[ScaleStatus]`` - status is the current status of the scale. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.
        Read-only.
    """
    apiVersion: 'Optional[str]' = None
    kind: 'Optional[str]' = None
    metadata: 'Optional[meta_v1.ObjectMeta]' = None
    spec: 'Optional[ScaleSpec]' = None
    status: 'Optional[ScaleStatus]' = None


@dataclass
class ScaleSpec(DictMixin):
    r"""ScaleSpec describes the attributes of a scale subresource.

      **parameters**

      * **replicas** ``Optional[int]`` - replicas is the desired number of instances for the scaled object.
    """
    replicas: 'Optional[int]' = None


@dataclass
class ScaleStatus(DictMixin):
    r"""ScaleStatus represents the current status of a scale subresource.

      **parameters**

      * **replicas** ``int`` - replicas is the actual number of observed instances of the scaled object.
      * **selector** ``Optional[str]`` - selector is the label query over pods that should match the replicas count.
        This is same as the label selector but in the string format to avoid
        introspection by clients. The string will be in the same format as the
        query-param syntax. More info about label selectors:
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
    """
    replicas: 'int'
    selector: 'Optional[str]' = None


