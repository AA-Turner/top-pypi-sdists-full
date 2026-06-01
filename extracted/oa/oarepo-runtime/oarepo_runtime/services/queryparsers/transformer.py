#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Transformers for query parsing."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from luqum.auto_head_tail import auto_head_tail
from luqum.parser import parser
from luqum.tree import Phrase, Term, Word
from luqum.visitor import TreeTransformer

if TYPE_CHECKING:
    from collections.abc import Generator

    from luqum.tree import Item

ILLEGAL_ELASTICSEARCH_CHARACTERS = {
    "\\",
    "/",
    "+",
    "&&",
    "||",
    "!",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "^",
    '"',
    "~",
    "*",
    "?",
    ":",
}

ILLEGAL_START_ELASTICSEARCH_CHARACTERS = {"-"}
ILLEGAL_ELASTICSEARCH_CHARACTERS_REGEX = r'[\\\/\+\!\(\)\{\}\[\]\^"~\*\?:]|&&|\|\|'
ILLEGAL_START_ELASTICSEARCH_CHARACTERS_REGEX = r"^\-"

SEARCH_FIELD_EDGE_CASES_REGEX = r"https?://|doi:|handle:|oai:https://"


def _get_phrase(val: str) -> Phrase:
    val = val.replace('"', '\\"').replace("'", "\\'")
    return Phrase(f'"{val}"')


class SearchQueryValidator(TreeTransformer):
    """Validate search terms for illegal Elasticsearch characters."""

    def __init__(self, mapping: Any, allow_list: Any, *args: Any, **kwargs: Any):
        """Initialize the transformer."""
        _, _ = mapping, allow_list  # currently unused
        super().__init__(*args, **kwargs)

    def visit(self, tree: Item, context: dict[str, Any] | None = None) -> Item:
        """Transform the tree."""
        query_str = str(auto_head_tail(tree))
        if re.search(SEARCH_FIELD_EDGE_CASES_REGEX, query_str):
            query_str = re.sub(
                r"(https?://)\s", r"\1", query_str
            )  # luqum breaks https://.+ into SearchField(http, Regex(//)) and Word/Phrase(.+);
            new_words = []
            words = query_str.split()
            for word in words:
                if re.search(SEARCH_FIELD_EDGE_CASES_REGEX, word):
                    new_words.append(_get_phrase(word).value)
                else:
                    new_words.append(word)
            new_query_string = " ".join(new_words)
            tree = parser.parse(new_query_string)
        return super().visit(tree, context=context)

    def visit_word(self, node: Word, context: Any) -> Generator[Term]:
        """Transform the word node."""
        # unused context here but keeping the signature required by luqum visitor
        _ = context
        val = node.value

        # convert to phrase if the value contains an illegal elasticsearch character
        if re.search(ILLEGAL_ELASTICSEARCH_CHARACTERS_REGEX, val) or re.search(
            ILLEGAL_START_ELASTICSEARCH_CHARACTERS_REGEX, val
        ):
            # Only \" is valid escape in ES phrases; single quotes don't need escaping
            yield _get_phrase(val)
            return

        yield node
