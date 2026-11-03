#
# Copyright 2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
"""URL path helpers for the pipelines client."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote


def escape_id(value: Any) -> str:
    """Percent-encode a caller-supplied id for use as a single URL path segment.

    Every pipelines route interpolates ids into a relative path which
    ``RESTClientObject._join_endpoint`` then hands to :func:`urllib.parse.urljoin`.
    urljoin resolves ``..`` and treats ``/`` as a separator, so an unescaped id
    does not merely produce a 404 -- it silently retargets the request, with the
    caller's token attached::

        id = "../../credentials"
        "pipelines/{id}/inputs/"  ->  https://host/api/credentials/inputs/

    ``safe=""`` is the load-bearing part. :func:`quote` defaults to
    ``safe="/"``, which leaves the separator intact and so does not prevent the
    attack -- note ``datarobot/models/feature.py`` uses the default, which is
    fine for the spaces and unicode it was added for but would not help here.

    Non-string ids (version numbers, task ids) are stringified first, so this is
    safe to apply uniformly and stays correct if one of them ever becomes a
    string.
    """
    return quote(str(value), safe="")
