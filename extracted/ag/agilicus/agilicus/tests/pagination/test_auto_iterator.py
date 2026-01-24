import pytest
from unittest.mock import Mock
from agilicus.pagination.auto_iterator import (
    AutoIterator,
    AutoIteratorWrapper,
    get_page_on,
    _determine_page_on,
    patch_endpoint,
    _handle_page_failure,
)
from agilicus_api.exceptions import ApiException
from agilicus import ListSSHResourcesResponse
from agilicus_api.api_client import Endpoint


class MockPageInfo:
    def __init__(self, page_at_key, page_on_value):
        self.page_at_key = page_at_key
        self.page_on = Mock(value=page_on_value)


class MockResponse:
    def __init__(
        self, items, page_at_key=None, page_on_value=None, legacy_pagination=False
    ):
        self.items = items
        self.attribute_map = {"items": "list[object]"}
        self.page_info = (
            MockPageInfo(page_at_key, page_on_value)
            if page_at_key and page_on_value
            else None
        )
        self.legacy_page_info = {}
        if legacy_pagination and page_on_value and page_at_key:
            self.legacy_page_info["page_at_" + page_on_value[0]] = page_at_key[0]

    def get(self, key, default=None):
        if key == "items":
            return self.items
        if self.legacy_page_info:
            return self.legacy_page_info.get(key, default)
        return default


class MockItem:
    def __init__(self, name, index):
        self.name = name
        self.id = index


class MockListFunction:
    def __init__(
        self,
        items_per_page,
        total_items,
        page_on_allowed=None,
        legacy_pagination_key=None,
    ):
        self._all_items = [MockItem(f"item_{i}", i) for i in range(total_items)]
        self._items_per_page = items_per_page
        self.call_count = 0
        self.allowed_values = {}
        self.params_map = {"all": []}
        if page_on_allowed is None:
            page_on_allowed = ["id"]
        if page_on_allowed:
            self.allowed_values = {("page_on",): {k: k for k in page_on_allowed}}
            self.params_map["all"].append("page_on")
        self.legacy_pagination_key = legacy_pagination_key

    def __call__(
        self, page_on=None, page_at_key=None, limit=None, page_sort=None, **kwargs
    ):
        if limit is None:
            limit = 1000
        if page_on is None:
            page_on = []
        self.call_count += 1
        start_index = 0
        if self.legacy_pagination_key:
            page_on = [self.legacy_pagination_key]
            page_at_key = [kwargs["page_at_" + self.legacy_pagination_key]]
        if page_at_key and page_at_key[0] not in (None, ""):
            try:
                start_index = len(self._all_items)
                for idx, item in enumerate(self._all_items):
                    compare_tuple = [getattr(item, key) for key in page_on]
                    if page_at_key < compare_tuple:
                        start_index = idx
                        break
            except ValueError:
                start_index = len(self._all_items)

        end_index = min(start_index + limit, len(self._all_items))
        current_items = self._all_items[start_index:end_index]

        next_page_at_key = None
        if end_index < len(self._all_items):
            next_page_at_key = [self._all_items[end_index - 1].id]

        return MockResponse(
            current_items,
            page_at_key=next_page_at_key,
            page_on_value=page_on if page_on else None,
            legacy_pagination=self.legacy_pagination_key is not None,
        )


def test_auto_iterator_basic_pagination():
    mock_list_function = MockListFunction(items_per_page=2, total_items=5)
    iterator = AutoIterator(mock_list_function, limit=None, page_size=2, page_sort=[])

    items = list(iterator)
    assert len(items) == 5
    assert mock_list_function.call_count == 3  # 5 items, 2 per page = 3 calls (2,2,1)
    assert [item.name for item in items] == [
        "item_0",
        "item_1",
        "item_2",
        "item_3",
        "item_4",
    ]


