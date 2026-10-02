"""決定論的 offline embedding（local integration lab 専用、molt#1610）。

cloud endpoint・API key・network を一切使わず、feature hashing（bag-of-words の
トークンを SHA-256 で次元へ写像し符号付きで加算 → L2 正規化）で埋め込みを生成する。

性質:
- 決定論: 同じ input と EMBEDDING_VERSION は常に同じベクトルを返す
  （tests/lab/test_lab_contract.py が既知ベクトル regression で固定）
- 意味: トークンの重なりがそのまま cosine 類似度に反映されるため、
  語彙が重なる synthetic 文書の retrieval デモが成立する
- 非 fallback: 外部 API への fallback 経路を持たない（本番 EmbeddingGenerator の
  代替品ではなく、lab の journey を credential 不要にするための専用実装）

QdrantManager が要求する duck-type 契約（dimensions / model_name /
generate / batch_generate）を満たす。英語トークン（[a-z0-9']+）前提。
"""

from __future__ import annotations

import hashlib
import math
import re
from typing import List

_TOKEN_RE = re.compile(r"[a-z0-9']+")


class OfflineEmbeddingGenerator:
    """lab 専用の決定論的 offline embedding。

    Args:
        dimensions: ベクトル次元数（QdrantConfig.vector_size と一致させる）
        version: アルゴリズム/語彙写像のバージョン文字列。ハッシュの seed に
            含まれるため、変えると全ベクトルが変わる（＝collection の再構築が必要）
    """

    def __init__(self, dimensions: int, version: str):
        self.dimensions = dimensions
        self.model_name = version  # QdrantManager が model_version として記録する

    def _embed(self, text: str) -> List[float]:
        vector = [0.0] * self.dimensions
        for token in _TOKEN_RE.findall(text.lower()):
            digest = hashlib.sha256(
                f"{self.model_name}:{token}".encode("utf-8")
            ).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(v * v for v in vector))
        if norm == 0.0:
            # トークンが 1 つもない入力の決定論的 fallback（単位ベクトル）
            vector[0] = 1.0
            return vector
        return [v / norm for v in vector]

    async def generate(self, text: str) -> List[float]:
        """単一テキストの embedding を生成（決定論・network なし）。"""
        return self._embed(text)

    async def batch_generate(self, texts: List[str]) -> List[List[float]]:
        """複数テキストの embedding を生成（決定論・network なし）。"""
        return [self._embed(t) for t in texts]
