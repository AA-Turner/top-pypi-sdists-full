"""
AGENTICSTAR Platform SDK - Marketplace Runner
ローカルで動く agent 関数を、Marketplace 互換の終端ライフサイクルへそのまま渡す。

開発者は agent 関数（ロジック 100% 自由）だけを書き、runner が
identity 読取 → 検証 → 入力取得 → agent 実行 → 結果保存/Webhook → terminal を
正確に 1 回 → cleanup を担う。手書きだった main ボイラープレートを SDK に集約する
（設計書 AGENTICSTAR_PLATFORM_SDK_IMPLEMENTATION_PLAN.md §2.1 / molt #1409）。

Example:
    >>> from agenticstar_platform import run_marketplace_agent
    >>>
    >>> async def my_agent(emitter, message: str) -> str:
    ...     return message.upper()  # ロジックは自由
    >>>
    >>> run_marketplace_agent(my_agent)

環境変数契約:
    identity（Marketplace executor が SandboxClaim spec.env で注入する。
    正本: executer-marketplace src/k8s_manager/pod_manager.py _build_dynamic_env）:
        EXECUTION_ID / CONVERSATION_ID / USER_ID / MESSAGE_ID   … 必須
        REQUEST_SOURCE / AGENT_ID                               … 任意
    infra（Marketplace のエージェント登録時に env var として設定する）:
        DB_HOST / DB_PORT / DB_DATABASE / DB_USER / DB_PASSWORD 等
            … PostgreSQLConfig.from_env() の契約に従う
        WEBHOOK_URL … 進捗/終端イベントの通知先

終端イベントの規約:
    - agent 関数が正常 return → runner が COMPLETION_SUCCESS を送る（戻り値が本文）
    - agent 関数が例外 → runner が COMPLETION_FAILURE を送り **None を返す**
      （traceback は logger のみ。agent の失敗は「イベントとして配信される業務結果」
      でありプロセスは正常終了する）
    - runner / インフラ自身の失敗（設定欠落・予期しない内部エラー・cancel）は
      **例外として raise** する（Pod の終了コード / 運用側で観測する事象のため）
    - agent 関数が自分で終端イベントを emit 済みなら runner は二重送信しない
      （README のローカルサンプルと同じ関数がそのまま動く）。terminal 送信後の
      イベント（進捗・二重 terminal）はすべて破棄され、terminal 後に agent が
      例外を投げても配信済みの終端は変わらない（ログのみ）
    - identity / infra 設定の欠落時は agent を呼ばずに MarketplaceRunnerConfigError

Note:
    - MESSAGE_ID は message-driven 実行では executor が必ず注入する
      （executor 実装上は「値がある場合のみ」の optional 枠。message 起点でない
      実行形態を将来 runner が扱う場合は契約拡張が必要）
    - ``run_marketplace_agent`` は内部で ``asyncio.run`` を使うため、稼働中の
      イベントループの中からは呼べない。その場合は ``arun_marketplace_agent`` を使う
"""

import asyncio
import contextlib
import json
import logging
from collections.abc import Awaitable, Callable, Mapping
from typing import Any

from .db import DataAccess, PostgreSQLConfig, create_postgresql_manager
from .db.execution_access import ExecutionAccess
from .events import EventEmitter, EventType
from .events.handlers import create_marketplace_handler

logger = logging.getLogger(__name__)

# Marketplace executor が agent コンテナへ注入する identity env（契約の正本は
# executer-marketplace src/k8s_manager/pod_manager.py _build_dynamic_env）。
# ここでの必須 4 つが揃わない実行は runner が agent を呼ばずに拒否する。
REQUIRED_IDENTITY_ENV = ("EXECUTION_ID", "CONVERSATION_ID", "USER_ID", "MESSAGE_ID")
OPTIONAL_IDENTITY_ENV = ("REQUEST_SOURCE", "AGENT_ID")

# infra env（エージェント登録時に marketplace_agent_env_vars として設定する）
WEBHOOK_URL_ENV = "WEBHOOK_URL"

# agent 関数の契約: (emitter, message) を受け取り、結果文字列を返す（None 可）
MarketplaceAgent = Callable[[EventEmitter, str], Awaitable[str | None]]


class MarketplaceRunnerConfigError(RuntimeError):
    """identity / infra 設定の欠落。agent 関数は呼ばれていない。"""


_TERMINAL_EVENT_TYPES = frozenset(
    {EventType.COMPLETION_SUCCESS, EventType.COMPLETION_FAILURE}
)


