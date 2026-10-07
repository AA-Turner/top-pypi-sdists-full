"""
AGENTICSTAR Platform SDK - 会話 runner の開始済みの印（started fence）

Marketplace の会話 runner（``arun_marketplace_agent``）が、サイクル型の実行（``execution_data.runtime_protocol``
= ``mp-chat/1``）で Agent を呼ぶ **前** に、同じ実行（conversation_id, message_id）の Agent を既に誰かが
始めていないかを DB で確かめ、始めていなければ印を永続化する。印があれば Agent を呼ばない。
サイクル型は「Agent 開始後に Pod が失われても同じ ID で再実行しない」契約（executer-marketplace の
chat_cycle_service）。通常の会話（restartPolicy=OnFailure で、異常終了の後に再起動して走り直す）は対象外。

なぜ DB か: 実行の workspace は emptyDir で、controller が Pod を作り直すと消える。
作り直された Pod の runner が同じ実行の Agent をもう一度走らせると、外部への書き込みが
二重になる（executor が ``pod_lost`` で回収するまでの照合間隔の間）。workflow runner は
server 側の fence を runtime API で取るが、会話 runner には DB 直結しか無い。

手順（1 つの接続・1 つの transaction の中で）:
    1. ``pg_advisory_xact_lock(key)`` — key は (conversation_id, message_id) から決定的に作る 64bit 値。
       同時に起動した 2 つの runner を直列にする（commit / rollback で解放。Agent 実行中は持たない）
    2. ``execution_messages`` に同じ (conversation_id, message_id) の行が **1 行でも** あるか
       （印に限らない。前の runner が書いたイベントも「始めていた」証拠として扱う）
    3. 無ければ印を 1 行 INSERT して commit。あれば ``StartedFenceTaken``

ロック待ちの後の存在確認は別の SQL 文なので、READ COMMITTED で先に commit した側の印が見える
（ロックと存在確認を 1 文にまとめると、待つ前の snapshot を読んでしまう）。分離レベルは transaction で
READ COMMITTED に固定する（DB の既定が REPEATABLE READ だと最初の文で snapshot が固定され、両方が通る）。

印は ``execution_messages`` に 1 行増える。この表を数える admin のダッシュボード（実行数・開始時刻・実行中の一覧）では
印も実行の 1 チャンクとして数え、開始時刻は印の時刻になる。実行トレース（実行記録から作る）には出ない。

DB の失敗（ロックの timeout・SELECT / INSERT / commit の失敗）は例外のまま返す = fail closed。
呼び出し側は Agent を呼ばずに止まる。commit の応答を失った場合も印は消さない（所有を推測しない）。
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

FENCE_NAMESPACE = b"agenticstar.marketplace.runner.started/1"
MARKER_KIND = "sdk.runner.started"
MARKER_MESSAGE = "Agent run started"
# ロック待ちの上限。同じ実行の別の runner が印を書くだけの短い transaction なので数秒で足りる
LOCK_TIMEOUT = "10s"
STATEMENT_TIMEOUT = "30s"


class StartedFenceTaken(RuntimeError):
    """同じ実行の Agent は既に始められていた（印か、前の runner のイベントがある）。"""


def fence_lock_key(conversation_id: str, message_id: str) -> int:
    """advisory lock の key（signed 64bit）。プロセスごとに変わる ``hash()`` は使わない。"""
    digest = hashlib.sha256(
        FENCE_NAMESPACE + b"\0" + conversation_id.encode("utf-8") + b"\0" + message_id.encode("utf-8")
    ).digest()
    return int.from_bytes(digest[:8], "big", signed=True)


def marker_content(execution_id: str) -> dict[str, Any]:
    """印の content_data。progress_message と同じ形（``{"progress_message": 本文}``）に印の種類と実行 ID を足す。"""
    return {"progress_message": MARKER_MESSAGE, "kind": MARKER_KIND, "execution_id": execution_id}


async def take_started_fence(
    pool: Any,
    *,
    user_id: str,
    conversation_id: str,
    message_id: str,
    execution_id: str,
) -> None:
    """開始済みの印を取る。取れたら None、既に取られていたら ``StartedFenceTaken``。

    Args:
        pool: asyncpg の接続プール（``PostgreSQLManager.pool``）
    """
    key = fence_lock_key(conversation_id, message_id)
    async with pool.acquire() as conn:
        async with conn.transaction(isolation="read_committed"):
            await conn.execute(f"SET LOCAL lock_timeout = '{LOCK_TIMEOUT}'")
            await conn.execute(f"SET LOCAL statement_timeout = '{STATEMENT_TIMEOUT}'")
            await conn.execute("SELECT pg_advisory_xact_lock($1)", key)
            exists = await conn.fetchval(
                "SELECT EXISTS (SELECT 1 FROM execution_messages "
                "WHERE conversation_id = $1 AND message_id = $2)",
                conversation_id,
                message_id,
            )
            if exists:
                raise StartedFenceTaken(
                    f"execution {execution_id}: the agent was already started for this message "
                    "(a previous runner left events or the started marker); not running it again"
                )
            await conn.execute(
                "INSERT INTO execution_messages "
                "(user_id, conversation_id, message_id, chunk_type, content_data) "
                "VALUES ($1, $2, $3, 'progress_message', $4::jsonb)",
                user_id,
                conversation_id,
                message_id,
                json.dumps(marker_content(execution_id), ensure_ascii=False),
            )
    logger.info("[%s] started fence taken", execution_id)
