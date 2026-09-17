# -*- coding: utf-8 -*-
"""Tests for geocif/phenology/refresh.py (DESIGN.md section 5).

``refresh_inputs`` is the one place the season monitor reaches out to the
network, so the properties that matter are: it never raises, both guards stop
it, and it calls the real geoprepare dataset modules with the params object
those modules expect. The geoprepare modules are stubbed through
``sys.modules`` -- ``refresh`` imports them with :mod:`importlib` at call time
precisely so this is possible without touching the network or /gpfs.
"""
import configparser
import datetime as dt
import os
import sys
import time
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock

from geocif.phenology import refresh


class _FakeGeoDownload:
    """Stand-in for ``geoprepare.geodownload.GeoDownload``."""

    instances: list = []

    def __init__(self, cfg_list):
        self.cfg_list = list(cfg_list)
        self.parser = None
        self.parsed_sections: list = []
        self.start_year = 1981
        self.end_year = 2025
        _FakeGeoDownload.instances.append(self)

    def parse_config(self, section="DEFAULT"):
        self.parsed_sections.append(section)
        self.parser = _FakeGeoDownload.parser_factory()
        self.redo_last_year = False


class _FakeDataset(types.ModuleType):
    """Stand-in for ``geoprepare.datasets.CHIRPS`` / ``CHIRPS_GEFS``."""

    def __init__(self, name, error=None):
        super().__init__(name)
        self.calls: list = []
        self.error = error

    def run(self, params):
        self.calls.append(params)
        if self.error is not None:
            raise self.error


class RefreshFixture(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

        self.dir_intermed = self.root / "intermed"
        self.dir_intermed.mkdir(parents=True, exist_ok=True)

        def _parser_factory():
            parser = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation(),
                inline_comment_prefixes=(";",),
            )
            parser.read_dict({
                "PATHS": {"dir_intermed": str(self.dir_intermed)},
                "CHIRPS": {"fill_value": "-2147483648", "version": "v3", "disagg": "sat"},
                "CHIRPS-GEFS": {"data_dir": "/products/CHIRPS-GEFS/v3"},
            })
            return parser

        _FakeGeoDownload.parser_factory = staticmethod(_parser_factory)
        _FakeGeoDownload.instances = []

        self.chirps = _FakeDataset("geoprepare.datasets.CHIRPS")
        self.gefs = _FakeDataset("geoprepare.datasets.CHIRPS_GEFS")
        geodownload = types.ModuleType("geoprepare.geodownload")
        geodownload.GeoDownload = _FakeGeoDownload

        patcher = mock.patch.dict(
            sys.modules,
            {
                "geoprepare.geodownload": geodownload,
                "geoprepare.datasets.CHIRPS": self.chirps,
                "geoprepare.datasets.CHIRPS_GEFS": self.gefs,
            },
        )
        patcher.start()
        self.addCleanup(patcher.stop)

        # Default: nothing else is downloading.
        running = mock.patch.object(refresh, "download_running", return_value=False)
        running.start()
        self.addCleanup(running.stop)

        self.cfg = ["geobase.txt", "countries.txt", "crops.txt", "geocif.txt"]

    @property
    def lock(self):
        return self.dir_intermed / refresh.LOCK_NAME


class TestDefaultYears(unittest.TestCase):
    def test_january_and_february_also_refresh_the_previous_year(self):
        self.assertEqual(refresh._default_years(dt.date(2026, 1, 15)), [2025, 2026])
        self.assertEqual(refresh._default_years(dt.date(2026, 2, 28)), [2025, 2026])

    def test_march_onwards_refreshes_only_the_current_year(self):
        self.assertEqual(refresh._default_years(dt.date(2026, 3, 1)), [2026])
        self.assertEqual(refresh._default_years(dt.date(2026, 9, 16)), [2026])


class TestBuildParams(RefreshFixture):
    def test_params_carry_the_geodownload_attribute_set(self):
        params = refresh.build_params(self.cfg, years=[2025, 2026])

        self.assertEqual(params.cfg_list, self.cfg)
        self.assertEqual(params.parsed_sections, ["DEFAULT"])
        self.assertEqual(params.fill_value, -2147483648)
        self.assertEqual(params.version, "v3")
        self.assertEqual(params.disagg, "sat")
        self.assertEqual(params.data_dir, "/products/CHIRPS-GEFS/v3")
        self.assertFalse(params.process_only)
        # years restrict the DEFAULT 1981-2025 span to exactly what we asked for
        self.assertEqual((params.start_year, params.end_year), (2025, 2026))

    def test_years_default_to_the_current_year(self):
        params = refresh.build_params(self.cfg)
        expected = refresh._default_years()
        self.assertEqual((params.start_year, params.end_year), (expected[0], expected[-1]))


