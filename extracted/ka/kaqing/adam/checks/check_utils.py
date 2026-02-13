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
from adam.utils_cassandra.cassandra_status import CassandraStatus
from adam.utils_concurrent import parallelize
from adam.utils_context import NULL
from adam.utils_k8s.secrets import Secrets
from adam.utils_k8s.statefulsets import StatefulSets
from adam.utils_log import log2

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

def run_checks(cluster: str = None,
               namespace: str = None,
               pod: str = None,
               checks: list[Check] = None,
               find_issues=True,
               status: CassandraStatus = None,
               ctx = NULL):
    if not checks:
        checks = all_checks()

    sts_ns: list[tuple[str, str]] = StatefulSets.list_sts_name_and_ns()

    sts_ns_pods: list[tuple[str, str, str]] = []
    for sts, ns in sts_ns:
        if (not cluster or cluster == sts) and (not namespace or namespace == ns):
            if ns == status.namespace:
                for pod_name in status.pod_names():
                    if not pod or pod == pod_name:
                        sts_ns_pods.append((sts, ns, pod_name))
            else:
                pods = StatefulSets.pods(sts, ns)
                for pod_name in [pod.metadata.name for pod in pods]:
                    if not pod or pod == pod_name:
                        sts_ns_pods.append((sts, ns, pod_name))

    with parallelize(sts_ns_pods,
                     msg='d`Running|Ran checks on {size} pods') as exec:
        return exec.collect(lambda sts_ns_pod: run_checks_on_pod(checks, sts_ns_pod[0], sts_ns_pod[1], sts_ns_pod[2], find_issues=find_issues, status=status, ctx=ctx))

def run_checks_on_pod(checks: list[Check], sts: str = None, namespace: str = None, pod: str = None, find_issues = True, status: CassandraStatus = None, ctx = NULL):
    host_id = status.host_id_from_pod_name(pod)
    user, pw = Secrets.get_user_pass(pod, namespace)
    results = {}
    issues: list[Issue] = []
    for c in checks:
        check_results = c.check(CheckContext.from_exec(ctx, sts, host_id, pod, namespace, user, pw, find_issues=find_issues))
        if check_results.details:
            results = results | {check_results.name: check_results.details}
        if check_results.issues:
            issues.extend(check_results.issues)

    return CheckResult(None, results, issues)