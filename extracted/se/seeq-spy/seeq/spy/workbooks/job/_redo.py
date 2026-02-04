from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import pandas as pd

from seeq.base import util
from seeq.spy._errors import *
from seeq.spy._status import Status
from seeq.spy.workbooks.job import _pull, _push


@Status.top_level_spy_function(no_session=True)
def redo(
    job_folder: Union[str, Path],
    workbooks_df: Union[pd.DataFrame, str, list] = None,
    *,
    action: Optional[str] = None,
    hard: bool = False,
    quiet: Optional[bool] = None,
    status: Optional[Status] = None
):
    """
    Marks a set of workbooks to be redone in the specified job folder.

    Parameters
    ----------
    job_folder : {str}
        A full or partial path to the job folder.

    workbooks_df : {pd.DataFrame, str, list}
        A DataFrame containing an 'ID' column that can be used to identify the
        workbooks to affect. These IDs are based on the source system (not the
        destination system). Alternatively, you can supply a workbook ID
        directly as a str or list of strs. If omitted, all workbooks in the
        job folder are affected.

    action : str
        If supplied, limits the redo to the specified actions. You can specify
        'pull' or 'push'. If not supplied, both pull and push are affected.
        Note that 'pull' automatically includes 'push'.

    hard : bool, default False
        If true, forces re-pushing of all inventory items. Otherwise, only
        causes re-push of workbook/worksheet/workstep definitions and Topic
        content.

    quiet : bool
        If True, suppresses progress output. Note that when status is
        provided, the quiet setting of the Status object that is passed
        in takes precedence.

    status : spy.Status, optional
        If specified, the supplied Status object will be updated as the command
        progresses. It gets filled in with the same information you would see
        in Jupyter in the blue/green/red table below your code while the
        command is executed.
    """
    if not util.safe_exists(job_folder):
        raise SPyValueError(f'Job folder "{job_folder}" does not exist.')

    if workbooks_df is None:
        job_workbooks_folder = _pull.get_workbooks_folder(job_folder)
        workbooks_df = pd.DataFrame([
            {'ID': workbook_id} for _, workbook_id in _pull.walk_workbook_folders(job_workbooks_folder)
        ])

    if isinstance(workbooks_df, str):
        workbooks_df = pd.DataFrame({'ID': [workbooks_df]})
    elif isinstance(workbooks_df, list):
        workbooks_df = pd.DataFrame({'ID': workbooks_df})

    if 'ID' not in workbooks_df:
        raise SPyValueError('workbooks_df must contain an ID column.')

    if action is not None:
        if action not in ['pull', 'push']:
            raise SPyValueError('action must be "pull" or "push".')
    else:
        action = 'pull'

    status_columns = [c for c in ['ID', 'Name', 'Type', 'Workbook Type'] if c in workbooks_df]

    status.df = workbooks_df[status_columns].copy()

    if action == 'pull':
        _pull.redo(job_folder, status)

    if action == 'push':
        _push.redo(job_folder, hard, status)

    status.update(
        'Successfully marked specified items to be redone. Execute spy.job.workbooks.pull() and/or '
        'spy.job.workbooks.push() again.', Status.SUCCESS)
