from __future__ import annotations

import datetime
import types
from dataclasses import dataclass
from typing import Callable, List, Dict, Union, Mapping, Optional, Set, Tuple

import pandas as pd

from seeq import spy
from seeq.base.seeq_names import SeeqNames
from seeq.sdk import *
from seeq.spy import _common, _compatibility, _item_finder, _login, _metadata, _swap, _version
from seeq.spy._context import WorkbookContext
from seeq.spy._errors import *
from seeq.spy._item_finder import ItemFinderPager, ItemFinderQueryBuilder
from seeq.spy._redaction import safely, request_safely
from seeq.spy._session import Session
from seeq.spy._status import Status

RESERVED_SEARCH_COLUMN_NAMES = ['Path', 'Asset', 'Type', 'Depth', 'Estimated Sample Period', 'Formula Parameters',
                                'Datasource Name']

VALID_ITEM_TYPES_FOR_SEARCH = [
    SeeqNames.Types.stored_signal, SeeqNames.Types.calculated_signal,
    SeeqNames.Types.stored_condition, SeeqNames.Types.calculated_condition,
    SeeqNames.Types.literal_scalar, SeeqNames.Types.calculated_scalar,
    SeeqNames.Types.datasource,
    SeeqNames.Types.threshold_metric, SeeqNames.Types.chart, SeeqNames.Types.asset,
    SeeqNames.Types.workbook, SeeqNames.Types.worksheet,
    SeeqNames.Types.display, SeeqNames.Types.display_template,
    SeeqNames.Types.table_definition
]

# The searchable types that live in their own extracted table. A superset of _item_finder.RESTRICTED_EXTRACTED_TYPES,
# which is only those that cannot share a search with another type.
EXTRACTED_ITEM_TYPES_FOR_SEARCH = [SeeqNames.Types.datasource, SeeqNames.Types.table_definition]

# Clauses that identify a datasource rather than the item itself. When resolving an asset path, these apply only to
# the root of the tree, matching what the legacy tree walk did.
DATASOURCE_CLAUSE_NAMES = (SeeqNames.Properties.datasource_class, SeeqNames.Properties.datasource_id)

# An ItemFinder property search must name its types, so a query with no Type gets this list.
DEFAULT_ITEM_TYPES_FOR_ITEM_FINDER = [t for t in VALID_ITEM_TYPES_FOR_SEARCH
                                      if t not in EXTRACTED_ITEM_TYPES_FOR_SEARCH]

ALL_PROPERTIES = ['@allProperties']

DEFAULT_PROPERTIES = ['ID', 'Path', 'Asset', 'Name', 'Description', 'Type', 'Value Unit Of Measure', 'Datasource Name',
                      'Archived']

PROPERTIES_NEVER_TRANSFORM_TO_STRING = ['Estimated Sample Period', 'Formula Parameters', 'Swappable Assets',
                                        'Thresholds']
PROPERTIES_ALWAYS_TRANSFORM_TO_BOOLEAN = [SeeqNames.Properties.archived,
                                          SeeqNames.Properties.asset_group_member,
                                          SeeqNames.Properties.cache_enabled,
                                          SeeqNames.Properties.enabled,
                                          SeeqNames.Properties.unsearchable,
                                          'Reference']

USE_DEFAULT_LIMIT = -1


@dataclass
class ItemSearchDefinition:
    """
    One query row reduced to the parts that decide what gets matched, independent of which endpoint runs it.

    _process_query() builds this alongside the legacy search_items kwargs. The legacy path keeps reading the
    kwargs; the ItemFinder path renders this instead, so neither has to parse the other's filter strings.
    """
    # Property name -> (comparison, matcher), where comparison is the legacy grammar's '==' or '~='.
    clauses: Dict[str, tuple]
    # Concrete item types, already expanded from the user's Type (so 'Signal' is StoredSignal + CalculatedSignal).
    # Empty means the user did not ask for a type.
    types: List[str]
    include_archived: bool
    # True when the query named a 'Scoped To', which the legacy path expressed as '@excludeGloballyScoped'.
    exclude_globally_scoped: bool = False


@dataclass
class SearchContext:
    session: Session
    status: Status

    include_properties: List[str]
    workbook: str
    recursive: bool
    ignore_unindexed_properties: bool
    include_archived: bool
    estimate_sample_period: dict
    include_swap_info: bool
    old_asset_format: bool
    order_by: Optional[Union[str, list]]
    limit: int

    status_index: int
    columns: List[str]
    metadata: List
    ids: Set
    comparison: str
    dupe_count: int
    sample_periods: Dict
    workbook_id: str
    pd_start: Optional[pd.Timestamp]
    pd_end: Optional[pd.Timestamp]
    use_search_items_api_for_this_query: bool
    used_search_items_api_at_least_once: bool
    use_item_finder: bool
    search_definition: Optional[ItemSearchDefinition]
    timer: datetime.datetime

    items_api: ItemsApi
    workbooks_api: WorkbooksApi
    trees_api: TreesApi
    formulas_api: FormulasApi
    displays_api: DisplaysApi
    display_templates_api: DisplayTemplatesApi

    search_by_id_helper_for_all_queries: SearchByIDHelper
    search_by_id_helper_for_tree_children: SearchByIDHelper

    def __init__(self, session: Session, status: Status):
        self.session = session
        self.status = status

        self.columns = list()
        self.metadata = list()
        self.ids = set()
        self.datasource_ids = dict()
        self.dupe_count = 0
        self.sample_periods = dict()

        self.use_item_finder = _compatibility.is_item_finder_search_available(session)
        self.search_definition = None

        self.items_api = ItemsApi(session.client)
        self.workbooks_api = WorkbooksApi(session.client)
        self.trees_api = TreesApi(session.client)
        self.formulas_api = FormulasApi(session.client)
        self.displays_api = DisplaysApi(session.client)
        self.display_templates_api = DisplayTemplatesApi(session.client)


# This chosen to not run afoul of Cloudflare's 414 (Request-URI Too Long) error for GET requests
search_by_id_helper_page_size = 500


class SearchByIDHelper:
    """
    In R62 and later, you can supply a list of filters to the search_items API in the form of ID=={ID}. This means we
    can do far fewer round trips to satisfy a query where the user supplies a DataFrame full of IDs. This class
    issues search_items() calls in pages and caches the results for retrieval by various parts of the search code.
    """

    def __init__(self, context: SearchContext, queries: List[dict]):
        self.context = context
        self.queries = queries
        self.page_size = search_by_id_helper_page_size
        self.current_index = -1
        self.page = None

    def get_by_index(self, index: int) -> ItemSearchPreviewV1:
        if index > self.current_index:
            if self.context.use_item_finder:
                self._get_next_page_via_item_finder()
            else:
                self._get_next_page_via_search_items()

        return self.page[index]

    def _next_page_of_ids(self, page_size: int) -> Tuple[List[str], int]:
        """
        Walk forward through the queries, collecting up to a page of IDs. Returns the index the page ends at.
        """
        ids = list()
        new_current_index = self.current_index
        while new_current_index < len(self.queries) - 1:
            new_current_index += 1
            if not _common.present(self.queries[new_current_index], 'ID'):
                continue

            ids.append(self.queries[new_current_index]['ID'])

            if len(ids) >= page_size:
                break

        return ids, new_current_index

    def _include_properties(self) -> Optional[List[str]]:
        if self.context.session.options.wants_compatibility_with(188):
            return ALL_PROPERTIES

        return self.context.include_properties

    def _get_next_page_via_item_finder(self) -> None:
        # search_by_id_helper_page_size exists only to keep a long filter string out of a GET URL, which a POST
        # body does not need.
        page_size = self.context.session.options.search_page_size
        ids, new_current_index = self._next_page_of_ids(page_size)

        include_properties = self._include_properties()
        builder = ItemFinderQueryBuilder(
            limit=page_size,
            include_properties=None if include_properties == ALL_PROPERTIES else (include_properties or None),
            include_all_properties=include_properties == ALL_PROPERTIES)
        # An ID predicate rather than a FixedListSearch. FixedListSearch currently errors if any of the items are not
        # readable. ID predicate is also slightly faster due to lacking that assertion.
        # Archived and Unsearchable only hide an item from searches by name and properties, so a lookup by ID opts out
        # of both defaults, as the legacy lookup below does with '@includeUnsearchable'. Leaving either one out makes
        # _add_properties_smartly() fetch each such item with its own request.
        # TODO CRAB-66331 ID predicates work fine, but a FixedListSearch is the more correct way of achieving this. It
        #  reads the listed IDs directly with neither default filter, so include_archived and include_unsearchable go
        #  away along with the ID predicate.
        builder.add_item_search(types=DEFAULT_ITEM_TYPES_FOR_ITEM_FINDER,
                                predicates=[_item_finder.predicate(SeeqNames.Properties.id,
                                                                   _item_finder.Operator.WITHIN, *ids)],
                                include_archived=True,
                                include_unsearchable=True)

        items = {item.id: item for item in ItemFinderPager(self.context.session, builder)}
        self._cache_page(items, new_current_index)

    def _get_next_page_via_search_items(self) -> None:
        ids, new_current_index = self._next_page_of_ids(self.page_size)
        filters = ['@includeUnsearchable'] + [f'ID=={item_id}' for item_id in ids]

        search_results = self.context.items_api.search_items(
            filters=filters,
            include_properties=self._include_properties(),
            limit=self.page_size
        )

        self._cache_page({item.id: item for item in search_results.items}, new_current_index)

    def _cache_page(self, items: dict, new_current_index: int) -> None:
        self.page = dict()
        while self.current_index < new_current_index:
            self.current_index += 1
            if not _common.present(self.queries[self.current_index], 'ID'):
                continue

            self.page[self.current_index] = items.get(self.queries[self.current_index]['ID'])


