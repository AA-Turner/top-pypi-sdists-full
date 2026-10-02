"""What the terminal charts promise, asserted against the characters they emit.

A chart is the one output nobody diffs -- it looks plausible whatever it draws,
so a curve rendered upside down, a series silently erased by an overlapping one,
or an axis labelled with values no point ever took all ship looking fine. These
pin the properties a reader is entitled to assume:

  the curve goes the way the data goes, and connects
  a tick label is a value the axis actually passes through
  identity survives losing color -- a pipe, a monochrome terminal, a CVD reader
  nothing is dropped without saying so

The braille bit table is asserted against the Unicode block itself rather than
against a golden string: a mistake there mirrors the whole plot vertically,
which no eyeball catches in a field of dots.
"""

from __future__ import annotations

import math

import pytest

from probe import cli
from probe.cli import charts
from tests.conftest import make_client

PLAIN = {"color": False, "unicode": True}


def _series(label: str, ys, xs=None) -> charts.Series:
    return charts.Series(label, list(zip(xs or range(len(ys)), ys)))


def _plot_rows(text: str) -> list[str]:
    """The plot area only: no title, axis rule, tick labels, legend or footer."""
    body = [line for line in text.splitlines() if "┤" in line or "│" in line]
    return [line.split("┤", 1)[-1].split("│", 1)[-1] for line in body]


# -- braille ------------------------------------------------------------------


@pytest.mark.parametrize(
    "sub_x,sub_y,expected",
    [
        (0, 0, "⠁"),
        (0, 1, "⠂"),
        (0, 2, "⠄"),
        (0, 3, "⡀"),
        (1, 0, "⠈"),
        (1, 1, "⠐"),
        (1, 2, "⠠"),
        (1, 3, "⢀"),
    ],
)
def test_every_subpixel_maps_to_its_own_braille_dot(sub_x, sub_y, expected):
    canvas = charts._Braille(1, 1)
    canvas.mark(sub_x, sub_y, 0)
    assert canvas.rows() == [[(expected, 0)]]


def test_marks_outside_the_canvas_are_dropped_not_wrapped():
    canvas = charts._Braille(2, 1)
    for x, y in ((-1, 0), (0, -1), (4, 0), (0, 4)):
        canvas.mark(x, y, 0)
    assert canvas.rows() == [[("⠀⠀", None)]]


# -- panel geometry -----------------------------------------------------------


def test_a_rising_series_climbs_from_bottom_left_to_top_right():
    text = charts.panel([_series("up", range(20))], width=20, height=6, **PLAIN)
    rows = _plot_rows(text)
    first = [r for r, row in enumerate(rows) if row[0] != "⠀"]
    last = [r for r, row in enumerate(rows) if row[-1] != "⠀"]
    assert max(first) > max(last), "the left end must sit below the right end"


def test_a_falling_series_is_not_silently_the_same_picture():
    up = charts.panel([_series("up", range(20))], width=20, height=6, **PLAIN)
    down = charts.panel([_series("down", range(19, -1, -1))], width=20, height=6, **PLAIN)
    assert _plot_rows(up) != _plot_rows(down)


def test_two_distant_points_are_joined_rather_than_left_as_dots():
    text = charts.panel([_series("sparse", [0.0, 1.0], xs=[0, 40])], width=40, height=6, **PLAIN)
    blanks = [column for row in _plot_rows(text) for column in row if column == "⠀"]
    drawn = sum(1 for row in _plot_rows(text) for column in row if column != "⠀")
    assert drawn >= 20, f"a two-point line left only {drawn} marked cells among {len(blanks)}"


def test_a_constant_series_sits_on_one_row_with_one_label():
    text = charts.panel([_series("flat", [7.0] * 10)], width=20, height=7, **PLAIN)
    marked = [r for r, row in enumerate(_plot_rows(text)) if row.strip("⠀")]
    assert marked == [3]
    assert len([line for line in text.splitlines() if "┤" in line]) == 1
    assert "7" in text


def test_a_panel_with_no_points_says_so_instead_of_dividing_by_zero():
    assert "(no points)" in charts.panel([charts.Series("empty", [])], title="empty", **PLAIN)


# -- axes ---------------------------------------------------------------------


