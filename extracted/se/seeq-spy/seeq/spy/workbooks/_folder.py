from __future__ import annotations

from typing import List, Optional, Tuple

from seeq.sdk import *
from seeq.spy import _common
from seeq.spy._errors import *
from seeq.spy._redaction import safely, request_safely
from seeq.spy._session import Session
from seeq.spy._status import Status
from seeq.spy.workbooks._context import WorkbookPushContext
from seeq.spy.workbooks._item import Item, ItemMap
from seeq.spy.workbooks._user import ItemWithOwnerAndAcl

SHARED = '__Shared__'
CORPORATE = '__Corporate__'
ALL = '__All__'
USERS = '__Users__'
MY_FOLDER = '__My_Folder__'
ORIGINAL_FOLDER = '__Original_Folder__'
PUBLIC = '__Public__'
SHARED_OR_PUBLIC = '__Shared_or_Public__'

SYNTHETIC_FOLDERS = [MY_FOLDER, SHARED, CORPORATE, ALL, USERS, PUBLIC, SHARED_OR_PUBLIC]

PATH_OPTIONS_FULL = 'full'
PATH_OPTIONS_RELATIVE = 'relative'
PATH_OPTIONS_RECONCILE_BY_ID = 'reconcile by id'
PATH_OPTIONS_RECONCILE_BY_NAME = 'reconcile by name'


def parse_path_options_str(path_options: str) -> Tuple[bool, bool]:
    use_full_path = None
    match_by_name = None

    for part in path_options.split(','):
        if part == PATH_OPTIONS_FULL:
            if use_full_path is not None:
                raise SPyValueError(f'path_options argument cannot specify both "{PATH_OPTIONS_FULL}" and '
                                    f'"{PATH_OPTIONS_RELATIVE}"')
            use_full_path = True
        elif part == PATH_OPTIONS_RELATIVE:
            if use_full_path is not None:
                raise SPyValueError(f'path_options argument cannot specify both "{PATH_OPTIONS_FULL}" and '
                                    f'"{PATH_OPTIONS_RELATIVE}"')
            use_full_path = False
        elif part == PATH_OPTIONS_RECONCILE_BY_ID:
            if match_by_name is not None:
                raise SPyValueError(f'path_options argument cannot specify both '
                                    f'"{PATH_OPTIONS_RECONCILE_BY_ID}" and "{PATH_OPTIONS_RECONCILE_BY_NAME}"')
            match_by_name = False
        elif part == PATH_OPTIONS_RECONCILE_BY_NAME:
            if match_by_name is not None:
                raise SPyValueError(f'path_options argument cannot specify both '
                                    f'"{PATH_OPTIONS_RECONCILE_BY_ID}" and "{PATH_OPTIONS_RECONCILE_BY_NAME}"')
            match_by_name = True
        else:
            raise SPyValueError(
                f'Invalid path_options argument: "{part}". path_options must be a comma-delimited combination of '
                f'one of "{PATH_OPTIONS_FULL}"/"{PATH_OPTIONS_RELATIVE}" and one of '
                f'"{PATH_OPTIONS_RECONCILE_BY_ID}"/"{PATH_OPTIONS_RECONCILE_BY_NAME}". For example: '
                f'path_options="{PATH_OPTIONS_RELATIVE},{PATH_OPTIONS_RECONCILE_BY_NAME}"')

    return use_full_path if use_full_path is not None else False, match_by_name if match_by_name is not None else False


def massage_ancestors(session: Session, item: Item):
    if not session.corporate_folder:
        return

    if len(item.definition['Ancestors']) > 0 and item.definition['Ancestors'][0] == session.corporate_folder.id:
        # Why replace the Corporate folder ID with the CORPORATE string token? The user doesn't want to have to
        # deal with the ID of the corporate folder, especially when importing/exporting workbooks from one server to
        # another.
        item.definition['Ancestors'][0] = CORPORATE


SYNTHETIC_FOLDER_TO_CONTENT_FILTER_MAP = {
    MY_FOLDER: 'OWNER',
    SHARED: 'SHARED',
    CORPORATE: 'CORPORATE',
    ALL: 'ALL',
    USERS: 'USERS',
    PUBLIC: 'PUBLIC',
    SHARED_OR_PUBLIC: 'SHAREDORPUBLIC'
}


def synthetic_folder_to_content_filter(synthetic_folder):
    if synthetic_folder not in SYNTHETIC_FOLDER_TO_CONTENT_FILTER_MAP:
        raise SPyValueError(f'Unrecognized synthetic folder: {synthetic_folder}')

    return SYNTHETIC_FOLDER_TO_CONTENT_FILTER_MAP[synthetic_folder]


