#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Null distribution analysis for shaping ES masking to real-world data patterns.

Compute per-column null rates from any data source — production exports, representative
samples, or the training data itself — and save the result as JSON. The ES training
pipeline can then load this distribution to bias its masking strategy, so the model
learns representations that are robust to the null patterns it will actually see.

Usage::

    from featrixsphere import compute_null_distribution

    # From a file
    dist = compute_null_distribution("production_sample.csv")

    # From a DataFrame
    dist = compute_null_distribution(df, ignore_columns=["id", "timestamp"])

    # Save for training
    import json
    with open("null_distribution.json", "w") as f:
        json.dump(dist, f, indent=2)
"""
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

logger = logging.getLogger(__name__)


def compute_null_distribution(
    data: Union[str, Path, pd.DataFrame],
    ignore_columns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Compute per-column null distribution from a data file or DataFrame.

    Point this at your production data, a representative sample, or any CSV/parquet/JSON
    to learn the null patterns your model will see in the real world.  The returned dict
    can be saved as JSON and passed to ES training via the ``null_distribution_path``
    config key.

    Args:
        data: One of:
            - ``str`` or ``Path``: path to a CSV, Parquet, or JSON file
            - ``pd.DataFrame``: an already-loaded DataFrame
        ignore_columns: Column names to exclude from analysis (e.g. IDs, timestamps).

    Returns:
        Dict with per-column null counts/rates and summary statistics::

            {
                "total_rows": 50000,
                "total_columns": 25,
                "per_column": {
                    "phone": {"null_count": 12500, "null_rate": 0.25},
                    "email": {"null_count": 5000, "null_rate": 0.10},
                    ...
                },
                "summary": {
                    "mean_null_rate": 0.12,
                    "median_null_rate": 0.08,
                    "max_null_rate": 0.45,
                    "columns_always_present": 15,
                    "columns_sometimes_null": 8,
                    "columns_mostly_null": 2,
                }
            }

    Raises:
        FileNotFoundError: If *data* is a path that does not exist.
        ValueError: If the resulting DataFrame is empty or has no analyzable columns.
    """
    df = _load_data(data)

    if ignore_columns:
        ignore_set = set(ignore_columns)
    else:
        ignore_set = set()

    cols = [c for c in df.columns if c not in ignore_set]

    if not cols:
        raise ValueError(
            "No columns to analyze after applying ignore_columns filter"
        )

    total_rows = len(df)
    if total_rows == 0:
        raise ValueError("DataFrame is empty — nothing to analyze")

    # Per-column null counts
    null_counts = df[cols].isna().sum(axis=0)

    per_column = {}
    null_rates = []
    for col in cols:
        nc = int(null_counts[col])
        rate = nc / total_rows
        per_column[col] = {
            "null_count": nc,
            "null_rate": round(rate, 6),
        }
        null_rates.append(rate)

    # Summary statistics
    import numpy as np

    rates_arr = np.array(null_rates)
    columns_always_present = int((rates_arr == 0.0).sum())
    columns_sometimes_null = int(((rates_arr > 0.0) & (rates_arr <= 0.5)).sum())
    columns_mostly_null = int((rates_arr > 0.5).sum())

    result = {
        "total_rows": total_rows,
        "total_columns": len(cols),
        "per_column": per_column,
        "summary": {
            "mean_null_rate": round(float(rates_arr.mean()), 6),
            "median_null_rate": round(float(np.median(rates_arr)), 6),
            "max_null_rate": round(float(rates_arr.max()), 6),
            "columns_always_present": columns_always_present,
            "columns_sometimes_null": columns_sometimes_null,
            "columns_mostly_null": columns_mostly_null,
        },
    }

    # Log a quick summary
    logger.info(
        "Null distribution: %d rows, %d columns — "
        "%d always present, %d sometimes null, %d mostly null (>50%%)",
        total_rows,
        len(cols),
        columns_always_present,
        columns_sometimes_null,
        columns_mostly_null,
    )

    return result


def _load_data(data: Union[str, Path, pd.DataFrame]) -> pd.DataFrame:
    """Load data from a file path or return the DataFrame as-is."""
    if isinstance(data, pd.DataFrame):
        return data

    path = Path(data)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    elif suffix in (".parquet", ".pq"):
        return pd.read_parquet(path)
    elif suffix == ".json":
        return pd.read_json(path)
    elif suffix in (".tsv",):
        return pd.read_csv(path, sep="\t")
    elif suffix in (".xlsx", ".xls"):
        return pd.read_excel(path)
    else:
        # Try CSV as fallback
        logger.warning("Unknown file extension %r — attempting CSV parse", suffix)
        return pd.read_csv(path)
