from typing import NamedTuple, Optional, List, Any


class SearchQueryVector(NamedTuple):
    """
    SearchQueryVector represents the vector values used to query.
    """

    values: Optional[List[float]] = None
    """
    The vector data included in the search request.
    Optional.
    """

    sparse_values: Optional[List[float]] = None
    """
    The sparse embedding values to search with.
    Required.
    """

    sparse_indices: Optional[List[int]] = None
    """
    The sparse embedding indices to search with.
    Optional.
    """

    def as_dict(self):
        """
        Returns the SearchQueryVector as a dictionary.
        """
        return self._asdict()
