import json
from pathlib import Path
from unittest import TestCase

from pycarlo.common.files import BytesFileReader, JsonFileReader, TextFileReader, to_path


class FileReaderTests(TestCase):
    test_file_path = f"{Path(__file__).parent}/data.json"

    def test_readers(self):
        as_bytes = BytesFileReader(self.test_file_path).read()
        as_dict = JsonFileReader(self.test_file_path).read()
        as_str = TextFileReader(self.test_file_path).read()

        self.assertEqual(as_dict, json.loads(as_bytes))
        self.assertEqual(as_dict, json.loads(as_str))
        self.assertEqual(as_bytes, as_str.encode("utf-8"))


class FileUtilsTests(TestCase):
    def test_to_path(self):
        path_as_str = "some/relative/path"
        path = to_path(path_as_str)

        self.assertIsInstance(path, Path)
        self.assertEqual(path_as_str, str(path))
        self.assertIs(to_path(path), path)
