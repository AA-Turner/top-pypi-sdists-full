import sys
from typing import Iterator

from adam.utils import log_timing
from adam.utils_context import Context
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_k8s.pods import Pods
from adam.utils_k8s.statefulsets import StatefulSets

# utility collection on cassandra clusters; methods are all static
class CassandraClusters:
    def exec(sts: str,
             namespace: str,
             command: str,
             action: str = 'action',
             max_workers=0,
             on_any = False,
             shell = '/bin/sh',
             samples = sys.maxsize,
             ctx: Context = Context.NULL) -> list[PodExecResult]:
        results: list[PodExecResult] = []

        # filter out pods that're reported as non-runnig by k8s API server
        pod_names = log_timing('running.pods', lambda: StatefulSets.running_pods(sts, namespace))
        if not pod_names:
            # no pod was reported as runnning; just try with the non-running pods
            pod_names = StatefulSets.pod_names(sts, namespace)

        # emulate pod failure
        # pod_names = ['cs-a7b13e29bd-cs-a7b13e29bd-default-sts-0', 'cs-a7b13e29bd-cs-a7b13e29bd-default-sts-9', 'cs-a7b13e29bd-cs-a7b13e29bd-default-sts-1', 'cs-a7b13e29bd-cs-a7b13e29bd-default-sts-2']

        if on_any:
            samples = 1

        # 1. If 3 samples are requested out of 96 nodes, first 32 pods are examined concurrently.
        # 2. If at least 3 samples are acquired, the method returns with the first 3 samples.
        # 3. If not all 3 samples are acquired, the next 32 pods are examined concurrently, and so on.
        # 4. After all 96 nodes are examined, if the number of samples is less than 3, the samples are returned.
        s = min(len(pod_names), max(samples * 3, int(len(pod_names) / 3)))

        # emulate more than one batch
        # s = 3

        pns = pod_names[:s]
        pod_names = pod_names[s:]

        results: list[PodExecResult] = []
        while samples and pns:
            msg = 'd`Running|Ran ' + action + ' command onto {size} pods'
            with log_timing(f'Pods.parallelize({len(pns)})'):
                with Pods.parallelize(pns, max_workers, -1, msg, collect=False, action=action) as exec:
                    rs: Iterator[PodExecResult] = exec.map(lambda pod: CassandraNodes.exec(pod, namespace, command, False, shell, ctx.copy(show_out=False)))

                    for r in rs:
                        if not r.client_err and r.exit_code() == 0:
                            results.append(r)

                            samples -= 1
                            if not samples:
                                break

            if s < len(pod_names):
                pns = pod_names[:s]
                pod_names = pod_names[s:]
            else:
                pns = pod_names
                pod_names = []

        if not ctx.debug:
            for r in results:
                ctx.log(r.command)
                r.log(ctx)

        return results

    def pod_names_by_host_id(sts: str, ns: str):
        pods = StatefulSets.pods(sts, ns)

        return {CassandraNodes.get_host_id(pod.metadata.name, ns): pod.metadata.name for pod in pods}