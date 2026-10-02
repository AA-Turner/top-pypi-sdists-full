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
"""Memory Service light ORM — public surface.

Install with ``pip install datarobot[application-utils]``; requires Python 3.11+
(enforced in :mod:`datarobot.application_utils`).

Quick start
-----------
.. code-block:: python

    import asyncio
    from typing import Annotated
    from datarobot.application_utils.persistence import (
        DRMemorySpace,
        DRSession,
        DREvent,
        DRDeduplicationKey,
        DRRangeKey,
        DRConcurrencyField,
        DRMemoryServiceClient,
        SYSTEM_PARTICIPANT,
    )

    class ChatSession(DRSession):
        __description_prefix__ = "chat"
        tenant: Annotated[str, DRRangeKey]
        chat_id: Annotated[str, DRDeduplicationKey]
        rev: Annotated[int, DRConcurrencyField]
        title: str  # -> metadata

    class ChatMessage(DREvent, session=ChatSession):
        __event_type__ = "message"
        score: float

    async def main() -> None:
        async with DRMemoryServiceClient() as client:
            space = await DRMemorySpace.post(client, description="my-space")
            session = await ChatSession.post(space, tenant="acme", chat_id="c1", title="Hello")
            msg = await ChatMessage.post(
                session=session, content="Hi", emitter_type="agent", score=0.9
            )
            print(msg.sequence_id)

    asyncio.run(main())
"""

from __future__ import annotations

from datarobot.application_utils.persistence._client import DRMemoryServiceClient
from datarobot.application_utils.persistence.event import DREvent
from datarobot.application_utils.persistence.exceptions import (
    DRMemoryBadRequestError,
    DRMemoryConflictError,
    DRMemoryNotFoundError,
    DRMemoryRateLimitError,
    DRMemoryServiceError,
    DRMemoryUnavailableError,
    DRMemoryValidationError,
    DRMemoryVersionConflictError,
)
from datarobot.application_utils.persistence.markers import (
    DEFAULT_SESSION_TTL_SECONDS,
    SYSTEM_PARTICIPANT,
    DRConcurrencyField,
    DRDeduplicationKey,
    DRRangeKey,
)
from datarobot.application_utils.persistence.session import DRSession
from datarobot.application_utils.persistence.space import DRMemorySpace

__all__ = [
    "DRMemorySpace",
    "DRSession",
    "DREvent",
    "DRDeduplicationKey",
    "DRRangeKey",
    "DRConcurrencyField",
    "DRMemoryServiceClient",
    "SYSTEM_PARTICIPANT",
    "DEFAULT_SESSION_TTL_SECONDS",
    "DRMemoryServiceError",
    "DRMemoryNotFoundError",
    "DRMemoryBadRequestError",
    "DRMemoryValidationError",
    "DRMemoryConflictError",
    "DRMemoryVersionConflictError",
    "DRMemoryRateLimitError",
    "DRMemoryUnavailableError",
]
