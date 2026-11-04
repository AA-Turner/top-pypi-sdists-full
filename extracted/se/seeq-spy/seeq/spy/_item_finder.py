from __future__ import annotations

import datetime
import re
import warnings
from typing import TYPE_CHECKING, Any, Dict, Iterator, List, Optional, Sequence, Union

from seeq.base.seeq_names import SeeqNames
from seeq.sdk import ItemsApi
from seeq.spy import _common
from seeq.spy._errors import SPyValueError
from seeq.spy._session import Session
from seeq.spy._status import Status

if TYPE_CHECKING:
    # The ItemFinder models do not exist in the older SDKs. Every runtime use imports them inside functions, which are
    # guarded by _compatibility checks. The `from __future__ import annotations` also keeps the type hints below lazy.
    from seeq.sdk.models import (AncestorFilterInputV1, ItemFinderSearchesInputV1, ItemSearchPreviewV1,
                                 PropertyFilterInputV1, PropertyInputV1, PropertySearchV1,
                                 TablePropertyFilterInputV1)


# TODO CRAB-52405 Delete Operator and SortOrder when the Python SDK emits named enum constants again.
#  Switch to the generated PropertyFilterInputV1.OperatorEnum / PropertySearchV1.SortOrderEnum.
class Operator:
    """Mirrors ReadItemsQuery.Operator in ItemFinder.kt. Only WITHIN and STRING_CONTAINS accept multiple values."""
    EQUALS = 'EQUALS'
    EQUALS_IGNORE_CASE = 'EQUALS_IGNORE_CASE'
    NOT_EQUALS = 'NOT_EQUALS'
    WITHIN = 'WITHIN'
    STRING_CONTAINS = 'STRING_CONTAINS'
    NOT_STRING_CONTAINS = 'NOT_STRING_CONTAINS'
    REGEX_MATCHES = 'REGEX_MATCHES'
    NOT_REGEX_MATCHES = 'NOT_REGEX_MATCHES'


class SortOrder:
    ASC = 'ASC'
    DESC = 'DESC'


# The only properties ItemFinder can sort by. See ItemSerializer.OrderBy / QueryUtilities.kt:44-53. A GUID
# tiebreaker is appended server-side, so pagination is stable even when the sort field has duplicates.
SORTABLE_PROPERTIES = (SeeqNames.Properties.id, SeeqNames.Properties.name, SeeqNames.Properties.description)

# Item types that live in their own database table and therefore cannot share a single PropertySearch with any other
# type. The server rejects such a search outright (prohibitSpecificExtractedItemTypes, PostgreSqlQueries.java:644).
# The authoritative set is EXTRACTED_TYPES_RESTRICTED_READ_WITH_MULTIPLE_TYPES in PostgreSqlItemSerializer.kt,
# which is computed by reflection over DeserializableExtractedItemModel subclasses; of the types spy.search can return,
# only TableDefinition is restricted (Datasource is extracted but explicitly exempted). If the server ever restricts
# a type we do not list here, the search fails loudly with "Extracted item types '...' are not supported for
# this method" rather than returning wrong results.
# TODO CRAB-66070 Remove this set and the split_types_for_search() fan-out when ItemFinder duplicates a predicate
#  across extracted item types on its own, so that callers can pass every type in one search.
RESTRICTED_EXTRACTED_TYPES = frozenset({'TableDefinition'})

# Properties that the legacy filter grammar matches exactly rather than as a regex. Must match case-insensitive
# property names since that's what the source used.
EXACT_MATCH_PROPERTIES = frozenset({
    SeeqNames.Properties.id.lower(),
    SeeqNames.Properties.formula.lower(),
    SeeqNames.Properties.datasource_class.lower(),
    SeeqNames.Properties.datasource_id.lower(),
    SeeqNames.Properties.data_id.lower(),
    SeeqNames.Properties.cache_id.lower(),
    SeeqNames.Properties.scoped_to.lower(),
    SeeqNames.Properties.table_type.lower(),
    SeeqNames.Properties.table_definition_id.lower(),
})


def is_exact_match_property(property_name: str) -> bool:
    return property_name.lower() in EXACT_MATCH_PROPERTIES


# Properties that the legacy filter grammar parses into a typed value for "==" instead of matching as text, and the
# kind of value each has to parse as. Mirrors NON_STRING_FIELDS in ItemQueriesV1.kt.
_BOOLEAN = 'boolean'
_NUMERIC = 'numeric'
TYPED_MATCH_PROPERTIES = {
    SeeqNames.Properties.cache_enabled.lower(): _BOOLEAN,
    SeeqNames.Properties.archived.lower(): _BOOLEAN,
    SeeqNames.Properties.enabled.lower(): _BOOLEAN,
    SeeqNames.Properties.maximum_interpolation.lower(): _NUMERIC,
    SeeqNames.Properties.maximum_duration.lower(): _NUMERIC,
}

