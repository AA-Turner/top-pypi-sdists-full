from adam.presentation.utils_table_render import show_table
from adam.utils_context import NULL
from adam.utils_repl.repl_state import ReplState
from adam.utils_k8s.statefulsets import StatefulSets

class TableRenderer:
    def __init__(self, handler: 'CassandraRendererHandler'):
        self.handler = handler

    def display_table(self, cols: str, header: str, find_issues = True, ctx = NULL):
        ctx.submit(lambda: self._display_table(cols, header, find_issues=find_issues, ctx=ctx))

    def _display_table(self, cols: str, header: str, find_issues=True, ctx = NULL):
        state = self.handler.state

        if state.pod:
            show_table(state, [state.pod], cols, header, find_issues=find_issues, ctx=ctx)
        elif state.sts:
            pod_names = [pod.metadata.name for pod in StatefulSets.pods(state.sts, state.namespace)]
            show_table(state, pod_names, cols, header, find_issues=find_issues, ctx=ctx)

class CassandraRendererHandler:
    def __init__(self, state: ReplState, pod: str = None):
        self.state = state
        self.pod = pod
        if not pod and state.pod:
            self.pod = state.pod

    def __enter__(self):
        return TableRenderer(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

def renderer(state: ReplState, pod: str=None):
    return CassandraRendererHandler(state, pod=pod)