def content_filter_to_synthetic_folder(content_filter: str):
    for synthetic_folder, mapped_content_filter in SYNTHETIC_FOLDER_TO_CONTENT_FILTER_MAP.items():
        if content_filter.upper() == mapped_content_filter:
            return synthetic_folder

    raise SPyValueError(f'Unrecognized content filter: {content_filter}')


class Folder(ItemWithOwnerAndAcl):
    """
    The SPy representation of a Seeq folder that can contain Analyses, Topics, and other Folders.
    """

    @staticmethod
    def pull(item_id, *, include_access_control=True,
             status: Status = None, session: Optional[Session] = None) -> Optional[Folder]:
        session = Session.validate(session)
        status = Status.validate(status, session)
        folders_api = FoldersApi(session.client)

        item_output = safely(lambda: Item._get_item_output(session, item_id),
                             action_description=f'pull Item {item_id}', status=status)
        if item_output is None:
            return None

        @request_safely(action_description=f'get Folder {item_id}', status=status)
        def _get_folder() -> FolderOutputV1:
            try:
                return folders_api.get_folder(
                    folder_id=item_id, full_ancestry=ItemWithOwnerAndAcl.should_use_full_ancestry(session))
            except TypeError:
                # full_ancestry is not supported in this version of Seeq
                return folders_api.get_folder(folder_id=item_id)

        folder_output = _get_folder()
        if folder_output is None:
            return None

        definition = Item._dict_from_item_output(item_output)
        folder = Folder(definition, provenance=Item.PULL)
        if include_access_control:
            folder._pull_owner_and_acl(session, folder_output.owner, status)
        folder._pull_ancestors(session, folder_output.ancestors)

        return folder

    def _pull_ancestors(self, session: Session, ancestors: List[ItemPreviewV1]):
        super()._pull_ancestors(session, ancestors)
        massage_ancestors(session, self)

    def _find_by_name(self, session: Session, folder_id, status: Status):
        folders_api = FoldersApi(session.client)

        offset = 0
        limit = session.options.search_page_size
        while True:
            if folder_id and folder_id != _common.PATH_ROOT:
                folders = safely(lambda: folders_api.get_folders(filter='owner' if folder_id is None else 'all',
                                                                 folder_id=folder_id,
                                                                 offset=offset,
                                                                 limit=limit),
                                 action_description=f'get "owner" folders within {folder_id}',
                                 additional_errors=[400],
                                 status=status)  # type: WorkbenchItemOutputListV1
            else:
                folders = folders_api.get_folders(filter='owner',
                                                  offset=offset,
                                                  limit=limit)  # type: WorkbenchItemOutputListV1

            content_dict = {content.name.lower(): content for content in folders.content}
            if self.name.lower() in content_dict and content_dict[self.name.lower()].type == 'Folder':
                found_folder = content_dict[self.name.lower()]
                Status.log_if(status, f'Found existing folder "{found_folder.name}" ({found_folder.id}) by name')
                return found_folder

            if len(folders.content) < limit:
                break

            offset += limit

        return None

    def push(self, context: WorkbookPushContext, parent_folder_id, datasource_output,
             item_map: ItemMap, *, owner=None, label=None, match_by_name: bool = False):
        session = context.session
        status = context.status
        items_api = ItemsApi(session.client)
        folders_api = FoldersApi(session.client)

        if _common.get(self, 'Unmodifiable', False):
            # Unmodifiable are system-managed folders, including the Corporate folder and individual user folders.
            # If we got this far, we have to assume that this is one of the user folders. We can't "push" to them and
            # we can't change their ACLs. But we need to map them appropriately. Unfortunately, we can only do this
            # if we are logged in as an admin.
            if not session.user.is_admin:
                status.log(f'Skipping unmodifiable folder {self["Name"]} since not logged in as admin')
                return None

            owner_id = self.decide_owner(context, item_map, owner=owner)
            home_folder = session.get_user_folder(owner_id)
            if home_folder is None:
                # User hasn't logged in yet, so their home folder doesn't exist
                # Create a dummy folder to trigger home folder creation, then archive it
                home_folder = create_user_folder_if_necessary(context, owner_id)
                if not context.dry_run and home_folder is None:
                    raise SPyRuntimeError(f'Could not find or create user folder for {owner}')

            if home_folder is not None:
                item_map[self.id] = home_folder.id
                status.log(f'Mapped unmodifiable folder {self["Name"]} to user\'s home folder '
                           f'({home_folder.id})')
            return home_folder

        if match_by_name:
            folder_item = self._find_by_name(session, parent_folder_id, status)
        else:
            folder_item = self.find_me(session, label, datasource_output, status=status)

            if folder_item is None and self.provenance == Item.CONSTRUCTOR:
                folder_item = self._find_by_name(session, parent_folder_id, status)

        folder_output: Optional[FolderOutputV1] = None
        if not folder_item:
            folder_input = FolderInputV1()
            folder_input.name = self['Name']
            if 'Description' in self:
                folder_input.description = self['Description']
            folder_input.owner_id = self.decide_owner(context, item_map, owner=owner)
            folder_input.parent_folder_id = parent_folder_id if parent_folder_id != _common.PATH_ROOT else None

            check_for_reserved_folder_name(folder_input.name)
            if not context.dry_run:
                folder_output = safely(lambda: folders_api.create_folder(body=folder_input),
                                       action_description=f'create Folder "{folder_input.name}"',
                                       status=status)  # type: FolderOutputV1
                if folder_output is not None:
                    status.log(f'Created Folder "{folder_output.name}" under parent ID {parent_folder_id}')
            else:
                status.log(f'[Dry Run] Would create Folder "{folder_input.name}" under parent ID'
                           f' {parent_folder_id}')

            if not match_by_name:
                # Folders reconciled by name are intentionally not tracked via Data ID, since that's the whole
                # point of matching by name -- stamping a Data ID here risks a collision (e.g. two ancestor
                # folders that share the same source ID/Custody ID being pushed to different destinations).
                props = [
                    ScalarPropertyV1(name='Datasource Class', value=datasource_output.datasource_class),
                    ScalarPropertyV1(name='Datasource ID', value=datasource_output.datasource_id),
                    ScalarPropertyV1(name='Data ID', value=self._construct_data_id(label))]

                new_folder_id_str = f' {folder_output.id}' if folder_output is not None else ''
                safely(lambda: items_api.set_properties(id=folder_output.id, body=props),
                       action_description=f'set common properties (e.g. Data ID) for new Folder{new_folder_id_str}',
                       status=status, dry_run=context.dry_run)
        else:
            folder_output = safely(lambda: folders_api.get_folder(folder_id=folder_item.id),
                                   action_description=f'get Folder {folder_item.id}',
                                   status=status)  # type: FolderOutputV1
            if folder_output is None:
                return None

            props = [ScalarPropertyV1(name='Name', value=self['Name'])]
            if 'Description' in self:
                props.append(ScalarPropertyV1(name='Description', value=self['Description']))

            # If the folder happens to be archived, un-archive it. If you're pushing a new copy it seems likely
            # you're intending to revive it.
            props.append(ScalarPropertyV1(name='Archived', value=False))

            check_for_reserved_folder_name(self['Name'])
            safely(lambda: items_api.set_properties(id=folder_output.id, body=props),
                   action_description=f'set common properties (Name, Description, Archived) for existing Folder'
                                      f' {folder_output.id}',
                   status=status, dry_run=context.dry_run)

            owner_id = self.decide_owner(context, item_map, owner=owner,
                                         current_owner_id=folder_output.owner.id)

            self._push_owner_and_location(session, folder_output, owner_id, parent_folder_id, status,
                                          dry_run=context.dry_run)

        if folder_output is not None:
            item_map[self.id] = folder_output.id

            if context.current_params.access_control:
                self._push_acl(context, folder_output.id, item_map)

        return folder_output


