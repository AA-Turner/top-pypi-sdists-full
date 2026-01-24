from collections.abc import Callable
import inspect
import re
import portforward

from adam.commands.command import InvalidStateException
from adam.repl_state import ReplState
from adam.utils import log2
from adam.utils_k8s.kube_context import KubeContext

class PortForwardHandler:
    connections: dict[str, int] = {}

    def __init__(self, state: ReplState, local_port: int, svc_or_pod: Callable[[bool],str], target_port: int):
        self.state = state
        self.local_port = local_port
        self.svc_or_pod = svc_or_pod
        self.target_port = target_port
        self.forward_connection = None
        self.pod = None

    def __enter__(self) -> tuple[str, str]:
        state = self.state

        if not self.svc_or_pod:
            log2('No service or pod found.')

            raise InvalidStateException(state)

        if KubeContext.in_cluster():
            svc_name = self.svc_or_pod(True)
            if not svc_name:
                log2('No service found.')

                raise InvalidStateException(state)

            # cs-a526330d23-cs-a526330d23-default-sts-0 ->
            # curl http://cs-a526330d23-cs-a526330d23-reaper-service.stgawsscpsr.svc.cluster.local:8080
            groups = re.match(r'^(.*?-.*?-.*?-.*?-).*', state.sts)
            if groups:
                svc = f'{groups[1]}{svc_name}.{state.namespace}.svc.cluster.local:{self.target_port}'
                return (svc, svc)
            else:
                raise InvalidStateException(state)
        else:
            pod = self.svc_or_pod(False)
            if not pod:
                log2('No pod found.')

                raise InvalidStateException(state)

            self.pod = pod

            # pf = portforward.forward(state.namespace, pod, self.local_port + 1, self.target_port, log_level=portforward.LogLevel.DEBUG)
            # print(inspect.getsource(pf.__enter__))
            # print('test portforward START', state.namespace, pod, self.local_port + 1, self.target_port, pf.__enter__)
            # with pf:
            #     print('test portforward BODY')
            # print('test portforward OK')

            self.forward_connection = portforward.forward(state.namespace, pod, self.local_port, self.target_port)
            if self.inc_connection_cnt() == 1:
                self.forward_connection.__enter__()

            return (f'localhost:{self.local_port}', f'{pod}:{self.target_port}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.forward_connection:
            if not self.dec_connection_cnt():
                return self.forward_connection.__exit__(exc_type, exc_val, exc_tb)

        return False

    def inc_connection_cnt(self):
        id = self.connection_id(self.pod)
        if id not in PortForwardHandler.connections:
            PortForwardHandler.connections[id] = 1
        else:
            PortForwardHandler.connections[id] += 1

        return PortForwardHandler.connections[id]

    def dec_connection_cnt(self):
        id = self.connection_id(self.pod)
        if id not in PortForwardHandler.connections:
            PortForwardHandler.connections[id] = 0
        elif PortForwardHandler.connections[id] > 0:
            PortForwardHandler.connections[id] -= 1

        return PortForwardHandler.connections[id]

    def connection_id(self, pod: str):
        return f'{self.local_port}:{pod}:{self.target_port}'

def port_forwarding(state: ReplState, local_port: int, svc_or_pod: Callable[[bool],str], target_port: int):
    return PortForwardHandler(state, local_port, svc_or_pod, target_port)