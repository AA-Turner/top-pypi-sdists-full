"""Tests for the NASS QuickStats fetcher (geocif/viz/nass.py).

Covers the cache-safety contract of ``fetch``: (a) an all-400 (empty) answer
must not clobber an existing non-empty cache; (b) a failure AFTER a successful
fetch — e.g. the cache write — must propagate, not masquerade as an
unreachable API; (c) the happy path still writes the cache; (d) a genuine
network failure still falls back to the cache. No network — ``fetch`` takes
an injected session.
"""
import tempfile
import unittest
from pathlib import Path

import pandas as pd
import requests


def _row(year=2024, period="YEAR - AUG FORECAST", value="180",
         load_time="2024-08-12 12:00:00", state="IOWA", fips="19"):
    """One QuickStats JSON row with just the fields _tidy consumes."""
    return {"year": year, "reference_period_desc": period, "Value": value,
            "load_time": load_time, "state_name": state,
            "state_fips_code": fips}


class _Resp:
    def __init__(self, status_code=200, data=None):
        self.status_code = status_code
        self._data = [] if data is None else data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        return {"data": self._data}


class _Session:
    """Hands out canned responses in call order."""

    def __init__(self, responses):
        self._responses = list(responses)

    def get(self, url, timeout=None, params=None):
        return self._responses.pop(0)


class TestFetchCacheSafety(unittest.TestCase):
    def setUp(self):
        self.cache = Path(tempfile.mkdtemp()) / "nass.csv"

    def _seed_cache(self):
        from geocif.viz import nass

        pd.DataFrame([{
            "crop": "maize", "year": 2023, "Region": "Iowa",
            "state_fips": "19", "period": "YEAR", "ref_month": pd.NA,
            "is_final": True, "yield_bu_ac": 201.0,
            "load_time": "2024-01-12 12:00:00",
        }], columns=nass.COLUMNS).to_csv(self.cache, index=False)

    def test_empty_result_does_not_overwrite_cache(self):
        from geocif.viz import nass

        self._seed_cache()
        # Every crop-year answers 400 ("no published estimate") -> a
        # legitimately empty slice, which must leave the cache untouched.
        out = nass.fetch("k", [2030], crops=("maize",), cache=self.cache,
                         session=_Session([_Resp(status_code=400)]))
        self.assertTrue(out.empty)
        kept = pd.read_csv(self.cache)
        self.assertEqual(len(kept), 1)
        self.assertEqual(kept.loc[0, "Region"], "Iowa")

    def test_cache_write_error_propagates(self):
        from unittest import mock

        from geocif.viz import nass

        self._seed_cache()
        sess = _Session([_Resp(data=[_row()])])
        # A post-fetch failure must surface, NOT silently fall back to the
        # stale cache as if the API had been unreachable.
        with mock.patch.object(pd.DataFrame, "to_csv",
                               side_effect=PermissionError("read-only")):
            with self.assertRaises(PermissionError):
                nass.fetch("k", [2024], crops=("maize",), cache=self.cache,
                           session=sess)

    def test_successful_fetch_writes_cache(self):
        from geocif.viz import nass

        out = nass.fetch("k", [2024], crops=("maize",), cache=self.cache,
                         session=_Session([_Resp(data=[_row()])]))
        self.assertEqual(len(out), 1)
        self.assertEqual(out.loc[0, "Region"], "Iowa")
        self.assertEqual(int(out.loc[0, "ref_month"]), 8)
        written = pd.read_csv(self.cache)
        self.assertEqual(len(written), 1)
        self.assertEqual(float(written.loc[0, "yield_bu_ac"]), 180.0)

    def test_fetch_failure_falls_back_to_cache(self):
        from geocif.viz import nass

        self._seed_cache()

        class _Boom:
            def get(self, *args, **kwargs):
                raise requests.ConnectionError("no egress")

        out = nass.fetch("k", [2024], crops=("maize",), cache=self.cache,
                         session=_Boom())
        self.assertEqual(len(out), 1)
        self.assertEqual(out.loc[0, "Region"], "Iowa")


if __name__ == "__main__":
    unittest.main()
