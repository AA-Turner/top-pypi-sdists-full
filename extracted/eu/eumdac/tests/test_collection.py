from datetime import datetime

from eumdac.token import AccessToken
from eumdac.datastore import DataStore
from eumdac.collection import Collection, CollectionError
from eumdac.product import Product
from .base import INTEGRATION_TESTING, DataServiceTestCase


class TestCollection(DataServiceTestCase):
    collection_id = "EO:EUM:DAT:MSG:HRSEVIRI"

    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)
        self.datastore = DataStore(token=self.token)
        self.collection = Collection(self.collection_id, self.datastore)

    def test_string_representation(self):
        self.assertEqual(self.collection_id, str(self.collection))
        self.assertIn(self.collection_id, repr(self.collection))

    def test_properties(self):
        self.assertIsInstance(self.collection.abstract, str)
        self.assertIsInstance(self.collection.title, str)
        self.assertIsInstance(self.collection.metadata, dict)
        self.assertIn("properties", self.collection.metadata)
        # check that the whitespaces have been fixed
        self.assertNotIn("\n", self.collection.abstract)

    def test_search(self):
        products = self.collection.search(
            dtstart=datetime(2022, 10, 1, 0, 0, 0), dtend=datetime(2022, 10, 1, 1, 0, 0)
        )
        product_ids = [str(product) for product in products]
        expected_product_ids = [
            "MSG4-SEVI-MSG15-0100-NA-20221001005743.037000000Z-NA",
            "MSG4-SEVI-MSG15-0100-NA-20221001004242.893000000Z-NA",
            "MSG4-SEVI-MSG15-0100-NA-20221001002742.762000000Z-NA",
            "MSG4-SEVI-MSG15-0100-NA-20221001001242.637000000Z-NA",
        ]
        self.assertEqual(product_ids, expected_product_ids)
        first = products.first()
        self.assertIsInstance(first, Product)

    def test_camparison(self):
        seviri_rss = Collection("EO:EUM:DAT:MSG:MSG15-RSS", self.datastore)
        avhrr_l1 = Collection("EO:EUM:DAT:METOP:AVHRRL1", self.datastore)
        self.assertLess(avhrr_l1, seviri_rss)
        self.assertNotEqual(avhrr_l1, seviri_rss)

    def test_product_type(self):
        self.assertEqual(self.collection.product_type, "HRSEVIRI")


class TestSearchResults(DataServiceTestCase):
    collection_id = "EO:EUM:DAT:MSG:HRSEVIRI"

    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)
        self.datastore = DataStore(token=self.token)
        self.collection = Collection(self.collection_id, self.datastore)
        self.search_results = self.collection.search(
            dtstart=datetime(2022, 10, 1, 0, 0, 0), dtend=datetime(2022, 10, 1, 1, 0, 0)
        )

    def test_string_representation(self):
        self.assertIn(self.collection_id, repr(self.search_results))

    def test_properties(self):
        total_results = self.search_results.total_results
        all_results = list(self.search_results)
        self.assertEqual(total_results, len(all_results))

        query = self.search_results.query
        self.assertIn("dtstart", query)
        self.assertIn("dtend", query)

    def test_update_query(self):
        new_results = self.search_results.update_query(dtend=datetime(2022, 10, 1, 2, 0, 0))
        # check that we created a new instance
        self.assertIsNot(self.search_results, new_results)

    def test_first(self):
        first = self.search_results.first()
        all_products = list(self.search_results)
        self.assertEqual(first, all_products[0])
        self.assertIsInstance(first, Product)

    def test_empty_results(self):
        empty_results = self.collection.search(
            dtstart=datetime(2000, 1, 1, 0, 0, 0), dtend=datetime(2000, 1, 1, 0, 0, 1)
        )
        first = empty_results.first()
        self.assertIsNone(first)
        self.assertEqual(empty_results.total_results, 0)
        self.assertEqual(list(empty_results), [])

    def test_pagination(self):
        self.datastore.collections
        total_results = self.search_results.total_results

        self.search_results._items_per_page = total_results
        n_calls_before = len(self.requests_mock.calls)
        assert len(list(self.search_results)) > 0
        n_calls_after = len(self.requests_mock.calls)
        self.assertEqual(n_calls_after, n_calls_before + 1)

        self.search_results._items_per_page = total_results // 2
        n_calls_before = len(self.requests_mock.calls)
        assert len(list(self.search_results)) > 0
        n_calls_after = len(self.requests_mock.calls)
        self.assertEqual(n_calls_after, n_calls_before + 2)

    def test_results_contain_product(self):
        first = self.search_results.first()
        self.assertIn(first, self.search_results)

        product_id = "MSG1-SEVI-MSG15-0201-NA-20040120075736.727000000Z-NA"
        other = self.datastore.get_product(self.collection_id, product_id)
        self.assertNotIn(other, self.search_results)

    def test_invalid_search_argument(self):
        with self.assertRaisesRegex(CollectionError, r"invalid search options .*"):
            self.collection.search(foo="bar")

    def test_search_no_starttime(self):
        results = self.collection.search(dtend=datetime(2022, 10, 1, 1, 0, 0))

    def test_search_no_endtime(self):
        results = self.collection.search(dtstart=datetime(2000, 1, 1, 0, 0, 0))
