"""UsageMeter の prompt cache 内訳 (cache_read_tokens / cache_creation_tokens) の unit test。

DB 不要。duck-typed な DB で execute_query(query, params) を記録する。検証する契約:
  - 内訳は明示値 (0 を含む) > provider の生 usage > cached_tokens (規約 = 読出し)。取れなければ NULL (0 で埋めない)
  - 明示値の無い従来の usage は、抽出もコストもこれまでと同じ (gateway の累積 dict / OpenAI 系を変えない)
  - cached_tokens に合算を入れてくる呼び出し側 (cli-api の Anthropic proxy) は明示値で内訳を渡し、それで課金される
  - 既存テーブルへの列追加は ensure_schema() の LEDGER_MIGRATIONS (冪等) が担う。日次集計表・集計関数は変えない
"""
import asyncio

import pytest

from agenticstar_platform.metering.meter import (
    _INSERT_SQL,
    DAILY_DDL,
    LEDGER_DDL,
    LEDGER_MIGRATIONS,
    ROLLUP_FN_DDL,
    UsageMeter,
    default_cost_fn,
    extract_usage,
)

_CACHED_IDX, _READ_IDX, _CREATION_IDX = 16, 19, 20


class _DB:
    """execute_query を記録するだけの duck-typed DB。"""

    def __init__(self):
        self.calls = []

    async def execute_query(self, query, params):
        self.calls.append((query, params))
        return {"success": True, "data": []}

    def inserts(self):
        return [(q, p) for q, p in self.calls if "INSERT INTO llm_usage_ledger" in q]


def _record(db, **kw):
    asyncio.run(UsageMeter(db=db, cost_fn=lambda *a: 0.5).record(model="bedrock/x", **kw))
    return db.inserts()


# --- extract_usage --------------------------------------------------------------------------

def test_explicit_split_wins_and_cached_tokens_keeps_its_meaning():
    u = extract_usage({"input_tokens": 1000, "output_tokens": 5, "cached_tokens": 900,
                       "cache_read_tokens": 600, "cache_creation_tokens": 300})
    assert (u["cached_tokens"], u["cache_read_tokens"], u["cache_creation_tokens"]) == (900, 600, 300)


def test_anthropic_raw_usage_shape():
    u = extract_usage({"input_tokens": 10, "output_tokens": 5,
                       "cache_read_input_tokens": 700, "cache_creation_input_tokens": 200})
    assert (u["cache_read_tokens"], u["cache_creation_tokens"]) == (700, 200)


def test_openai_shape_cached_tokens_is_read_and_creation_is_unknown():
    u = extract_usage({"prompt_tokens": 1000, "completion_tokens": 5, "prompt_tokens_details": {"cached_tokens": 800}})
    assert u["cache_read_tokens"] == 800 and "cache_creation_tokens" not in u


def test_cached_tokens_without_explicit_split_is_read_by_convention():
    """cached_tokens の規約は読出し。書込みが併記されていても差し引かない (gateway は SDK で正規化済みの
    {cached_tokens = 読出し, cache_creation_input_tokens} を累積して渡してくる)。details 由来でも同じ。"""
    direct = extract_usage({"input_tokens": 1000, "output_tokens": 5, "cached_tokens": 800, "cache_creation_input_tokens": 200})
    details = extract_usage({"prompt_tokens": 1000, "completion_tokens": 5, "prompt_tokens_details": {"cached_tokens": 800},
                             "cache_creation_input_tokens": 200})
    for u in (direct, details):
        assert (u["cached_tokens"], u["cache_read_tokens"], u["cache_creation_tokens"]) == (800, 800, 200)


def test_explicit_zero_creation_is_not_overridden_by_the_raw_field():
    u = extract_usage({"input_tokens": 1000, "output_tokens": 5, "cached_tokens": 600,
                       "cache_creation_tokens": 0, "cache_creation_input_tokens": 200})
    assert (u["cache_read_tokens"], u["cache_creation_tokens"]) == (600, 0)


BAD_VALUES = ["n/a", object(), [1], float("nan"), float("inf"), float("-inf"), True, False]


@pytest.mark.parametrize("bad", BAD_VALUES)
def test_unreadable_split_values_do_not_raise_and_are_kept_for_the_cost_function(bad):
    u = extract_usage({"input_tokens": 10, "output_tokens": 5, "cache_read_tokens": bad, "cache_creation_tokens": bad})
    assert u["cache_read_tokens"] is bad and u["cache_creation_tokens"] is bad   # 捨てない (コスト側が不明と判断する)
    assert (u["input_tokens"], u["output_tokens"]) == (10, 5)


