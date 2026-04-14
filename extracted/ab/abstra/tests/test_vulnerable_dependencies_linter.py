import json
from unittest import TestCase

from abstra_internals.repositories.linter.rules.vulnerable_dependencies import (
    UpgradeAllPackages,
    VulnerableDependenciesFound,
    _highest_version,
    _parse_findings,
)


def _build_report(dependencies: list) -> str:
    return json.dumps({"dependencies": dependencies})


class TestHighestVersion(TestCase):
    def test_empty_list_returns_empty_string(self):
        self.assertEqual(_highest_version([]), "")

    def test_single_version(self):
        self.assertEqual(_highest_version(["1.2.3"]), "1.2.3")

    def test_picks_highest_among_multiple(self):
        self.assertEqual(
            _highest_version(["1.0.0", "2.3.1", "1.9.9"]),
            "2.3.1",
        )

    def test_ignores_invalid_versions(self):
        self.assertEqual(
            _highest_version(["not-a-version", "1.0.0", "garbage"]),
            "1.0.0",
        )

    def test_all_invalid_returns_empty(self):
        self.assertEqual(_highest_version(["foo", "bar"]), "")


class TestParseFindingsInputHandling(TestCase):
    def test_empty_stdout_returns_no_issues(self):
        self.assertEqual(_parse_findings(""), [])

    def test_whitespace_only_stdout_returns_no_issues(self):
        self.assertEqual(_parse_findings("   \n\t  "), [])

    def test_invalid_json_returns_no_issues(self):
        self.assertEqual(_parse_findings("not json"), [])

    def test_missing_dependencies_key_returns_no_issues(self):
        self.assertEqual(_parse_findings("{}"), [])

    def test_empty_dependencies_returns_no_issues(self):
        self.assertEqual(_parse_findings(_build_report([])), [])


class TestParseFindingsFiltering(TestCase):
    def test_skips_deps_without_vulnerabilities(self):
        """
        pip-audit lists ALL dependencies (vulnerable + safe) in its JSON.
        Safe deps have `vulns: []` and must not show up as issues.
        """
        report = _build_report(
            [
                {"name": "safe-pkg", "version": "1.0.0", "vulns": []},
                {
                    "name": "vuln-pkg",
                    "version": "1.0.0",
                    "vulns": [{"id": "CVE-1", "fix_versions": ["2.0.0"]}],
                },
            ]
        )
        issues = _parse_findings(report)
        self.assertEqual(len(issues), 1)
        label = issues[0].label
        self.assertIn("vuln-pkg", label)
        self.assertNotIn("safe-pkg", label)

    def test_skips_deps_without_name_or_version(self):
        report = _build_report(
            [
                {"name": "", "version": "1.0", "vulns": [{"id": "X"}]},
                {"name": "pkg", "version": "", "vulns": [{"id": "X"}]},
                {
                    "name": "valid",
                    "version": "1.0",
                    "vulns": [{"id": "X", "fix_versions": ["2.0"]}],
                },
            ]
        )
        issues = _parse_findings(report)
        self.assertEqual(len(issues), 1)
        self.assertIn("valid", issues[0].label)

    def test_returns_no_issues_when_all_deps_are_safe(self):
        report = _build_report(
            [
                {"name": "a", "version": "1.0", "vulns": []},
                {"name": "b", "version": "2.0", "vulns": []},
            ]
        )
        self.assertEqual(_parse_findings(report), [])