# A number and an optional unit, such as "40", "1.5h" or "2 min". Deliberately simpler than the Value.parse the legacy
# grammar used, which also accepted hex and read some leading zeros as octal. The unit is left as text for the server
# to parse with Scalar.parseUnit, so unit grammar is not reproduced here at all.
_TYPED_NUMBER = re.compile(r'(-?(?:[0-9]+\.?[0-9]*|\.[0-9]+)(?:e[+-]?[0-9]+)?)\s*(.*)', re.IGNORECASE)

# Ported verbatim from Regexes.kt so that the regexes SPy sends to ItemFinder are byte-identical to the ones the
# legacy /items endpoint built server-side from the same user input. "*" and "?" are deliberately not escaped,
# because the globbing logic below turns them into ".*" and ".".
_REGEX_SPECIAL_CHARS = re.compile(r'([.+\-\[\](){}<>^|$#@&~\\"])')
_REGEX_IS_REGEX = re.compile(r'^/.*/[ism]*$', re.DOTALL)


def is_regex_delimited(value: str) -> bool:
    # fullmatch, not match: the Kotlin uses Matcher.matches(), and a trailing newline must not sneak past "$".
    return _REGEX_IS_REGEX.fullmatch(value) is not None


def extract_regex_body(search: str, as_substring: bool) -> str:
    end_index = search.rindex('/')
    regex = search[1:end_index]

    if not as_substring:
        if not regex.startswith('^'):
            regex = f'^{regex}'
        if not regex.endswith('$'):
            regex = f'{regex}$'

    # Users write /.../i for case-insensitivity; Postgres wants the (?i) prefix instead.
    modifiers = search[end_index + 1:]
    return regex if not modifiers else f'(?{modifiers}){regex}'


def convert_input_string_to_regex(search: str, as_substring: bool, case_insensitive: bool = False) -> str:
    """Python port of Regexes.convertInputStringToRegex. Keep in lockstep with the Kotlin."""
    if not search:
        return '.*' if as_substring else ''

    if is_regex_delimited(search):
        return extract_regex_body(search, as_substring)

    regex = _REGEX_SPECIAL_CHARS.sub(r'\\\1', search)
    regex = regex.replace('*', '.*').replace('?', '.')

    if not as_substring:
        regex = f'^{regex}$'

    flags = 's'  # all globs should match newline characters
    if case_insensitive:
        flags += 'i'

    return f'(?{flags}){regex}'


def _property_values(values: Sequence) -> List[PropertyInputV1]:
    from seeq.sdk.models import PropertyInputV1

    return [PropertyInputV1(value=value) for value in values]


def predicate(property_name: str, operator: str, *values: Any) -> PropertyFilterInputV1:
    from seeq.sdk.models import PropertyFilterInputV1

    return PropertyFilterInputV1(property_name=property_name, operator=operator, values=_property_values(values))


def to_table_predicate(filter_input: PropertyFilterInputV1) -> TablePropertyFilterInputV1:
    """
    Ancestor predicates take a TablePropertyFilterInputV1, which is a PropertyFilterInputV1 plus an optional
    stored-table column. This restates one as the other so the same clause can filter an item or its ancestor.
    """
    from seeq.sdk.models import TablePropertyFilterInputV1

    return TablePropertyFilterInputV1(property_name=filter_input.property_name, operator=filter_input.operator,
                                      values=list(filter_input.values))


def ancestor_predicate(property_name: str, operator: str, *values: Any,
                       level: Optional[int] = None) -> AncestorFilterInputV1:
    """
    An EXISTS semi-join over the item's ancestors: "this item has an ancestor (at `level`, if given) matching all
    of these predicates". `level` counts upward, so 1 is the direct parent and 2 the grandparent.
    """
    from seeq.sdk.models import AncestorFilterInputV1, TablePropertyFilterInputV1

    table_predicate = TablePropertyFilterInputV1(property_name=property_name, operator=operator,
                                                 values=_property_values(values))
    return AncestorFilterInputV1(level=level, predicates=[table_predicate])