def check_for_reserved_folder_name(folder_name: str):
    if folder_name in SYNTHETIC_FOLDERS:
        raise SPyValueError(f'Folder name "{folder_name}" is reserved and cannot be used for a real folder. '
                            f'Please choose a different name.')


def create_user_folder_if_necessary(context: WorkbookPushContext, user_id: str) -> Optional[FolderOutputV1]:
    user_folder = context.session.get_user_folder(user_id)
    if user_folder is not None:
        return user_folder

    if context.dry_run:
        context.status.log(f'[Dry Run] User folder does not exist for {user_id}, would create it')
        return None

    temp_folder_name = f'__temp_folder_for_home_creation__'
    context.status.log(f'User folder does not exist for {user_id}, creating it')
    dummy_folder_input = FolderInputV1()
    dummy_folder_input.name = temp_folder_name
    dummy_folder_input.owner_id = user_id
    dummy_folder_input.parent_folder_id = None

    items_api = ItemsApi(context.session.client)
    folders_api = FoldersApi(context.session.client)
    dummy_folder = safely(lambda: folders_api.create_folder(body=dummy_folder_input),
                          action_description=f'create temporary folder for home folder creation',
                          status=context.status)

    if dummy_folder is not None:
        try:
            safely(lambda: items_api.archive_item(id=dummy_folder.id, delete=False),
                   action_description=f'archive temporary folder {dummy_folder.id}',
                   status=context.status)
        finally:
            safely(lambda: items_api.archive_item(id=dummy_folder.id, delete=True),
                   action_description=f'delete temporary folder {dummy_folder.id}',
                   status=context.status)

    context.session.clear_user_folder_cache()
    return context.session.get_user_folder(user_id)
