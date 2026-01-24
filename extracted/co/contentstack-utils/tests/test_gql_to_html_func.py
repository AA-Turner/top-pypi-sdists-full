import json
import os
import unittest

from contentstack_utils.gql import GQL
from contentstack_utils.render.options import Options


def mock_entry():
    path_gql = 'mocks/graphqlmock'
    file = os.path.dirname(os.path.abspath(__file__))
    gql_entry = os.path.join(file, path_gql, 'content.json')
    with open(gql_entry) as file:
        return json.load(file)


class TestGQLToHtml(unittest.TestCase):
    srt_zero = '<p></p><div><p>Abcd Three</p><div><p>Content type: <span></span></p></div>'

    def setUp(self):
        print("logger for convert style")

    def test_read_entry(self):
        entry = mock_entry()
        self.assertIsNotNone(entry)

    def test_read_entry_uid(self):
        entry = mock_entry()
        self.assertEqual('sameple_uid', entry['srte']['json']['uid'])

    def test_gql_to_html(self):
        entry = mock_entry()
        option = Options()
        path_keys = ['json']
        response = GQL.json_to_html(entry['srte'], path_keys, option)
        self.assertEqual(response,
                         '<p>sample text</p><img src="https://images.contentstack.com/v3/assets/51807f919e0e4/11.jpg" alt="11.jpg" class="embedded-asset"  />')
