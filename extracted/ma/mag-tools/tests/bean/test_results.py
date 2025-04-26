import unittest

from jsonparser.json_parser import JsonParser
from mag_tools.bean.db_list import DbList
from mag_tools.bean.results import Results


class TestResults(unittest.TestCase):
    def test(self):
        d = [1,2,3]
        data = DbList(d, total_count=10)
        results = Results.success(data)
        print(JsonParser.from_results(results))