from __future__ import annotations

import queue
import types
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Callable, Dict, List, Optional

from seeq.sdk import *

import numpy as np
import pandas as pd
from seeq.spy import _common
from seeq.spy import _login
from seeq.spy._errors import *
from seeq.spy._redaction import safely, request_safely
from seeq.spy._session import Session
from seeq.spy._status import Status
from seeq.spy.workbooks._folder import SYNTHETIC_FOLDERS, synthetic_folder_to_content_filter


@dataclass
class WorkbookSearchContext:
    session: Session
    status: Status
    top_level_query: dict
    all_properties: bool
    recursive: bool
    include_archived: bool
    executor: ThreadPoolExecutor

    futures_queue: queue.Queue = field(default_factory=queue.Queue)
    total_processed_queue: queue.Queue = field(default_factory=queue.Queue)
    results_queue: queue.Queue = field(default_factory=queue.Queue)
    results: Dict[str, dict] = field(default_factory=dict)

    def add_future(self, future):
        self.futures_queue.put(future)

    def add_to_total_processed(self, count):
        self.total_processed_queue.put(count)

    def add_result(self, result):
        self.results_queue.put(result)

    def drain_queues(self):
        while not self.total_processed_queue.empty():
            self.status.df.at[0, 'Total Processed'] += self.total_processed_queue.get()
            self.total_processed_queue.task_done()

        while not self.results_queue.empty():
            self.results.update(self.results_queue.get())
            self.status.df.at[0, 'Total Returned'] = len(self.results)
            self.results_queue.task_done()

        self.status.df.at[0, 'Time'] = self.status.get_timer()
        self.post_message()

    def post_message(self):
        self.status.update('Searching' + (' and retrieving all properties' if self.all_properties else ''),
                           Status.RUNNING)


@Status.handle_keyboard_interrupt()
def search(query: dict, *, content_filter: str = 'owner', all_properties: bool = False, recursive: bool = False,
           include_archived: bool = False, errors: Optional[str] = None, quiet: Optional[bool] = None,
           status: Optional[Status] = None, session: Optional[Session] = None):
    """
    Issues a query to the Seeq Server to retrieve metadata for workbooks.
    This metadata can be used to pull workbook definitions into memory.

    Parameters
    ----------
    query : dict
        A mapping of property / match-criteria pairs. Match criteria uses
        the same syntax as the Data tab in Seeq (contains, or glob, or regex).
        Available options are:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        ID                  ID of the workbook, as seen in the URL.
        Name                Name of the workbook.
        Path                Path to the workbook through the folder hierarchy.
        Description         Description of the workbook.
        Workbook Type       One of 'Analysis', 'Topic', 'Project', or 'Vantage'
        =================== ===================================================

    content_filter : str, default 'owner'
        Filters workbooks according to the following possible values:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        owner               Only content owned by the logged-in user.
        shared              Only content shared specifically with the logged-in
                            user. Note: To obtain the same results as you would
                            when looking at the "Shared" tab in the Seeq home
                            screen, use "sharedorpublic" (see below).
        public              Only content shared with Everyone.
        sharedorpublic      Content shared with Everyone or with the logged-in user
        corporate           Only content in the Corporate folder
        all                 All content, across all users (logged-in user must
                            be admin).
        users               Every user's home folder (logged-in user must be admin)
        =================== ===================================================

    all_properties : bool, default False
        True if all workbook properties should be retrieved. This currently makes
        the search operation much slower as retrieval of properties for an item
        requires a separate call.

    recursive : bool, default False
        True if workbooks further down in the folder path should be returned.

    include_archived : bool, default False
        True if archived (aka "trashed") folders/workbooks should be returned.

    errors : {'raise', 'catalog'}, default 'raise'
        If 'raise', any errors encountered will cause an exception. If 'catalog',
        errors will be added to a 'Result' column in the status.df DataFrame.

    quiet : bool, default False
        If True, suppresses progress output. Note that when status is
        provided, the quiet setting of the Status object that is passed
        in takes precedence.

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
        A DataFrame with rows for each workbook found and columns for each
        property.

    """
    input_args = _common.validate_argument_types([
        (query, 'query', dict),
        (content_filter, 'content_filter', str),
        (all_properties, 'all_properties', bool),
        (recursive, 'recursive', bool),
        (errors, 'errors', str),
        (quiet, 'quiet', bool),
        (status, 'status', Status),
        (session, 'session', Session)
    ])

    _login.validate_login(session, status)

    status.reset_timer()

    status.df = pd.DataFrame([{
        'Time': timedelta(0),
        'Total Processed': 0,
        'Total Returned': 0
    }])

    try:
        # We don't use status.execute_jobs() here because this can be a recursive operation that adds more jobs
        # as the search progresses, which is something that Status doesn't support.
        with ThreadPoolExecutor(max_workers=session.options.max_concurrent_requests) as executor:
            context = WorkbookSearchContext(
                session=session,
                status=status,
                top_level_query=query,
                all_properties=all_properties,
                recursive=recursive,
                include_archived=include_archived,
                executor=executor,
            )

            # Call post_message() to ensure that the status message is initialized
            context.post_message()

            _search(context, query, content_filter.upper())

            while not context.futures_queue.empty():
                # Call Future.result() so that we wait for the thread and raise any exceptions that may have occurred
                context.futures_queue.get().result()
                context.drain_queues()

    except KeyboardInterrupt:
        context.drain_queues()
        status.update('Search canceled.', Status.CANCELED)
        return

    context.drain_queues()

    output_df = pd.DataFrame.from_dict(context.results, orient='index')
    output_df.reset_index(inplace=True, drop=True)

    status.update('Search successful.', Status.SUCCESS)

    output_df_properties = types.SimpleNamespace(
        func='spy.workbooks.search',
        kwargs=input_args,
        status=status)

    _common.put_properties_on_df(output_df, output_df_properties)

    return output_df