def ancestors_within(ancestor_ids: Sequence[str], *, level: Optional[int] = None) -> AncestorFilterInputV1:
    """
    "Descended from any of these ancestors", equivalent to unioning one ancestorId search per candidate. Only the
    property name ID maps to the seeq_guid column; GUID is not an alias and matches nothing.
    """
    return ancestor_predicate(SeeqNames.Properties.id, Operator.WITHIN, *ancestor_ids, level=level)


def path_ancestor_predicates(ancestor_segments: Sequence[str],
                             root_predicates: Optional[List[TablePropertyFilterInputV1]] = None
                             ) -> List[AncestorFilterInputV1]:
    """
    Pin every leading segment of an asset path to the depth it must sit at, so that one query can resolve a path
    that otherwise takes a round trip per level.

    `level` counts upward from the matched item, so for 'A >> B >> C' the segment B is level 1 and A is level 2.
    `root_predicates` are added to the outermost segment, which is where the legacy walk applied its datasource
    filter.
    """
    predicates = list()

    for depth, segment in enumerate(ancestor_segments, start=1):
        level = len(ancestor_segments) - depth + 1
        matcher = query_fragment_predicate(SeeqNames.Properties.name, segment, contains=False)
        entry = ancestor_predicate(matcher.property_name, matcher.operator,
                                   *[value.value for value in matcher.values], level=level)
        if root_predicates and level == len(ancestor_segments):
            entry.predicates = list(entry.predicates) + list(root_predicates)
        predicates.append(entry)

    return predicates


def _typed_predicate(property_name: str, value: str) -> PropertyFilterInputV1:
    """The "==" branch for TYPED_MATCH_PROPERTIES: an EQUALS on a boolean, or on a number with an optional unit."""
    from seeq.sdk.models import PropertyFilterInputV1, PropertyInputV1

    unit = None
    if TYPED_MATCH_PROPERTIES[property_name.lower()] == _BOOLEAN:
        if value.lower() not in ('true', 'false'):
            raise SPyValueError(f'"{property_name}" must be true or false, not "{value}"')
        parsed = value.lower() == 'true'
    else:
        match = _TYPED_NUMBER.fullmatch(value)
        if match is None:
            raise SPyValueError(f'"{property_name}" must be a number with an optional unit, such as "2 min", '
                                f'not "{value}"')
        number, unit = match.group(1), match.group(2) or None
        parsed = float(number) if any(c in number for c in '.eE') else int(number)

    return PropertyFilterInputV1(property_name=property_name, operator=Operator.EQUALS,
                                 values=[PropertyInputV1(value=parsed, unit_of_measure=unit)])


def legacy_filter_predicate(property_name: str, comparison: str, value: str) -> Optional[PropertyFilterInputV1]:
    """
    Translate one clause of the legacy `filters` grammar (`Name==foo`, `Name~=/bar/`) into the equivalent
    ItemFinder predicate, following what ItemQueriesV1.filtersStringToSearchablePairs did server-side.

    Returns None for an empty or whitespace-only value, which is no filter at all, so callers must leave it out.

    `==` is a typed EQUALS for TYPED_MATCH_PROPERTIES, an exact match for EXACT_MATCH_PROPERTIES, and an anchored,
    case-sensitive regex for everything else. `~=` is a case-insensitive substring match, except that a value
    containing a glob is anchored.
    """
    if comparison not in ('==', '~='):
        raise SPyValueError(f'Unrecognized filter comparison "{comparison}", expected "==" or "~="')

    # The legacy grammar trims too, so a stray space around a pasted name still matches.
    value = value.strip()
    if not value:
        return None

    if comparison == '==':
        if property_name.lower() in TYPED_MATCH_PROPERTIES:
            return _typed_predicate(property_name, value)

        if is_exact_match_property(property_name):
            return predicate(property_name, Operator.EQUALS, value)

        return predicate(property_name, Operator.REGEX_MATCHES, convert_input_string_to_regex(value, False, False))

    # A plain (non-glob, non-regex) contains-match is what STRING_CONTAINS does via likeIgnoreCase('%v%'), and
    # unlike a regex it can use an index, so prefer it.
    if '*' not in value and '?' not in value and not is_regex_delimited(value):
        return predicate(property_name, Operator.STRING_CONTAINS, value)

    return predicate(property_name, Operator.REGEX_MATCHES,
                     convert_input_string_to_regex(value, '*' not in value, True))


def legacy_filter_predicates(clauses: Dict[str, tuple]) -> List[PropertyFilterInputV1]:
    """
    legacy_filter_predicate() over {property name: (comparison, value)}, leaving out the clauses it drops. This is
    what a caller wants for a whole query, so the rule for which clauses vanish stays in one place.
    """
    translated = (legacy_filter_predicate(name, comparison, value) for name, (comparison, value) in clauses.items())
    return [p for p in translated if p is not None]


