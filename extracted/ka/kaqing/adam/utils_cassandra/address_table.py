from copy import copy
import threading

from adam.utils_log import log_timing
from adam.utils_cassandra.cassandra_status import CassandraStatus
from adam.utils_cassandra.pod_service import cassandra
from adam.utils_context import Context
from adam.repl_state import ReplState
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_net import is_valid_ip

class AddressTable:
    # additive; remembers last ip to pod mappings
    pods_by_ip: dict[str, str] = {}
    ips_by_pod: dict[str, str] = {}
    host_ids_by_pod: dict[str, str] = {}
    pod_names_by_host_id: dict[str, str] = {}

    lock = threading.Lock()

    def snapshot(state: ReplState, ctx: Context = Context.NULL):
        host_ids_by_ip = {}

        try:
            with log_timing('AddressTable.snapshot'):
                with cassandra(state.with_no_pod()) as pods:
                    cql = 'select broadcast_address, host_id from system.local; select peer, host_id from system.peers'
                    result: PodExecResult = pods.cql(cql, ctx=ctx.copy(show_out=ctx.debug), no_color=True, on_any=True)
                    if isinstance(result, list):
                        result = result[0]

                    for line in result.stdout.splitlines():
                        if line:
                            #    172.18.6.43 | 87625c74-b1f3-4694-b4e7-e6b9dec4bcb5
                            tokens = [t.strip(' \r\n\t') for t in line.strip(' ').split('|')]
                            if len(tokens) == 2 and is_valid_ip(tokens[0]):
                                host_ids_by_ip[tokens[0]] = tokens[1]

                    for pod, ip in pods.pod_name_n_ips():
                        with AddressTable.lock:
                            AddressTable.pods_by_ip[ip] = pod
                            AddressTable.ips_by_pod[pod] = ip
                            if ip in host_ids_by_ip:
                                host_id = host_ids_by_ip[ip]
                                AddressTable.host_ids_by_pod[pod] = host_id
                                AddressTable.pod_names_by_host_id[host_id] = pod

        except Exception as e:
            # traceback.print_exc()
            pass

        return AddressTable(copy(AddressTable.host_ids_by_pod))

    def __init__(self, host_ids_by_pod: dict):
        self._host_ids_by_pod = host_ids_by_pod
        self._status: list[dict] = None

    def local_ip_from_pod_name(self, pod_name: str, default: str = None) -> str:
        with AddressTable.lock:
            if pod_name not in AddressTable.ips_by_pod:
                if default:
                    return default

                raise NATError(f'Cannot locate local ip from pod: {pod_name}.', self)

            return AddressTable.ips_by_pod[pod_name]

    def pod_name_from_local_ip(self, local_ip: str, default: str = None) -> str:
        with AddressTable.lock:
            if local_ip not in AddressTable.pods_by_ip:
                if default:
                    return default

                raise NATError(f'Cannot locate pod name from local ip: {local_ip}.', self)

            return AddressTable.pods_by_ip[local_ip]

    def host_id_from_pod_name(self, pod_name: str, default: str = None) -> str:
        with AddressTable.lock:
            if pod_name not in AddressTable.host_ids_by_pod:
                if default:
                    return default

                raise NATError(f'Cannot locate host id from pod: {pod_name}.', self)

            return AddressTable.host_ids_by_pod[pod_name]

    def pod_name_from_host_id(self, host_id: str, default: str = None) -> str:
        with AddressTable.lock:
            if host_id not in AddressTable.pod_names_by_host_id:
                if default:
                    return default

                raise NATError(f'Cannot locate pod from host_id: {host_id}.', self)

            return AddressTable.pod_names_by_host_id[host_id]

    def status_by_host_id(self, state: ReplState):
        return {s['host_id']: s for s in self.status(state)}

    def status_by_ip(self, state: ReplState):
        return {s['address']: s for s in self.status(state)}

    def status_by_pod_name(self, state: ReplState):
        return {s['address']: s for s in self.status(state)}

    def status(self, state: ReplState):
        if not self._status:
            self._status = CassandraStatus.snapshot(state).status

        return self._status

class NATError(Exception):
    def __init__(self, message, nat: AddressTable = None):
        super().__init__(message)
        self.nat = nat
