"""
AGENTICSTAR Platform SDK - Event Handlers
イベントハンドラー実装（DB保存、Webhook送信、複合ハンドラー）

マーケットプレイスUI連携のための低レベル機能を提供。

Example:
    >>> from agenticstar_platform.events import EventEmitter
    >>> from agenticstar_platform.events.handlers import (
    ...     DatabaseEventHandler,
    ...     WebhookEventHandler,
    ...     CompositeEventHandler,
    ... )
    >>>
    >>> # DB + Webhookの複合ハンドラーを作成
    >>> db_handler = DatabaseEventHandler(
    ...     data_access=data_access,
    ...     user_id="user-123",
    ...     conversation_id="conv-456",
    ...     message_id="msg-789",
    ... )
    >>> webhook_handler = WebhookEventHandler(
    ...     webhook_url="http://your-api:3081/webhook/notify",
    ...     conversation_id="conv-456",
    ...     message_id="msg-789",
    ... )
    >>> composite = CompositeEventHandler([db_handler, webhook_handler])
    >>>
    >>> # EventEmitterに設定
    >>> emitter = EventEmitter(execution_id="exec-123", handler=composite)
"""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional

from .types import EventType
from .models import StreamingEvent, ExecutionMessage, build_content_data

logger = logging.getLogger(__name__)

# 受信側（chatboardfront monitoring.js）はトップレベル type で処理を分岐するため、
# HITL / progress_message はトップレベル type ごと切り替える必要がある。
# 本体 PodWebhookSubscriber (src/subscribers/pod_webhook.py) と同じ契約。
_DEFAULT_MESSAGE_TYPE_MAP: Dict[EventType, str] = {
    EventType.HITL_REQUIRED_BROWSER_VNC: "vnc_hitl_event",
    EventType.HITL_COMPLETED: "vnc_hitl_event",
    EventType.PROGRESS_MESSAGE: "progress_message",
}


class DatabaseEventHandler:
    """
    データベースにイベントを保存するハンドラー

    SDKのDataAccessを使用してexecution_messagesテーブルにイベントを保存。
    マーケットプレイスUIとの連携に使用。

    Features:
        - StreamingEventをExecutionMessageに変換
        - 汎用DataAccessによるDB保存
        - テーブル名のカスタマイズ対応

    Example:
        >>> from agenticstar_platform.db import DataAccess, PostgreSQLConfig
        >>>
        >>> config = PostgreSQLConfig.from_env()
        >>> async with DataAccess(config) as data_access:
        ...     handler = DatabaseEventHandler(
        ...         data_access=data_access,
        ...         user_id="user-123",
        ...         conversation_id="conv-456",
        ...         message_id="msg-789",
        ...     )
        ...     await handler(event)

    Note:
        テーブルスキーマ（execution_messages）:
        - user_id: VARCHAR
        - conversation_id: VARCHAR
        - message_id: VARCHAR
        - chunk_type: VARCHAR
        - content_data: JSONB
        - created_at: TIMESTAMP (自動設定)
    """

    def __init__(
        self,
        data_access: Any,  # DataAccess型だが循環インポート回避のためAny
        user_id: str,
        conversation_id: str,
        message_id: str,
        table_name: str = "execution_messages",
        chunk_type_map: Optional[Dict[EventType, str]] = None,
    ):
        """
        DatabaseEventHandlerを初期化

        Args:
            data_access: SDKのDataAccessインスタンス
            user_id: ユーザーID
            conversation_id: 会話ID
            message_id: メッセージID
            table_name: 保存先テーブル名（デフォルト: execution_messages）
            chunk_type_map: EventType→chunk_typeのカスタムマッピング（オプション）

        Example:
            >>> handler = DatabaseEventHandler(
            ...     data_access=data_access,
            ...     user_id="user-123",
            ...     conversation_id="conv-456",
            ...     message_id="msg-789",
            ... )
        """
        self.data_access = data_access
        self.user_id = user_id
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.table_name = table_name

        # デフォルトのchunk_typeマッピング
        self._chunk_type_map = chunk_type_map or {
            EventType.PHASE_START: "content",
            EventType.PROGRESS_UPDATE: "content",
            EventType.THOUGHT_MESSAGE: "reasoning_content",
            EventType.TOOL_START: "task_created",
            EventType.TOOL_RESULT: "task_created",
            EventType.FILE_CREATED: "task_created",
            EventType.USER_INTERACTION_REQUIRED: "content",
            EventType.COMPLETION_SUCCESS: "content",
            EventType.COMPLETION_FAILURE: "content",
            EventType.HITL_REQUIRED_BROWSER_VNC: "vnc_hitl_event",
            EventType.HITL_COMPLETED: "vnc_hitl_event",
            EventType.PROGRESS_MESSAGE: "progress_message",
            EventType.FINAL_RESULT: None,
        }

        logger.debug(
            f"DatabaseEventHandler initialized: table={table_name}, "
            f"user_id={user_id}, conversation_id={conversation_id}"
        )

    async def __call__(self, event: StreamingEvent) -> Optional[str]:
        """
        イベントをデータベースに保存

        Args:
            event: ストリーミングイベント

        Returns:
            None（DBハンドラーはストリーミングチャンクを返さない）
        """
        try:
            # chunk_typeを決定（Noneの場合はスキップ）
            chunk_type = self._chunk_type_map.get(event.event_type, "content")
            if chunk_type is None:
                logger.debug(f"Event skipped (chunk_type=None): {event.event_type.value}")
                return None

            # ExecutionMessageを作成
            exec_msg = ExecutionMessage.from_streaming_event(
                event=event,
                user_id=self.user_id,
                conversation_id=self.conversation_id,
                message_id=self.message_id,
                chunk_type=chunk_type,
            )

            # DataAccessでDB保存
            result = await self.data_access.insert(
                self.table_name,
                exec_msg.to_dict(),
            )

            if not result.get("success"):
                logger.error(
                    f"Failed to save event to database: {result.get('error')}"
                )
            else:
                logger.debug(
                    f"Event saved to database: {event.event_type.value}"
                )

            return None

        except Exception as e:
            logger.error(f"Error saving event to database: {e}")
            return None


