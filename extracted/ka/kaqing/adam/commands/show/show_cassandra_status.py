import sys

from adam.checks.check_result import CheckResult
from adam.checks.check_utils import run_checks
from adam.checks.compactionstats import CompactionStats
from adam.checks.gossip import Gossip
from adam.columns.columns import Columns
from adam.commands.command import Command
from adam.commands.issues import Issues
from adam.config import Config
from adam.k8s_utils.cassandra_nodes import CassandraNodes
from adam.k8s_utils.secrets import Secrets
from adam.k8s_utils.statefulsets import StatefulSets
from adam.repl_state import ReplState, RequiredState
from adam.utils import lines_to_tabular, log, log2
from adam.checks.status import parse_nodetool_status

class ShowCassandraStatus(Command):
    COMMAND = 'show cassandra status'

    # the singleton pattern
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'): cls.instance = super(ShowCassandraStatus, cls).__new__(cls)

        return cls.instance

    def __init__(self, successor: Command=None):
        super().__init__(successor)

    def command(self):
        return ShowCassandraStatus.COMMAND

    def required(self):
        return RequiredState.CLUSTER_OR_POD

    def run(self, cmd: str, state: ReplState):
        if not(args := self.args(cmd)):
            return super().run(cmd, state)

        state, args = self.apply_state(args, state)
        if not self.validate_state(state):
            return state

        args, show_output = Command.extract_options(args, ['-s', '--show'])

        if state.namespace and state.pod:
            # self.show_table(state, [state.pod], state.namespace, show_output=show_output)
            self.show_single_pod(state.sts, state.pod, state.namespace, show_output=show_output)
        elif state.namespace and state.sts:
            self.merge(state.sts, StatefulSets.pod_names(state.sts, state.namespace), state.namespace, Config().get('nodetool.samples', sys.maxsize), show_output=show_output)

        return state

    def show_single_pod(self, statefulset: str, pod_name: str, ns: str, show_output = False):
        pod_name = pod_name.split('(')[0]
        user, pw = Secrets.get_user_pass(pod_name, ns)
        try:
            result = CassandraNodes.exec(pod_name, ns, f"nodetool -u {user} -pw {pw} status", show_out=False)
            status = parse_nodetool_status(result.stdout)
            check_results = run_checks(cluster=statefulset, namespace=ns, checks=[CompactionStats(), Gossip()], show_output=show_output)
            self.show_table(status, check_results)
        except Exception as e:
            log2(e)

    def merge(self, statefulset: str, pod_names: list[str], ns: str, samples: int, show_output=False):
        statuses: list[list[dict]] = []
        for pod_name in pod_names:
            pod_name = pod_name.split('(')[0]
            user, pw = Secrets.get_user_pass(pod_name, ns)

            try:
                result = CassandraNodes.exec(pod_name, ns, f"nodetool -u {user} -pw {pw} status", show_out=False)
                status = parse_nodetool_status(result.stdout)
                if status:
                    statuses.append(status)
                if samples <= len(statuses) and len(pod_names) != len(statuses):
                    break
            except Exception as e:
                log2(e)

        combined_status = self.merge_status(statuses)
        log2(f'Showing merged status from {len(statuses)}/{len(pod_names)} nodes...')
        check_results = run_checks(cluster=statefulset, namespace=ns, checks=[CompactionStats(), Gossip()], show_output=show_output)
        self.show_table(combined_status, check_results)

        return combined_status

    def merge_status(self, statuses: list[list[dict]]):
        combined = statuses[0]

        status_by_host = {}
        for status in statuses[0]:
            status_by_host[status['host_id']] = status
        for status in statuses[1:]:
            for s in status:
                if s['host_id'] in status_by_host:
                    c = status_by_host[s['host_id']]
                    if c['status'] == 'UN' and s['status'] == 'DN':
                        c['status'] = 'DN*'
                else:
                    combined.append(s)

        return combined

    def show_table(self, status: list[dict[str, any]], check_results: list[CheckResult]):
        cols = Config().get('status.columns', 'status,address,load,tokens,owns,host_id,gossip,compactions')
        header = Config().get('status.header', '--,Address,Load,Tokens,Owns,Host ID,GOSSIP,COMPACTIONS')
        columns = Columns.create_columns(cols)

        def line(status: dict):
            cells = [c.host_value(check_results, status) for c in columns]
            return ','.join(cells)

        lines = [line(d) for d in status]
        lines.sort()

        log(lines_to_tabular(lines, header, separator=','))

        Issues.show(check_results)

    def completion(self, state: ReplState):
        if state.sts:
            return super().completion(state)

        return {}

    def help(self, _: ReplState):
        return f'{ShowCassandraStatus.COMMAND} [-s]\t show merged nodetool status  -s show commands on nodes'