@Status.top_level_spy_function()
def search(
        query: Union[str, dict, list, pd.DataFrame, pd.Series],
        *,
        all_properties: bool = False,
        include_properties: Optional[List[str]] = None,
        workbook: Optional[str] = _common.DEFAULT_WORKBOOK_PATH,
        recursive: Optional[bool] = True,
        ignore_unindexed_properties: Optional[bool] = True,
        include_archived: Optional[bool] = False,
        include_swappable_assets: Optional[bool] = False,
        estimate_sample_period: Optional[dict] = None,
        old_asset_format: Optional[bool] = None,
        order_by: Optional[Union[str, List[str]]] = None,
        limit: Optional[int] = USE_DEFAULT_LIMIT,
        errors: Optional[str] = None,
        quiet: Optional[bool] = None,
        status: Optional[Status] = None,
        session: Optional[Session] = None
) -> pd.DataFrame:
    """
    Issues a query to the Seeq Server to retrieve metadata for signals,
    conditions, scalars and assets. This metadata can then be used to retrieve
    samples, capsules for a particular time range via spy.pull().

    Parameters
    ----------
    query : {str, dict, list, pd.DataFrame, pd.Series}
        A mapping of property / match-criteria pairs or a Seeq Workbench URL

        If you supply a dict or list of dicts, then the matching
        operations are "contains" (instead of "equal to").

        If you supply a DataFrame or a Series, then the matching
        operations are "equal to" (instead of "contains").

        If you surround the match criteria with a leading/trailing slash (/),
        that indicates that the match criteria is a regular expression that
        must match on the entire property.

        If you supply a str, it must be the URL of a Seeq Workbench worksheet.
        The retrieved metadata will be the signals, conditions and scalars
        currently present on the Details Panel.

        'Name' and 'Description' fields support wildcard and regular expression
        (regex) matching with the same syntax as within the Data tab in Seeq
        Workbench.

        The 'Path' field allows you to query within an asset tree, where >>
        separates each level from the next. E.g.: 'Path': 'Example >> Cooling*'
        You can use wildcard and regular expression matching at any level but,
        unlike the Name/Description fields, the match must be a "full match",
        meaning that 'Path': 'Example' will match on a root asset tree node of
        'Example' but not 'Example (AF)'. To retrieve all items in an entire
        tree, specify {'Path': '', 'Asset': '<Root Asset Name>'} and
        recursive=True.

        Available options are:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        Name                Name of the item (wildcards/regex supported)
        Path                Asset tree path of the item (should not include the
                            "leaf" asset), using ' >> ' hierarchy delimiters
        Asset               Asset name (i.e., the name of the leaf asset) or ID
        Type                The item type. One of 'Signal', 'Condition',
                            'Scalar', 'Asset', 'Chart', 'Metric', 'Workbook',
                            'Worksheet', and 'Display'
        ID                  The item ID. If specified, all other properties
                            are ignored and the item is retrieved directly. If
                            the item ID is not found, an error will be raised.
        Description         Description of the item (wildcards/regex supported)
        Datasource Name     Name of the datasource
        Datasource ID       The datasource ID, which corresponds to the Id
                            field in the connector configuration
        Datasource Class    The datasource class (e.g. 'OSIsoft PI')
        Data ID             The data ID, whose format is managed by the
                            datasource connector
        Cache Enabled       True to find items where data caching is enabled
        Scoped To           The Seeq ID of a workbook such that results are
                            limited to ONLY items scoped to that workbook.
        =================== ===================================================

    all_properties : bool, default False
        Return all item properties in the result. If you would like to specify
        exactly which properties to return (for better performance/less data),
        use include_properties instead. If both all_properties and
        include_properties are omitted, you will get only the properties that
        come "for free" (no performance penalty) with the query.

    include_properties : list, optional
        A list of extra properties to include in the results. If omitted, the
        default set of properties will be returned. If both all_properties and
        include_properties are omitted, you will get only the properties that
        come "for free" (no performance penalty) with the query.

    workbook : {str, None}, default 'Data Lab >> Data Lab Analysis'
        A path string (with ' >> ' delimiters) or an ID to indicate a workbook
        such that, in addition to globally-scoped items, the workbook's scoped
        items will also be returned in the results.

        If you want all items regardless of scope, use
        workbook=spy.GLOBALS_AND_ALL_WORKBOOKS (equivalent to workbook=None)

        If you want only globally-scoped items, use
        workbook=spy.GLOBALS_ONLY

        If you don't want globally-scoped items in your results, use the
        'Scoped To' field in the 'query' argument instead. (See 'query'
        argument documentation above.)

        The ID for a workbook is visible in the URL of Seeq Workbench, directly
        after the "workbook/" part.

    recursive : bool, default True
        If True, searches that include a Path entry will include items at and
        below the specified location in an asset tree. If False, then only
        items at the specified level will be returned. To get only the root
        assets, supply a Path value of ''.

    ignore_unindexed_properties : bool, default True
        If False, a ValueError will be raised if any properties are supplied
        that cannot be used in the search.

    include_archived : bool, default False
        If True, includes trashed/archived items in the output.

    include_swappable_assets : bool, default False
        Adds a "Swappable Assets" column to the output where each cell is an
        embedded DataFrame that includes the assets that the item refers to and
        can theoretically be swapped for other assets using spy.swap().

    estimate_sample_period : dict, default None
        A dict with the keys 'Start' and 'End'. If provided, an estimated
        sample period for all signals will be included in the output. The
        values for the 'Start' and 'End' keys must be a string that
        pandas.to_datetime() can parse, or a pandas.Timestamp. The start
        and end times are used to bound the calculation of the sample period.
        If the start and end times encompass a time range that is insufficient
        to determine the sample period, a pd.NaT will be returned.
        If the value of 'Start' is set to None, it will default to the value
        of 'End' minus 1 hour. Conversely, if the value of 'End' is set to
        None, it will default to now.

    old_asset_format : bool, default True
        Historically, spy.search() returned rows with a "Type" of "Asset"
        whereby the "Asset" column was the name of the parent asset. This is
        inconsistent with all other aspects of SPy, including
        spy.push(metadata). If you would like Asset rows to instead be
        consistent with the rest of SPy (whereby the "Asset" column is the
        name of the current asset, not the parent), pass in False for this
        argument.

    order_by : {str, list}, default None
        An optional field or list of fields used to sort the search results.
        Fields on which results can be sorted are 'ID', 'Name', and
        'Description'.

    limit : int, default 1000
        A limit on the number of results returned. By default, the limit is
        1000. Specify limit=None to return all results.

    quiet : bool, default False
        If True, suppresses progress output. Note that when status is
        provided, the quiet setting of the Status object that is passed
        in takes precedence.

    errors : {'raise', 'catalog'}, default 'raise'
        If 'raise', any errors encountered will cause an exception. If
        'catalog', errors will be added to a 'Result' column in the status.df
        DataFrame.

    status : spy.Status, optional
        If specified, the supplied Status object will be updated as the command
        progresses. It gets filled in with the same information you would see
        in Jupyter in the blue/green/red table below your code while the
        command is executed. The table itself is accessible as a DataFrame via
        the status.df property.

    session : spy.Session, optional
        If supplied, the Session object (and its Options) will be used to
        store the login session state. This is useful to log in to different
        Seeq servers at the same time or with different credentials.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with rows for each item found and columns for each
        property.

        Additionally, the following properties are stored on the "spy"
        attribute of the output DataFrame:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        func                A str value of 'spy.search'
        kwargs              A dict with the values of the input parameters
                            passed to spy.search to get the output DataFrame
        old_asset_format    True if the old Asset format was used (see doc for
                            old_asset_format argument)
        status              A spy.Status object with the status of the
                            spy.search call
        =================== ===================================================

    Examples
    --------
    Search for signals with the name 'Humid' on the asset tree under
    'Example >> Cooling Tower 1', retrieving all properties on the results:

    >>> search_results = spy.search({'Name': 'Humid', 'Path': 'Example >> Cooling Tower 1'}, all_properties=True)

    To access the stored properties:
    >>> search_results.spy.kwargs
    >>> search_results.spy.status

    Search for signals that have a name that starts with 'Area' in the
    datasource 'Example Data' and determine the sample period of each signal
    during the month of January 2018

    >>> search_results = spy.search({
    >>>    'Name': 'Area ?_*',
    >>>    'Datasource Name': 'Example Data'
    >>> }, estimate_sample_period=dict(Start='2018-01-01', End='2018-02-01'))

    Using a pandas.DataFrame as the input:

    >>> my_items = pd.DataFrame(
    >>>     {'Name': ['Area A_Temperature', 'Area B_Compressor Power', 'Optimize' ],
    >>>      'Datasource Name': 'Example Data'})
    >>> spy.search(my_items)

    Using a URL from a Seeq Workbench worksheet:

    >>> my_worksheet_items = spy.search(
    >>> 'https://seeq.com/workbook/17F31703-F0B6-4C8E-B7FD-E20897BD4819/worksheet/CE6A0B92-EE00-45FC-9EB3-D162632DBB48')

    """
    input_args = locals()

    if all_properties:
        if include_properties is not None:
            status.warn(f'If you specify all_properties=True, the include_properties argument is ignored.')
        include_properties = ALL_PROPERTIES.copy()

    context = SearchContext(session, status)
    context.workbook = workbook
    context.recursive = recursive
    context.ignore_unindexed_properties = ignore_unindexed_properties
    context.include_archived = include_archived
    context.estimate_sample_period = estimate_sample_period
    context.include_swap_info = include_swappable_assets
    context.old_asset_format = old_asset_format
    context.order_by = order_by

    if limit != USE_DEFAULT_LIMIT:
        context.limit = limit
    elif session.options.wants_compatibility_with(188):
        # In v188 and earlier, there was no limiting capability.
        context.limit = None
    else:
        # In v189 and later, we apply a default limit of 1000 to reduce the likelihood of a user accidentally running
        # a search that returns a huge number of results.
        context.limit = 1000

    context.columns = ['ID', 'Type']
    if include_properties is not None and include_properties != ALL_PROPERTIES:
        context.columns.extend(include_properties)

    context.include_properties = include_properties if include_properties is not None else list()

    # The SPy user knows the formula parameters property as "Formula Parameters", but the backend knows it as
    # "FormulaParameters". So just convert it here to keep things consistent for the SPy user.
    context.include_properties = [p.replace('Formula Parameters', SeeqNames.Properties.formula_parameters)
                                  for p in context.include_properties]

    if context.order_by:
        context.order_by = _validate_order_by(context.order_by)

    if context.estimate_sample_period is not None:
        if context.estimate_sample_period.keys() != {'Start', 'End'}:  # strict comparison, allowing only these two keys
            raise SPyValueError(f"estimate_sample_period must have 'Start' and 'End' keys but got "
                                f"{context.estimate_sample_period.keys()}")
        context.pd_start, context.pd_end = _login.validate_start_and_end(context.session,
                                                                         context.estimate_sample_period['Start'],
                                                                         context.estimate_sample_period['End'])

    if not context.recursive and 'Path' not in query:
        raise SPyValueError("'Path' must be included in query when recursive=False")

    context.old_asset_format = old_asset_format
    if context.old_asset_format is None:
        # In the future, we may wish to change this default to False, in which case we should use
        # spy.options.compatibility and keep it True for users expecting older behavior.
        context.old_asset_format = True

    queries: List[Union[Dict, Mapping]]
    if isinstance(query, pd.DataFrame):
        queries = query.to_dict(orient='records')
        context.comparison = '=='
    elif isinstance(query, pd.Series):
        queries = [query.to_dict()]
        context.comparison = '=='
    elif isinstance(query, list):
        queries = query
        context.comparison = '~='
    elif isinstance(query, str):
        worksheet = spy.utils.pull_worksheet_via_url(query, minimal=True, include_archived=context.include_archived,
                                                     quiet=context.status.quiet, session=session)
        queries = worksheet.display_items.to_dict(orient='records')
        context.comparison = '=='
    else:
        queries = [query]
        context.comparison = '~='

    all_queries_have_id = True  # if all queries are by ID, we can skip searching for the workbook
    for query in queries:
        if _common.present(query, 'ID'):
            query['ID'] = query['ID'].upper()  # Handle the case where the user provides a lower-case ID (CRAB-38168)
        else:
            all_queries_have_id = False

    context.status.df = pd.DataFrame(queries)
    context.status.df['Time'] = datetime.timedelta(0)
    context.status.df['Count'] = 0
    context.status.df['Pages'] = 0
    context.status.df['Result'] = 'Queued'
    context.status.update('Initializing', Status.RUNNING)

    context.workbook_id = None
    if context.workbook and not all_queries_have_id:
        if _common.is_guid(context.workbook):
            context.workbook_id = _common.sanitize_guid(context.workbook)
            if context.use_item_finder:
                _validate_scope_workbook_id(context, context.workbook_id)
        else:
            search_query, _ = WorkbookContext.create_analysis_search_query(context.workbook)
            search_df = spy.workbooks.search(search_query,
                                             status=context.status.create_inner('Find Workbook', quiet=True),
                                             session=context.session)
            context.workbook_id = search_df.iloc[0]['ID'] if len(search_df) > 0 else None
            if context.workbook == _common.DEFAULT_WORKBOOK_PATH and context.workbook_id is None:
                context.workbook_id = _common.GLOBALS_ONLY

    context.search_by_id_helper_for_all_queries = SearchByIDHelper(context, queries)

    context.used_search_items_api_at_least_once = False

    try:
        for status_index in range(len(queries)):
            context.status_index = status_index
            _process_query(context, queries[status_index])
    except StopIteration:
        limit_warning = f'Search results limited to {context.limit}. Supply increased "limit" parameter to return more.'
        tiebreak_field = _item_finder_unsupported_tiebreak_field(context)
        if tiebreak_field is not None:
            limit_warning += (f' Items with the same "{context.order_by[0]}" may be returned based on sorting their ID '
                              f'rather than their "{tiebreak_field}". Only the first order_by field is applied within '
                              f'the {context.limit} limit.')
        status.warn(limit_warning)

    if context.dupe_count > 0:
        if context.used_search_items_api_at_least_once and not context.use_item_finder:
            # The order_by advice below only applies to offset pagination, where an unsorted result set can shift
            # between pages. ItemFinder pages with a keyset cursor and always has a deterministic sort.
            arg_to_use = context.order_by if context.order_by is not None else list()
            if 'ID' in arg_to_use:
                context.status.warn(
                    f'{context.dupe_count} duplicates removed from returned DataFrame. If you used a list of '
                    f'searches, those searches may have had overlap.')
            else:
                arg_to_use.append('ID')
                context.status.warn(
                    f'{context.dupe_count} duplicates removed from returned DataFrame. Use order_by={arg_to_use} in '
                    f'your spy.search to ensure results are not missing any items.')
        else:
            context.status.warn(f'{context.dupe_count} duplicates removed from returned DataFrame.')

    context.status.update('Query successful', Status.SUCCESS)

    # We want the default properties to always appear first and in a certain order, so we make a final_column_set
    # list, add in the additional properties, and then filter any absent properties from the final list
    final_column_set = DEFAULT_PROPERTIES.copy()
    final_column_set += [c for c in context.columns if c not in final_column_set]
    final_column_set = [c for c in final_column_set if c in context.columns]
    output_df = pd.DataFrame(data=context.metadata, columns=final_column_set)

    if context.order_by and not output_df.empty:
        output_df.sort_values(context.order_by, ignore_index=True, inplace=True)

    if old_asset_format is None:
        type_column = output_df['Type']
        if len(type_column.loc[type_column == 'Asset']) > 0:
            context.status.warn(
                'This search result includes Assets. Consider passing in "old_asset_format=False" so that the '
                '"Path" and "Asset" columns are populated in a way that is consistent with all other aspects '
                'of SPy. The default behavior without this argument emulates the (incorrect) way SPy would '
                'return such results historically.')

    output_df_properties = types.SimpleNamespace(
        func='spy.search',
        kwargs=input_args,
        old_asset_format=context.old_asset_format,
        status=context.status)

    _common.put_properties_on_df(output_df, output_df_properties)

    return output_df


