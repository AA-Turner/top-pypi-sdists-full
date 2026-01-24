"""
AutoIterator for paginating API client list functions.
"""

import json
from agilicus_api.exceptions import ApiException

_page_on_preference = ["name", "created", "id"]
_default_page_on = "id"


def get_page_on(list_function):
    """
    tries to figure out the pagination key to use based on the endpoint:
     - If it's an enum, uses the preferred one in the list, otherwise the first
     - If it's not an enum, just tries the 'default', which is id.
    """
    # yes, the key here is a tuple or some reason
    result = list(list_function.allowed_values.get(("page_on",), {}).values())
    if not result and "page_on" in list_function.params_map["all"]:
        return [_default_page_on]
    return result


def _determine_page_on(list_function):
    page_on_list = get_page_on(list_function)
    if not page_on_list:
        raise NotImplementedError("pagination not implemented on this endpoint")
    for page_on in _page_on_preference:
        if page_on in page_on_list:
            return [page_on]

    return [page_on_list[0]]


def patch_endpoint(list_function):
    setattr(list_function, "auto_paging_iter", AutoIteratorWrapper(list_function))


class AutoIteratorWrapper:
    def __init__(self, list_function):
        self.list_function = list_function

    def __call__(self, *args, limit=None, page_size=100, page_sort=None, **kwargs):
        return AutoIterator(
            self.list_function, limit, page_size, page_sort, *args, **kwargs
        )


class AutoIterator:
    PLACE_HOLDER = object()

    def __init__(
        self,
        list_function,
        limit,
        page_size,
        page_sort,
        *args,
        page_on=None,
        legacy_pagination=False,
        **kwargs,
    ):
        """
        Initializes the AutoIterator.

        :param list_function: The API client list function to paginate.
        :param args: Positional arguments to pass to the list_function.
        :param kwargs: Keyword arguments to pass to the list_function.
        """
        self._list_function = list_function
        self._args = args
        self._kwargs = kwargs
        self.page_sort = page_sort or []
        self.limit = limit
        self.page_size = page_size
        self.legacy_pagination = legacy_pagination
        if not self.legacy_pagination:
            self.configured_page_on = page_on or _determine_page_on(self._list_function)
        else:
            self.configured_page_on = page_on or "page_at_id"
        self._reset()

    def _reset(self):
        self._total_items = 0
        self._page_on = self.configured_page_on
        if self.legacy_pagination:
            self._next_page = ""
        else:
            self._next_page = []
        self._has_more = True
        self._current_page_items = []

    def __iter__(self):
        """
        Returns the iterator object itself.
        """
        return self

    def __next__(self):
        """
        Fetches the next item from the paginated results.
        """
        if not self._current_page_items and self._has_more:
            self._fetch_next_page()

        if self._current_page_items:
            return self._current_page_items.pop(0)
        else:
            raise StopIteration

    def _get_page_list(self, response):
        for key in response.attribute_map:
            if isinstance(response.get(key), list):
                return response.get(key)
        return []

    def _build_page_params(self):
        params = {}
        if self.legacy_pagination:
            params[self.configured_page_on] = self._next_page
        else:
            params["page_on"] = self._page_on
            params["page_at_key"] = self._next_page
            params["page_sort"] = self.page_sort
        return params

    def _fetch_next_page(self):
        limit = self.page_size
        if self.limit is not None:
            limit = min(limit, self.limit - self._total_items)
        page_params = self._build_page_params()
        params = self._kwargs | page_params
        try:
            response = self._list_function(
                limit=limit,
                **params,
            )
        except ApiException as exc:
            if exc.status != 400:
                raise

            _handle_page_failure(exc.body)
            # Shut up the linter, which thinks the above doesn't always throw even
            # though it does
            assert False

        self._current_page_items = self._get_page_list(response)
        self._total_items = self._total_items + len(self._current_page_items)
        if not self._build_next_page(response):
            self._has_more = False
            return

    def _build_next_page(self, response):
        if not self._current_page_items or (
            self.limit and self._total_items >= self.limit
        ):
            return False

        if self.legacy_pagination:
            if len(self._current_page_items) < self.page_size:
                return False
            next_page = response.get(self.configured_page_on, self.PLACE_HOLDER)
            if next_page is self.PLACE_HOLDER:
                return False
            self._next_page = next_page
            return True

        page_info = response.page_info
        if not page_info:
            return False

        self._next_page = page_info.page_at_key
        self._page_on = page_info.page_on.value
        return True

    # Additional functionality when interacted with as an object
    def all(self):
        """
        Returns all items by iterating through all pages.
        """
        all_items = []
        for item in self:
            all_items.append(item)
        return all_items

    def first(self):
        """
        Returns the first item, or None if no items.
        """
        self._reset()
        try:
            return next(self)
        except StopIteration:
            return None

    def __repr__(self):
        return f"<AutoIterator for {self._list_function.__name__}>"


def _handle_page_failure(body):
    if not body:
        raise
    result = {}
    try:
        result = json.loads(body)
    except Exception:
        pass
    error_message = result.get("error_message", "")
    if "pagination key" not in error_message:
        raise

    raise NotImplementedError("Pagination not implemented on this key") from None
