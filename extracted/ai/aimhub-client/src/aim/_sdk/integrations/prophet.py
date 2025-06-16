from typing import Any, Dict, Optional, TypeVar

from aim._sdk.types.run import Run

Prophet = TypeVar("Prophet")


class AimLogger:
    def __init__(
        self,
        prophet_model: Prophet,
        repo: Optional[str] = None,
        experiment: Optional[str] = None,
        log_system_params: Optional[bool] = True,
    ):
        """
        AimLogger for Prophet models.
        Prophet doesn't have a callback system and isn't trained iteratively.
        Thus, only the hyperparameters and user-provided metrics are logged.
        """
        self._repo_path = repo
        self._experiment = experiment
        self._log_system_params = log_system_params
        self._run = None
        self._run_hash = None
        self.setup(prophet_model.__dict__)

    @property
    def experiment(self) -> Run:
        if not self._run:
            self.setup()
        return self._run

    def setup(self, hparams: Dict[str, Any]) -> None:
        """
        Sets up a Run and logs hyperparameters (this method is only used in the constructor).
        """
        if self._run:
            return
        if self._run_hash:
            self._run = Run(self._run_hash, repo=self._repo_path)
        else:
            self._run = Run(repo=self._repo_path)
            if self._experiment is not None:
                self._run.experiment = self._experiment
            self._run_hash = self._run.hash
        if self._log_system_params:
            self._run.enable_system_monitoring()

        for hparam, value in hparams.items():
            self._run.set(hparam, value, strict=False)

    def __del__(self) -> None:
        if self._run and self._run.active:
            self._run.close()

    def track_metrics(
        self,
        metrics: Dict[str, float],
        context: Dict = None,
    ) -> None:
        """
        Since Prophet doesn't compute loss during training,
        only hyperparameters are logged by default.
        This method can be used to log any user-provied metrics.
        NOTE: if context is not provided, it's assumed all metrics are validation metrics.
        """
        if context is None:
            context = {"subset": "val"}
        for metric, value in metrics.items():
            self._run.track(value, name=metric, context=context)
