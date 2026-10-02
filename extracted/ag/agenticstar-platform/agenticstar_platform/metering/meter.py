"""
LLM 利用量・コスト計測 (usage metering)。

純インフラ: LLM 応答/トークンからコストを算出し、利用量台帳(DB)へ記録する。
エージェントロジックには非依存 ─ マーケットプレイス BYO でも自社 cli-api でも同一に使える。

コスト算出はプラガブル:
  - 既定 (`default_cost_fn`) は **litellm があれば** `litellm.completion_cost` /
    `litellm.cost_per_token` を使用 (long-context / cache / tier も litellm 側で反映)。
  - litellm が無ければコストは None (tokens のみ記録)。SDK は litellm を必須依存にしない。
  - `cost_fn` を渡せば任意エンジンに差し替え可能。

DB は duck-typed: ``execute_query(query: str, params) -> {"success", "data", "error"}`` を持つもの
(`agenticstar_platform.db.DataAccess` / `PostgreSQLManager`、および同契約の実装) をそのまま渡せる。

使用例::

    from agenticstar_platform.metering import UsageMeter

    meter = UsageMeter(db=data_access)
    await meter.ensure_schema()                       # 台帳/集計表が無ければ作成
    await meter.record(                               # 1 呼び出し = 1 行
        model="gpt-5.5", response=resp, endpoint="chat/completions",
        labels={"execution_id": eid, "message_id": mid, "user_id": uid},
    )
    usd = UsageMeter.cost_usd("gpt-5.5", response=resp)   # コストのみ
    await meter.rollup_recent()                       # 日次集計
    rows = await meter.daily_cost(by="model", since_days=30)
"""
from __future__ import annotations

import logging
import math
from decimal import Decimal, InvalidOperation
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

# cost_fn(model, response, usage) -> USD or None
CostFn = Callable[[str, Any, Optional[dict]], Optional[float]]


# ---------------------------------------------------------------------------
# usage 抽出 (OpenAI chat / responses / embeddings の shape 差を吸収)
# ---------------------------------------------------------------------------
def extract_usage(usage: Any) -> Optional[dict]:
    """usage オブジェクト/ dict から {input,output,total} tokens を取り出す。取れねば None。"""
    if usage is None:
        return None

    def _g(field: str):
        return usage.get(field) if isinstance(usage, dict) else getattr(usage, field, None)

    inp = _g("input_tokens")
    if inp is None:
        inp = _g("prompt_tokens")
    out = _g("output_tokens")
    if out is None:
        out = _g("completion_tokens")
    tot = _g("total_tokens")

    # cached 入力トークン: 直接の cached_tokens、無ければ details から。
    # chat = prompt_tokens_details / responses = input_tokens_details (両 shape を吸収)。
    cached = _g("cached_tokens")
    if cached is None:
        details = _g("prompt_tokens_details") or _g("input_tokens_details")
        if details is not None:
            cached = (details.get("cached_tokens") if isinstance(details, dict)
                      else getattr(details, "cached_tokens", None))
    if cached is None:
        cached = _g("cache_read_input_tokens")  # Anthropic 系 cache-read（直値）の fallback

    # cache 書込トークン (Anthropic 等が報告)。fallback の cache_creation 単価計算に使う。
    cache_creation = _g("cache_creation_input_tokens")

    # cache の読出し / 書込みの内訳 (単価が 0.1 倍 / 1.25 倍と 12.5 倍違う)。明示値 (cache_read_tokens /
    # cache_creation_tokens。0 を含む) が最優先、無ければ上で解決済みの cached / cache_creation をそのまま使う
    # (本関数が返す cached_tokens の規約 = 読出し。従来キーの解決順は変えない)。cached_tokens に 読出し + 書込み の
    # 合算を入れてくる呼び出し側 (cli-api の Anthropic proxy) は、必ず明示値で内訳を渡すこと。取れなければ None。
    # 値があるのに数値として読めないものは、ここでは捨てずにそのまま返す: コスト算出側がそれを見てコスト不明 (None) に
    # し (0 とみなして誤ったコストを出さない)、台帳へは record() が NULL として書く (行は失わない)。
    cache_read = _int_or_raw(_first_not_none(_g("cache_read_tokens"), cached))
    cache_write = _int_or_raw(_first_not_none(_g("cache_creation_tokens"), cache_creation))

    if inp is None and out is None and tot is None:
        return None
    if tot is None:
        tot = (inp or 0) + (out or 0)
    result = {
        "input_tokens": inp if inp is not None else 0,
        "output_tokens": out if out is not None else 0,
        "total_tokens": tot,
    }
    if cached is not None:
        result["cached_tokens"] = cached
    if cache_creation is not None:
        result["cache_creation_input_tokens"] = cache_creation
    if cache_read is not None:
        result["cache_read_tokens"] = cache_read
    if cache_write is not None:
        result["cache_creation_tokens"] = cache_write
    return result


