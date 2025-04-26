import json
import unittest
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from anytree import RenderTree

from mag_tools.enums.base_enum import BaseEnum
from mag_tools.bean.sys.cpu import Cpu
from mag_tools.bean.results import Results
from mag_tools.jsonparser.json_parser import JsonParser
from mag_tools.enums.service_status import ServiceStatus

class AType(BaseEnum):
    A = ('AA', 'A值')
    B = ('bb', 'B值')

@dataclass
class Test:
    name: Optional[str]
    shape: tuple[int]
    height: int
    a_type: Optional[AType]

class TestJsonParser(unittest.TestCase):
    def test_to_string(self):
        json_str = '"Hello,World!"'
        result = JsonParser.to_string(json_str)
        self.assertEqual(result, "Hello,World!")

    def test_to_decimal(self):
        decimal_str = '123.45'
        result = JsonParser.to_decimal(decimal_str)
        self.assertEqual(result, 123.45)

    def test_to_float(self):
        float_str = '123.45'
        result = JsonParser.to_float(float_str)
        self.assertEqual(result, 123.45)

    def test_to_int(self):
        int_str = '123'
        result = JsonParser.to_int(int_str)
        self.assertEqual(result, 123)

    def test_to_datetime(self):
        datetime_str = '"2023-04-06T11:54:03.000Z"'
        result = JsonParser.to_datetime(datetime_str)
        self.assertEqual(result, datetime.strptime("2023-04-06T11:54:03.000Z", '%Y-%m-%dT%H:%M:%S.%fZ'))

    def test_to_bool(self):
        bool_str = '"true"'
        result = JsonParser.to_bool(bool_str)
        self.assertTrue(result)

    def test_to_list(self):
        list_str = '[{"name":"John"}, {"name":"Jane"}]'
        result = JsonParser.to_list(list_str, dict)
        self.assertEqual(result, [{'name':'John'}, {'name':'Jane'}])

    def test_to_map(self):
        map_str = '{"key1": "value1", "key2": "value2"}'
        result = JsonParser.to_map(map_str, str, str)
        self.assertEqual(result, {"key1": "value1", "key2": "value2"})

    def test_to_tree(self):
        tree_str = '{"name": "root", "children": [{"name": "child1"}, {"name": "child2"}]}'
        result = JsonParser.to_tree(tree_str, str)
        self.assertEqual(result.name, "root")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].name, "child1")
        self.assertEqual(result.children[1].name, "child2")

        # 打印树结构
        for pre, fill, node in RenderTree(result):
            print("%s%s" % (pre, node.name))

    def test_to_bean(self):
        str_ = '{"name": "root", "height": 12, "shape": [1, 2, 3], "a_type": "A"}'
        result = JsonParser.to_bean(str_, Test)
        print(result)

        str_ = '{"name": "root", "height": 12, "shape": [1, 2, 3], "a_type": "bb"}'
        result = JsonParser.to_bean(str_, Test)
        print(result)

    def test_from_bean(self):
        test = Test(name='name', shape=[1, 2, 3], height=12, a_type=AType.A)
        json_str = JsonParser.from_bean(test)
        print(json_str)

    def test_from_list(self):
        cpus = [Cpu.get_info()]
        json_str = JsonParser.from_bean(cpus)
        print(json_str)

    def test_from_tuple(self):
        data_ = (1,2,3,4,)
        json_str = JsonParser.from_bean(data_)
        print(json_str)
        data_ = JsonParser.to_tuple(json_str, tuple)
        print(data_)

    def test_from_results(self):
        cpu = Cpu.get_info()
        results = Results(code=ServiceStatus.OK, message="OK", data=[cpu], total_count=10)
        json_str = JsonParser.from_bean(results)
        self.assertEqual(json.loads(json_str)['code'], 'OK')
        self.assertEqual(json.loads(json_str)['message'], "OK")

        cpus= json.loads(json_str)['data']
        self.assertEqual(cpus[0]['base_clock'], cpu.base_clock)

        self.assertEqual(json.loads(json_str)['total_count'], 10)

    def test_from_results_1(self):
        t = True
        results = Results(code=ServiceStatus.OK, message="OK", data=[t], total_count=10)
        json_str = JsonParser.from_bean(results)
        self.assertEqual(json.loads(json_str)['code'], 'OK')
        self.assertEqual(json.loads(json_str)['message'], "OK")

        t= json.loads(json_str)['data']
        self.assertEqual(t, True)

        self.assertEqual(json.loads(json_str)['total_count'], 10)

    def test_from_results_2(self):
        cpu = Cpu.get_info()
        results = Results(code=ServiceStatus.OK, message="OK", data=[cpu], total_count=10)
        json_str = JsonParser.from_results(results)
        self.assertEqual(json.loads(json_str)['code'], 'OK')
        self.assertEqual(json.loads(json_str)['message'], "OK")

        cpus= json.loads(json_str)['data']
        self.assertEqual(cpus[0]['baseClock'], cpu.base_clock)

        self.assertEqual(json.loads(json_str)['totalCount'], 10)

    def test_to_results(self):
        json_str = '{"code": "200", "message": "OK", "timestamp": "2023-04-06T11:54:03.000Z", "data": [true], "total_count": 1}'
        results = JsonParser.to_results(json_str, bool)
        self.assertEqual(results.code, ServiceStatus.OK)
        self.assertEqual(results.message, "OK")
        self.assertEqual(results.first, True)
        self.assertEqual(results.total_count, 1)

if __name__ == '__main__':
    unittest.main()
