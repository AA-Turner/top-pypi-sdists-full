import json
import os
import unittest
from contentstack_utils import Utils
from contentstack_utils.render.options import Options
from tests.mocks.supercharged.results import Results


def __is_json(file):
    try:
        json.dumps(file)
        return True
    except ValueError:
        return False


def load_mock():
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'mocks/supercharged', 'supercharged.json')
    with open(path) as file:
        return json.load(file)


class TestSuperchargedUtils(unittest.TestCase):
    global _json_data  # Note that the PyCharm warnings are not actual python errors

    def setUp(self):
        self._json_data = load_mock()

    def test_plaintext_in_supercharged_dict_to_html(self):
        array_str = ['plaintext']
        response = Utils.json_to_html(self._json_data, array_str, Options())
        self.assertEqual(Results.plainTextHtml, response)

    def test_plaintext_in_supercharged_list_to_html(self):
        array_str = ['plaintext_array']
        response = Utils.json_to_html(self._json_data, array_str, Options())
        self.assertEqual(Results.plainTextHtml, response)

    def test_paragraph_in_supercharged_dict_to_html(self):
        array_str = ['paragraph']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.paragraphHtml, response)

    def test_h1_in_supercharged_dict_to_html(self):
        array_str = ['h_one']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h1Html, response)

    def test_h2_in_supercharged_dict_to_html(self):
        array_str = ['h_two']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h2Html, response)

    def test_h3_in_supercharged_dict_to_html(self):
        array_str = ['h_three']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h3Html, response)

    def test_h4_in_supercharged_dict_to_html(self):
        array_str = ['h_four']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h4Html, response)

    def test_h5_in_supercharged_dict_to_html(self):
        array_str = ['h_five']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h5Html, response)

    def test_h6_in_supercharged_dict_to_html(self):
        array_str = ['h_six']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.h6Html, response)

    def test_order_list_in_supercharged_dict_to_html(self):
        array_str = ['order_list']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.orderListHtml, response)

    def test_un_order_list_in_supercharged_dict_to_html(self):
        array_str = ['un_order_list']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.unorderListHtml, response)

    def test_image_list_in_supercharged_dict_to_html(self):
        array_str = ['img']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.imgHtml, response)

    def test_table_list_in_supercharged_dict_to_html(self):
        array_str = ['table']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.tableHtml, response)

    def test_blockquote_list_in_supercharged_dict_to_html(self):
        array_str = ['blockquote']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.blockquoteHtml, response)

    def test_code_list_in_supercharged_dict_to_html(self):
        array_str = ['code']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.codeHtml, response)

    def test_linkin_list_in_supercharged_dict_to_html(self):
        array_str = ['link']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.linkInPHtml, response)

    def test_reference_list_in_supercharged_dict_to_html(self):
        array_str = ['reference']
        response = Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.refImgHtml, response)
    
    def test_nested_order_list_in_supercharged_dict_to_html(self):
        array_str = ['nested_order_list_with_fragment']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.nested_order_list_with_fragment, "<ol><li><fragment>List Item 1</fragment><ol><li>List Item 1.1</li><li>List Item 1.2</li><li>List Item 1.3</li></ol></li></ol>")

    def test_reference_image_in_supercharged_dict_to_html(self):
         array_str = ['reference']
         response = Utils.json_to_html([self._json_data], array_str, Options())
         self.assertEqual(Results.refImgHtml, response)
    
    def test_nested_order_list_in_supercharged_dict_to_html(self):
        array_str = ['nested_order_list_with_fragment']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.nested_order_list_with_fragment, "<ol><li><fragment>List Item 1</fragment><ol><li>List Item 1.1</li><li>List Item 1.2</li><li>List Item 1.3</li></ol></li></ol>")

    def test_nested_unorder_list_in_supercharged_dict_to_html(self):
        array_str = ['nested_unorder_list_with_fragment']
        Utils.json_to_html([self._json_data], array_str, Options())
        self.assertEqual(Results.nested_unorder_list_with_fragment, "<ul><li><fragment>List Item 1</fragment><ul><li>List Item 1.1</li><li>List Item 1.2</li><li>List Item 1.3</li></ul></li></ul>")