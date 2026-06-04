from __future__ import annotations

import json
import os
import pickle
import types
from pathlib import Path
from typing import Callable, List, Optional, Union, Tuple

import pandas as pd

from seeq import spy
from seeq.base import util
from seeq.spy import _common
from seeq.spy._errors import *
from seeq.spy._session import Session
from seeq.spy._status import Status
from seeq.spy.workbooks._context import WorkbookPushContext, WorkbookPushMode
from seeq.spy.workbooks._item import Item
from seeq.spy.workbooks._item_map import ItemMap
from seeq.spy.workbooks._workbook import Workbook
from seeq.spy.workbooks.job import _pull


@Status.top_level_spy_function()
def push(
        job_folder: Union[str, Path],
        *,
        resume: bool = True,
        path: Optional[Union[str, Callable]] = None,
        owner: Optional[str] = None,
        label: Optional[str] = None,
        datasource: Optional[str] = None,
        datasource_map_folder: Optional[Union[str, Path]] = None,
        mode: str = WorkbookPushMode.NORMAL,
        use_full_path: bool = False,
        access_control: Optional[str] = None,
        override_max_interp: bool = False,
        global_inventory: Optional[str] = None,
        create_dummy_items: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
        errors: Optional[str] = None,
        quiet: Optional[bool] = None,
        status: Optional[Status] = None,
        session: Optional[Session] = None,
        scope_globals_to_workbook: Optional[bool] = None
) -> pd.DataFrame:
    """
    Pushes the definitions for each workbook that was pulled by the
    spy.workbooks.job.pull() function, in a restartable "job"-like fashion.

    Parameters
    ----------
    job_folder : {str, pathlib.Path}
        A full or partial path to the job folder created by
        spy.workbooks.job.pull().

    resume : bool, default True
        True if the push should resume from where it left off, False if it
        should push everything again.

    path : {str, callable}, default None
        A '>>'-delimited folder path to create to contain the workbooks. Note
        that a further subfolder hierarchy will be created to preserve the
        relative paths that the folders were in when they were searched for
        and pulled. If you specify None, then the workbook will stay where
        it is (if it has already been pushed once).

        If you specify spy.workbooks.MY_FOLDER, it will be moved to the user's
        home folder.

        If you specify a folder ID directly, it will be pushed to that folder.

        If you specify spy.workbooks.ORIGINAL_FOLDER, it will be pushed to the
        folder it was in when it was originally pulled. The folder hierarchy
        will be recreated on the target server if it doesn't already exist.
        (You must be an admin to use this to ensure you have permissions to
        put things where they need to go.)

        If you specify a callable, it will be called once per workbook with the
        Workbook instance as its sole argument and must return the desired path
        string (or None) for that workbook. This allows you to route different
        workbooks to different folders in a single push call.

    owner : str, default None
        Determines the ownership of pushed workbooks and folders.

        By default, the current owner will be preserved. If the content doesn't
        exist yet, the logged-in user will be the owner.

        All other options require that the logged-in user is an admin:

        If spy.workbooks.ORIGINAL_OWNER, ownership is assigned according to the
        original owner of the pulled content.

        If spy.workbooks.FORCE_ME_AS_OWNER, existing content will be
        reassigned to the logged-in user.

        If a username or a user's Seeq ID is supplied, that user will be
        assigned as owner.

        You may need to supply an appropriate datasource map if the usernames
        are different between the original and the target servers.

    label : str
        A user-defined label that differentiates this push operation from
        others. By default, the label will be the logged-in user's username
        OR the username from the 'owner' argument so that push activity will
        generally be isolated by user. But you can override this with a label
        of your choosing.

    datasource : str, optional, default 'Seeq Data Lab'
        The name of the datasource within which to contain all the pushed items.
        Items inherit access control permissions from their datasource unless it
        has been overridden at a lower level. If you specify a datasource using
        this argument, you can later manage access control (using spy.acl functions)
        at the datasource level for all the items you have pushed.

        If you instead want access control for your items to be inherited from the
        workbook they are scoped to, specify `spy.INHERIT_FROM_WORKBOOK`.

    datasource_map_folder : {str, pathlib.Path}, default None
        A folder containing Datasource_Map_Xxxx_Yyyy_Zzzz.json files that can
        provides a means to map stored items (i.e., those originating from
        external datasources like OSIsoft PI) from one server to another or
        from one datasource to another (i.e., for workbook swapping). A default
        set of datasource map files is created during a pull/save sequence, and
        you can copy these default files to a folder, alter them, and then
        specify the folder as this argument.

    mode : {'normal', 'in-place datasource swap'}, default 'normal'
        The push mode to use. The default is 'normal', which performs a full
        push of all workbook content and inventory. When set to 'in-place
        datasource swap', the push operation performs minimal updates to effect
        a datasource swap using the provided datasource_map_folder. This mode
        requires datasource_map_folder to be specified and enforces specific
        parameter constraints (path, owner, label, and datasource must be None;
        reconcile_inventory_by must be 'id'; global_inventory must be either
        'overwrite' or 'do not touch').

    use_full_path : bool, default False
        If True, the original full path for an item is reconstructed, as
        opposed to the path that is relative to the Path property supplied to
        the spy.workbooks.search() call that originally helped create these
        workbook definitions. Note that this full path will still be inside
        the folder specified by the 'path' argument, if supplied.

    access_control : str, default None
        Specifies how Access Control Lists should be treated, via the
        following keywords: add/replace,loose/strict

        - If None, then no access control entries are pushed.
        - If 'add', then existing access control entries will not be disturbed
          but new entries will be added.
        - If 'replace', then existing access control entries will be removed
          and replaced with the entries from workbook definitions.
        - If 'loose', then any unmapped users/groups from the workbook
          definitions will be silently ignored.
        - If 'strict', then any unmapped users/groups will result in errors.

        Example: access_control='replace,loose'

    override_max_interp : bool, default False
        If True, then the Maximum Interpolation overrides from the source
        system will be written to the destination system.

    global_inventory : {'copy global', 'copy local', 'overwrite', 'do not touch'}, default 'copy global'
        Determines how SPy handles global inventory items, especially in
        conjunction with a label argument. 'copy global' will cause different
        global items to be created if their labels differ. If no label is
        specified, the existing global item will be reused/updated if possible.
        'copy local' will scope the global items to the pushed workbook,
        making copies for different workbooks if necessary. 'overwrite' will
        use an existing global item if possible and ignore the label. 'do not touch'
        will skip processing global inventory entirely, using the items as-is
        without any modifications or datasource mapping.

    create_dummy_items : bool, default False
        If true, then "dummy" items will be created for any stored items
        that are not successfully mapped to the target system. This should
        be specified as True if you intend to use the spy.workbooks.job.data
        module. The dummy items will be created in the target system's
        "Seeq Data Lab" datasource and will have the same name as the original
        item, and no data. They will be scoped to a workbook under a
        "SPy Workbook Jobs" folder and named after the job folder.

    dry_run : bool, default False
        If True, then no actual push will be performed. Instead, the function
        will simulate the push. Verbose logs will be printed as the operation
        proceeds.

    verbose : bool
        If True, outputs verbose logs to "push_log.txt" within the job folder.
        Note that when status is provided, the verbose setting of the Status
        object that is passed in takes precedence.

    errors : {'raise', 'catalog'}, default 'raise'
        If 'raise', any errors encountered will cause an exception. If
        'catalog', errors will be added to a 'Result' column in the status.df
        DataFrame (errors='catalog' must be combined with
        status=<Status object>).

    quiet : bool
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

    scope_globals_to_workbook : bool, default False
        Deprecated. Use global_inventory instead: 'copy global' is the
        equivalent of False, 'copy local' is the equivalent of True.

    """
    input_args = locals()

    # Jobs always write the log file, even if the user doesn't want verbose
    default_log_file = os.path.join(job_folder, 'push_log.txt')
    status.validate_verbose(verbose, default_log_file)
    status.add_log_section_marker('] Pushing')

    function_name = 'spy.workbooks.job.push'

    if not util.safe_exists(job_folder):
        raise SPyValueError(f'Job folder "{job_folder}" does not exist.')

    item_map = ItemMap()
    if resume:
        item_map = load_item_map(job_folder)

    workbook_list: List[WorkbookFolderRef] = list()
    job_workbooks_folder = _pull.get_workbooks_folder(job_folder)
    for workbook_folder, _ in _pull.walk_workbook_folders(job_workbooks_folder):
        full_workbook_folder = os.path.join(job_workbooks_folder, workbook_folder)
        if not resume and _PUSH_COMPLETE.is_complete(full_workbook_folder):
            _PUSH_COMPLETE.clear(full_workbook_folder)
        workbook_list.append(WorkbookFolderRef(full_workbook_folder, job_folder))

    job_datasource_map_folder = datasource_map_folder

    if job_datasource_map_folder is None:
        # We used to copy datasource maps to Datasource Maps and always use them as overrides, which causes
        # subtle, confusing behavior differences between spy.workbooks.job.push() and spy.workbooks.push().
        # Now we use the Datasource Map Overrides/Possibilities scheme, but for backward compatibility we look
        # for the old folder and use it if it exists (and trigger the old, confusing, behavior).
        if util.safe_exists(os.path.join(job_folder, 'Datasource Maps')):
            job_datasource_map_folder = os.path.join(job_folder, 'Datasource Maps')
            item_map.only_override_maps = True
        elif util.safe_exists(os.path.join(job_folder, 'Datasource Map Overrides')):
            job_datasource_map_folder = os.path.join(job_folder, 'Datasource Map Overrides')

    create_dummy_items_in_workbook = get_dummy_workbook_name(job_folder) if create_dummy_items else None

    spy.workbooks.push(workbook_list, path=path, owner=owner, label=label, datasource=datasource, mode=mode,
                       use_full_path=use_full_path, access_control=access_control,
                       override_max_interp=override_max_interp, global_inventory=global_inventory,
                       datasource_map_folder=job_datasource_map_folder, refresh=False,
                       create_dummy_items_in_workbook=create_dummy_items_in_workbook,
                       dry_run=dry_run, status=status, session=session, item_map=item_map,
                       scope_globals_to_workbook=scope_globals_to_workbook)

    results_df = status.df.copy()

    results_df_properties = types.SimpleNamespace(
        func='spy.workbooks.job.push',
        kwargs=input_args,
        status=status,
        item_map=item_map
    )

    _common.put_properties_on_df(results_df, results_df_properties)

    return results_df


