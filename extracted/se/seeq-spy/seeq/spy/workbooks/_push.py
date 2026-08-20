from __future__ import annotations

import datetime
import logging
import types
from pathlib import Path
from typing import Callable, List, Optional, Union

import numpy as np
import pandas as pd

from seeq.spy import _common
from seeq.spy import _login
from seeq.spy import _metadata
from seeq.spy._context import WorkbookContext
from seeq.spy._errors import *
from seeq.spy._session import Session
from seeq.spy._status import Status
from seeq.spy.workbooks import _folder
from seeq.spy.workbooks import _pull
from seeq.spy.workbooks import _user
from seeq.spy.workbooks._annotation import Annotation
from seeq.spy.workbooks._context import WorkbookPushContext, WorkbookPushMode, WorkbookPushParameters
from seeq.spy.workbooks._item import Item, ItemMap
from seeq.spy.workbooks._template import ItemTemplate
from seeq.spy.workbooks._workbook import Workbook, WorkbookList

MAX_PUSH_ERRORS_TO_DISPLAY = 10


@Status.top_level_spy_function()
def push(
        workbooks: Union[Workbook, List[Workbook], WorkbookList],
        *,
        path: Optional[Union[str, Callable]] = None,
        path_options: Optional[str] = None,
        owner: Optional[str] = None,
        label: Optional[str] = None,
        datasource: Optional[str] = None,
        datasource_map_folder: Optional[Union[str, Path]] = None,
        mode: str = WorkbookPushMode.NORMAL,
        access_control: Optional[str] = None,
        override_max_interp: bool = False,
        include_inventory: Optional[bool] = None,
        include_annotations: bool = True,
        dry_run: bool = False,
        refresh: bool = True,
        lookup_df: Optional[pd.DataFrame] = None,
        specific_worksheet_ids: Optional[List[str]] = None,
        create_dummy_items_in_workbook: Optional[str] = None,
        assume_dependencies_exist: bool = False,
        reconcile_inventory_by: str = 'id',
        global_inventory: Optional[str] = None,
        item_map: Optional[ItemMap] = None,
        verbose: bool = False,
        errors: Optional[str] = None,
        quiet: Optional[bool] = None,
        status: Optional[Status] = None,
        session: Optional[Session] = None,
        scope_globals_to_workbook: Optional[bool] = None,
        use_full_path: Optional[bool] = None
) -> pd.DataFrame:
    """
    Pushes workbooks into Seeq using a list of Workbook object definitions.

    Parameters
    ----------
    workbooks : {Workbook, list[Workbook], WorkbookList}
        A Workbook object, list of Workbook objects, or WorkbookList to be pushed into Seeq.

    path : {str, callable}, default None
        A '>>'-delimited folder path to create to contain the workbooks. Note
        that a further subfolder hierarchy will be created to preserve the
        relative paths that the folders were in when they were searched for
        and pulled.

        If you specify None, then the workbook will stay where it is (if it
        has already been pushed once).

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

    path_options : str, optional
        A comma-delimited combination of options that control how containing
        folders are reconstructed at the destination. Two independent
        settings can be specified, each of which is optional and defaults
        independently if omitted:

        - 'full' or 'relative' (default 'relative'): If 'full', the original
          full path for an item is reconstructed, as opposed to the path
          that is relative to the Path property supplied to the
          spy.workbooks.search() call that originally helped create these
          workbook definitions. Note that this full path will still be
          inside the folder specified by the 'path' argument, if supplied.

        - 'reconcile by id' or 'reconcile by name' (default 'reconcile by
          id'): Determines how SPy matches containing (ancestor) folders
          against folders that may already exist on the target server. The
          default, 'reconcile by id', matches folders via their Data ID
          (derived from the original folder's ID), which is how SPy has
          always behaved. 'reconcile by name' instead matches (or creates)
          folders purely by name within their parent folder, ignoring Data
          ID entirely.

        Example: path_options='full,reconcile by name'

    owner : str, default None
        Determines the ownership of pushed workbooks and folders.

        By default, the current owner will be preserved. If the content doesn't
        exist yet, the logged-in user will be the owner.

        All other options require that the logged-in user is an admin:

        If spy.workbooks.ORIGINAL_OWNER, ownership is assigned according to the
        original owner of the pulled content. (You must be an admin to use
        this.)

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
        reconcile_inventory_by must be 'id'; global_inventory must be
        'overwrite' or 'do not touch').

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

    include_inventory : bool, optional
        If True, then all calculated items that are scoped to the workbook
        will be pushed as well.

        If omitted, SPy will push inventory in any non-template scenarios.

    include_annotations : bool, default True
        If True, pushes the HTML for Journal and Organizer Topic content.

    dry_run : bool, default False
        If True, then no actual push will be performed. Instead, the function
        will simulate the push. Verbose logs will be printed as the operation
        proceeds.

    refresh : bool, default True
        If True, then the Workbook objects that were supplied as input will
        be updated to be "fresh" from the server after the push. All
        identifiers will reflect the actual pushed IDs. Since refreshing
        takes time, you can set this to False if you don't plan to make
        further modifications to the Workbook objects or use the new IDs.

    lookup_df : pd.DataFrame, optional
        A DataFrame of item metadata that can be used to look up identifiers
        that correspond to template parameters (when pushing AnalysisTemplate
        objects). This argument is automatically specified by the spy.push()
        function.

    specific_worksheet_ids : List[str], default None
        If supplied, only the worksheets with IDs specified in the supplied
        list will be pushed. This should be used when it would otherwise take
        too long to push all worksheets and you're interested in optimizing
        the push operation. No existing worksheets will be archived or moved
        in their ordering.

    create_dummy_items_in_workbook : str, optional
        If specified, then "dummy" items will be created for any stored items
        that are not successfully mapped to the target system. This is useful
        when you want to push a workbook to a system that doesn't have the same
        datasources/items as the source system. The dummy items will be
        created in the target system's "Seeq Data Lab" datasource and will
        have the same name as the original item, and no data. They will be
        scoped to the workbook specified.

    assume_dependencies_exist : bool, default False
        If True, then the push operation will assume that any dependencies
        not found in the set of workbooks pushed are already present on the
        target server. This is useful, for example, when you are pushing a
        subset of workbooks (like a single Organizer Topic) and don't need
        or want to push all of the referenced Workbench Analyses.

    reconcile_inventory_by : {'id', 'name'}, default 'id'
        Determines how SPy correlates inventory items being pushed with items
        that may already exist on the server. The default value is 'id', which
        reconciles (via the Data ID property) using the original ID of the
        item (which may or may not exist depending on whether you're pushing to
        the same server and/or using a label). The other option is 'name',
        which reconciles using the fully-qualified name (FQN) of the item. (The
        FQN includes the Path, Asset and Name.) This option makes the pushed
        items "compatible" with the spy.push(metadata) function, which allows
        you to use spy.Tree() to make modifications to an asset tree.

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

    item_map : dict
        A dictionary that "pre-maps" original IDs to new IDs. This is useful
        when you want to directly manage certain items and exclude them from the
        push. You can effectively tell SPy not to push/update an item just by
        adding a map where the original ID is the same as the new ID.

    verbose : bool
        If True, outputs verbose logs to a "spy_verbose_log.txt" file.
        Note that when status is provided, the verbose setting of the Status
        object that is passed in takes precedence.

    errors : {'raise', 'catalog'}, default 'raise'
        If 'raise', any errors encountered will cause an exception. If
        'catalog', errors will be added to a 'Result' column in the status.df
        DataFrame (errors='catalog' must be combined with
        status=<Status object>).

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

    scope_globals_to_workbook : bool, default False
        Deprecated. Use global_inventory instead: 'copy global' is the
        equivalent of False, 'copy local' is the equivalent of True.

    use_full_path : bool, optional
        Deprecated, use path_options instead: 'full' is equivalent to
        use_full_path=True, 'relative' (the default) is equivalent to
        use_full_path=False. Cannot be combined with path_options.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with status on the items pushed. The IDs for the pushed
        workbooks are in the "Pushed Workbook ID" column.

        Additionally, the following properties are stored on the "spy"
        attribute of the output DataFrame:

        =================== ===================================================
        Property            Description
        =================== ===================================================
        func                A str value of 'spy.workbooks.push'
        kwargs              A dict with the values of the input parameters
                            passed to this function
        input               The set of workbooks passed in to this function
        output              The set of workbooks pulled from the server if
                            refresh=True
        datasource          The datasource that all pushed items will fall
                            under (as a DatasourceOutputV1 object).
        item_map            A dictionary of IDs that map from the input
                            workbooks and inventory to the actual IDs as they
                            were created/updated on the server
        pushed_inventory    A dictionary of DataFrames that map from the
                            workbook ID to the DataFrame of any inventory that
                            was pushed along with the workbook
        status              A spy.Status object with the status of the
                            spy.workbooks.push call
        =================== ===================================================
    """
    input_args = locals()

    if (dry_run or verbose) and not status.verbose:
        status.set_verbose(True)

    status.add_log_section_marker('] Pushing')

    if dry_run:
        # Doesn't make sense to refresh when we're not actually pushing
        refresh = False

    if path_options is not None:
        if use_full_path is not None:
            raise SPyValueError('use_full_path argument cannot be combined with path_options. Use path_options '
                                'only.')
        use_full_path, match_folders_by_name = _folder.parse_path_options_str(path_options)
    elif use_full_path is not None:
        status.warn(f'use_full_path={use_full_path} is deprecated. Use path_options='
                    f'"{"full" if use_full_path else "relative"}" instead.')
        match_folders_by_name = False
    else:
        use_full_path, match_folders_by_name = False, False

    if not callable(path):
        if path == _folder.ORIGINAL_FOLDER and not use_full_path:
            raise SPyValueError('You must specify path_options="full" (or the deprecated use_full_path=True) when '
                                'path=spy.workbooks.ORIGINAL_FOLDER')

        if path == _folder.ORIGINAL_FOLDER and not session.user.is_admin:
            raise SPyValueError('Must be an admin to use path=spy.workbooks.ORIGINAL_FOLDER')

        if path == _folder.ORIGINAL_FOLDER and owner not in (_user.ORIGINAL_OWNER, _user.FORCE_ME_AS_OWNER):
            raise SPyValueError(
                'You must specify owner=spy.workbooks.ORIGINAL_OWNER or owner=spy.workbooks.FORCE_ME_AS_OWNER to use '
                'path=spy.workbooks.ORIGINAL_FOLDER')

    if owner == _user.ORIGINAL_OWNER and not session.user.is_admin:
        raise SPyValueError('Must be an admin to use owner=spy.workbooks.ORIGINAL_OWNER')

    if label is not None and ('[' in label or ']' in label):
        raise SPyValueError('label argument cannot contain square brackets []')

    if reconcile_inventory_by not in ['id', 'name']:
        raise SPyValueError('reconcile_inventory_by must be either "id" or "name"')

    if global_inventory is not None:
        # For compatibility with older versions
        if global_inventory == 'always reuse':
            global_inventory = 'overwrite'

        if global_inventory not in ['copy global', 'copy local', 'overwrite', 'do not touch']:
            raise SPyValueError(
                'global_inventory must be either "copy global", "copy local", "overwrite", or "do not touch"')

        if scope_globals_to_workbook is not None:
            raise SPyValueError('scope_globals_to_workbook argument cannot be combined with global_inventory. Use '
                                'global_inventory only.')
    else:
        if scope_globals_to_workbook is not None:
            if scope_globals_to_workbook:
                status.warn('scope_globals_to_workbook=True is deprecated. Use global_inventory="copy local" instead.')
                global_inventory = 'copy local'
            else:
                status.warn(
                    'scope_globals_to_workbook=False is deprecated. Use global_inventory="copy global" instead.')
                global_inventory = 'copy global'
        else:
            global_inventory = 'copy global'

    # Validate mode parameter
    if mode not in ['normal', 'in-place datasource swap']:
        raise SPyValueError('mode must be either "normal" or "in-place datasource swap"')

    # Validate in-place datasource swap mode requirements
    if mode == 'in-place datasource swap':
        if datasource_map_folder is None:
            raise SPyValueError('datasource_map_folder must be specified when mode="in-place datasource swap"')
        if path is not None:
            raise SPyValueError('path must be None when mode="in-place datasource swap"')
        if owner is not None:
            raise SPyValueError('owner must be None when mode="in-place datasource swap"')
        if label is not None:
            raise SPyValueError('label must be None when mode="in-place datasource swap"')
        if datasource is not None:
            raise SPyValueError('datasource must be None when mode="in-place datasource swap"')
        if use_full_path or match_folders_by_name:
            raise SPyValueError('path_options must be left at its default (or use_full_path must be False) when '
                                'mode="in-place datasource swap"')
        if access_control is not None:
            raise SPyValueError('access_control must be None when mode="in-place datasource swap"')
        if override_max_interp is not False:
            raise SPyValueError('override_max_interp must be False when mode="in-place datasource swap"')
        if include_inventory is not None:
            raise SPyValueError('include_inventory must be None when mode="in-place datasource swap"')
        if include_annotations is not True:
            raise SPyValueError('include_annotations must be True when mode="in-place datasource swap"')
        if create_dummy_items_in_workbook is not None:
            raise SPyValueError('create_dummy_items_in_workbook must be None when mode="in-place datasource swap"')
        if assume_dependencies_exist is not False:
            raise SPyValueError('assume_dependencies_exist must be False when mode="in-place datasource swap"')
        if reconcile_inventory_by != 'id':
            raise SPyValueError('reconcile_inventory_by must be "id" when mode="in-place datasource swap"')
        if global_inventory not in ['overwrite', 'do not touch']:
            raise SPyValueError('global_inventory must be "overwrite" or "do not touch" when '
                                'mode="in-place datasource swap"')
    else:
        if global_inventory == 'do not touch':
            raise SPyValueError('global_inventory="do not touch" is only valid when mode="in-place datasource swap"')

    if isinstance(item_map, dict):
        for k, v in item_map.values():
            if not _common.is_guid(k) or not _common.is_guid(v):
                raise SPyValueError('item_map keys and values must be IDs')
        item_map = ItemMap(item_map)

    owner_identity = None
    if owner not in [None, _user.ORIGINAL_OWNER, _user.FORCE_ME_AS_OWNER]:
        owner_identity = _login.find_user(session, owner)
        owner = owner_identity.id

    status.update('Pushing workbooks', Status.RUNNING)

    if item_map is None:
        item_map = ItemMap(lookup_df=lookup_df)

    if not isinstance(workbooks, list):
        workbooks = [workbooks]

    # Make sure the datasource exists (skip for in-place datasource swap mode)
    datasource_output = None
    if mode != WorkbookPushMode.IN_PLACE_DATASOURCE_SWAP:
        datasource_output = _metadata.create_datasource(session, datasource, status=status, dry_run=dry_run)

    workbook_context: Optional[WorkbookContext] = None
    if create_dummy_items_in_workbook is not None:
        workbook_context = WorkbookContext.from_args(session, status, create_dummy_items_in_workbook,
                                                     None, datasource, dry_run=dry_run)

    context = WorkbookPushContext(
        dummy_items_workbook_context=workbook_context,
        session=session,
        pushed_inventory={},
        status=status,
        dry_run=dry_run,
        datasource_output=datasource_output,
    )

    # Sort such that Analyses are pushed before Topics, since the latter usually depends on the former
    remaining_workbooks = list()
    sorted_workbooks = sorted(list(workbooks), key=lambda w: w['Workbook Type'])
    status.df = pd.DataFrame(columns=['ID', 'Name', 'Type', 'Workbook Type', 'Count', 'Time', 'Errors', 'Result'])
    for index in range(len(sorted_workbooks)):  # type: int
        workbook = sorted_workbooks[index]
        remaining_workbooks.append((index, workbook))
        status.df.at[index, 'ID'] = workbook.id if workbook.id else np.nan
        status.df.at[index, 'Name'] = workbook.name
        status.df.at[index, 'Type'] = workbook.type
        status.df.at[index, 'Workbook Type'] = workbook['Workbook Type']
        status.df.at[index, 'Count'] = 0
        status.df.at[index, 'Time'] = datetime.timedelta(0)
        status.df.at[index, 'Errors'] = 0
        status.df.at[index, 'Result'] = 'Queued'

    if datasource_map_folder:
        context.datasource_map_overrides = Workbook.load_datasource_maps(datasource_map_folder, overrides=True,
                                                                         status=status)
        context.add_server_scoped_item_level_map_files(context.datasource_map_overrides)

    at_least_one_thing_pushed = False
    search_folder_ids = dict()
    while len(remaining_workbooks) > 0:
        at_least_one_thing_pushed_this_iteration = False

        dependencies_not_found = list()
        for index, workbook in remaining_workbooks.copy():  # type: (int, Workbook)
            if not isinstance(workbook, Workbook):
                raise SPyRuntimeError('"workbooks" argument contains a non Workbook item: %s' % workbook)

            if label is None:
                # If a label is not supplied, check to see if we should be automatically isolating by user.
                isolate_by_user = False
                if _common.get(workbook.definition, 'Isolate By User', default=False):
                    # Workbooks can be marked as 'Isolate By User' so they're not stepping on each other when
                    # they do spy.workbook.push(). All of the Example Exports are marked with "Isolate By User"
                    # equal to True.
                    status.log('Isolating pushed items by user due to workbook setting "Isolate By User"')
                    isolate_by_user = True

                if workbook.provenance == Item.CONSTRUCTOR:
                    # If a Workbook is constructed (and not persisted -- i.e., not pulled/loaded) then the best
                    # policy is to isolate such workbooks so that their Data IDs can't collide in the event that
                    # two users happen to name their workbooks the same.
                    status.log('Isolating pushed items by user due to workbook provenance being CONSTRUCTOR')
                    isolate_by_user = True

                if isolate_by_user:
                    label = owner_identity.username if owner_identity is not None else session.user.username

            resolved_path = path(workbook.real) if callable(path) else path

            push_params = WorkbookPushParameters(
                path=resolved_path,
                owner=owner,
                label=label,
                mode=mode,
                use_full_path=use_full_path,
                match_folders_by_name=match_folders_by_name,
                access_control=access_control,
                override_max_interp=override_max_interp,
                include_inventory=include_inventory,
                include_annotations=include_annotations,
                specific_worksheet_ids=specific_worksheet_ids.copy() if specific_worksheet_ids is not None else None,
                create_dummy_items_in_workbook=create_dummy_items_in_workbook,
                assume_dependencies_exist=assume_dependencies_exist,
                reconcile_inventory_by=reconcile_inventory_by,
                global_inventory=global_inventory,
            )

            context.current_params = push_params

            if isinstance(workbook, ItemTemplate) and push_params.label is not None:
                raise SPyValueError('Cannot specify a label when pushing a Template workbook')

            try:
                status.reset_timer()
                status.current_df_index = index
                status.put('Count', 0)
                status.put('Time', datetime.timedelta(0))
                status.put('Result', 'Pushing')

                status.update('[%d/%d] Pushing %s "%s" (%s)' %
                              (len(status.df[status.df['Result'] != 'Queued']),
                               len(status.df), workbook['Workbook Type'], workbook['Name'],
                               workbook['ID']),
                              Status.RUNNING)

                context.datasource_maps = workbook.datasource_maps.copy()
                context.datasource_maps.extend(context.datasource_map_overrides.copy(), overwrite=True)

                try:
                    if push_params.include_inventory is None:
                        include_inventory_for_this_workbook = not isinstance(workbook, ItemTemplate)
                        if include_inventory_for_this_workbook:
                            status.log('"include_inventory" is None; including inventory for this workbook because it '
                                       'is not a Template')
                        else:
                            status.log('"include_inventory" is None; not including inventory for this workbook because '
                                       'it is a Template')
                    else:
                        status.log(f'"include_inventory" is {push_params.include_inventory}')
                        include_inventory_for_this_workbook = push_params.include_inventory

                    if not include_inventory_for_this_workbook and len(context.datasource_map_overrides) > 0:
                        status.warn('Ignoring datasource_map_folder argument because inventory is not being pushed. '
                                    'Add include_inventory=True to push inventory and use the datasource map folder.')

                    if context.current_params.mode != WorkbookPushMode.IN_PLACE_DATASOURCE_SWAP:
                        search_folder_id, workbook_folder_id = workbook.push_containing_folders(
                            context, item_map, push_params.use_full_path, push_params.path,
                            push_params.owner, push_params.label, push_params.access_control,
                            match_folders_by_name=push_params.match_folders_by_name)
                    else:
                        if 'Ancestors' not in workbook or len(workbook['Ancestors']) == 0:
                            workbook_folder_id = None
                            search_folder_id = None
                        else:
                            workbook_folder_id = workbook['Ancestors'][-1]
                            search_folder_id = workbook_folder_id

                    search_folder_ids[workbook.id] = search_folder_id

                    # Grab the success message now because already_pushed will always be true after the push
                    success_message = 'Success'
                    if workbook.already_pushed:
                        success_message += ': Already pushed'

                    try:
                        workbook.push(context=context, folder_id=workbook_folder_id, item_map=item_map,
                                      label=push_params.label,
                                      include_inventory=include_inventory_for_this_workbook)
                    except (SPyException, ApiException) as e:
                        status.raise_or_put(e, 'Result')
                        continue

                    at_least_one_thing_pushed = True
                    at_least_one_thing_pushed_this_iteration = True

                    remaining_workbooks.remove((index, workbook))

                    status.put('Time', status.get_timer())
                    status.put('Errors', len(workbook.push_errors))

                    if len(workbook.push_errors) > 0:
                        errors_str = _format_workbook_push_errors(workbook.push_errors, context, status)
                        success_message += f', but with errors:\n{errors_str}'
                        status.put('Result', success_message)
                        status.log(f'{workbook}: {success_message}', level=logging.ERROR)
                        if status.errors == 'raise':
                            raise SPyRuntimeError(errors_str)
                    else:
                        status.put('Result', success_message)
                        status.log(f'{workbook}: {success_message}')

                except SPyDependencyNotFound as e:
                    status.put('Count', 0)
                    status.put('Time', datetime.timedelta(0))
                    status.put('Errors', 0)
                    status.put('Result', f'Need dependency: {str(e)}')
                    if not e.intentional_no_mapping:
                        dependencies_not_found.append(str(e))

            except ApiException as e:
                raise SPyRuntimeError(_common.format_exception(e)) from e

        if not at_least_one_thing_pushed_this_iteration:
            if assume_dependencies_exist and not item_map.fall_through:
                item_map.fall_through = True
                continue

            if status.errors == 'raise':
                raise SPyRuntimeError('Could not find the following dependencies:\n%s\n'
                                      'Therefore, could not push the following workbooks:\n%s\n' %
                                      ('\n'.join(dependencies_not_found),
                                       '\n'.join([str(workbook) for _, workbook in remaining_workbooks])))

            break

    Annotation.push_fixups(context, item_map)

    new_workbooks = None
    if refresh and at_least_one_thing_pushed:
        refresh_workbook_inner_status = status.create_inner('Refresh Workbook')

        new_workbooks = WorkbookList()
        for workbook in workbooks:
            old_workbook_id = workbook.id
            if context.current_params.mode == WorkbookPushMode.IN_PLACE_DATASOURCE_SWAP:
                new_workbook_id = workbook.id
            else:
                new_workbook_id = item_map[workbook.id]

            specific_worksheet_ids_to_pull = None
            if specific_worksheet_ids is not None:
                specific_worksheet_ids_to_pull = [item_map[ws] for ws in specific_worksheet_ids]

            include_inventory_for_refresh = include_inventory if include_inventory is not None else True
            pulled_workbooks = _pull.pull(new_workbook_id, include_inventory=include_inventory_for_refresh,
                                          specific_worksheet_ids=specific_worksheet_ids_to_pull,
                                          include_annotations=include_annotations, status=refresh_workbook_inner_status,
                                          session=session)

            new_workbook = pulled_workbooks[0]
            new_workbooks.append(new_workbook)

            if isinstance(workbook, ItemTemplate):
                continue

            workbook.refresh_from(context, new_workbook, item_map, refresh_workbook_inner_status,
                                  include_inventory=include_inventory_for_refresh,
                                  specific_worksheet_ids=specific_worksheet_ids)

            search_folder_id = search_folder_ids.get(old_workbook_id)
            if (search_folder_id is not None and search_folder_id != _common.PATH_ROOT and
                    search_folder_id != _folder.ORIGINAL_FOLDER):
                workbook['Search Folder ID'] = search_folder_id

    max_errors = status.df['Errors'].max()
    if max_errors > 0:
        status.update('Errors encountered, look at Result column in returned DataFrame', Status.FAILURE)
        if status.log_file is not None:
            status.log(f'Open a terminal and execute the following command to see the errors:\n'
                       f'{status.get_grep_errors_command()}')
    else:
        status.update('Push successful', Status.SUCCESS)

    output_df_properties = types.SimpleNamespace(
        func='spy.workbooks.push',
        kwargs=input_args,
        input=workbooks,
        output=new_workbooks,
        datasource=datasource_output,
        pushed_inventory=context.pushed_inventory,
        item_map=item_map,
        status=status)

    output_df = status.df.copy()

    status.log(f'Final results:\n{output_df.to_string(index=False)}')

    _common.put_properties_on_df(output_df, output_df_properties)

    return output_df