def test_tick_labels_land_on_round_numbers_the_axis_passes_through():
    text = charts.panel([_series("v", [0.0, 324.3])], width=20, height=9, **PLAIN)
    labels = [line.split("┤")[0].strip() for line in text.splitlines() if "┤" in line]
    assert labels == ["300", "200", "100", "0"]


@pytest.mark.parametrize(
    "lo,hi,expected",
    [
        (0.3117, 0.3128, ["0.3125", "0.312"]),
        (-2.0, 2.0, ["2", "1", "0", "-1", "-2"]),
        (0.0, 1.2e-06, ["1.000e-06", "5.000e-07", "0"]),
        (0.0, 1_400_000.0, ["1.000e+06", "5.000e+05", "0"]),
    ],
)
def test_ticks_stay_round_at_every_scale(lo, hi, expected):
    text = charts.panel([_series("v", [lo, hi])], width=20, height=9, **PLAIN)
    assert [line.split("┤")[0].strip() for line in text.splitlines() if "┤" in line] == expected


def test_a_zero_width_range_labels_its_own_value_rather_than_dividing_by_zero():
    assert charts._ticks(charts._Scale(4.0, 4.0, flat=False), 5) == {0: "4", 4: "4"}


def test_the_x_axis_carries_the_step_range():
    text = charts.panel([_series("v", range(10), xs=range(100, 110))], width=40, **PLAIN)
    axis = text.splitlines()[-1]
    assert axis.strip().startswith("100") and "109" in axis and axis.endswith("step")


# -- identity -----------------------------------------------------------------


def test_a_second_series_gets_its_own_glyph_and_a_legend_naming_both():
    text = charts.panel(
        [_series("train/loss", [0.0, 1.0]), _series("eval/loss", [1.0, 0.0])],
        width=20,
        height=5,
        **PLAIN,
    )
    assert "o train/loss" in text and "x eval/loss" in text
    plot = "".join(_plot_rows(text))
    assert "o" in plot and "x" in plot, "identity must not depend on color"


def test_one_series_needs_no_legend_because_the_title_names_it():
    text = charts.panel([_series("train/loss", [0.0, 1.0])], title="train/loss", **PLAIN)
    assert text.count("train/loss") == 1


def test_coincident_curves_are_marked_as_overlap_not_reduced_to_one():
    """Two identical curves used to draw as one: the second series had no glyph
    anywhere on the canvas while the legend still named it."""
    both = [_series("first", [0.0, 1.0]), _series("second", [0.0, 1.0])]
    text = charts.panel(both, width=20, height=5, **PLAIN)
    plot = "".join(_plot_rows(text))
    assert "%" in plot, "a contested cell must say so"
    assert "% overlap" in text, "and the legend must name the glyph"


def test_color_repeats_identity_and_never_replaces_it():
    text = charts.panel(
        [_series("a", [0.0, 1.0]), _series("b", [1.0, 0.0])],
        width=20,
        height=5,
        color=True,
        unicode=True,
    )
    assert "\033[36m" in text and "\033[33m" in text
    assert "o" in text and "x" in text


def test_a_lone_curve_is_not_painted_at_all():
    text = charts.panel([_series("a", [0.0, 1.0])], width=20, color=True, unicode=True)
    assert "\033[36m" not in text


# -- degraded terminals -------------------------------------------------------


def test_ascii_mode_emits_nothing_the_encoding_cannot_carry():
    """Built from the REAL footers and a non-ASCII label, not a placeholder: the
    middot in `summarize()` slipped past a `footer="f"` version of this test and
    made `--ascii` raise UnicodeEncodeError on the stream the flag is for."""
    pair = [_series("训练/loss", range(10)), _series("b", range(10, 0, -1))]
    ascii_only = {"color": False, "unicode": False}
    text = charts.panel(
        pair,
        title=" + ".join(s.label for s in pair),
        footer=charts.overlay_footer(pair, unicode=False),
        width=30,
        **ascii_only,
    )
    text.encode("ascii")  # raises if a braille, box-drawing or CJK glyph escaped
    charts.panel(
        [pair[0]],
        title=pair[0].label,
        footer=charts.summarize(pair[0], unicode=False),
        width=30,
        **ascii_only,
    ).encode("ascii")
    charts.board(pair, width=60, **ascii_only).encode("ascii")


def test_board_in_ascii_mode_still_shows_the_shape():
    text = charts.board([_series("a", range(10))], width=60, color=False, unicode=False)
    text.encode("ascii")
    assert "^" in text and "_" in text


