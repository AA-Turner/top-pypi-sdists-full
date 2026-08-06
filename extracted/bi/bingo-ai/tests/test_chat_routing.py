"""일반 대화 vs 펜테스트 의도 라우팅 회귀 테스트.

CLI REPL은 타겟이 설정돼 있어도 일반 질문은 대화로, 명시적 공격/스캔
지시는 AgentLoop(펜테스트)로 라우팅해야 한다. 기법 이름(sqli/xss)이
설명 질문에 등장하는 경우도 대화로 취급한다.
"""
from __future__ import annotations

import bingo.cli as cli
from bingo.models.base import StreamChunk
from rich.console import Console


def test_general_conversation_is_not_pentest():
    for text in [
        "안녕 뭐해?",
        "SQLi가 뭐야?",
        "XSS 설명해줘",
        "sql injection이랑 xss 차이가 뭐야?",
        "방금 뭐 찾았어?",
        "파이썬으로 퀵소트 짜줘",
        "what is an SSRF vulnerability?",
    ]:
        assert cli._looks_like_pentest(text) is False, text


def test_explicit_attack_is_pentest():
    for text in [
        "이 사이트 스캔해줘",
        "취약점 찾아봐",
        "scan this target",
        "exploit the login form",
        "SQL injection 공격 시도해",
        "sqlmap 돌려서 덤프해",
        "포트 스캔 진행해",
    ]:
        assert cli._looks_like_pentest(text) is True, text


def test_chat_reply_streams_and_keeps_history(monkeypatch):
    class FakeModel:
        def __init__(self):
            self.config = type("C", (), {"get_system_prompt": lambda s: "sys"})()

        def chat_stream(self, messages, **kw):
            assert messages[0]["role"] == "system"
            assert messages[-1]["content"] == "안녕 너 뭐야?"
            for t in ["안녕", "하세요"]:
                yield StreamChunk(text=t)
            yield StreamChunk(text="", done=True)

    class FakeCfg:
        lang = "ko"

        def get_active_model_config(self):
            return object()

    import bingo.models.registry as reg
    monkeypatch.setattr(reg.ModelRegistry, "build", staticmethod(lambda mc: FakeModel()))

    history: list[dict] = []
    reply = cli._chat_reply(FakeCfg(), Console(), history, "안녕 너 뭐야?")

    assert reply == "안녕하세요"
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "안녕 너 뭐야?"}
    assert history[1]["role"] == "assistant"


def test_chat_reply_without_model_returns_empty():
    class NoModelCfg:
        lang = "en"

        def get_active_model_config(self):
            return None

    history: list[dict] = []
    reply = cli._chat_reply(NoModelCfg(), Console(), history, "hi")
    assert reply == ""
    assert history == []
