# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
# Copyright (C) 2025 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test InvenioCelery extension."""

from importlib.metadata import EntryPoint
from unittest.mock import MagicMock, patch

import pytest

from invenio_celery import InvenioCelery


def _mock_entry_points(group=None, name=None):
    """Return EntryPoints from different groups."""
    data = {
        "only_first_tasks": [
            EntryPoint(
                name="bpackage", value="bpackage.first_tasks", group="only_first_tasks"
            )
        ],
        "only_second_tasks": [
            EntryPoint(
                name="bpackage",
                value="bpackage.second_tasks",
                group="only_second_tasks",
            )
        ],
        "bare_module_tasks": [
            EntryPoint(
                name="second_tasks", value="second_tasks", group="bare_module_tasks"
            )
        ],
        "invenio_celery.tasks": [
            EntryPoint(
                name="bpackage_1",
                value="bpackage.first_tasks",
                group="invenio_celery.tasks",
            ),
            EntryPoint(
                name="bpackage_2",
                value="bpackage.second_tasks",
                group="invenio_celery.tasks",
            ),
            EntryPoint(
                name="apackage",
                value="apackage.third_tasks",
                group="invenio_celery.tasks",
            ),
        ],
        "invenio_celery.signals": [],
    }
    assert name is None
    return data[group] if group else data


def test_version():
    """Test version import."""
    from invenio_celery import __version__

    assert __version__


def test_init(app):
    """Test Celery initialization."""
    celery = InvenioCelery(app)
    assert app.extensions["invenio-celery"] == celery

    called = {}

    @celery.celery.task
    def test1():
        called["test1"] = True

    test1.delay()
    assert called["test1"]


@patch("importlib.metadata.entry_points", _mock_entry_points)
def test_enabled_autodiscovery(app):
    """Test shared task detection."""
    ext = InvenioCelery(app)
    ext.load_entry_points()
    assert "conftest.shared_compute" in ext.celery.tasks.keys()
    assert "bpackage.first_tasks.first_task" in ext.celery.tasks.keys()
    assert "bpackage.second_tasks.second_task_a" in ext.celery.tasks.keys()
    assert "bpackage.second_tasks.second_task_b" in ext.celery.tasks.keys()
    assert "apackage.third_tasks.third_task" in ext.celery.tasks.keys()


@patch("importlib.metadata.entry_points", _mock_entry_points)
def test_only_first_tasks(app):
    """Test loading different entrypoint group."""
    ext = InvenioCelery(app, entry_point_group="only_first_tasks")
    ext.load_entry_points()
    assert "conftest.shared_compute" in ext.celery.tasks.keys()
    assert "bpackage.first_tasks.first_task" in ext.celery.tasks.keys()
    assert "bpackage.second_tasks.second_task_a" not in ext.celery.tasks.keys()
    assert "bpackage.second_tasks.second_task_b" not in ext.celery.tasks.keys()
    assert "apackage.third_tasks.third_task" not in ext.celery.tasks.keys()


@patch("importlib.metadata.entry_points", _mock_entry_points)
def test_bare_module_warning(app):
    """Test loading different entrypoint group."""
    ext = InvenioCelery(app, entry_point_group="bare_module_tasks")
    with pytest.warns(RuntimeWarning):
        ext.load_entry_points()


def test_disabled_autodiscovery(app):
    """Test disabled discovery."""
    ext = InvenioCelery(app, entry_point_group=None)
    ext.load_entry_points()
    assert "conftest.shared_compute" in ext.celery.tasks.keys()
    assert "bpackage.first_tasks.first_task" not in ext.celery.tasks.keys()
    assert "bpackage.second_tasks.second_task_a" not in ext.celery.tasks.keys()
    assert "bpackage.second_tasks.second_task_b" not in ext.celery.tasks.keys()
    assert "apackage.third_tasks.third_task" not in ext.celery.tasks.keys()


@patch("importlib.metadata.entry_points", _mock_entry_points)
def test_worker_loading(app):
    """Test that tasks are only loaded on the worker."""
    ext = InvenioCelery(app)
    assert "bpackage.first_tasks.first_task" not in ext.celery.tasks.keys()
    ext.celery.loader.import_default_modules()
    assert "bpackage.first_tasks.first_task" in ext.celery.tasks.keys()


def test_get_queues(app):
    """Test get queues."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    assert ext.get_queues() == []


def test_enable_queue(app):
    """Test enable queues."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    ext.enable_queue("feed")


def test_disable_queue(app):
    """Test enable queues."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    ext.disable_queue("feed")


def test_get_active_tasks(app):
    """Test get active tasks."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    assert ext.get_active_tasks() == []


def test_suspend_queues(app):
    """Test suspend queues."""
    ext = InvenioCelery(app)
    ext.celery.control = MagicMock()
    c = {"i": 0}

    def _mock():
        c["i"] += 1
        return [] if c["i"] > 1 else ["test"]

    ext.get_active_tasks = _mock
    ext.suspend_queues(["feed"], sleep_time=0.1)
