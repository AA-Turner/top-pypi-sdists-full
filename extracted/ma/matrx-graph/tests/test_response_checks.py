"""The response-check engine (``matrx_graph.checks``) — planted breaks per check type."""

from __future__ import annotations

import pytest

from matrx_graph.checks import (
    ResponseCheckSpec,
    UnknownHostCheckError,
    configure_host_checks,
    configure_host_projections,
    project_plain,
    run_checks,
    text_metrics,
)


def _words(n: int) -> str:
    return " ".join(["word"] * n)


def _length(**kw) -> ResponseCheckSpec:
    return ResponseCheckSpec(key="length", type="length", **kw)


def test_over_long_answer_fails_with_cut_direction_and_facts():
    res = run_checks(_words(1450), [_length(target=300)])
    assert res.verdict == "fail"
    m = res.checks[0]
    assert (m.measured, m.band_min, m.band_max, m.direction) == (1450, 240, 360, "cut")
    assert "1,450 words; target 300 (240–360); cut about 1,150" in res.rendered


def test_answer_inside_the_default_20pct_band_passes():
    assert run_checks(_words(350), [_length(target=300)]).verdict == "pass"
    assert run_checks(_words(361), [_length(target=300)]).verdict == "fail"
    assert run_checks(_words(239), [_length(target=300)]).checks[0].direction == "add"


def test_tolerance_is_the_callers_knob_value():
    assert run_checks(_words(350), [_length(target=300)], default_tolerance_pct=10).verdict == "fail"


def test_blank_target_skips_never_invents_one():
    res = run_checks(_words(5000), [_length(target_value="target_word_count")], {"target_word_count": ""})
    assert res.verdict == "skipped"
    assert res.checks[0].detail == "skipped: no target"


def test_target_read_from_mapped_values():
    res = run_checks(_words(100), [_length(target_value="target_word_count")], {"target_word_count": 300})
    assert res.verdict == "fail" and res.checks[0].direction == "add"


def test_plain_projection_does_not_count_markup():
    text = "# Title\n\n<b>bold</b> **two** words\n```\ncode code code\n```"
    assert text_metrics(project_plain(text))["words"] == 4


def test_host_projection_and_check_by_name():
    configure_host_projections({"t.spoken": lambda s: s.split("|", 1)[1]})
    configure_host_checks({"t.has_bar": lambda s, v: None if "|" in s else "no bar"})
    specs = [
        _length(target=2, projection="t.spoken", tolerance_pct=0),
        ResponseCheckSpec(key="shape", type="host", host_check="t.has_bar", on_exhausted="fail"),
    ]
    assert run_checks("LABEL LABEL LABEL|one two", specs).verdict == "pass"
    bad = run_checks("one two", [specs[1]])
    assert bad.verdict == "fail" and bad.checks[0].direction == "fix"
    assert "no bar" in bad.rendered


def test_unregistered_host_name_is_loud_never_a_pass():
    with pytest.raises(UnknownHostCheckError):
        run_checks("x", [ResponseCheckSpec(key="k", type="host", host_check="nobody.registered")])
    with pytest.raises(UnknownHostCheckError):
        run_checks("x", [_length(target=1, projection="nobody.registered")])


def test_word_count_node_uses_the_one_counter():
    from matrx_utils.source_guard import stable_source

    from matrx_graph.nodes.text.manipulate import WordCountExecutor

    src = stable_source(WordCountExecutor.execute)
    assert "text_metrics" in src and "re.findall" not in src
