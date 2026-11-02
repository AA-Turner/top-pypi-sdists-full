"""A database timeout wrapped as an ExecutionError is OUR write failing, never "the step ran past its time limit".

Live 2026-10-28 (run bcf4958b, Setup's crawl unit): a ``QueryTimeoutError`` while saving a step's result reached
the person as "What was crawled ran past its time limit and was stopped." — the wrapper type
``ExecutionError`` was given, so the class name opening the text was ignored and the prose ladder matched
"timed out" first.
"""

from __future__ import annotations

from matrx_graph.failure import Cause, failure_from_text


def test_a_wrapped_query_timeout_is_a_persistence_failure() -> None:
    f = failure_from_text("QueryTimeoutError:\nQuery timed out during execute_query\n  Operation: execute_query",
                          step_id="result", step_label="What was crawled", error_type="ExecutionError")
    assert f.cause == Cause.PERSISTENCE_FAILED
    assert "time limit" not in f.message


def test_a_real_step_timeout_still_reads_as_a_time_limit() -> None:
    f = failure_from_text("NodeTimeoutError: step exceeded 30s", step_id="x", error_type="ExecutionError")
    assert f.cause == Cause.TIMED_OUT


def test_a_wrapper_with_no_class_in_the_text_keeps_its_prose_reading() -> None:
    f = failure_from_text("the provider timed out", step_id="x", error_type="ExecutionError")
    assert f.cause == Cause.TIMED_OUT