def _validate_scope_workbook_id(context: SearchContext, workbook_id: str) -> None:
    """
    Ensure a workbook given as a UUID exists and is readable by the user. search_items() validated its scope
    argument server-side, but ItemFinders state scope as an ordinary Scoped To predicate and predicates do not
    validate their values, so an unreadable or unknown ID would quietly return just the globally scoped items.
    """
    if workbook_id == _common.GLOBALS_ONLY:
        return
    workbook_output = None
    if _common.is_guid(workbook_id):
        workbook_output = safely(lambda: context.workbooks_api.get_workbook(id=workbook_id),
                                 action_description=f'find the workbook {workbook_id} to scope the search to',
                                 ignore_errors=[400, 403, 404])
    if workbook_output is None:
        raise SPyRuntimeError(f'Workbook "{workbook_id}" not found, or is not accessible by you')


def _process_query(context: SearchContext, current_query: dict) -> None:
    """
    Called for each query "row" in the list of queries
    """
    context.timer = _common.timer_start()

    if _common.present(current_query, 'ID'):
        context.search_by_id_on_this_query = True

        # If ID is specified, short-circuit everything and just get the item directly.
        current_id = current_query['ID']
        prop_dict = _create_prop_dict(context, current_id)
        _add_to_metadata(context, prop_dict)

        context.status.df.at[context.status_index, 'Time'] = _common.timer_elapsed(context.timer)
        context.status.df.at[context.status_index, 'Count'] = 1
        context.status.df.at[context.status_index, 'Result'] = 'Success'
        return

    context.search_by_id_on_this_query = False

    # If the user wants a recursive search or there's no 'Path' in the query, then use the ItemsApi.search_items API
    context.use_search_items_api_for_this_query = context.recursive or not _common.present(current_query, 'Path')
    context.used_search_items_api_at_least_once = (context.used_search_items_api_at_least_once or
                                                   context.use_search_items_api_for_this_query)

    # ItemFinders replace the tree walk for a non-recursive Path. (Except empty path, which uses the Trees API)
    uses_trees_api = not context.use_search_items_api_for_this_query and (
            not context.use_item_finder or
            (len(current_query['Path'].strip()) == 0 and not _common.present(current_query, 'Asset')))

    if uses_trees_api and context.include_archived:
        # The TreesApi.get_tree() API doesn't have the ability to request archived items. Disallow that combination
        # if we have to use those endpoints.
        raise SPyValueError('include_archived=True can only be used with recursive searches or searches that do '
                            'not involve a Path parameter')

    allowed_properties = ['Type', 'Name', 'Description', 'Path', 'Asset', 'Datasource Class', 'Datasource ID',
                          'Datasource Name', 'Data ID', 'Cache Enabled', 'Scoped To']

    disallowed_properties = list()
    for key, value in current_query.items():
        if key not in allowed_properties:
            disallowed_properties.append(key)

    for key in disallowed_properties:
        del current_query[key]

    allowed_properties_str = '"' + '", "'.join(allowed_properties) + '"'
    if len(disallowed_properties) > 0:
        disallowed_properties_str = '"' + '", "'.join(disallowed_properties) + '"'
        message = f'The following properties are not indexed' \
                  f'{" and will be ignored" if context.ignore_unindexed_properties else ""}:\n' \
                  f'{disallowed_properties_str}\n' \
                  f'Use any of the following searchable properties and then filter further using DataFrame ' \
                  f'operations:\n{allowed_properties_str}'

        if not context.ignore_unindexed_properties:
            raise SPyValueError(message)
        else:
            context.status.warn(message)

    if len(current_query) == 0:
        raise SPyValueError('No recognized properties present in "query" argument. You must provide a dict or a '
                            'DataFrame with keys or columns with at least one of the following properties: \n' +
                            allowed_properties_str)

    item_types = list()
    clauses: Dict = dict()

    if _common.present(current_query, 'Type'):
        item_type_specs = list()
        if isinstance(current_query['Type'], list):
            item_type_specs.extend(current_query['Type'])
        else:
            item_type_specs.append(current_query['Type'])

        for item_type_spec in item_type_specs:
            if item_type_spec == 'Signal':
                item_types.extend(['StoredSignal', 'CalculatedSignal'])
            elif item_type_spec == 'Condition':
                item_types.extend(['StoredCondition', 'CalculatedCondition'])
            elif item_type_spec == 'Scalar':
                item_types.extend(['LiteralScalar', 'CalculatedScalar'])
            elif item_type_spec == 'Datasource':
                item_types.extend(['Datasource'])
            elif item_type_spec == 'Metric':
                item_types.extend(['ThresholdMetric'])
            elif item_type_spec == 'Table':
                item_types.extend(['TableDefinition'])
            elif item_type_spec not in VALID_ITEM_TYPES_FOR_SEARCH:
                raise SPyValueError(f'Type field value not recognized: {item_type_spec}\n'
                                    f'Valid types: {", ".join(VALID_ITEM_TYPES_FOR_SEARCH)}')
            else:
                item_types.append(item_type_spec)

        current_query['Type'] = item_types

    for prop_name in ['Name', 'Description', 'Datasource Class', 'Datasource ID', 'Data ID']:
        if prop_name in current_query and not pd.isna(current_query[prop_name]):
            this_comparison = context.comparison
            this_query_matcher = current_query[prop_name]
            if this_query_matcher.startswith('/') and this_query_matcher.endswith('/'):
                # The user wants to do regex for this query, which means we have to use ~=
                this_comparison = '~='

            clauses[prop_name] = (this_comparison, this_query_matcher)

    if _common.present(current_query, 'Datasource Name'):
        datasource_name = _common.get(current_query, 'Datasource Name')
        if datasource_name in context.datasource_ids:
            clauses['Datasource ID'], clauses['Datasource Class'] = context.datasource_ids[datasource_name]
        else:
            filters = ['Name == %s' % datasource_name]
            if _common.present(current_query, 'Datasource ID'):
                filters.append('Datasource ID == %s' % _common.get(current_query, 'Datasource ID'))
            if _common.present(current_query, 'Datasource Class'):
                filters.append('Datasource Class == %s' % _common.get(current_query, 'Datasource Class'))

            filter_list = [' && '.join(filters)]
            if context.include_archived:
                filter_list.append('@includeUnsearchable')

            datasource_results = context.items_api.search_items(
                filters=filter_list, types=['Datasource'], limit=100000)

            if len(datasource_results.items) > 1:
                raise SPyRuntimeError('Multiple datasources found that match "%s"' % datasource_name)
            elif len(datasource_results.items) == 0:
                raise SPyRuntimeError('No datasource found that matches "%s"' % datasource_name)

            datasource = datasource_results.items[0]

            @request_safely(action_description=f'get datasource details for "{datasource_name}" {datasource.id}',
                            status=context.status)
            def request_datasource_and_set_clause():
                property_output = context.items_api.get_property(id=datasource.id, property_name='Datasource Class')
                clauses['Datasource Class'] = ('==', property_output.value)
                property_output = context.items_api.get_property(id=datasource.id, property_name='Datasource ID')
                clauses['Datasource ID'] = ('==', property_output.value)
                context.datasource_ids[datasource_name] = (clauses['Datasource ID'], clauses['Datasource Class'])

            request_datasource_and_set_clause()

        del current_query['Datasource Name']

    filters = list()
    if len(clauses.items()) > 0:
        filters.append(' && '.join([p + c + v for p, (c, v) in clauses.items()]))

    if context.include_archived:
        filters.append('@includeUnsearchable')

    kwargs = {
        'filters': filters,
        'types': item_types
    }

    if context.limit is None:
        kwargs['limit'] = context.session.options.search_page_size
    else:
        # If the user supplied a limit argument, then use it (if it's smaller than the page size)
        kwargs['limit'] = min(context.session.options.search_page_size, context.limit)

    if context.include_properties is not None and _version.is_sdk_module_version_at_least(62):
        kwargs['include_properties'] = context.include_properties

    if context.workbook:
        if context.workbook_id:
            kwargs['scope'] = context.workbook_id
        elif context.workbook != _common.DEFAULT_WORKBOOK_PATH:
            raise SPyRuntimeError(f'Workbook "{context.workbook}" not found, or is not accessible by you')

    context.search_definition = ItemSearchDefinition(clauses=clauses, types=item_types,
                                                     include_archived=context.include_archived)

    if _common.present(current_query, 'Scoped To'):
        if context.use_item_finder:
            scoped_to = current_query['Scoped To']
            for workbook_id in scoped_to if isinstance(scoped_to, list) else [scoped_to]:
                _validate_scope_workbook_id(context, workbook_id)
        kwargs['scope'] = current_query['Scoped To']
        kwargs['filters'].append('@excludeGloballyScoped')
        context.search_definition.exclude_globally_scoped = True

    if _common.present(current_query, 'Asset'):
        if _common.is_guid(_common.get(current_query, 'Asset')):
            kwargs['asset'] = _common.get(current_query, 'Asset')
        elif not _common.present(current_query, 'Path'):
            raise SPyValueError('"Path" query parameter must be present when "Asset" name parameter present')

    if _common.present(current_query, 'Path'):
        path_to_query = current_query['Path'].strip()
        if _common.present(current_query, 'Asset'):
            if len(path_to_query) > 0:
                path_to_query = path_to_query + ' >> ' + current_query['Asset']
            else:
                path_to_query = current_query['Asset']

        # If there is a 'Path' property in the query, then first we have to drill down through the tree to the
        # appropriate depth so we can find the asset ID to use for the results gathering stage.

        if len(path_to_query) == 0:
            _gather_results(context, current_query, kwargs, list())
        elif context.use_item_finder:
            _process_query_path_string_via_item_finder(context, current_query, kwargs, path_to_query, clauses)
        else:
            _process_query_path_string(context, current_query, kwargs, path_to_query, list(), clauses)
    else:
        # If there's no 'Path' property in the query, we can immediately proceed to the results gathering stage.
        _gather_results(context, current_query, kwargs)

    context.status.df.at[context.status_index, 'Result'] = 'Success'


