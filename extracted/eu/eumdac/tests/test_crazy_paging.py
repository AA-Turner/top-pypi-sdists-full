import unittest
import copy
from eumdac.collection import SearchResults
from .base import FakeCollection, FakeProduct

from typing import Mapping, Any


class LoadPageMock:
    def __init__(self, products):
        self.products = products
        self.called_with_params = []
        self.total_results = sum([len(x) for x in products])
        self.no_called = 0
        self.no_returned_features = 0
        self.first_call = True

    def mocked_load_page(self, params: Mapping[str, Any], session=None):
        if self.no_called % 2 == 0 and self.no_called != 0:
            self.total_results = sum([len(x) for x in self.products[self.no_called :]])
            self.products = self.products[self.no_called :]
            self.first_call = True
            self.no_called = 0
            self.no_returned_features = 0
        if self.no_called >= len(self.products):
            # Return an empty collection so iteration can finish cleanly
            return {
                "id": "fakeid",
                "type": "FeatureCollection",
                "totalResults": self.total_results,
                "itemsPerPage": 0,
                "startIndex": self.no_returned_features,
                "features": [],
            }
        selected_list = self.products[self.no_called]
        ret = {
            "id": "fakeid",
            "type": "FeatureCollection",
            "totalResults": self.total_results,
            "itemsPerPage": len(selected_list),
            "startIndex": self.no_returned_features,
            "features": [
                {
                    "type": "Feature",
                    "id": f"FAKE_PRODUCT_ID_no{x}",
                    "properties": {
                        "type": "Properties",
                        "date": "2014-09-28T13:39:00Z/2014-09-29T15:17:59Z",
                        "updated": "2022-03-20T19:41:33.714Z",
                    },
                }
                for x in selected_list
            ],
        }

        if self.first_call:
            self.first_call = False
            return ret

        self.no_called += 1
        self.no_returned_features += len(selected_list)
        self.called_with_params.append(copy.deepcopy(params))
        return ret


