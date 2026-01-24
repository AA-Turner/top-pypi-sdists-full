import os
import unittest
import json
from contentstack_utils.helper.metadata import Metadata, StyleType
from contentstack_utils.render import options


def read_mock_path(path):
    path_to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'mocks', path)
    return path_to_json


class TestRenderOption(unittest.TestCase):

    def test_get_default_options_render_asset_display(self):
        json_array = None
        path = read_mock_path('embedded_items.json')
        with open(path) as file:
            json_array = json.load(file)
        dictionary = json_array['entries'][0]['_embedded_items']['rich_text_editor'][0]
        default_opt = options.Options()
        metadata = Metadata("this is sample text", "asset", 'blt8928738723', 'products',
                            StyleType.DISPLAY, "this is outer html", 'sample attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual('<img src=/sample-entry-one alt=Hi sample entry for embedding/>', result)

    def test_get_default_options_render_no_style(self):
        with open('tests/mocks/embedded_items.json', 'r') as f:
            array = json.load(f)
            dictionary = array['entries'][0]['_embedded_items']['rich_text_editor'][0]
            default_opt = options.Options()
            metadata = Metadata("this is sample text", "asset", 'blt8928738723', 'products',
                                StyleType.DOWNLOAD, "this is outer html", 'sample attributes')
            result = default_opt.render_options(dictionary, metadata)
            self.assertEqual('<a href=/sample-entry-one>Hi sample entry for embedding</a>', result)
