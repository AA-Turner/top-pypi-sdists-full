"""Equivalence tests: LocalLinterRepository (in-process) vs
SidecarLinterRepository (real child) must produce identical checks (PR1, TDD).

This is the core non-regression proof of the sidecar move: same project, same
rules, two execution models, byte-equal serialized results — for full subset
runs, path-scoped merge re-runs, and a real on-disk fix applied by name.

The rule subset is restricted to deterministic, network-free rules (no PyPI,
no pyrefly). A fake rule cannot cross the process boundary, so only real
registered rules are used. EnvInBundle stays in the subset for serialization
coverage, but its issue count is environment-dependent (global gitignore may
ignore .env), so no absolute assertion is made on it — only Local×Sidecar
equality.
"""

import os
import unittest
from unittest.mock import Mock

import pytest

from abstra_internals.controllers.main import MainController
from abstra_internals.repositories.factory import build_editor_repositories
from abstra_internals.repositories.linter.repository import LocalLinterRepository
from abstra_internals.repositories.linter.rules import rules as ALL_RULES
from abstra_internals.repositories.linter.sidecar.client import (
    SidecarLinterRepository,
)
from tests.fixtures import clear_dir, init_dir

# method="signal": the thread-based timer (a non-daemon thread) deadlocks
# BaseTest.tearDown's wait_non_daemon_threads — pre-existing interaction.
pytestmark = pytest.mark.timeout(120, method="signal")

SUBSET_NAMES = [
    "SyntaxErrors",
    "BigPyFiles",
    "CssSyntax",
    "HtmlAndJinja2Syntax",
    "EnvInBundle",
    "MissingAbstraInRequirements",
]


def _subset():
    by_name = {r.name: r for r in ALL_RULES}
    return [by_name[name] for name in SUBSET_NAMES]


def _rule(name):
    return next(r for r in ALL_RULES if r.name == name)


def _normalize(checks):
    """Serialized, order-insensitive view of a list of checks."""
    dicts = [c.to_dict() for c in checks]
    for d in dicts:
        d["issues"] = sorted(d["issues"], key=lambda i: i["label"])
    return sorted(dicts, key=lambda d: (d["type"], d["name"]))


class EquivalenceTest(unittest.TestCase):
    """Light project fixture: init_dir + MainController (for create_stage),
    deliberately WITHOUT BaseTest's consumer/executor pool — the pool's warmup
    children asynchronously rewrite requirements.txt/.env/.gitignore
    (MainController.__init__ in each executor) and would race these fixtures.
    Equivalence requires an exclusive project directory."""

    def setUp(self):
        self._old_bundled = os.environ.get("ABSTRA_RUNNING_IN_BUNDLED_APP")
        os.environ["ABSTRA_RUNNING_IN_BUNDLED_APP"] = "1"
        self.root = init_dir()
        self.repositories = build_editor_repositories()
        self.controller = MainController(self.repositories)

    def tearDown(self):
        clear_dir(self.root)
        if self._old_bundled is None:
            os.environ.pop("ABSTRA_RUNNING_IN_BUNDLED_APP", None)
        else:
            os.environ["ABSTRA_RUNNING_IN_BUNDLED_APP"] = self._old_bundled

    def _build_fixture(self):
        a = self.controller.create_stage("tasklet", "A", "broken_a.py")
        a.file_path.write_text("print('a'")
        b = self.controller.create_stage("tasklet", "B", "broken_b.py")
        b.file_path.write_text("def x(:")
        big = self.controller.create_stage("tasklet", "Big", "big.py")
        big.file_path.write_text("x = 1\n" * 1001)
        (self.root / "bad.css").write_text("body { : red; }")
        (self.root / "bad.html").write_text("{% endif %}")
        (self.root / ".env").write_text("A=1\n")
        (self.root / "requirements.txt").write_text("")
        return a, b

    def _make_sidecar(self):
        repo = SidecarLinterRepository(
            request_timeout=90.0,
            backoff_schedule=[0.1, 0.1],
            is_web=False,
            exiter=Mock(),
            diagnostics_handler=lambda code: [],
        )
        self.addCleanup(repo.stop)
        return repo

    def test_full_subset_run_is_equivalent(self):
        self._build_fixture()

        local = LocalLinterRepository()
        local_state = _normalize(local.update_specific_checks(_subset()))

        sidecar = self._make_sidecar()
        sidecar_state = _normalize(sidecar.update_specific_checks(_subset()))

        self.assertEqual(local_state, sidecar_state)

        # Sanity: the fixture actually fires the deterministic rules — an
        # empty==empty comparison would prove nothing.
        counts = {d["name"]: len(d["issues"]) for d in local_state}
        self.assertEqual(counts["SyntaxErrors"], 2)
        self.assertEqual(counts["BigPyFiles"], 1)
        self.assertEqual(counts["CssSyntax"], 1)
        self.assertEqual(counts["HtmlAndJinja2Syntax"], 1)
        self.assertEqual(counts["MissingAbstraInRequirements"], 1)

    def test_scoped_rerun_merges_equivalently(self):
        a, b = self._build_fixture()
        syntax = _rule("SyntaxErrors")

        # Local world: full subset seed, fix a, scoped re-run on a only
        local = LocalLinterRepository()
        local.update_specific_checks(_subset())
        a.file_path.write_text("print('a')")
        local.update_specific_checks([syntax], paths=[a.file_path])
        local_state = _normalize(local.checks)

        syntax_local = next(d for d in local_state if d["name"] == "SyntaxErrors")
        self.assertEqual(len(syntax_local["issues"]), 1)
        self.assertIn("broken_b.py", syntax_local["issues"][0]["label"])

        # Reset the project to the broken state and replay in the sidecar world
        a.file_path.write_text("print('a'")

        sidecar = self._make_sidecar()
        sidecar.update_specific_checks(_subset())
        a.file_path.write_text("print('a')")
        sidecar.update_specific_checks([syntax], paths=[a.file_path])
        sidecar_state = _normalize(sidecar.checks)

        self.assertEqual(local_state, sidecar_state)

    def test_apply_fix_by_name_is_equivalent_on_disk_and_in_checks(self):
        self._build_fixture()
        requirements = self.root / "requirements.txt"

        def _post_fix_check(repo):
            return next(
                c.to_dict()
                for c in repo.checks
                if c.name == "MissingAbstraInRequirements"
            )

        # Local world
        local = LocalLinterRepository()
        local.update_specific_checks(_subset())
        ok_local = local.fix_issue_in_codebase(
            "MissingAbstraInRequirements", "AddAbstraToRequirements"
        )
        req_local = requirements.read_text()
        post_local = _post_fix_check(local)

        # Reset and replay in the sidecar world
        requirements.write_text("")

        sidecar = self._make_sidecar()
        sidecar.update_specific_checks(_subset())
        ok_sidecar = sidecar.fix_issue_in_codebase(
            "MissingAbstraInRequirements", "AddAbstraToRequirements"
        )
        req_sidecar = requirements.read_text()
        post_sidecar = _post_fix_check(sidecar)

        self.assertTrue(ok_local)
        self.assertTrue(ok_sidecar)
        self.assertIn("abstra==", req_local)
        self.assertEqual(req_local, req_sidecar)
        self.assertEqual(post_local, post_sidecar)
        self.assertEqual(post_local["issues"], [])


if __name__ == "__main__":
    unittest.main()
