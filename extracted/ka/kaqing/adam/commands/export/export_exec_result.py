from adam.commands.export.utils_export import ExportSpec, ExportTableStatus
from adam.utils_local import LocalExecResult

class ExportExecResult(LocalExecResult):
    def __init__(self, stdout: str = None, stderr: str = None, command: str = None, exit_code = 0, log_file: str = None, job_id: str = None,
                 spec: ExportSpec = None, statuses: list[ExportTableStatus] = None):
        super().__init__(stdout, stderr, command, exit_code, log_file, job_id)
        self.spec = spec
        self.statuses = statuses

    def exit_code(self) -> int:
        return self.code

    def cat_log_file_cmd(self):
        if self.pod and self.log_file:
            return f'@{self.pod} cat {self.log_file}'

        return None

    def get_job_id(self) -> str:
        return self.job_id

    def header(self) -> str:
        return self.spec.session if self.spec else self.job_id

    def __str__(self):
        return f'{"OK" if self.exit_code() == 0 else self.exit_code()} {self.command}'

    def __audit_extra__(self):
        return self.log_file if self.log_file else None