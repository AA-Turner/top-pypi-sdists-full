from adam.commands.devices.devices import Devices
from adam.commands.export.utils_export import state_with_pod
from adam.commands.fs.utils_fs import find_pids_for_cluster
from adam.commands.reaper.utils_reaper import reaper
from adam.config import Config
from adam.repl_state import ReplState
from adam.utils import log2

def find_running_nodetool_tasks(subcommand: str, state: ReplState) -> list[list[str]]:
    lines = []
    processes = find_pids_for_cluster(state, [subcommand])
    for p in processes:
        l = [p.pod, p.cmd, p.pid, p.last_arg]
        lines.append(l)

    if subcommand == 'repair':
        with reaper(state) as http:
            response = http.get('repair_run?state=RUNNING', params={
                'cluster_name': 'all',
                'limit': Config().get('reaper.show-runs-batch', 10)
            })

            runs = response.json()
            if runs:
                for r in runs:
                    l = ['reaper', 'reaper', r['id'], '', r['state']]
                    lines.append(l)

    return lines

def abort_nodetool_tasks(state: ReplState, subcommand: str, processes: list[list[str]]):
    for p in processes:
        pod = p[0]
        cmd = p[1]
        id = p[2]

        if pod == 'reaper':
            with reaper(state) as http:
                http.put(f'repair_run/{id}/state/ABORTED')
        elif cmd == subcommand:
            log2(f'@{pod} bash kill -9 {id}')

            with state_with_pod(state, pod) as state1:
                Devices.of(state).bash(state, state1, ['kill', '-9', id])