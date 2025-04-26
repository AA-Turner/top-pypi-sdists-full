import unittest

from mag_tools.enums.base_enum import BaseEnum
from mag_tools.enums.client_type import ClientType


class TestBaseEnum(unittest.TestCase):
    def test_of(self):
        e = BaseEnum.of(ClientType, 'IPAD')
        print(e.code)