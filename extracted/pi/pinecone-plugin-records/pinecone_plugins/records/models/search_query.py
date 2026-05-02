from typing import NamedTuple, Optional, Any, Dict, Union
from .search_query_vector import SearchQueryVector


class SearchQuery(NamedTuple):
    """
    SearchQuery represents the query when searching within a specific namespace.
    """

    inputs: Dict[str, Any]
    """
    The input data to search with.
    Required.
    """

    top_k: int
    """
    The number of results to return with each search.
    Required.
    """

    filter: Optional[Dict[str, Any]] = None
    """
    The filter to apply to the search.
    Optional.
    """

    vector: Optional[Union[Dict[str, Any], SearchQueryVector]] = None
    """
    The vector values to search with. If provided, it overwrites the inputs.
    """

    id: Optional[str] = None
    """
    The unique ID of the vector to be used as a query vector.
    """

    def as_dict(self):
        """
        Returns the SearchQuery as a dictionary.
        """
        return self._asdict()
