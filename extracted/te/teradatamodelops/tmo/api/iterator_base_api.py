import abc
import json

from tmo.api.api_iterator import ApiIterator
from tmo.api.base_api import BaseApi


class IteratorBaseApi(BaseApi):  # noqa
    __metaclass__ = abc.ABCMeta

    def __init__(self, tmo_client=None, iterator_projection=None, show_archived=True):
        super().__init__(tmo_client=tmo_client)

        self.iterator_projection = iterator_projection

        # Initialize iterator state variables
        # None indicates "not yet fetched from backend"
        # 0 indicates "fetched and result is empty"
        self._iterator_total_elements = None
        self._iterator_total_pages = None
        self._iterator_cache = []

        if show_archived:
            self.iterator_func = self.find_all
        else:
            self.iterator_func = self.find_by_archived

    def __iter__(self):
        return ApiIterator(
            api_func=self.iterator_func,
            entities=list(filter(str.strip, self.path.split("/")))[-1],
            projection=self.iterator_projection,
            api_instance=self,
        )

    def __len__(self):
        """
        Return the total number of elements available from the backend.
        If the iterator has not yet been used to fetch any data (and thus
        `_iterator_total_elements` has not been populated from the API
        response), this method will trigger a minimal fetch by advancing
        a temporary iterator once. This preserves the historical behavior
        where `len(api)` reflects the actual backend count rather than
        always returning the initial value of 0.
        """
        if self._iterator_total_elements is None:
            # Trigger a single fetch to populate pagination info via
            # `set_iterator_page_info`, without affecting any external
            # iteration state.
            iterator = iter(self)
            try:
                next(iterator)
            except StopIteration:
                # No elements available; total remains 0.
                pass

        return (
            self._iterator_total_elements
            if self._iterator_total_elements is not None
            else 0
        )

    def set_iterator_page_info(self, page_info: dict):
        """
        Set pagination information for the iterator from API response.

        Parameters:
            page_info (dict): Dictionary containing 'totalElements' and 'totalPages'
        """
        if page_info:
            self._iterator_total_elements = page_info.get("totalElements", 0)
            self._iterator_total_pages = page_info.get("totalPages", 0)

    def set_iterator_cache(self, cache: list):
        """
        Set cache data for the iterator.

        Parameters:
            cache (list): List of items to cache
        """
        self._iterator_cache = cache if cache else []

    def __repr__(self) -> str:
        """
        Returns a simple, side-effect free representation of the iterator API.
        This method intentionally avoids calling ``len(self)`` because
        ``__len__`` may trigger a backend fetch to populate pagination
        information. Instead, it uses the cached ``_iterator_total_elements``
        value directly and falls back to ``'unknown'`` if the total number
        of elements has not yet been populated from the backend (None).
        A value of 0 indicates a known empty result.
        Returns:
            str: Simple string representation
        """
        class_name = self.__class__.__name__
        total_elements = getattr(self, "_iterator_total_elements", None)
        if total_elements is None:
            # Total elements have not yet been populated from the backend,
            # so avoid triggering a fetch here and show an 'unknown' marker.
            total_display = "unknown"
        else:
            # Display the actual value (including 0 for known empty results)
            total_display = total_elements
        return f"{class_name}(total_elements={total_display})"

    def __str__(self) -> str:
        """
        Returns a pretty JSON representation of all items in the iterator.
        This method materializes all items by iterating through them.

        Returns:
            str: Pretty JSON representation of all items
        """
        try:
            # Materialize all items
            items = list(self)

            # Convert items to dictionaries
            items_dict = []
            for item in items:
                if hasattr(item, "to_dict"):
                    items_dict.append(item.to_dict())
                else:
                    # Fallback to string representation
                    items_dict.append(str(item))

            # Return pretty JSON
            result = {
                "total": len(items_dict),
                "items": items_dict,
            }
            return json.dumps(result, indent=2, default=str)

        except Exception as e:
            # Fallback to simple representation on error
            return json.dumps(
                {
                    "class": self.__class__.__name__,
                    "error": f"Error generating JSON representation: {str(e)}",
                },
                indent=2,
            )