def _gather_results(context: SearchContext, current_query: dict, kwargs: dict,
                    actual_path_list: Optional[List[str]] = None) -> None:
    """
    Once we're at the appropriate depth in the tree, we can gather the results. If we're not doing a tree-based
    query, then we just search at the top level.
    """
    if context.use_search_items_api_for_this_query:
        if context.use_item_finder:
            _iterate_over_item_finder(context, current_query, kwargs, actual_path_list)
        else:
            _iterate_over_output(context, _do_search, 'items', _gather_results_via_item_search, current_query,
                                 kwargs, actual_path_list)
    else:
        _iterate_over_output(context, _do_search, 'children', _gather_results_via_get_tree, current_query,
                             kwargs, actual_path_list)


def _build_item_finder_query(context: SearchContext, kwargs: dict,
                             clause_predicates: Optional[List[PropertyFilterInputV1]] = None) -> ItemFinderQueryBuilder:
    """
    Render context.search_definition as an ItemFinder query. The ancestor and scope arguments are read from kwargs
    rather than the definition because the Path walk rewrites kwargs['asset'] for each asset it resolves.
    clause_predicates replaces the definition's clauses, rendered in the legacy filter grammar by default.
    """
    definition = context.search_definition

    predicates = (_item_finder.legacy_filter_predicates(definition.clauses) if clause_predicates is None
                  else list(clause_predicates))

    # The legacy path sends '@includeUnsearchable' whenever include_archived is set, so an archived search also
    # picks up unsearchable items. ItemFinder needs that stated as a predicate.
    unsearchable = _item_finder.unsearchable_predicate(definition.include_archived)
    if unsearchable is not None:
        predicates.append(unsearchable)

    predicates.extend(_scope_predicates(context, kwargs))

    builder = ItemFinderQueryBuilder(limit=kwargs.get('limit'),
                                     include_properties=_item_finder_include_properties(context),
                                     include_all_properties=context.include_properties == ALL_PROPERTIES)

    # TODO CRAB-66070 Delete this note once add_item_search() can use a single property search for every type. Until
    #  then it adds one per restricted extracted type group, and the server pages through them one after another
    #  rather than merging them by sort field. So when a finite limit truncates the results, an order_by search can
    #  keep a late row from the first search and drop an early row from a later one, which the final DataFrame sort
    #  cannot recover.
    builder.add_item_search(types=definition.types if definition.types else DEFAULT_ITEM_TYPES_FOR_ITEM_FINDER,
                            predicates=predicates,
                            ancestor_id=kwargs.get('asset'),
                            sort_field=_item_finder_sort_field(context),
                            include_archived=definition.include_archived)

    return builder