def test_auto_iterator_basic_legacy():
    mock_list_function = MockListFunction(
        items_per_page=2, total_items=5, legacy_pagination_key="id"
    )
    iterator = AutoIterator(
        mock_list_function,
        limit=None,
        page_size=2,
        page_sort=[],
        page_on="page_at_id",
        legacy_pagination=True,
    )

    items = list(iterator)
    assert len(items) == 5
    assert mock_list_function.call_count == 3  # 5 items, 2 per page = 3 calls (2,2,1)
    assert [item.name for item in items] == [
        "item_0",
        "item_1",
        "item_2",
        "item_3",
        "item_4",
    ]


def test_auto_iterator_with_limit():
    mock_list_function = MockListFunction(items_per_page=2, total_items=5)
    iterator = AutoIterator(mock_list_function, limit=3, page_size=2, page_sort=[])

    items = list(iterator)
    assert len(items) == 3
    assert mock_list_function.call_count == 2  # 3 items, 2 per page = 2 calls (2,1)
    assert [item.name for item in items] == ["item_0", "item_1", "item_2"]


def test_auto_iterator_empty_result():
    mock_list_function = MockListFunction(items_per_page=2, total_items=0)
    iterator = AutoIterator(mock_list_function, limit=None, page_size=2, page_sort=[])

    items = list(iterator)
    assert len(items) == 0
    assert mock_list_function.call_count == 1


def test_auto_iterator_first_method():
    mock_list_function = MockListFunction(items_per_page=2, total_items=5)
    iterator = AutoIterator(mock_list_function, limit=None, page_size=2, page_sort=[])

    first_item = iterator.first()
    assert first_item.name == "item_0"
    assert mock_list_function.call_count == 1

    # Calling first again should re-initialize and get the first item again
    first_item = iterator.first()
    assert first_item.name == "item_0"
    assert mock_list_function.call_count == 2


def test_auto_iterator_first_method_empty():
    mock_list_function = MockListFunction(items_per_page=2, total_items=0)
    iterator = AutoIterator(mock_list_function, limit=None, page_size=2, page_sort=[])

    first_item = iterator.first()
    assert first_item is None
    assert mock_list_function.call_count == 1


def test_auto_iterator_all_method():
    mock_list_function = MockListFunction(items_per_page=2, total_items=5)
    iterator = AutoIterator(mock_list_function, limit=None, page_size=2, page_sort=[])

    all_items = iterator.all()
    assert len(all_items) == 5
    assert mock_list_function.call_count == 3
    assert [item.name for item in all_items] == [
        "item_0",
        "item_1",
        "item_2",
        "item_3",
        "item_4",
    ]


def test_auto_iterator_all_method_empty():
    mock_list_function = MockListFunction(items_per_page=2, total_items=0)
    iterator = AutoIterator(mock_list_function, limit=None, page_size=2, page_sort=[])

    all_items = iterator.all()
    assert len(all_items) == 0
    assert mock_list_function.call_count == 1


def test_auto_iterator_wrapper():
    mock_list_function = MockListFunction(items_per_page=2, total_items=5)
    wrapper = AutoIteratorWrapper(mock_list_function)
    iterator = wrapper(limit=3, page_size=2, page_sort=["name"])

    assert isinstance(iterator, AutoIterator)
    assert iterator.limit == 3
    assert iterator.page_size == 2
    assert iterator.page_sort == ["name"]


def test_get_page_on_with_allowed_values():
    mock_list_function = Mock()
    mock_list_function.allowed_values = {("page_on",): {"id": "id", "name": "name"}}
    mock_list_function.params_map = {"all": ["page_on"]}
    assert get_page_on(mock_list_function) == ["id", "name"]


def test_get_page_on_without_allowed_values_but_in_params_map():
    mock_list_function = Mock()
    mock_list_function.allowed_values = {}
    mock_list_function.params_map = {"all": ["page_on"]}
    assert get_page_on(mock_list_function) == ["id"]


def test_get_page_on_not_in_params_map():
    mock_list_function = Mock()
    mock_list_function.allowed_values = {}
    mock_list_function.params_map = {"all": []}
    assert get_page_on(mock_list_function) == []


def test_determine_page_on_preference():
    mock_list_function = Mock()
    mock_list_function.allowed_values = {
        ("page_on",): {"created": "created", "id": "id"}
    }
    mock_list_function.params_map = {"all": ["page_on"]}
    assert _determine_page_on(mock_list_function) == ["created"]


