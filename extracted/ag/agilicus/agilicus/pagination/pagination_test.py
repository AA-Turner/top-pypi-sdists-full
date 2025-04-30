from .pagination import get_many_entries


class fakeAPI:
    def __init__(self, item_key, page_key, start_page=""):
        self.item_key = item_key
        self.page_key = page_key
        self.pages = {}
        self.next_page = start_page

    def _make_page(self, items, next_page):
        return {
            "limit": len(items),
            self.item_key: items,
            self.page_key: next_page,
        }

    def add_page(self, items, next_page):
        self.pages[self.next_page] = self._make_page(items, next_page)

        self.next_page = next_page

    def do_list(self, **kwargs):
        page = kwargs[self.page_key]
        result = self.pages.get(page)
        if not result:
            return self._make_page([], page)
        return result


def make_test_page(items, item_key, page_key, next_page):
    return {
        "limit": len(items),
        item_key: items,
        page_key: next_page,
    }


def test_get_many_entries_gets_all():
    api = fakeAPI("items", "page_at_id")
    api.add_page([10, 8, 6], 6)
    api.add_page([4, 3, 2], 2)
    api.add_page([1, 0], 0)

    result = get_many_entries(api.do_list, api.item_key, page_size=3)
    assert [10, 8, 6, 4, 3, 2, 1, 0] == result


def test_get_many_entries_limits_to_max():
    api = fakeAPI("items", "page_at_id")
    api.add_page([10, 8, 6], 6)
    api.add_page([4, 3, 2], 2)
    api.add_page([1, 0], 0)

    result = get_many_entries(api.do_list, api.item_key, page_size=3, maximum=4)
    assert [10, 8, 6, 4] == result


def test_get_many_entries_invokes_callback():
    api = fakeAPI("items", "page_at_id")
    api.add_page([10, 8, 6], 6)
    api.add_page([4, 3, 2], 2)
    api.add_page([1, 0], 0)

    calls = []

    def callback():
        calls.append(None)

    result = get_many_entries(
        api.do_list, api.item_key, page_size=3, page_callback=callback
    )
    assert [10, 8, 6, 4, 3, 2, 1, 0] == result
    assert len(calls) == 3


def test_get_many_entries_invokes_callback_with_page():
    api = fakeAPI("items", "page_at_id")
    api.add_page([10, 8, 6], 6)
    api.add_page([4, 3, 2], 2)
    api.add_page([1, 0], 0)

    calls = []

    def callback(page):
        calls.append(page)

    result = get_many_entries(
        api.do_list, api.item_key, page_size=3, page_callback=callback
    )
    assert [10, 8, 6, 4, 3, 2, 1, 0] == result

    assert [[10, 8, 6], [4, 3, 2], [1, 0]] == calls


def test_get_many_entries_invokes_callback_args_but_not_page():
    api = fakeAPI("items", "page_at_id")
    api.add_page([10, 8, 6], 6)
    api.add_page([4, 3, 2], 2)
    api.add_page([1, 0], 0)

    calls = []

    def callback(other=None, arg=None):
        calls.append(None)

    result = get_many_entries(
        api.do_list, api.item_key, page_size=3, page_callback=callback
    )
    assert [10, 8, 6, 4, 3, 2, 1, 0] == result
    assert len(calls) == 3