def _scope_predicates(context: SearchContext, kwargs: dict, *, include_globally_scoped: bool = False) -> List:
    scope = kwargs.get('scope')
    if scope is None:
        return list()

    scope_ids = scope if isinstance(scope, list) else [scope]
    if context.search_definition.exclude_globally_scoped and not include_globally_scoped:
        return [_item_finder.predicate(SeeqNames.Properties.scoped_to, _item_finder.Operator.WITHIN, *scope_ids)]

    # Legacy search's scope arg meant global OR workbook-scoped items. ItemFinders use explicit WITHIN [ID,null].
    return [_item_finder.predicate(SeeqNames.Properties.scoped_to, _item_finder.Operator.WITHIN, *scope_ids, None)]


def _item_finder_include_properties(context: SearchContext) -> Optional[List[str]]:
    if not context.include_properties or context.include_properties == ALL_PROPERTIES:
        return None

    return context.include_properties


def _item_finder_sort_field(context: SearchContext) -> Optional[str]:
    """
    ItemFinder sorts on one field, while order_by accepts several, so only the first one goes to the server. The
    rest are applied when spy.search sorts the assembled DataFrame at the end, which happens whichever endpoint
    produced it. Sorting on the first field still matters when `limit` truncates the results, because it decides
    which rows survive, so sorting on it is closer to what the legacy endpoint returned than sorting on ID.

    Returning None here does not mean "unsorted". ItemFinderQueryBuilder substitutes a sort by ID, because an
    unsorted ItemFinder search cannot paginate at all.

    Ties on the first field are broken by ID rather than by the next order_by field. That is a known gap and doesn't
    seem likely to be super useful to add to ItemFinders, see _item_finder_unsupported_tiebreak_field().
    """
    if not context.order_by:
        return None

    sort_field = context.order_by[0]
    return sort_field if sort_field in _item_finder.SORTABLE_PROPERTIES else None


def _item_finder_unsupported_tiebreak_field(context: SearchContext) -> Optional[str]:
    """
    The order_by field that would have broken ties on the first one, when ItemFinder's ID tiebreaker differs from it,
    otherwise None. order_by accepts only ID, Name and Description, so this is just a Name and Description pair: an
    ID first is unique, and an ID next is what ItemFinder breaks ties with anyway. It only changes which rows survive
    a limit that truncates the results, because the final DataFrame sort applies every field to the rows that remain.
    """
    if not context.use_item_finder or not context.order_by:
        return None

    first_field = context.order_by[0]
    tiebreak_fields = [field for field in context.order_by[1:] if field != first_field]
    if first_field == SeeqNames.Properties.id or not tiebreak_fields:
        return None

    return tiebreak_fields[0] if tiebreak_fields[0] != SeeqNames.Properties.id else None


def _resolve_path_to_assets(context: SearchContext, kwargs: dict, path_to_query: str,
                            clauses: dict) -> List[ItemSearchPreviewV1]:
    """
    Find every asset matching an asset path in one ItemFinder query.

    Each leading segment becomes an ancestor predicate pinned to its depth, and `ancestor_id` plus `level` anchors
    the whole path to the TreeDefinition, so the depth of the path costs nothing.
    """
    segments = _common.path_string_to_list(path_to_query)

    predicates = [_item_finder.query_fragment_predicate(SeeqNames.Properties.name, segments[-1], contains=False)]

    # The legacy walk only applied the datasource filter at the root of the tree, "in case the tree is mixed", so
    # it belongs on the outermost segment rather than on every one.
    datasource_filters = _item_finder.legacy_filter_predicates(
        {prop_name: clause for prop_name, clause in clauses.items() if prop_name in DATASOURCE_CLAUSE_NAMES})

    if len(segments) == 1:
        # A one-segment path makes the root and the target the same asset.
        predicates.extend(datasource_filters)
        ancestor_predicates = None
    else:
        ancestor_predicates = _item_finder.path_ancestor_predicates(
            segments[:-1], root_predicates=[_item_finder.to_table_predicate(f) for f in datasource_filters])

    # The legacy walk never asked TreesApi to exclude globally scoped assets, even for a Scoped To query, so a
    # workbook-scoped item beneath a global asset is still found. Scoped To narrows only the item query.
    predicates.extend(_scope_predicates(context, kwargs, include_globally_scoped=True))

    builder = ItemFinderQueryBuilder(limit=kwargs.get('limit'), include_all_properties=True)
    builder.add_item_search(types=[SeeqNames.Types.asset],
                            predicates=predicates,
                            ancestor_id=_common.EMPTY_GUID,
                            level=len(segments),
                            ancestor_predicates=ancestor_predicates,
                            include_archived=context.search_definition.include_archived)

    return list(ItemFinderPager(context.session, builder, status=context.status,
                                status_index=context.status_index, timer=context.timer))


