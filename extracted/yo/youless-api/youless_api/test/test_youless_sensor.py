import unittest

from youless_api.youless_sensor import YoulessSensor


class TestYoulessData(unittest.TestCase):

    def test_value(self):
        value = YoulessSensor(1.232, "w")
        self.assertTrue(value.value == 1.232)
        self.assertTrue(value.unit_of_measurement == "w")
