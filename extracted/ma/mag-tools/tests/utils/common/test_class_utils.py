import unittest
from types import NoneType
from typing import Optional

from enums.client_type import ClientType
from utils.common.class_utils import ClassUtils


class TestClassUtils(unittest.TestCase):
    def test_get_origin_type(self):
        print(ClassUtils.get_origin_type(Optional[str]))
        print(ClassUtils.get_origin_type(Optional[int]))
        print(ClassUtils.get_origin_type(int))
        print(ClassUtils.get_origin_type(NoneType))
        print(ClassUtils.get_origin_type(ClientType))
        print(ClassUtils.get_origin_type(tuple[int]))
        print(ClassUtils.get_origin_type(list[list[int]]))