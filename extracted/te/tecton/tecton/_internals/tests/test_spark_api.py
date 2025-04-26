import tempfile
from unittest import TestCase

from tecton._internals.spark_api import _get_checkpoint_dir_name


class SparkApiTest(TestCase):
    def test_get_checkpoint_dir(self):
        tmp_dir = tempfile.mkdtemp(prefix="abc_")
        checkpoint_dir = _get_checkpoint_dir_name(tmp_dir)
        assert checkpoint_dir.startswith(tmp_dir)
