from collections.abc import Callable
from functools import partial
from typing import List, cast
from kubernetes import client
import re

import requests
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import Color, convert_seconds, epoch, log2, wait_log
from adam.utils_tabulize import tabulize
from adam.utils_context import Context
from adam.utils_k8s.k8s import port_forwarding

class ReaperService:
    def __init__(self, state: ReplState, local_addr: str, remote_addr: str, show_out = True):
        self.state = state
        self.local_addr = local_addr
        self.remote_addr = remote_addr
        self.show_out = show_out
        self.headers = None

    def get(self, path: str, params: dict[str, any] = {}):
        with logging(self, 'GET', path) as (url, headers):
            return requests.get(url, headers=headers, params=params)

    def put(self, path: str, params: dict[str, any] = {}):
        with logging(self, 'PUT', path) as (url, headers):
            return requests.put(url, headers=headers, params=params)

    def post(self, path: str, params: dict[str, any] = {}):
        with logging(self, 'POST', path) as (url, headers):
            return requests.post(url, headers=headers, params=params)

class ReaperLoggingHandler:
    def __init__(self, svc: ReaperService, method: str, path: str):
        self.svc = svc
        self.method = method
        self.path = path

    def __enter__(self) -> tuple[str, dict[str, any]]:
        if not self.svc.headers:
            self.svc.headers = Reapers.cookie_header(self.svc.state, self.svc.local_addr, self.svc.remote_addr, show_output=self.svc.show_out)

        if self.svc.show_out and self.method:
            log2(f'{self.method} {self.svc.remote_addr}/{self.path}', text_color=Color.gray)

        return (f'http://{self.svc.local_addr}/{self.path}', self.svc.headers)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val and isinstance(exc_val, requests.Response):
            if int(exc_val.status_code / 100) != 2:
                if self.svc.show_out:
                    log2(exc_val.status_code)

        return False

def logging(svc: ReaperService, method: str, path: str):
    return ReaperLoggingHandler(svc, method, path)

class ReaperHandler:
    def __init__(self, state: ReplState, show_out = True):
        self.state = state
        self.show_out = show_out
        self.headers = None
        self.forwarding = None

    def __enter__(self):
        self.forwarding = port_forwarding(self.state, Reapers.local_port(), partial(Reapers.svc_or_pod, self.state), Reapers.target_port())
        (local_addr, remote_addr) = self.forwarding.__enter__()

        return ReaperService(self.state, local_addr, remote_addr, show_out=self.show_out)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.forwarding:
            return self.forwarding.__exit__(exc_type, exc_val, exc_tb)

        return False

def reaper(state: ReplState, show_out = True):
    return ReaperHandler(state, show_out=show_out)

