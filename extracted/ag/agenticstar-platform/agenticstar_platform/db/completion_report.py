"""
AGENTICSTAR Platform SDK - サイクル型の完遂報告（completion report）

サイクル型の実行（``execution_data.runtime_protocol`` = ``mp-chat/1``）で、Agent が「完遂したか」を
報告する。executor は **exit 0 の終端のときだけ** この報告を読み、あれば ``outcome`` に採用する
（devdocs 3.1req 指示書 37）。報告が無ければ従来どおり ``outcome`` なし・``runner_exited``（未計測）。

なぜ DB か: サイクル型の Agent には front の実行時 API が渡らない（開始済みの印
（``started_fence.py``）が DB 直結を選んだ理由と同じ）。印と同じ ``execution_messages`` に 1 行書く。
**DDL は要らない。**

``execution_data`` の列（``outcome`` / ``outcome_reason_code`` / ``completion_envelope``）は
**executor が書く**（writer の分担は変えない）。SDK は報告を置くだけで、成否を決めない。

報告は**任意**:
    - 報告しない Agent は従来どおり未計測。既存の Agent を壊さない（3.0 方向性メモ §4.5 の
      「任意の報告契約」）
    - 報告は 1 回。同じ実行に報告が既にあれば書かずに警告ログ（終端イベントの二重送信を捨てる
      既存の作りと揃える）。同時に 2 回呼ばれても 1 行だけになるよう、開始済みの印と同じく
      advisory lock で直列にしてから存在を確かめる（READ COMMITTED。ロック待ちの後の別の文で読む）
    - **書き込みの失敗で Agent の処理を失敗させない**（握って警告ログ・戻り値 False）。報告が
      無い = 未計測に落ちるだけ。印の fail closed とは逆（印は所有の証明なので raise する）
    - ``outcome`` の語彙違いだけは呼び出し側の誤りなので ``ValueError``。それ以外の値（ID・reason・summary）が
      壊れていても例外にせず ``False``。取消（``asyncio.CancelledError``）だけはそのまま伝える。
      対象は文書どおりの型の引数（str / bool / None。StrEnum など str の派生は値として扱う）と asyncpg の pool。
      ``__class__`` を偽装する・dunder が例外を投げるといった敵対的なオブジェクトまでは塞がない（Agent は同じ
      プロセスで何でもできるので、ここで防ぐ意味がない）
    - ``reason`` は理由コード（workflow runner と同じ短い snake_case）。合わない値（文章・例外の文字列・
      長すぎる値）は ``outcome`` に置き換えて警告ログ。executor は ``outcome_reason_code``（VARCHAR(64)）に
      そのまま書くので、長い値を置くと終端できなくなる

正常終了を完遂として読み替えてはいけない（3.0 方向性メモ §4.5 が撤回した案）。報告するかどうかと
何を報告するかは Agent が決める。
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
from typing import Any, Optional

logger = logging.getLogger(__name__)

# 保存語彙（3.0req 指示書 25 の 7 値）。新しい語彙を作らない
OUTCOMES = ("completed", "incomplete", "failed", "timeout", "stopped", "denied", "skipped")

# 理由コードの形（workflow runner の envelope と同じ規則）。workflow パッケージは runner 等を読み込むので
# import せずに同じ規則を置く
_REASON_RE = re.compile(r"^[a-z][a-z0-9_]{0,31}$")

REPORT_KIND = "sdk.runner.completion"
REPORT_MESSAGE = "Agent run completion reported"
LOCK_NAMESPACE = b"agenticstar.marketplace.runner.completion/1"
# 接続の取得・ロック待ち・各文の上限。報告は 1 行書くだけの短い transaction なので数秒〜数十秒で足りる
ACQUIRE_TIMEOUT_SECONDS = 30.0
LOCK_TIMEOUT = "10s"
STATEMENT_TIMEOUT = "30s"


def report_lock_key(conversation_id: str, message_id: str) -> int:
    """advisory lock の key（signed 64bit）。印（``started_fence.fence_lock_key``）とは namespace を分ける。"""
    digest = hashlib.sha256(
        LOCK_NAMESPACE + b"\0" + conversation_id.encode("utf-8") + b"\0" + message_id.encode("utf-8")
    ).digest()
    return int.from_bytes(digest[:8], "big", signed=True)


def _plain_str(value: Any) -> Optional[str]:
    """str（と StrEnum などの派生）を素の str にする。それ以外は None。派生の ``__eq__`` / ``__str__`` を呼ばない。"""
    return str.__str__(value) if isinstance(value, str) else None


def _cancelled_in_chain(error: BaseException) -> bool:
    """例外の連鎖に取消が含まれるか（取消中の rollback / release の失敗が取消を置き換えた場合）。

    ``raise ... from`` の cause と、暗黙の context の両方を辿る（cause が付いていても context 側に取消が残る）。
    """
    seen: set[int] = set()
    pending: list[Optional[BaseException]] = [error]
    while pending:
        current = pending.pop()
        if current is None or id(current) in seen:
            continue
        if isinstance(current, asyncio.CancelledError):
            return True
        seen.add(id(current))
        pending.append(current.__cause__)
        pending.append(current.__context__)
    return False


def normalize_reason(reason: Any, outcome: str, execution_id: str = "") -> str:
    """理由コードを正規化する。省略・空なら ``outcome``。合わない値は ``outcome`` に置き換える（例外を投げない）。

    正規化は workflow runner と同じ（前後の空白を除き、小文字にし、``-`` と空白を ``_`` に）。
    """
    try:
        # str の派生（``class Reason(str, Enum)`` など）は名前ではなく値を使う
        plain = _plain_str(reason)
        text = plain if plain is not None else str(reason or "")
        value = text.strip().lower().replace("-", "_").replace(" ", "_")
    except Exception:  # noqa: BLE001 — 文字列にできない値も呼び出し側の処理を止めない
        value = None
    if value == "":
        return outcome
    if value is not None and _REASON_RE.match(value):
        return value
    # 値そのものはログに出さない（例外の文字列や本文が入りうる）
    logger.warning(
        "[%s] completion reason is not a short snake_case code (^[a-z][a-z0-9_]{0,31}$); using the outcome %r",
        execution_id,
        outcome,
    )
    return outcome


def report_content(
    execution_id: str,
    outcome: str,
    reason: str,
    had_mutating_success: Optional[bool] = None,
    summary: Optional[str] = None,
) -> dict[str, Any]:
    """報告の content_data。印と同じ形（``{"progress_message": 本文}``）に報告の中身を足す。"""
    content: dict[str, Any] = {
        "progress_message": REPORT_MESSAGE,
        "kind": REPORT_KIND,
        "execution_id": execution_id,
        "outcome": outcome,
        "outcome_reason_code": reason,
        "had_mutating_success": had_mutating_success,
    }
    if summary is not None:
        content["summary"] = summary
    return content


async def report_completion(
    pool: Any,
    *,
    user_id: str,
    conversation_id: str,
    message_id: str,
    execution_id: str,
    outcome: str,
    reason: Optional[str] = None,
    had_mutating_success: Optional[bool] = None,
    summary: Optional[str] = None,
) -> bool:
    """完遂を報告する。書いたら True、書かなかったら False（既に報告済み / DB の失敗）。

    Args:
        pool: asyncpg の接続プール（``PostgreSQLManager.pool``）
        outcome: 7 値のいずれか。語彙外は ``ValueError``
        reason: 理由コード（短い snake_case。``^[a-z][a-z0-9_]{0,31}$``）。省略時と、正規化しても
            合わないときは ``outcome`` と同じ値
        had_mutating_success: 外部への書き込みの成功があったか（分からなければ None）
        summary: 人が読む補足（任意）

    Raises:
        ValueError: ``outcome`` が語彙外のとき（呼び出し側の誤り）。それ以外は例外にせず False
        asyncio.CancelledError: 呼び出し中に取消されたとき（握らない）
    """
    plain_outcome = _plain_str(outcome)
    if plain_outcome not in OUTCOMES:
        shown = repr(plain_outcome) if plain_outcome is not None else f"a {type(outcome).__name__}"
        raise ValueError(f"unknown outcome: {shown} (expected one of {', '.join(OUTCOMES)})")
    outcome = plain_outcome
    # ログに出す実行 ID。文字列でない値はログの整形で失敗しうるので出さない
    eid = _plain_str(execution_id) or "?"
    code = outcome
    try:
        # 正規化・中身の組み立て・key の生成も try の中（ID・reason・summary が壊れていても Agent の処理を止めない）
        code = normalize_reason(reason, outcome, eid)
        content = report_content(execution_id, outcome, code, had_mutating_success, summary)
        key = report_lock_key(conversation_id, message_id)
        async with pool.acquire(timeout=ACQUIRE_TIMEOUT_SECONDS) as conn:
            async with conn.transaction(isolation="read_committed"):
                await conn.execute(f"SET LOCAL lock_timeout = '{LOCK_TIMEOUT}'")
                await conn.execute(f"SET LOCAL statement_timeout = '{STATEMENT_TIMEOUT}'")
                # 同じ実行への同時の報告を直列にする（commit / rollback で解放）。存在確認はロックの後の別の文で
                # 読むので、先に commit した側の行が見える（DB の既定が REPEATABLE READ でも transaction で固定する）
                await conn.execute("SELECT pg_advisory_xact_lock($1)", key)
                exists = await conn.fetchval(
                    "SELECT EXISTS (SELECT 1 FROM execution_messages "
                    "WHERE conversation_id = $1 AND message_id = $2 "
                    "AND content_data->>'kind' = $3)",
                    conversation_id,
                    message_id,
                    REPORT_KIND,
                )
                if exists:
                    logger.warning(
                        "[%s] completion already reported for this message; keeping the first report",
                        eid,
                    )
                    return False
                await conn.execute(
                    "INSERT INTO execution_messages "
                    "(user_id, conversation_id, message_id, chunk_type, content_data) "
                    "VALUES ($1, $2, $3, 'progress_message', $4::jsonb)",
                    user_id,
                    conversation_id,
                    message_id,
                    json.dumps(content, ensure_ascii=False),
                )
    except Exception as e:  # noqa: BLE001 — 報告の失敗で Agent の処理を失敗させない
        if _cancelled_in_chain(e):
            # 取消の後片付け（rollback / release）が失敗して取消を置き換えた。取消は握らずに伝える
            raise asyncio.CancelledError() from e
        logger.warning(
            "[%s] completion report not confirmed (%s: %s); if it was not saved, the execution stays unmeasured",
            eid, type(e).__name__, e,
        )
        return False
    logger.info("[%s] completion reported: %s/%s", eid, outcome, code)
    return True
