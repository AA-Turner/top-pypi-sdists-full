from typing import Union

from adam.repl_state import ReplState
from adam.utils_cassandra.cassandra_clusters import CassandraClusters
from adam.utils_cassandra.cassandra_nodes import CassandraNodes
from adam.utils_context import NULL
from adam.utils_k8s.pod_exec_result import PodExecResult

def cassandra_exec(state: ReplState,
                   pod: str,
                   command: str,
                   action='bash',
                   on_any = False,
                   throw_err = False,
                   shell = '/bin/sh',
                   ctx = NULL) -> Union[PodExecResult, list[PodExecResult]]:
    if pod:
        return CassandraNodes.exec(pod,
                                    state.namespace,
                                    command,
                                    throw_err=throw_err,
                                    shell=shell,
                                    ctx=ctx)
    elif state.sts:
        return CassandraClusters.exec(state.sts,
                                        state.namespace,
                                        command,
                                        action=action,
                                        on_any=on_any,
                                        shell=shell,
                                        ctx=ctx)

    return []