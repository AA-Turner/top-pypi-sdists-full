# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import random
import time

import pytest

from geneva.utils import deep_merge, retry_lance
from geneva.utils.commit_conflict import is_retryable_commit_conflict
from geneva.utils.ray import size_to_bytes


def test_preserves_function_metadata() -> None:
    """Wrapper should preserve __name__ and __doc__ via functools.wraps."""

    def fn(a, b) -> int:
        """original doc"""
        return a + b

    wrapped = retry_lance(fn)
    assert wrapped.__name__ == fn.__name__
    assert wrapped.__doc__ == fn.__doc__


def test_success_no_retries(monkeypatch) -> None:
    """If the function succeeds immediately, no sleep or warning should occur."""
    called = []

    def fast_fn(x) -> list:
        called.append(x)
        return x * 2

    # spy on sleep and uniform
    monkeypatch.setattr(
        time,
        "sleep",
        lambda s: (_ for _ in ()).throw(AssertionError("sleep should not be called")),
    )
    monkeypatch.setattr(random, "uniform", lambda a, b: b)

    wrapped = retry_lance(fast_fn)
    result = wrapped(10)
    assert result == 20
    assert called == [10]


def test_retries_and_backoff(monkeypatch, caplog) -> None:
    """Function fails twice then succeeds on 3rd attempt with correct sleep calls and
    logs."""
    attempts = {"count": 0}
    sleep_calls = []

    def flaky(x) -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ValueError(f"fail #{attempts['count']}")
        return "ok"

    # force deterministic jitter = full delay
    monkeypatch.setattr(random, "uniform", lambda a, b: b)
    # record sleep calls
    monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

    # capture warnings
    caplog.set_level(logging.WARNING)

    wrapped = retry_lance(flaky)

    res = wrapped(0)
    assert res == "ok"

    assert sleep_calls == [1.5, 2.0]

    # check that two warning logs were emitted
    warning_texts = [
        r.getMessage() for r in caplog.records if r.levelno == logging.WARNING
    ]
    assert any("as it raised ValueError: fail #1" in text for text in warning_texts)
    assert any("as it raised ValueError: fail #2" in text for text in warning_texts)


def test_max_attempts_exhaustion(monkeypatch, caplog) -> None:
    """After max_attempts is reached, the exception is re-raised and an error is
    logged."""

    def always_fail() -> None:
        raise ValueError("no hope")

    sleep_calls = []
    monkeypatch.setattr(random, "uniform", lambda a, b: 0)  # jitter=0 for clarity
    monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

    caplog.set_level(logging.ERROR)
    wrapped = retry_lance(always_fail)

    with pytest.raises(ValueError, match="no hope"):
        wrapped()

    # should have slept once (only one retry before giving up)
    assert sleep_calls == [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]

    # check error log
    errors = [r.getMessage() for r in caplog.records if r.levelno == logging.ERROR]
    assert any(
        "always_fail' failed after 7 attempts; giving up." in msg for msg in errors
    )


def test_non_retryable_exception(monkeypatch) -> None:
    """Exceptions not in the tuple should propagate immediately (no retry)."""
    sleep_calls = []
    monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

    @retry_lance
    def raises_type() -> None:
        raise TypeError("wrong kind")

    with pytest.raises(TypeError):
        raises_type()

    assert sleep_calls == []  # no backoff/sleep occurred


def test_retries_lance_retryable_runtime_error(monkeypatch) -> None:
    """RuntimeError tagged 'lance error: Retryable' should be retried (GEN-474)."""
    attempts = {"count": 0}
    sleep_calls = []

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise RuntimeError(
                "lance error: Retryable commit conflict for version 2: "
                "This Merge transaction was preempted by concurrent transaction "
                "Delete at version 2. Please retry."
            )
        return "ok"

    monkeypatch.setattr(random, "uniform", lambda a, b: 0)
    monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

    wrapped = retry_lance(flaky)
    assert wrapped() == "ok"
    assert attempts["count"] == 3
    assert len(sleep_calls) == 2  # slept between retries


