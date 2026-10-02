import os
import unittest


class BaseTest(unittest.TestCase):
    tool = None

    def setUp(self):
        self.file_descriptors = []

    def tearDown(self):
        for fd in self.file_descriptors:
            fd.close()

    def _get_file_handle(self, filename):
        fd = open(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "data", filename
        ), encoding="utf-8")
        self.file_descriptors.append(fd)
        return fd

    def _get_file_content(self, filename):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "data", filename), encoding="utf-8") as fh:
            content = fh.read()
        return content
