"""3.2 R32-072: Embedding の次元を設定で選ぶ (SDK)。

- 設定なし: 1536 とみなし、API に dimensions を渡さない (今までどおり・長さも確かめない)
- 設定あり: API に dimensions を渡し、返ってきた長さが違えば EmbeddingDimensionError (キャッシュに入れない)
- ada-002 は dimensions を受けないので渡さない (長さは確かめる)
"""
from types import SimpleNamespace

import pytest

from agenticstar_platform.memory.semantic import LLMProviderConfig, convert_embedder_to_mem0
from agenticstar_platform.rag import (
    DEFAULT_EMBEDDING_DIMENSIONS,
    EmbeddingConfig,
    EmbeddingDimensionError,
    EmbeddingError,
    EmbeddingGenerator,
    parse_embedding_dimensions,
)


class _Embeddings:
    def __init__(self, length):
        self.length, self.calls = length, []

    async def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(data=[SimpleNamespace(embedding=[0.1] * self.length) for _ in kwargs["input"]])


def _generator(dimensions, returned, model="openai/embed-v-4-0"):
    config = EmbeddingConfig.from_dict({"base_url": "https://example/models", "api_key": "k", "model": model,
                                        **({"dimensions": dimensions} if dimensions is not None else {})})
    gen = EmbeddingGenerator(config)
    gen.client = SimpleNamespace(embeddings=_Embeddings(returned))
    return gen


async def test_without_setting_nothing_changes():
    gen = _generator(None, 1536)
    assert gen.dimensions == DEFAULT_EMBEDDING_DIMENSIONS
    assert len(await gen.generate("a")) == 1536
    assert "dimensions" not in gen.client.embeddings.calls[0]


async def test_without_setting_other_lengths_are_not_checked():
    gen = _generator(None, 3072)  # 今までどおり (コレクション側で分かる)
    assert len(await gen.generate("a")) == 3072


async def test_setting_is_sent_and_checked():
    gen = _generator(1024, 1024)
    assert gen.dimensions == 1024
    assert len(await gen.generate("a")) == 1024
    assert len((await gen.batch_generate(["b", "c"]))[1]) == 1024
    assert all(call["dimensions"] == 1024 for call in gen.client.embeddings.calls)


@pytest.mark.parametrize("call", ["generate", "batch_generate"])
async def test_mismatch_is_a_clear_error_and_not_cached(call):
    gen = _generator(1024, 1536)
    with pytest.raises(EmbeddingDimensionError, match="configured 1024.*returned 1536"):
        await (gen.generate("a") if call == "generate" else gen.batch_generate(["a"]))
    assert len(gen.client.embeddings.calls) == 1  # 待って再試行しない
    assert gen._memory_cache == {}
    assert issubclass(EmbeddingDimensionError, EmbeddingError)


async def test_ada_002_is_not_sent_dimensions_but_still_checked():
    gen = _generator(1536, 1536, model="azure/text-embedding-ada-002")
    await gen.generate("a")
    assert "dimensions" not in gen.client.embeddings.calls[0]


@pytest.mark.parametrize("value,expected", [(None, None), (1024, 1024), ("3072", 3072)])
def test_parse_accepts_positive_integers(value, expected):
    assert parse_embedding_dimensions(value) == expected


@pytest.mark.parametrize("value", [0, -1, 1.5, "abc", True, [1024], {"secret": "s3cr3t"}])
def test_parse_rejects_others_at_startup(value):
    with pytest.raises(ValueError, match="positive integer") as e:
        parse_embedding_dimensions(value)
    assert "s3cr3t" not in str(e.value)  # 値は出さない
    with pytest.raises(ValueError):
        EmbeddingConfig.from_dict({"base_url": "https://x", "api_key": "k", "dimensions": value})
    with pytest.raises(ValueError):  # 直接作っても検査する
        EmbeddingConfig(base_url="https://x", api_key="k", dimensions=value)


def test_unset_dimensions_survive_cloning_and_existing_qdrant_callers_keep_working():
    """未設定は None のまま (dataclasses.replace / asdict → from_dict で「1536 を設定」に化けない)。
    既存の呼び手の QdrantConfig(vector_size=config.dimensions) は None を 1536 として受ける。"""
    import dataclasses

    from agenticstar_platform.rag import QdrantConfig

    config = EmbeddingConfig(base_url="https://x", api_key="k")
    assert config.dimensions is None
    assert dataclasses.replace(config, api_key="k2").dimensions is None
    assert EmbeddingConfig.from_dict(dataclasses.asdict(config)).dimensions is None
    assert QdrantConfig(url="http://q", collection_name="c", vector_size=config.dimensions).vector_size == 1536
    assert EmbeddingGenerator(config).dimensions == 1536
    set_config = dataclasses.replace(config, dimensions=1024)
    assert set_config.dimensions == 1024 and EmbeddingGenerator(set_config).dimensions == 1024


def test_mem0_embedder_gets_dimensions_only_when_set():
    with_dims = LLMProviderConfig.from_dict({"model": "openai/embed-v-4-0", "api_key": "k", "base_url": "https://x", "dimensions": 1024})
    without = LLMProviderConfig.from_dict({"model": "openai/embed-v-4-0", "api_key": "k", "base_url": "https://x"})
    assert convert_embedder_to_mem0(with_dims)["config"]["embedding_dims"] == 1024
    assert "embedding_dims" not in convert_embedder_to_mem0(without)["config"]


@pytest.mark.parametrize("value", ["²", "₃", "١٠٢٤"])
def test_parse_rejects_non_ascii_digits_without_echoing(value):
    with pytest.raises(ValueError, match="positive integer") as e:
        parse_embedding_dimensions(value)
    assert value not in str(e.value)
