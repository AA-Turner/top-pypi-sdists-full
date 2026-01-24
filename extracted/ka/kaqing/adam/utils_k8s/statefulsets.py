from datetime import datetime
import functools
import re
from typing import List, TypeVar, cast
from kubernetes import client

from .kube_context import KubeContext
from adam.utils import log2


T = TypeVar('T')

# utility collection on statefulsets; methods are all static
class StatefulSets:
    def list_sts(label_selector="app.kubernetes.io/name=cassandra") -> List[client.V1StatefulSet]:
        apps_v1_api = client.AppsV1Api()
        if ns := KubeContext.in_cluster_namespace():
            statefulsets = apps_v1_api.list_namespaced_stateful_set(ns, label_selector=label_selector)
        else:
            statefulsets = apps_v1_api.list_stateful_set_for_all_namespaces(label_selector=label_selector)

        return statefulsets.items

    @functools.lru_cache()
    def list_sts_name_and_ns():
        return [(statefulset.metadata.name, statefulset.metadata.namespace) for statefulset in StatefulSets.list_sts()]

    def list_sts_names():
        if not KubeContext.in_cluster_namespace():
            return [f"{sts}@{ns}" for sts, ns in StatefulSets.list_sts_name_and_ns()]
        else:
            return [f"{sts}" for sts, _ in StatefulSets.list_sts_name_and_ns()]

    def pods(sts_name: str, namespace: str) -> List[client.V1Pod]:
        v1 = client.CoreV1Api()

        # this filters out with labels first -> saves about 1 second
        # cassandra.datastax.com/cluster: cs-9834d85c68
        # cassandra.datastax.com/datacenter: cs-9834d85c68
        # cassandra.datastax.com/rack: default
        # cs-9834d85c68-cs-9834d85c68-default-sts-0
        # cs-d0767a536f-cs-d0767a536f-reaper-946969766-rws92
        groups = re.match(r'(.*?-.*?)-(.*?-.*?)-(.*?)-.*', sts_name)
        label_selector = f'cassandra.datastax.com/cluster={groups[1]},cassandra.datastax.com/datacenter={groups[2]},cassandra.datastax.com/rack={groups[3]}'

        pods = cast(List[client.V1Pod], v1.list_namespaced_pod(namespace, label_selector=label_selector).items)
        statefulset_pods = []

        for pod in pods:
            if pod.metadata.owner_references:
                for owner in pod.metadata.owner_references:
                    if owner.kind == "StatefulSet" and owner.name == sts_name:
                        statefulset_pods.append(pod)
                        break

        return statefulset_pods

    @functools.lru_cache()
    def pod_names(sts: str, ns: str):
        if not sts:
            return []

        return [pod.metadata.name for pod in StatefulSets.pods(sts, ns)]

    def restarted_at(ss: str, ns: str):
        # returns timestamp and if being rolled out
        restarted: float = 0.0

        apps_v1_api = client.AppsV1Api()
        statefulset = apps_v1_api.read_namespaced_stateful_set(name=ss, namespace=ns)
        spec = statefulset.spec
        status = statefulset.status
        if spec and spec.template and spec.template.metadata and spec.template.metadata.annotations and 'kubectl.kubernetes.io/restartedAt' in spec.template.metadata.annotations:
            s = spec.template.metadata.annotations['kubectl.kubernetes.io/restartedAt']
            dt_object = datetime.fromisoformat(s.replace('Z', ''))
            restarted = dt_object.timestamp()
            if status.current_revision != status.update_revision:
                return restarted, True

            if status.ready_replicas is not None and status.ready_replicas < spec.replicas:
                if status.current_revision == status.update_revision and status.updated_replicas is not None and status.updated_replicas < spec.replicas:
                    return restarted, True

        return restarted, False

    @functools.lru_cache()
    def get_datacenter(sts: str, ns: str) -> str:
        v1 = client.AppsV1Api()
        namespace = ns
        statefulset_name = sts
        try:
            s = v1.read_namespaced_stateful_set(name=statefulset_name, namespace=namespace)
            dc = s.metadata.labels['cassandra.datastax.com/datacenter']
            return dc
        except client.ApiException as e:
            log2(f"Error while executing get_datacenter, fetching datacenter: {e}")
        return None