def test_numeric_strings_and_floats_are_coerced_to_int():
    u = extract_usage({"input_tokens": 10, "output_tokens": 5, "cache_read_tokens": 900.0, "cache_creation_tokens": "300"})
    assert (u["cache_read_tokens"], u["cache_creation_tokens"]) == (900, 300)
    assert type(u["cache_read_tokens"]) is int and type(u["cache_creation_tokens"]) is int


def test_no_cache_information_leaves_split_absent():
    u = extract_usage({"input_tokens": 10, "output_tokens": 5})
    assert "cache_read_tokens" not in u and "cache_creation_tokens" not in u and "cached_tokens" not in u


# --- INSERT -----------------------------------------------------------------------------------

def test_insert_carries_split_after_the_legacy_columns():
    assert _INSERT_SQL.count("$") == 21
    (query, params), = _record(_DB(), usage={"input_tokens": 1000, "output_tokens": 5, "cached_tokens": 900,
                                             "cache_read_tokens": 600, "cache_creation_tokens": 300})
    assert query == _INSERT_SQL and len(params) == 21
    assert (params[_CACHED_IDX], params[_READ_IDX], params[_CREATION_IDX]) == (900, 600, 300)


def test_unknown_split_is_stored_as_null_not_zero():
    (_, params), = _record(_DB(), usage={"input_tokens": 10, "output_tokens": 5})
    assert params[_READ_IDX] is None and params[_CREATION_IDX] is None


@pytest.mark.parametrize("key", ["cache_read_tokens", "cache_creation_tokens", "cache_creation_input_tokens"])
@pytest.mark.parametrize("bad", ["n/a", float("inf"), False, True])
def test_unreadable_cache_value_keeps_the_row_with_null_split_and_unknown_cost(key, bad):
    """値があるのに読めない: 台帳の行は失わず内訳は NULL、コストは 0 とみなして計算せず不明 (NULL) にする。"""
    db = _DB()
    usage = {"input_tokens": 1000, "output_tokens": 5, key: bad}
    asyncio.run(UsageMeter(db=db).record(model="bedrock/global.anthropic.claude-sonnet-4-6", usage=usage))
    (_, params), = db.inserts()
    assert params[13] == 1000                                           # 行は記録される
    assert params[17] is None                                           # cost_usd は不明
    if key == "cache_read_tokens":
        assert params[_READ_IDX] is None
    if key in ("cache_creation_tokens", "cache_creation_input_tokens"):
        assert params[_CREATION_IDX] is None


def test_missing_usage_row_has_null_split():
    (_, params), = _record(_DB(), usage=None, missing_reason="provider_omitted")
    assert params[11] == "missing" and params[_READ_IDX] is None and params[_CREATION_IDX] is None


# --- DDL ----------------------------------------------------------------------------------------

def test_ledger_schema_and_migrations_carry_the_split_and_the_daily_rollup_is_untouched():
    """内訳は台帳 (llm_usage_ledger) にだけ持つ。日次集計表と集計関数は変えない: 集計関数はどの版の SDK も
    起動時に上書きする共有物で、そこに内訳を載せると新旧 SDK の混在時に上書き競合で値が 0 に戻る。"""
    assert "cache_read_tokens" in LEDGER_DDL and "cache_creation_tokens" in LEDGER_DDL
    assert sum("llm_usage_ledger ADD COLUMN IF NOT EXISTS cache_" in m for m in LEDGER_MIGRATIONS) == 2
    assert "cache_read_tokens" not in DAILY_DDL and "cache_read_tokens" not in ROLLUP_FN_DDL


def test_ensure_schema_adds_the_ledger_columns():
    db = _DB()
    asyncio.run(UsageMeter(db=db).ensure_schema())
    executed = [q for q, _ in db.calls]
    assert all(m in executed for m in LEDGER_MIGRATIONS)
    assert executed.index(LEDGER_DDL) < executed.index(LEDGER_MIGRATIONS[-1])


def _legacy_cached_and_creation(usage):
    """1.0.4 までの extract_usage が cached_tokens / cache_creation_input_tokens を解決していた規則 (比較用)。"""
    g = usage.get
    cached = g("cached_tokens")
    if cached is None:
        details = g("prompt_tokens_details") or g("input_tokens_details")
        if details is not None:
            cached = details.get("cached_tokens")
    if cached is None:
        cached = g("cache_read_input_tokens")
    return cached, g("cache_creation_input_tokens")