def query_fragment_predicate(property_name: str, fragment: str, *, contains: bool = True) -> PropertyFilterInputV1:
    """
    The server-side equivalent of _common.does_query_fragment_match, which SPy uses to filter tree results and
    match path segments client-side. That helper is not the legacy filter grammar: it is regex_from_query_fragment
    followed by a case-insensitive re.fullmatch with no DOTALL, so this reuses regex_from_query_fragment itself
    rather than the Regexes.kt port.

    A bare fragment becomes an EQUALS_IGNORE_CASE, and a bare contains-fragment a STRING_CONTAINS. A glob or a regex
    becomes a REGEX_MATCHES that states what fullmatch does implicitly.
    """
    is_regex = fragment.startswith('/') and fragment.endswith('/')  # regex_from_query_fragment's own test
    is_glob = '*' in fragment or '?' in fragment

    if not is_regex and not is_glob:
        return predicate(property_name, Operator.STRING_CONTAINS if contains else Operator.EQUALS_IGNORE_CASE,
                         fragment)

    regex = _common.regex_from_query_fragment(fragment, contains=contains)

    # PostgreSQL "~" is an unanchored, case-sensitive search in which "." matches a newline, whereas fullmatch has
    # to consume the whole string, ignores case, and stops "." at a newline. Grouping before anchoring keeps an
    # alternation such as /foo|bar/ from anchoring only its outer branches. The "p" option is PostgreSQL's partial
    # newline-sensitive mode, the closest it has to Python's default. It also keeps a negated bracket expression
    # such as [^a] from matching a newline, which Python would allow, but only an item name containing a newline
    # could tell the two apart.
    return predicate(property_name, Operator.REGEX_MATCHES, f'(?ip)^(?:{regex})$')


def unsearchable_predicate(include_unsearchable: bool) -> Optional[PropertyFilterInputV1]:
    """
    ItemFinders exclude unsearchable items by default due to an implicit `Unsearchable NOT_EQUALS true`. Adding an
    explicit `Unsearchable WITHIN [true, false]` suppresses that and returns all items regardless of searchability.
    This, in conjunction with including archived items, is equivalent to the legacy '@includeUnsearchable' filter.
    """
    if not include_unsearchable:
        return None

    return predicate(SeeqNames.Properties.unsearchable, Operator.WITHIN, True, False)


def archived_predicate(include_archived: bool) -> Optional[PropertyFilterInputV1]:
    """
    ItemFinders exclude archived items by default due to an implicit `Archived NOT_EQUALS true`. Adding an
    explicit `Archived WITHIN [true, false]` suppresses that and returns all items regardless of archival status.
    This, in conjunction with including unsearchable items, is equivalent to the legacy '@includeUnsearchable' filter.
    """
    if not include_archived:
        return None

    return predicate(SeeqNames.Properties.archived, Operator.WITHIN, True, False)


def split_types_for_search(types: Sequence[str]) -> List[List[str]]:
    """
    Group types into the smallest number of property searches the server will accept. Base types expand to their
    subtypes server-side (isSubtypesIncluded defaults true), so ['Signal'] already finds StoredSignal and
    CalculatedSignal. Callers should pass base types rather than enumerating subtypes.
    """
    shareable = [item_type for item_type in types if item_type not in RESTRICTED_EXTRACTED_TYPES]
    restricted = [item_type for item_type in types if item_type in RESTRICTED_EXTRACTED_TYPES]

    groups = [[item_type] for item_type in restricted]
    if shareable:
        groups.insert(0, shareable)

    return groups


