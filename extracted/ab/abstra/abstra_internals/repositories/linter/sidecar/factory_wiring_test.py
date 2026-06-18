"""Wiring tests for the ABSTRA_LINTER_SIDECAR kill-switch (PR1, TDD).

Default ON: editor factories build SidecarLinterRepository. "0"/"false"
fall back to the untouched in-process LocalLinterRepository (rollback path).
The flag is read at factory call time, not at import time.
"""

import os
import unittest
from unittest.mock import patch

from abstra_internals.environment import linter_sidecar_enabled
from abstra_internals.repositories.factory import build_editor_repositories
from abstra_internals.repositories.linter.repository import LocalLinterRepository
from abstra_internals.repositories.linter.sidecar.client import (
    SidecarLinterRepository,
)
from tests.fixtures import clear_dir, init_dir


class LinterSidecarEnabledTest(unittest.TestCase):
    def test_default_is_enabled(self):
        env = {k: v for k, v in os.environ.items() if k != "ABSTRA_LINTER_SIDECAR"}
        with patch.dict(os.environ, env, clear=True):
            self.assertTrue(linter_sidecar_enabled())

    def test_disabled_values(self):
        for value in ("0", "false", "False", "FALSE"):
            with patch.dict(os.environ, {"ABSTRA_LINTER_SIDECAR": value}):
                self.assertFalse(linter_sidecar_enabled(), value)

    def test_enabled_values(self):
        for value in ("1", "true", "True"):
            with patch.dict(os.environ, {"ABSTRA_LINTER_SIDECAR": value}):
                self.assertTrue(linter_sidecar_enabled(), value)


class EditorFactoryWiringTest(unittest.TestCase):
    def setUp(self):
        self.root = init_dir()

    def tearDown(self):
        clear_dir(self.root)

    def test_default_builds_sidecar_repository(self):
        env = {k: v for k, v in os.environ.items() if k != "ABSTRA_LINTER_SIDECAR"}
        with patch.dict(os.environ, env, clear=True):
            repositories = build_editor_repositories()
        self.assertIsInstance(repositories.linter, SidecarLinterRepository)

    def test_kill_switch_builds_local_repository(self):
        with patch.dict(os.environ, {"ABSTRA_LINTER_SIDECAR": "0"}):
            repositories = build_editor_repositories()
        self.assertIsInstance(repositories.linter, LocalLinterRepository)
        self.assertNotIsInstance(repositories.linter, SidecarLinterRepository)


if __name__ == "__main__":
    unittest.main()
