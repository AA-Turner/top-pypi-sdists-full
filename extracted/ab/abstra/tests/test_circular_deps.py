from pathlib import Path
from unittest import TestCase

from circular_imports import cycles_in_path

_PROJECT_ROOT = str(Path(__file__).parent.parent.resolve())


class TestCircularDeps(TestCase):
    def test_no_cycles(self):
        cycles = cycles_in_path(_PROJECT_ROOT, ".venv,build,.pyrefly_buffer")
        # Filter out false positives: single-file "cycles" caused by
        # file and directory having the same name (e.g., connectors.py and connectors/)
        real_cycles = [c for c in cycles if len(c) > 1]
        self.assertEqual(len(real_cycles), 0)
