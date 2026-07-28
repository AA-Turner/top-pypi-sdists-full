import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from abstra_internals.controllers.execution import snippet_packages


class SnippetPackagesTest(unittest.TestCase):
    def setUp(self):
        self.overlay = Path(tempfile.mkdtemp()) / "overlay"
        self._patch = mock.patch.object(
            snippet_packages, "SMARTCHAT_PACKAGES_FOLDER", str(self.overlay)
        )
        self._patch.start()
        self._orig_path = list(sys.path)

    def tearDown(self):
        self._patch.stop()
        sys.path[:] = self._orig_path

    def test_dir_uses_env_var_and_is_created(self):
        p = snippet_packages.get_smartchat_packages_dir()
        self.assertEqual(p, self.overlay)
        self.assertTrue(p.is_dir())

    def test_empty_overlay_is_not_added_to_path(self):
        # Empty overlay → nothing to import, nothing can leak → stay off sys.path
        # so the executor is not needlessly recycled.
        self.assertFalse(snippet_packages.add_smartchat_packages_to_path())
        self.assertNotIn(str(self.overlay), sys.path)

    def test_nonempty_overlay_is_added_once(self):
        snippet_packages.get_smartchat_packages_dir()
        (self.overlay / "some_pkg").mkdir(parents=True)
        self.assertTrue(snippet_packages.add_smartchat_packages_to_path())
        self.assertIn(str(self.overlay), sys.path)
        # idempotent — no duplicate entries on repeated calls
        self.assertTrue(snippet_packages.add_smartchat_packages_to_path())
        self.assertEqual(sys.path.count(str(self.overlay)), 1)

    def test_ensure_requirements_is_noop_when_empty(self):
        # No requirements → never shells out to pip (and must not raise).
        snippet_packages.ensure_snippet_requirements(None)
        snippet_packages.ensure_snippet_requirements([])


if __name__ == "__main__":
    unittest.main()
