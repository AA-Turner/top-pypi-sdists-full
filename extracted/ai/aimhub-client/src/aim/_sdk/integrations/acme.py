from typing import Optional, Dict
from aim._sdk.types.run import Run
from acme.utils.loggers.base import Logger, LoggingData


class AimCallback:
    def __init__(
        self,
        repo: Optional[str] = None,
        experiment_name: Optional[str] = None,
        log_system_params: Optional[bool] = True,
        args: Optional[Dict] = None,
    ):
        self.repo = repo
        self.experiment_name = experiment_name
        self.log_system_params = log_system_params
        self._run = None
        self._run_hash = None

        self.setup(args)

    @property
    def experiment(self):
        if not self._run:
            self.setup()
        return self._run

    def setup(self, args=None):
        if not self._run:
            if self._run_hash:
                self._run = Run(self._run_hash, repo=self.repo)
            else:
                self._run = Run(repo=self.repo)
                if self.experiment_name is not None:
                    self._run.experiment = self.experiment_name
                self._run_hash = self._run.hash
            if self.log_system_params:
                self._run.enable_system_monitoring()

        if args:
            for key, value in args.items():
                self._run.set(key, value, strict=False)

    def track(self, logs, step=None, context=None):
        self._run.track(logs, step=step, context=context)

    def close(self):
        if self._run and self._run.active:
            self._run.close()


class AimWriter(Logger):
    def __init__(self, aim_run, logger_label, steps_key, task_id):
        self.aim_run = aim_run
        self.logger_label = logger_label
        self.steps_key = steps_key
        self.task_id = task_id

    def write(self, values: LoggingData):
        self.aim_run.track(values, context={"logger_label": self.logger_label})

    def close(self):
        if self.aim_run and self.aim_run.active:
            self.aim_run.close()
