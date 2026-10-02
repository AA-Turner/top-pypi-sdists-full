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
"""Chat-history layer over the Memory Service persistence ORM.

Public API re-exports for the chat models, DTOs and low-level helpers.  This
package extends :mod:`datarobot.application_utils.persistence`; the
persistence sub-package itself never imports from here (or from ``ag_ui``).
"""

from __future__ import annotations

from datarobot.application_utils.chat_history.ag_ui_storage import AGUIAgent, AGUIStorageAgent, ErrorCodes, StorageState
from datarobot.application_utils.chat_history.constants import (
    LOCATOR_KIND_CHAT,
    LOCATOR_KIND_MESSAGE,
    LOCATOR_KIND_REASONING,
    LOCATOR_KIND_TOOL_CALL,
    MEMORY_CHAT_MESSAGE_EVENT_TYPE,
    PAYLOAD_VERSION,
    app_str,
    chat_deduplication_key,
    emitter_for_role,
    locator_key,
    normalize_participant_id,
    participant_id,
    session_deduplication_key,
    wire_non_empty_str,
)
from datarobot.application_utils.chat_history.models import (
    Chat,
    ChatCreate,
    EntityLocator,
    Message,
    MessageCreate,
    MessagePublic,
    MessageReasoningCreate,
    MessageReasoningUpdate,
    MessageStatus,
    MessageToolCallCreate,
    MessageToolCallUpdate,
    MessageUpdate,
    Reasoning,
    Role,
    ToolCall,
)
from datarobot.application_utils.chat_history.repositories import (
    ChatRepository,
    ChatRepositoryLike,
    ChatSessionRegistry,
    LocatorIndex,
    MessageRepository,
    MessageRepositoryLike,
)
from datarobot.application_utils.chat_history.stream_manager import NoMoreEvents, RunHandle, StreamPersistenceManager
from datarobot.application_utils.chat_history.translate import ExtendedBaseMessage, translate_messages

__all__ = [
    # constants / helpers
    "MEMORY_CHAT_MESSAGE_EVENT_TYPE",
    "PAYLOAD_VERSION",
    "app_str",
    "wire_non_empty_str",
    "session_deduplication_key",
    "chat_deduplication_key",
    "normalize_participant_id",
    "participant_id",
    "emitter_for_role",
    "locator_key",
    "LOCATOR_KIND_CHAT",
    "LOCATOR_KIND_MESSAGE",
    "LOCATOR_KIND_TOOL_CALL",
    "LOCATOR_KIND_REASONING",
    # enums
    "Role",
    "MessageStatus",
    # nested models
    "ToolCall",
    "Reasoning",
    # ORM models
    "Chat",
    "Message",
    "EntityLocator",
    # DTOs
    "ChatCreate",
    "MessageCreate",
    "MessageUpdate",
    "MessageToolCallCreate",
    "MessageToolCallUpdate",
    "MessageReasoningCreate",
    "MessageReasoningUpdate",
    "MessagePublic",
    # repositories
    "ChatRepositoryLike",
    "MessageRepositoryLike",
    "ChatSessionRegistry",
    "LocatorIndex",
    "ChatRepository",
    "MessageRepository",
    # translate
    "translate_messages",
    "ExtendedBaseMessage",
    # AG-UI storage
    "AGUIAgent",
    "AGUIStorageAgent",
    "StorageState",
    "ErrorCodes",
    # stream manager (disconnect survival + cancellation)
    "StreamPersistenceManager",
    "RunHandle",
    "NoMoreEvents",
]
