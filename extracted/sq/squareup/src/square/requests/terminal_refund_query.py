# This file was auto-generated by Fern from our API Definition.

import typing_extensions
import typing_extensions
from .terminal_refund_query_filter import TerminalRefundQueryFilterParams
from .terminal_refund_query_sort import TerminalRefundQuerySortParams


class TerminalRefundQueryParams(typing_extensions.TypedDict):
    filter: typing_extensions.NotRequired[TerminalRefundQueryFilterParams]
    """
    The filter for the Terminal refund query.
    """

    sort: typing_extensions.NotRequired[TerminalRefundQuerySortParams]
    """
    The sort order for the Terminal refund query.
    """
