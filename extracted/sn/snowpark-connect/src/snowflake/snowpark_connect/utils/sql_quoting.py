#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Helpers for safely constructing SQL string literals."""


def quote_single(s: str) -> str:
    """Wrap a string in single quotes for use as a SQL string literal.

    Inner single quotes are escaped by doubling them so that values
    containing apostrophes cannot break out of the literal (which would
    otherwise produce malformed SQL or allow SQL injection).
    """
    return "'" + s.replace("'", "''") + "'"


def escape_sql_comment(comment: str) -> str:
    """Escape ``'`` → ``''`` and ``\\`` → ``\\\\`` for a hand-built SQL COMMENT clause."""
    return str(comment).replace("'", "''").replace("\\", "\\\\")
