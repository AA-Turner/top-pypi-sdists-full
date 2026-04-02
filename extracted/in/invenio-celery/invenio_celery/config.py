# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Default configuration values for Celery integration.

For further Celery configuration variables see
`Celery <http://docs.celeryproject.org/en/3.1/configuration.html>`_
documentation.
"""

BROKER_URL = "redis://localhost:6379/0"
CELERY_BROKER_URL = BROKER_URL  # For Celery 4
"""Broker settings."""

CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
"""The backend used to store task results."""

CELERY_ACCEPT_CONTENT = ["json", "msgpack", "yaml"]
"""A whitelist of content-types/serializers."""

CELERY_RESULT_SERIALIZER = "msgpack"
"""Result serialization format. Default is ``msgpack``."""

CELERY_TASK_SERIALIZER = "msgpack"
"""The default serialization method to use. Default is ``msgpack``."""