def _process_query_path_string_via_item_finder(context: SearchContext, current_query: dict, kwargs: dict,
                                               path_to_query: str, clauses: dict) -> None:
    """
    The ItemFinder replacement for _process_query_path_string(). Two queries regardless of how deep or wide the
    path is: one to resolve the path to assets, one to collect the items beneath them.
    """
    assets = _resolve_path_to_assets(context, kwargs, path_to_query, clauses)

    if not context.session.options.wants_compatibility_with(191):
        # The matched assets themselves belong in the results. See CRAB-41197.
        for asset in assets:
            _add_asset_to_metadata_from_preview(context, asset, current_query)

    if not assets:
        return

    clause_predicates = None if context.recursive else _tree_children_predicates(context)
    builder = _build_item_finder_query(context, kwargs, clause_predicates)
    # recursive=True wants everything beneath the assets, so the ancestor predicate carries no level.
    # recursive=False wants only their direct children, which is level 1 above the item.
    level = None if context.recursive else 1
    for property_search in builder.property_searches:
        property_search.ancestor_predicates = [_item_finder.ancestors_within([a.id for a in assets], level=level)]
        # The resolved assets already say where to look, and the legacy walk likewise discarded any Asset GUID
        # the caller passed alongside a Path. Leaving ancestor_id set would AND a second constraint on top.
        property_search.ancestor_id = None

    pager = ItemFinderPager(context.session, builder, status=context.status,
                            status_index=context.status_index, timer=context.timer)
    for item in pager:
        _gather_results_via_item_search(context, current_query, None, item)


def _tree_children_predicates(context: SearchContext) -> List[PropertyFilterInputV1]:
    """
    The clause predicates for a non-recursive Path search. A recursive one used search_items() and so the legacy
    filter grammar, but the legacy non-recursive walk listed children with TreesApi.get_tree() and filtered only
    their Name and Description, through _common.does_query_fragment_match() in _gather_results_via_get_tree().
    Datasource and Data ID clauses applied to the root of the path alone, so a mixed tree keeps its children.
    """
    return [_item_finder.query_fragment_predicate(prop_name, matcher, contains=context.comparison == '~=')
            for prop_name, (_, matcher) in context.search_definition.clauses.items()
            if prop_name in (SeeqNames.Properties.name, SeeqNames.Properties.description)]


def _add_asset_to_metadata_from_preview(context: SearchContext, asset: ItemSearchPreviewV1,
                                        current_query: dict) -> None:
    """
    _add_asset_to_metadata() for an asset we already hold, so it costs no extra lookup. The walk tracked the path
    above each asset as it descended; here the asset's own ancestors say the same thing.
    """
    actual_path_list = [ancestor.name for ancestor in (asset.ancestors or [])]
    if not _asset_matches_query(actual_path_list, asset.name, asset.type, current_query):
        return

    _add_to_metadata(context, _create_prop_dict(context, asset))


def _iterate_over_item_finder(context: SearchContext, current_query: dict, kwargs: dict,
                              actual_path_list: Optional[List[str]]) -> None:
    """
    The ItemFinder equivalent of _iterate_over_output(). Walks continuation tokens instead of offsets, which is
    why it does not need the page-size bookkeeping the offset loop does.
    """
    builder = _build_item_finder_query(context, kwargs)
    pager = ItemFinderPager(context.session, builder, status=context.status,
                            status_index=context.status_index, timer=context.timer)

    for item in pager:
        _gather_results_via_item_search(context, current_query, actual_path_list, item)


# noinspection PyUnusedLocal
def _iterate_over_output(context: SearchContext, _output_func: Callable, _collection_name: str,
                         _action_func: Callable, current_query: dict, kwargs: dict,
                         _actual_path_list: Optional[List[str]]) -> None:
    """
    Handles pagination for the various ways that we need to churn through results.
    """
    offset = 0
    while True:
        output = _output_func(context, kwargs, offset)

        collection = getattr(output, _collection_name)

        context.status.df.at[context.status_index, 'Time'] = _common.timer_elapsed(context.timer)
        context.status.df.at[context.status_index, 'Count'] = offset + len(collection)
        context.status.df.at[context.status_index, 'Pages'] += 1
        context.status.df.at[context.status_index, 'Result'] = 'Querying'
        context.status.update('Querying Seeq Server for items', Status.RUNNING)

        for item in collection:
            _action_func(context, current_query, _actual_path_list, item)

        if len(collection) != output.limit:
            break

        offset += output.limit


def _do_search(context: SearchContext, kwargs: dict, offset: int):
    """
    Executes an actual search. Sometimes this uses the SearchItems API, sometimes it uses the GetTree API.
    """
    kwargs['offset'] = offset
    if 'scope' in kwargs and isinstance(kwargs['scope'], str):
        kwargs['scope'] = [kwargs['scope']]
    if context.use_search_items_api_for_this_query:
        if context.order_by:
            kwargs['order_by'] = context.order_by
        return context.items_api.search_items(**kwargs)

    kwargs2 = {
        'offset': kwargs['offset'],
        'limit': kwargs['limit'],
        'exclude_globally_scoped': ('@excludeGloballyScoped' in kwargs['filters'])
    }

    if _common.present(kwargs, 'scope'):
        kwargs2['scope'] = kwargs['scope']

    if 'asset' in kwargs:
        kwargs2['id'] = kwargs['asset']
        tree_output = context.trees_api.get_tree(**kwargs2)
    else:
        tree_output = context.trees_api.get_tree_root_nodes(**kwargs2)
    if len(kwargs['types']) > 0:
        tree_output.children = [x for x in tree_output.children if x.type in kwargs['types']]

    # This will speed up retrieval of properties in R62 and later
    for i in range(len(tree_output.children)):
        # Plant an index on the child object so we can find it later
        setattr(tree_output.children[i], 'child_index', i)

    # Create a SearchByIDHelper that will be called (in R62 and later) if we need to retrieve extra properties for the
    # child. This case only happens when performing a tree-based query with recursive=False.
    context.search_by_id_helper_for_tree_children = SearchByIDHelper(context, [{'ID': child.id} for child in
                                                                               tree_output.children])

    return tree_output


# noinspection PyUnusedLocal
def _gather_results_via_item_search(context: SearchContext, current_query, actual_path_list,
                                    result: ItemSearchPreviewV1):
    item_search_preview: ItemSearchPreviewV1 = result
    prop_dict = _create_prop_dict(context, item_search_preview)
    _add_to_metadata(context, prop_dict)


def _gather_results_via_get_tree(context: SearchContext, current_query: dict, actual_path_list: List[str],
                                 result: TreeItemOutputV1) -> None:
    tree_item_output: TreeItemOutputV1 = result

    for prop, _attr in [('Name', 'name'), ('Description', 'description')]:
        if prop not in current_query:
            continue

        if not _common.does_query_fragment_match(current_query[prop],
                                                 getattr(tree_item_output, _attr),
                                                 contains=(context.comparison == '~=')):
            return

    prop_dict = _create_prop_dict(context, tree_item_output)

    _add_ancestors_to_prop_dict(
        context, tree_item_output.type, tree_item_output.name, actual_path_list, prop_dict)

    _add_to_metadata(context, prop_dict)


def _create_prop_dict(context: SearchContext, item: Union[str, TreeItemOutputV1, ItemSearchPreviewV1]):
    """
    Each individual search result row is represented by a dictionary. This function creates that dictionary,
    and handles the various permutations of types that we might encounter.
    """

    def _add_error_message_and_warn(msg):
        _add_to_dict(context, prop_dict, 'Pull Result', msg)
        context.status.warn(msg)

    item_id = item if isinstance(item, str) else item.id

    prop_dict = dict()
    prop_dict['ID'] = item_id

    @request_safely(action_description=f'get included item properties for {item_id}',
                    status=context.status,
                    on_error=_add_error_message_and_warn)
    def _request_item_properties():
        output_object = _add_properties_smartly(context, item, prop_dict)
        if not hasattr(output_object, 'type'):
            # The acting user probably doesn't have permission to read the item or it's not found in Appserver.
            # Fake an API error so that the redaction process handles it.
            raise ApiException(status=404,
                               reason=f'The item {item_id} was not found or the acting user does not have '
                                      f'permission to read it.')

        if output_object.type in ['CalculatedSignal', 'CalculatedCondition', 'CalculatedScalar', 'LiteralScalar']:
            formula_parameters = None
            if _version.is_sdk_module_version_at_least(62) and hasattr(output_object, 'parameters'):
                formula_parameters = output_object.parameters
            elif (_has_requested_property(context, 'Formula') or
                  _has_requested_property(context, 'FormulaParameters')):
                # Formula isn't always included in the output (in this R61-and-earlier-case), and Formula Parameters
                # is never included. So we have to make a separate request.
                formula_output = context.formulas_api.get_item(id=output_object.id)
                if _has_requested_property(context, 'Formula'):
                    _add_to_dict(context, prop_dict, 'Formula', formula_output.formula)
                formula_parameters = formula_output.parameters

            if formula_parameters is not None and _has_requested_property(context, 'FormulaParameters'):
                _add_to_dict(context, prop_dict, 'Formula Parameters', [
                    '%s=%s' % (_p.name, _p.item.id if _p.item else _p.formula) for _p in formula_parameters
                ])

        elif output_object.type == 'ThresholdMetric':
            formula_parameters = _metadata.formula_parameters_dict_from_threshold_metric(
                context.session, output_object.id)
            for key, value in formula_parameters.items():
                _add_to_dict(context, prop_dict, key, value)

        elif output_object.type == 'Display':
            display_output = context.displays_api.get_display(id=output_object.id)
            _add_to_dict(context, prop_dict, 'Template ID', display_output.template.id)
            if display_output.swap is not None:
                _add_to_dict(context, prop_dict, 'Swap Out Asset ID', display_output.swap.swap_out)
                _add_to_dict(context, prop_dict, 'Swap In Asset ID', display_output.swap.swap_in)
            else:
                _add_to_dict(context, prop_dict, 'Swap Out Asset ID', display_output.template.swap_source_asset_id)

        elif output_object.type == 'DisplayTemplate':
            display_template_output = context.display_templates_api.get_display_template(id=output_object.id)
            _add_to_dict(context, prop_dict, 'Source Workstep ID', display_template_output.source_workstep_id)

    _request_item_properties()
    return prop_dict