def _response_usage(response: Any) -> Optional[dict]:
    if response is None:
        return None
    u = getattr(response, "usage", None)
    if u is None and isinstance(response, dict):
        u = response.get("usage")
    return extract_usage(u)


def _first_not_none(*values: Any) -> Any:
    return next((v for v in values if v is not None), None)


def _strict_int(value: Any) -> int:
    """cache トークン数として読める値だけを int にする。読めない値 (文字列の "n/a"・bool・NaN・±inf・オブジェクト) は送出する。
    「読めるか」の判定はここ 1 箇所 (台帳への NULL 化とコスト不明の判断が食い違わないようにする)。"""
    if isinstance(value, bool):
        raise TypeError("bool is not a token count")
    return int(value)  # TypeError / ValueError (NaN, 非数値) / OverflowError (±inf)


def _as_int(value: Any) -> Optional[int]:
    """整数へ寄せる。None と、数値として読めない値は None = 不明 (送出しない)。"""
    if value is None:
        return None
    try:
        return _strict_int(value)
    except (TypeError, ValueError, OverflowError):
        return None


def _int_or_raw(value: Any) -> Any:
    """整数として読めれば int、読めなければ元の値のまま返す (None は None)。"""
    converted = _as_int(value)
    return value if converted is None else converted


def _cache_creation_for_cost(usage: dict) -> int:
    """cost 算出に渡す cache 書込みトークン数。明示値 (0 を含む) が生値より優先。

    値が無ければ 0。値があるのに数値として読めないときは送出する (呼び出し元の default_cost_fn が握り、
    コスト不明 = None を返す。読めない値を 0 とみなして誤ったコストを出さない)。
    """
    value = _first_not_none(usage.get("cache_creation_tokens"), usage.get("cache_creation_input_tokens"))
    return 0 if value is None else _strict_int(value)


def _cache_read_for_cost(usage: dict) -> int:
    """cost 算出に渡す cache 読出しトークン数。

    明示値 (cache_read_tokens) > cached_tokens (規約 = 読出し)。cached_tokens に 読出し + 書込み の合算を入れてくる
    呼び出し側は明示値を渡すので、合算が読出しとして課金される (書込み分が 0.1 倍でも数えられてコスト過小になる)
    ことは無い。明示値の無い従来の usage では、これまでと同じ値を渡す。読めない値の扱いは書込みと同じ。
    """
    value = _first_not_none(usage.get("cache_read_tokens"), usage.get("cached_tokens"))
    return 0 if value is None else _strict_int(value)


def default_cost_fn(model: str, response: Any = None, usage: Optional[dict] = None) -> Optional[float]:
    """litellm があればコスト(USD)を算出。無ければ None (＝SDK は litellm 非必須)。

    response 優先 (litellm.completion_cost は long-context/cache/tier を反映)、
    取れなければ usage の token 数から cost_per_token で算出。全例外は握る。
    """
    try:
        import litellm  # type: ignore
    except Exception:
        return None
    try:
        if response is not None:
            c = litellm.completion_cost(completion_response=response)
            if c is not None:
                return float(c)
    except Exception:
        pass
    try:
        if usage and (usage.get("input_tokens") or usage.get("output_tokens")):
            # cache 割引を fallback でも反映する。litellm.cost_per_token は prompt_tokens を
            # cache 込みの総入力として扱い、cache_read / cache_creation を内部で差し引いて
            # それぞれの単価で課金する (実測確認済: 1000総入力/900cache → 非cache100満額+900を
            # 0.1x)。これらを渡さないと cache hit 分も満額計上され、completion_cost 失敗時
            # (例: 未マップ model / response 欠落) のコストが過大になる。
            pc, cc = litellm.cost_per_token(
                model=model,
                prompt_tokens=int(usage.get("input_tokens") or 0),
                completion_tokens=int(usage.get("output_tokens") or 0),
                cache_read_input_tokens=_cache_read_for_cost(usage),
                cache_creation_input_tokens=_cache_creation_for_cost(usage),
            )
            return float(pc or 0) + float(cc or 0)
    except Exception:
        pass
    return None