class TestRefreshInputs(RefreshFixture):
    def test_happy_path_calls_both_dataset_modules(self):
        result = refresh.refresh_inputs(self.cfg, datasets=("CHIRPS", "CHIRPS-GEFS"))

        self.assertEqual(sorted(result), ["CHIRPS", "CHIRPS-GEFS"])
        for name in result:
            self.assertTrue(result[name]["ok"], result[name])
            self.assertIsNone(result[name]["error"])
            self.assertFalse(result[name]["skipped"])
            self.assertGreaterEqual(result[name]["seconds"], 0.0)

        self.assertEqual(len(self.chirps.calls), 1)
        self.assertEqual(len(self.gefs.calls), 1)
        # Both modules get the SAME params object geodownload would have built.
        self.assertIs(self.chirps.calls[0], self.gefs.calls[0])
        self.assertTrue(self.lock.is_file())

    def test_empty_dataset_list_disables_the_refresh(self):
        self.assertEqual(refresh.refresh_inputs(self.cfg, datasets=()), {})
        self.assertEqual(self.chirps.calls, [])
        self.assertFalse(self.lock.exists())

    def test_a_failing_dataset_is_reported_not_raised(self):
        self.gefs.error = RuntimeError("source is down")
        result = refresh.refresh_inputs(self.cfg)

        self.assertTrue(result["CHIRPS"]["ok"])
        self.assertFalse(result["CHIRPS-GEFS"]["ok"])
        self.assertIn("source is down", result["CHIRPS-GEFS"]["error"])
        self.assertFalse(result["CHIRPS-GEFS"]["skipped"])

    def test_unknown_dataset_is_reported_not_raised(self):
        result = refresh.refresh_inputs(self.cfg, datasets=("CHIRPS", "NOT-A-DATASET"))
        self.assertTrue(result["CHIRPS"]["ok"])
        self.assertFalse(result["NOT-A-DATASET"]["ok"])
        self.assertIn("unknown dataset", result["NOT-A-DATASET"]["error"])

    def test_a_config_failure_is_reported_not_raised(self):
        with mock.patch.object(
            refresh, "build_params", side_effect=ValueError("no such section")
        ):
            result = refresh.refresh_inputs(self.cfg)
        self.assertFalse(result["CHIRPS"]["ok"])
        self.assertIn("no such section", result["CHIRPS"]["error"])
        self.assertEqual(self.chirps.calls, [])

    def test_a_running_download_skips_everything(self):
        with mock.patch.object(refresh, "download_running", return_value=True):
            result = refresh.refresh_inputs(self.cfg)

        for name in ("CHIRPS", "CHIRPS-GEFS"):
            self.assertFalse(result[name]["ok"])
            self.assertTrue(result[name]["skipped"])
            self.assertIn("download is running", result[name]["error"])
        self.assertEqual(self.chirps.calls, [])
        self.assertFalse(self.lock.exists())

    def test_a_fresh_lock_skips_everything(self):
        self.lock.write_text("held", encoding="utf-8")
        result = refresh.refresh_inputs(self.cfg)

        for name in ("CHIRPS", "CHIRPS-GEFS"):
            self.assertTrue(result[name]["skipped"])
            self.assertIn("lock", result[name]["error"])
        self.assertEqual(self.chirps.calls, [])

    def test_a_stale_lock_does_not_block(self):
        self.lock.write_text("held", encoding="utf-8")
        # 7 h old > LOCK_MAX_AGE_HOURS (6 h) -> stale.
        stale = time.time() - 7 * 3600
        os.utime(self.lock, (stale, stale))

        result = refresh.refresh_inputs(self.cfg)
        self.assertTrue(result["CHIRPS"]["ok"])
        self.assertEqual(len(self.chirps.calls), 1)
        # The lock was rewritten, so it is fresh again.
        self.assertTrue(refresh.lock_is_fresh(self.lock))


class TestGuardHelpers(unittest.TestCase):
    def test_lock_is_fresh_handles_a_missing_file(self):
        with TemporaryDirectory() as tmp:
            self.assertFalse(refresh.lock_is_fresh(Path(tmp) / "nope.lock"))

    def test_download_running_is_false_without_pgrep(self):
        # pgrep does not exist on Windows; a missing binary must NOT be read as
        # "a download is running", or the monitor would never refresh there.
        with mock.patch.object(refresh.shutil, "which", return_value=None):
            self.assertFalse(refresh.download_running())

    def test_download_running_reads_a_pgrep_match(self):
        completed = mock.Mock(returncode=0, stdout="4242 python -c geodownload.run(cfg)\n")
        with mock.patch.object(refresh.shutil, "which", return_value="/usr/bin/pgrep"), \
                mock.patch.object(refresh.subprocess, "run", return_value=completed):
            self.assertTrue(refresh.download_running())

    def test_download_running_is_false_on_no_match(self):
        completed = mock.Mock(returncode=1, stdout="")
        with mock.patch.object(refresh.shutil, "which", return_value="/usr/bin/pgrep"), \
                mock.patch.object(refresh.subprocess, "run", return_value=completed):
            self.assertFalse(refresh.download_running())

    def test_download_running_is_false_when_pgrep_blows_up(self):
        with mock.patch.object(refresh.shutil, "which", return_value="/usr/bin/pgrep"), \
                mock.patch.object(refresh.subprocess, "run", side_effect=OSError("boom")):
            self.assertFalse(refresh.download_running())


if __name__ == "__main__":
    unittest.main()
