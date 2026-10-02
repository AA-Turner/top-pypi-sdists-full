"""Early-stopping validation rows are held out by year (2026-09-30 audit).

``optuna_objective`` and the fine-tuned TabPFN / TabICL fitters used a
random row split, which puts the same season's regions on both sides.
"""
import numpy as np
import pandas as pd

from geocif.ml import trainers


def _frame(n_years, per_year=6):
    rng = np.random.default_rng(0)
    years = np.repeat(np.arange(2000, 2000 + n_years), per_year)
    X = pd.DataFrame({"x": rng.normal(size=len(years)), "Harvest Year": years})
    y = pd.Series(rng.normal(size=len(years)), index=X.index)
    return X, y


def test_year_holdout_split_never_shares_a_year():
    X, y = _frame(10)
    X_tr, X_val, y_tr, y_val = trainers.year_holdout_split(X, y, test_size=0.2)
    assert not set(X_tr["Harvest Year"]) & set(X_val["Harvest Year"])
    assert len(X_tr) + len(X_val) == len(X)
    assert list(y_tr.index) == list(X_tr.index)
    assert list(y_val.index) == list(X_val.index)


def test_year_holdout_split_falls_back_to_rows_with_few_years():
    X, y = _frame(3)
    X_tr, X_val, _, _ = trainers.year_holdout_split(X, y, test_size=0.2)
    assert len(X_tr) + len(X_val) == len(X)
    assert len(X_val) == round(0.2 * len(X))


def test_year_holdout_split_without_year_column_uses_rows():
    X, y = _frame(10)
    X = X.drop(columns=["Harvest Year"])
    X_tr, X_val, _, _ = trainers.year_holdout_split(X, y, test_size=0.25)
    assert len(X_val) == len(X) // 4
