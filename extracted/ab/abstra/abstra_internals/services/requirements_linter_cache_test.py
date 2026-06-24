"""Item 3: the linter import-analysis path reuses the package-distribution and
transitive-dependency caches (instead of bypassing them), guarded by a lock for
concurrent access, and the sidecar child refreshes those install-sensitive
caches on the package-install pass (run_after_package_install) — the editor-side
invalidate() hooks can't reach the child's separate process memory, and narrowing
to that pass avoids cold recomputes after unrelated config changes."""

import threading
import time
from pathlib import Path
from typing import List
from unittest import TestCase
from unittest.mock import patch

from abstra_internals.repositories.linter.models import LinterIssue, LinterRule
from abstra_internals.repositories.linter.repository import LocalLinterRepository
from abstra_internals.repositories.linter.rules import run_after_package_install
from abstra_internals.services.requirements import (
    _PackagesDistributionsCache,
    _TransitiveDependenciesCache,
    analyze_project_imports,
)
from tests.fixtures import BaseTest

_PKG_DIST = "abstra_internals.services.requirements.packages_distributions"


class PackagesDistributionsCacheTest(TestCase):
    def setUp(self):
        _PackagesDistributionsCache.invalidate()

    def tearDown(self):
        _PackagesDistributionsCache.invalidate()

    def test_get_caches_across_calls(self):
        with patch(_PKG_DIST, return_value={"a": ["a"]}) as mock:
            _PackagesDistributionsCache.get()
            _PackagesDistributionsCache.get()
        self.assertEqual(mock.call_count, 1)

    def test_invalidate_forces_recompute(self):
        with patch(_PKG_DIST, return_value={"a": ["a"]}) as mock:
            _PackagesDistributionsCache.get()
            _PackagesDistributionsCache.invalidate()
            _PackagesDistributionsCache.get()
        self.assertEqual(mock.call_count, 2)

    def test_concurrent_get_computes_once(self):
        call_count = [0]

        def slow():
            call_count[0] += 1
            time.sleep(0.05)
            return {"a": ["a"]}

        with patch(_PKG_DIST, side_effect=slow):
            threads = [
                threading.Thread(target=_PackagesDistributionsCache.get)
                for _ in range(8)
            ]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
        self.assertEqual(call_count[0], 1)


class AnalyzeProjectImportsCacheTest(BaseTest):
    def setUp(self):
        super().setUp()
        _PackagesDistributionsCache.invalidate()
        _TransitiveDependenciesCache.invalidate()

    def tearDown(self):
        _PackagesDistributionsCache.invalidate()
        _TransitiveDependenciesCache.invalidate()
        super().tearDown()

    def test_analyze_project_imports_reuses_packages_distributions_cache(self):
        script = self.controller.create_stage("tasklet", "S", "script.py")
        script.file_path.write_text("import pandas")
        with patch(_PKG_DIST, return_value={"pandas": ["pandas"]}) as mock:
            analyze_project_imports(skip_pypi_check=True, paths=[script.file_path])
            analyze_project_imports(skip_pypi_check=True, paths=[script.file_path])
        self.assertEqual(mock.call_count, 1)


class _NoopRule(LinterRule):
    label = "Noop"
    type = "info"

    def find_issues(self) -> List[LinterIssue]:
        return []


class InstallSensitiveCacheRefreshTest(BaseTest):
    """R2 (narrowed): ONLY the package-install pass (run_after_package_install —
    the editor's post-install signal) drops the child's install-sensitive caches.
    A generic unscoped pass (boot/abstra.json/.env) and scoped saves keep them
    warm, so an unrelated config change no longer forces a cold recompute on the
    next save."""

    def test_package_install_pass_invalidates(self):
        repo = LocalLinterRepository()
        # Stub the fan-out so the real (heavy/network) install-group rules don't
        # run; the invalidation trigger fires before _execute_rules.
        with patch.object(repo, "_execute_rules", return_value=([], [])):
            with patch.object(_PackagesDistributionsCache, "invalidate") as inv:
                repo.update_specific_checks(list(run_after_package_install))
        self.assertTrue(inv.called)

    def test_generic_unscoped_pass_does_not_invalidate(self):
        repo = LocalLinterRepository()
        with patch.object(_PackagesDistributionsCache, "invalidate") as inv:
            repo.update_specific_checks([_NoopRule()], paths=None)
        self.assertFalse(inv.called)

    def test_scoped_pass_does_not_invalidate(self):
        repo = LocalLinterRepository()
        with patch.object(_PackagesDistributionsCache, "invalidate") as inv:
            repo.update_specific_checks([_NoopRule()], paths=[Path("script.py")])
        self.assertFalse(inv.called)
