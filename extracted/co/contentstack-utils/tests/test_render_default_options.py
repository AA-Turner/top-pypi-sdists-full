import json
import os
import unittest

from contentstack_utils.helper.metadata import Metadata, StyleType
from contentstack_utils.render import options


def _is_json(file):
    try:
        json.dumps(file)
        return True
    except ValueError:
        return False


def read_mock_path():
    to_json = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'mocks', 'embedded_items.json')
    with open(to_json) as file:
        to_json = json.load(file)
    return to_json['entries'][0]


class TestRenderDefaultOption(unittest.TestCase):

    def test_read_json_file_by_absolute_path(self):
        self.assertIsNotNone(read_mock_path())

    def test_read_json_file_by_content_path(self):
        result = _is_json("/tests/mocks/embedded_items.json")
        instance = isinstance(result, bool)
        self.assertTrue(instance, 'this is to check the bool value')

    def test_get_title_or_uid(self):
        should_return_title = options._title_or_uid(read_mock_path())
        self.assertEqual("Entry one", should_return_title, "It should match dictionary title")

    def test_get_asset_title_or_uid(self):
        should_return_title = options._asset_title_or_uid(read_mock_path())
        self.assertEqual("Entry one", should_return_title, "It should match dictionary title")

    def test_get_default_options_render_option_block(self):
        dictionary = read_mock_path()['_embedded_items']['rich_text_editor'][0]
        default_opt = options.Options()
        metadata = Metadata("Hi sample entry for embedding", "entry", 'bltb5a04880fbb74f26', 'samplect',
                            StyleType.BLOCK, "this is outer html", 'samplect attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual("<div><p>Hi sample entry for embedding</p><div><p>Content type: "
                         "<span>samplect</span></p></div>", result)

    def test_get_default_options_render_option_inline(self):
        dictionary = read_mock_path()['_embedded_items']['rich_text_editor'][0]
        default_opt = options.Options()
        metadata = Metadata("this is sample text", "entry", 'blt8928738723', 'products',
                            StyleType.INLINE, "this is outer html", 'sample attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual('<span>Hi sample entry for embedding</span>', result)

    def test_get_default_options_render_option_link(self):
        dictionary = read_mock_path()['_embedded_items']['rich_text_editor'][0]
        default_opt = options.Options()
        metadata = Metadata("this is sample text", "entry", 'blt8928738723', 'products',
                            StyleType.LINK, "this is outer html", 'sample attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual('<a href=/sample-entry-one>Hi sample entry for embedding</a>', result)

    def test_get_default_options_render_asset_display(self):
        dictionary = read_mock_path()['_embedded_items']['rich_text_editor'][0]
        default_opt = options.Options()
        metadata = Metadata("this is sample text", "asset", 'blt8928738723', 'products',
                            StyleType.DISPLAY, "this is outer html", 'sample attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual('<img src=/sample-entry-one alt=Hi sample entry for embedding/>', result)

    def test_get_default_options_render_asset_none(self):
        dictionary = read_mock_path()['_embedded_items']['rich_text_editor'][0]
        default_opt = options.Options()
        metadata = Metadata("this is sample text", "asset", 'blt8928738723', 'products',
                            StyleType.DOWNLOAD, "this is outer html", 'sample attributes')
        result = default_opt.render_options(dictionary, metadata)
        self.assertEqual('<a href=/sample-entry-one>Hi sample entry for embedding</a>', result)