def test_no_color_env_is_honored_over_a_tty(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "")
    monkeypatch.setattr("sys.stdout.isatty", lambda: True, raising=False)
    assert charts.use_color() is False


class _Stream:
    def __init__(self, encoding: str) -> None:
        self.encoding = encoding

    def isatty(self) -> bool:
        return True


@pytest.mark.parametrize("encoding,expected", [("ascii", False), ("utf-8", True), ("", False)])
def test_unicode_is_decided_by_what_the_stream_can_encode(monkeypatch, encoding, expected):
    monkeypatch.setattr(charts.sys, "stdout", _Stream(encoding))
    assert charts.use_unicode() is expected


# -- board and sparklines -----------------------------------------------------


def test_sparkline_puts_the_extremes_on_the_extreme_blocks():
    spark = charts.sparkline([0.0, 0.5, 1.0])
    assert spark[0] == "▁" and spark[-1] == "█" and len(spark) == 3


def test_sparkline_averages_into_buckets_rather_than_sampling():
    # A spike between samples must survive; a stride would step over it.
    assert charts.sparkline([0.0, 0.0, 9.0, 0.0, 0.0, 0.0], 3)[1] == "█"


def test_a_constant_sparkline_is_flat_not_empty():
    assert charts.sparkline([2.0] * 5) == "▅" * 5


def test_board_rows_line_up_and_carry_the_numbers_the_spark_cannot():
    text = charts.board(
        [_series("train/loss", [1.0, 0.5]), _series("lr", [1e-6, 1e-6])],
        width=80,
        color=False,
        unicode=True,
    )
    lines = text.splitlines()
    assert len({len(line) for line in lines}) == 1, "columns must align"
    assert "1.000e-06" in text and "0.5" in text


def test_a_long_metric_name_is_truncated_visibly():
    text = charts.board([_series("a/" + "b" * 90, [1.0, 2.0])], width=60, color=False, unicode=True)
    assert "…" in text


# -- the wide-table adapter ---------------------------------------------------


def _wide(columns, rows) -> dict:
    return {"columns": columns, "rows": rows}


def test_holes_in_the_pivot_are_closed_not_drawn_as_breaks():
    table = _wide(
        [{"key": "loss", "dimensions": {}}],
        [{"step_index": s, "values": [1.0 if s % 10 == 0 else None]} for s in range(21)],
    )
    (series,) = charts.series_from_wide(table)
    assert [x for x, _ in series.points] == [0.0, 10.0, 20.0]


def test_a_column_with_nothing_in_it_is_not_a_series():
    table = _wide(
        [{"key": "loss", "dimensions": {}}, {"key": "acc", "dimensions": {}}],
        [{"step_index": 0, "values": [0.5, None]}],
    )
    assert [s.label for s in charts.series_from_wide(table)] == ["loss"]


def test_a_key_split_across_coordinates_keeps_them_apart_in_the_label():
    table = _wide(
        [{"key": "loss", "dimensions": {"rank": 1, "split": "train"}}],
        [{"step_index": 0, "values": [0.5]}],
    )
    assert charts.series_from_wide(table)[0].label == "loss{rank=1,split=train}"


def test_one_key_under_two_kinds_stays_two_named_series():
    """A column is (kind, key, dimensions) and `probe log --kind` is user-set, so
    two columns can differ by kind alone. Named identically they are one series
    to every reader; keyed identically they were one series to `board`."""
    table = _wide(
        [
            {"kind": "model", "key": "loss", "dimensions": {}},
            {"kind": "system", "key": "loss", "dimensions": {}},
        ],
        [{"step_index": 0, "values": [0.5, 99.0]}],
    )
    assert [s.label for s in charts.series_from_wide(table)] == ["model:loss", "system:loss"]


def test_the_kind_is_spent_only_where_it_disambiguates():
    table = _wide(
        [
            {"kind": "model", "key": "loss", "dimensions": {}},
            {"kind": "model", "key": "acc", "dimensions": {}},
        ],
        [{"step_index": 0, "values": [0.5, 0.9]}],
    )
    assert [s.label for s in charts.series_from_wide(table)] == ["loss", "acc"]


