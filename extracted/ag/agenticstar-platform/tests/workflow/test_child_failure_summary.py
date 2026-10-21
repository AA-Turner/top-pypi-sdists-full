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
