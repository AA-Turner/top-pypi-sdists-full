"""
Model for Jobs API filter conditions.
Used with POST /jobs/_search for advanced filtering.
"""

from typing import Union, Optional


class JobFilter:
    """
    Represents a single filter condition for querying jobs.

    Allowed comparators: =, !=, >, <, LIKE, NOT LIKE, ILIKE, NOT ILIKE
    Allowed joiners: AND (default), OR
    """

    ALLOWED_COMPARATORS = frozenset({'=', '!=', '>', '<', 'LIKE', 'NOT LIKE', 'ILIKE', 'NOT ILIKE'})
    ALLOWED_JOINERS = frozenset({'AND', 'OR'})

    def __init__(self,
                 key: str,
                 comparator: str,
                 value: Union[str, int, bool],
                 joiner: Optional[str] = 'AND'):
        """
        :param key: Column name to filter on (e.g. status, type, params.workflowId)
        :param comparator: Comparison operator (=, !=, >, <, LIKE, NOT LIKE, ILIKE, NOT ILIKE)
        :param value: Filter value
        :param joiner: How to join with next filter (AND or OR). Default AND.
        """
        self.key = key
        self.comparator = comparator
        self.value = value
        self.joiner = joiner or 'AND'

        if self.comparator not in self.ALLOWED_COMPARATORS:
            raise ValueError(
                f"Invalid comparator '{comparator}'. "
                f"Allowed: {', '.join(sorted(self.ALLOWED_COMPARATORS))}"
            )
        if self.joiner not in self.ALLOWED_JOINERS:
            raise ValueError(
                f"Invalid joiner '{joiner}'. Allowed: {', '.join(self.ALLOWED_JOINERS)}"
            )

    def to_json(self) -> dict:
        """Serialize to API request format."""
        return {
            'key': self.key,
            'comparator': self.comparator,
            'value': self.value,
            'joiner': self.joiner,
        }
