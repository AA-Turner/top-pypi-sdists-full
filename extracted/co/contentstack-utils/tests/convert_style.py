from contentstack_utils.helper import converter
from contentstack_utils.embedded.styletype import StyleType
import unittest


class TestConvertStyle(unittest.TestCase):

    def setUp(self):
        print("logger for ConvertStyle")

    def test_converter_style_block(self):
        _returns = converter.convert_style('block')
        self.assertEquals(StyleType.BLOCK, _returns)

    def test_converter_style_inline(self):
        _returns = converter.convert_style('inline')
        self.assertEqual(StyleType.INLINE, _returns)

    def test_converter_style_link(self):
        _returns = converter.convert_style('link')
        self.assertEqual(StyleType.LINK, _returns)

    def test_converter_style_display(self):
        _returns = converter.convert_style('display')
        self.assertEqual(StyleType.DISPLAY, _returns)

    def test_converter_style_download(self):
        _returns = converter.convert_style('download')
        self.assertEqual(StyleType.DOWNLOAD, _returns)