class _RunnerEventEmitter(EventEmitter):
    """terminal イベントの「正確に 1 回・かつ最終」を emit 境界で保証する EventEmitter。

    素の EventEmitter は「terminal をキューに入れた」事実を consumer が処理する
    まで観測できない（``is_completed`` は consumer 側で立つ）。そのため
    agent 関数が自分で terminal を emit した直後に runner 側が二重 emit する
    レースがあり、また terminal の後に積まれた進捗イベントも配信されてしまう。
    キュー投入時点で terminal を記録し、以降の**全イベント**を破棄する
    （terminal を真に最終イベントにする）。
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.terminal_emitted = False

    async def emit_event(self, event_type, message, metadata=None, sub_event_type=None):  # type: ignore[override]
        if self.terminal_emitted:
            logger.warning(
                "[%s] event after terminal suppressed: %s",
                self.execution_id,
                getattr(event_type, "value", event_type),
            )
            return
        if event_type in _TERMINAL_EVENT_TYPES:
            # 先にフラグを立てて同時 emit の二重投入を防ぎ、投入失敗時のみ戻す
            self.terminal_emitted = True
            try:
                await super().emit_event(event_type, message, metadata, sub_event_type)
            except BaseException:
                self.terminal_emitted = False
                raise
            return
        await super().emit_event(event_type, message, metadata, sub_event_type)


def _validate_identity(env: Mapping[str, str]) -> dict:
    """必須 identity env を検証して返す。欠落・空文字は設定エラー。"""
    missing = [name for name in REQUIRED_IDENTITY_ENV if not env.get(name)]
    if missing:
        raise MarketplaceRunnerConfigError(
            "Missing required environment variable(s): "
            + ", ".join(missing)
            + ". These are injected by the marketplace executor on the platform. "
            "When running elsewhere (local test etc.), set them explicitly or "
            "pass env={...} to run_marketplace_agent()."
        )
    return {name: env[name] for name in REQUIRED_IDENTITY_ENV}


def _latest_user_message(messages: list | None) -> str | None:
    """会話履歴から最新の user メッセージ本文を取り出す。"""
    if not messages:
        return None
    for entry in reversed(messages):
        if not isinstance(entry, dict) or entry.get("role") != "user":
            continue
        content = entry.get("content")
        if content is None or content == "":
            continue
        if isinstance(content, str):
            return content
        # multimodal 等の非文字列 content はそのまま JSON で渡す（情報を落とさない）
        return json.dumps(content, ensure_ascii=False)
    return None


async def arun_marketplace_agent(
    agent_func: MarketplaceAgent,
    *,
    env: Mapping[str, str] | None = None,
    webhook_url: str | None = None,
    db_config: PostgreSQLConfig | None = None,
    data_access: Any | None = None,
    event_handler: Callable | None = None,
    request_source: str | None = None,
) -> str | None:
    """agent 関数を Marketplace 互換ライフサイクルで実行する（async 版）。

    Args:
        agent_func: ``async def agent(emitter, message) -> Optional[str]``
        env: identity/infra の読取元（デフォルト: os.environ）。テストで注入可
        webhook_url: WEBHOOK_URL env の明示上書き
        db_config: PostgreSQLConfig の明示指定（デフォルト: from_env()。
            from_env は env 引数ではなく os.environ を読む）。
            create_postgresql_manager() でマネージャ化して接続する（DB 直結のみ。
            api_url / DB_API_PROXY_URL 設定時は MarketplaceRunnerConfigError）
        data_access: 構築済み DataAccess の注入（テスト / synthetic adapter 用。
            指定時は runner は接続の開閉を行わない）
        event_handler: EventEmitter に渡す handler の差し替え（テスト用。
            デフォルト: create_marketplace_handler による DB+Webhook 複合）
        request_source: REQUEST_SOURCE env の明示上書き

    Returns:
        agent 関数の戻り値（失敗時は None）

    Raises:
        MarketplaceRunnerConfigError: identity / WEBHOOK_URL の欠落、または
            api_url（DB_API_PROXY_URL）設定（runner は token_provider を供給できない）
            （agent 未呼出・イベント未送信のまま終了する）
    """
    if env is None:
        import os

        env = os.environ

    identity = _validate_identity(env)

    if event_handler is None:
        webhook_url = webhook_url or env.get(WEBHOOK_URL_ENV)
        if not webhook_url:
            raise MarketplaceRunnerConfigError(
                f"Missing webhook URL: set the {WEBHOOK_URL_ENV} environment variable "
                "(configure it as an agent env var on the marketplace) or pass "
                "webhook_url=... explicitly."
            )

    async with contextlib.AsyncExitStack() as stack:
        if data_access is None:
            config = db_config or PostgreSQLConfig.from_env()
            if config.api_url:
                # HTTP API モードは token_provider が必須だが runner には供給経路が
                # 無い。factory の ValueError に任せず設定エラーとして明示する
                raise MarketplaceRunnerConfigError(
                    "api_url (DB_API_PROXY_URL) is configured, but the "
                    "marketplace runner cannot supply the token_provider "
                    "required for HTTP-API mode. Unset DB_API_PROXY_URL to use "
                    "a direct DB connection, or build the manager yourself and "
                    "pass data_access=DataAccess(manager)."
                )
            data_access = await stack.enter_async_context(
                DataAccess(create_postgresql_manager(config))
            )

        handler = event_handler or create_marketplace_handler(
            data_access=data_access,
            webhook_url=webhook_url,
            user_id=identity["USER_ID"],
            conversation_id=identity["CONVERSATION_ID"],
            message_id=identity["MESSAGE_ID"],
            request_source=request_source or env.get("REQUEST_SOURCE", "internal"),
        )

        execution_id = identity["EXECUTION_ID"]
        emitter = _RunnerEventEmitter(execution_id=execution_id, handler=handler)
        # handler は drain() が駆動する（emit だけではイベントは配信されない）
        consumer = asyncio.create_task(emitter.drain())

        result: str | None = None
        runner_error: BaseException | None = None
        try:
            messages = await ExecutionAccess(data_access).get_messages(execution_id)
            message = _latest_user_message(messages)
            if message is None:
                # 入力が取れない実行は agent を呼ばずに terminal failure へ収束
                await emitter.emit_event(
                    EventType.COMPLETION_FAILURE,
                    f"input fetch failed: no user message found for execution "
                    f"{execution_id}",
                )
            else:
                try:
                    result = await agent_func(emitter, message)
                except Exception as exc:
                    # traceback は logger のみ（stdout / イベント本文へは出さない）
                    logger.exception(
                        "[%s] agent function raised", execution_id
                    )
                    if not emitter.terminal_emitted:
                        await emitter.emit_event(
                            EventType.COMPLETION_FAILURE,
                            f"agent failed: {type(exc).__name__}: {exc}",
                        )
                else:
                    if not emitter.terminal_emitted:
                        await emitter.emit_event(
                            EventType.COMPLETION_SUCCESS,
                            "" if result is None else str(result),
                        )
        except BaseException as exc:  # noqa: BLE001 — runner 自身の予期しない失敗
            runner_error = exc
            logger.exception("[%s] runner internal error", execution_id)
            if not emitter.terminal_emitted:
                try:
                    await emitter.emit_event(
                        EventType.COMPLETION_FAILURE,
                        f"runner internal error: {type(exc).__name__}",
                    )
                except BaseException:  # noqa: BLE001
                    emitter.mark_completed()
        finally:
            # emit 済みイベントは consumer が全量処理してから終了する。
            # terminal が 1 つも emit できなかった経路でも drain を停止させる
            if not emitter.terminal_emitted:
                emitter.mark_completed()
            try:
                await asyncio.shield(consumer)
            except BaseException as consumer_exc:  # noqa: BLE001 — 外部 cancel 含む
                # 配信中の consumer は中断しない（terminal は必ず届けきる）。
                # 自タスクが cancel されても consumer の完了を待つ。待ち時間は
                # handler 側の timeout（webhook ClientTimeout / DB command_timeout）
                # で有界。伝播はその後（runner_error 経由）
                while not consumer.done():
                    with contextlib.suppress(BaseException):
                        await asyncio.shield(consumer)
                # 既に本体エラーがある場合はそちらを優先し、二次エラーで塗り潰さない
                if runner_error is None:
                    runner_error = consumer_exc
            finally:
                # cleanup の失敗/cancel は既存の本体エラーを塗り潰さず、
                # 他にエラーが無い場合のみ表面化させる（正常 return に化けさせない）
                try:
                    await emitter.cleanup()
                except BaseException as cleanup_exc:  # noqa: BLE001
                    logger.exception("[%s] emitter cleanup failed", execution_id)
                    if runner_error is None:
                        runner_error = cleanup_exc

        if runner_error is not None:
            raise runner_error
        return result
    return result  # AsyncExitStack が例外を抑制した場合の保険（通常到達しない）


def run_marketplace_agent(
    agent_func: MarketplaceAgent,
    **kwargs: Any,
) -> str | None:
    """agent 関数を Marketplace 互換ライフサイクルで実行する（同期エントリ）。

    Pod の entrypoint から 1 行で呼ぶ想定。引数は
    :func:`arun_marketplace_agent` と同じ。

    Example:
        >>> from agenticstar_platform import run_marketplace_agent
        >>>
        >>> async def my_agent(emitter, message: str) -> str:
        ...     return message.upper()
        >>>
        >>> if __name__ == "__main__":
        ...     run_marketplace_agent(my_agent)
    """
    return asyncio.run(arun_marketplace_agent(agent_func, **kwargs))