class TestParseFindingsGrouping(TestCase):
    def test_fixable_dep_becomes_single_grouped_issue(self):
        report = _build_report(
            [
                {
                    "name": "requests",
                    "version": "2.31.0",
                    "vulns": [{"id": "CVE-1", "fix_versions": ["2.33.0"]}],
                }
            ]
        )
        issues = _parse_findings(report)
        self.assertEqual(len(issues), 1)
        self.assertIn("requests 2.31.0 → 2.33.0", issues[0].label)

    def test_unfixable_dep_marked_with_no_update_available(self):
        report = _build_report(
            [
                {
                    "name": "abandoned",
                    "version": "1.0",
                    "vulns": [{"id": "CVE-1", "fix_versions": []}],
                }
            ]
        )
        issues = _parse_findings(report)
        self.assertEqual(len(issues), 1)
        self.assertIn("abandoned 1.0", issues[0].label)
        self.assertIn("no update available", issues[0].label)

    def test_mixed_fixable_and_unfixable_grouped_into_one_issue(self):
        report = _build_report(
            [
                {
                    "name": "fixable",
                    "version": "1.0",
                    "vulns": [{"id": "CVE-1", "fix_versions": ["2.0"]}],
                },
                {
                    "name": "unfixable",
                    "version": "1.0",
                    "vulns": [{"id": "CVE-2", "fix_versions": []}],
                },
            ]
        )
        issues = _parse_findings(report)
        self.assertEqual(len(issues), 1)
        label = issues[0].label
        self.assertIn("fixable 1.0 → 2.0", label)
        self.assertIn("unfixable 1.0", label)
        self.assertIn("no update available", label)

    def test_multiple_vulns_same_package_consolidated(self):
        """Two CVEs for the same package should collapse to one line."""
        report = _build_report(
            [
                {
                    "name": "pkg",
                    "version": "1.0",
                    "vulns": [
                        {"id": "CVE-1", "fix_versions": ["2.0"]},
                        {"id": "CVE-2", "fix_versions": ["2.0"]},
                    ],
                }
            ]
        )
        issues = _parse_findings(report)
        self.assertEqual(len(issues), 1)
        # Package should appear exactly once in the details
        self.assertEqual(issues[0].label.count("- pkg"), 1)

    def test_multiple_fix_versions_picks_highest(self):
        report = _build_report(
            [
                {
                    "name": "pkg",
                    "version": "1.0",
                    "vulns": [
                        {"id": "CVE-1", "fix_versions": ["2.0", "3.5", "2.9"]},
                    ],
                }
            ]
        )
        issues = _parse_findings(report)
        self.assertIn("pkg 1.0 → 3.5", issues[0].label)


class TestVulnerableDependenciesFoundLabel(TestCase):
    def test_singular_summary_when_total_is_one(self):
        issue = VulnerableDependenciesFound(
            fixable=[("requests", "1.0", "2.0")], unfixable=[]
        )
        self.assertTrue(issue.label.startswith("1 dependency has"))

    def test_plural_summary_when_total_is_more_than_one(self):
        issue = VulnerableDependenciesFound(
            fixable=[("a", "1", "2"), ("b", "1", "2")], unfixable=[]
        )
        self.assertTrue(issue.label.startswith("2 dependencies have"))

    def test_summary_counts_fixable_and_unfixable(self):
        issue = VulnerableDependenciesFound(
            fixable=[("a", "1", "2")],
            unfixable=[("b", "1"), ("c", "1")],
        )
        self.assertTrue(issue.label.startswith("3 dependencies have"))

    def test_first_line_is_summary_rest_are_details(self):
        """Label must be newline-separated so the frontend 'See more' works."""
        issue = VulnerableDependenciesFound(fixable=[("a", "1", "2")], unfixable=[])
        lines = issue.label.split("\n")
        self.assertEqual(len(lines), 2)
        self.assertIn("security updates available", lines[0])
        self.assertTrue(lines[1].startswith("- a"))


class TestVulnerableDependenciesFoundFixes(TestCase):
    def test_fixable_produces_single_upgrade_all_fix(self):
        issue = VulnerableDependenciesFound(
            fixable=[("a", "1", "2"), ("b", "1", "3")], unfixable=[]
        )
        self.assertEqual(len(issue.fixes), 1)
        self.assertIsInstance(issue.fixes[0], UpgradeAllPackages)

    def test_fix_includes_only_fixable_packages(self):
        issue = VulnerableDependenciesFound(
            fixable=[("a", "1", "2")],
            unfixable=[("b", "1")],
        )
        fix = issue.fixes[0]
        assert isinstance(fix, UpgradeAllPackages)
        self.assertEqual(fix.packages, [("a", "2")])

    def test_only_unfixable_means_no_fixes(self):
        issue = VulnerableDependenciesFound(fixable=[], unfixable=[("a", "1")])
        self.assertEqual(issue.fixes, [])