def _search(context: WorkbookSearchContext, query: dict, content_filter, *, parent_id=None, parent_path='',
            search_folder_id=None, top_level=True) -> None:
    workbooks_api = WorkbooksApi(context.session.client)

    # allowed_content_filter must be updated every time there is a change to the ItemWithOwner#Filter
    allowed_content_filters = ['OWNER', 'SHARED', 'PUBLIC', 'CORPORATE', 'ALL', 'USERS', 'SHAREDORPUBLIC']
    if content_filter not in allowed_content_filters:
        raise SPyValueError('content_filter must be one of: %s' % ', '.join(allowed_content_filters))

    for _key, _ in query.items():
        supported_query_fields = ['ID', 'Path', 'Name', 'Description', 'Workbook Type']
        if _key not in supported_query_fields:
            raise SPyValueError('"%s" unsupported query field, use instead one or more of: %s' %
                                (_key, ', '.join(supported_query_fields)))

    if 'ID' in query:
        workbook_output: Optional[WorkbookOutputV1] = safely(
            lambda: workbooks_api.get_workbook(id=query['ID']),
            action_description=f'get the details for Workbook {query["ID"]}',
            status=context.status)
        if workbook_output is None:
            return

        content_dict = {
            'ID': workbook_output.id,
            'Type': 'Workbook',
            'Workbook Type': workbook_output.type,
            'Path': _common.path_list_to_string([a.name for a in workbook_output.ancestors]),
            'Name': workbook_output.name,
            'Archived': workbook_output.is_archived,
            'Pinned': workbook_output.marked_as_favorite,
            'Created At': pd.to_datetime(workbook_output.created_at),
            'Updated At': pd.to_datetime(workbook_output.updated_at)
        }

        if workbook_output.owner:
            content_dict['Owner Name'] = workbook_output.owner.name
            content_dict['Owner Username'] = workbook_output.owner.username
            content_dict['Owner ID'] = workbook_output.owner.id
        if workbook_output.creator:
            content_dict['Creator Name'] = workbook_output.creator.name
            content_dict['Creator Username'] = workbook_output.creator.username
            content_dict['Creator ID'] = workbook_output.creator.id

        context.add_result({content_dict['ID']: content_dict})
        return

    path_filter = query['Path'] if 'Path' in query else None

    path_filter_parts = list()
    path_start = None

    if path_filter is not None:
        path_filter_parts = _common.path_string_to_list(path_filter)
        if len(path_filter_parts) > 0:
            path_start = path_filter_parts[0]

    # We want the predefined synthetic folders like workbooks.CORPORATE and workbooks.MY_FOLDER to
    # work as root directories when specified at the beginning of Path
    if path_start in SYNTHETIC_FOLDERS:
        path_start_no_underscore = path_start.replace('__', '').replace('_', ' ')
        warning_message = f'The content_filter {content_filter} was overwritten, and the searched directory was ' \
                          f'set to {path_start_no_underscore} based on the provided path.'

        new_content_filter = synthetic_folder_to_content_filter(path_start)

        if content_filter != new_content_filter and context.status is not None:
            context.status.warn(warning_message)
        # Apply the corresponding content_filter and use the rest of the path
        content_filter = new_content_filter
        path_filter_parts.pop(0)

    contents: list[WorkbenchSearchResultPreviewV1] = list()

    _folder_id_sub_description = f'within {parent_id} ' if parent_id else ''
    _request_folder_contents_description = f'get Folders {_folder_id_sub_description}using filter {content_filter}'

    def _status_callback(count: int):
        context.add_to_total_processed(count)
        if top_level:
            context.drain_queues()

    @request_safely(action_description=_request_folder_contents_description,
                    additional_errors=[400], status=context.status)
    def _add_to_folder_contents(archived):
        folder_output_list = get_folders(context.session,
                                         content_filter=content_filter,
                                         folder_id=parent_id,
                                         archived=archived,
                                         status_callback=_status_callback)
        contents.extend(folder_output_list)

    _add_to_folder_contents(False)
    if context.include_archived:
        _add_to_folder_contents(True)

    for content in contents:
        context.add_future(
            context.executor.submit(_process_content, context, content, content_filter,
                                    parent_path, path_filter_parts, search_folder_id)
        )


