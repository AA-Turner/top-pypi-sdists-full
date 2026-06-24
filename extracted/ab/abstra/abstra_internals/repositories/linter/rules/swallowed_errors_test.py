import contextlib
import io
from typing import TYPE_CHECKING, Type
from unittest.mock import patch

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter.models import LinterRule
from abstra_internals.repositories.linter.rules.abstra_dir_reference import (
    AbstraDirReference,
)
from abstra_internals.repositories.linter.rules.deprecated_functions import (
    DeprecatedFunctionUsage,
)
from abstra_internals.repositories.linter.rules.internal_page_reference import (
    InternalPageReference,
)
from abstra_internals.repositories.linter.rules.main_block_in_stage import (
    MainBlockInStage,
)
from abstra_internals.utils.ast_cache import ASTCache
from tests.fixtures import BaseTest

# Typed as BaseTest so pyright resolves the TestCase API on the mixin; object at
# runtime so the mixin itself is not collected as a test (concrete classes add
# BaseTest).
if TYPE_CHECKING:
    _MixinBase = BaseTest
else:
    _MixinBase = object


class _SwallowedErrorsMixin(_MixinBase):
    """Per-file processing errors must be handled silently (deleted/unreadable
    files are normal mid-pass) and real bugs logged via AbstraLogger — never
    printed to stdout (which corrupts the sidecar's JSON-RPC framing on fd 1)."""

    rule_cls: Type[LinterRule]

    def setUp(self):
        super().setUp()
        # At least one entrypoint/py file so the rule's per-file loop executes.
        stage = self.controller.create_stage("tasklet", "New script", "script.py")
        stage.file_path.write_text("print('ok')\n")

    def _make_rule(self):
        return self.rule_cls()

    def test_deleted_file_midpass_returns_no_issue_and_no_crash(self):
        rule = self._make_rule()
        with patch.object(ASTCache, "get", side_effect=FileNotFoundError()):
            issues = rule.find_issues()
        self.assertEqual(issues, [])

    def test_no_print_to_stdout_on_error(self):
        rule = self._make_rule()
        buf = io.StringIO()
        with patch.object(ASTCache, "get", side_effect=Exception("boom")):
            with contextlib.redirect_stdout(buf):
                rule.find_issues()
        self.assertEqual(buf.getvalue(), "")

    def test_real_exception_is_logged(self):
        rule = self._make_rule()
        with patch.object(ASTCache, "get", side_effect=Exception("boom")):
            with patch.object(AbstraLogger, "error") as mock_error:
                with patch.object(AbstraLogger, "capture_exception"):
                    rule.find_issues()
        self.assertTrue(mock_error.called)


class AbstraDirReferenceSwallowedErrorsTest(_SwallowedErrorsMixin, BaseTest):
    rule_cls = AbstraDirReference


class InternalPageReferenceSwallowedErrorsTest(_SwallowedErrorsMixin, BaseTest):
    rule_cls = InternalPageReference


class DeprecatedFunctionUsageSwallowedErrorsTest(_SwallowedErrorsMixin, BaseTest):
    rule_cls = DeprecatedFunctionUsage


class MainBlockInStageSwallowedErrorsTest(_SwallowedErrorsMixin, BaseTest):
    rule_cls = MainBlockInStage
