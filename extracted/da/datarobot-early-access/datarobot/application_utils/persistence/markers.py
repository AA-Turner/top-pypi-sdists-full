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
"""ORM marker types for the Memory Service light ORM.

These sentinel classes are used as ``Annotated`` metadata to declare how
``DRSession`` and ``DREvent`` subclass fields map to the Memory Service wire
format.

Examples
--------
.. code-block:: python

    from typing import Annotated
    from datarobot.application_utils.persistence import (
        DRSession,
        DRDeduplicationKey,
        DRRangeKey,
        DRConcurrencyField,
        SYSTEM_PARTICIPANT,
    )

    class ChatSession(DRSession):
        __description_prefix__ = "chat"
        tenant: Annotated[str, DRRangeKey]            # description segment 1
        topic: Annotated[str, DRRangeKey]             # description segment 2
        chat_id: Annotated[str, DRDeduplicationKey]   # point-lookup key
        rev: Annotated[int, DRConcurrencyField]       # mirrors server version
        title: str                                    # -> metadata.title
"""

from __future__ import annotations


class DRDeduplicationKey:
    """Marker: field maps to the session ``deduplicationKey`` (point-lookup primary key).

    At most one field per ``DRSession`` subclass may carry this marker.
    Enables ``MySession.get(space, my_key="value")`` exact-match point lookups
    and idempotent session creation (409 → adopt the existing session).
    """


class DRRangeKey:
    """Marker: field maps to a segment of the session ``description`` (range/prefix queries).

    Segments are appended to ``description`` in declaration order, encoded
    with the ``//prefix/seg1/seg2/`` scheme. Values must be non-empty strings.

    Known limitation
    ----------------
    The Memory Service ``description`` filter is **case-insensitive**, so values
    differing only in case (e.g. ``Foo`` vs ``foo``) will collide when querying.
    """


class DRConcurrencyField:
    """Marker: field is kept in sync with the server ``version`` integer.

    Enables user code to inspect the current optimistic-concurrency version
    without calling ``.version`` directly.  At most one field per ``DRSession``
    subclass may carry this marker.

    Whether or not this marker is present, the ORM always tracks the server
    version internally for ``If-Match`` concurrency control on ``patch()``.
    """


#: Sentinel ObjectId for sessions that belong to no specific user.
#: This is a client-side convention; the Memory Service treats it as any
#: other valid 24-hex ObjectId.
SYSTEM_PARTICIPANT: str = "000000000000000000000000"

#: Default session TTL in seconds (2 years). Also the Memory Service maximum for a
#: TTL trigger; used to build the default ``soft_delete`` lifecycle strategy.
DEFAULT_SESSION_TTL_SECONDS: int = 2 * 365 * 24 * 60 * 60  # 2 years
