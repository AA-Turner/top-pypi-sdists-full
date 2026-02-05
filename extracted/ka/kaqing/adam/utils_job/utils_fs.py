import itertools
import re

from adam.commands.devices.devices import device
from adam.repl_state import ReplState
from adam.utils import Color
from adam.utils_tabulize import tabulize
from adam.utils_context import Context
from adam.utils_k8s.pod_exec_result import PodExecResult
from adam.utils_k8s.pods import Pods

def proc_for_pid(pod: str, container: str, namespace: str, pid: str, ctx: Context = Context.NULL) -> list['ProcessInfo']:
    awk = "awk '{ print $1, $2, $8, $NF }'"
    cmd = f"ps -fp {pid} | tail -n +2 | {awk}"

    r: PodExecResult = Pods.exec(pod, container, namespace, cmd, ctx.copy(text_color=Color.gray))
    return ProcessInfo.from_find_process_results(r)

def find_pids_for_cluster(state: ReplState, keywords: list[str], match_last_arg = False, kill = False) -> list['ProcessInfo']:
    container = device(state).default_container(state)

    action = 'find-procs'
    msg = 'd`Running|Ran ' + action + ' onto {size} pods'
    pods = device(state).pod_names(state)
    with Pods.parallelize(pods, len(pods), msg=msg, action=action) as exec:
        r: list[list[ProcessInfo]] = exec.map(lambda pod: find_pids_for_pod(pod, container, state.namespace, keywords, match_last_arg=match_last_arg, kill=kill))

        return list(itertools.chain.from_iterable(r))

def find_pids_for_pod(pod: str, container: str, namespace: str, keywords: list[str], match_last_arg = False, kill = False, ctx: Context = Context.NULL) -> list['ProcessInfo']:
    r: PodExecResult = Pods.exec(pod, container, namespace, _find_procs_command(keywords), ctx.copy(text_color=Color.gray))

    procs: list[ProcessInfo] = ProcessInfo.from_find_process_results(r, last_arg = keywords[-1] if match_last_arg else None)

    if kill:
        for proc in procs:
            Pods.exec(pod, container, namespace, f'kill -9 {proc.pid}', ctx.copy(show_out=True, text_color=Color.gray))

    return procs

def _find_procs_command(keywords: list[str]):
    regex_pattern = re.compile(r'[^\w\s]')

    greps = []
    for a in keywords:
        a = a.strip('"\'').strip(' ')

        if a and not regex_pattern.search(a):
            greps.append(f'grep -- {a}')

    awk = "awk '{ print $1, $2, $8, $NF }'"

    return f"ps -ef | grep -v grep | {' | '.join(greps)} | {awk}"

class ProcessInfo:
    header = 'POD\tUSER\tPID\tCMD\tLAST_ARG'

    def __init__(self, user: str, pid: str, cmd: str, last_arg: str, pod: str = None):
        self.user = user
        self.pid = pid
        self.cmd = cmd
        self.last_arg = last_arg
        self.pod = pod

    def from_find_process_results(rs: PodExecResult, last_arg: str = None):
        processes: list[ProcessInfo] = []

        for l in rs.stdout.split('\n'):
            l = l.strip(' \t\r\n')
            if not l:
                continue

            tokens = l.split(' ')
            if last_arg and tokens[3] != last_arg:
                continue

            processes.append(ProcessInfo(tokens[0], tokens[1], tokens[2], tokens[3], pod=rs.pod))

        return processes

    def table_line(self):
        return '\t'.join([self.pod, self.user, self.pid, self.cmd, self.last_arg])

    def tabulize(processes: list['ProcessInfo'], ctx: Context = Context.NULL):
        tabulize(processes,
                 lambda p: p.table_line(),
                 header = ProcessInfo.header,
                 separator='\t',
                 ctx=ctx.copy(show_out=True))

class LogLine(ProcessInfo):
    header='ORDINAL\tPID\tEXIT_CODE\tCMD\tLAST_ARG\tOUT_SIZE\tERR_SIZE\tLOG(ERR)_FILES'

    def __init__(self, ordinal: str = '-', exit_code: str = '-', out: str = '-', err: str = '-', file: str = '-', user: str = '-', pid: str = '-', cmd: str = '-', last_arg: str = '-', pod: str = '-'):
        super().__init__(user, pid, cmd, last_arg, pod)
        self.ordinal = ordinal
        self.exit_code = exit_code
        self.out = out
        self.err = err
        self.file = file

    def __repr__(self):
        return f"LogLine({', '.join([self.ordinal, self.pid, self.exit_code, self.cmd, self.last_arg, self.out, self.err, self.file])})"

    def table_line(self):
        return '\t'.join([self.ordinal, self.pid, self.exit_code, self.cmd, self.last_arg, self.out, self.err, self.file if self.err not in ['-', '0'] else self.file.replace('.err', '.log')])

    def merge(self, process: ProcessInfo):
        self.user = process.user
        # self.pid = process.pid
        self.exit_code = 'Running'
        self.cmd = process.cmd
        self.last_arg = process.last_arg
        self.pod = process.pod