class WebhookEventHandler:
    """
    Webhookにイベントを送信するハンドラー

    HTTP POSTでイベントをWebhookエンドポイントに送信。
    AgenticStar API等との連携に使用。

    Features:
        - 非同期HTTP POST送信
        - カスタムヘッダー対応
        - タイムアウト設定
        - メッセージフォーマットのカスタマイズ

    Example:
        >>> handler = WebhookEventHandler(
        ...     webhook_url="http://your-api:3081/webhook/notify",
        ...     conversation_id="conv-456",
        ...     message_id="msg-789",
        ... )
        >>> await handler(event)

    Note:
        送信されるJSON形式:
        {
            "type": "append_message",
            "data": {
                "conversationId": "...",
                "messageId": "...",
                "chunk_type": "content",
                "content": {"content": "..."},
                "finish_reason": null,
                "request_source": "external"
            }
        }

        トップレベル type はイベント種別で切り替わる（受信側 monitoring.js が
        type で処理を分岐するため）。デフォルトのマッピング:
          - HITL_REQUIRED_BROWSER_VNC / HITL_COMPLETED → "vnc_hitl_event"
            （content は metadata を素のまま送る）
          - PROGRESS_MESSAGE → "progress_message"
            （content は {"progress_message": "..."} 形式）
          - それ以外 → message_type（デフォルト: "append_message"）

        request_source は受信側（chatboardfront monitoring.js）が
        Progress SSE 配信（internal）と外部Webhook送信（external）の振り分けに使用する。
        指定しない場合は data から省略され、受信側のデフォルト挙動（internal扱い）となる。
    """

    def __init__(
        self,
        webhook_url: str,
        conversation_id: str,
        message_id: str,
        headers: Optional[Dict[str, str]] = None,
        timeout_seconds: int = 30,
        message_type: str = "append_message",
        token_provider: Optional[Callable[[], Optional[str]]] = None,
        chunk_type_map: Optional[Dict[EventType, str]] = None,
        request_source: Optional[str] = None,
        message_type_map: Optional[Dict[EventType, str]] = None,
    ):
        """
        WebhookEventHandlerを初期化

        Args:
            webhook_url: WebhookエンドポイントURL
            conversation_id: 会話ID
            message_id: メッセージID
            headers: カスタムHTTPヘッダー（オプション）
            timeout_seconds: リクエストタイムアウト秒数
            message_type: マッピングに無いイベントのトップレベルtype
                （デフォルト: append_message）
            token_provider: 認証トークン取得関数（オプション）
            chunk_type_map: EventType→chunk_typeのカスタムマッピング（オプション）
            request_source: リクエスト発信元（"internal" / "external"）。
                受信側で Progress SSE 配信 と 外部Webhook送信 の振り分けに使われる。
                None の場合は payload.data から省略される（受信側で internal 扱い）。
            message_type_map: EventType→トップレベルtypeのカスタムマッピング
                （オプション）。省略時は HITL系→"vnc_hitl_event"、
                PROGRESS_MESSAGE→"progress_message" を切り替えるデフォルトを使用。

        Example:
            >>> handler = WebhookEventHandler(
            ...     webhook_url="http://your-api:3081/webhook/notify",
            ...     conversation_id="conv-456",
            ...     message_id="msg-789",
            ...     headers={"X-Custom-Header": "value"},
            ...     request_source="external",
            ... )
        """
        self.webhook_url = webhook_url
        self.conversation_id = conversation_id
        self.message_id = message_id
        self.headers = headers or {}
        self.timeout_seconds = timeout_seconds
        self.message_type = message_type
        self.token_provider = token_provider
        self.request_source = request_source
        self._message_type_map = (
            message_type_map if message_type_map is not None
            else _DEFAULT_MESSAGE_TYPE_MAP
        )

        # デフォルトのchunk_typeマッピング
        self._chunk_type_map = chunk_type_map or {
            EventType.PHASE_START: "content",
            EventType.PROGRESS_UPDATE: "content",
            EventType.THOUGHT_MESSAGE: "reasoning_content",
            EventType.TOOL_START: "task_created",
            EventType.TOOL_RESULT: "task_created",
            EventType.FILE_CREATED: "task_created",
            EventType.USER_INTERACTION_REQUIRED: "content",
            EventType.COMPLETION_SUCCESS: "content",
            EventType.COMPLETION_FAILURE: "content",
            EventType.HITL_REQUIRED_BROWSER_VNC: "vnc_hitl_event",
            EventType.HITL_COMPLETED: "vnc_hitl_event",
            EventType.PROGRESS_MESSAGE: "progress_message",
            EventType.FINAL_RESULT: None,
        }

        # finish_reasonマッピング
        self._finish_reason_map = {
            EventType.COMPLETION_SUCCESS: "stop",
            EventType.COMPLETION_FAILURE: "error",
        }

        logger.debug(
            f"WebhookEventHandler initialized: url={webhook_url}, "
            f"conversation_id={conversation_id}"
        )

    async def __call__(self, event: StreamingEvent) -> Optional[str]:
        """
        イベントをWebhookに送信

        Args:
            event: ストリーミングイベント

        Returns:
            None（Webhookハンドラーはストリーミングチャンクを返さない）
        """
        try:
            # aiohttpをここでimport（オプション依存のため）
            try:
                import aiohttp
            except ImportError:
                logger.error(
                    "aiohttp is required for WebhookEventHandler: "
                    "pip install aiohttp"
                )
                return None

            # chunk_typeを決定（Noneの場合はスキップ）
            chunk_type = self._chunk_type_map.get(event.event_type, "content")
            if chunk_type is None:
                logger.debug(f"Webhook event skipped (chunk_type=None): {event.event_type.value}")
                return None

            # finish_reasonを決定
            finish_reason = self._finish_reason_map.get(event.event_type)

            # contentを構築（vnc_hitl_event / progress_message は本体と同じ独自形式）
            content = build_content_data(event, chunk_type)

            # Webhookペイロードを構築
            data: Dict[str, Any] = {
                "conversationId": self.conversation_id,
                "messageId": self.message_id,
                "chunk_type": chunk_type,
                "content": content,
                "finish_reason": finish_reason,
            }
            # request_source は受信側で Progress SSE / 外部Webhook の振り分けに使われる。
            # None の場合は payload に含めない（後方互換: 受信側で internal 扱い）。
            if self.request_source is not None:
                data["request_source"] = self.request_source

            # トップレベル type はイベント種別で切替（受信側が type で分岐するため）
            payload = {
                "type": self._message_type_map.get(event.event_type, self.message_type),
                "data": data,
            }

            # ヘッダーを設定
            headers = {"Content-Type": "application/json"}
            headers.update(self.headers)

            # トークンプロバイダーがあれば認証ヘッダーを追加
            if self.token_provider:
                token = self.token_provider()
                if token:
                    headers["Authorization"] = f"Bearer {token}"

            # HTTP POSTを送信
            timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    headers=headers,
                ) as response:
                    # レスポンスを読み取り（リソースリークを防ぐ）
                    await response.text()

                    if response.status == 200:
                        logger.debug(
                            f"Webhook notification sent: {event.event_type.value}"
                        )
                    else:
                        logger.warning(
                            f"Webhook returned status {response.status}"
                        )

            return None

        except asyncio.TimeoutError:
            logger.error("Webhook notification timeout")
            return None
        except Exception as e:
            logger.error(f"Error sending webhook notification: {e}")
            return None


