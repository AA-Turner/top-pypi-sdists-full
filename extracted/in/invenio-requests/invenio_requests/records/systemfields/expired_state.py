# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2022 TU Wien.
# Copyright (C) 2025-2026 Graz University of Technology.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Systemfield for calculating the ``is_expired`` property of a request."""

from datetime import datetime, timezone

import arrow
from invenio_records_resources.records.systemfields.calculated import CalculatedField


class ExpiredStateCalculatedField(CalculatedField):
    """Systemfield for calculating whether or not the request is expired."""

    def __init__(self, key=None):
        """Constructor."""
        super().__init__(key=key, use_cache=False)

    def calculate(self, record):
        """Calculate the ``is_expired`` property of the request."""
        expires_at = getattr(record, self.key)

        # if 'expires_at' is not set, that means it doesn't expire
        if expires_at is None:
            return False

        expires_at = arrow.get(expires_at, tzinfo=timezone.utc).datetime
        now = datetime.now(timezone.utc)

        return expires_at < now