class Reapers:
    schedules_ids_by_cluster: dict[str, list[str]] = {}

    def pod_name(state: ReplState):
        pods = Reapers.list_reaper_pods(state.sts if state.sts else state.pod, state.namespace)
        if pods:
            return pods[0].metadata.name

        return None

    def show_schedule(state: ReplState, schedule_id: str, ctx: Context = Context.NULL):
        def filter(schedules: list[dict]):
            return [schedule for schedule in schedules if schedule['id'] == schedule_id]

        Reapers.show_schedules(state, filter, ctx=ctx)

    def show_schedules(state: ReplState, filter: Callable[[list[dict]], dict] = None, ctx: Context = Context.NULL):
        schedules = Reapers.list_schedules(state, filter=filter)

        # forced refresh of schedule list
        if not filter:
            Reapers.schedules_ids_by_cluster[state.sts] = [schedule['id'] for schedule in schedules]

        tabulize(schedules,
                 lambda s: f"{s['id']} {s['state']} {s['cluster_name']} {s['keyspace_name']}",
                 header='ID STATE CLUSTER KEYSPACE',
                 err=True,
                 ctx=ctx.copy(show_out=True))

    def schedule_ids(state: ReplState, show_output = True, filter: Callable[[list[dict]], dict] = None):
        schedules = Reapers.list_schedules(state, show_output=show_output, filter=filter)
        return [schedule['id'] for schedule in schedules]

    def list_schedules(state: ReplState, show_output = True, filter: Callable[[list[dict]], dict] = None) -> list[dict]:
        with reaper(state, show_out=show_output) as requests:
            if not (response := requests.get('repair_schedule')):
                return

            res = response.json()
            if filter:
                res = filter(res)

            return res

    def list_reaper_pods(sts_name: str, namespace: str) -> List[client.V1Pod]:
        v1 = client.CoreV1Api()

        # k8ssandra.io/reaper: cs-d0767a536f-cs-d0767a536f-reaper
        groups = re.match(Config().get('reaper.pod.cluster-regex', r'(.*?-.*?-.*?-.*?)-.*'), sts_name)
        label_selector = Config().get('reaper.pod.label-selector', 'k8ssandra.io/reaper={cluster}-reaper').replace('{cluster}', groups[1])

        return cast(List[client.V1Pod], v1.list_namespaced_pod(namespace, label_selector=label_selector).items)

    def cookie_header(state: ReplState, local_addr, remote_addr, show_output = True):
        return {'Cookie': Reapers.login(state, local_addr, remote_addr, show_output=show_output)}

    def login(state: ReplState, local_addr: str, remote_addr: str, show_output = True) -> str :
        user, pw = state.user_pass(secret_path='reaper.secret')

        response = requests.post(f'http://{local_addr}/login', headers={
            'Accept': '*'
        },data={
            'username':user,
            'password':pw})
        if show_output:
            log2(f'POST {remote_addr}/login', text_color=Color.gray)
            log2(f'      username={user}&password={pw}', text_color=Color.gray)

        if int(response.status_code / 100) != 2:
            if show_output:
                log2("login failed", text_color=Color.gray)
            return None

        return response.headers['Set-Cookie']

    def reaper_spec(state: ReplState) -> dict[str, any]:
        if not (pod := Reapers.pod_name(state)):
            return {}

        user, pw = state.user_pass(secret_path='reaper.secret')

        return {
            'pod': pod,
            'exec': f'kubectl exec -it {pod} -n {state.namespace} -- bash',
            'forward': f'kubectl port-forward pods/{pod} -n {state.namespace} {Reapers.local_port()}:{Reapers.target_port()}',
            'web-uri': f'http://localhost:{Reapers.local_port()}/webui',
            'username': user,
            'password': pw
        }

    def cached_schedule_ids(state: ReplState) -> list[str]:
        if state.sts in Reapers.schedules_ids_by_cluster:
            return Reapers.schedules_ids_by_cluster[state.sts]

        if pod := Reapers.pod_name(state):
            wait_log('Inspecting Cassandra Reaper...')

            schedules = Reapers.schedule_ids(state, show_output = False)
            Reapers.schedules_ids_by_cluster[state.sts] = schedules

            return schedules

        return []

    def svc_name():
        return Config().get('reaper.service-name', 'reaper-service')

    def local_port():
        return Config().get('reaper.port-forward.local-port', 9001)

    def target_port():
        return 8080

    def svc_or_pod(state: ReplState, is_service: bool):
        if is_service:
            return Reapers.svc_name()
        else:
            return Reapers.pod_name(state)

    def schedules_auto_completion(ids: callable):
        auto = Config().get('reaper.schedules-auto-complete', 'off')

        leaf = None
        if auto == 'on':
            leaf = {id: None for id in ids()}

        return (leaf, auto == 'lazy')

    def tabulize_runs(state: ReplState, response: dict, ctx: Context = Context.NULL) -> dict[str, any]:
        header = 'ID,START,DURATION,STATE,CLUSTER,KEYSPACE,TABLES,REPAIRED'

        def line(run):
            id = run['id']
            state = run['state']
            start_time = run['start_time']
            end_time = run['end_time']
            duration = '-'
            if state == 'DONE' and end_time:
                hours, minutes, seconds = convert_seconds(epoch(end_time) - epoch(start_time))
                if hours:
                    duration = f"{hours:2d}h {minutes:2d}m {seconds:2d}s"
                elif minutes:
                    duration = f"{minutes:2d}m {seconds:2d}s"
                else:
                    duration = f"{seconds:2d}s"

            return f"{id},{start_time},{duration},{state},{run['cluster_name']},{run['keyspace_name']},{len(run['column_families'])},{run['segments_repaired']}/{run['total_segments']}"

        runs = response.json()
        if runs:
            tabulize(sorted([line(run) for run in runs], reverse=True),
                     header=header,
                     separator=",",
                     ctx=ctx.copy(show_out=True))

        return runs