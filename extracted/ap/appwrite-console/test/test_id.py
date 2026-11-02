import unittest

from appwrite_console.id import ID


class TestIDMethods(unittest.TestCase):

    def test_unique(self):
        self.assertEqual(len(ID.unique()), 20)

    def test_custom(self):
        self.assertEqual(ID.custom('custom'), 'custom')
