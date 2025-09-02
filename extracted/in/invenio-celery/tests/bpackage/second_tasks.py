# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Demo task module with two tasks."""

from celery import shared_task


@shared_task
def second_task_a():
    """Second example task A."""


@shared_task
def second_task_b():
    """Second example task B."""
