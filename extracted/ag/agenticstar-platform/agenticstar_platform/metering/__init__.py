"""
agenticstar_platform.metering — LLM 利用量・コスト計測モジュール。

LLM 応答/トークンからコストを算出し、利用量台帳 (llm_usage_ledger) へ記録、
日次集計 (llm_usage_daily) とコスト可視化クエリを提供する純インフラ。

- コスト算出はプラガブル (既定: litellm があれば使用、無ければ tokens のみ)。
- DB は `execute_query(query, params) -> {success,data,error}` を持つもの (SDK の DataAccess 等) を渡す。

公開 API:
    UsageMeter         計測・記録・集計のエントリポイント
    default_cost_fn    既定コスト算出関数 (litellm ベース)
    extract_usage      usage オブジェクト/dict → {input,output,total} tokens
    round_cost_usd     cost(USD) を numeric へ綺麗に格納する Decimal 整形（worker/gateway 共有）
"""
from .meter import UsageMeter, default_cost_fn, extract_usage, round_cost_usd

__all__ = ["UsageMeter", "default_cost_fn", "extract_usage", "round_cost_usd"]
