import json
import time
import unittest
import sys
from typing import List

from appian_locust.utilities.helper import (find_component_by_attribute_in_dict,
                                            find_component_by_attribute_and_type_in_dict,
                                            find_component_by_attribute_and_index_in_dict,
                                            find_component_by_index_in_dict,
                                            repeat)

from .mock_reader import read_mock_file
import os
import appian_locust.utilities.helper as helper


class TestHelper(unittest.TestCase):
    form_dict = json.loads(read_mock_file("test_response.json"))

    def test_find_component_by_label_and_type(self) -> None:
        component = find_component_by_attribute_and_type_in_dict('label', 'Request Pass', 'StartProcessLink', self.form_dict)
        # finds first component with that label and type
        self.assertEqual(component['cacheKey'], 'c93e2f33-06eb-42b2-9cfc-2c4a0e14088e')
        self.assertEqual(component['processModelOpaqueId'], 'iQB8GmxIr5iZT6YnVytCx9QKdJBPaRDdv_-hRj3HM747ZtRjSw')

    def test_find_component_by_attribute_in_dict(self) -> None:
        component = find_component_by_attribute_in_dict('label', 'Request Pass', self.form_dict)
        # finds first component by that label
        self.assertEqual(component['#t'], 'RichTextDisplayField')

    def test_find_component_by_attribute_and_index_in_dict(self) -> None:
        component = find_component_by_attribute_and_index_in_dict('label', 'Request Pass', 1, self.form_dict)
        self.assertEqual(component['_cId'], 'f9214210c2a2f69865a434c6a773ec71')
        self.assertEqual(component['#t'], 'RichTextDisplayField')

    def test_find_component_by_index_in_git(self) -> None:
        component = find_component_by_index_in_dict('FormattedText', 1, self.form_dict)
        self.assertEqual(component['_cId'], 'b2a256d7e6b636ae3cf17bcb7cf8925e')
        self.assertEqual(component['#t'], 'FormattedText')

    def test_repeat_decorator(self) -> None:
        # Given
        my_list: List[int] = []

        @repeat(2)
        def append_one(my_list: List) -> None:
            my_list.append(1)

        # When
        append_one(my_list)
        # Then
        self.assertEqual([1, 1], my_list)

    def test_repeat_decorator_naked(self) -> None:
        # Given
        my_list: List[int] = []

        @repeat()
        def append_one(my_list: List) -> None:
            my_list.append(1)

        # When
        append_one(my_list)
        # Then
        self.assertEqual([1, 1], my_list)

    def test_repeat_decorator_sleeping(self) -> None:
        # Given
        my_list: List[int] = []
        wait_time = 0.5
        start = time.time()

        @repeat(wait_time=wait_time)
        def append_one(my_list: List) -> None:
            my_list.append(1)

        # When
        append_one(my_list)
        # Then
        self.assertLessEqual(2 * wait_time, time.time() - start)
        self.assertGreaterEqual(2 * wait_time + 0.05, time.time() - start)

    def test_format_label(self) -> None:
        var = helper.format_label("first second")
        self.assertEqual(var, "first_second")

    def test_get_random_item(self) -> None:
        testlist = [10, 5, 6, 8, 2, 4]
        var = helper.get_random_item(testlist)
        self.assertIn(var, testlist)

    def test_get_random_item_with_exclude(self) -> None:
        testlist = [10, 5, 6, 8, 2, 4]
        exclude = [2, 4]
        var = helper.get_random_item(testlist, exclude)
        self.assertTrue((var in testlist and var not in exclude))

    def test_get_random_item_with_no_item_to_choose(self) -> None:
        testlist = [2]
        exclude = [2]
        with self.assertRaisesRegex(Exception, "There is no item to select randomly"):
            helper.get_random_item(testlist, exclude)

    def test_find_component_by_attribute_in_dict_check_step2_status(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))

        raw_data = read_mock_file("library_utils.json")
        testdata = json.loads(raw_data)

        output = helper.find_component_by_attribute_in_dict('step2_status', 'pass', testdata)
        self.assertTrue(output["step2_status"] == "pass")
