# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2024 CERN.
# Copyright (C) 2024-2025 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery distributed task queue module for Invenio.

Invenio-Celery is a small discovery layer that takes care of discovering and
loading tasks from other Invenio modules, as well as providing configuration
defaults for Celery usage in Invenio. Invenio-Celery relies on Flask-CeleryExt
for integrating Flask and Celery with application factories.

Defining tasks
--------------
Invenio modules that wish to define Celery tasks should use the
``@shared_task`` decorator (usually in ``tasks.py``):

.. code-block:: python

    # mymodule/tasks.py
    from celery import shared_task

    @shared_task
    def sum(x, y):
         return x + y

Additionally the Invenio module should add the task module into the
``invenio_celery.tasks`` entry point:

.. code-block:: python

    # setup.py
    setup(
        # ...
        entry_points=[
            'invenio_celery.tasks' : [
                'mymodule = mymodule.tasks'
            ]
        ]
    )

Using tasks
-----------
Invenio modules that need to call tasks do not need to do anything special as
long as the Invenio-Celery extension has been initialized. Hence calling tasks
is as simple as:

.. code-block:: python

    from mymodule.tasks import sum
    result = sum.delay(2, 2)

Periodic tasks
--------------
Periodic tasks can be configured via ``CELERYBEAT_SCHEDULE`` configuration
variable:

.. code-block:: python

    # config.py
    CELERYBEAT_SCHEDULE = {
        'indexer': {
            'task': 'invenio_indexer.tasks.process_bulk_queue',
            'schedule': timedelta(minutes=5),
        },
    }

For further information about see `Periodic Tasks
<http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html>`_
chapter of the `Celery documentation
<http://docs.celeryproject.org/en/latest/index.html>`_.


Celery workers
--------------
Invenio-Celery hooks into the Celery application loading process so that when
a worker starts, all the tasks modules defined in ``invenio_celery.tasks`` will
be imported and cause the tasks to be registered in the worker. Note that this
only happens on the Celery worker side which needs to know upfront all the
possible tasks.

For further details on how to setup Celery and define an Celery application
factory please see `Flask-CeleryExt <https://flask-celeryext.readthedocs.io/>`_
"""

from __future__ import absolute_import, print_function

from .ext import InvenioCelery

__version__ = "2.2.0"

__all__ = ("__version__", "InvenioCelery")
