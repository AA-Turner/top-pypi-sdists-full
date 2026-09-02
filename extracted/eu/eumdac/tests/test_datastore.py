import pytest
from eumdac.token import AccessToken
from eumdac.datastore import DataStore, DataStoreError, Product
from eumdac.collection import Collection

from .base import DataServiceTestCase


class TestDataStore(DataServiceTestCase):
    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)
        self.datastore = DataStore(token=self.token)

    def test_property_collections(self):
        collections = self.datastore.collections
        self.assertIsInstance(collections, list)
        self.assertIn("EO:EUM:DAT:MSG:HRSEVIRI", map(str, collections))
        self.assertIsInstance(collections[0], Collection)

    def test_product_from_url(self):
        valid_url = "https://api.eumetsat.int/data/download/1.0.0/collections/EO%3AEUM%3ADAT%3AMSG%3AMSG15-RSS/products/MSG4-SEVI-MSG15-0100-NA-20240404125918.061000000Z-NA"
        invalid_url = "https://fake.url.int/other/api/download"
        valid_product = self.datastore.get_product_from_url(valid_url)
        self.assertIsInstance(valid_product, Product)
        with pytest.raises(Exception):
            self.datastore.get_product_from_url(invalid_url)