def round_cost_usd(v: Any) -> Any:
    """cost(USD) を numeric へ綺麗に格納するため Decimal 整形（float 表現ゆらぎ抑制、8 桁）。

    billing の合算精度には影響しない。None / 非数 / bool はそのまま返す。
    worker(UsageMeter.record) と gateway 監査ログ(audit) で共有する単一実装。
    """
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return v
    if not math.isfinite(v):
        return None  # NaN/Inf は格納しない
    try:
        return Decimal(str(round(v, 8)))
    except (InvalidOperation, ValueError):
        return v


# ---------------------------------------------------------------------------
# スキーマ (BYO 向けの可搬な既定。大規模では月次パーティション化を推奨)
# ---------------------------------------------------------------------------
LEDGER_DDL = """
CREATE TABLE IF NOT EXISTS llm_usage_ledger (
    id              bigint        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    created_at      timestamptz   NOT NULL DEFAULT now(),
    execution_id    text,
    message_id      text,
    conversation_id text,
    user_id         text,
    request_id      text,
    endpoint        text,
    agent_type      text,
    level           text,
    model           text          NOT NULL,
    stream          boolean,
    success         boolean,
    usage_status    text,
    missing_reason  text,
    input_tokens    integer,
    output_tokens   integer,
    total_tokens    integer,
    cached_tokens   integer,
    cache_read_tokens     integer,
    cache_creation_tokens integer,
    cost_usd        numeric(14,8),
    currency        text          NOT NULL DEFAULT 'USD'
)
"""

LEDGER_INDEXES = (
    "CREATE INDEX IF NOT EXISTS idx_llm_usage_exec_msg ON llm_usage_ledger (execution_id, message_id)",
    "CREATE INDEX IF NOT EXISTS idx_llm_usage_conv     ON llm_usage_ledger (conversation_id)",
    "CREATE INDEX IF NOT EXISTS idx_llm_usage_user_ts  ON llm_usage_ledger (user_id, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_llm_usage_model_ts ON llm_usage_ledger (model, created_at)",
)

DAILY_DDL = """
CREATE TABLE IF NOT EXISTS llm_usage_daily (
    day            date          NOT NULL,
    user_id        text          NOT NULL DEFAULT '',
    model          text          NOT NULL DEFAULT '',
    agent_type     text          NOT NULL DEFAULT '',
    calls          integer       NOT NULL DEFAULT 0,
    input_tokens   bigint        NOT NULL DEFAULT 0,
    output_tokens  bigint        NOT NULL DEFAULT 0,
    total_tokens   bigint        NOT NULL DEFAULT 0,
    cached_tokens  bigint        NOT NULL DEFAULT 0,
    cost_usd       numeric(16,6) NOT NULL DEFAULT 0,
    updated_at     timestamptz   NOT NULL DEFAULT now(),
    PRIMARY KEY (day, user_id, model, agent_type)
)
"""

ROLLUP_FN_DDL = """
CREATE OR REPLACE FUNCTION rollup_llm_usage_daily(p_day date) RETURNS void AS $fn$
BEGIN
    -- 複数 replica が同時実行すると DELETE+INSERT が PK 衝突する
    -- (READ COMMITTED で後発の DELETE が先発コミット前の行を見えず 0 行削除 → INSERT 衝突)。
    -- ロックを取れなかった側は skip する: 勝った側が同じ ledger から同一集計を書くので冗長。
    IF NOT pg_try_advisory_xact_lock(hashtext('rollup_llm_usage_daily'), p_day - date '2000-01-01') THEN
        RETURN;
    END IF;
    DELETE FROM llm_usage_daily WHERE day = p_day;
    INSERT INTO llm_usage_daily
      (day, user_id, model, agent_type, calls, input_tokens, output_tokens,
       total_tokens, cached_tokens, cost_usd, updated_at)
    SELECT p_day, COALESCE(user_id,''), COALESCE(model,''), COALESCE(agent_type,''),
           count(*), COALESCE(sum(input_tokens),0), COALESCE(sum(output_tokens),0),
           COALESCE(sum(total_tokens),0), COALESCE(sum(cached_tokens),0),
           COALESCE(sum(cost_usd),0), now()
    FROM llm_usage_ledger
    WHERE created_at >= p_day::timestamptz AND created_at < (p_day + 1)::timestamptz
    GROUP BY COALESCE(user_id,''), COALESCE(model,''), COALESCE(agent_type,'');
END; $fn$ LANGUAGE plpgsql
"""

