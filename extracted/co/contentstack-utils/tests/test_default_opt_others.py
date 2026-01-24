import json
import os
import unittest

from contentstack_utils.helper.metadata import Metadata, StyleType
from contentstack_utils.render import options


def read_mock_path():
    to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'mocks', 'embedded_items_without_title.json')
    with open(to_json) as file:
        to_json = json.load(file)
    return to_json['entries'][0]['_embedded_items']['rich_text_editor']


class TestDefaultOptOther(unittest.TestCase):

    def test_get_default_options_render_option_block_without_title(self):
        to_json = read_mock_path()
        dictionary = to_json[0]
        default_opt = options.Options()
        metadata = Metadata("Hi sample entry for embedding", "entry", 'bltb5a04880fbb74f26', 'samplect',
                            StyleType.BLOCK, "this is outer html", 'samplect attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual('<div><p>removed_for_security_reasons</p><div><p>Content type: <span>samplect</span></p></div>', result)

    def test_get_render_option_asset_without_title_link(self):
        to_json = read_mock_path()
        dictionary = to_json[0]
        default_opt = options.Options()
        metadata = Metadata("Hi sample entry for embedding", "entry", 'bltb5a04880fbb74f26', 'samplect',
                            StyleType.DISPLAY, "this is outer html", 'samplect attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual('<img src=/sample-entry-one alt=samplect_filename/>', result)

    def test_get_render_option_asset_without_title_filename_link(self):
        to_json = read_mock_path()
        dictionary = to_json[1]
        default_opt = options.Options()
        metadata = Metadata("Hi sample entry for embedding", "entry", 'b5a04880fbb74f26', 'samplect',
                            StyleType.DISPLAY, "this is outer html", 'samplect attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual('<img src=/sample-entry-one alt=removed_for_security_reasons/>', result)