def _process_content(context: WorkbookSearchContext, content: WorkbenchSearchResultPreviewV1, content_filter: str,
                     parent_path: str, path_filter_parts: List[str], search_folder_id: str) -> None:
    items_api = ItemsApi(context.session.client)
    path_matches = False
    props_match = True
    if content.type == 'Folder' and len(path_filter_parts) > 0 and \
            _common.does_query_fragment_match(path_filter_parts[0], content.name, contains=False):
        path_matches = True

    for query_key, content_key in [('Name', 'name'), ('Description', 'description')]:
        attr_value = getattr(content, content_key)
        if query_key in context.top_level_query and (attr_value is None or
                                                     not _common.does_query_fragment_match(
                                                         context.top_level_query[query_key], attr_value)):
            props_match = False
            break

    workbook_type = content.type

    if ('Workbook Type' in context.top_level_query and
            not _common.does_query_fragment_match(context.top_level_query['Workbook Type'], workbook_type)):
        props_match = False

    absolute_path = parent_path

    _type = content.type or np.nan
    if _type in ['Analysis', 'Topic', 'Vantage']:
        # This is for backward compatibility with .49 and earlier, which used the same type (Workbook) for both
        # Analysis and Topic. Eventually we may want to deprecate "Workbook Type" and fold it into the "Type"
        # property.
        _type = 'Workbook'

    if props_match and len(path_filter_parts) == 0:
        content_dict = {
            'ID': content.id or np.nan,
            'Type': _type,
            'Workbook Type': workbook_type,
            'Path': absolute_path,
            'Name': content.name or np.nan,
            'Archived': content.is_archived or np.nan,
            'Pinned': content.is_pinned or np.nan,
            'Created At': pd.to_datetime(content.created_at),
            'Updated At': pd.to_datetime(content.updated_at)
        }

        if content.owner:
            content_dict['Owner Name'] = content.owner.name
            content_dict['Owner Username'] = content.owner.username
            content_dict['Owner ID'] = content.owner.id
        if content.creator:
            content_dict['Creator Name'] = content.creator.name
            content_dict['Creator Username'] = content.creator.username
            content_dict['Creator ID'] = content.creator.id

        if search_folder_id:
            content_dict['Search Folder ID'] = search_folder_id

        if context.all_properties:
            excluded_properties = [
                # Exclude these because they're in ns-since-epoch when we retrieve them this way
                'Created At', 'Updated At',

                # Exclude this because it's a bunch of JSON that will clutter up the DataFrame
                'Data', 'workbookState'
            ]

            def _add_error_message_and_warn(msg):
                content_dict['Pull Result'] = msg
                context.status.warn(msg)

            @request_safely(action_description=f'get all properties for Workbook "{content.name}" {content.id}',
                            status=context.status, on_error=_add_error_message_and_warn)
            def _request_workbook_properties():
                _item: ItemOutputV1 = items_api.get_item_and_all_properties(id=content.id)
                for prop in _item.properties:  # type: PropertyOutputV1
                    if prop.name not in excluded_properties:
                        content_dict[prop.name] = _common.none_to_nan(prop.value)

            _request_workbook_properties()

        context.add_result({content_dict['ID']: content_dict})

    if content.type == 'Folder' and ((context.recursive and len(path_filter_parts) == 0) or path_matches):
        child_path_filter = None
        if path_filter_parts and len(path_filter_parts) > 1:
            child_path_filter = _common.path_list_to_string(path_filter_parts[1:])

        if len(parent_path) == 0:
            new_parent_path = content.name
        else:
            new_parent_path = parent_path + ' >> ' + content.name

        child_query = dict(context.top_level_query)
        if not child_path_filter and 'Path' in child_query:
            # We've finished drilling down using the provided 'Path' so now we can use the current folder ID as the
            # "root" from which all paths can be made relative (if desired)
            search_folder_id = content.id
            del child_query['Path']
        else:
            child_query['Path'] = child_path_filter

        _search(context, child_query, content_filter, parent_id=content.id, parent_path=new_parent_path,
                search_folder_id=search_folder_id, top_level=False)


