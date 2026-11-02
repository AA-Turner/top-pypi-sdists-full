from __future__ import annotations

import pytest

from textcharts import ChartOptions, RankTable, RankTableData
from textcharts.rank_table import from_matrix


def _opts(**kw):
    return ChartOptions(use_color=False, width=80, **kw)


def test_empty_data():
    data = RankTableData(items=[], groups=[], values={})
    assert "No data" in RankTable(data=data).render()


def test_ranking_computation():
    data = RankTableData(
        items=["Q1", "Q2"],
        groups=["A", "B", "C"],
        values={
            ("A", "Q1"): 100, ("B", "Q1"): 200, ("C", "Q1"): 300,
            ("A", "Q2"): 300, ("B", "Q2"): 100, ("C", "Q2"): 200,
        },
    )
    result = RankTable(data=data, options=_opts()).render()
    # Q1: A=1st, B=2nd, C=3rd
    # Q2: B=1st, C=2nd, A=3rd
    assert "1st" in result
    assert "2nd" in result
    assert "3rd" in result


def test_ordinal_formatting():
    assert RankTable._ordinal(1) == "1st"
    assert RankTable._ordinal(2) == "2nd"
    assert RankTable._ordinal(3) == "3rd"
    assert RankTable._ordinal(4) == "4th"
    assert RankTable._ordinal(11) == "11th"
    assert RankTable._ordinal(12) == "12th"
    assert RankTable._ordinal(13) == "13th"
    assert RankTable._ordinal(21) == "21st"


def test_win_counts():
    data = RankTableData(
        items=["Q1", "Q2", "Q3"],
        groups=["A", "B"],
        values={
            ("A", "Q1"): 10, ("B", "Q1"): 20,   # A wins
            ("A", "Q2"): 20, ("B", "Q2"): 10,   # B wins
            ("A", "Q3"): 10, ("B", "Q3"): 20,   # A wins
        },
    )
    result = RankTable(data=data, options=_opts()).render()
    assert "Wins" in result
    # A has 2 wins, B has 1 win
    lines = result.splitlines()
    wins_line = next(line for line in lines if "Wins" in line)
    assert "2" in wins_line
    assert "1" in wins_line


def test_georank_computation():
    data = RankTableData(
        items=["Q1"],
        groups=["A", "B"],
        values={("A", "Q1"): 10, ("B", "Q1"): 20},
    )
    result = RankTable(data=data, options=_opts()).render()
    assert "GeoRank" in result
    # A is rank 1, georank = 1.0; B is rank 2, georank = 2.0
    lines = result.splitlines()
    geo_line = next(line for line in lines if "GeoRank" in line)
    assert "1.0" in geo_line
    assert "2.0" in geo_line


def test_natural_sort_queries():
    data = RankTableData(
        items=["Q10", "Q2", "Q1"],
        groups=["A"],
        values={("A", "Q1"): 10, ("A", "Q2"): 20, ("A", "Q10"): 30},
    )
    result = RankTable(data=data, options=_opts()).render()
    lines = result.splitlines()
    query_positions = {}
    for idx, line in enumerate(lines):
        first_token = line.split()[0] if line.split() else ""
        if first_token in {"Q1", "Q2", "Q10"}:
            query_positions[first_token] = idx

    assert query_positions["Q1"] < query_positions["Q2"] < query_positions["Q10"]


def test_from_matrix_factory():
    matrix = [[100, 200], [300, 100]]
    chart = from_matrix(matrix, ["Q1", "Q2"], ["A", "B"], title="Factory Test", options=_opts())
    result = chart.render()
    assert isinstance(chart, RankTable)
    assert "Factory Test" in result
    assert "Q1" in result
    assert "Q2" in result


def test_from_matrix_validation():
    with pytest.raises(ValueError, match="items length"):
        from_matrix([[1, 2]], ["Q1", "Q2"], ["A", "B"])
    with pytest.raises(ValueError, match="columns"):
        from_matrix([[1, 2], [3]], ["Q1", "Q2"], ["A", "B"])
