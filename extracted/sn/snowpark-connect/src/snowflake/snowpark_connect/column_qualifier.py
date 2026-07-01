#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from __future__ import annotations

from dataclasses import dataclass

from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
)


@dataclass(frozen=True)
class ColumnQualifier:
    parts: tuple[str, ...]

    def __post_init__(self) -> None:
        if not all(isinstance(x, str) for x in self.parts):
            raise TypeError("ColumnQualifier.parts must be strings")

    @property
    def is_empty(self) -> bool:
        return len(self.parts) == 0

    def all_qualified_names(self, name: str) -> list[str]:
        qualifier_parts = self.parts
        qualifier_prefixes = [
            ".".join(quote_name_without_upper_casing(x) for x in qualifier_parts[i:])
            for i in range(len(qualifier_parts))
        ]
        return [f"{prefix}.{name}" for prefix in qualifier_prefixes]

    def to_upper(self):
        return ColumnQualifier(tuple(part.upper() for part in self.parts))

    def matches(self, target: ColumnQualifier) -> bool:
        if self.is_empty or target.is_empty:
            return False
        # If the column has fewer qualifiers than the target, it cannot match
        if len(self.parts) < len(target.parts):
            return False
        return self.parts[-len(target.parts) :] == target.parts
