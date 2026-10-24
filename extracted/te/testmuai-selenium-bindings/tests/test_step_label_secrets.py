"""Step labels ship on lambda-testCase-start/end: a secret value must never reach them."""
from testmu_selenium._step import _resolve_label
from testmu_selenium._vars import set_var, var


def test_label_keeps_secret_token_as_authored(monkeypatch):
    monkeypatch.setenv("login_pw", "hunter2-real")
    set_var("user", "parth")
    out = _resolve_label("Type {{secrets.org.login_pw}} for {{user}}")
    assert out == "Type {{secrets.org.login_pw}} for parth"


def test_label_redacts_secret_copied_into_a_plain_variable(monkeypatch):
    monkeypatch.setenv("login_pw", "hunter2-real")
    set_var("pwd", var("{{secrets.org.login_pw}}"))
    out = _resolve_label("Type {{pwd}} in password")
    assert out == "Type ***** in password"
