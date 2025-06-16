from typing import Optional

from aim._sdk.types.run import Run
from .keras_mixins import TrackerKerasCallbackMetricsEpochEndMixin

try:
    from keras.callbacks import Callback
except ImportError:
    raise RuntimeError(
        'This contrib module requires keras to be installed. '
        'Please install it with command: \n pip install keras'
    )


class AimCallback(TrackerKerasCallbackMetricsEpochEndMixin, Callback):
    def __init__(self, repo: Optional[str] = None,
                 experiment: Optional[str] = None,
                 log_system_params: Optional[bool] = True,
                 ):
        super(Callback, self).__init__()

        self._log_system_params = log_system_params

        if repo is None:
            self._run = Run()
        else:
            self._run = Run(repo=repo)
        if experiment is not None:
            self._run.experiment = experiment
        if log_system_params:
            self._run.enable_system_monitoring()

        self._run_hash = self._run.hash
        self._repo_path = repo

    @property
    def experiment(self) -> Run:
        if not self._run:
            self._run = Run(self._run_hash, repo=self._repo_path)
            if self._log_system_params:
                self._run.enable_system_monitoring()
        return self._run

    @classmethod
    def metrics(cls, repo: Optional[str] = None,
                experiment: Optional[str] = None,
                run: Optional[Run] = None):
        # Keep `metrics` method for backward compatibility
        return cls(repo, experiment, run)

    def close(self) -> None:
        if self._run:
            self._run.close()
            del self._run
            self._run = None

    def __del__(self):
        self.close()


# Keep `AimTracker` for backward compatibility
AimTracker = AimCallback
