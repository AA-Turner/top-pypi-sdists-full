"""Prompt Shield が documents (外部コンテンツ) を末尾まで検査する。

旧実装は documents を合計 9,500 bytes に頭切りして最初の呼び出しでだけ送り、警告も出さなかった。外部コンテンツの
9.5KB より後ろ (日本語なら約 3,100 文字より後ろ) に置いた間接 injection は検査されなかった。documents も userPrompt と
同じく重なり付きウィンドウに分け、1 呼び出しあたり合計 9,500 bytes 以下に詰めて送り、結果を OR する。

Azure の HTTP 応答だけを差し替える。
"""

import httpx
import pytest

from agenticstar_platform.security import AzureSecurityClient, AzureSecurityConfig
from agenticstar_platform.security import azure as az

MARK = "INJECT-ME"


class _FakeHttp:
    def __init__(self):
        self.bodies = []

    async def post(self, endpoint, headers=None, json=None):
        self.bodies.append(json)
        docs = json.get("documents") or []
        return httpx.Response(200, json={
            "userPromptAnalysis": {"attackDetected": MARK in json["userPrompt"]},
            "documentsAnalysis": [{"attackDetected": MARK in d} for d in docs],
        })


@pytest.fixture
def shield(monkeypatch):
    client = AzureSecurityClient(AzureSecurityConfig(
        content_safety_endpoint="https://cs.invalid", content_safety_api_key="k", prompt_shield_enabled=True))
    http = _FakeHttp()
    monkeypatch.setattr(client, "_get_http_client", lambda: http)
    return client, http


def _sent_documents(http):
    return [d for body in http.bodies for d in (body.get("documents") or [])]


async def test_injection_after_the_first_9500_bytes_is_detected(shield):
    client, http = shield
    doc = "これは普通の本文です。" * 1000 + MARK  # 約 33KB。注入は末尾

    result = await client.check_prompt_shield(user_prompt="この文書を要約して", documents=[doc])

    assert result.attack_detected and result.documents_attack and not result.user_prompt_attack


async def test_every_part_of_the_documents_is_sent_within_the_per_call_limit(shield):
    client, http = shield
    doc = "".join(f"{i:06d}" for i in range(6000))  # 36,000 bytes の ASCII

    await client.check_prompt_shield(user_prompt="q", documents=[doc])

    for body in http.bodies:
        assert sum(len(d.encode("utf-8")) for d in body.get("documents") or []) <= az._AZURE_CS_MAX_BYTES
        assert body["userPrompt"] == "q"
    sent = _sent_documents(http)
    assert all(f"{i:06d}" in "".join(sent) for i in range(6000))
    assert sent[0].startswith("000000") and sent[-1].endswith(f"{5999:06d}")


async def test_multibyte_documents_are_split_on_character_boundaries(shield):
    client, http = shield
    doc = "漢字🙂" * 6000  # 3 + 4 bytes を交互に

    await client.check_prompt_shield(user_prompt="q", documents=[doc])

    sent = _sent_documents(http)
    assert len(sent) > 1
    assert all(w in doc for w in sent)  # 文字の途中で切れた窓は元の文書の部分文字列にならない


async def test_a_short_document_is_checked_in_one_call_as_before(shield):
    client, http = shield

    result = await client.check_prompt_shield(user_prompt="q", documents=["short " + MARK])

    assert result.attack_detected and result.documents_attack
    assert http.bodies == [{"userPrompt": "q", "documents": ["short " + MARK]}]


async def test_long_prompt_and_long_document_are_both_covered(shield):
    client, http = shield
    prompt = "p" * 20000 + MARK
    doc = "d" * 20000

    result = await client.check_prompt_shield(user_prompt=prompt, documents=[doc])

    assert result.user_prompt_attack and not result.documents_attack
    assert "".join(_sent_documents(http)).count("d") >= 20000


async def test_each_call_carries_at_most_five_documents(shield):
    client, http = shield
    docs = ["x" * 9000] + ["d"] * 101

    await client.check_prompt_shield(user_prompt="q", documents=docs)

    assert all(len(body.get("documents") or []) <= az._AZURE_CS_MAX_DOCS_PER_REQUEST for body in http.bodies)
    assert len(_sent_documents(http)) == len(docs)
