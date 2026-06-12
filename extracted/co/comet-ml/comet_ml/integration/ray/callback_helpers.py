# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2024 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************

from typing import Any, Dict

import comet_ml

# Connection details the callback injects into the user's ``ray_config`` so each
# worker can reach the shared experiment. They are not user hyperparameters and
# must be stripped before logging the config as parameters. Matched exactly (not
# by ``_comet_`` prefix) so a user hyperparameter that happens to start with
# ``_comet_`` is preserved.
INJECTED_CONFIG_KEYS = (
    "_comet_experiment_key",
    "_comet_api_key",
    "_comet_online",
    "_comet_offline_directory",
)


def is_online_experiment(experiment: Any) -> bool:
    return isinstance(experiment, comet_ml.Experiment)


def strip_injected_keys(config: Dict[str, Any]) -> Dict[str, Any]:
    """Return a copy of ``config`` without the connection details the callback
    injected into ``ray_config`` to reach the workers."""
    return {
        key: value for key, value in config.items() if key not in INJECTED_CONFIG_KEYS
    }
