from __future__ import absolute_import


class ApiIterator(object):
    _pos = 0
    _current_page = 0
    entities_container = "_embedded"

    def __init__(
        self,
        api_func=None,
        entities: str = None,
        projection: str = None,
        page_size: int = None,
        sort: str = None,
        api_instance=None,
    ):
        self._api_instance = api_instance
        self._api_func = api_func
        self._projection = projection
        self._page_size = page_size
        self._sort = sort
        self._entities = entities

        # Initialize with defaults
        self._total_elements = 0
        self._total_pages = 0
        self._cache = []

        # Load pagination data from available sources
        self._initialize_pagination_data(
            api_func, entities, projection, page_size, sort, api_instance
        )

    def __next__(self):
        if self._pos < len(self._cache):
            result = self._cache[self._pos]
            self._pos += 1
            return result
        elif (
            self._total_pages is not None and self._current_page < self._total_pages - 1
        ):
            self._current_page += 1
            self._pos = 1  # so we skip the first one in next iteration

            # Fetch next page
            next_page_result = self._api_func(
                projection=self._projection,
                page=self._current_page,
                size=self._page_size,
                sort=self._sort,
            )

            # Handle both legacy dict and new list results
            if self._is_legacy_dict_result(next_page_result):
                self._cache = next_page_result[self.entities_container][self._entities]
            elif isinstance(next_page_result, list):
                self._cache = next_page_result
            else:
                raise StopIteration

            if not self._cache:
                raise StopIteration
            return self._cache[0]
        else:
            raise StopIteration

    def __iter__(self):
        return self

    @staticmethod
    def _can_fetch_data(api_func, entities):
        """
        Checks if we have the necessary parameters to fetch data.

        Args:
            api_func: Function to call for fetching data
            entities: Entity type name

        Returns:
            bool: True if data can be fetched
        """
        return api_func is not None and entities is not None

    def _fetch_and_process_data(
        self, api_func, entities, projection, page_size, sort, api_instance
    ):
        """
        Fetches data using api_func and processes the result.

        Args:
            api_func: Function to call for fetching data
            entities: Entity type name for legacy API
            projection: Projection parameter
            page_size: Page size parameter
            sort: Sort parameter
            api_instance: API instance that may receive cached data
        """
        try:
            result = api_func(projection=projection, page=0, size=page_size, sort=sort)
            self._process_api_result(result, entities, api_instance)
        except (KeyError, TypeError):
            self._handle_fetch_error(api_instance)

    def _handle_fetch_error(self, api_instance):
        """
        Handles errors during data fetching by trying to load from api_instance.

        Args:
            api_instance: API instance to load data from
        """
        if api_instance is not None:
            self._load_from_cache(api_instance)

    @staticmethod
    def _has_cached_data(api_instance):
        """
        Checks if api_instance has pre-cached iterator data.

        Args:
            api_instance: API instance to check

        Returns:
            bool: True if cached data exists
        """
        if api_instance is None:
            return False

        if not hasattr(api_instance, "_iterator_cache"):
            return False

        cache = getattr(api_instance, "_iterator_cache", [])
        return len(cache) > 0

    def _initialize_pagination_data(
        self, api_func, entities, projection, page_size, sort, api_instance
    ):
        """
        Initializes pagination data from api_instance cache or by calling api_func.

        Args:
            api_func: Function to call for fetching data
            entities: Entity type name for legacy API
            projection: Projection parameter
            page_size: Page size parameter
            sort: Sort parameter
            api_instance: API instance that may have pre-cached data
        """
        if self._has_cached_data(api_instance):
            self._load_from_cache(api_instance)
        elif self._can_fetch_data(api_func, entities):
            self._fetch_and_process_data(
                api_func, entities, projection, page_size, sort, api_instance
            )

    @staticmethod
    def _is_legacy_dict_result(result):
        """
        Checks if result is a legacy dict with pagination structure.

        Args:
            result: Result to check

        Returns:
            bool: True if legacy dict result
        """
        return isinstance(result, dict) and "page" in result

    def _load_from_cache(self, api_instance):
        """
        Loads pagination data from api_instance cache.

        Args:
            api_instance: API instance with cached data
        """
        self._total_elements = getattr(api_instance, "_iterator_total_elements", 0)
        self._total_pages = getattr(api_instance, "_iterator_total_pages", 0)
        self._cache = getattr(api_instance, "_iterator_cache", [])

    def _load_from_instance_or_result(self, result, api_instance):
        """
        Loads pagination data from api_instance or uses result as fallback.

        Args:
            result: List result
            api_instance: API instance with potential pagination info
        """
        self._total_elements = getattr(
            api_instance, "_iterator_total_elements", len(result)
        )
        self._total_pages = getattr(
            api_instance, "_iterator_total_pages", 1 if result else 0
        )
        self._cache = getattr(api_instance, "_iterator_cache", result)

    def _process_api_result(self, result, entities, api_instance):
        """
        Processes the result from api_func based on its type.

        Args:
            result: Result from api_func (dict or list)
            entities: Entity type name for legacy API
            api_instance: API instance for fallback data
        """
        if self._is_legacy_dict_result(result):
            self._process_legacy_result(result, entities)
        elif isinstance(result, list):
            self._process_list_result(result, api_instance)
        else:
            self._reset_to_defaults()

    def _process_legacy_result(self, result, entities):
        """
        Processes legacy dict result with pagination structure.

        Args:
            result: Dict result with 'page' and '_embedded' keys
            entities: Entity type name
        """
        page_info = result["page"]
        self._total_elements = page_info["totalElements"]
        self._total_pages = page_info["totalPages"]
        self._cache = result[self.entities_container][entities]

    def _process_list_result(self, result, api_instance):
        """
        Processes list result from find_all().

        Args:
            result: List result
            api_instance: API instance that may have pagination info
        """
        if api_instance is not None:
            self._load_from_instance_or_result(result, api_instance)
        else:
            self._use_result_directly(result)

    def _reset_to_defaults(self):
        """Resets pagination data to default values."""
        self._cache = []
        self._total_elements = 0
        self._total_pages = 0

    def _use_result_directly(self, result):
        """
        Uses result directly when no api_instance is available.

        Args:
            result: List result
        """
        self._cache = result
        self._total_elements = len(result)
        self._total_pages = 1 if result else 0
