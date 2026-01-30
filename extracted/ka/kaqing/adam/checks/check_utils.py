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
from adam.utils_context import Context
from adam.utils_k8s.cassandra_nodes import CassandraNodes
from adam.utils_k8s.secrets import Secrets
from adam.utils_k8s.statefulsets import StatefulSets
from adam.utils import parallelize, log2

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

def run_checks(cluster: str = None, namespace: str = None, pod: str = None, checks: list[Check] = None, ctx: Context = Context.NULL):
    if not checks:
        checks = all_checks()

    sts_ns: list[tuple[str, str]] = StatefulSets.list_sts_name_and_ns()

    sts_ns_pods: list[tuple[str, str, str]] = []
    for sts, ns in sts_ns:
        if (not cluster or cluster == sts) and (not namespace or namespace == ns):
            pods = StatefulSets.pods(sts, ns)
            for pod_name in [pod.metadata.name for pod in pods]:
                if not pod or pod == pod_name:
                    sts_ns_pods.append((sts, ns, pod_name))

    with parallelize(sts_ns_pods,
                     Config().action_workers('issues', 30),
                     msg='d`Running|Ran checks on {size} pods') as exec:
        return exec.map(lambda sts_ns_pod: run_checks_on_pod(checks, sts_ns_pod[0], sts_ns_pod[1], sts_ns_pod[2], ctx))

def run_checks_on_pod(checks: list[Check], cluster: str = None, namespace: str = None, pod: str = None, ctx: Context = Context.NULL):
    host_id = CassandraNodes.get_host_id(pod, namespace)
    user, pw = Secrets.get_user_pass(pod, namespace)
    results = {}
    issues: list[Issue] = []
    for c in checks:
        check_results = c.check(CheckContext.from_exec(ctx, cluster, host_id, pod, namespace, user, pw))
        if check_results.details:
            results = results | {check_results.name: check_results.details}
        if check_results.issues:
            issues.extend(check_results.issues)

    return CheckResult(None, results, issues)