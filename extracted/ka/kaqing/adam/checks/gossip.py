import re

from adam.checks.check import Check
from adam.checks.check_context import CheckContext
from adam.checks.check_result import CheckResult
from adam.checks.issue import Issue
from adam.utils import Color
from adam.utils_k8s.cassandra_nodes import CassandraNodes

class Gossip(Check):
    def name(self):
        return 'gossip'

    def check(self, ctx: CheckContext) -> CheckResult:
        issues: list[Issue] = []
        #   STATUS:23:NORMAL,-1215576004580455029
        # /172.0.201.227
        #   generation:1749575365
        #   heartbeat:2147483647
        #   STATUS:555372:shutdown,true
        #   LOAD:555418:7.340546332E9
        #   SCHEMA:17:06026fbd-8b70-3488-a497-8aeb080590da
        #   DC:13:cs-9834d85c68
        #   RACK:15:default
        #   RELEASE_VERSION:6:4.1.7
        #   NET_VERSION:2:12
        #   HOST_ID:3:aa56d161-8bbd-4f03-98e1-646321fb42ef
        #   RPC_READY:555373:false
        #   INTERNAL_ADDRESS_AND_PORT:9:172.0.201.227:7000
        #   NATIVE_ADDRESS_AND_PORT:4:172.0.201.227:9042
        #   STATUS_WITH_PORT:555371:shutdown,true
        #   SSTABLE_VERSIONS:7:big-nb
        #   TOKENS:21:<hidden>
        # STATUS line missing -> NORMAL
        # user, pw = get_user_pass(pod_name, ns)
        ctx_fg = ctx.copy(backgrounded=False, text_color=Color.gray)
        result = CassandraNodes.exec(ctx.pod, ctx.namespace, f"nodetool -u {ctx.user} -pw {ctx.pw} gossipinfo", ctx=ctx_fg)

        nodes = self.parse_gossipinfo(result.stdout)
        details = {
            'name': ctx.pod,
            'namespace': ctx.namespace,
            'statefulset': ctx.statefulset,
            'nodes': nodes
        }

        for node in nodes:
            if 'STATUS' in node and node['STATUS']['value'] == 'shutdown,true':
                host = node['HOST_ID']
                issues.append(Issue(
                    statefulset=ctx.statefulset,
                    namespace=ctx.namespace,
                    pod=ctx.pod,
                    host=host,
                    category='gossip',
                    desc=f'Gossip is down: {host}',
                    suggestion=f"qing restart {ctx.pod}@{ctx.namespace}"
                ))

        return CheckResult(self.name(), details, issues)

    def parse_gossipinfo(self, stdout: str):
        nodes = []

        node = None
        for line in stdout.split('\n'):
            line = line.strip(' \r')
            if line.startswith('/'):
                if node:
                    nodes.append(node)

                node = {'header': line}
            elif node and line:
                groups = re.match(r"(.*?):(.*?):(.*)", line)
                if groups:
                    node[groups[1]] = {
                        'index': groups[2],
                        'value': groups[3]
                    }
                else:
                    groups = re.match(r"(.*?):(.*)", line)
                    if groups:
                        node[groups[1]] = {
                            'index': groups[2]
                        }
        nodes.append(node)

        return nodes

    def help(self):
        return f'{Gossip().name()}: check if gossip is up with nodetool gossipinfo'