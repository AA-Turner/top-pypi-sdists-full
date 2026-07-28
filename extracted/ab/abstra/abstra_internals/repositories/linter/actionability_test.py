import inspect
import typing
import unittest
from pathlib import Path
from typing import List
from unittest.mock import MagicMock

from abstra_internals.repositories.linter.models import (
    LinterContractError,
    LinterFix,
    LinterIssue,
    assert_actionable,
)
from abstra_internals.repositories.linter.rules import rules
from abstra_internals.repositories.linter.rules.imports_analyzer import (
    InvalidImport,
    MissingPackageInRequirements,
)
from tests.fixtures import BaseTest


class _Fix(LinterFix):
    label = "do it"

    def fix(self):
        pass


class _Issue(LinterIssue):
    def __init__(self, fixes: List[LinterFix], fix_with_ai: bool = False) -> None:
        self.title = "synthetic issue"
        self.label = "synthetic issue"
        self.fixes = fixes
        self.fix_with_ai = fix_with_ai


class ActionabilityContractTest(unittest.TestCase):
    """assert_actionable encodes the editor's button predicate (fixes ||
    fixWithAi) — the single per-issue rule the meta-test enforces across every
    rule. It rejects the fixes=[] + fix_with_ai=False gap."""

    def test_fixless_issue_without_ai_is_rejected(self):
        with self.assertRaises(LinterContractError):
            assert_actionable("Synthetic", [_Issue([])])

    def test_fixless_issue_with_ai_is_allowed(self):
        assert_actionable("Synthetic", [_Issue([], fix_with_ai=True)])

    def test_issue_with_fix_is_allowed(self):
        assert_actionable("Synthetic", [_Issue([_Fix()])])

    def test_no_issues_is_allowed(self):
        assert_actionable("Synthetic", [])


def _all_subclasses(cls) -> set:
    found: set = set()
    stack = [cls]
    while stack:
        for sub in stack.pop().__subclasses__():
            if sub not in found:
                found.add(sub)
                stack.append(sub)
    return found


def _dummy_for_type(annotation):
    """A throwaway value of the right shape for one constructor argument.

    Scalars the issue labels format (str/int/Path/list/...) get real values so
    string interpolation and length/iteration work; anything domain-specific
    (a Stage, etc.) becomes a MagicMock, which tolerates arbitrary attribute
    access. We only need the constructor to run far enough to set self.fixes."""
    origin = typing.get_origin(annotation)
    if origin is typing.Union:  # Optional[T] / Union[T, ...]
        non_none = [a for a in typing.get_args(annotation) if a is not type(None)]
        return _dummy_for_type(non_none[0]) if non_none else None
    if annotation in (str, inspect.Parameter.empty):
        return "x"
    if annotation is int:
        return 1
    if annotation is float:
        return 1.0
    if annotation is bool:
        return False
    if annotation is Path:
        return Path("x")
    if annotation is SyntaxError:
        return SyntaxError("boom")
    if origin in (list, tuple, set) or annotation in (list, tuple, set):
        return ["x"]
    if origin is dict or annotation is dict:
        return {"x": "x"}
    return MagicMock()


def _instantiate_issue(issue_cls):
    sig = inspect.signature(issue_cls.__init__)
    args = []
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        if param.default is not inspect.Parameter.empty:
            args.append(param.default)
        else:
            args.append(_dummy_for_type(param.annotation))
    return issue_cls(*args)


class AllRegisteredRulesAreActionableTest(BaseTest):
    """CI guard for the per-issue invariants: every issue owned by a registered
    rule must (a) carry a fix or set fix_with_ai (a button), and (b) declare a
    mandatory severity `type` of "error" | "warning". Walking issue *classes*
    catches a violation the moment it is defined — no fixture has to reproduce
    the project state that emits it at runtime.

    Both severity and fix_with_ai live on the issue, so this needs no rule
    attribution: the predicates are entirely per-issue."""

    def test_every_registered_rule_issue_has_a_button(self):
        owned_modules = {type(rule).__module__ for rule in rules}

        checked: list = []
        uncheckable: list = []
        for issue_cls in _all_subclasses(LinterIssue):
            if issue_cls.__module__ not in owned_modules:
                # Not owned by a registered rule (test doubles, unregistered
                # rules like vulnerable_dependencies) — out of scope.
                continue
            try:
                checked.append((issue_cls.__module__, _instantiate_issue(issue_cls)))
            except Exception as e:  # noqa: BLE001 - surfaced via the assertion below
                uncheckable.append(
                    f"{issue_cls.__module__}.{issue_cls.__name__}: {e!r}"
                )

        # Coverage guard: if a must-check issue class can't be built here, the
        # test isn't actually verifying it — extend _dummy_for_type rather than
        # let it slip through silently.
        self.assertEqual(
            uncheckable,
            [],
            "Could not instantiate these issue classes to check actionability:\n"
            + "\n".join(uncheckable),
        )
        self.assertTrue(checked, "no issue classes were checked — is the walk broken?")

        for module, issue in checked:
            # Raises LinterContractError (failing the test) naming the module and
            # issue if it has no fix and fix_with_ai is False.
            assert_actionable(module, [issue])
            # Severity is mandatory and per-issue: every issue must declare it.
            self.assertIn(
                getattr(issue, "type", None),
                ("error", "warning"),
                f"{module}: issue {issue.make_label()!r} must set "
                f"type = 'error' | 'warning' (got "
                f"{getattr(issue, 'type', None)!r}).",
            )
            title = getattr(issue, "title", None)
            self.assertTrue(
                isinstance(title, str) and title.strip(),
                f"{module}: issue {issue.make_label()!r} must set a non-empty "
                f"title (got {title!r}).",
            )


class ActionabilityRegressionTest(unittest.TestCase):
    """The imports analyzer is why fix_with_ai belongs on the issue: one rule,
    heterogeneous issues — InvalidImport needs AI, the others are deterministic."""

    def test_invalid_import_is_actionable_via_ai(self):
        self.assertTrue(InvalidImport("foo", "main.py", 1).fix_with_ai)

    def test_deterministically_fixable_issue_is_not_ai(self):
        # The precision win: this used to inherit the rule-wide AI button.
        issue = MissingPackageInRequirements("foo", "foo", "main.py", 1)
        self.assertFalse(issue.fix_with_ai)
        self.assertTrue(issue.fixes)


if __name__ == "__main__":
    unittest.main()
