# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request Files Resource module."""

from .config import RequestFilesResourceConfig
from .resource import RequestFilesResource

__all__ = (
    "RequestFilesResource",
    "RequestFilesResourceConfig",
)