def test_the_board_prints_each_series_own_numbers_not_its_namesakes():
    same = [charts.Series("loss", [(0, 0.5)]), charts.Series("loss", [(0, 99.0)])]
    body = charts.board(same, width=80, color=False, unicode=True).splitlines()[1:]
    assert [line.split()[-1] for line in body] == ["0.5", "99"]


def test_a_control_character_in_a_key_cannot_shift_the_columns():
    table = _wide(
        [{"kind": "model", "key": "loss\t\033[2Jrogue", "dimensions": {}}],
        [{"step_index": 0, "values": [0.5]}],
    )
    (series,) = charts.series_from_wide(table)
    assert "\t" not in series.label and "\033" not in series.label
    assert series.label == "loss??[2Jrogue"


def test_a_nan_is_counted_out_loud_not_quietly_skipped():
    """A loss that goes NaN is the single most important thing a run logs. Left
    out of the scale AND out of the count, a diverged run draws as a clean line
    from the value before the NaN to the value after it."""
    table = _wide(
        [{"key": "loss", "dimensions": {}}],
        [
            {"step_index": 0, "values": [1.0]},
            {"step_index": 1, "values": [float("nan")]},
            {"step_index": 2, "values": [float("inf")]},
            {"step_index": 3, "values": [0.8]},
        ],
    )
    (series,) = charts.series_from_wide(table)
    assert series.points == [(0.0, 1.0), (3.0, 0.8)]
    assert series.dropped == 2
    assert "2 non-finite, not plotted" in charts.summarize(series, unicode=False)


def test_an_all_nan_series_survives_as_a_reportable_zero_point_curve():
    table = _wide(
        [{"key": "loss", "dimensions": {}}],
        [{"step_index": 0, "values": [float("nan")]}],
    )
    (series,) = charts.series_from_wide(table)
    assert series.points == [] and series.dropped == 1


def test_a_span_too_wide_to_be_a_scale_does_not_crash():
    text = charts.panel([_series("v", [-1e308, 1e308])], width=20, height=5, **PLAIN)
    assert "(no points)" not in text


def test_a_span_too_narrow_to_divide_does_not_crash():
    text = charts.panel([_series("v", [5e-324, 1e-323])], width=20, height=5, **PLAIN)
    assert "┤" in text


def test_a_dimension_value_carrying_the_separators_is_quoted():
    one = charts.label_for({"key": "loss", "dimensions": {"a": "b,c=d"}})
    two = charts.label_for({"key": "loss", "dimensions": {"a": "b", "c": "d"}})
    assert one != two


def test_a_wide_label_is_padded_by_terminal_cells_not_code_points():
    text = charts.board(
        [_series("训练损失率", [1.0, 2.0]), _series("loss", [1.0, 2.0])],
        width=80,
        color=False,
        unicode=True,
    )
    assert len({charts._cells(line) for line in text.splitlines()}) == 1


def test_the_overlay_footer_names_the_cost_of_the_shared_axis():
    footer = charts.overlay_footer([_series("big", [0.0, 300.0]), _series("small", [0.0, 1e-9])])
    assert "one shared axis" in footer and "orders of magnitude" in footer


def test_comparable_scales_get_no_caution():
    footer = charts.overlay_footer([_series("a", [0.0, 1.0]), _series("b", [0.0, 2.0])])
    assert "orders of magnitude" not in footer


def test_fmt_keeps_ordinary_numbers_out_of_scientific_notation():
    assert charts.fmt(0.0342) == "0.0342"
    assert charts.fmt(0) == "0"
    assert charts.fmt(1.863e-09) == "1.863e-09"
    assert charts.fmt(math.inf) == "inf"


# -- the CLI verb -------------------------------------------------------------


@pytest.fixture
def wired(app, tmp_path, monkeypatch):
    def factory(**_kw):
        return make_client(app, tmp_spool=tmp_path / "spool")

    monkeypatch.setattr(cli, "Client", factory)
    cli.main(["project", "create", "--kind", "general", "p"])
    cli.main(["experiment", "create", "e", "--question", "h", "--project", "p"])
    return app


def _run_with_points(wired, capsys) -> str:
    cli.main(["run", "start", "--experiment", "e", "--name", "r1"])
    rid = capsys.readouterr().out.strip()
    wired.metric_points[rid] = [
        {
            "id": i + 1,
            "key": "loss",
            "kind": "model",
            "value": 1.0 - i / 10,
            "step_index": i,
            "dimensions": {},
        }
        for i in range(10)
    ] + [
        {
            "id": 100 + i,
            "key": "lr",
            "kind": "model",
            "value": 1e-6,
            "step_index": i,
            "dimensions": {},
        }
        for i in range(10)
    ]
    return rid