def test_usage_without_the_explicit_split_resolves_exactly_as_before():
    """明示の内訳キーが無い usage は、従来キーの値も新しい内訳も 1.0.4 までの解決結果と一致する
    (= OpenAI 系・gateway の累積 dict の記録とコストを変えない)。"""
    import random

    rng = random.Random(5)
    keys = ["input_tokens", "prompt_tokens", "output_tokens", "completion_tokens", "total_tokens",
            "cached_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"]
    checked = 0
    for _ in range(3000):
        usage = {k: rng.choice([None, 0, 5, 800, 100_000]) for k in keys if rng.random() < 0.6}
        if rng.random() < 0.4:
            usage[rng.choice(["prompt_tokens_details", "input_tokens_details"])] = {"cached_tokens": rng.choice([None, 0, 700])}
        got = extract_usage(usage)
        if got is None:
            continue
        checked += 1
        cached, creation = _legacy_cached_and_creation(usage)
        assert got.get("cached_tokens") == cached and got.get("cache_creation_input_tokens") == creation, usage
        assert got.get("cache_read_tokens") == cached and got.get("cache_creation_tokens") == creation, usage
    assert checked > 2000


# --- cost fallback ------------------------------------------------------------------------------

@pytest.fixture
def cost_kwargs(monkeypatch):
    """default_cost_fn が litellm.cost_per_token へ渡す引数を捕捉する (価格表・ネットワークに依存しない)。"""
    litellm = pytest.importorskip("litellm")
    seen = {}

    def fake(**kwargs):
        seen.update(kwargs)
        return 1.0, 2.0

    monkeypatch.setattr(litellm, "cost_per_token", fake)
    return seen


def test_cost_fallback_uses_the_explicit_split_not_the_merged_cached_tokens(cost_kwargs):
    """cli-api の Anthropic proxy は cached_tokens に 読出し + 書込み の合算を入れる。明示の内訳があればそれで課金する
    (合算を読出しとして渡すと、書込み分が 0.1 倍でも数えられてコスト過小になる)。"""
    usage = {"input_tokens": 100_000, "output_tokens": 7, "cached_tokens": 90_000,
             "cache_read_tokens": 50_000, "cache_creation_tokens": 40_000}
    assert default_cost_fn("bedrock/x", None, usage) == 3.0
    assert (cost_kwargs["prompt_tokens"], cost_kwargs["completion_tokens"]) == (100_000, 7)
    assert (cost_kwargs["cache_read_input_tokens"], cost_kwargs["cache_creation_input_tokens"]) == (50_000, 40_000)


def test_cost_fallback_is_unchanged_for_usage_without_the_explicit_split(cost_kwargs):
    """明示の内訳が無い従来の usage (gateway の累積 dict / OpenAI 系) は、これまでと同じ引数で課金する。"""
    default_cost_fn("m", None, {"input_tokens": 1000, "output_tokens": 5, "cached_tokens": 800, "cache_creation_input_tokens": 200})
    assert (cost_kwargs["cache_read_input_tokens"], cost_kwargs["cache_creation_input_tokens"]) == (800, 200)
    default_cost_fn("m", None, {"input_tokens": 1000, "output_tokens": 5, "cached_tokens": 800})
    assert (cost_kwargs["cache_read_input_tokens"], cost_kwargs["cache_creation_input_tokens"]) == (800, 0)


def test_cost_fallback_explicit_zero_creation_wins_over_the_raw_field(cost_kwargs):
    default_cost_fn("m", None, {"input_tokens": 1000, "output_tokens": 5, "cached_tokens": 600, "cache_read_tokens": 600,
                                "cache_creation_tokens": 0, "cache_creation_input_tokens": 200})
    assert (cost_kwargs["cache_read_input_tokens"], cost_kwargs["cache_creation_input_tokens"]) == (600, 0)


@pytest.mark.parametrize("usage", [
    {"input_tokens": 1000, "output_tokens": 5, "cached_tokens": 800, "cache_creation_input_tokens": "n/a"},
    {"input_tokens": 1000, "output_tokens": 5, "cached_tokens": "n/a"},
    {"input_tokens": 1000, "output_tokens": 5, "cache_read_tokens": float("inf")},
])
def test_cost_fallback_stays_unknown_when_a_cache_value_is_unreadable(cost_kwargs, usage):
    """読めない値を 0 とみなして誤ったコストを出さない (従来どおりコスト不明 = None)。"""
    assert default_cost_fn("m", None, usage) is None and cost_kwargs == {}
