import re

import sqlparse
from sqlparse import tokens
from sqlparse.keywords import KEYWORDS, SQL_REGEX

# sqlparse 0.5.4 introduced DoS protection with conservative defaults (depth=100,
# tokens=10000). Real-world enterprise SQL regularly exceeds those limits, causing
# silently truncated parse trees and wrong lineage. Values here are set to 100x the
# defaults to handle large production queries. Raise further if lineage is missing on
# unusually large or deeply nested SQL.
sqlparse.engine.grouping.MAX_GROUPING_DEPTH = 10000
sqlparse.engine.grouping.MAX_GROUPING_TOKENS = 1000000


def _patch_adding_builtin_type() -> None:
    KEYWORDS["STRING"] = tokens.Name.Builtin
    KEYWORDS["DATETIME"] = tokens.Name.Builtin


def _patch_updating_lateral_view_lexeme() -> None:
    for i, (regex, lexeme) in enumerate(SQL_REGEX):
        rgx = re.compile(regex, re.IGNORECASE | re.UNICODE).match
        if rgx("LATERAL VIEW EXPLODE(col)"):
            new_regex = r"(LATERAL\s+VIEW\s+)(OUTER\s+)?(EXPLODE|INLINE|PARSE_URL_TUPLE|POSEXPLODE|STACK|JSON_TUPLE)\b"
            SQL_REGEX[i] = (new_regex, lexeme)
            break


def _monkey_patch() -> None:
    _patch_adding_builtin_type()
    _patch_updating_lateral_view_lexeme()


_monkey_patch()
