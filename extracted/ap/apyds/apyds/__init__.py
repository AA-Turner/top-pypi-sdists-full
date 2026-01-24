"""Python wrapper for a deductive system implemented in C++.

Provides classes and functions for working with logical terms, rules, and inference.
"""

__all__ = [
    "buffer_size",
    "scoped_buffer_size",
    "String",
    "Variable",
    "Item",
    "List",
    "Term",
    "Rule",
    "Search",
]

from .buffer_size import buffer_size, scoped_buffer_size
from .string_t import String
from .variable_t import Variable
from .item_t import Item
from .list_t import List
from .term_t import Term
from .rule_t import Rule
from .search_t import Search
