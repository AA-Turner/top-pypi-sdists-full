"""
AGENTICSTAR Platform SDK - Event Models
イベントデータモデル定義

ストリーミングイベントと順序付きイベントのデータ構造
"""

import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from .types import EventType, SubEventType


def _current_timestamp() -> float:
    """現在のUnix timestampを返す（dataclass default_factory用）"""
    return time.time()


def build_content_data(event: "StreamingEvent", chunk_type: str) -> Dict[str, Any]:
    """chunk_type に応じた content ペイロードを構築する。

    本体 PodWebhookSubscriber と同じ契約:
      - vnc_hitl_event: metadata を素のまま送る（"content" ラップなし）
      - progress_message: {"progress_message": message} の独自形式
      - それ以外: {"content": message} + metadata
    """
    if chunk_type == "vnc_hitl_event":
        return dict(event.metadata or {})
    if chunk_type == "progress_message":
        return {"progress_message": event.message}
    content: Dict[str, Any] = {"content": event.message}
    if event.metadata:
        content.update(event.metadata)
    return content


@dataclass
class StreamingEvent:
    """
    ストリーミングイベントデータ

    リアルタイムストリーミング（SSE等）で使用される基本イベント構造

    Attributes:
        event_type: イベントタイプ（EventType enum）
        execution_id: 実行ID
        message: イベントメッセージ
        timestamp: イベント発生時刻（Unix timestamp、省略時は現在時刻）
        metadata: 追加メタデータ（オプション）
        sub_event_type: サブイベントタイプ（フロント表示用、オプション）
    """

    event_type: EventType
    execution_id: str
    message: str
    timestamp: float = field(default_factory=_current_timestamp)
    metadata: Optional[Dict[str, Any]] = None
    sub_event_type: Optional[SubEventType] = None

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        result = {
            "event_type": self.event_type.value,
            "execution_id": self.execution_id,
            "message": self.message,
            "timestamp": self.timestamp,
        }
        if self.metadata is not None:
            result["metadata"] = self.metadata
        if self.sub_event_type is not None:
            result["sub_event_type"] = self.sub_event_type.value
        return result


@dataclass
class SequencedEvent:
    """
    順序付きイベント

    イベントの順序保証が必要な場合に使用

    Attributes:
        sequence: シーケンス番号（0から開始、負の値は不可）
        event_type: イベントタイプ（EventType enum）
        execution_id: 実行ID
        message: イベントメッセージ
        timestamp: イベント発生時刻（Unix timestamp、省略時は現在時刻）
        metadata: 追加メタデータ（オプション）
        sub_event_type: サブイベントタイプ（フロント表示用、オプション）
    """

    sequence: int
    event_type: EventType
    execution_id: str
    message: str
    timestamp: float = field(default_factory=_current_timestamp)
    metadata: Optional[Dict[str, Any]] = None
    sub_event_type: Optional[SubEventType] = None

    def __post_init__(self):
        """シーケンス番号のバリデーション"""
        if self.sequence < 0:
            raise ValueError(f"sequence must be >= 0, got {self.sequence}")

    def to_streaming_event(self) -> StreamingEvent:
        """StreamingEventに変換"""
        return StreamingEvent(
            event_type=self.event_type,
            execution_id=self.execution_id,
            message=self.message,
            timestamp=self.timestamp,
            metadata=self.metadata,
            sub_event_type=self.sub_event_type,
        )

    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        result = {
            "sequence": self.sequence,
            "event_type": self.event_type.value,
            "execution_id": self.execution_id,
            "message": self.message,
            "timestamp": self.timestamp,
        }
        if self.metadata is not None:
            result["metadata"] = self.metadata
        if self.sub_event_type is not None:
            result["sub_event_type"] = self.sub_event_type.value
        return result


@dataclass
class ExecutionMessage:
    """
    実行メッセージデータ（DB保存用）

    エージェント実行中のイベントをデータベースに保存するための構造体。
    マーケットプレイスUIとの連携に使用。

    Attributes:
        user_id: ユーザーID
        conversation_id: 会話ID
        message_id: メッセージID
        chunk_type: チャンクタイプ（content, reasoning_content, task_created等）
        content_data: コンテンツデータ（JSON）

    Example:
        >>> msg = ExecutionMessage(
        ...     user_id="user-123",
        ...     conversation_id="conv-456",
        ...     message_id="msg-789",
        ...     chunk_type="content",
        ...     content_data={"content": "処理中です..."}
        ... )
        >>> await data_access.insert("execution_messages", msg.to_dict())
    """

    user_id: str
    conversation_id: str
    message_id: str
    chunk_type: str
    content_data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """DB挿入用の辞書形式に変換"""
        return {
            "user_id": self.user_id,
            "conversation_id": self.conversation_id,
            "message_id": self.message_id,
            "chunk_type": self.chunk_type,
            "content_data": self.content_data,
        }

    @classmethod
    def from_streaming_event(
        cls,
        event: "StreamingEvent",
        user_id: str,
        conversation_id: str,
        message_id: str,
        chunk_type: Optional[str] = None,
    ) -> "ExecutionMessage":
        """StreamingEventからExecutionMessageを作成

        Args:
            event: ストリーミングイベント
            user_id: ユーザーID
            conversation_id: 会話ID
            message_id: メッセージID
            chunk_type: チャンクタイプ（省略時はevent_typeから推定）

        Returns:
            ExecutionMessage instance

        Example:
            >>> msg = ExecutionMessage.from_streaming_event(
            ...     event=event,
            ...     user_id="user-123",
            ...     conversation_id="conv-456",
            ...     message_id="msg-789"
            ... )
        """
        # チャンクタイプの推定（省略時）
        if chunk_type is None:
            chunk_type_map = {
                EventType.PHASE_START: "content",
                EventType.PROGRESS_UPDATE: "content",
                EventType.THOUGHT_MESSAGE: "reasoning_content",
                EventType.TOOL_START: "task_created",
                EventType.TOOL_RESULT: "task_created",
                EventType.FILE_CREATED: "task_created",
                EventType.COMPLETION_SUCCESS: "content",
                EventType.COMPLETION_FAILURE: "content",
                EventType.HITL_REQUIRED_BROWSER_VNC: "vnc_hitl_event",
                EventType.HITL_COMPLETED: "vnc_hitl_event",
                EventType.PROGRESS_MESSAGE: "progress_message",
            }
            chunk_type = chunk_type_map.get(event.event_type, "content")

        content_data = build_content_data(event, chunk_type)

        return cls(
            user_id=user_id,
            conversation_id=conversation_id,
            message_id=message_id,
            chunk_type=chunk_type,
            content_data=content_data,
        )