_PUSH_COMPLETE = _pull.CompletionFlagHelper('Completely Pushed')


def get_item_map_filename(job_folder):
    return os.path.join(job_folder, 'item_map.pickle')


def load_item_map(job_folder):
    item_map_file = get_item_map_filename(job_folder)
    if not util.safe_exists(item_map_file):
        return ItemMap()

    with util.safe_open(item_map_file, 'rb') as f:
        return pickle.load(f)


def save_item_map(job_folder, item_map):
    item_map_file = get_item_map_filename(job_folder)
    with util.safe_open(item_map_file, 'wb') as f:
        pickle.dump(item_map, f, protocol=_common.DEFAULT_PICKLE_PROTOCOL)


def get_dummy_workbook_name(job_folder):
    return f'SPy Dummy Workbooks >> Dummy Workbook for {job_folder}'


def redo(job_folder: str, hard: bool, status: Status):
    job_workbooks_folder = _pull.get_workbooks_folder(job_folder)
    workbook_folders = {i: f for f, i in _pull.walk_workbook_folders(job_workbooks_folder)}
    workbook_ids: pd.Series = status.df['ID']
    for index, workbook_id in workbook_ids.items():
        if workbook_id in workbook_folders:
            _PUSH_COMPLETE.clear(os.path.join(job_workbooks_folder, workbook_folders[workbook_id]))
            item_map_file = get_item_map_filename(job_folder)
            if hard and util.safe_exists(item_map_file):
                util.safe_remove(item_map_file)
            status.df.at[index, 'Result'] = 'Push will be redone' + (', including all inventory' if hard else '')
        else:
            status.df.at[index, 'Result'] = 'Not found'


