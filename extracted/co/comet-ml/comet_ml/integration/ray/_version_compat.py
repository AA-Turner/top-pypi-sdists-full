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
"""Selects the right Ray callback base class for the installed Ray version.

Ray Train V2 (Ray >= 2.43 with RAY_TRAIN_V2_ENABLED=1; default since 2.51)
exposes ``ray.train.UserCallback`` and rejects ``ray.tune.Callback`` subclasses
at ``RunConfig`` construction time. Ray Train V1 keeps the old
``ray.tune.logger.LoggerCallback`` path. Ray's own ``ray.train.__init__``
gates the ``UserCallback`` export on ``is_v2_enabled()``, so a successful
import is a sufficient signal that the new API is the one to use.
"""

try:
    from ray.train import UserCallback  # noqa: F401

    USE_USER_CALLBACK = True
except ImportError:
    USE_USER_CALLBACK = False
