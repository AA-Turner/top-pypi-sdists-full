"""Regression tests for the cid_vs_yield scatter picker.

Pre-0.4.689 the picker used day-of-year span to choose the "full-season"
column per CID, which under `monthly_r` mis-selected the 2-stage
`Dec 1-Nov 30` column (looks like 365 days, actually 2 months of data)
over the true full-season `Apr 1-Nov 30` (6-stage chain covering
Nov->Apr). The 0.4.689 rewrite switched to method-aware stage-chain
counting.
"""

from geocif.viz.diagnostics import _stage_chain_length, _parse_cid_column


def test_monthly_r_dec_to_nov_is_two_stages_not_twelve():
    # The label `Dec 1-Nov 30` under monthly_r encodes the chain
    # [12, 11] — Nov + Dec — NOT the full year.
    assert _stage_chain_length("Dec", "Nov", "monthly_r") == 2


def test_monthly_r_apr_to_nov_is_full_six_stage_season():
    # `Apr 1-Nov 30` under monthly_r is the chain [4, 3, 2, 1, 12, 11]
    # — the full Nov->Apr season.
    assert _stage_chain_length("Apr", "Nov", "monthly_r") == 6


def test_monthly_r_single_month_chain_is_one():
    assert _stage_chain_length("Apr", "Apr", "monthly_r") == 1


def test_monthly_forward_three_stage_chain():
    assert _stage_chain_length("Mar", "May", "monthly") == 3


def test_monthly_forward_year_wrap_is_twelve():
    assert _stage_chain_length("Dec", "Nov", "monthly") == 12


def test_parse_cid_column_returns_chain_length_under_method():
    # Under monthly_r the same label is 6 stages; under forward monthly
    # it walks the long way around to 8.
    assert _parse_cid_column("H-INDEX_NDVI Apr 1-Nov 30", "monthly_r") == ("H-INDEX_NDVI", 6)
    assert _parse_cid_column("H-INDEX_NDVI Apr 1-Nov 30", "monthly") == ("H-INDEX_NDVI", 8)


def test_parse_cid_column_rejects_non_stage_columns():
    # Pre-Season aggregates, categorical, and the target column must
    # all be filtered out — none of them match the `<CID> Mon dd-Mon dd`
    # canonical format.
    assert _parse_cid_column("Pre-Season") is None
    assert _parse_cid_column("Yield (tn per ha)") is None
    assert _parse_cid_column("Region") is None
