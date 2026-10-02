"""
AGENTICSTAR Platform SDK - Events Module
イベントシステムの型定義とモデルを提供

Example:
    >>> from agenticstar_platform.events import (
    ...     EventType,
    ...     StreamingEvent,
    ...     EventEmitter,
    ... )
    >>>
    >>> # イベントエミッター作成
    >>> emitter = EventEmitter(execution_id="exec-123")
    >>>
    >>> # イベント発行
    >>> await emitter.emit_event(EventType.PHASE_START, "処理開始")
"""

from .types import EventType, SubEventType
from .models import StreamingEvent, SequencedEvent, ExecutionMessage, build_content_data
from .emitter import (
    EventEmitter,
    EventHandler,
    create_sse_handler,
    create_json_handler,
)
from .handlers import (
    DatabaseEventHandler,
    WebhookEventHandler,
    CompositeEventHandler,
    create_marketplace_handler,
)

__all__ = [
    # Event Types
    "EventType",
    "SubEventType",
    # Event Models
    "StreamingEvent",
    "SequencedEvent",
    "ExecutionMessage",
    "build_content_data",
    # Event Emitter
    "EventEmitter",
    "EventHandler",
    "create_sse_handler",
    "create_json_handler",
    # Event Handlers (DB/Webhook/Composite)
    "DatabaseEventHandler",
    "WebhookEventHandler",
    "CompositeEventHandler",
    "create_marketplace_handler",
]
