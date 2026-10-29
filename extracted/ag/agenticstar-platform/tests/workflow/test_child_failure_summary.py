"""Agent の entrypoint が失敗したとき、子プロセスは原因の連鎖を本文なしで stderr に添える (3.1.3)。

`agent entrypoint failed: SecurityAPIError` だけでは、egress のサイドカーの 503 か Azure の障害かが分からなかった
(devdocs 3.2req reviews 06)。クラス名・SDK の error_code / HTTP status・通信先のホスト名だけを出す。
"""

import httpx

from agenticstar_platform.security.base import SecurityAPIError
from agenticstar_platform.workflow.child import _safe_failure_summary


def _raise_like_the_sdk():
    request = httpx.Request(
        "POST", "https://example.services.ai.azure.com/contentsafety/text:analyze?api-version=2024-09-01&key=SECRET")
    try:
        raise httpx.ProxyError("503 Service Unavailable body-secret", request=request)
    except httpx.RequestError as e:  # SDK の azure.py と同じく except の中で変換する (暗黙の __context__)
        raise SecurityAPIError(str(e), error_code="REQUEST_ERROR")


def test_sdk_error_shows_code_and_the_proxy_failure_with_its_host():
    try:
        _raise_like_the_sdk()
    except SecurityAPIError as e:
        text = _safe_failure_summary(e)

    assert text == "SecurityAPIError(error_code=REQUEST_ERROR) <- ProxyError(host=example.services.ai.azure.com)"
    assert "SECRET" not in text and "contentsafety" not in text and "body-secret" not in text


def test_plain_errors_show_only_class_names():
    try:
        try:
            raise ValueError("secret-value-123")
        except ValueError as inner:
            raise RuntimeError("boom secret-value-123") from inner
    except RuntimeError as e:
        text = _safe_failure_summary(e)

    assert text == "RuntimeError <- ValueError"


def test_status_code_and_suppressed_context_and_cycles():
    err = SecurityAPIError("Status 503: upstream", 503)
    assert _safe_failure_summary(err) == "SecurityAPIError(error_code=API_ERROR, status=503)"

    try:
        try:
            raise KeyError("x")
        except KeyError:
            raise ValueError("y") from None  # 連鎖を切った例外は先を見ない
    except ValueError as e:
        assert _safe_failure_summary(e) == "ValueError"

    a = RuntimeError("a")
    b = RuntimeError("b")
    a.__cause__ = b
    b.__cause__ = a  # 循環しても止まる
    assert _safe_failure_summary(a) == "RuntimeError <- RuntimeError"


def test_odd_error_code_values_are_not_written():
    err = SecurityAPIError("x", error_code="not an identifier; rm -rf")
    assert _safe_failure_summary(err) == "SecurityAPIError"


def test_a_broken_exception_class_does_not_stop_the_report():
    class Weird(Exception):
        def __getattr__(self, name):
            raise KeyError(name)

    assert _safe_failure_summary(Weird("secret")) == "Weird"

    class WeirdRequest(Exception):
        @property
        def request(self):
            raise KeyError("request")

    assert _safe_failure_summary(WeirdRequest("secret")) == "WeirdRequest"


def test_error_code_of_agent_exceptions_is_not_written():
    """Agent が作った例外の error_code は、文言と同じく何が入っているか分からないので出さない (SDK の例外だけ)。"""
    class AgentError(Exception):
        error_code = "REVIEW_SECRET"
        status_code = 418

    assert _safe_failure_summary(AgentError("x")) == "AgentError(status=418)"


def _proxy_error(host="example.services.ai.azure.com"):
    return httpx.ProxyError("503 body-secret", request=httpx.Request("POST", f"https://{host}/path?key=SECRET"))


def test_long_chain_stops_at_five_causes():
    errors = [RuntimeError(f"secret-{i}") for i in range(8)]
    for i in range(len(errors) - 1):
        errors[i].__cause__ = errors[i + 1]

    assert _safe_failure_summary(errors[0]) == " <- ".join(["RuntimeError"] * 5)


def test_cause_wins_over_context_and_context_is_followed_otherwise():
    err = RuntimeError("outer")
    err.__context__ = KeyError("context")
    err.__cause__ = ValueError("cause")
    err.__suppress_context__ = False  # __cause__ の代入で True になるので戻す (context を抑えずに cause が勝つか)
    assert _safe_failure_summary(err) == "RuntimeError <- ValueError"

    try:
        try:
            raise _proxy_error()
        except httpx.ProxyError:
            raise RuntimeError("while handling")  # noqa: B904 — 暗黙の __context__ をたどる
    except RuntimeError as e:
        assert _safe_failure_summary(e) == "RuntimeError <- ProxyError(host=example.services.ai.azure.com)"


def test_cycles_through_context_or_itself_stop():
    a = RuntimeError("a")
    a.__context__ = a
    assert _safe_failure_summary(a) == "RuntimeError"

    b = ValueError("b")
    c = KeyError("c")
    b.__context__ = c
    c.__context__ = b
    assert _safe_failure_summary(b) == "ValueError <- KeyError"


def test_a_broken_exception_in_the_middle_keeps_the_rest_of_the_chain():
    class Weird(Exception):
        def __getattr__(self, name):
            raise KeyError(name)

    middle = Weird("secret")
    middle.__cause__ = _proxy_error()
    top = RuntimeError("top")
    top.__cause__ = middle

    assert _safe_failure_summary(top) == "RuntimeError <- Weird <- ProxyError(host=example.services.ai.azure.com)"


def test_falls_back_to_the_class_name_when_the_chain_cannot_be_read():
    class Unreadable(Exception):
        status_code = 503  # 途中で打ち切るだけの実装なら Unreadable(status=503) になる

        def __getattribute__(self, name):
            if name == "__cause__":
                raise KeyError(name)
            return super().__getattribute__(name)

    top = Unreadable("secret")
    top.__cause__ = ValueError("cause")
    assert _safe_failure_summary(top) == "Unreadable"


def test_bool_status_and_empty_or_non_str_host_are_not_written():
    class BoolStatus(Exception):
        status_code = True

    class EmptyHost(Exception):
        request = type("Req", (), {"url": type("Url", (), {"host": ""})()})()

    class BytesHost(Exception):
        request = type("Req", (), {"url": type("Url", (), {"host": b"example.com"})()})()

    assert _safe_failure_summary(BoolStatus("x")) == "BoolStatus"
    assert _safe_failure_summary(EmptyHost("x")) == "EmptyHost"
    assert _safe_failure_summary(BytesHost("x")) == "BytesHost"


def test_only_sdk_shaped_error_codes_are_written():
    """3.2.1: 要約は終了時の報告にも載る。SDK の例外クラスを Agent が自分の値で作った error_code（秘密が入りうる）は、
    SDK の語の形（大文字の snake_case、64 字まで）でなければ出さない。"""
    for code in ("sk_live_secret123", "request_error", "Bearer abc", "A" * 65, "1ABC", ""):
        assert _safe_failure_summary(SecurityAPIError("x", error_code=code)) == "SecurityAPIError", code
    for code in ("REQUEST_ERROR", "RATE_LIMITED", "A" * 64):
        assert _safe_failure_summary(SecurityAPIError("x", error_code=code)) == f"SecurityAPIError(error_code={code})"
