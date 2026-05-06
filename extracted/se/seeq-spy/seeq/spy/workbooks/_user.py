from __future__ import annotations

import logging
from functools import lru_cache
from typing import List, Optional, Dict, Union

import pandas as pd

from seeq.sdk import *
from seeq.spy import _common, _metadata, _compatibility
from seeq.spy._errors import *
from seeq.spy._redaction import request_safely, safely
from seeq.spy._session import Session
from seeq.spy._status import Status
from seeq.spy.workbooks._context import WorkbookPushContext
from seeq.spy.workbooks._data import StoredItem
from seeq.spy.workbooks._item import Item, ItemMap

ORIGINAL_OWNER = '__original__'
FORCE_ME_AS_OWNER = '__me__'


class ItemWithOwnerAndAcl(Item):
    def decide_owner(self, context: WorkbookPushContext, item_map: ItemMap, *, owner=None, current_owner_id=None):
        session = context.session
        requires_admin = True
        if _common.is_guid(owner):
            owner_id = owner
        elif owner is None:
            requires_admin = False
            if current_owner_id is None:
                owner_id = session.user.id
            else:
                owner_id = current_owner_id
        elif owner == ORIGINAL_OWNER:
            if _common.get(self, 'Owner'):
                try:
                    owner_id = Identity.find_identity(context, self['Owner'], item_map=item_map)
                except SPyDependencyNotFound as e:
                    context.status.log(str(e))

                    # If we can't map the original owner to an identity on the target server, we have to abort the
                    # push and tell the user not to supply spy.workbooks.ORIGINAL_OWNER.
                    raise SPyRuntimeError(
                        f'Original owner "{self["Owner"]["Username"]}" [{self["Owner"].get("Email", "Unknown Email")}] '
                        'does not exist on the target server and was not mapped via Datasource Maps. '
                        'Cannot push with owner=spy.workbooks.ORIGINAL_OWNER'
                    )
            else:
                # There is no original owner so make it the current user as a placeholder
                owner_id = session.user.id
        elif owner == FORCE_ME_AS_OWNER:
            owner_id = session.user.id
        else:
            matches = Identity.search(context.session, {'Type': 'User', 'Username': owner})
            if len(matches) == 0:
                raise SPyRuntimeError(
                    f'Could not find owner username "{owner}"')
            elif len(matches) > 1:
                raise SPyRuntimeError(
                    f'Multiple matches found for owner username "{owner}":\n' +
                    '\n'.join([f'ID {match.id}: {match.name} [{match.datasource.name}]' for match in matches]) +
                    "\nSpecify the user's ID directly to disambiguate.")
            else:
                owner_id = matches[0].id

        if current_owner_id is None or current_owner_id == owner_id:
            requires_admin = False

        if requires_admin and not session.user.is_admin:
            raise SPyRuntimeError("Logged in user must be an admin as a result of owner='%s'" % owner)

        return owner_id

    def _pull_owner_and_acl(self, session: Session, owner: IdentityPreviewV1, status: Status):
        items_api = ItemsApi(session.client)

        if owner is not None:
            self['Owner'] = {'ID': owner.id}
            self['Owner']['Redacted'] = owner.is_redacted
            if not owner.is_redacted:
                owner_details = User.pull(owner.id, session=session, status=status)
                if owner_details is not None:
                    self['Owner'] = owner_details.definition

        @request_safely(action_description=f'get access control list for Item {self["ID"]}', status=status)
        def _request_acl(_id):
            acl_output = items_api.get_access_control(id=_id)  # type: AclOutputV1
            access_control = list()

            for ace_output in acl_output.entries:  # type: AceOutputV1
                ace_dict = Item.dict_via_attribute_map(ace_output, {
                    'created_at': 'Created At',
                    'id': 'ID',
                    'role': 'Role'
                })

                ace_dict['Origin'] = ace_output.origin.id if ace_output.origin is not None else None
                ace_dict['Permissions'] = ItemWithOwnerAndAcl._permissions_to_dict(ace_output.permissions)
                ace_dict['Redacted'] = ace_output.identity.is_redacted

                if not ace_output.identity.is_redacted:
                    if ace_output.identity.type == 'User':
                        identity = User.pull(ace_output.identity.id, session=session, status=status)
                    else:
                        identity = UserGroup.pull(ace_output.identity.id, session=session, status=status)

                    if identity is not None:
                        ace_dict['Identity'] = identity.definition
                access_control.append(ace_dict)
            return access_control

        maybe_acl = _request_acl(self['ID'])
        self.definition['Access Control'] = list() if maybe_acl is None else maybe_acl

    def _push_owner_and_location(self, session: Session, item_output, owner_id, folder_id, status: Status, *,
                                 dry_run: bool = False):
        items_api = ItemsApi(session.client)
        folders_api = FoldersApi(session.client)

        if item_output.owner.id != owner_id:
            if not dry_run:
                Status.log_if(status, f'Changing owner of {item_output.id} to {owner_id}')
                safely(lambda: items_api.change_owner(item_id=item_output.id, new_owner_id=owner_id),
                       action_description=f'change owner of {item_output.id} to {owner_id}',
                       status=status)
            else:
                Status.log_if(status, f'[Dry Run] Would change owner of {item_output.id} to {owner_id}')

        if folder_id is not None and getattr(item_output, 'parent_folder_id') != folder_id:
            if not dry_run:
                Status.log_if(status,
                              f'Moving {self.type} "{item_output.name}" ({item_output.id}) to folder {folder_id}')
                safely(lambda: folders_api.move_item_to_folder(folder_id=folder_id, item_id=item_output.id),
                       action_description=f'change Folder of {item_output.id} to {folder_id}',
                       status=status)
            else:
                Status.log_if(
                    status,
                    f'[Dry Run] Would move  {self.type} "{item_output.name}" ({item_output.id}) to folder {folder_id}')

    def _push_acl(self, context: WorkbookPushContext, pushed_id, item_map: ItemMap):
        session = context.session
        status = context.status
        replace, strict = ItemWithOwnerAndAcl.parse_access_control_str(context.current_params.access_control)

        if 'Access Control' not in self:
            status.log(f'No Access Control to push for item {pushed_id}')
            return

        acl_df = pd.DataFrame({
            'ID': pd.Series(dtype=str),
            'Read': pd.Series(dtype=bool),
            'Write': pd.Series(dtype=bool),
            'Manage': pd.Series(dtype=bool)
        })

        for acl_to_push in self['Access Control']:
            try:
                identity_id = Identity.find_identity(context, acl_to_push['Identity'], item_map)
            except SPyDependencyNotFound as e:
                status.log(str(e), level=logging.ERROR if strict else logging.WARN)
                if strict:
                    raise

                status.log(f'Skipping ACL entry for missing identity {acl_to_push["Identity"]} '
                           f"on item {pushed_id} because access_control='strict' not specified")
                continue

            acl_df = pd.concat([acl_df, pd.DataFrame([{
                'ID': identity_id,
                'Read': acl_to_push['Permissions']['Read'],
                'Write': acl_to_push['Permissions']['Write'],
                'Manage': acl_to_push['Permissions']['Manage']
            }])], ignore_index=True)

        _metadata.push_access_control(session, pushed_id, acl_df, replace, status=status, dry_run=context.dry_run)

    @staticmethod
    def parse_access_control_str(access_control):
        replace = False
        strict = False
        if access_control:
            treatment_parts = access_control.split(',')
            for treatment_part in treatment_parts:
                if treatment_part == 'add':
                    replace = False
                elif treatment_part == 'replace':
                    replace = True
                elif treatment_part == 'loose':
                    strict = False
                elif treatment_part == 'strict':
                    strict = True
                else:
                    raise SPyValueError("access_control argument must be 'add' or 'replace' comma 'loose' or "
                                        "'strict'. For example: replace,strict")
        return replace, strict

    @staticmethod
    def _dict_to_permissions(d):
        return PermissionsV1(
            manage=_common.get(d, 'Manage', False),
            read=_common.get(d, 'Read', False),
            write=_common.get(d, 'Write', False)
        )

    @staticmethod
    def _permissions_to_dict(permissions):
        """
        :type permissions: PermissionsV1
        """
        return {
            'Read': permissions.read,
            'Write': permissions.write,
            'Manage': permissions.manage
        }

    def _pull_ancestors(self, session: Session, ancestors: List[ItemPreviewV1]):
        if ancestors is None:
            return

        self.definition['Ancestors'] = \
            [(ancestor.id if ancestor.id is not None else f'__{ancestor.name}__')
             for ancestor in ancestors]

    @staticmethod
    def should_use_full_ancestry(session: Session):
        # We generally want the true ancestors if at all possible, because this helps us transfer workbooks/folders
        # accurately between servers.
        return session.user.is_admin and not session.options.wants_compatibility_with(189)

    @staticmethod
    def _find_auth_provider(session: Session, datasource_class, datasource_id) -> Optional[DatasourceOutputV1]:
        for auth_provider in session.auth_providers:
            if auth_provider.datasource_class == datasource_class and auth_provider.datasource_id == datasource_id:
                return auth_provider

        return None

    def _scrape_auth_datasources(self, session: Session) -> Dict[str, DatasourceOutputV1]:
        referenced_datasources: Dict[str, DatasourceOutputV1] = dict()

        def _scrape_auth_datasource(d, key):
            if key in d and 'Datasource Class' in d[key] and 'Datasource ID' in d[key]:
                auth_provider = ItemWithOwnerAndAcl._find_auth_provider(
                    session, d[key]['Datasource Class'], d[key]['Datasource ID'])
                if auth_provider:
                    referenced_datasources[auth_provider.id] = auth_provider

        _scrape_auth_datasource(self, 'Owner')
        if 'Access Control' in self:
            for acl in self['Access Control']:
                _scrape_auth_datasource(acl, 'Identity')

        return referenced_datasources


