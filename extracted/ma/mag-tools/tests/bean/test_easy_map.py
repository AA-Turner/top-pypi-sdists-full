import unittest
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from mag_tools.bean.easy_map import EasyMap
from mag_tools.enums.base_enum import BaseEnum


class TestEasyMap(unittest.TestCase):
    def setUp(self):
        self.map = EasyMap()

    def test_add_and_get_string(self):
        self.map.add("key1", "value1")
        self.assertEqual(self.map.get_string("key1"), "value1")

    def test_get_integer(self):
        self.map.add("key2", "123")
        self.assertEqual(self.map.get_int("key2"), 123)

    def test_get_double(self):
        self.map.add("key3", "123.45")
        self.assertEqual(self.map.get_float("key3"), 123.45)

    def test_get_boolean(self):
        self.map.add("key4", "true")
        self.assertTrue(self.map.get_bool("key4"))

    def test_get_date(self):
        self.map.add("key5", "2024-12-31")
        self.assertEqual(self.map.get_date("key5"), date(2024, 12, 31))

    def test_get_local_date_time(self):
        self.map.add("key6", "2024-12-31 23:59:59")
        self.assertEqual(self.map.get_datetime("key6"), datetime(2024, 12, 31, 23, 59, 59))

    def test_get_big_decimal(self):
        self.map.add("key7", "12345.6789")
        self.assertEqual(self.map.get_decimal("key7"), Decimal("12345.6789"))

    def test_get_enum(self):
        class Color(BaseEnum):
            RED = "red"
            GREEN = "green"
            BLUE = "blue"

        self.map.add("key8", "RED")
        self.assertEqual(self.map.get_enum("key8", Color), Color.RED)

    def test_to_map(self):
        self.map.add("key1", "value1")
        self.map.add("key2", "value2")
        expected_map = {"key1": "value1", "key2": "value2"}
        self.assertEqual(self.map.to_map(), expected_map)

    def test_get_by_json(self):
        self.map.add("key9", '{"name": "John", "age": 30}')
        result = self.map.get_by_json("key9", dict)
        self.assertEqual(result, {"name": "John", "age": 30})

    def test_keys_to_hump(self):
        @dataclass
        class ChildInfo:
            first_name: Optional[str] = None
            real_age: Optional[int] = None
            real_height: Optional[int] = None

        map_ = EasyMap().add("key_a1", "value1").add("key_a2", "value2").add("child", ChildInfo(first_name="John", real_age=30, real_height=100))
        new_map = map_.keys_to_hump()
        print(new_map)

if __name__ == "__main__":
    unittest.main()

