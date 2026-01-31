from datetime import datetime
import os
import re
import traceback
from typing import TextIO

from adam.utils import log_dir

class AsyncJobs:
    _last_command: 'CommandInfo' = None
    _show_restarts_command: 'CommandInfo' = None
    _commands: dict[str, 'CommandInfo'] = {}

    def local_log_file(command: str, job_id: str = None, err = False, dir: str = None, extra: dict[str, str] = {}):
        try:
            job_id, cmd_name = AsyncJobs.job_n_cmd_name(job_id, command, extra)

            if not dir:
                dir = log_dir()

            return f'{dir}/{job_id}{cmd_name}.{"err" if err else "log"}'
        except:
            traceback.print_exc()

    def pod_log_file(command: str, pod_name: str = None, job_id: str = None, pod_suffix: str = None, suffix = '.log', err = False, dir: str = None, extra: dict[str, str] = {}):
        try:
            # for export, local file creates the last file, then pods will try to create the last file again
            job_id, cmd_name = AsyncJobs.job_n_cmd_name(job_id, command, extra, replace_last_file = False)

            if pod_suffix is None:
                pod_suffix = '{pod}'
                if pod_name:
                    pod_suffix = pod_name
                    if groups := re.match(r'.*-(.*)', pod_name):
                        pod_suffix = f'-{groups[1]}'

            if not dir:
                dir = log_dir()

            if suffix:
                return f'{dir}/{job_id}{cmd_name}{pod_suffix}{suffix}'

            return f'{dir}/{job_id}{cmd_name}{pod_suffix}.{"err" if err else "log"}'
        except:
            traceback.print_exc()

    def job_n_cmd_name(job_id: str, command: str, extra: dict[str, str], replace_last_file = True):
        if not job_id:
            job_id = AsyncJobs.new_id()

        if command:
            cmd = CommandInfo(command, job_id, extra)
            if AsyncJobs.write_last_command(cmd, replace=replace_last_file):
                AsyncJobs._last_command = cmd
                AsyncJobs._commands[job_id] = cmd

            if (tks := command.split(' ')) and tks[0] == 'restart' and tks[1] == 'nodes':
                AsyncJobs._show_restarts_command = cmd

        cmd_name = ''
        if command and command.startswith('nodetool '):
            command = command.strip(' &')
            cmd_name = command.split(' ')[-1]
            if cmd_name:
                cmd_name = f'-{cmd_name}'

        return job_id, cmd_name

    def new_id(dt: datetime = None):
        if not dt:
            dt = datetime.now()

        id = dt.strftime("%d%H%M%S")
        AsyncJobs._last_command = CommandInfo(job_id=id)

        return id

    def last_command(job_id: str = None):
        if job_id:
            if job_id in AsyncJobs._commands:
                return AsyncJobs._commands[job_id]

            return None
        else:
            if cmd := AsyncJobs._last_command:
                return cmd

            cmd = AsyncJobs.read_last_command()
            AsyncJobs._last_command = cmd

            return cmd

    def commands():
        return AsyncJobs._commands

    def show_restarts_command():
        return AsyncJobs._show_restarts_command

    def write_last_command(cmd: 'CommandInfo', replace = True):
        file = f'{log_dir()}/last'

        if not replace and os.path.exists(file):
            return False

        with open(file, 'wt') as f:
            cmd.write(f)

        return True

    def read_last_command() -> 'CommandInfo':
        path = f'{log_dir()}/last'
        with open(path, 'rt') as f:
            return CommandInfo.read(f)

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