class Identity(StoredItem):
    @staticmethod
    def find_identity(context: WorkbookPushContext, identity_dict, item_map: ItemMap) -> str:
        if _common.get(identity_dict, 'ID') in item_map:
            return item_map[identity_dict['ID']]

        if _common.get(identity_dict, 'Type') == 'User':
            identity = User(identity_dict)
        else:
            identity = UserGroup(identity_dict)

        pushed_identity = identity._lookup(context, datasource_output=None, item_map=item_map)

        return pushed_identity.id

    @staticmethod
    def search(session: Session, acl_row: Union[dict, pd.Series]):
        matches = list()
        query = _common.get(acl_row, 'Username') if _common.present(acl_row, 'Username') else \
            _common.get(acl_row, 'Name')

        users_api = UsersApi(session.client)
        identities = users_api.autocomplete_users_and_groups(query=query, limit=100000)

        for identity in identities.items:  # type: IdentityPreviewV1
            if (_common.present(acl_row, 'Name') and
                    Identity._insensitive_not_equal(identity.name, _common.get(acl_row, 'Name'))):
                continue

            if (_common.present(acl_row, 'Username') and
                    Identity._insensitive_not_equal(identity.username, _common.get(acl_row, 'Username'))):
                continue

            if (_common.present(acl_row, 'Type') and
                    Identity._insensitive_not_equal(identity.type, _common.get(acl_row, 'Type'))):
                continue

            if (_common.present(acl_row, 'Directory') and
                    Identity._insensitive_not_equal(identity.datasource.name, _common.get(acl_row, 'Directory'))):
                continue

            matches.append(identity)

        return matches

    @staticmethod
    def _insensitive_not_equal(a: Optional[str], b: Optional[str]):
        if a is None and b is None:
            return False
        elif a is not None and b is None:
            return True
        elif a is None and b is not None:
            return True
        else:
            return a.lower() != b.lower()

    def pull_datasource(self, session: Session, identity: Union[UserOutputV1, UserGroupOutputV1, IdentityPreviewV1]):
        if isinstance(identity, IdentityPreviewV1):
            datasource_preview: DatasourcePreviewV1 = identity.datasource
            self['Datasource Class'] = datasource_preview.datasource_class
            self['Datasource ID'] = datasource_preview.datasource_id
            self['Datasource Name'] = datasource_preview.name
        else:
            datasource_name = identity.datasource_name

            # noinspection PyBroadException
            try:
                for auth_provider in session.auth_providers:  # type: DatasourceOutputV1
                    if auth_provider.name == datasource_name:
                        self['Datasource Class'] = auth_provider.datasource_class
                        self['Datasource ID'] = auth_provider.datasource_id
                        self['Datasource Name'] = auth_provider.name
                        break

            except Exception:
                # If we can't get extra data on the user, that's OK
                pass

    @staticmethod
    @lru_cache()
    def pull(item_id, *, allowed_types=None, status: Status = None, session: Optional[Session] = None):
        try:
            user = User.pull(item_id, allowed_types=allowed_types, status=status, session=session)
            if user is not None:
                return user
        except ApiException as e:
            if e.status not in (400, 404):
                raise

        try:
            user_group = UserGroup.pull(item_id, allowed_types=allowed_types, status=status, session=session)
            if user_group is not None:
                return user_group
        except ApiException as e:
            if e.status not in (400, 404):
                raise

        return None