def test_determine_page_on_default():
    mock_list_function = Mock()
    mock_list_function.allowed_values = {("page_on",): {"foo": "foo"}}
    mock_list_function.params_map = {"all": ["page_on"]}
    assert _determine_page_on(mock_list_function) == ["foo"]


def test_determine_page_on_not_implemented():
    mock_list_function = Mock()
    mock_list_function.allowed_values = {}
    mock_list_function.params_map = {"all": []}
    with pytest.raises(NotImplementedError):
        _determine_page_on(mock_list_function)


def test_patch_endpoint():
    mock_list_function = Mock()
    patch_endpoint(mock_list_function)
    assert hasattr(mock_list_function, "auto_paging_iter")
    assert isinstance(mock_list_function.auto_paging_iter, AutoIteratorWrapper)


def test_handle_page_failure_pagination_key_error():
    exc = ApiException(status=400, reason="Bad Request", http_resp=Mock())
    exc.body = '{"error_message": "Invalid pagination key"}'
    with pytest.raises(
        NotImplementedError, match="Pagination not implemented on this key"
    ):
        _handle_page_failure(exc.body)


def test_handle_page_failure_other_400_error():
    exc = ApiException(status=400, reason="Bad Request", http_resp=Mock())
    exc.body = '{"error_message": "Some other error"}'
    with pytest.raises(ApiException):
        try:
            raise exc
        except Exception as exc:
            _handle_page_failure(exc.body)


def test_handle_page_failure_no_body():
    exc = ApiException(status=400, reason="Bad Request", http_resp=Mock())
    exc.body = None
    with pytest.raises(ApiException):
        try:
            raise exc
        except Exception as exc:
            _handle_page_failure(exc.body)


def test_handle_page_failure_invalid_json():
    exc = ApiException(status=400, reason="Bad Request", http_resp=Mock())
    exc.body = "invalid json"
    with pytest.raises(ApiException):
        try:
            raise exc
        except Exception as exc:
            _handle_page_failure(exc.body)


def test_auto_iterator_api_exception_other_status():
    mock_list_function = Mock()
    mock_list_function.allowed_values = {("page_on",): {"foo": "foo"}}
    mock_list_function.params_map = {"all": ["page_on"]}
    mock_list_function.side_effect = ApiException(
        status=500, reason="Internal Server Error"
    )
    iterator = AutoIterator(mock_list_function, limit=None, page_size=2, page_sort=[])

    with pytest.raises(ApiException):
        list(iterator)


def test_auto_iterator_repr():
    mock_list_function = Mock(
        __name__="mock_list_function",
        allowed_values={("page_on",): {"id": "id"}},
        params_map={"all": ["page_on"]},
    )
    iterator = AutoIterator(mock_list_function, limit=None, page_size=2, page_sort=[])
    assert repr(iterator) == "<AutoIterator for mock_list_function>"


def test_auto_patch_endpoint():
    mock_list_function = MockListFunction(items_per_page=2, total_items=5)

    def wrap_list(*args, **kwargs):
        return mock_list_function(**kwargs)

    foo = Endpoint(
        settings={
            "response_type": (ListSSHResourcesResponse,),
            "auth": ["token-valid"],
            "endpoint_path": "/v1/ssh_resources",
            "operation_id": "list_ssh_resources",
            "http_method": "GET",
            "servers": None,
        },
        params_map={
            "all": [
                "page_on",
                "page_at_key",
                "page_sort",
                "search_direction",
            ],
            "required": [],
            "nullable": [],
            "enum": [
                "page_sort",
                "search_direction",
            ],
            "validation": [
                "name",
                "limit",
            ],
        },
        root_map={
            "validations": [],
            "allowed_values": {("page_on,"): ["name"]},
            "openapi_types": {},
            "attribute_map": {},
            "location_map": {},
            "collection_format_map": {},
        },
        callable=wrap_list,
    )

    assert foo.auto_paging_iter is not None
    assert next(foo.auto_paging_iter()).name == "item_0"
