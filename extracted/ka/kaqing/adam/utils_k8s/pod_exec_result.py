import yaml

from adam.utils import ExecResult, log_exc
from adam.utils_context import Context

class PodExecResult(ExecResult):
    # {
    #   'metadata': {},
    #   'status': 'Failure',
    #   'message': 'command terminated with non-zero exit code: error executing command [/bin/sh -c cqlsh -u cs-9834d85c68-superuser -p 07uV-5ogoDro9e7NDXvN  -e "select name"], exit code 2',
    #   'reason': 'NonZeroExitCode',
    #   'details': {
    #     'causes': [
    #       {
    #         'reason': 'ExitCode',
    #         'message': '2'
    #       }
    #     ]
    #   }
    # }
    def __init__(self, stdout: str, stderr: str, command: str = None, error_output: str = None, pod: str = None, log_file: str = None, job_id: str = None):
        self.stdout: str = stdout
        self.stderr: str = stderr
        self.command: str = command
        if error_output:
            self.error = yaml.safe_load(error_output)
        self.pod = pod
        self.log_file = log_file
        self.job_id = job_id

    def exit_code(self) -> int:
        code = 0

        with log_exc(False):
            code = self.error['details']['causes'][0]['message']

        return code

    def cat_log_file_cmd(self):
        if self.pod and self.log_file:
            return f'@{self.pod} cat {self.log_file}'

        return None

    def get_job_id(self) -> str:
        return self.job_id

    def header(self) -> str:
        return self.job_id

    def log(self, ctx: Context):
        # ctx.log(self.command)
        if self.stdout:
            ctx.log(self.stdout)
        if self.stderr:
            ctx.log2(self.stderr)
        if not self.stdout and not self.stderr:
            ctx.log(self.error if self.exit_code() else 'OK')

    def __str__(self):
        return f'{"OK" if self.exit_code() == 0 else self.exit_code()} {self.command}'

    def __audit_extra__(self):
        return self.log_file if self.log_file else None