# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2024 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


"""Pytest configuration."""

from __future__ import absolute_import, print_function

import sys

import celery._state
import pytest
from celery import Celery, shared_task
from flask import Flask


@pytest.fixture()
def app(request):
    """Flask app fixture."""
    app = Flask("testapp")
    app.config.update(
        dict(
            CELERY_ALWAYS_EAGER=True,  # v3
            CELERY_CACHE_BACKEND="memory",
            CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,  # v3
            CELERY_RESULT_BACKEND="cache",
            CELERY_TASK_ALWAYS_EAGER=True,  # v4
            CELERY_TASK_EAGER_PROPAGATES=True,  # v4
        )
    )

    @shared_task
    def shared_compute():
        """Dummy function."""
        pass

    def set_celery_state():
        celery._state._apps.discard(
            app.extensions["invenio-celery"].celery._get_current_object()
        )
        celery._state._on_app_finalizers = set()
        celery._state.set_default_app(Celery())

        # Clear our modules to get them re-imported by Celery.
        pkgs = [
            "bpackage.first_tasks",
            "bpackage.second_tasks",
            "apackage.third_tasks",
        ]
        for pkg in pkgs:
            if pkg in sys.modules:
                del sys.modules[pkg]

    request.addfinalizer(set_celery_state)
    return app