class User(Identity):
    @staticmethod
    @lru_cache()
    def pull(item_id, *, allowed_types=None, status: Status = None, session: Optional[Session] = None):
        session = Session.validate(session)

        user_output = safely(lambda: _compatibility.get_user(session.client, user_id=item_id, include_groups=False),
                             action_description=f'get User {item_id}',
                             status=status)  # type: UserOutputV1
        if user_output is None:
            return None

        user_dict = {
            'ID': user_output.id,
            'Type': user_output.type,
            'Datasource Name': user_output.datasource_name,
            'Name': user_output.name,
            'Username': user_output.username,
            'First Name': user_output.first_name,
            'Last Name': user_output.last_name,
            'Email': user_output.email,
            'Is Admin': user_output.is_admin
        }

        if user_output.datasource_name in session.directories:
            datasource_output = session.directories[user_output.datasource_name]
            user_dict.update({
                'Datasource Class': datasource_output.datasource_class,
                'Datasource ID': datasource_output.datasource_id
            })

        item = User(user_dict)

        item.pull_datasource(session, user_output)
        return item


class UserGroup(Identity):
    @staticmethod
    @lru_cache()
    def pull(item_id, *, allowed_types=None, status: Status = None, session: Optional[Session] = None):
        session = Session.validate(session)
        usergroup_output = safely(
            lambda: _compatibility.get_user_group(session.client, user_group_id=item_id, include_members=False),
            action_description=f'get User Group {item_id}',
            status=status)  # type: UserGroupOutputV1
        if usergroup_output is None:
            return None

        item = UserGroup({
            'ID': usergroup_output.id,
            'Type': usergroup_output.type,
            'Name': usergroup_output.name
        })

        item.pull_datasource(session, usergroup_output)
        return item

    @staticmethod
    def from_identity(identity: IdentityPreviewV1, *, session: Optional[Session] = None):
        session = Session.validate(session)

        item = UserGroup({
            'ID': identity.id,
            'Type': identity.type,
            'Name': identity.name
        })

        item.pull_datasource(session, identity)
        return item