class WorkbookFolderRef(Workbook):
    workbook_folder: str
    _real_workbook: Optional[Workbook]
    _search_folder_id: Optional[str]
    _parent_folder_id: Optional[str]

    def __init__(self, workbook_folder, job_folder):
        super().__init__()

        self.workbook_folder = workbook_folder
        self.job_folder = job_folder
        self._provenance = Item.LOAD
        self._real_workbook = None
        self._search_folder_id = None
        self._parent_folder_id = None

        with util.safe_open(os.path.join(self.workbook_folder, 'Workbook.json'), 'r', encoding='utf-8') as f:
            self._definition = json.load(f)

    @property
    def already_pushed(self):
        return _PUSH_COMPLETE.is_complete(self.workbook_folder)

    @property
    def real(self):
        self._ensure_loaded()
        return self._real_workbook

    def _ensure_loaded(self):
        if self._real_workbook is not None:
            return

        self._real_workbook = Workbook.load(self.workbook_folder)

    @property
    def datasource_maps(self):
        return self.real.datasource_maps

    def push_containing_folders(self, context: WorkbookPushContext, item_map: ItemMap, use_full_path,
                                parent_folder_id, owner, label, access_control) -> Tuple[Optional[str], Optional[str]]:
        if _PUSH_COMPLETE.is_complete(self.workbook_folder):
            d = _PUSH_COMPLETE.get_data(self.workbook_folder)

            # Older versions of SPy didn't store off Search Folder ID so we use get() to maintain compatibility with
            # existing job folders.
            self._search_folder_id = d.get('Search Folder ID')
            self._parent_folder_id = d.get('Parent Folder ID')
            return self._search_folder_id, self._parent_folder_id

        self._search_folder_id, self._parent_folder_id = self.real.push_containing_folders(
            context, item_map, use_full_path, parent_folder_id, owner, label, access_control)

        return self._search_folder_id, self._parent_folder_id

    def push(self, *, context: WorkbookPushContext, folder_id=None, item_map: ItemMap = None, label=None,
             include_inventory=True):
        if self.already_pushed:
            self._push_errors = Workbook.load_push_errors(self.workbook_folder)
            context.status.put('Pushed Workbook ID', item_map[self.id])
            link_url = Workbook.construct_url(
                context.session,
                folder_id,
                item_map[self.id]
            )
            context.status.put('URL', link_url)
            return

        try:
            self._real_workbook.push(context=context, folder_id=folder_id, item_map=item_map, label=label,
                                     include_inventory=include_inventory)
        finally:
            self._push_errors = self._real_workbook.push_errors

        if context.dry_run:
            return

        save_item_map(self.job_folder, item_map)
        Workbook.save_push_errors(self.workbook_folder, self._push_errors)
        if context.status.errors == 'catalog' or len(self._real_workbook.push_errors) == 0:
            _PUSH_COMPLETE.mark(self.workbook_folder, {
                'Search Folder ID': self._search_folder_id,
                'Parent Folder ID': self._parent_folder_id
            })