class CompositeEventHandler:
    """
    複数のハンドラーを並列実行する複合ハンドラー

    DatabaseEventHandlerとWebhookEventHandlerを同時実行し、
    autonomousのPodWebhookSubscriberと同等の機能を提供。

    Features:
        - 複数ハンドラーの並列実行
        - エラー時も他のハンドラーは継続
        - 最初のSSEチャンクを返す（SSEハンドラーがある場合）

    Example:
        >>> db_handler = DatabaseEventHandler(...)
        >>> webhook_handler = WebhookEventHandler(...)
        >>> composite = CompositeEventHandler([db_handler, webhook_handler])
        >>>
        >>> # EventEmitterに設定
        >>> emitter = EventEmitter(
        ...     execution_id="exec-123",
        ...     handler=composite
        ... )

    Note:
        asyncio.gatherでreturn_exceptions=Trueを使用するため、
        一部のハンドラーがエラーでも他は正常に実行される。
    """

    def __init__(
        self,
        handlers: List[Callable[[StreamingEvent], Optional[str]]],
        return_first_chunk: bool = True,
    ):
        """
        CompositeEventHandlerを初期化

        Args:
            handlers: イベントハンドラーのリスト
            return_first_chunk: 最初のNon-Noneチャンクを返すか（デフォルト: True）

        Example:
            >>> composite = CompositeEventHandler([
            ...     DatabaseEventHandler(...),
            ...     WebhookEventHandler(...),
            ...     create_sse_handler(),  # SSEチャンクを返すハンドラー
            ... ])
        """
        self.handlers = handlers
        self.return_first_chunk = return_first_chunk

        logger.debug(
            f"CompositeEventHandler initialized with {len(handlers)} handlers"
        )

    async def __call__(self, event: StreamingEvent) -> Optional[str]:
        """
        全ハンドラーを並列実行

        Args:
            event: ストリーミングイベント

        Returns:
            最初のNon-Noneチャンク（return_first_chunk=Trueの場合）
            またはNone
        """
        try:
            # 全ハンドラーを並列実行
            tasks = [handler(event) for handler in self.handlers]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # エラーをログ出力
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    logger.error(
                        f"Handler {i} raised exception: {result}"
                    )

            # 最初のNon-Noneチャンクを返す
            if self.return_first_chunk:
                for result in results:
                    if result is not None and not isinstance(result, Exception):
                        return result

            return None

        except Exception as e:
            logger.error(f"Error in CompositeEventHandler: {e}")
            return None


