# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import logging
from typing import Any, Dict, List, Optional

import comet_ml
from comet_ml.dataclasses import hidden_api_key

import ray._private.worker as worker
import ray.tune.experiment
import ray.tune.logger

from ...constants import OTHER_KEY_CREATED_FROM
from . import (
    callback_helpers,
    controller_flush_patcher,
    trial_result_logger,
    trial_save_logger,
)
from ._version_compat import USE_USER_CALLBACK
from .callback_helpers import strip_injected_keys

if USE_USER_CALLBACK:
    from ray.train import UserCallback as _RayCallbackBase
else:
    from ray.tune.logger import (  # type: ignore[assignment]
        LoggerCallback as _RayCallbackBase,
    )

Trial = ray.tune.experiment.Trial

LOGGER = logging.getLogger(__name__)


class CometTrainLoggerCallback(_RayCallbackBase):
    """
    Ray Callback for logging Train results to Comet.

    This Ray Train callback sends metrics and parameters to Comet for tracking.
    On Ray Train V2 (Ray >= 2.43 with ``RAY_TRAIN_V2_ENABLED=1``, the default
    since 2.51) it inherits from ``ray.train.UserCallback``; on older Ray it
    inherits from ``ray.tune.logger.LoggerCallback``. The selection is made at
    import time based on what ``ray.train`` exposes.

    This callback is based on the Ray native Comet callback and has been modified to allow to track
    resource usage on all distributed workers when running a distributed training job. It cannot be
    used with Ray Tune.

    Args:
        ray_config: Ray configuration dictionary to share with workers.
            It must be the same dictionary instance, not a copy.
        tags: Tags to add to the logged Experiment.
        save_checkpoints: If `True`, model checkpoints will be saved to
            Comet ML as artifacts.
        share_api_key_to_workers: If `True`, Comet API key will be shared
            with workers via ray_config dictionary. This is an unsafe solution and we recommend you
            uses a [more secure way to set up your API Key in your
            cluster](/docs/v2/guides/tracking-ml-training/distributed-training/).
        experiment_name: Custom name for the Comet experiment. If ``None``, a name
            is generated automatically.
        api_key (string): Comet API key.
        workspace (string): Comet workspace name.
        project_name (string): Comet project name.
        experiment_key (string): Experiment key to be used for logging.
        mode (string): Controls how the Comet experiment is started, 3 options are possible:

            - "get": Continue logging to an existing experiment identified by the `experiment_key` value.
            - "create": Always creates of a new experiment, useful for HPO sweeps.
            - "get_or_create" (default): Starts a fresh experiment if required, or persists logging to an existing one.
        online (bool): if True, the data will be logged to Comet server, otherwise it will be stored locally in offline experiment.
        experiment_kwargs: Other keyword arguments will be passed to the
            constructor for comet_ml.Experiment.

    Return: None

    Example:
        ```python linenums="1"
        config = {"lr": 1e-3, "batch_size": 64, "epochs": 20}

        comet_callback = CometTrainLoggerCallback(
            config,
            tags=["torch_ray_callback"],
            save_checkpoints=True,
            share_api_key_to_workers=True,
        )

        trainer = TorchTrainer(
            train_func,
            train_loop_config=config,
            scaling_config=ScalingConfig(num_workers=num_workers, use_gpu=use_gpu),
            run_config=RunConfig(callbacks=[comet_callback]),
        )
        result = trainer.fit()
        ```

    """

    def __init__(
        self,
        ray_config: Dict[str, Any],
        tags: Optional[List[str]] = None,
        save_checkpoints: bool = False,
        share_api_key_to_workers: bool = False,
        experiment_name: Optional[str] = None,
        api_key: Optional[str] = None,
        workspace: Optional[str] = None,
        project_name: Optional[str] = None,
        experiment_key: Optional[str] = None,
        mode: Optional[str] = None,
        online: Optional[bool] = None,
        **experiment_kwargs: Any  # fmt: skip
    ) -> None:
        self._save_checkpoints = save_checkpoints
        self._trial: Optional[Trial] = None
        self._experiment: Any = None
        self._experiment_ended: bool = False

        self._setup_shared_comet_experiment(
            api_key=api_key,
            workspace=workspace,
            project_name=project_name,
            experiment_key=experiment_key,
            mode=mode,
            online=online,
            tags=tags,
            experiment_name=experiment_name,
            **experiment_kwargs,
        )
        self._push_info_into_ray_configuration(
            ray_config,
            share_api_key_to_workers,
            offline_directory=experiment_kwargs.get("offline_directory"),
        )

        if save_checkpoints and not self._online:
            LOGGER.warning(
                "CometTrainLoggerCallback(save_checkpoints=True) has no effect for "
                "offline experiments: Comet artifacts require an online experiment, "
                "so checkpoints will not be logged."
            )

        if share_api_key_to_workers:
            LOGGER.warning(
                "Using CometTrainLoggerCallback(share_api_key_to_workers=True) is insecure. "
                "Please refer to https://www.comet.com/docs/v2/guides/tracking-ml-training/distributed-training/ for more secure alternatives."
            )

    @property
    def experiment_key(self) -> str:
        return self._experiment_key

    def _setup_shared_comet_experiment(
        self,
        api_key: Optional[str],
        workspace: Optional[str],
        project_name: Optional[str],
        experiment_key: Optional[str],
        mode: Optional[str],
        online: Optional[bool],
        tags: Optional[List[str]],
        experiment_name: Optional[str],
        **experiment_kwargs: Any
    ) -> None:
        experiment_config_kwargs: Dict[str, Any] = {
            "log_env_gpu": False,
            "log_env_cpu": False,
            "log_env_disk": False,
            "log_env_network": False,
            "log_env_host": True,
            "display_summary_level": 0,
        }
        experiment_config_kwargs.update(experiment_kwargs)

        experiment_config = comet_ml.ExperimentConfig(**experiment_config_kwargs)

        experiment = comet_ml.start(
            api_key=api_key,
            workspace=workspace,
            project=project_name,
            experiment_key=experiment_key,
            mode=mode,
            online=online,
            experiment_config=experiment_config,
        )

        if experiment_name is not None:
            experiment.set_name(experiment_name)
        if tags is not None:
            experiment.add_tags(tags)
        experiment._log_other(OTHER_KEY_CREATED_FROM, "Ray", include_context=False)

        self._experiment_key: str = experiment.id
        # ``api_key`` exists on the online ``Experiment`` but not on the
        # ``CometExperiment`` base; read defensively for offline handles.
        self._api_key: Optional[str] = getattr(experiment, "api_key", None)
        self._online: bool = callback_helpers.is_online_experiment(experiment)

    def _push_info_into_ray_configuration(
        self,
        config: Dict[str, Any],
        share_api_key_to_workers: bool,
        offline_directory: Optional[str] = None,
    ) -> None:
        config["_comet_experiment_key"] = self._experiment_key
        if share_api_key_to_workers:
            config["_comet_api_key"] = hidden_api_key.HiddenApiKey(value=self._api_key)

        config["_comet_online"] = self._online

        # Share the offline directory so worker archives land alongside the
        # driver's instead of scattering into Ray's per-session temp dir.
        # Only relevant offline; workers may still override via their own kwargs.
        if not self._online and offline_directory is not None:
            config["_comet_offline_directory"] = offline_directory

    def _connect_to_shared_experiment(self) -> Any:
        """Re-attach to the shared experiment created in ``__init__``.

        The controller process that fires the Ray callback hooks can be a
        different process than the one that constructed the callback, so the
        experiment handle has to be re-resolved by key.
        """
        experiment_config = comet_ml.ExperimentConfig(
            log_env_gpu=False,
            log_env_cpu=False,
            log_env_details=False,
            log_env_host=False,
            display_summary_level=0,
        )

        return comet_ml.start(
            experiment_key=self._experiment_key,
            api_key=self._api_key,
            experiment_config=experiment_config,
            online=self._online,
            mode="get",
        )

    # ------------------------------------------------------------------
    # Ray Train V1 / Tune-style hooks (inert when USE_USER_CALLBACK).
    # ------------------------------------------------------------------

    def log_trial_start(self, trial: Trial) -> None:
        # Different trial than the one already running — this callback is
        # single-trial only. Raise before any state is touched.
        if self._trial is not None and trial.trial_id != self._trial.trial_id:
            raise Exception(
                "CometTrainLoggerCallback has been already started. Only one start is allowed "
            )

        # Same trial that is already attached — idempotent no-op.
        if self._experiment is not None:
            return

        # First start for this trial, or a retry after a previous attach
        # failure. ``_attach_shared_experiment`` commits ``self._experiment``
        # only after both connect and parameter logging succeed; we mirror
        # that here by committing ``self._trial`` only afterwards, so a
        # failure does not trap a later ``log_trial_start`` call in the
        # ``trial_id`` match branch and leave ``log_trial_result`` building
        # a ``TrialResultLogger`` around a ``None`` experiment.
        self._attach_shared_experiment(trial.config)
        self._trial = trial

    def _attach_shared_experiment(self, config: Dict[str, Any]) -> None:
        """Connect to the shared experiment and log its initial parameters.

        ``self._experiment`` is committed only after BOTH the connect and
        the parameter log succeed. Any failure leaves the lazy-attach guard
        (``self._experiment is None``) intact so callers can retry — and so
        ``train_loop_config`` is never silently dropped because a transient
        ``log_parameters`` error tripped before the retry guard cleared.
        Exceptions from either step propagate to the caller.
        """
        experiment = self._connect_to_shared_experiment()
        self._log_parameters_from_config(experiment, config)
        self._experiment = experiment
        # Note: these parameters are logged once from the controller process and
        # sent lazily, so they would be dropped when Ray hard-kills the
        # controller. They are NOT flushed here — the controller-shutdown drain
        # installed in ``after_report`` (controller_flush_patcher) flushes the
        # experiment once at the end of the run, covering parameters, the final
        # metrics, and async checkpoint uploads in a single drain.

    @staticmethod
    def _log_parameters_from_config(experiment: Any, config: Dict[str, Any]) -> None:
        # Ray Train V1 hands us ``trial.config``, which nests the user's
        # ``train_loop_config`` under a ``"train_loop_config"`` key; the V2
        # ``after_report`` path already passes the inner dict. Unwrap it so the
        # individual hyperparameters (``lr``, ``batch_size``, ...) are logged
        # one-per-parameter and identically on both Ray Train versions —
        # otherwise V1 logs a single opaque ``train_loop_config`` parameter.
        inner_config = config.get("train_loop_config")
        if isinstance(inner_config, dict):
            config = inner_config
        # Drop the connection details the callback injected to reach the workers
        # (not user hyperparameters) and Ray's own ``callbacks`` entry.
        config = strip_injected_keys(config)
        config.pop("callbacks", None)
        if config:
            experiment.log_parameters(config, nested_support=False)

    def log_trial_result(self, iteration: int, trial: Trial, result: Dict) -> None:
        if self._trial is None:
            self.log_trial_start(trial)

        if self._trial is not trial:
            raise Exception("Only one trial is allowed for CometTrainLoggerCallback")

        result_logger = trial_result_logger.TrialResultLogger(self._experiment, result)
        result_logger.process()

    def log_trial_save(self, trial: Trial) -> None:
        if not (self._save_checkpoints and trial.checkpoint is not None):
            return
        # Artifacts are online-only; skip offline (warned once at construction).
        # Wrap so a checkpoint-logging failure never aborts the training run.
        if not self._online:
            return
        try:
            trial_save_logger.go(self._experiment, trial)
        except Exception:
            LOGGER.warning(
                "Failed to log Ray checkpoint to Comet; continuing training",
                exc_info=True,
            )

    def log_trial_end(self, trial: Trial, failed: bool = False) -> None:
        # self._experiment.end()
        pass

    def on_experiment_end(self, trials: List["Trial"], **info: Any) -> None:
        if self._experiment is None:
            return
        # On a worker, end the experiment to avoid losing changes. On the driver
        # (Ray Train V1), flush so lazily-sent parameters and metrics reach the
        # backend before ``fit()`` returns — without an explicit drain they are
        # delivered only at interpreter exit (atexit), which races any
        # post-``fit()`` reads. (V2's equivalent drain is controller_flush_patcher.)
        if worker.global_worker.mode == worker.WORKER_MODE:
            self._experiment.end()
        else:
            self._experiment.flush()

    # ------------------------------------------------------------------
    # Ray Train V2 ``UserCallback`` hooks (inert when not USE_USER_CALLBACK).
    # ------------------------------------------------------------------

    def after_report(
        self,
        run_context: Any,
        metrics: List[Dict[str, Any]],
        checkpoint: Any,
    ) -> None:
        if self._experiment is None:
            self._attach_shared_experiment(self._train_loop_config(run_context))

        # This hook runs in the controller process with the live controller on
        # the call stack. Wrap its shutdown to flush the experiment (and its
        # async checkpoint uploads) before Ray hard-kills the controller.
        # ``ensure_drain`` is idempotent, so it is called on every report rather
        # than only on the attach branch — that way an experiment attached
        # earlier (e.g. by ``after_exception``) still gets the drain installed.
        if self._experiment is not None:
            controller_flush_patcher.ensure_drain(self._experiment)

        if metrics and metrics[0] is not None:
            # Ray Train hands us one metrics dict per worker; rank 0 is the
            # canonical source for the driver-level experiment. Per-worker
            # logging is handled separately via ``comet_worker_logger``.
            result_logger = trial_result_logger.TrialResultLogger(
                self._experiment, metrics[0]
            )
            result_logger.process()

        if self._save_checkpoints and checkpoint is not None:
            self._log_checkpoint_v2(run_context, checkpoint)

    def after_exception(self, run_context: Any, worker_exceptions: Any) -> None:
        # The shared Comet experiment is created on the driver in ``__init__``;
        # without a prior ``after_report`` the controller process has no handle
        # to it yet, so attach lazily before ending so failures are recorded
        # instead of leaving an open experiment behind. We also log the trial
        # parameters in that branch — V1's ``log_trial_start`` runs on the
        # equivalent path, and a setup-time failure should still leave the
        # parameter set visible on the experiment for debugging.
        if self._experiment_ended:
            return

        if self._experiment is None:
            try:
                self._attach_shared_experiment(self._train_loop_config(run_context))
            except Exception:
                LOGGER.warning(
                    "Failed to set up shared Comet experiment from after_exception",
                    exc_info=True,
                )
                # ``_attach_shared_experiment`` commits ``self._experiment``
                # only after both connect and log succeed, so on any failure
                # the handle is still unattached and there is nothing to end.
                # Leave ``_experiment_ended`` False so a later
                # after_exception call can retry the full setup.
                return

        try:
            self._experiment.end()
        except Exception:
            LOGGER.warning(
                "Failed to end Comet experiment from after_exception", exc_info=True
            )
            # End failed — leave _experiment_ended as False so a later
            # after_exception call can retry on the same handle.
            return

        self._experiment_ended = True

    @staticmethod
    def _train_loop_config(run_context: Any) -> Dict[str, Any]:
        return getattr(run_context, "train_loop_config", None) or {}

    def _log_checkpoint_v2(self, run_context: Any, checkpoint: Any) -> None:
        # Artifacts are online-only; skip offline (warned once at construction).
        # Wrap so a checkpoint-logging failure never aborts the training run —
        # on Ray Train V2 an exception here propagates out of after_report and
        # is raised as a ControllerError that kills the whole run.
        if not self._online:
            return
        try:
            name = self._checkpoint_artifact_name(run_context)
            # ``Checkpoint.as_directory`` materialises remote checkpoints locally
            # for the duration of the context manager, mirroring how the legacy
            # path consumed ``trial.checkpoint.dir_or_data``.
            with checkpoint.as_directory() as local_dir:
                trial_save_logger.log_checkpoint(
                    self._experiment, name=name, directory=local_dir
                )
        except Exception:
            LOGGER.warning(
                "Failed to log Ray checkpoint to Comet; continuing training",
                exc_info=True,
            )

    def _checkpoint_artifact_name(self, run_context: Any) -> str:
        try:
            run_config = run_context.get_run_config()
            name = getattr(run_config, "name", None)
        except Exception:
            name = None
        return name or self._experiment_key
