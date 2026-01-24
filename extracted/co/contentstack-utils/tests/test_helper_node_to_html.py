import unittest

from contentstack_utils.helper.node_to_html import NodeToHtml
from contentstack_utils.render.options import Options


class TestHelperNodeToHtml(unittest.TestCase):
    node_dict = {
        "text": "Lorem ipsum dolor sit amet"
    }

    def setUp(self):
        print("Test Helper Class Node To Html")

    def test_test_helper_node_superscript(self):
        option = Options()
        what_does_it_returns = NodeToHtml.text_node_to_html(self.node_dict, option)
        print(what_does_it_returns)
        self.assertEqual("Lorem ipsum dolor sit amet", what_does_it_returns)

    def test_test_helper_node_subscript(self):
        option = Options()
        what_does_it_returns = NodeToHtml.text_node_to_html(self.node_dict, option)
        print(what_does_it_returns)
        self.assertEqual("Lorem ipsum dolor sit amet", what_does_it_returns)

    def test_test_helper_node_inline_code(self):
        option = Options()
        what_does_it_returns = NodeToHtml.text_node_to_html(self.node_dict, option)
        print(what_does_it_returns)
        self.assertEqual("Lorem ipsum dolor sit amet", what_does_it_returns)

    def test_test_helper_node_strikethrough(self):
        option = Options()
        what_does_it_returns = NodeToHtml.text_node_to_html(self.node_dict, option)
        print(what_does_it_returns)
        self.assertEqual("Lorem ipsum dolor sit amet", what_does_it_returns)

    def test_test_helper_node_underline(self):
        option = Options()
        what_does_it_returns = NodeToHtml.text_node_to_html(self.node_dict, option)
        print(what_does_it_returns)
        self.assertEqual("Lorem ipsum dolor sit amet", what_does_it_returns)

    def test_test_helper_node_italic(self):
        option = Options()
        what_does_it_returns = NodeToHtml.text_node_to_html(self.node_dict, option)
        print(what_does_it_returns)
        self.assertEqual("Lorem ipsum dolor sit amet", what_does_it_returns)

    def test_test_helper_node_bold(self):
        option = Options()
        what_does_it_returns = NodeToHtml.text_node_to_html(self.node_dict, option)
        print(what_does_it_returns)
        self.assertEqual("Lorem ipsum dolor sit amet", what_does_it_returns)

    def test_test_helper_node_undefined(self):
        option = Options()
        what_does_it_returns = NodeToHtml.text_node_to_html(self.node_dict, option)
        print(what_does_it_returns)
        self.assertEqual("Lorem ipsum dolor sit amet", what_does_it_returns)