_INSERT_SQL = """
INSERT INTO llm_usage_ledger
  (execution_id, message_id, conversation_id, user_id, request_id, endpoint,
   agent_type, level, model, stream, success, usage_status, missing_reason,
   input_tokens, output_tokens, total_tokens, cached_tokens, cost_usd, currency,
   cache_read_tokens, cache_creation_tokens)
VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21)
"""

# 既存 (列なし) テーブルへの後方互換 migration。INSERT は下の列を前提にするので、既存テーブルには
# ensure_schema() (cli-api は起動時に呼ぶ) か Alembic で先に当てること。partition 親へ ADD COLUMN すると
# 全パーティションへ伝播し、metadata-only(PG11+)で即時・無 rewrite。BYO/fresh は
# LEDGER_DDL で既に列を持つので冪等。live(月次パーティション)はこの ALTER を deploy 前に当てる。
LEDGER_MIGRATIONS = (
    "ALTER TABLE llm_usage_ledger ADD COLUMN IF NOT EXISTS missing_reason text",
    "ALTER TABLE llm_usage_ledger ADD COLUMN IF NOT EXISTS cache_read_tokens integer",
    "ALTER TABLE llm_usage_ledger ADD COLUMN IF NOT EXISTS cache_creation_tokens integer",
)

# daily_cost の集計軸ホワイトリスト (SQL identifier 注入防止: ユーザー入力を直接埋めない)
_DAILY_GROUP_COLS = {"model": "model", "user": "user_id", "agent": "agent_type", "day": "day"}


