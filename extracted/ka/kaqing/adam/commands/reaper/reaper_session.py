from collections.abc import Callable
import threading
from kubernetes import client
import portforward
import re
import requests
from typing import List, cast

from adam.config import Config
from adam.k8s_utils.kube_context import KubeContext
from adam.repl_state import ReplState
from adam.utils import lines_to_tabular, log2

class ReaperSession:
    is_forwarding = False
    stopping = threading.Event()
    schedules_ids_by_cluster: dict[str, list[str]] = {}

    def __init__(self, pod: str, headers: dict[str, str] = None):
        self.pod = pod
        self.headers = headers

    def login(self, state: ReplState, local_addr: str, remote_addr: str, show_output = True) -> str :
        user, pw = state.user_pass(secret_path='reaper.secret')

        response = requests.post(f'http://{local_addr}/login', headers={
            'Accept': '*'
        },data={
            'username':user,
            'password':pw})
        if show_output:
            log2(f'POST {remote_addr}/login')
            log2(f'     username={user}&password={pw}')

        if int(response.status_code / 100) != 2:
            if show_output:
                log2("login failed")
            return None

        return response.headers['Set-Cookie']

    def port_forwarded(self, state: ReplState, path: str, body: Callable[[str, dict[str, str]], requests.Response], method: str = None, show_output = True):
        local_port = Config().get('reaper.port-forward.local-port', 9001)
        target_port = 8080

        def f(local_addr: str, remote_addr: str):
            if not self.headers:
                self.headers = self.cookie_header(state, local_addr, remote_addr, show_output=show_output)

            if show_output and method:
                log2(f'{method} {remote_addr}/{path}')
            response = body(f'http://{local_addr}/{path}', self.headers)

            if response:
                if int(response.status_code / 100) != 2:
                    if show_output:
                        log2(response.status_code)
                    return response

            if show_output:
                log2()

            return response if response else 'no-response'

        if KubeContext.in_cluster():
            # cs-a526330d23-cs-a526330d23-default-sts-0 ->
            # curl http://cs-a526330d23-cs-a526330d23-reaper-service.stgawsscpsr.svc.cluster.local:8080
            groups = re.match(r'^(.*?-.*?-.*?-.*?-).*', state.sts)
            if groups:
                svc_name = Config().get('reaper.service-name', 'reaper-service')
                svc = f'{groups[1]}{svc_name}.{state.namespace}.svc.cluster.local:{target_port}'
                return f(local_addr=svc, remote_addr=svc)
            else:
                return None
        else:
            with portforward.forward(state.namespace, self.pod, local_port, target_port):
                return f(local_addr=f'localhost:{local_port}', remote_addr=f'{self.pod}:{target_port}')

    def cookie_header(self, state: ReplState, local_addr, remote_addr, show_output = True):
        return {'Cookie': self.login(state, local_addr, remote_addr, show_output=show_output)}

    def create(state: ReplState) -> 'ReaperSession':
        pods = ReaperSession.list_reaper_pods(state.sts if state.sts else state.pod, state.namespace)
        if pods:
            return ReaperSession(pods[0].metadata.name)
        else:
            log2('No reaper found.')

            return None

    def list_reaper_pods(sts_name: str, namespace: str) -> List[client.V1Pod]:
        v1 = client.CoreV1Api()

        # k8ssandra.io/reaper: cs-d0767a536f-cs-d0767a536f-reaper
        groups = re.match(Config().get('reaper.pod.cluster-regex', r'(.*?-.*?-.*?-.*?)-.*'), sts_name)
        label_selector = Config().get('reaper.pod.label-selector', 'k8ssandra.io/reaper={cluster}-reaper').replace('{cluster}', groups[1])

        return cast(List[client.V1Pod], v1.list_namespaced_pod(namespace, label_selector=label_selector).items)

    def show_schedules(self, state: ReplState, filter: Callable[[list[dict]], dict] = None):
        schedules = self.list_schedules(state, filter=filter)
        # forced refresh of schedule list
        if not filter:
            self.schedules_ids_by_cluster[state.sts] = [schedule['id'] for schedule in schedules]
        self.show_schedules_tabular(schedules)

    def schedule_ids(self, state: ReplState, show_output = True, filter: Callable[[list[dict]], dict] = None):
        schedules = self.list_schedules(state, show_output=show_output, filter=filter)
        return [schedule['id'] for schedule in schedules]

    def list_schedules(self, state: ReplState, show_output = True, filter: Callable[[list[dict]], dict] = None) -> list[dict]:
        def body(uri: str, headers: dict[str, str]):
            return requests.get(uri, headers=headers)

        response = self.port_forwarded(state, 'repair_schedule', body, method='GET', show_output=show_output)
        if not response:
            return

        res = response.json()
        if filter:
            res = filter(res)

        return res

    def show_schedules_tabular(self, schedules: list[dict]):
        log2(lines_to_tabular([f"{schedule['id']} {schedule['state']} {schedule['cluster_name']} {schedule['keyspace_name']}" for schedule in schedules], 'ID STATE CLUSTER KEYSPACE'))

    def show_schedule(self, state: ReplState, schedule_id: str):
        def filter(schedules: list[dict]):
            return [schedule for schedule in schedules if schedule['id'] == schedule_id]

        self.show_schedules(state, filter)

    def reaper_spec(self, state: ReplState) -> dict[str, any]:
        user, pw = state.user_pass(secret_path='reaper.secret')
        local_port = Config().get('reaper.port-forward.local-port', 9001)

        return {
            'pod': self.pod,
            'exec': f'kubectl exec -it {self.pod} -n {state.namespace} -- bash',
            'forward': f'kubectl port-forward pods/{self.pod} -n {state.namespace} {local_port}:8080',
            'web-uri': f'http://localhost:{local_port}/webui',
            'username': user,
            'password': pw
        }

    def cached_schedule_ids(state: ReplState) -> list[str]:
        if state.sts in ReaperSession.schedules_ids_by_cluster:
            return ReaperSession.schedules_ids_by_cluster[state.sts]

        if reaper := ReaperSession.create(state):
            state.wait_log("Inspecting Cassandra Reaper...")

            schedules = reaper.schedule_ids(state, show_output = False)
            ReaperSession.schedules_ids_by_cluster[state.sts] = schedules

            return schedules

        return []