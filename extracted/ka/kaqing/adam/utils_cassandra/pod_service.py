import sys
from typing import Union

from adam.commands.command import Command
from adam.commands.cql.utils_cql import run_cql
from adam.utils_cassandra import cassandra_exec
from adam.utils_cassandra.cassandra_clusters import CassandraClusters
from adam.utils_cassandra.cassandra_nodes import CassandraNodes
from adam.utils_context import Context
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.repl_state import ReplState
from adam.utils_log import log2
from adam.utils_k8s.k8s_context import K8sContext
from adam.utils_k8s.statefulsets import StatefulSets

class CassandraPodService:
    def __init__(self, handler: 'CassandraExecHandler'):
        self.handler = handler

    def exec(self,
             command: str,
             action='bash',
             on_any = False,
             throw_err = False,
             shell = '/bin/sh',
             ctx: Context = Context.NULL) -> Union[PodExecResult, list[PodExecResult]]:
        return cassandra_exec.cassandra_exec(self.handler.state, self.handler.pod, command, action, on_any, throw_err, shell, ctx)

    def cql(self, args: list[str], opts: list = [], use_single_quotes = False, on_any = False, no_color = False, ctx: Context = Context.NULL):
        state = self.handler.state
        query: str = args

        if isinstance(query, list):
            opts = []
            cqls = []
            for arg in args:
                if arg.startswith('--'):
                    opts.append(arg)
                elif arg != '-e':
                    cqls.append(arg)
            if not cqls:
                if self.state.in_repl:
                    log2('Please enter cql statement. e.g. select host_id from system.local')
                else:
                    log2('* CQL statement is missing.')
                    log2()
                    Command.display_help()

                return 'no-cql'

            query = ' '.join(cqls)

        return run_cql(state, query, opts=opts, use_single_quotes=use_single_quotes, on_any=on_any, no_color=no_color, ctx=ctx)

    def nodetool(self, args: str, status = False, samples = sys.maxsize, k8s: K8sContext = K8sContext.NULL, ctx: Context = Context.NULL) -> Union[PodExecResult, list[PodExecResult]]:
        state = self.handler.state
        pod = self.handler.pod

        user, pw = state.user_pass()
        command = f"nodetool -u {user} -pw {pw} {args}"

        if pod:
            return CassandraNodes.exec(pod, state.namespace, command, ctx=ctx)
        else:
            return CassandraClusters.exec(state.sts,
                                          state.namespace,
                                          command,
                                          action='nodetool.status' if status else 'nodetool',
                                          samples=samples,
                                          k8s=k8s,
                                          ctx=ctx)
    def pod_names(self):
        state = self.handler.state

        return StatefulSets.pod_names(state.sts, state.namespace)

    def pod_name_n_ips(self):
        state = self.handler.state

        return StatefulSets.pod_name_n_ips(state.sts, state.namespace)

    def pods(self):
        state = self.handler.state

        return StatefulSets.pods(state.sts, state.namespace)

class CassandraExecHandler:
    def __init__(self, state: ReplState, pod: str = None):
        self.state = state
        self.pod = pod
        if not pod and state.pod:
            self.pod = state.pod

    def __enter__(self):
        return CassandraPodService(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def cassandra(state: ReplState, pod: str=None):
    return CassandraExecHandler(state, pod=pod)
