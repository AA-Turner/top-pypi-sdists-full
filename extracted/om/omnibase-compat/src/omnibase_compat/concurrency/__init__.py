# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""omnibase_compat.concurrency — sync/async bridging primitives.

Exports helpers that downstream repos (omnibase_core, omnibase_infra) can
import in place of ad-hoc copies of the sync-from-async pattern. The first
entry is ``run_coro_sync``; see OMN-9237.
"""

from omnibase_compat.concurrency.util_run_coro_sync import run_coro_sync

__all__: list[str] = [
    "run_coro_sync",
]