def get_folders(session: Session, content_filter: str = 'ALL', folder_id: Optional[str] = None, archived: bool = False,
                sort_order: str = 'createdAt ASC', only_pinned: bool = False, name_equals_filter: Optional[str] = None,
                types_filter: Optional[list[str]] = None,
                status_callback: Optional[Callable] = None) -> list[WorkbenchSearchResultPreviewV1]:
    folders_api = FoldersApi(session.client)
    offset = 0
    limit = session.options.search_page_size
    results: list[WorkbenchSearchResultPreviewV1] = list()
    kwargs = {
        'is_archived': archived,
        'sort_order': sort_order,
        'offset': offset,
        'limit': limit,
        'only_pinned': only_pinned
    }

    if _common.is_guid(folder_id):
        kwargs['folder_id'] = folder_id
    elif content_filter in ('OWNER', 'CORPORATE', 'USERS'):
        kwargs['folder_id'] = content_filter
    else:
        kwargs['filter'] = content_filter
    if name_equals_filter:
        kwargs['text_search'] = name_equals_filter
        kwargs['is_exact'] = True
    if types_filter:
        kwargs['types'] = types_filter

    while True:
        folders = folders_api.get_folders(**kwargs)
        results.extend(folders.content)

        if status_callback is not None:
            status_callback(len(folders.content))

        if len(folders.content) < limit:
            break

        offset += limit
        kwargs['offset'] = offset

    return results