class UsageMeter:
    """LLM 利用量・コストの計測と記録。"""

    def __init__(self, db: Any, *, cost_fn: Optional[CostFn] = None, currency: str = "USD"):
        """
        Args:
            db: ``execute_query(query, params) -> {"success","data","error"}`` を持つ DB ハンドル
                (agenticstar_platform.db.DataAccess / PostgreSQLManager / 互換実装)。
            cost_fn: コスト算出関数 (既定: litellm があれば使用、無ければ None)。
            currency: 記録通貨ラベル (既定 USD。FX は集計/表示時に適用)。
        """
        self._db = db
        self._cost_fn: CostFn = cost_fn or default_cost_fn
        self._currency = currency

    # --- コスト算出 (記録なし) ---------------------------------------------
    @staticmethod
    def cost_usd(model: str, response: Any = None, usage: Any = None,
                 cost_fn: Optional[CostFn] = None) -> Optional[float]:
        """コスト(USD)のみ算出。usage は dict / usage オブジェクトどちらでも可。"""
        fn = cost_fn or default_cost_fn
        u = usage if isinstance(usage, dict) else extract_usage(usage)
        try:
            return fn(model, response, u)
        except Exception:
            return None

    # --- スキーマ作成 (BYO 向け。既存環境では不要) -------------------------
    async def ensure_schema(self, *, with_rollup: bool = True) -> None:
        """台帳/集計表/集計関数が無ければ作成する (冪等)。

        既に運用中(例: cli-api の月次パーティション版)では呼ぶ必要は無い。
        大規模では `llm_usage_ledger` の月次パーティション化を別途推奨。
        """
        await self._db.execute_query(LEDGER_DDL, ())
        for ddl in LEDGER_INDEXES:
            await self._db.execute_query(ddl, ())
        for ddl in LEDGER_MIGRATIONS:  # 既存テーブルへの後方互換列追加 (冪等)
            await self._db.execute_query(ddl, ())
        await self._db.execute_query(DAILY_DDL, ())
        if with_rollup:
            await self._db.execute_query(ROLLUP_FN_DDL, ())

    # --- 記録 --------------------------------------------------------------
    async def record(self, *, model: str, response: Any = None, usage: Any = None,
                     endpoint: Optional[str] = None, agent_type: Optional[str] = None,
                     level: Optional[str] = None, labels: Optional[dict] = None,
                     stream: bool = False, success: bool = True,
                     request_id: Optional[str] = None, cost_usd: Optional[float] = None,
                     missing_reason: Optional[str] = None,
                     fail_safe: bool = True) -> Optional[float]:
        """1 LLM 呼び出しを台帳へ記録し、算出コスト(USD)を返す。

        labels に execution_id / message_id / conversation_id / user_id を入れる(欠落は NULL)。
        cost_usd 未指定時は cost_fn で算出。fail_safe=True なら記録失敗を握り潰す(呼び出し元を壊さない)。
        missing_reason は usage 欠落時の理由(provider_omitted / stream_interrupted 等)。usage が
        取れた行では矛盾を避けるため NULL を保存する(present 行に reason は付けない)。ログだけでなく
        台帳/offline export 側に残し、cost_usd is NULL / usage_status=missing / true-zero を区別可能にする。
        """
        # fail_safe=True のとき record は決して送出しない(extract/params/INSERT 全体を保護)。
        # cost_fn の失敗だけは個別に握り、token だけは記録できるようにする。
        try:
            labels = labels or {}
            u = extract_usage(usage) if usage is not None else _response_usage(response)
            if cost_usd is None:
                try:
                    cost_usd = self._cost_fn(model, response, u)
                except Exception:
                    cost_usd = None
            u = u or {}
            # present 行に missing_reason は付けない(矛盾防止)。missing 行のみ理由を保存。
            mr = None if u else (missing_reason or None)
            params = (
                labels.get("execution_id"), labels.get("message_id"),
                labels.get("conversation_id"), labels.get("user_id"),
                request_id, endpoint, agent_type, level, model,
                bool(stream), bool(success), ("present" if u else "missing"), mr,
                u.get("input_tokens"), u.get("output_tokens"), u.get("total_tokens"),
                u.get("cached_tokens"), round_cost_usd(cost_usd), self._currency,
                _as_int(u.get("cache_read_tokens")), _as_int(u.get("cache_creation_tokens")),
            )
            await self._db.execute_query(_INSERT_SQL, params)
        except Exception as e:
            if not fail_safe:
                raise
            logger.warning("usage ledger record skipped: %s: %s", type(e).__name__, e)
        return cost_usd

    def track(self, *, model: Optional[str] = None, endpoint: Optional[str] = None,
              agent_type: Optional[str] = None, level: Optional[str] = None,
              labels: Optional[dict] = None, fail_safe: bool = True):
        """async LLM 呼び出しをラップし、完了時に自動記録するデコレータ。

        例::
            resp = await meter.track(model="gpt-5.5", labels=ids)(litellm.acompletion)(**params)
        """
        def deco(fn):
            async def wrapped(*args, **kwargs):
                resp = await fn(*args, **kwargs)
                m = model or kwargs.get("model") or ""
                await self.record(model=m, response=resp, endpoint=endpoint,
                                  agent_type=agent_type, level=level, labels=labels,
                                  stream=bool(kwargs.get("stream")), fail_safe=fail_safe)
                return resp
            return wrapped
        return deco

    # --- 集計 / 可視化 -----------------------------------------------------
    async def rollup_recent(self) -> None:
        """前日・当日分を集計表 (llm_usage_daily) へ反映 (冪等)。"""
        await self._db.execute_query("SELECT rollup_llm_usage_daily((now()::date - 1))", ())
        await self._db.execute_query("SELECT rollup_llm_usage_daily(now()::date)", ())

    async def daily_cost(self, *, by: str = "model", since_days: int = 30) -> list:
        """集計表からコスト内訳を取得 (可視化/請求用)。

        by: 'model' | 'user' | 'agent' | 'day' (ホワイトリスト。それ以外は 'model')。
        """
        col = _DAILY_GROUP_COLS.get(by, "model")
        sql = (
            f"SELECT {col} AS key, sum(cost_usd) AS cost_usd, "
            f"sum(total_tokens) AS tokens, sum(calls) AS calls "
            # $1 は無キャストだと date - date に解決され day >= integer で常時失敗する (dev-portal#170)
            f"FROM llm_usage_daily WHERE day >= (now()::date - $1::int) "
            f"GROUP BY {col} ORDER BY cost_usd DESC"
        )
        result = await self._db.execute_query(sql, (since_days,))
        if isinstance(result, dict):
            if result.get("success") is False:
                logger.warning("daily_cost query failed: %s", result.get("error"))
                return []
            return result.get("data", []) or []
        return result or []
