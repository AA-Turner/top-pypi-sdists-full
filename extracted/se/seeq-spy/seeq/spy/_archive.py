from __future__ import annotations

import types
from datetime import datetime, timedelta, timezone
from typing import Optional

import pandas as pd

from seeq.sdk import *
from seeq.spy import _common
from seeq.spy import _login
from seeq.spy._errors import *
from seeq.spy._redaction import safely
from seeq.spy._session import Session
from seeq.spy._status import Status


@Status.handle_keyboard_interrupt()
def archive(items: pd.DataFrame,
            *,
            note: Optional[str] = None,
            undo: bool = False,
            errors: Optional[str] = None,
            quiet: Optional[bool] = None,
            status: Optional[Status] = None,
            session: Optional[Session] = None) -> pd.DataFrame:
    """
    Archives (moves to the trash) the items whose IDs are in the input
    DataFrame.

    Parameters
    ----------
    items : pandas.DataFrame
        A DataFrame representing the items that should be archived. Each row
        must include a valid GUID in the "ID" column.

    note : str, default 'Archived from SPy by <username> at <timestamp>.'
        The note that will be added to the archival event for historic
        observability.

    undo : bool, default False
        If True, the items will be unarchived (moved out of the trash) instead
        of archived. The 'note' argument will be ignored.

    errors : {'raise', 'catalog'}, default 'raise'
        If 'raise', any errors encountered will cause an exception. If
        'catalog', errors will be added to a 'Result' column in the status.df
        DataFrame.

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
        A DataFrame with the metadata for the items that have been archived,
        along with any errors and statistics about the operation.

        Additionally, the following properties are stored on the "spy"
        attribute of the output DataFrame:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        func                A str value of 'spy.archive'
        kwargs              A dict with the values of the input parameters
                            passed to spy.archive to get the output DataFrame
        status              A spy.Status object with the status of the
                            spy.archive call
        =================== ===================================================

    Examples
    --------
    Search for signals with the name matching 'Well Head 00*' in the 'Custom Views' datasource and move
    them to the trash while ignoring any errors:

    >>> search_results = spy.search({'Name': 'Well Head 00*', 'Datasource Name': 'Custom Views'})
    >>> archive_results = spy.archive(search_results, errors='catalog')

    Pull the global asset tree with the name 'BioWorks Operations' and archive the entire heirarchy:

    >>> tree = spy.assets.Tree('BioWorks Operations', workbook=None)
    >>> archive_results = spy.archive(tree.df)

    Find all my workbooks with the name 'Condenser Maintenance' and trash them:

    >>> workbooks = spy.workbooks.search({'Name': 'Condenser Maintenance'}, content_filter='owner')
    >>> archive_results = spy.archive(workbooks)
    """
    input_args = _common.validate_argument_types([
        (items, 'items', pd.DataFrame),
        (note, 'note', str),
        (errors, 'errors', str),
        (quiet, 'quiet', bool),
        (status, 'status', Status),
        (session, 'session', Session)
    ])

    _login.validate_login(session, status)
    activity = 'archiv' if not undo else 'unarchiv'

    if not _common.present(items, 'ID'):
        raise SPyValueError('The items DataFrame must contain an "ID" column.')

    if note is None:
        note = f'Archived from SPy by {session.user.username} at {datetime.now(timezone.utc).isoformat()}.'

    item_count = len(items)
    results_list = list()
    status.df = pd.DataFrame([{'Count': 0, 'Time': timedelta(0)}])
    status.update(f'Archiving 0 of {item_count} items', Status.RUNNING)

    items_api = ItemsApi(session.client)

    def _handle_row(_row: pd.Series):
        """
        Safely archives the item with the given ID.
        Adds the row with the additional 'Result' column to the results_list.
        """
        _item_id = _row['ID']

        def _add_error_message_and_warn(msg):
            _row['Result'] = msg
            results_list.append(_row)
            status.warn(msg)

        def _archive_row():
            if not _common.is_guid(_item_id):
                raise SPyValueError(f'ID "{_item_id}" is not a valid GUID')
            items_api.archive_item(id=_item_id, note=note)
            _row['Result'] = 'Success'
            results_list.append(_row)

        def _unarchive_row():
            if not _common.is_guid(_item_id):
                raise SPyValueError(f'ID "{_item_id}" is not a valid GUID')
            items_api.set_property(id=_item_id, property_name='Archived', body=PropertyInputV1(value=False))
            _row['Result'] = 'Success'
            results_list.append(_row)

        _func = _unarchive_row if undo else _archive_row
        safely(lambda: _func(),
               action_description=f'{activity}e item with ID {_item_id}',
               additional_errors=[400, 409],
               on_error=_add_error_message_and_warn,
               status=status)

    def _update_status(_index, _result):
        completion_count = len(results_list)
        if completion_count % 100 == 0:
            status.df.at[0, 'Count'] = completion_count
            status.df.at[0, 'Time'] = status.get_timer()
            status.update(f'{activity.capitalize()}ing {completion_count} of {item_count} items',
                          Status.RUNNING)

    for index, row in items.iterrows():
        status.add_job(index, (_handle_row, row), _update_status)

    status.execute_jobs(session, simple=True)

    archive_result_df = pd.DataFrame(results_list)

    status.df.at[0, 'Count'] = len(results_list)
    status.df.at[0, 'Time'] = status.get_timer()
    if 'Result' in archive_result_df.columns:
        success_count = len(archive_result_df[archive_result_df['Result'] == 'Success'])
    else:
        success_count = 0

    status.update(f'Successfully {activity}ed {success_count} of {item_count} items', Status.SUCCESS)
    archive_df_properties = types.SimpleNamespace(func='spy.archive', kwargs=input_args, status=status)
    _common.put_properties_on_df(archive_result_df, archive_df_properties)

    return archive_result_df
