# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2024-2025 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery application for Invenio."""

from __future__ import absolute_import, print_function

import time
import warnings

from celery.signals import import_modules
from flask_celeryext import FlaskCeleryExt
from invenio_base.utils import entry_points

from . import config


class InvenioCelery(object):
    """Invenio celery extension."""

    def __init__(self, app=None, **kwargs):
        """Extension initialization."""
        self.celery = None

        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, entry_point_group="invenio_celery.tasks", **kwargs):
        """Initialize application object."""
        self.init_config(app)
        self.celery = FlaskCeleryExt(app).celery
        self.entry_point_group = entry_point_group
        self.load_celery_signals()
        app.extensions["invenio-celery"] = self

    def load_celery_signals(self):
        """Load Celery signals."""
        # Import Celery signals via entry points
        for ep in entry_points(group="invenio_celery.signals"):
            __import__(ep.module)  # Just import the module to trigger registration

    def load_entry_points(self):
        """Load tasks from entry points."""
        if self.entry_point_group:
            task_packages = {}

            for ep in entry_points(group=self.entry_point_group):
                # Celery 4.2 requires autodiscover to be called with
                # related_name for Python 2.7.
                try:
                    pkg, related_name = ep.module.rsplit(".", 1)
                except ValueError:
                    warnings.warn(
                        'The celery task module "{}" was not loaded. '
                        "Defining modules in bare Python modules is no longer "
                        "supported due to Celery v4.2 constraints. Please "
                        "move the module into a Python package.".format(ep.module),
                        RuntimeWarning,
                    )
                    continue
                if related_name not in task_packages:
                    task_packages[related_name] = []
                task_packages[related_name].append(pkg)

            if task_packages:
                for related_name, packages in task_packages.items():
                    self.celery.autodiscover_tasks(
                        packages, related_name=related_name, force=True
                    )

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("CELERY_") or k.startswith("BROKER_"):
                app.config.setdefault(k, getattr(config, k))

        app.config.setdefault("broker_connection_retry_on_startup", True)

    def get_queues(self):
        """Return a list of current active Celery queues."""
        res = self.celery.control.inspect().active_queues() or dict()
        return [result.get("name") for host in res.values() for result in host]

    def disable_queue(self, name):
        """Disable given Celery queue."""
        self.celery.control.cancel_consumer(name)

    def enable_queue(self, name):
        """Enable given Celery queue."""
        self.celery.control.add_consumer(name)

    def get_active_tasks(self):
        """Return a list of UUIDs of active tasks."""
        current_tasks = self.celery.control.inspect().active() or dict()
        return [task.get("id") for host in current_tasks.values() for task in host]

    def suspend_queues(self, active_queues, sleep_time=10.0):
        """Suspend Celery queues and wait for running tasks to complete."""
        for queue in active_queues:
            self.disable_queue(queue)
        while self.get_active_tasks():
            time.sleep(sleep_time)


@import_modules.connect()
def celery_module_imports(sender, signal=None, **kwargs):
    """Load shared celery tasks."""
    app = getattr(sender, "flask_app", None)
    if app:
        app.extensions["invenio-celery"].load_entry_points()
