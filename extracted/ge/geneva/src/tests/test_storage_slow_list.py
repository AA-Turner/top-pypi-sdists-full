# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Tests for ``geneva.utils.storage.timed_list`` slow-list warnings."""

import logging
import time
from collections.abc import Callable, Iterator
from typing import Any

import pytest

from geneva.utils import storage as storage_mod
from geneva.utils.storage import timed_list


class _FakeSession:
    """Minimal session stub exposing a ``list(scope)`` iterator."""

    def __init__(
        self,
        items: list[str],
        delay_s: float = 0.0,
        on_list: Callable[[str | None], None] | None = None,
    ) -> None:
        self._items = items
        self._delay_s = delay_s
        self._on_list = on_list
        self.last_scope: str | None = None

    def list(self, scope: str | None) -> Iterator[str]:
        self.last_scope = scope
        if self._on_list is not None:
            self._on_list(scope)
        if self._delay_s:
            time.sleep(self._delay_s)
        return iter(self._items)


@pytest.fixture(autouse=True)
def _reset_rate_limit() -> Iterator[None]:
    """Clear the WARN rate-limit dict between tests."""
    storage_mod._slow_list_warn_last.clear()
    yield
    storage_mod._slow_list_warn_last.clear()


def _read_records(
    caplog: pytest.LogCaptureFixture,
    level: int,
) -> list[logging.LogRecord]:
    return [
        r for r in caplog.records if r.levelno == level and "slow list" in r.message
    ]


def test_below_threshold_no_log(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "100000")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "100000")
    session = _FakeSession(["a.lance", "b.lance"])
    with caplog.at_level(logging.INFO, logger="geneva.utils.storage"):
        out = timed_list(session, "scope", op="list_keys", layout="flat", root="s3://x")
    assert out == ["a.lance", "b.lance"]
    assert _read_records(caplog, logging.INFO) == []
    assert _read_records(caplog, logging.WARNING) == []


def test_above_info_emits_info(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "10")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "100000")
    session = _FakeSession(["a", "b", "c"], delay_s=0.05)
    with caplog.at_level(logging.INFO, logger="geneva.utils.storage"):
        out = timed_list(
            session, "myscope", op="list_keys", layout="flat", root="az://acct/path"
        )
    assert out == ["a", "b", "c"]
    info = _read_records(caplog, logging.INFO)
    assert len(info) == 1
    msg = info[0].getMessage()
    assert "op=list_keys" in msg
    assert "layout=flat" in msg
    assert "'myscope'" in msg
    assert "items=3" in msg
    assert "store=az://acct/path" in msg
    assert _read_records(caplog, logging.WARNING) == []


def test_above_warn_emits_warning(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "5")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "10")
    session = _FakeSession(["x"], delay_s=0.05)
    with caplog.at_level(logging.INFO, logger="geneva.utils.storage"):
        timed_list(session, "s", op="list_keys", layout="hierarchical", root="s3://x")
    warns = _read_records(caplog, logging.WARNING)
    assert len(warns) == 1
    assert "layout=hierarchical" in warns[0].getMessage()
    # INFO is not also emitted when WARN fires.
    assert _read_records(caplog, logging.INFO) == []


def test_warn_rate_limited_within_window(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "5")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "10")
    session = _FakeSession(["x"], delay_s=0.05)
    with caplog.at_level(logging.INFO, logger="geneva.utils.storage"):
        timed_list(session, "s", op="list_keys", layout="flat", root="s3://x")
        timed_list(session, "s", op="list_keys", layout="flat", root="s3://x")
    # First call WARNs; second is suppressed by the rate limit and is slow
    # enough to fall back to INFO.
    assert len(_read_records(caplog, logging.WARNING)) == 1
    assert len(_read_records(caplog, logging.INFO)) == 1


def test_warn_not_rate_limited_for_distinct_scope(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "5")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "10")
    session = _FakeSession(["x"], delay_s=0.05)
    with caplog.at_level(logging.INFO, logger="geneva.utils.storage"):
        timed_list(session, "scope-a", op="list_keys", layout="flat", root="s3://x")
        timed_list(session, "scope-b", op="list_keys", layout="flat", root="s3://x")
    assert len(_read_records(caplog, logging.WARNING)) == 2


def test_info_threshold_zero_disables_info(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "0")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "100000")
    session = _FakeSession(["x"], delay_s=0.05)
    with caplog.at_level(logging.INFO, logger="geneva.utils.storage"):
        timed_list(session, "s", op="list_keys", layout="flat", root="s3://x")
    assert _read_records(caplog, logging.INFO) == []
    assert _read_records(caplog, logging.WARNING) == []


def test_warn_threshold_zero_disables_warn(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "5")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "0")
    session = _FakeSession(["x"], delay_s=0.05)
    with caplog.at_level(logging.INFO, logger="geneva.utils.storage"):
        timed_list(session, "s", op="list_keys", layout="flat", root="s3://x")
    # WARN disabled, INFO still fires.
    assert _read_records(caplog, logging.WARNING) == []
    assert len(_read_records(caplog, logging.INFO)) == 1


def test_drains_iterator_returns_list(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Caller should get a fully materialized list, not a lazy iterator."""
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "100000")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "100000")
    consumed: list[Any] = []

    def _record(scope: str | None) -> None:
        consumed.append(scope)

    session = _FakeSession(["a", "b"], on_list=_record)
    out = timed_list(session, "s", op="list_keys", layout="flat", root="s3://x")
    assert isinstance(out, list)
    assert out == ["a", "b"]
    # session.list was invoked exactly once during the call (not deferred).
    assert consumed == ["s"]


def test_scope_none_is_safe(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "10")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "100000")
    session = _FakeSession(["a"], delay_s=0.05)
    with caplog.at_level(logging.INFO, logger="geneva.utils.storage"):
        timed_list(session, None, op="list_keys", layout="flat", root="s3://x")
    info = _read_records(caplog, logging.INFO)
    assert len(info) == 1
    assert "scope=''" in info[0].getMessage()


def test_malformed_env_falls_back_to_default(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A non-numeric env var must not raise out of ``timed_list``.

    ``_check_coexistence_with_flat`` wraps ``timed_list`` in ``except
    Exception`` and would silently degrade correctness if a bad env value
    leaked an exception through.
    """
    monkeypatch.setenv("GENEVA_SLOW_LIST_INFO_MS", "disabled")
    monkeypatch.setenv("GENEVA_SLOW_LIST_WARN_MS", "off")
    session = _FakeSession(["a", "b"])
    with caplog.at_level(logging.WARNING, logger="geneva.utils.storage"):
        out = timed_list(session, "s", op="list_keys", layout="flat", root="s3://x")
    assert out == ["a", "b"]
    # Both thresholds get a one-line warning; the slow-list path itself does
    # not (the fake session is fast).
    fallback_msgs = [
        r.getMessage()
        for r in caplog.records
        if r.levelno == logging.WARNING and "ignoring non-numeric" in r.getMessage()
    ]
    assert any("GENEVA_SLOW_LIST_INFO_MS" in m for m in fallback_msgs)
    assert any("GENEVA_SLOW_LIST_WARN_MS" in m for m in fallback_msgs)
