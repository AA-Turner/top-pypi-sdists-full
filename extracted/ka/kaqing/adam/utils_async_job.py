from datetime import datetime
import re
import traceback
from typing import TextIO, Union

from adam.repl_session import ReplSession
from adam.utils import ExecResult, log2, log_dir

class AsyncJobs:
    _last_command: 'CommandInfo' = None

    def local_log_file(command: str, job_id: str = None, err = False, dir: str = None, extra: dict[str, str] = {}):
        try:
            if not job_id:
                job_id = AsyncJobs.new_id()

            cmd = CommandInfo(command, job_id, extra)
            AsyncJobs._last_command = cmd
            AsyncJobs.write_last_command(cmd)

            cmd_name = ''
            if command.startswith('nodetool '):
                command = command.strip(' &')
                cmd_name = f".{'_'.join(command.split(' ')[5:])}"

            if not dir:
                dir = log_dir()

            return f'{dir}/{job_id}{cmd_name}.{"err" if err else "log"}'
        except:
            traceback.print_exc()

    def pod_log_file(command: str, pod_name: str = None, job_id: str = None, pod_suffix: str = None, err = False, dir: str = None, extra: dict[str, str] = {}):
        try:
            if not job_id:
                job_id = AsyncJobs.new_id()

            cmd = CommandInfo(command, job_id, extra)
            AsyncJobs._last_command = cmd
            AsyncJobs.write_last_command(cmd)

            cmd_name = ''
            if command.startswith('nodetool '):
                command = command.strip(' &')
                cmd_name = f".{'_'.join(command.split(' ')[5:])}"

            if pod_suffix is None:
                pod_suffix = '{pod}'
                if pod_name:
                    pod_suffix = pod_name
                    if groups := re.match(r'.*-(.*)', pod_name):
                        pod_suffix = f'-{groups[1]}'

            if not dir:
                dir = log_dir()

            return f'{dir}/{job_id}{cmd_name}{pod_suffix}.{"err" if err else "log"}'
        except:
            traceback.print_exc()

    def new_id(dt: datetime = None):
        if not dt:
            dt = datetime.now()

        id = dt.strftime("%d%H%M%S")
        AsyncJobs._last_command = CommandInfo(job_id=id)

        return id

    def last_command():
        if cmd := AsyncJobs._last_command:
            return cmd

        cmd = AsyncJobs.read_last_command()
        AsyncJobs._last_command = cmd

        return cmd

    def write_last_command(cmd: 'CommandInfo'):
        with open(f'{log_dir()}/last', 'wt') as f:
            cmd.write(f)

    def read_last_command() -> 'CommandInfo':
        with open(f'{log_dir()}/last', 'rt') as f:
            return CommandInfo.read(f)

    def print_start(r: Union[ExecResult, list[ExecResult]]):
        if r and isinstance(r, list):
            r = r[0]

        if r and isinstance(r, ExecResult) and (header := r.header()):
            log2(f'[{header}] Use :? to get the results.')

    def new_job(cmd: str, backgrounded = True) -> str:
        if not backgrounded:
            return None

        job_id = AsyncJobs.new_id()
        job_log = AsyncJobs.local_log_file(cmd, job_id)
        ReplSession().append_history(f':cat {job_log}')

        log2(f'[{job_id}] Use :? to get the results.')

        return job_log

class CommandInfo:
    def __init__(self, command: str = None, job_id: str = None, extra: dict[str, str] = {}):
        self.command = command
        self.job_id = job_id
        self.extra = extra

    def read(f: TextIO):
        job_id = None
        command = None
        extra: dict[str, str] = {}
        try:
            job_id = f.readline().strip(' \r\n')
            command = f.readline().strip(' \r\n')
            while(e := f.readline().strip(' \r\n')):
                if groups := re.match(r'(.*?):(.*)', e):
                    extra[groups[1]] = groups[2].strip(' \r\n')
        except:
            pass

        return CommandInfo(command, job_id, extra)

    def write(self, f: TextIO):
        f.write(self.job_id)
        f.write('\n')
        f.write(self.command)
        if self.extra:
            for k, v in self.extra.items():
                f.write('\n')
                f.write(f'{k}: {v}')