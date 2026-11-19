"""Definitions of the segment classes."""

from collate_sqlfluff.core.parser.segments.base import (
    BaseSegment,
    SourceFix,
    UnparsableSegment,
)
from collate_sqlfluff.core.parser.segments.bracketed import BracketedSegment
from collate_sqlfluff.core.parser.segments.common import (
    BinaryOperatorSegment,
    CodeSegment,
    CommentSegment,
    ComparisonOperatorSegment,
    CompositeBinaryOperatorSegment,
    CompositeComparisonOperatorSegment,
    IdentifierSegment,
    LiteralSegment,
    NewlineSegment,
    SymbolSegment,
    UnlexableSegment,
    WhitespaceSegment,
    WordSegment,
)
from collate_sqlfluff.core.parser.segments.file import BaseFileSegment
from collate_sqlfluff.core.parser.segments.generator import SegmentGenerator
from collate_sqlfluff.core.parser.segments.keyword import (
    KeywordSegment,
    LiteralKeywordSegment,
)
from collate_sqlfluff.core.parser.segments.meta import (
    Dedent,
    EndOfFile,
    ImplicitIndent,
    Indent,
    MetaSegment,
    TemplateLoop,
    TemplateSegment,
)
from collate_sqlfluff.core.parser.segments.raw import RawSegment

__all__ = (
    "BaseSegment",
    "BaseFileSegment",
    "UnparsableSegment",
    "BracketedSegment",
    "SegmentGenerator",
    "RawSegment",
    "CodeSegment",
    "UnlexableSegment",
    "CommentSegment",
    "WhitespaceSegment",
    "NewlineSegment",
    "KeywordSegment",
    "LiteralKeywordSegment",
    "SymbolSegment",
    "MetaSegment",
    "Indent",
    "Dedent",
    "ImplicitIndent",
    "TemplateSegment",
    "EndOfFile",
    "TemplateLoop",
    "SourceFix",
    "IdentifierSegment",
    "LiteralSegment",
    "BinaryOperatorSegment",
    "CompositeBinaryOperatorSegment",
    "ComparisonOperatorSegment",
    "CompositeComparisonOperatorSegment",
    "WordSegment",
)
