from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from adam.checks.check import Check
from adam.checks.check_context import CheckContext
from adam.checks.check_result import CheckResult
from adam.checks.compactionstats import CompactionStats
from adam.checks.cpu import Cpu
from adam.checks.disk import Disk
from adam.checks.gossip import Gossip
from adam.checks.issue import Issue
from adam.checks.memory import Memory
from adam.checks.status import Status
from adam.config import Config
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.k8s_utils.kube_context import KubeContext
from adam.k8s_utils.secrets import Secrets
from adam.k8s_utils.statefulsets import StatefulSets
from adam.utils import elapsed_time, log2

def all_checks() -> list[Check]:
    return [CompactionStats(), Cpu(), Gossip(), Memory(), Disk(), Status()]

def checks_from_csv(check_str: str):
    checks: list[Check] = []

    checks_by_name = {c.name(): c for c in all_checks()}

    if check_str:
        for check_name in check_str.strip(' ').split(','):
            if check_name in checks_by_name:
                checks.append(checks_by_name[check_name])
            else:
                log2(f'Invalid check name: {check_name}.')

                return None

    return checks

def run_checks(cluster: str = None, namespace: str = None, pod: str = None, checks: list[Check] = None, show_output=True):
    if not checks:
        checks = all_checks()

    sss: list[tuple[str, str]] = StatefulSets.list_sts_name_and_ns()

    action = 'issues'
    crs: list[CheckResult] = []

    def on_clusters(f: Callable[[any, list[str]], any]):
        for ss, ns in sss:
            if (not cluster or cluster == ss) and (not namespace or namespace == ns):
                pods = StatefulSets.pods(ss, ns)
                for pod_name in [pod.metadata.name for pod in pods]:
                    if not pod or pod == pod_name:
                        f(ss, ns, pod_name, show_output)

    max_workers = Config().action_workers(action, 30)
    if max_workers < 2:
        def serial(ss, ns, pod_name, show_output):
            if not pod or pod == pod_name:
                crs.append(run_checks_on_pod(checks, ss[0], ns, pod_name, show_output))

        on_clusters(serial)
    else:
        if KubeContext.show_parallelism():
            log2(f'Executing on all nodes from statefulset with {max_workers} workers...')
        start_time = time.time()
        try:
            futures = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                def submit(ss, ns, pod_name, show_output):
                    f = executor.submit(run_checks_on_pod, checks, ss, ns, pod_name, show_output,)
                    if f: futures.append(f)

                on_clusters(submit)

            crs = [future.result() for future in as_completed(futures)]
        finally:
            if KubeContext.show_parallelism():
                log2(f"Parallel {action} elapsed time: {elapsed_time(start_time)} with {max_workers} workers")

    return crs

def run_checks_on_pod(checks: list[Check], cluster: str = None, namespace: str = None, pod: str = None, show_output=True):
    host_id = CassandraNodes.get_host_id(pod, namespace)
    user, pw = Secrets.get_user_pass(pod, namespace)
    results = {}
    issues: list[Issue] = []
    for c in checks:
        check_results = c.check(CheckContext(cluster, host_id, pod, namespace, user, pw, show_output=show_output))
        if check_results.details:
            results = results | {check_results.name: check_results.details}
        if check_results.issues:
            issues.extend(check_results.issues)

    return CheckResult(None, results, issues)