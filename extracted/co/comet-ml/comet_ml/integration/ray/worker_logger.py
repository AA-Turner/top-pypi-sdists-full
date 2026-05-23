# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.com
#  Copyright (C) 2015-2021 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

import contextlib
import logging
import os
from typing import Any, Dict, Optional

import comet_ml
import comet_ml.api
import comet_ml.system.gpu.gpu_logging

import ray
import ray.train

from ...constants import OTHER_KEY_CREATED_FROM

LOGGER = logging.getLogger(__file__)


@contextlib.contextmanager
def comet_worker_logger(
    ray_config: Dict[str, Any], api_key: Optional[str] = None, **experiment_kwargs
):
    """
    This context manager allows you to track resource usage from each distributed worker when
    running a distributed training job. It must be used in conjunction with
    [comet_ml.integration.ray.CometTrainLoggerCallback][] callback.

    Args:
        ray_config (dict): Ray configuration dictionary from ray driver node.
        api_key (str, optional): Comet API key. If not None it will be passed to ExistingExperiment.
            This argument has priority over api_key in ray_config dict and api key in environment.
        **experiment_kwargs: Other keyword arguments will be passed to the
            constructor for comet_ml.ExistingExperiment.

    Returns: An Experiment object.

    Example:
        ```python linenums="1"
        def train_func(ray_config: Dict):
            with comet_worker_logger(ray_config) as experiment:
                # ray worker training code
        ```

    Notes:
    If some required information is missing (like the API Key) or something wrong happens, this will
    return a disabled Experiment, all methods calls will succeed but no data is gonna be logged.

    """
    experiment = None
    try:
        api_key = _get_api_key(api_key, ray_config)
        experiment_key = _get_experiment_key(ray_config)
        online = ray_config.get("_comet_online", None)
        mode = "get" if online else "get_or_create"

        if experiment_key is None:
            experiment = comet_ml.OfflineExperiment(disabled=True)
            yield experiment
            return

        try:
            _setup_environment()
            experiment_config_kwargs = {
                "log_env_gpu": True,
                "log_env_cpu": True,
                "log_env_network": True,
                "log_env_disk": True,
                "log_env_host": False,
                "log_env_details": True,
                "display_summary_level": 0,
            }
            _prepare_experiment_kwargs_for_passing_to_experiment_config(
                experiment_kwargs
            )
            experiment_config_kwargs.update(experiment_kwargs)
            experiment_config = comet_ml.ExperimentConfig(**experiment_config_kwargs)

            experiment = comet_ml.start(
                api_key=api_key,
                experiment_key=experiment_key,
                experiment_config=experiment_config,
                online=online,
                mode=mode,
            )
            _preserve_driver_created_from_stamp(experiment)
        except Exception:
            LOGGER.warning(
                "Internal error occurred when creating experiment object."
                "\nReturning disabled experiment. Nothing will be logged.",
                exc_info=True,
            )
            experiment = comet_ml.OfflineExperiment(disabled=True)
        yield experiment

    finally:
        if experiment is not None:
            experiment.end()


def _get_api_key(api_key: Optional[str], ray_config: Dict[str, Any]) -> Optional[str]:
    if api_key is not None:
        return api_key

    if "_comet_api_key" in ray_config:
        hidden_api_key = ray_config["_comet_api_key"]
        return hidden_api_key.value

    return None


def _get_experiment_key(ray_config: Dict[str, Any]) -> Optional[str]:
    if "_comet_experiment_key" in ray_config:
        return ray_config["_comet_experiment_key"]

    LOGGER.warning(
        "Experiment key wasn't found in RAY config. "
        "Make sure you are using CometTrainLoggerCallback."
        "\nReturning disabled experiment. Nothing will be logged."
    )

    return None


def _prepare_experiment_kwargs_for_passing_to_experiment_config(
    experiment_kwargs: Dict[str, Any]
) -> None:
    # workspace and project_name are not relevant because comet_ml.start will get an id
    # of already existing experiment. However, someone could pass these values and we don't want
    # the script to fail
    experiment_kwargs.pop("workspace", None)
    experiment_kwargs.pop("project_name", None)


def _setup_environment() -> None:
    os.environ["COMET_DISTRIBUTED_NODE_IDENTIFIER"] = str(_get_world_rank())
    comet_ml.system.gpu.gpu_logging.set_devices_to_report(ray.get_gpu_ids())


def _preserve_driver_created_from_stamp(experiment: Any) -> None:
    # ``CometTrainLoggerCallback.__init__`` stamps ``Created from = Ray`` on
    # the shared experiment from the driver process. The worker reconnects
    # to that experiment here, and during training the auto-loggers of
    # frameworks like PyTorch register themselves in ``experiment._frameworks``
    # via ``_track_framework_usage``. On ``experiment.end()`` (fired from
    # this context manager's ``finally``), ``CometExperiment._clean_experiment``
    # iterates that set and re-stamps ``Created from = <framework>`` for each
    # one — the last write wins on the backend, so the driver's ``Ray`` stamp
    # gets clobbered by whatever framework name sorts last (``pytorch`` under
    # this distributed-training setup). The iteration emits each re-stamp via
    # ``_log_other(..., framework="comet", ...)``, which short-circuits when
    # ``"comet:<key>"`` is in ``autolog_others_ignore``. Marking the
    # ``Created from`` other as ignored for the ``comet`` pseudo-framework
    # makes that loop a no-op on the worker's connection, preserving the
    # driver's ``Ray`` stamp.
    try:
        experiment.autolog_others_ignore.add("comet:%s" % OTHER_KEY_CREATED_FROM)
    except AttributeError:
        # Disabled experiments and other non-standard handles may not expose
        # the ignore set. The override only matters when the framework loop
        # would actually fire, so swallowing this is safe.
        LOGGER.debug(
            "Could not register %r in autolog_others_ignore on worker experiment",
            OTHER_KEY_CREATED_FROM,
            exc_info=True,
        )


def _get_world_rank() -> int:
    # ``ray.train.get_context()`` works on both Ray Train V1 and V2; the
    # legacy ``ray.air.session.get_world_rank()`` raises under V2 because the
    # Tune session is no longer initialised. We deliberately let the exception
    # propagate when there is no Train context — ``comet_worker_logger`` wraps
    # this call in the same try/except that protects ``comet_ml.start()`` and
    # yields a disabled experiment on failure. Defaulting to 0 here would
    # collide every non-Train worker's per-rank GPU and system-metric stream
    # onto a single identifier, which defeats the purpose of stamping the
    # rank in the first place.
    return ray.train.get_context().get_world_rank()