class ItemFinderQueryBuilder:
    """
    Assembles an ItemFinderSearchesInputV1. Splits types the server will not let share a search and phrases the
    archived and unsearchable opt-ins as predicates, so that call sites can describe what they want rather than how
    ItemFinder needs it phrased.
    """

    def __init__(self, *, limit: Optional[int] = None, include_properties: Optional[List[str]] = None,
                 include_all_properties: bool = False):
        self.limit = limit
        self.include_properties = include_properties
        self.include_all_properties = include_all_properties
        self.property_searches: List[PropertySearchV1] = list()

    def add_item_search(self, *, types: Sequence[str], predicates: Optional[List[PropertyFilterInputV1]] = None,
                        ancestor_id: Optional[str] = None,
                        ancestor_predicates: Optional[List[AncestorFilterInputV1]] = None,
                        level: Optional[int] = None, folder_id: Optional[str] = None,
                        sort_field: Optional[str] = None, sort_order: str = SortOrder.ASC,
                        include_archived: bool = False, include_unsearchable: bool = False,
                        is_include: bool = True, search_order: Optional[int] = None) -> ItemFinderQueryBuilder:
        from seeq.sdk.models import PropertySearchV1

        if not types:
            raise SPyValueError('At least one item type must be specified for an ItemFinder property search')

        if sort_field is not None and sort_field not in SORTABLE_PROPERTIES:
            raise SPyValueError(f'ItemFinder cannot sort by "{sort_field}", only {", ".join(SORTABLE_PROPERTIES)}')

        # An IF search with no sort order cannot be paginated. Default to ID so the server can return pages
        if sort_field is None:
            sort_field = SeeqNames.Properties.id

        base_predicates = list(predicates) if predicates else list()

        for opt_in in [unsearchable_predicate(include_unsearchable), archived_predicate(include_archived)]:
            if opt_in is not None:
                base_predicates.append(opt_in)

        for type_group in split_types_for_search(types):
            self.property_searches.append(PropertySearchV1(
                types=list(type_group),
                predicates=list(base_predicates) if base_predicates else None,
                ancestor_id=ancestor_id,
                ancestor_predicates=list(ancestor_predicates) if ancestor_predicates else None,
                level=level,
                folder_id=folder_id,
                sort_field=sort_field,
                sort_order=sort_order,
                is_include=is_include,
                search_order=search_order))

        return self

    def build(self, continuation_token: Optional[str] = None) -> ItemFinderSearchesInputV1:
        from seeq.sdk.models import ItemFinderSearchesInputV1

        if not self.property_searches:
            raise SPyValueError('An ItemFinder search requires at least one include search')

        # A FixedListSearchV1 is the other kind of include an ItemFinder search can carry. Nothing in SPy builds
        # one yet, so this does not either; see the TODO on CRAB-66331 in SearchByIDHelper for when that changes.
        return ItemFinderSearchesInputV1(
            property_searches=self.property_searches,
            include_properties=self.include_properties,
            include_all_properties=self.include_all_properties,
            limit=self.limit,
            continuation_token=continuation_token)


class ItemFinderPager:
    """
    Walks the ItemFinder search endpoint's continuation tokens, yielding one ItemSearchPreviewV1 at a time. The token
    is fingerprinted to the exact searches and limit that produced it, so neither may change mid-walk.
    """

    def __init__(self, session: Session, query: Union[ItemFinderQueryBuilder, ItemFinderSearchesInputV1], *,
                 status: Optional[Status] = None, status_index: Optional[int] = None,
                 timer: Optional[datetime.datetime] = None):
        self.session = session
        self.query = query
        self.status = status
        self.status_index = status_index
        self.timer = timer
        self.items_api = ItemsApi(session.client)
        self.page_count = 0

    def _input(self, continuation_token: Optional[str]) -> ItemFinderSearchesInputV1:
        if isinstance(self.query, ItemFinderQueryBuilder):
            return self.query.build(continuation_token)

        self.query.continuation_token = continuation_token
        return self.query

    def _report_progress(self, count: int, warnings: Optional[List[str]]) -> None:
        if self.status is None:
            return

        for warning in warnings or []:
            self.status.warn(warning)

        if self.status_index is None:
            return

        if self.timer is not None:
            self.status.df.at[self.status_index, 'Time'] = _common.timer_elapsed(self.timer)
        self.status.df.at[self.status_index, 'Count'] = count
        self.status.df.at[self.status_index, 'Pages'] += 1
        self.status.df.at[self.status_index, 'Result'] = 'Querying'
        self.status.update('Querying Seeq Server for items', Status.RUNNING)

    def __iter__(self) -> Iterator[ItemSearchPreviewV1]:
        continuation_token = None
        yielded = 0

        while True:
            with warnings.catch_warnings():
                # The SDK wraps this experimental endpoint in a deprecation decorator. SPy opts into it
                # deliberately, so the warning is noise for the user, and an error wherever warnings are escalated.
                warnings.simplefilter('ignore', DeprecationWarning)
                output = self.items_api.execute_item_finder_searches_v2(body=self._input(continuation_token))
            self.page_count += 1

            items = output.items or list()
            self._report_progress(yielded + len(items), output.warnings)

            for item in items:
                yield item
                yielded += 1

            continuation_token = output.continuation_token
            if not output.has_more or not continuation_token:
                return