def _format_workbook_push_errors(push_errors: set, context: WorkbookPushContext, status: Status) -> str:
    sorted_errors = sorted(list(push_errors))
    errors_remaining_budget = MAX_PUSH_ERRORS_TO_DISPLAY - context.errors_displayed_count

    if errors_remaining_budget > 0:
        errors_to_display = sorted_errors[:errors_remaining_budget]
        context.errors_displayed_count += len(errors_to_display)

        errors_str = '\n'.join(errors_to_display)

        total_undisplayed = len(sorted_errors) - len(errors_to_display)
        if total_undisplayed > 0 or context.errors_displayed_count >= MAX_PUSH_ERRORS_TO_DISPLAY:
            if status.log_filename is not None:
                additional_message = (
                    f'\n\n{total_undisplayed} additional error(s) from this workbook not shown above. '
                    f'Check the log file for all errors: {status.log_filename}')
            else:
                additional_message = (
                    f'\n\n{total_undisplayed} additional error(s) from this workbook not shown above. '
                    f'To see all errors, specify a log file by setting verbose=True')
            errors_str += additional_message

        return errors_str
    else:
        if status.log_filename is not None:
            return (f'{len(sorted_errors)} error(s) occurred but error display limit reached. '
                    f'Check the log file for all errors: {status.log_filename}')
        else:
            return (f'{len(sorted_errors)} error(s) occurred but error display limit reached. '
                    f'To see all errors, specify a log file by setting verbose=True')
