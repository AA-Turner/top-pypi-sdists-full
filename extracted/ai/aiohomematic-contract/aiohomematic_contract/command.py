# SPDX-License-Identifier: MIT
# Copyright (c) 2021-2026
"""
Shared command-priority enum.

``CommandPriority`` orders outgoing device commands in aiohomematic's command
throttle. It lives in the contract package because the model layer references
it without depending on the (client-side) throttle implementation, and any
alternative backend that drives the same model needs the same priority values.
"""

from enum import IntEnum

__all__ = ["CommandPriority"]


class CommandPriority(IntEnum):
    """
    Command priority levels.

    Lower numeric value = higher priority in queue.
    """

    CRITICAL = 0  # Security, access control - bypass throttle
    HIGH = 1  # Interactive user commands - normal throttle
    LOW = 2  # Bulk operations, automations - normal throttle