def _validate_order_by(order_by: Union[str, List[str]]) -> List[str]:
    """
    Validate and process order_by arg of spy.search
    """
    # convert string order_by to a list
    if isinstance(order_by, str):
        order_by = [order_by]

    # validate order_by
    order_fields = ['ID', 'Name', 'Description']
    invalid_fields = [x for x in order_by if x not in order_fields]
    if len(invalid_fields) > 0:
        raise SPyValueError(
            f"Invalid order_by fields: {invalid_fields}. Search results can only be ordered on "
            f"{order_fields} fields.")

    return order_by


def _add_properties_smartly(context: SearchContext,
                            item: Union[str, TreeItemOutputV1, ItemSearchPreviewV1, ItemOutputV1],
                            prop_dict: dict):
    # This function does a bunch of heavy lifting to handle the differences in how properties are returned
    # in different versions of the SDK.
    #
    # R62 and later:   Extra properties are returned in ItemSearchPreviewV1 objects
    # R61 and earlier: Extra properties must be fetched in a separate request

    # The following two variables will be filled in if we find that we already had them or needed them to fulfill the
    # user's request.
    item_search_preview: Optional[ItemSearchPreviewV1] = None
    item_output: Optional[ItemOutputV1] = None

    # This is the variable that we use to grab all the default/common properties
    item_object: Union[str, TreeItemOutputV1, ItemSearchPreviewV1, ItemOutputV1] = item

    if isinstance(item, str):
        # R62+: Try to look up the item properties using the much faster SearchByIDHelper.
        if _version.is_sdk_module_version_at_least(62):
            item_search_preview = context.search_by_id_helper_for_all_queries.get_by_index(context.status_index)
            item_object = item_search_preview

        # If SearchByIDHelper isn't available or it didn't work due to an edge case (E.G. CRAB-40580),
        # get the properties directly from the get_item_and_all_properties or get_item_preview endpoint.
        if not isinstance(item_object, ItemSearchPreviewV1) and not isinstance(item_object, ItemOutputV1):
            # Note: This doesn't need to be wrapped in request_safely because it's safely called in _create_prop_dict()
            if hasattr(context.items_api, 'get_item_preview'):
                item_search_preview = context.items_api.get_item_preview(id=item)
                item_object = item_search_preview
            else:
                item_output = context.items_api.get_item_and_all_properties(id=item)
                item_object = item_output
    elif isinstance(item, ItemSearchPreviewV1):
        item_search_preview = item

    _add_if_available(context, prop_dict, 'ID', item_object, 'id')
    _add_if_available(context, prop_dict, 'Name', item_object, 'name')
    _add_if_available(context, prop_dict, 'Description', item_object, 'description')
    _add_if_available(context, prop_dict, 'Type', item_object, 'type')
    _add_if_available(context, prop_dict, 'Archived', item_object, 'is_archived')
    _add_if_available(context, prop_dict, 'Scoped To', item_object, 'scoped_to')

    if hasattr(item_object, 'value_unit_of_measure'):
        if item_object.value_unit_of_measure is None and hasattr(item_object, 'source_value_unit_of_measure'):
            uom = item_object.source_value_unit_of_measure
        else:
            uom = item_object.value_unit_of_measure

        _add_to_dict(context, prop_dict, 'Value Unit Of Measure', uom)
    elif item_output is not None:
        value_unit_of_measure = [p.value for p in item_output.properties if p.name == 'Value Unit Of Measure']
        source_value_unit_of_measure = [p.value for p in item_output.properties
                                        if p.name == 'Source Value Unit Of Measure']
        if len(value_unit_of_measure) == 0 and len(source_value_unit_of_measure) == 1:
            uom = source_value_unit_of_measure[0]
        elif len(value_unit_of_measure) == 1:
            uom = value_unit_of_measure[0]
        else:
            uom = None

        _add_to_dict(context, prop_dict, 'Value Unit Of Measure', uom)

    if _has_requested_property(context, 'Source Value Unit Of Measure'):
        _add_if_available(context, prop_dict, 'Source Value Unit Of Measure', item_object,
                          'source_value_unit_of_measure')

    if hasattr(item_object, 'datasource'):
        datasource_item_preview: ItemPreviewV1 = item_object.datasource
        _add_to_dict(context, prop_dict, 'Datasource Name',
                     datasource_item_preview.name if datasource_item_preview else None)

    if hasattr(item_object, 'ancestors'):
        _add_ancestors_to_prop_dict_from_item_output(context, item_object, prop_dict)

    if ((context.include_swap_info
         or (not hasattr(item_object, 'ancestors')
             and (_has_requested_property(context, 'Path')
                  or _has_requested_property(context, 'Asset'))))
            and hasattr(item_object, 'id')):
        _retrieve_ancestors_and_swap_info(context, item_object.id, prop_dict)

    if context.estimate_sample_period is not None and hasattr(item_object, 'id'):
        _estimate_sample_period(context, item_object)
        _add_to_dict(context, prop_dict, 'Estimated Sample Period', context.sample_periods[item_object.id])

    # Check if we need any more properties. If we don't, we can avoid more API calls.
    need_more_properties = False
    if isinstance(item, str) and context.session.options.wants_compatibility_with(188):
        need_more_properties = True
    else:
        for prop in context.include_properties:
            if prop not in prop_dict:
                need_more_properties = True
                break

    if not need_more_properties:
        return item_object

    if _version.is_sdk_module_version_at_least(62):
        if item_search_preview is None and isinstance(item, TreeItemOutputV1):
            item_search_preview = context.search_by_id_helper_for_tree_children.get_by_index(
                getattr(item, 'child_index'))
        if hasattr(item_search_preview, 'included_properties'):
            for prop in item_search_preview.included_properties.values():  # type: ScalarPropertyV1
                _add_included_property_to_dict(context, prop_dict, prop.name, prop.value, prop.unit_of_measure)
        elif hasattr(item_output, 'properties'):
            for prop in item_output.properties:  # type: PropertyOutputV1
                _add_included_property_to_dict(context, prop_dict, prop.name, prop.value, prop.unit_of_measure)
    else:
        if item_output is None:
            # This does not need to be wrapped in request_safely because it is only called from a safe place in
            # _create_prop_dict()
            item_output = context.items_api.get_item_and_all_properties(id=item_object.id)

        for prop in item_output.properties:  # type: PropertyOutputV1
            _add_included_property_to_dict(context, prop_dict, prop.name, prop.value, prop.unit_of_measure)

    return item_object


def _add_included_property_to_dict(context: SearchContext, prop_dict: dict, prop_name: str, prop_value: object,
                                   prop_unit_of_measure: str):
    if prop_name in RESERVED_SEARCH_COLUMN_NAMES:
        return

    if not context.session.options.wants_compatibility_with(188) and not _has_requested_property(context, prop_name):
        return

    _add_to_dict(context, prop_dict, prop_name, prop_value, prop_unit_of_measure)


def _add_if_available(context: SearchContext, prop_dict: dict, key: str, obj: object, attr: str):
    if hasattr(obj, attr):
        _add_to_dict(context, prop_dict, key, getattr(obj, attr))


def _add_to_dict(context: SearchContext, prop_dict: dict, key: str, val: object, uom: str = None):
    if (key not in PROPERTIES_NEVER_TRANSFORM_TO_STRING
            and key not in PROPERTIES_ALWAYS_TRANSFORM_TO_BOOLEAN):
        if context.session.options.wants_compatibility_with(188):
            # In v188 and earlier, all scalar properties on items were returned as strings from
            # items_api.get_item_and_all_properties(). So for scripts that are expecting that, cast it to a string.
            val = str(val)
        elif (not context.session.options.wants_compatibility_with(195) and
              isinstance(val, (int, float)) and uom and uom != 'string'):
            # In v196 and later, join the value and UoM together for unitful values so it can be fully
            # expressed. This is important to be able to feed CalculatedConditions' max duration into new
            # StoredConditions.
            val = f'{val}{uom}'

    elif key.endswith('Unit Of Measure') and val == '':
        # This property is returned as None in ItemSearchPreviewV1.value_unit_of_measure, but as an empty string in
        # the ItemSearchPreviewV1.included_properties. Normalize to None in v189 and later.
        val = None

    if key in PROPERTIES_ALWAYS_TRANSFORM_TO_BOOLEAN and isinstance(val, str):
        val = val.lower() == 'true'

    prop_dict[key] = _common.none_to_nan(val)

    # We want the columns to appear in a certain order (the order we added them in) for readability
    if key not in context.columns:
        context.columns.append(key)