def test_does_not_retry_non_retryable_lance_runtime_error(monkeypatch) -> None:
    """RuntimeError without a known retryable marker should propagate immediately."""
    sleep_calls = []
    monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

    @retry_lance
    def raises_runtime() -> None:
        raise RuntimeError("lance error: some other non-retryable failure")

    with pytest.raises(RuntimeError):
        raises_runtime()

    assert sleep_calls == []


def test_retries_lance_namespace_throttle_error(monkeypatch) -> None:  # noqa: ANN001
    """Typed namespace throttle errors are bare Exceptions the OSError/
    ValueError retry set misses, so retry_lance must catch them explicitly."""
    from lance_namespace.errors import ServiceUnavailableError

    attempts = {"count": 0}
    sleep_calls = []

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise ServiceUnavailableError("service unavailable")
        return "ok"

    monkeypatch.setattr(random, "uniform", lambda a, b: 0)
    monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

    assert retry_lance(flaky)() == "ok"
    assert attempts["count"] == 3
    assert len(sleep_calls) == 2


def test_does_not_retry_table_not_found(monkeypatch) -> None:  # noqa: ANN001
    """TableNotFoundError stays non-retryable in retry_lance; its transient
    handling lives only in the checkpoint session-open wrapper."""
    from lance_namespace.errors import TableNotFoundError

    sleep_calls = []
    monkeypatch.setattr(time, "sleep", lambda s: sleep_calls.append(s))

    @retry_lance
    def raises_not_found() -> None:
        raise TableNotFoundError("Table not found: table id 'tbl'")

    with pytest.raises(TableNotFoundError):
        raises_not_found()

    assert sleep_calls == []


# Tests for deep_merge


def test_deep_merge_simple_dicts() -> None:
    """Test merging simple dictionaries."""
    base = {"a": 1, "b": 2}
    override = {"b": 3, "c": 4}
    result = deep_merge(base, override)

    assert result == {"a": 1, "b": 3, "c": 4}
    # Ensure original dicts are not modified
    assert base == {"a": 1, "b": 2}
    assert override == {"b": 3, "c": 4}


def test_deep_merge_nested_dicts() -> None:
    """Test merging nested dictionaries."""
    base = {"a": 1, "b": {"c": 2, "d": 3}}
    override = {"b": {"d": 4, "e": 5}, "f": 6}
    result = deep_merge(base, override)

    assert result == {"a": 1, "b": {"c": 2, "d": 4, "e": 5}, "f": 6}


def test_deep_merge_deeply_nested() -> None:
    """Test merging deeply nested dictionaries."""
    base = {"a": {"b": {"c": {"d": 1}}}}
    override = {"a": {"b": {"c": {"e": 2}}}}
    result = deep_merge(base, override)

    assert result == {"a": {"b": {"c": {"d": 1, "e": 2}}}}


def test_deep_merge_lists_append() -> None:
    """Test that lists are appended, not replaced."""
    base = {"containers": [{"name": "ray", "image": "ray:2.54.0"}]}
    override = {"containers": [{"name": "sidecar", "image": "sidecar:1.0"}]}
    result = deep_merge(base, override)

    assert len(result["containers"]) == 2
    assert result["containers"][0] == {"name": "ray", "image": "ray:2.54.0"}
    assert result["containers"][1] == {"name": "sidecar", "image": "sidecar:1.0"}


def test_deep_merge_empty_override() -> None:
    """Test merging with empty override returns base copy."""
    base = {"a": 1, "b": 2}
    override = {}
    result = deep_merge(base, override)

    assert result == base
    assert result is not base  # Should be a copy


def test_deep_merge_empty_base() -> None:
    """Test merging empty base with override."""
    base = {}
    override = {"a": 1, "b": 2}
    result = deep_merge(base, override)

    assert result == override


def test_deep_merge_type_mismatch_override_wins() -> None:
    """Test that when types mismatch, override value replaces base."""
    base = {"a": {"nested": "dict"}}
    override = {"a": "string"}  # Different type
    result = deep_merge(base, override)

    assert result == {"a": "string"}


