"""
AGENTICSTAR Platform SDK - Event Emitter
イベント発行機能を提供

汎用イベント発行クライアント（ユースケース非依存）

Note:
    このモジュールは汎用的なイベント発行機能のみを提供します。
    シングルトンパターンや特定のSubscriber管理は含まれません。
    それらはユーザーのアプリケーション層で実装してください。
"""

import asyncio
import logging
import time
from typing import Any, AsyncGenerator, Callable, Dict, Optional, Protocol

from .types import EventType, SubEventType
from .models import StreamingEvent, SequencedEvent

logger = logging.getLogger(__name__)


class EventHandler(Protocol):
    """イベントハンドラープロトコル

    イベント受信時のコールバック関数の型定義

    Example:
        >>> async def my_handler(event: StreamingEvent) -> Optional[str]:
        ...     print(f"Received: {event.message}")
        ...     return f"data: {event.to_dict()}"
    """

    async def __call__(self, event: StreamingEvent) -> Optional[str]:
        """イベントを処理してストリーミングチャンクを返す"""
        ...


class EventEmitter:
    """
    イベント発行クライアント

    非同期イベントキューを使用してイベントを発行・消費します。
    シーケンス番号による順序保証を提供します。

    Features:
        - 非同期イベント発行（emit_event）
        - シーケンス番号による順序保証
        - 非同期イベント消費（consume_events）
        - カスタムイベントハンドラー対応

    Example:
        >>> # 基本的な使い方
        >>> emitter = EventEmitter(execution_id="exec-123")
        >>>
        >>> # イベント発行
        >>> await emitter.emit_event(
        ...     EventType.PHASE_START,
        ...     "処理を開始します"
        ... )
        >>>
        >>> # イベント消費
        >>> async for chunk in emitter.consume_events():
        ...     print(chunk)
        >>>
        >>> # 完了通知
        >>> await emitter.emit_event(
        ...     EventType.COMPLETION_SUCCESS,
        ...     "処理が完了しました"
        ... )

    Note:
        - emit_eventとconsume_eventsは非同期で実行してください
        - 完了イベント（COMPLETION_SUCCESS/COMPLETION_FAILURE）発行後、
          consume_eventsは自動的に終了します
    """

    def __init__(
        self,
        execution_id: str,
        handler: Optional[EventHandler] = None,
    ):
        """
        EventEmitterを初期化

        Args:
            execution_id: 実行ID（イベントの識別に使用）
            handler: イベントハンドラー（オプション）
                     指定しない場合、デフォルトのJSON変換が使用されます

        Example:
            >>> emitter = EventEmitter(execution_id="exec-123")

            >>> # カスタムハンドラー付き
            >>> async def custom_handler(event: StreamingEvent) -> Optional[str]:
            ...     return f"data: {event.to_dict()}\\n\\n"
            >>> emitter = EventEmitter(execution_id="exec-123", handler=custom_handler)
        """
        self.execution_id = execution_id
        self._handler = handler
        self._event_queue: asyncio.Queue[SequencedEvent] = asyncio.Queue()
        self._sequence_number = 0
        self._is_completed = False
        self._completion_event = asyncio.Event()

        logger.debug(f"[{execution_id}] EventEmitter initialized")

    @property
    def is_completed(self) -> bool:
        """完了状態を取得"""
        return self._is_completed

    @property
    def sequence_number(self) -> int:
        """現在のシーケンス番号を取得"""
        return self._sequence_number

    async def emit_event(
        self,
        event_type: EventType,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
        sub_event_type: Optional[SubEventType] = None,
    ) -> None:
        """
        イベントを発行

        Args:
            event_type: イベントタイプ
            message: イベントメッセージ
            metadata: 追加メタデータ（オプション）
            sub_event_type: サブイベントタイプ（オプション）

        Example:
            >>> await emitter.emit_event(
            ...     EventType.THOUGHT_MESSAGE,
            ...     "処理中です...",
            ...     metadata={"progress": 50}
            ... )

        Note:
            完了イベント発行後にイベントを発行しようとすると、
            警告ログが出力され、イベントは無視されます。
        """
        if self._is_completed:
            logger.warning(
                f"[{self.execution_id}] Event emission after completion: {event_type}"
            )
            return

        sequenced_event = SequencedEvent(
            sequence=self._sequence_number,
            event_type=event_type,
            execution_id=self.execution_id,
            message=message,
            timestamp=time.time(),
            metadata=metadata,
            sub_event_type=sub_event_type,
        )
        self._sequence_number += 1

        try:
            await self._event_queue.put(sequenced_event)
            logger.info(
                f"[{self.execution_id}] Event queued: {event_type.value} "
                f"(seq={sequenced_event.sequence})"
            )
        except Exception as e:
            logger.error(
                f"[{self.execution_id}] Failed to queue event {event_type}: {e}"
            )
            raise

    async def emit(
        self,
        event_type: EventType,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
        sub_event_type: Optional[SubEventType] = None,
    ) -> None:
        """emit_eventのエイリアス（短縮形）"""
        await self.emit_event(event_type, message, metadata, sub_event_type)

    async def consume_events(
        self,
        timeout: float = 0.1,
    ) -> AsyncGenerator[str, None]:
        """
        イベントを順序通りに消費してストリーミングチャンクを生成

        Args:
            timeout: イベント待機タイムアウト（秒）

        Yields:
            str: ストリーミングチャンク（ハンドラーの戻り値）

        Example:
            >>> async for chunk in emitter.consume_events():
            ...     await response.write(chunk)

        Note:
            完了イベント（COMPLETION_SUCCESS/COMPLETION_FAILURE）を受信し、
            キューが空になった時点で自動的に終了します。
        """
        logger.info(f"[{self.execution_id}] Starting event consumption")

        while True:
            try:
                event = await asyncio.wait_for(
                    self._event_queue.get(),
                    timeout=timeout,
                )

                logger.debug(
                    f"[{self.execution_id}] Processing event: {event.event_type.value} "
                    f"(seq={event.sequence})"
                )

                # イベントをストリーミングチャンクに変換
                chunk = await self._process_event(event)
                if chunk:
                    yield chunk

                # 完了イベントを処理したら完了状態に設定
                if event.event_type in [
                    EventType.COMPLETION_SUCCESS,
                    EventType.COMPLETION_FAILURE,
                ]:
                    self._completion_event.set()
                    self._is_completed = True
                    logger.info(
                        f"[{self.execution_id}] Completion event processed"
                    )

            except asyncio.TimeoutError:
                # 完了済みでキューが空なら終了
                if self._completion_event.is_set() and self._event_queue.empty():
                    logger.info(f"[{self.execution_id}] No more events, terminating")
                    break
                continue
            except Exception as e:
                logger.error(f"[{self.execution_id}] Error consuming events: {e}")
                break

        logger.info(f"[{self.execution_id}] Event consumption completed")

    async def _process_event(self, event: SequencedEvent) -> Optional[str]:
        """イベントをストリーミング用に処理"""
        streaming_event = event.to_streaming_event()

        if self._handler:
            try:
                return await self._handler(streaming_event)
            except Exception as e:
                logger.error(
                    f"[{self.execution_id}] Error in event handler: {e}"
                )
                return None
        else:
            # デフォルト: SSE形式で返す
            import json
            return f"data: {json.dumps(streaming_event.to_dict())}\n\n"

    async def drain(self, timeout: float = 0.1) -> None:
        """登録ハンドラを駆動してキューを消費する（SSE を返さない用途向け）。

        ``consume_events()`` は SSE ストリームを ``yield`` する設計のため、
        webhook / runner のように handler 側で配信が完結する用途では、消費を
        誰も回さないとイベントが配信されない（``emit`` + ``cleanup`` だけだと
        全イベントが破棄される）。本メソッドは ``consume_events()`` を内部で
        回して handler を発火させ、完了イベント後に自動終了する。

        使い方は2通り:
            # (a) すべて emit してから drain（逐次）
            await emitter.emit_event(...); ...; await emitter.emit_event(COMPLETION_SUCCESS, ...)
            await emitter.drain()

            # (b) 処理と並行に配信（背景タスク）
            consumer = asyncio.create_task(emitter.drain())
            ... emit ... COMPLETION_SUCCESS
            await consumer

        Args:
            timeout: イベント待機タイムアウト（秒、``consume_events`` と同じ）

        Note:
            内部で ``consume_events()`` を回すため、**単一 consumer 前提**です。
            同じ emitter で ``consume_events()`` を別途消費している場合は ``drain()``
            を併用しないでください（同一キューを分割消費してしまいます）。
        """
        async for _ in self.consume_events(timeout=timeout):
            pass

    def mark_completed(self) -> None:
        """
        手動で完了状態に設定

        Note:
            通常はCOMPLETION_SUCCESS/COMPLETION_FAILUREイベントで
            自動的に完了状態になります。
            このメソッドは特殊なケースでのみ使用してください。
        """
        self._is_completed = True
        self._completion_event.set()
        logger.info(f"[{self.execution_id}] Manually marked as completed")

    async def cleanup(self) -> None:
        """
        リソースのクリーンアップ

        キューに残っているイベントを破棄し、状態をリセットします。

        Example:
            >>> await emitter.cleanup()
        """
        # キューをクリア
        while not self._event_queue.empty():
            try:
                self._event_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        self._is_completed = True
        self._completion_event.set()
        logger.info(f"[{self.execution_id}] EventEmitter cleaned up")


def create_sse_handler() -> EventHandler:
    """
    SSE（Server-Sent Events）形式のイベントハンドラーを作成

    Returns:
        EventHandler: SSE形式でイベントを変換するハンドラー

    Example:
        >>> emitter = EventEmitter(
        ...     execution_id="exec-123",
        ...     handler=create_sse_handler()
        ... )
    """
    import json

    async def sse_handler(event: StreamingEvent) -> Optional[str]:
        return f"data: {json.dumps(event.to_dict())}\n\n"

    return sse_handler


def create_json_handler() -> EventHandler:
    """
    JSON形式のイベントハンドラーを作成

    Returns:
        EventHandler: JSON形式でイベントを変換するハンドラー

    Example:
        >>> emitter = EventEmitter(
        ...     execution_id="exec-123",
        ...     handler=create_json_handler()
        ... )
    """
    import json

    async def json_handler(event: StreamingEvent) -> Optional[str]:
        return json.dumps(event.to_dict())

    return json_handler