def _add_ancestors_to_prop_dict_from_item_output(context: SearchContext, item_output, prop_dict: dict):
    _ancestors = [a.name for a in item_output.ancestors]
    _add_ancestors_to_prop_dict(context, item_output.type, item_output.name, _ancestors, prop_dict)


def _add_ancestors_to_prop_dict(context: SearchContext, item_type: str, name: str, ancestors: list, prop_dict: dict):
    _common.add_ancestors_to_definition(item_type, name, ancestors, prop_dict, context.old_asset_format)
    for key in ['Path', 'Asset']:
        if key in prop_dict and key not in context.columns:
            context.columns.append(key)


def _add_to_metadata(context: SearchContext, prop_dict: dict):
    if prop_dict['ID'] not in context.ids:
        if len(context.metadata) == context.limit:
            raise StopIteration()

        context.metadata.append(prop_dict)
        context.ids.add(prop_dict['ID'])
    else:
        context.dupe_count += 1


def _estimate_sample_period(context: SearchContext, item: Union[TreeItemOutputV1, ItemSearchPreviewV1]):
    if 'Signal' not in item.type:
        context.sample_periods[item.id] = pd.NaT
        return

    if item.id in context.sample_periods:
        # Already done
        return

    sampling_formula = "$signal.estimateSamplePeriod(" \
                       f"capsule('{context.pd_start.isoformat()}','{context.pd_end.isoformat()}'))"

    formula_run_output = safely(
        lambda: context.formulas_api.run_formula(formula=sampling_formula, parameters=[f"signal={item.id}"]),
        action_description='estimate sample period',
        status=context.status,
        additional_errors=[400])

    if formula_run_output is not None and formula_run_output.scalar.value is not None:
        context.sample_periods[item.id] = pd.to_timedelta(
            formula_run_output.scalar.value, unit=formula_run_output.scalar.uom)
    else:
        context.status.warn(
            f'Could not determine the sample period for signal "{item.name}" {item.id} within the '
            f'time period {context.pd_start.isoformat()} to {context.pd_end.isoformat()}. '
            f'There might not be enough data in the specified time range. Modify the time period with the '
            f'`estimate_start` and `estimate_end` arguments.'
        )
        context.sample_periods[item.id] = pd.NaT


def _has_requested_property(context: SearchContext, prop_name: str) -> bool:
    return prop_name in context.include_properties or context.include_properties == ALL_PROPERTIES


def _retrieve_ancestors_and_swap_info(context: SearchContext, item_id: str, prop_dict: dict):
    """
    This function tries to economically retrieve ancestors and swap information if necessary.
    """
    item_output = None
    if context.include_swap_info:
        item_dependency_output: ItemDependencyOutputV1 = safely(
            lambda: context.items_api.get_formula_dependencies(id=item_id),
            action_description=f'get dependencies for {item_id}',
            status=context.status)
        if item_dependency_output is not None:
            item_output = item_dependency_output

        dependencies_with_relevant_assets = _swap.get_swappable_assets(item_dependency_output)

        def _swappable_asset_dict(d):
            leaf_asset = d.ancestors[-1]
            return {
                'ID': leaf_asset.id,
                'Type': leaf_asset.type,
                'Path': _common.path_list_to_string([a.name for a in d.ancestors[0:-1]]),
                'Asset': leaf_asset.name
            }

        swappable_assets = pd.DataFrame([_swappable_asset_dict(d) for d in dependencies_with_relevant_assets],
                                        columns=['ID', 'Type', 'Path', 'Asset'])

        _add_to_dict(context, prop_dict, 'Swappable Assets', swappable_assets)
    else:
        asset_tree_output: AssetTreeOutputV1 = safely(lambda: context.trees_api.get_tree(id=item_id),
                                                      action_description=f'get asset tree ancestors for {item_id}',
                                                      status=context.status)
        if asset_tree_output is not None:
            item_output = asset_tree_output.item

    if item_output is not None:
        _add_ancestors_to_prop_dict_from_item_output(context, item_output, prop_dict)

    return prop_dict


def _process_query_path_string(context: SearchContext, current_query: dict, kwargs: dict,
                               remaining_query_path_string: str, actual_path_list: List[str], clauses: dict,
                               asset_id: Optional[str] = None) -> None:
    """
    Walks down an asset path and processes each level, including wildcards and regexes.
    """
    query_path_list = _common.path_string_to_list(remaining_query_path_string)

    query_path_part = query_path_list[0]

    tree_kwargs = dict()
    tree_kwargs['limit'] = kwargs['limit']
    tree_kwargs['offset'] = 0

    if 'scope' in kwargs and isinstance(kwargs['scope'], str):
        tree_kwargs['scope'] = [kwargs['scope']]

    while True:
        tree_output: AssetTreeOutputV1
        if not asset_id:
            tree_output = context.trees_api.get_tree_root_nodes(**tree_kwargs)
        else:
            tree_kwargs['id'] = asset_id
            tree_output = context.trees_api.get_tree(**tree_kwargs)

        for child in tree_output.children:  # type: TreeItemOutputV1
            if not _common.does_query_fragment_match(query_path_part, child.name, contains=False):
                continue

            if not asset_id:
                @request_safely(action_description=f'check if "{child.name}" {child.id} has '
                                                   f'datasource matching request',
                                status=context.status,
                                default_value=True)
                def _is_item_in_filter_datasources():
                    child_item_output = context.items_api.get_item_and_all_properties(id=child.id)
                    for prop in ['Datasource Class', 'Datasource ID']:
                        if prop in clauses:
                            _, val = clauses[prop]
                            p_list = [_p.value for _p in child_item_output.properties if
                                      _p.name == prop]
                            if len(p_list) == 0 or p_list[0] != val:
                                return False
                    return True

                # We only filter out datasource at the top level, in case the tree is mixed
                if not _is_item_in_filter_datasources():
                    continue

            actual_path_list_for_child = actual_path_list.copy()
            actual_path_list_for_child.append(child.name)
            if len(query_path_list) == 1:
                if not context.session.options.wants_compatibility_with(191):
                    # We need to include the asset in the results if appropriate. See CRAB-41197
                    _add_asset_to_metadata(context, actual_path_list, child, current_query)
                kwargs['asset'] = child.id
                _gather_results(context, current_query, kwargs, actual_path_list=actual_path_list_for_child)
            else:
                _process_query_path_string(context,
                                           current_query,
                                           kwargs,
                                           _common.path_list_to_string(query_path_list[1:]),
                                           actual_path_list_for_child,
                                           clauses,
                                           child.id)

        if len(tree_output.children) < tree_kwargs['limit']:
            break

        tree_kwargs['offset'] += tree_kwargs['limit']


def _asset_matches_query(actual_path_list: List[str], name: str, item_type: str, current_query: dict) -> bool:
    """
    Whether an asset that a Path query walked through should itself appear in the results. See CRAB-41197.

    `actual_path_list` is the path above the asset, not including it, so a query whose Path names the asset does
    not match: the criteria and the names have to line up segment for segment.
    """
    matches = _common.does_query_fragment_match(_common.get(current_query, 'Name', name), name, contains=False)
    current_query_type = _common.get(current_query, 'Type', item_type)
    if isinstance(current_query_type, list):
        found = False
        for _type in current_query_type:
            found |= _common.does_query_fragment_match(_type, item_type, contains=False)
        matches &= found
    else:
        matches &= _common.does_query_fragment_match(current_query_type, item_type, contains=False)
    path = _common.path_list_to_string(actual_path_list)
    if _common.present(current_query, 'Path'):
        matches &= _common.do_paths_match_criteria(_common.get(current_query, 'Path'), path)
    return matches


def _add_asset_to_metadata(context: SearchContext, actual_path_list: List[str], child: TreeItemOutputV1,
                           current_query: dict) -> None:
    if not _asset_matches_query(actual_path_list, child.name, child.type, current_query):
        return

    if _version.is_sdk_module_version_at_least(62):
        search_by_id_helper = SearchByIDHelper(context, [{'ID': child.id}])
        item_object = search_by_id_helper.get_by_index(0)
        asset_dict = _create_prop_dict(context, item_object)
    else:
        item_object = context.items_api.get_item_and_all_properties(id=child.id)
        asset_dict = _create_prop_dict(context, item_object)
        _common.add_ancestors_to_definition(child.type, child.name, actual_path_list, asset_dict,
                                            context.old_asset_format)

    _add_to_metadata(context, asset_dict)
