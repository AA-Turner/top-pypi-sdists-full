from typing import TYPE_CHECKING, Type

from abstra_internals.repositories.linter.models import (
    PathScopedLinterRule,
    linter_path_key,
)
from abstra_internals.repositories.linter.repository import LocalLinterRepository
from abstra_internals.repositories.linter.rules.css_syntax import CssSyntax
from abstra_internals.repositories.linter.rules.html_and_jinja2_syntax import (
    HtmlAndJinja2Syntax,
)
from abstra_internals.repositories.linter.rules.js_syntax import JsSyntax
from tests.fixtures import BaseTest

# Typed as BaseTest so pyright resolves the TestCase API on the mixin; object at
# runtime so the mixin itself is not collected as a test (concrete classes add
# BaseTest).
if TYPE_CHECKING:
    _MixinBase = BaseTest
else:
    _MixinBase = object


def _normalize(checks):
    dicts = [c.to_dict() for c in checks]
    for d in dicts:
        d["issues"] = sorted(d["issues"], key=lambda i: i["label"])
    return sorted(dicts, key=lambda d: d["name"])


class _FrontScopedMixin(_MixinBase):
    """HTML/CSS/JS rules must be path-scoped: a save re-checks only the saved
    file, and the merge (which keeps issues whose path is outside the scope)
    relies on every issue carrying issue.path == linter_path_key(file). Without
    that, fixing a file would never clear its stale errors."""

    rule_cls: Type[PathScopedLinterRule]
    suffix: str
    good: str
    bad: str

    def _check(self, repo, rule):
        return next(c for c in repo.checks if c.name == rule.name)

    def test_is_path_scoped(self):
        self.assertIsInstance(self.rule_cls(), PathScopedLinterRule)

    def test_full_run_sets_path_on_every_issue(self):
        bad_file = self.root / f"bad{self.suffix}"
        bad_file.write_text(self.bad)
        rule = self.rule_cls()
        issues = rule.find_issues()
        self.assertGreater(len(issues), 0)
        for issue in issues:
            self.assertEqual(issue.path, linter_path_key(bad_file))

    def test_scoped_returns_only_the_saved_file(self):
        other = self.root / f"other{self.suffix}"
        other.write_text(self.bad)
        bad_file = self.root / f"bad{self.suffix}"
        bad_file.write_text(self.bad)

        rule = self.rule_cls()
        issues = rule.find_issues(path=bad_file)
        self.assertGreater(len(issues), 0)
        self.assertEqual({i.path for i in issues}, {linter_path_key(bad_file)})

    def test_scoped_wrong_suffix_returns_empty(self):
        rule = self.rule_cls()
        self.assertEqual(rule.find_issues(path=self.root / "script.py"), [])

    def test_full_equals_scoped_plus_merge(self):
        (self.root / f"good{self.suffix}").write_text(self.good)
        bad1 = self.root / f"bad1{self.suffix}"
        bad1.write_text(self.bad)
        bad2 = self.root / f"bad2{self.suffix}"
        bad2.write_text(self.bad)

        rule = self.rule_cls()
        repo = LocalLinterRepository()
        repo.update_specific_checks([rule])  # full seed: bad1 + bad2 flagged
        seeded = {i.path for i in self._check(repo, rule).issues}
        self.assertEqual(seeded, {linter_path_key(bad1), linter_path_key(bad2)})

        # Fix bad1, re-lint only bad1 (scoped) → merge keeps bad2, drops bad1.
        bad1.write_text(self.good)
        repo.update_specific_checks([rule], paths=[bad1])

        fresh = LocalLinterRepository()
        fresh.update_specific_checks([rule])  # full run on the edited tree

        self.assertEqual(_normalize(repo.checks), _normalize(fresh.checks))
        remaining = {i.path for i in self._check(repo, rule).issues}
        self.assertEqual(remaining, {linter_path_key(bad2)})


class CssScopedTest(_FrontScopedMixin, BaseTest):
    rule_cls = CssSyntax
    suffix = ".css"
    good = "body { color: red; margin: 0; }"
    bad = "body { : red; }"


class HtmlScopedTest(_FrontScopedMixin, BaseTest):
    rule_cls = HtmlAndJinja2Syntax
    suffix = ".html"
    good = "<div><p>Hello</p></div>"
    bad = "<div><p>unclosed<span></div>"


class JsScopedTest(_FrontScopedMixin, BaseTest):
    rule_cls = JsSyntax
    suffix = ".js"
    good = "function foo() { return 1; }"
    bad = "function foo( { return 1; }"
