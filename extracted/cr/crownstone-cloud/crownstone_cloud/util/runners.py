"""Functions to run async functions from sync context"""
from __future__ import annotations

import asyncio
from collections.abc import Coroutine
from typing import Any


def run_async(coroutine: Coroutine[Any, Any, None]) -> Any:
    """Run an async function from sync context."""
    return asyncio.get_event_loop().run_until_complete(coroutine)
