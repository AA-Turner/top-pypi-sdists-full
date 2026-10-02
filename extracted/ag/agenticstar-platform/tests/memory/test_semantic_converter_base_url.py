"""OpenAI互換LLM/embedderのbase_url保持契約（molt#1626、offline）

公開済み0.5.36ではembedder変換だけが明示base_urlをMem0の
openai_base_urlへ写像し、LLM変換は値を捨てていた。Mem0のfallbackにより
memory addが公式api.openai.comへ向かい得るため、private gateway利用時の
credential誤送信境界となる。ここではLLM/embedderのendpoint parityと
「private URL指定時はそのURLのみが接続先になる」契約をofflineで固定する。
"""

from unittest.mock import MagicMock, patch

from agenticstar_platform.memory.semantic import (
    LLMProviderConfig,
    SemanticMemoryClient,
    convert_embedder_to_mem0,
    convert_llm_to_mem0,
)

PRIVATE_BASE_URL = "https://gateway.example/v1"
OFFICIAL_OPENAI_BASE_URL = "https://api.openai.com/v1"


def _openai_compat_config(base_url=PRIVATE_BASE_URL) -> LLMProviderConfig:
    return LLMProviderConfig(
        model="openai/custom-chat",
        api_key="sk-test-not-real",
        base_url=base_url,
    )


def _clear_endpoint_env(monkeypatch) -> None:
    """接続先決定に影響する環境変数を排除（offline固定の前提）"""
    for name in (
        "OPENROUTER_API_KEY",
        "OPENAI_BASE_URL",
        "OPENAI_API_BASE",
        "OPENAI_API_KEY",
    ):
        monkeypatch.delenv(name, raising=False)


class TestConverterBaseUrlContract:
    """converter出力レベルの契約（AC1/AC2/AC4）"""

    def test_llm_preserves_explicit_base_url(self):
        result = convert_llm_to_mem0(_openai_compat_config())
        assert result["provider"] == "openai"
        assert result["config"]["openai_base_url"] == PRIVATE_BASE_URL

    def test_llm_and_embedder_endpoint_parity(self):
        config = _openai_compat_config()
        llm = convert_llm_to_mem0(config)
        embedder = convert_embedder_to_mem0(config)
        assert (
            llm["config"]["openai_base_url"]
            == embedder["config"]["openai_base_url"]
            == PRIVATE_BASE_URL
        )

    def test_no_base_url_keeps_official_openai_contract(self):
        config = _openai_compat_config(base_url=None)
        llm = convert_llm_to_mem0(config)
        embedder = convert_embedder_to_mem0(config)
        assert "openai_base_url" not in llm["config"]
        assert "openai_base_url" not in embedder["config"]
        assert llm["config"] == {"model": "custom-chat", "api_key": "sk-test-not-real"}


class TestSemanticMemoryClientDelegation:
    """SemanticMemoryClient実使用経路（委譲）がmodule関数と一致すること（AC5）"""

    def test_instance_converters_match_module_functions(self):
        client = object.__new__(SemanticMemoryClient)
        for config in (_openai_compat_config(), _openai_compat_config(base_url=None)):
            assert client._convert_llm_to_mem0(config) == convert_llm_to_mem0(config)
            assert client._convert_embedder_to_mem0(config) == convert_embedder_to_mem0(
                config
            )


class TestEffectiveEndpoint:
    """Mem0実配線（LlmFactory/EmbedderFactory）での接続先固定（AC2/AC3）

    OpenAI clientのconstructorをpatchし、private URL指定時は
    そのURLだけがbase_urlとして渡され、api.openai.comへの接続構成が
    0件であることを固定する。HTTP requestは一切発生しない。
    """

    def test_private_url_is_sole_llm_destination(self, monkeypatch):
        _clear_endpoint_env(monkeypatch)
        converted = convert_llm_to_mem0(_openai_compat_config())

        from mem0.utils.factory import LlmFactory

        with patch("mem0.llms.openai.OpenAI", return_value=MagicMock()) as ctor:
            LlmFactory.create(converted["provider"], dict(converted["config"]))

        assert ctor.call_count == 1
        base_url = ctor.call_args.kwargs["base_url"]
        assert base_url == PRIVATE_BASE_URL
        assert "api.openai.com" not in base_url

    def test_private_url_is_sole_embedder_destination(self, monkeypatch):
        _clear_endpoint_env(monkeypatch)
        converted = convert_embedder_to_mem0(_openai_compat_config())

        from mem0.utils.factory import EmbedderFactory

        with patch("mem0.embeddings.openai.OpenAI", return_value=MagicMock()) as ctor:
            EmbedderFactory.create(
                converted["provider"], dict(converted["config"]), None
            )

        assert ctor.call_count == 1
        base_url = ctor.call_args.kwargs["base_url"]
        assert base_url == PRIVATE_BASE_URL
        assert "api.openai.com" not in base_url

    def test_explicit_private_url_wins_over_env_base_url(self, monkeypatch):
        """OPENAI_BASE_URL が公式 URL を指していても明示 base_url が勝つこと"""
        _clear_endpoint_env(monkeypatch)
        monkeypatch.setenv("OPENAI_BASE_URL", OFFICIAL_OPENAI_BASE_URL)
        converted = convert_llm_to_mem0(_openai_compat_config())

        from mem0.utils.factory import LlmFactory

        with patch("mem0.llms.openai.OpenAI", return_value=MagicMock()) as ctor:
            LlmFactory.create(converted["provider"], dict(converted["config"]))

        assert ctor.call_args.kwargs["base_url"] == PRIVATE_BASE_URL

    def test_no_base_url_falls_back_to_official_openai(self, monkeypatch):
        _clear_endpoint_env(monkeypatch)
        converted = convert_llm_to_mem0(_openai_compat_config(base_url=None))

        from mem0.utils.factory import LlmFactory

        with patch("mem0.llms.openai.OpenAI", return_value=MagicMock()) as ctor:
            LlmFactory.create(converted["provider"], dict(converted["config"]))

        assert ctor.call_count == 1
        assert ctor.call_args.kwargs["base_url"] == OFFICIAL_OPENAI_BASE_URL
