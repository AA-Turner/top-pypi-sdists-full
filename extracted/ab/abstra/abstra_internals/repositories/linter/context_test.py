"""Items 1/2: the per-pass LintContext loads the project once (was once per
project-reading rule) and gives serial and threaded fan-outs identical results.
"""

from unittest.mock import patch

from abstra_internals.repositories.linter.repository import LocalLinterRepository
from abstra_internals.repositories.linter.rules.abstra_dir_reference import (
    AbstraDirReference,
)
from abstra_internals.repositories.linter.rules.big_py_files import BigPyFiles
from abstra_internals.repositories.linter.rules.internal_page_reference import (
    InternalPageReference,
)
from abstra_internals.repositories.linter.rules.missing_env import MissingEnv
from abstra_internals.repositories.linter.rules.syntax_errors import SyntaxErrors
from abstra_internals.repositories.project.project import LocalProjectRepository
from tests.fixtures import BaseTest


def _normalize(checks):
    dicts = [c.to_dict() for c in checks]
    for d in dicts:
        d["issues"] = sorted(d["issues"], key=lambda i: i["label"])
    return sorted(dicts, key=lambda d: (d["type"], d["name"]))


class LintContextTest(BaseTest):
    def _project_loaders(self):
        return [
            SyntaxErrors(),
            BigPyFiles(),
            AbstraDirReference(),
            InternalPageReference(),
            MissingEnv(),
        ]

    def test_project_loaded_once_per_pass(self):
        script = self.controller.create_stage("tasklet", "S", "script.py")
        script.file_path.write_text("import os\n")

        original = LocalProjectRepository.load
        count = [0]

        def counting(self):
            count[0] += 1
            return original(self)

        repo = LocalLinterRepository()
        with patch.object(LocalProjectRepository, "load", counting):
            repo.update_specific_checks(
                self._project_loaders(), paths=[script.file_path]
            )

        # One shared load for the whole pass instead of one per project-rule.
        self.assertEqual(count[0], 1)

    def test_serial_equals_threaded(self):
        a = self.controller.create_stage("tasklet", "A", "a.py")
        a.file_path.write_text("print('a'")  # syntax error
        big = self.controller.create_stage("tasklet", "Big", "big.py")
        big.file_path.write_text("x = 1\n" * 1001)

        rules = self._project_loaders()

        threaded = LocalLinterRepository(serial=False)
        threaded_state = _normalize(threaded.update_specific_checks(rules))

        serial = LocalLinterRepository(serial=True)
        serial_state = _normalize(serial.update_specific_checks(rules))

        self.assertEqual(threaded_state, serial_state)

    def test_context_matches_standalone_find_issues(self):
        a = self.controller.create_stage("tasklet", "A", "a.py")
        a.file_path.write_text("print('a'")  # syntax error

        # Standalone (no context) — the path unit tests exercise.
        standalone = {i.label for i in SyntaxErrors().find_issues()}

        # Through a full repository pass (context injected).
        repo = LocalLinterRepository()
        repo.update_specific_checks([SyntaxErrors()])
        check = next(c for c in repo.checks if c.name == "SyntaxErrors")
        through_repo = {i.label for i in check.issues}

        self.assertEqual(standalone, through_repo)
