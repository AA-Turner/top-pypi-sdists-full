import json
import os
import unittest

from contentstack_utils.render.options import Options
from contentstack_utils.utils import Utils


def _is_json(file):
    try:
        json.dumps(file)
        return True
    except ValueError:
        return False


def read_mock_path(path):
    path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'mocks', path)
    return path_to_json


class TestUtility(unittest.TestCase):

    def test_cover_valid_json(self):
        valid = _is_json(_is_json("outfile"))
        self.assertTrue(valid)

    def test_cover_render_fn_if_entry_obj_is_dict(self):
        key_path = ['global_rich_multiple.group.rich_text_editor',
                    'global_rich_multiple.group'
                    '.rich_text_editor_multiple']
        path = read_mock_path('multiple_rich_text_content.json')
        with open(path) as file:
            entry_list = json.load(file)['entries'][0]
            option = Options()
            return_value = Utils.render(entry_list, key_path, option)
            self.assertIsNone(return_value)

    def test_cover_render_fn_if_entry_obj_is_list(self):
        key_path = ['global_rich_multiple.group.rich_text_editor',
                    'global_rich_multiple.group'
                    '.rich_text_editor_multiple']
        path = read_mock_path('multiple_rich_text_content.json')
        with open(path) as file:
            entry_list = json.load(file)['entries']
            option = Options()
            return_value = Utils.render(entry_list, key_path, option)
            self.assertIsNone(return_value)

    def test_if_entry_object_render_content_asset(self):
        path = read_mock_path('multiple_rich_text_content.json')
        with open(path) as file:
            json_array = json.load(file)
            entry_list = json_array['entries'][0]
            callback = Options()
            rte_content = "<p>Global multiple group 1</p><figure class=\"embedded-asset\" " \
                          "data-redactor-type=\"embed\" data-widget-code=\"\" " \
                          "data-sys-asset-filelink=\"https://app.contentstack.com/v3/assets" \
                          "/11.jpg\" " \
                          "data-sys-asset-uid=\"7324a68403ee7281\" data-sys-asset-filename=\"11.jpg\" " \
                          "data-sys-asset-contenttype=\"image/jpeg\" type=\"asset\" " \
                          "sys-style-type=\"display\"></figure>"
            response = Utils.render_content(rte_content, entry_list, callback, )
            # self.assertEqual('<p>Global multiple group 1</p><img '
            #                  'src=https://app.contentstack.com/v3/assets/'
            #                  '11.jpg alt=11.jpg/>', response)

    def test_if_entry_object_render_content_entry(self):
        path = read_mock_path('multiple_rich_text_content.json')
        with open(path) as file:
            json_array = json.load(file)
            entry_list = json_array['entries'][0]
            option = Options()
            rte_content = "<p><a data-sys-entry-uid=\"1c9e75e3608f8c6b\" data-sys-entry-locale=\"en-us\" " \
                          "data-sys-content-type-uid=\"0_solve\" sys-style-type=\"link\" data-sys-can-edit=\"true\" " \
                          "class=\"embedded-entry\" type=\"entry\" href=\"/untitled\" title=\"Entry 001 123\">Global " \
                          "multiple modular 1</a></p>"
            response = Utils.render_content(rte_content, entry_list, option)
            self.assertEqual('<p><a href=/untitled>Entry 001 123</a></p>', response)