def create_marketplace_handler(
    data_access: Any,
    webhook_url: str,
    user_id: str,
    conversation_id: str,
    message_id: str,
    token_provider: Optional[Callable[[], Optional[str]]] = None,
    request_source: Optional[str] = None,
) -> CompositeEventHandler:
    """
    マーケットプレイス向けの標準ハンドラーを作成

    DB保存 + Webhook送信の複合ハンドラーを簡単に作成するファクトリ関数。

    Args:
        data_access: SDKのDataAccessインスタンス
        webhook_url: WebhookエンドポイントURL
        user_id: ユーザーID
        conversation_id: 会話ID
        message_id: メッセージID
        token_provider: 認証トークン取得関数（オプション）
        request_source: リクエスト発信元（"internal" / "external"）。
            受信側で Progress SSE 配信 と 外部Webhook送信 の振り分けに使われる。
            外部API経由（extapi）からの呼び出しでは "external" を指定すること。
            通常はPod起動スクリプトで os.environ.get("REQUEST_SOURCE", "internal") を渡す。

    Returns:
        CompositeEventHandler: DB + Webhookの複合ハンドラー

    Example:
        >>> import os
        >>> from agenticstar_platform.db import DataAccess, PostgreSQLConfig
        >>> from agenticstar_platform.events import EventEmitter
        >>> from agenticstar_platform.events.handlers import create_marketplace_handler
        >>>
        >>> config = PostgreSQLConfig.from_env()
        >>> async with DataAccess(config) as da:
        ...     handler = create_marketplace_handler(
        ...         data_access=da,
        ...         webhook_url="http://your-api:3081/webhook/notify",
        ...         user_id="user-123",
        ...         conversation_id="conv-456",
        ...         message_id="msg-789",
        ...         request_source=os.environ.get("REQUEST_SOURCE", "internal"),
        ...     )
        ...     emitter = EventEmitter(execution_id="exec-001", handler=handler)
        ...     await emitter.emit(EventType.PHASE_START, "処理開始")
    """
    db_handler = DatabaseEventHandler(
        data_access=data_access,
        user_id=user_id,
        conversation_id=conversation_id,
        message_id=message_id,
    )

    webhook_handler = WebhookEventHandler(
        webhook_url=webhook_url,
        conversation_id=conversation_id,
        message_id=message_id,
        token_provider=token_provider,
        request_source=request_source,
    )

    return CompositeEventHandler([db_handler, webhook_handler])