class TestCrazyPaging(unittest.TestCase):
    def setUp(self):
        self.called_args = []

    # This tests the paging implementation with the default sorting options
    def test_crazy_page_sense_desc(self):
        expected_params = [
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "dtend": "2014-09-29T15:17:59",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 6,
                "c": 3,
                "set": "brief",
                "dtend": "2014-09-29T15:17:59",
            },
        ]
        search_options = {
            "pi": {},
            "set": {},
            "sort": {},
            "dtstart": {},
            "dtend": {},
        }
        fake_col = FakeCollection(search_options=search_options)
        uut = SearchResults(fake_col, {"pi": "foobbar", "set": "brief"})
        load_page_mock = LoadPageMock([[1, 1, 3], [2, 2, 2], [4, 5, 6], [7, 8, 9]])
        uut._load_page = load_page_mock.mocked_load_page
        uut._items_per_page = 3
        uut._max_items_per_search = 6
        results = []
        results = list(uut)

        expected = [
            FakeProduct(id="FAKE_PRODUCT_ID_no1", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no3", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no2", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no4", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no5", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no6", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no7", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no8", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no9", collection=fake_col),
        ]
        assert [x._id for x in results] == [x._id for x in expected]
        print(load_page_mock.called_with_params)
        assert all(item in load_page_mock.called_with_params for item in expected_params)

    # This tests the paging implementation sorting by sensing time ascending
    def test_crazy_page_sense_asc(self):
        expected_params = [
            {
                "format": "json",
                "pi": "foobbar",
                "si": 0,
                "c": 3,
                "set": "brief",
                "sort": "start,time,1",
                "dtend": "2025-10-29T10:24:39",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "sort": "start,time,1",
                "dtend": "2025-10-29T10:24:39",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "sort": "start,time,1",
                "dtend": "2025-10-29T10:24:39",
                "dtstart": "2014-09-28T13:39:00",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 6,
                "c": 3,
                "set": "brief",
                "sort": "start,time,1",
                "dtend": "2025-10-29T10:24:39",
                "dtstart": "2014-09-28T13:39:00",
            },
        ]
        search_options = {
            "pi": {},
            "set": {},
            "sort": {},
            "dtstart": {},
            "dtend": {},
        }
        fake_col = FakeCollection(search_options=search_options)
        uut = SearchResults(fake_col, {"pi": "foobbar", "set": "brief", "sort": "start,time,1"})
        load_page_mock = LoadPageMock([[1, 1, 3], [2, 2, 2], [4, 5, 6], [7, 8, 9]])
        uut._load_page = load_page_mock.mocked_load_page
        uut._items_per_page = 3
        uut._max_items_per_search = 6
        results = []
        results = list(uut)

        expected = [
            FakeProduct(id="FAKE_PRODUCT_ID_no1", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no3", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no2", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no4", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no5", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no6", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no7", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no8", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no9", collection=fake_col),
        ]
        assert [x._id for x in results] == [x._id for x in expected]
        for expected, actual in zip(expected_params, load_page_mock.called_with_params):
            expected_copy = expected.copy()
            actual_copy = actual.copy()

            expected_copy.pop("dtend", None)
            actual_copy.pop("dtend", None)

        assert expected_copy == actual_copy

    # This tests the paging implementation sorting by publication ascending
    def test_crazy_page_pub_asc(self):
        expected_params = [
            {
                "format": "json",
                "pi": "foobbar",
                "si": 0,
                "c": 3,
                "set": "brief",
                "sort": "publicationDate,,1",
                "dtend": "2025-10-29T10:31:02",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "sort": "publicationDate,,1",
                "dtend": "2025-10-29T10:31:02",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "sort": "publicationDate,,1",
                "dtend": "2025-10-29T10:31:02",
                "publication": "[2022-03-20T19:41:33.714",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 6,
                "c": 3,
                "set": "brief",
                "sort": "publicationDate,,1",
                "dtend": "2025-10-29T10:31:02",
                "publication": "[2022-03-20T19:41:33.714",
            },
        ]
        search_options = {
            "pi": {},
            "set": {},
            "sort": {},
            "dtstart": {},
            "dtend": {},
        }
        fake_col = FakeCollection(search_options=search_options)
        uut = SearchResults(
            fake_col, {"pi": "foobbar", "set": "brief", "sort": "publicationDate,,1"}
        )
        load_page_mock = LoadPageMock([[1, 1, 3], [2, 2, 2], [4, 5, 6], [7, 8, 9]])
        uut._load_page = load_page_mock.mocked_load_page
        uut._items_per_page = 3
        uut._max_items_per_search = 6
        results = []
        results = list(uut)

        expected = [
            FakeProduct(id="FAKE_PRODUCT_ID_no1", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no3", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no2", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no4", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no5", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no6", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no7", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no8", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no9", collection=fake_col),
        ]
        assert [x._id for x in results] == [x._id for x in expected]
        for expected, actual in zip(expected_params, load_page_mock.called_with_params):
            expected_copy = expected.copy()
            actual_copy = actual.copy()

            expected_copy.pop("dtend", None)
            actual_copy.pop("dtend", None)

        assert expected_copy == actual_copy

    # This tests the paging implementation sorting by publication descending
    def test_crazy_page_pub_desc(self):
        expected_params = [
            {
                "format": "json",
                "pi": "foobbar",
                "si": 0,
                "c": 3,
                "set": "brief",
                "sort": "publicationDate,,0",
                "dtend": "2025-10-29T10:35:41",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "sort": "publicationDate,,0",
                "dtend": "2025-10-29T10:35:41",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "sort": "publicationDate,,0",
                "dtend": "2025-10-29T10:35:41",
                "publication": "2022-03-20T19:41:33.714]",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 6,
                "c": 3,
                "set": "brief",
                "sort": "publicationDate,,0",
                "dtend": "2025-10-29T10:35:41",
                "publication": "2022-03-20T19:41:33.714]",
            },
        ]
        search_options = {
            "pi": {},
            "set": {},
            "sort": {},
            "dtstart": {},
            "dtend": {},
        }
        fake_col = FakeCollection(search_options=search_options)
        uut = SearchResults(
            fake_col, {"pi": "foobbar", "set": "brief", "sort": "publicationDate,,0"}
        )
        load_page_mock = LoadPageMock([[1, 1, 3], [2, 2, 2], [4, 5, 6], [7, 8, 9]])
        uut._load_page = load_page_mock.mocked_load_page
        uut._items_per_page = 3
        uut._max_items_per_search = 6
        results = []
        results = list(uut)

        expected = [
            FakeProduct(id="FAKE_PRODUCT_ID_no1", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no3", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no2", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no4", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no5", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no6", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no7", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no8", collection=fake_col),
            FakeProduct(id="FAKE_PRODUCT_ID_no9", collection=fake_col),
        ]
        assert [x._id for x in results] == [x._id for x in expected]
        for expected, actual in zip(expected_params, load_page_mock.called_with_params):
            expected_copy = expected.copy()
            actual_copy = actual.copy()

            expected_copy.pop("dtend", None)
            actual_copy.pop("dtend", None)

        assert expected_copy == actual_copy

    # This tests the paging implementation where everh single product is a duplicate to ensure duplications are handled successfully for all pages
    def test_crazy_page_large_amount_duplicates(self):
        expected_params = [
            {
                "format": "json",
                "pi": "foobbar",
                "si": 0,
                "c": 3,
                "set": "brief",
                "dtend": "2025-10-29T10:27:39",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "dtend": "2025-10-29T10:27:39",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 3,
                "c": 3,
                "set": "brief",
                "dtend": "2014-09-29T15:17:59",
            },
            {
                "format": "json",
                "pi": "foobbar",
                "si": 6,
                "c": 3,
                "set": "brief",
                "dtend": "2014-09-29T15:17:59",
            },
        ]
        search_options = {
            "pi": {},
            "set": {},
            "sort": {},
            "dtstart": {},
            "dtend": {},
        }
        fake_col = FakeCollection(search_options=search_options)
        uut = SearchResults(fake_col, {"pi": "foobbar", "set": "brief"})
        load_page_mock = LoadPageMock([[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]])
        uut._load_page = load_page_mock.mocked_load_page
        uut._items_per_page = 3
        uut._max_items_per_search = 6
        results = []
        results = list(uut)

        expected = [FakeProduct(id="FAKE_PRODUCT_ID_no1", collection=fake_col)]
        assert [x._id for x in results] == [x._id for x in expected]
        for expected, actual in zip(expected_params, load_page_mock.called_with_params):
            expected_copy = expected.copy()
            actual_copy = actual.copy()

            expected_copy.pop("dtend", None)
            actual_copy.pop("dtend", None)

        assert expected_copy == actual_copy
