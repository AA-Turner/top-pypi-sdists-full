from __future__ import absolute_import


class ApiIterator(object):
    _pos = 0
    _current_page = 0

    def __init__(
        self,
        api_func=None,
        entities: str = None,
        projection: str = None,
        page_size: int = None,
        sort: str = None,
    ):
        if api_func is not None and entities is not None:
            self._api_func = api_func
            self._projection = projection
            self._page_size = page_size
            self._sort = sort
            page_info = api_func(
                projection=projection, page=0, size=page_size, sort=sort
            )["page"]
            self._total_elements = page_info["totalElements"]
            self._total_pages = page_info["totalPages"]
            self._cache = api_func(
                projection=projection, page=0, size=page_size, sort=sort
            )["_embedded"][entities]
            self._entities = entities

    def __next__(self):
        if self._pos < len(self._cache):
            result = self._cache[self._pos]
            self._pos += 1
            return result
        elif self._current_page < self._total_pages - 1:
            self._current_page += 1
            self._pos = 1  # so we skip the first one in next iteration
            self._cache = self._api_func(
                projection=self._projection,
                page=self._current_page,
                size=self._page_size,
                sort=self._sort,
            )["_embedded"][self._entities]
            return self._cache[0]
        else:
            raise StopIteration

    def __iter__(self):
        return self
