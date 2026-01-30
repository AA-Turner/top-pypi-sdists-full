import os
import subprocess
import traceback

from adam.config import Config
from adam.utils import ExecResult, creating_dir, debug

def local_qing_dir():
    return creating_dir(Config().get('local-qing-dir', '/tmp/qing-db/q'))

def local_downloads_dir():
    return creating_dir(Config().get('local-downloads-dir', '/tmp/qing-db/q/downloads'))

class LocalExecResult(ExecResult):
    def __init__(self, stdout: str, stderr: str, command: str = None, exit_code = 0, log_file: str = None, job_id: str = None):
        self.stdout: str = stdout
        self.stderr: str = stderr
        self.command: str = command
        self.code = exit_code
        self.pod = 'local'
        self.log_file = log_file
        self.job_id = job_id

    def exit_code(self) -> int:
        return self.code

    def cat_log_file_cmd(self):
        if self.log_file:
            return f':cat {self.log_file}'

        return None

    def get_job_id(self) -> str:
        return self.job_id

    def header(self) -> str:
        return self.job_id

    def __str__(self):
        return f'{"OK" if self.exit_code() == 0 else self.exit_code()} {self.command}'

    def __audit_extra__(self):
        return self.log_file if self.log_file else None

    def from_completed_process(command: str, p: subprocess.CompletedProcess):
        return LocalExecResult(stdout=p.stdout, stderr=p.stderr, command=command, exit_code=p.returncode)

def local_exec(cmd: list[str], shell=False, show_out=False):
    stdout = ''
    stderr = ''
    returncode = 0

    try:
        if show_out:
            debug(' '.join(cmd))

        r = subprocess.run(cmd, capture_output=True, text=True, shell=shell)
        stdout = r.stdout
        stderr = r.stderr
        returncode = r.returncode
    except FileNotFoundError as e:
        pass

    return LocalExecResult(stdout, stderr, ' '.join(cmd), returncode)

def find_local_files(pattern: str = f'{local_qing_dir()}/*', file_type: str = None, max_depth = 0, mmin: int = 0):
    # find . -maxdepth 1 -type f -name '*'
    log_files = []
    try:
        dir = os.path.dirname(pattern)
        base = os.path.basename(pattern)
        cmd = ['find', dir]
        if file_type:
            cmd += ['-type', file_type]
        if max_depth:
            cmd += ['-maxdepth', str(max_depth)]
        if mmin:
                cmd += ['-mmin',  f'-{mmin}']
        cmd += ['-name', base]

        stdout = local_exec(cmd, show_out=Config().is_debug()).stdout

        for line in stdout.split('\n'):
            line = line.strip(' \r')
            if line:
                log_files.append(line)
    except:
        traceback.print_exc()

    return log_files