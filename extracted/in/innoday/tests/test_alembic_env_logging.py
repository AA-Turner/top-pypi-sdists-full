"""`alembic/env.py` must not switch off the caller's loggers.

`env.py` runs in-process whenever anything calls `alembic.command.*` -- the
test suite's `pg_engine` fixture does, and so would any future startup or
management path. `logging.config.fileConfig` defaults to
`disable_existing_loggers=True`, which disables every logger created before it
ran and reports nothing. The symptom is a `caplog` assertion, or an operator's
log line, that simply stops appearing.

Checked structurally rather than by running a migration: the behavioural version
needs a live database, and the thing worth pinning is the argument, which is
exactly what a later edit would drop.
"""

import ast
from pathlib import Path

ENV_PY = Path(__file__).resolve().parent.parent / "alembic" / "env.py"


def _file_config_calls(tree):
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and getattr(node.func, "id", getattr(node.func, "attr", None)) == "fileConfig"
    ]


def test_file_config_does_not_disable_existing_loggers():
    calls = _file_config_calls(ast.parse(ENV_PY.read_text()))
    assert calls, "expected env.py to configure logging via fileConfig"

    for call in calls:
        kwargs = {kw.arg: kw.value for kw in call.keywords}
        disable = kwargs.get("disable_existing_loggers")
        assert disable is not None, (
            f"fileConfig at env.py:{call.lineno} omits disable_existing_loggers, "
            "which defaults to True and silences every logger the caller already "
            "created -- alembic is run in-process by the test suite"
        )
        assert isinstance(disable, ast.Constant) and disable.value is False, (
            f"fileConfig at env.py:{call.lineno} must pass "
            "disable_existing_loggers=False"
        )