def test_deep_merge_kubernetes_example() -> None:
    """Test realistic Kubernetes spec deep merge."""
    base = {
        "template": {
            "spec": {
                "containers": [
                    {
                        "name": "ray",
                        "image": "rayproject/ray:2.54.0",
                        "resources": {"limits": {"cpu": "4", "memory": "16Gi"}},
                    }
                ]
            }
        }
    }

    override = {
        "template": {
            "spec": {
                "securityContext": {"runAsNonRoot": True, "fsGroup": 1000},
                "initContainers": [{"name": "init", "image": "busybox:1.35"}],
            }
        }
    }

    result = deep_merge(base, override)

    # Original container should be preserved
    assert result["template"]["spec"]["containers"][0]["name"] == "ray"
    assert (
        result["template"]["spec"]["containers"][0]["image"] == "rayproject/ray:2.54.0"
    )

    # New fields should be added
    assert result["template"]["spec"]["securityContext"] == {
        "runAsNonRoot": True,
        "fsGroup": 1000,
    }
    assert len(result["template"]["spec"]["initContainers"]) == 1
    assert result["template"]["spec"]["initContainers"][0]["name"] == "init"


def test_deep_merge_nested_lists() -> None:
    """Test merging with nested lists in dicts."""
    base = {"spec": {"env": [{"name": "A", "value": "1"}]}}
    override = {"spec": {"env": [{"name": "B", "value": "2"}]}}
    result = deep_merge(base, override)

    # Lists should be appended
    assert len(result["spec"]["env"]) == 2
    assert result["spec"]["env"][0] == {"name": "A", "value": "1"}
    assert result["spec"]["env"][1] == {"name": "B", "value": "2"}


# Tests for size_to_bytes


def test_size_to_bytes_binary_suffixes() -> None:
    """Test binary suffixes (Ki, Mi, Gi, Ti)."""
    assert size_to_bytes("1Ki") == 1024
    assert size_to_bytes("1Mi") == 1024**2
    assert size_to_bytes("1Gi") == 1024**3
    assert size_to_bytes("8Gi") == 8 * 1024**3
    assert size_to_bytes("16Gi") == 16 * 1024**3
    assert size_to_bytes("16Ti") == 16 * 1024**4
    assert size_to_bytes("16Pi") == 16 * 1024**5
    assert size_to_bytes("16Ei") == 16 * 1024**6


def test_size_to_bytes_si_suffixes() -> None:
    """Test SI suffixes (k, M, G, T)."""
    assert size_to_bytes("1k") == 1000
    assert size_to_bytes("1M") == 1000**2
    assert size_to_bytes("1G") == 1000**3
    assert size_to_bytes("8G") == 8 * 1000**3
    assert size_to_bytes("8T") == 8 * 1000**4
    assert size_to_bytes("8P") == 8 * 1000**5
    assert size_to_bytes("8E") == 8 * 1000**6


def test_size_to_bytes_decimal_values() -> None:
    """Test decimal values like 1.5Gi."""
    assert size_to_bytes("1.5Gi") == int(1.5 * 1024**3)
    assert size_to_bytes("2.5G") == int(2.5 * 1000**3)


def test_size_to_bytes_plain_numbers() -> None:
    """Test plain numbers without suffix."""
    assert size_to_bytes("1000") == 1000
    assert size_to_bytes("1000000000") == 1000000000


def test_size_to_bytes_int_passthrough() -> None:
    """Test that integers pass through unchanged."""
    assert size_to_bytes(1000) == 1000
    assert size_to_bytes(8 * 1024**3) == 8 * 1024**3


def test_size_to_bytes_invalid_format_error_message() -> None:
    """Test that invalid formats produce helpful error messages."""
    with pytest.raises(ValueError, match="Invalid quantity format") as exc_info:
        size_to_bytes("invalid")

    error_msg = str(exc_info.value)
    assert "'invalid'" in error_msg
    assert "8Gi" in error_msg  # Example in error message
    assert "Ki, Mi, Gi" in error_msg  # Mentions binary units
    assert "k, M, G" in error_msg  # Mentions SI units


@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Commit conflict for version 6: ...", True),  # legacy lance wording
        ("Retryable commit conflict for version 6: ...", True),  # current wording
        ("RETRYABLE COMMIT CONFLICT FOR VERSION 6", True),  # case-insensitive
        ("Some other IO error", False),
        ("IncompatibleTransaction: removed target", False),
    ],
)
def test_is_retryable_commit_conflict(message: str, expected: bool) -> None:
    assert is_retryable_commit_conflict(OSError(message)) is expected
