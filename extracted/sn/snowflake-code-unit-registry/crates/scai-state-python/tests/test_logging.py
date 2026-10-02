"""Logging tests — validates ScaiLogger via the native layer's init_in_dir."""

from __future__ import annotations

from pathlib import Path

from snowflake_code_unit_registry import ScaiLogger as _PublicScaiLogger
from snowflake_code_unit_registry._native import ScaiLogger


def test_logger_writes_to_file(tmp_path: Path):
    log_dir = str(tmp_path / "logs")
    logger = ScaiLogger.init_in_dir("TEST_PY", log_dir)

    logger.info("hello from python")
    logger.warn("a warning")
    logger.error("an error")

    content = Path(logger.log_path()).read_text()
    assert "[INF] ps=TEST_PY: hello from python" in content
    assert "[WRN] ps=TEST_PY: a warning" in content
    assert "[ERR] ps=TEST_PY: an error" in content


def test_logger_with_project(tmp_path: Path):
    log_dir = str(tmp_path / "logs")
    logger = ScaiLogger.init_in_dir("TEST_PY", log_dir, project_id="my-proj")

    logger.info("with project")

    content = Path(logger.log_path()).read_text()
    assert "[INF] ps=TEST_PY pr=my-proj: with project" in content


def test_log_with_structured_context(tmp_path: Path):
    log_dir = str(tmp_path / "logs")
    logger = ScaiLogger.init_in_dir("TEST_PY", log_dir)

    logger.log("info", "structured entry", {"key": "value", "n": 42})

    content = Path(logger.log_path()).read_text()
    assert "[INF] ps=TEST_PY: structured entry |" in content
    assert '"key"' in content
    assert '"value"' in content


def test_log_path_uses_compact_date(tmp_path: Path):
    from datetime import datetime, timezone

    log_dir = str(tmp_path / "logs")
    logger = ScaiLogger.init_in_dir("TEST_PY", log_dir)

    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    assert f"scai{today}.log" in logger.log_path()


# ──────────────────────────────────────────────────────────────────────────
# Public-wrapper ergonomics: warning alias, context kwarg, error(exception=)
# ──────────────────────────────────────────────────────────────────────────


def _public_logger(tmp_path: Path) -> _PublicScaiLogger:
    """Construct the public ScaiLogger backed by a tmp-dir native logger."""
    log_dir = str(tmp_path / "logs")
    return _PublicScaiLogger(ScaiLogger.init_in_dir("TEST_PY", log_dir))


def test_public_warning_aliases_warn(tmp_path: Path):
    logger = _public_logger(tmp_path)

    logger.warning("a warning via alias")

    content = Path(logger.log_path()).read_text()
    assert "[WRN] ps=TEST_PY: a warning via alias" in content


def test_public_info_with_context_kwarg(tmp_path: Path):
    logger = _public_logger(tmp_path)

    logger.info("info with ctx", context={"key": "value", "n": 42})

    content = Path(logger.log_path()).read_text()
    assert "[INF] ps=TEST_PY: info with ctx |" in content
    assert '"key"' in content
    assert '"value"' in content


def test_public_warning_with_context_kwarg_routes_to_warn(tmp_path: Path):
    logger = _public_logger(tmp_path)

    logger.warning("warn with ctx", context={"k": "v"})

    content = Path(logger.log_path()).read_text()
    assert "[WRN] ps=TEST_PY: warn with ctx |" in content
    assert '"k"' in content
    assert '"v"' in content


def test_public_debug_with_context_kwarg_routes_to_debug_level(tmp_path: Path):
    """When context is supplied, the level method should route through log()."""
    import os

    log_dir = str(tmp_path / "logs")
    # Need DEBUG min-level so the entry isn't filtered out.
    os.environ["SCAI_LOG_LEVEL"] = "debug"
    try:
        logger = _PublicScaiLogger(ScaiLogger.init_in_dir("TEST_PY", log_dir))
        logger.debug("debug with ctx", context={"x": 1})
        content = Path(logger.log_path()).read_text()
        assert "[DBG] ps=TEST_PY: debug with ctx |" in content
        assert '"x"' in content
    finally:
        del os.environ["SCAI_LOG_LEVEL"]


def test_public_error_with_exception_serialises_type_message_stacktrace(
    tmp_path: Path,
):
    logger = _public_logger(tmp_path)

    try:
        raise ValueError("boom")
    except ValueError as ex:
        logger.error("something failed", exception=ex)

    content = Path(logger.log_path()).read_text()
    assert "[ERR] ps=TEST_PY: something failed |" in content
    assert '"type"' in content
    assert "ValueError" in content
    assert '"message"' in content
    assert "boom" in content
    assert '"stackTrace"' in content


def test_public_error_exception_plus_context_caller_overrides(tmp_path: Path):
    import json

    logger = _public_logger(tmp_path)

    try:
        raise ValueError("original-message")
    except ValueError as ex:
        logger.error(
            "failed",
            exception=ex,
            context={"message": "caller-override", "userId": "u-123"},
        )

    content = Path(logger.log_path()).read_text()
    line = next(line for line in content.splitlines() if "failed |" in line)
    ctx = json.loads(line.split(" | ", 1)[1])

    # Caller-supplied "message" wins over str(exception).
    assert ctx["message"] == "caller-override"
    assert ctx["userId"] == "u-123"
    # Exception type still surfaces (caller didn't override "type").
    assert ctx["type"] == "ValueError"
    assert "stackTrace" in ctx


def test_public_error_no_exception_no_context_uses_simple_path(tmp_path: Path):
    logger = _public_logger(tmp_path)

    logger.error("plain error")

    content = Path(logger.log_path()).read_text()
    # No structured context separator after the message.
    assert "[ERR] ps=TEST_PY: plain error" in content
    # Confirm no JSON context attached.
    line = next(
        line for line in content.splitlines() if "plain error" in line
    )
    assert " | {" not in line


def test_public_error_context_only_uses_log_path(tmp_path: Path):
    logger = _public_logger(tmp_path)

    logger.error("ctx-only", context={"k": "v"})

    content = Path(logger.log_path()).read_text()
    assert "[ERR] ps=TEST_PY: ctx-only |" in content
    assert '"k"' in content
    assert '"v"' in content
