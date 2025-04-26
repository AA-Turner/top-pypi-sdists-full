import unittest
from shortid import ShortId

class TestShortId(unittest.TestCase):
    def setUp(self):
        self.shortid = ShortId()

    def test_should_be_unambiquous_on_a_bunch_of_iterations(self):
        ids = []
        for i in range(0, 100000):
            ids.append(self.shortid.generate())

        self.assertEqual(len(set(ids)), len(ids))

    def test_should_be_unambiquous_on_a_bunch_of_iterations_new_instance(self):
        ids = []
        for i in range(0, 100000):
            ids.append(ShortId().generate())

        self.assertEqual(len(set(ids)), len(ids))

    def test_generate_max_length(self):
        lengths = []
        for i in range(0, 50000):
            lengths.append(len(self.shortid.generate()))
        self.assertEqual(max(lengths) < 12, True)


    def test_generate_max_length_new_instance(self):
        lengths = []
        for i in range(0, 50000):
            lengths.append(len(ShortId().generate()))
        self.assertEqual(max(lengths) < 12, True)
