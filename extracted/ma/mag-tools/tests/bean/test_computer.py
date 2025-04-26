import unittest

from bean.sys.computer import Computer


class TestComputer(unittest.TestCase):
    def test_get_config(self):
        computer = Computer.get_info()
        print(computer.hash)