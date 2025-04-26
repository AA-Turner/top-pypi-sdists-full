from unittest import TestCase

from montecarlodata.common.common import ConditionalDictionary


class MyTestCase(TestCase):
    def test_no_nones_set(self):
        dictionary = ConditionalDictionary(lambda x: x is not None)
        dictionary["a"] = 0
        dictionary["b"] = True
        dictionary["c"] = None
        dictionary["d"] = False
        self.assertEqual({"a": 0, "b": True, "d": False}, dictionary)

    def test_no_nones_update(self):
        dictionary = ConditionalDictionary(lambda x: x is not None)
        dictionary.update({"a": 0, "b": True, "c": None, "d": False})
        self.assertEqual({"a": 0, "b": True, "d": False}, dictionary)
