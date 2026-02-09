from kubernetes import client

from adam.utils_log import log_timing
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets

class K8sContext:
    def preload_pods(sts: str, namespace: str):
        context = K8sContext()

        context.pods(sts, namespace)

        return context

    def __init__(self):
        self._pods: list[client.V1Pod] = None

    # does not seem updating reliably - reports Running when Down
    def pods(self, sts: str, namespace: str) -> list[client.V1Pod]:
        if not self._pods:
            self._pods = StatefulSets.pods(sts, namespace)

        return self._pods

    def pod_names(self, sts: str, namespace: str):
        return [Pods.pod_name(p) for p in self.pods(sts, namespace)]

    def running_pods(self, sts: str, namespace: str):
        return [Pods.pod_name(p) for p in self.pods(sts, namespace) if Pods.pod_status(p) == 'Running']

K8sContext.NULL = K8sContext()