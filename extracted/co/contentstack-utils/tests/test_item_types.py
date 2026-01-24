import unittest
from contentstack_utils.embedded.item_type import ItemType


class TestItemType(unittest.TestCase):

    def test_item_type_entry(self):
        typeof = ItemType.ENTRY
        self.assertEqual('entry', typeof.value)

    def test_item_type_asset(self):
        typeof = ItemType.ASSET
        self.assertEqual('asset', typeof.value)
