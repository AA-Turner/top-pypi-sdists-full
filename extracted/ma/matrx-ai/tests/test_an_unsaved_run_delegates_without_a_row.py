"""An ephemeral run (store=false) has no chat.tool_call row; delegating a client tool must not read ``id = ''``."""

from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest

from matrx_ai.tools.logger import ToolExecutionLogger

pytestmark = pytest.mark.asyncio


async def test_no_row_id_means_nothing_to_park_or_prove():
    logger = ToolExecutionLogger()
    with patch.object(ToolExecutionLogger, "assert_delegated_on_disk", new=AsyncMock()) as proof, \
         patch.object(ToolExecutionLogger, "log_delegated", new=AsyncMock()) as park:
        await logger.delegate_durably("", expires_at=datetime(2030, 1, 1, tzinfo=UTC), reason="t")
    proof.assert_not_called()
    park.assert_not_called()