def test_plot_without_keys_draws_the_whole_board(wired, capsys):
    rid = _run_with_points(wired, capsys)
    assert cli.main(["metrics", "plot", rid, "--width", "80"]) == 0
    out = capsys.readouterr().out
    assert "loss" in out and "lr" in out and "curve" in out


def test_plot_with_a_key_draws_a_panel_with_axes(wired, capsys):
    rid = _run_with_points(wired, capsys)
    assert cli.main(["metrics", "plot", rid, "--key", "loss", "--width", "60"]) == 0
    out = capsys.readouterr().out
    assert "┤" in out and "10 points" in out
    request = next(r for r in wired.requests if r.url.path.endswith("/metrics/wide"))
    assert request.url.params.get_list("key") == ["loss"]


def test_plot_resolves_the_run_ref_its_siblings_pass_through(wired, capsys):
    """`metrics wide` hands the argument straight to a uuid-typed path param, so a
    petname 422s there. Plot goes through the run resolver first, which is the
    route that accepts both spellings."""
    rid = _run_with_points(wired, capsys)
    assert cli.main(["metrics", "plot", rid, "--key", "loss"]) == 0
    assert any(r.url.path == f"/v1/runs/{rid}" for r in wired.requests)


def test_overlaying_more_series_than_glyphs_names_what_it_dropped(wired, capsys):
    cli.main(["run", "start", "--experiment", "e", "--name", "r2"])
    rid = capsys.readouterr().out.strip()
    keys = [f"m{i}" for i in range(charts.MAX_OVERLAY + 2)]
    wired.metric_points[rid] = [
        {
            "id": i + 1,
            "key": k,
            "kind": "model",
            "value": float(i),
            "step_index": 0,
            "dimensions": {},
        }
        for i, k in enumerate(keys)
    ]
    argv = ["metrics", "plot", rid, "--overlay", "--width", "40"]
    for k in keys:
        argv += ["--key", k]
    assert cli.main(argv) == 0
    captured = capsys.readouterr()
    assert f"overlaying the first {charts.MAX_OVERLAY}" in captured.err
    dropped = set(keys) - set(captured.out.splitlines()[0].split(" + "))
    assert dropped and all(name in captured.err for name in dropped)


def test_a_partial_read_is_announced_rather_than_drawn_as_the_whole_curve(wired, capsys):
    """`--max-rows` (and the SDK's page cap) return `truncated` + `next_step`. Drawn
    without a word, a cut-short window is a complete-looking curve."""
    rid = _run_with_points(wired, capsys)
    assert cli.main(["metrics", "plot", rid, "--key", "loss", "--max-rows", "3"]) == 0
    captured = capsys.readouterr()
    assert "PARTIAL" in captured.err and "--max-rows" in captured.err
    assert "3 points" in captured.out


def test_a_key_that_matched_nothing_is_named_even_when_others_drew(wired, capsys):
    rid = _run_with_points(wired, capsys)
    assert cli.main(["metrics", "plot", rid, "--key", "loss", "--key", "typo"]) == 0
    captured = capsys.readouterr()
    assert "no series for: typo" in captured.err
    assert "loss" in captured.out


# No end-to-end NaN test, deliberately. The fake refuses to encode one, and so
# does the real backend: FastAPI's JSONResponse renders with `allow_nan=False`,
# so a stored NaN raises there rather than arriving here. The client's own
# `json.loads` DOES accept a bare `NaN` literal, so the guard is reachable from
# any producer that serializes differently -- which is why it exists and why it
# is tested at `series_from_wide`, the boundary it actually defends.


def test_overlay_without_keys_is_refused_rather_than_guessed(wired, capsys):
    rid = _run_with_points(wired, capsys)
    assert cli.main(["metrics", "plot", rid, "--overlay"]) != 0


def test_an_empty_window_says_where_to_look_instead_of_drawing_nothing(wired, capsys):
    rid = _run_with_points(wired, capsys)
    assert cli.main(["metrics", "plot", rid, "--key", "nope"]) == 0
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "no series for: nope" in captured.err
    assert "no plottable metric points" in captured.err and "probe run series" in captured.err
