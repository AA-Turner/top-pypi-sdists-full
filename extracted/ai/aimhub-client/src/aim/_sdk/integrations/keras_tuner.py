from typing import Optional, List

from aim._sdk.types.run import Run

try:
    from kerastuner.engine.tuner_utils import TunerCallback
except ImportError:
    raise RuntimeError(
        'This contrib module requires KerasTuner to be installed. '
        'Please install it with command: \n pip install keras-tuner'
    )


class AimCallback(TunerCallback):
    def __init__(self, tuner=None,
                 repo: Optional[str] = None,
                 experiment: Optional[str] = None,
                 log_system_params: Optional[bool] = True,
                 ):
        self.tuner = tuner
        self._repo_path = repo
        self._experiment_name = experiment
        self._log_system_params = log_system_params

        self._started_trials: List[str] = []
        self.trial = None
        self._run = None

    @property
    def experiment(self) -> Run:
        if self._run is not None:
            return self._run

    def on_epoch_begin(self, epoch, logs=None):
        trial_dict = self.tuner.oracle.ongoing_trials
        tuner_key = next(iter(trial_dict))
        self._current_trial_id = trial_dict[tuner_key].trial_id
        if self._current_trial_id not in self._started_trials:
            if self._repo_path is None:
                self._run = Run()
            else:
                self._run = Run(repo=self._repo_path)
            if self._experiment_name is not None:
                self._run.experiment = self._experiment_name
            if self._log_system_params:
                self._run.enable_system_monitoring()
            self._run['trial_id'] = self._current_trial_id
            self._started_trials.append(self._current_trial_id)
        trial = self.tuner.oracle.get_trial(self._current_trial_id)
        hparams = trial.hyperparameters.values
        for key in hparams:
            self._run.set(key, hparams[key], strict=False)

    def on_batch_end(self, batch, logs=None):
        if logs:
            for log_name, log_value in logs.items():
                self._run.track(log_value, name=log_name)

    def __del__(self):
        if self._run is not None and self._run.active:
            self._run.close()
