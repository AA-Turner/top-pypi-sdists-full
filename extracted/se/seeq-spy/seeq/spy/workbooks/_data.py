from __future__ import annotations

import copy
import json
import logging
import os
import re
import textwrap
from typing import Union, Optional, Tuple

import pandas as pd

from seeq.base import util
from seeq.sdk import *
from seeq.spy import _common, _metadata
from seeq.spy._errors import *
from seeq.spy._redaction import safely
from seeq.spy._session import Session
from seeq.spy._status import Status
from seeq.spy.workbooks._context import WorkbookPushContext, WorkbookPushMode, DatasourceMapList
from seeq.spy.workbooks._item import Item, ItemMap, ItemExists

SEARCHABLE_ITEM_PROPS = ['Datasource Class', 'Datasource ID', 'Datasource Name', 'Data ID',
                         'Type', 'Name', 'Description', 'Path', 'Asset']

SEARCHABLE_USER_PROPS = ['ID', 'Type', 'Datasource Name', 'Datasource ID', 'Datasource Class', 'Name', 'First Name',
                         'Last Name', 'Email', 'Username']

SEARCHABLE_GROUP_PROPS = ['ID', 'Type', 'Datasource Name', 'Datasource ID', 'Datasource Class', 'Name']


class StoredOrCalculatedItem(Item):
    def __init__(self, definition=None, *, provenance=None):
        super().__init__(definition, provenance=provenance)

    def _populate_asset_and_path(self, session: Session, item_id, status, item_search_preview: ItemSearchPreviewV1):
        if item_search_preview is None:
            trees_api = TreesApi(session.client)
            asset_tree_output = safely(
                lambda: trees_api.get_tree(id=item_id),
                action_description=f'get Tree information for {item_id}',
                status=status)  # type: AssetTreeOutputV1
            if asset_tree_output is None or asset_tree_output.item is None:
                return

            ancestors = [a.name for a in asset_tree_output.item.ancestors]
            if len(asset_tree_output.item.ancestors) > 0:
                self.definition['Parent ID'] = asset_tree_output.item.ancestors[-1].id
        else:
            ancestors = [a.name for a in item_search_preview.ancestors]
            if len(item_search_preview.ancestors) > 0:
                self.definition['Parent ID'] = item_search_preview.ancestors[-1].id

        _common.add_ancestors_to_definition(self.type, self.name, ancestors, self.definition, old_asset_format=False)

    def _pull(self, session: Session, item_id, status: Status, item_search_preview: ItemSearchPreviewV1):
        super()._pull(session, item_id, status, item_search_preview)

        if 'Path' not in self.definition:
            self._populate_asset_and_path(session, item_id, status, item_search_preview)

    def get_metadata_to_push(self, context: WorkbookPushContext, datasource_maps, datasource_output,
                             item_inventory: dict, *, pushed_workbook_id=None, item_map: ItemMap = None, label=None,
                             item_exists: ItemExists = ItemExists.MAYBE,
                             item_search_preview: ItemSearchPreviewV1 = None):
        raise SPyRuntimeError('get_metadata_to_push() called but StoredOrCalculatedItem.get_metadata_to_push() not '
                              'overloaded')

    def _attach_to_parent(self, session: Session, item_map: ItemMap, item_id: str):
        if self['Scoped To'] is None:
            # Do not move around global items
            return

        if 'Parent ID' not in self.definition:
            return

        parent_id = self.definition['Parent ID']
        if parent_id != Item.ROOT and self.definition['Parent ID'] not in item_map:
            return

        trees_api = TreesApi(session.client)
        if parent_id == Item.ROOT:
            trees_api.move_nodes_to_root_of_tree(body=ItemIdListInputV1(items=[item_id]))
        else:
            trees_api.move_nodes_to_parent(parent_id=item_map[self.definition['Parent ID']],
                                           body=ItemIdListInputV1(items=[item_id]))

    @staticmethod
    def _find_datasource_name(datasource_class, datasource_id, datasource_maps):
        for datasource_map in datasource_maps:
            if datasource_map['Datasource Class'] == datasource_class and \
                    datasource_map['Datasource ID'] == datasource_id:
                return datasource_map['Datasource Name']

        raise SPyRuntimeError('Could not find Datasource Class "%s" and Datasource ID "%s" in datasource maps' %
                              (datasource_class, datasource_id))

    @staticmethod
    def _get_datasource_map_name_log_str(datasource_map):
        override_str = 'override ' if datasource_map.get('Override', False) else 'non-override '
        provenance_str = f'"{os.path.basename(datasource_map["File"])}"' if 'File' in datasource_map else 'default map'
        return override_str + provenance_str

    def _execute_regex_map(self, old_definition, regex_map, regex_map_index, item_map: ItemMap, *,
                           allow_missing_properties=False):
        for prop in ['Old', 'New']:
            if prop not in regex_map:
                raise SPyValueError(f'RegEx-Based Map {regex_map_index} must have "{prop}" property')

        capture_groups = dict()
        for prop, regex in regex_map['Old'].items():
            if prop not in old_definition:
                if allow_missing_properties:
                    continue
                else:
                    item_map.log(self.id, f'- RegEx-Based Map {regex_map_index}: Unsuccessful match. Details:')
                    item_map.log(self.id, f'    "{prop}" not defined for this item')
                    return None, None

            pythonized_regex = util.pythonize_regex_capture_group_names(regex)

            try:
                match = re.fullmatch(pythonized_regex, old_definition[prop])
            except re.error as e:
                raise SPyValueError(
                    f'Invalid regular expression "{regex}" for property "{prop}" in RegEx-Based Map '
                    f'{regex_map_index}: {e}')

            if not match:
                item_map.log(self.id, f'- RegEx-Based Map {regex_map_index}: Unsuccessful match. Details:')
                item_map.log(self.id, f'    "{prop}"')
                item_map.log(self.id, f'        regex          "{regex}"')
                item_map.log(self.id, f'        does not match "{old_definition[prop]}"')
                return None, None

            capture_groups.update(match.groupdict())

        new_definition = dict()
        for prop, regex in regex_map['New'].items():
            new_definition[prop] = util.replace_tokens_in_regex(regex, capture_groups, escape=False)

        return new_definition, capture_groups

    def _lookup_item_via_datasource_map(
            self, context: WorkbookPushContext, pushed_workbook_id: str,
            item_map: ItemMap, *, only_override_maps: bool = False, force_direct_lookup: bool = False,
            item_exists: ItemExists = ItemExists.MAYBE,
            item_search_preview: Optional[ItemSearchPreviewV1] = None) -> Optional[Item]:
        item: Optional[Item] = None

        item_map.clear_logs(self.id)

        # First, we process the "overrides". These are the cases where, even if the item with the ID exists in the
        # destination, we still want to map to something else. Useful for swapping datasources on the same server.
        override = self._lookup_relevant_datasource_map(context.datasource_maps, override=True)
        if override is not None:
            if "File" in override:
                item_map.log(self.id, f'Using overrides from {os.path.dirname(override["File"])}:')
            item = self._lookup_in_datasource_map(context, pushed_workbook_id, override, item_map)
        else:
            item_map.log(self.id, f'No datasource map overrides found')

        if item is not None:
            item_map.log(self.id, f'Successful mapping:')
            item_map.log(self.id, f'  Old: {self}')
            item_map.log(self.id, f'  New: {item}')
            return item

        if only_override_maps:
            item_map.log(self.id, f'{self} not mapped, only override maps used', at_top=True)
            if not force_direct_lookup:
                return None

        # If an override map was found, we don't want to continue to direct lookup and non-overrides because the user
        # did not necessarily intend us to, and it's confusing to have things potentially still map correctly despite
        # supplying an override.
        if override is not None and not force_direct_lookup:
            item_map.log(self.id,
                         f'{self} not successfully mapped via override (skipped direct ID lookup and non-overrides)',
                         at_top=True)
            return None

        # Second, we just try to look the item up by its ID. This case will occur when the user pulls a workbook,
        # makes a change, and pushes it back.
        if item_exists != ItemExists.NO:
            try:
                item = Item.pull(self.id, session=context.session, item_search_preview=item_search_preview)
            except ApiException:
                item_map.log(self.id, f"Item's ID {self.id} not found directly in target server")
        else:
            item_map.log(self.id, f"Item's ID {self.id} not found directly in target server")

        if item is not None:
            item_map.log(self.id, f"Item's ID {self.id} found directly in target server")
            Status.log_if(context, f'Successfully mapped {self} -> {item} via direct ID lookup')
            return item

        if only_override_maps or override is not None:
            return None

        # Finally, we try to use the non-override maps to find the item. This case will occur mostly when
        # transferring workbooks between servers.
        non_override = self._lookup_relevant_datasource_map(context.datasource_maps, override=False)
        if non_override is not None:
            if "File" in non_override:
                item_map.log(self.id, f'Using non-overrides from {os.path.dirname(non_override["File"])}:')
            item = self._lookup_in_datasource_map(context, pushed_workbook_id, non_override, item_map)
        else:
            item_map.log(self.id, f'No (non-override) datasource maps found')

        if item is None:
            item_map.log(self.id, f'{self} not successfully mapped', at_top=True)
            return None

        item_map.log(self.id, f'Successful mapping:')
        item_map.log(self.id, f'  Old: {self}')
        item_map.log(self.id, f'  New: {item}')

        return item

    def _lookup_relevant_datasource_map(self, datasource_maps: DatasourceMapList,
                                        *, override: bool = False) -> Optional[dict]:
        for datasource_map in datasource_maps:
            if (_common.get(self, 'Datasource Class') == datasource_map['Datasource Class']
                    and _common.get(self, 'Datasource ID') == datasource_map['Datasource ID']
                    and _common.get(datasource_map, 'Override', default=False) == override):
                return datasource_map

        return None

    def _lookup_in_datasource_map(self, context: WorkbookPushContext, pushed_workbook_id: str, datasource_map: dict,
                                  item_map: ItemMap) -> Optional[Item]:
        item: Optional[Item] = None

        try:
            if "File" in datasource_map:
                item_map.log(self.id, f'- Used "{datasource_map["File"]}"')
            else:
                item_map.log(self.id,
                             f'- Used datasource map for Datasource Class "{datasource_map["Datasource Class"]}" '
                             f'and Datasource ID "{datasource_map["Datasource ID"]}"')

            if _common.DATASOURCE_MAP_ITEM_LEVEL_MAP_FILES in datasource_map:
                item = self._lookup_in_item_level_map_files(context, datasource_map, item_map)

            if item is None:
                if _common.DATASOURCE_MAP_REGEX_BASED_MAPS in datasource_map:
                    item = self._lookup_in_regex_based_maps(context, datasource_map, item_map, pushed_workbook_id)

                    if item is not None:
                        context.append_to_server_scoped_item_level_map_file(datasource_map, self, item)

        except SPyException as e:
            raise SPyRuntimeError(
                f'Error processing datasource map "{datasource_map["File"]}" (see inner exception)') from e

        return item

    def _lookup_in_item_level_map_files(self, context: WorkbookPushContext, datasource_map,
                                        item_map: ItemMap) -> Optional[Item]:
        session = context.session
        item: Optional[ItemOutputV1] = None
        item_level_map_files = datasource_map[_common.DATASOURCE_MAP_ITEM_LEVEL_MAP_FILES]
        if not isinstance(item_level_map_files, list):
            item_level_map_files = [item_level_map_files]

        if 'DataFrames' not in datasource_map:
            datasource_map['DataFrames'] = dict()

        df_map = datasource_map['DataFrames']

        for item_level_map_file in item_level_map_files:
            if item_level_map_file not in df_map:
                if not util.safe_exists(item_level_map_file):
                    raise SPyValueError('Item-Level Map File "%s" does not exist' % item_level_map_file)

                df_map[item_level_map_file] = pd.read_csv(item_level_map_file)

            df = df_map[item_level_map_file]

            if 'Old ID' not in df.columns or 'New ID' not in df.columns:
                raise SPyValueError('Item-Level Map File must have "Old ID" and "New ID" columns')

            mapped_row = df[df['Old ID'] == self.id]

            if len(mapped_row) > 1:
                raise SPyValueError('Ambiguous map: %d rows in "%s" match "Old ID" == "%s"\n%s' % (
                    len(mapped_row), item_level_map_file, self.id, mapped_row))

            if len(mapped_row) == 0:
                item_map.log(
                    self.id,
                    f'- Item-Level Map File "{item_level_map_file}" did not match for "Old ID" value "{self.id}"')
                continue

            new_id = mapped_row.iloc[0]['New ID']

            if self.type == 'User':
                from seeq.spy.workbooks._user import User
                item = User.pull(new_id, session=session)
            elif self.type == 'UserGroup':
                from seeq.spy.workbooks._user import UserGroup
                item = UserGroup.pull(new_id, session=session)
            else:
                item = Item.pull(new_id, session=session)

            if 'Server_Scoped_Item_Level_Datasource_Map_' in datasource_map.get('File', ''):
                Status.log_if(context, f'Successfully mapped {self} -> {item} via Server-Scoped Item-Level Map '
                                       f'File "{item_level_map_file}"')
            else:
                Status.log_if(context, f'Successfully mapped {self} -> {item} via Item-Level Map File '
                                       f'"{item_level_map_file}" specified in '
                                       f'{self._get_datasource_map_name_log_str(datasource_map)}')
            break

        return item

    def _lookup_in_regex_based_maps(
            self, context: WorkbookPushContext, datasource_map, item_map: ItemMap,
            pushed_workbook_id) -> Optional[Item]:
        session = context.session
        for i in range(len(datasource_map['RegEx-Based Maps'])):
            regex_map_index = i
            regex_map = datasource_map['RegEx-Based Maps'][regex_map_index]
            item_object, old_criteria_matched = self._lookup_in_regex_based_map(
                context, regex_map_index, regex_map, item_map, pushed_workbook_id)

            if item_object is not None:
                Status.log_if(context, f'Successfully mapped {self} -> {item_object} via Regex-based Map '
                                       f'{regex_map_index} specified in '
                                       f'{self._get_datasource_map_name_log_str(datasource_map)}')
                return item_object

            on_match_default = 'Stop' if session.options.wants_compatibility_with(191) else 'Continue'
            on_match = str(_common.get(regex_map, 'On Match', on_match_default)).lower()
            if not isinstance(on_match, str) and on_match not in ['continue', 'stop']:
                raise SPyValueError('RegEx-Based Map "On Match" parameter must be either "Continue" or "Stop"')

            if old_criteria_matched and on_match == 'stop':
                item_map.log(self.id,
                             f'- "On Match" parameter is "Stop", so no further RegEx-Based Maps will be used')
                break

        return None

    def _lookup_in_regex_based_map(
            self, context: WorkbookPushContext, regex_map_index, regex_map, item_map: ItemMap,
            pushed_workbook_id) -> Tuple[Optional[Item], bool]:
        session = context.session
        items_api = ItemsApi(session.client)
        old_definition = self.definition_dict
        new_definition = None
        item: Optional[Item] = None
        capture_groups = None

        if 'Type' not in old_definition:
            raise SPyValueError('"Type" property required in "Old" datasource map definitions')

        if 'Datasource Class' in old_definition and 'Datasource ID' in old_definition:
            old_definition['Datasource Name'] = \
                StoredOrCalculatedItem._find_datasource_name(old_definition['Datasource Class'],
                                                             old_definition['Datasource ID'],
                                                             context.datasource_maps)

        new_definition, capture_groups = self._execute_regex_map(
            old_definition, regex_map, regex_map_index, item_map,
            allow_missing_properties=self.type.endswith('Datasource'))

        if new_definition is None:
            return None, False

        if 'Type' not in new_definition:
            raise SPyValueError('"Type" property required in "New" datasource map definitions')

        new_type = _common.get(new_definition, 'Type', '?')
        # Simplify the types so that the search will find stored or calculated signals/conditions etc. This
        # helps when mapping, for example, an AF tree to a Data Lab tree.
        for t in ['Signal', 'Condition', 'Scalar', 'Datasource']:
            if t in new_type:
                new_definition['Type'] = t

        def _log_criteria(_and_found=None):
            for key, value in new_definition.items():
                item_map.log(self.id, f'    "{key}"')
                if key in regex_map['Old']:
                    item_map.log(self.id, f'        regex          "{regex_map["Old"][key]}"')
                    item_map.log(self.id, f'        matched on     "{self[key]}"')
                item_map.log(self.id, f'        searched for   "{value}"')
                if _and_found is not None:
                    item_map.log(self.id, f'        and found      "{_and_found[key]}"')
            if capture_groups is not None and len(capture_groups) > 0:
                item_map.log(self.id, f'    Capture groups:')
                for n, v in capture_groups.items():
                    item_map.log(self.id, f'        {n:14} "{v}"')

        if new_type not in ['User', 'UserGroup']:
            for prop in new_definition.keys():
                if prop not in SEARCHABLE_ITEM_PROPS:
                    searchable_props_string = '\n'.join(SEARCHABLE_ITEM_PROPS)
                    raise SPyRuntimeError(
                        f'Datasource Map contains an unsearchable property "{prop}".'
                        f'Searchable properties:\n{searchable_props_string}')

            if 'Datasource Name' in new_definition:
                if 'Datasource ID' not in new_definition:
                    if 'Datasource Class' not in new_definition:
                        raise SPyValueError('"Datasource Class" required with "Datasource Name" in map:\n%s' %
                                            json.dumps(new_definition))

                    key = (new_definition['Datasource Class'], new_definition['Datasource Name'])
                    if key in context.datasource_id_cache:
                        new_definition['Datasource ID'] = context.datasource_id_cache[key]
                    else:
                        datasource_results = items_api.search_items(
                            # Note here that 'Name' supports RegEx but 'Datasource Class' doesn't. Users have to be careful in
                            # the Datasource Maps not to supply a RegEx. See Workbook._construct_default_datasource_maps().
                            filters=['Datasource Class==%s&&Name==/%s/' % (new_definition['Datasource Class'],
                                                                           new_definition['Datasource Name']),
                                     '@includeUnsearchable'],
                            types=['Datasource'],
                            limit=2)  # type: ItemSearchPreviewPaginatedListV1

                        items = datasource_results.items
                        if len(items) > 1:
                            # Try filtering out any archived items first
                            items = [i for i in items if not i.is_archived]

                        if len(items) > 1:
                            multiple_items_str = "\n".join([i.id for i in items])
                            raise SPyRuntimeError(
                                f'Multiple datasources found that match "{new_definition["Datasource Name"]}":\n'
                                f'{multiple_items_str}'
                            )
                        elif len(items) == 0:
                            item_map.log(self.id,
                                         f'No datasource found that matches "{new_definition["Datasource Name"]}"')
                            return None, True

                        new_datasource = items[0]  # type: ItemSearchPreviewV1
                        try:
                            new_definition['Datasource ID'] = items_api.get_property(
                                id=new_datasource.id, property_name='Datasource ID').value
                        except ApiException:
                            raise SPyRuntimeError(f'Could not get Datasource ID for '
                                                  f'"{new_definition["Datasource Name"]}" {new_datasource.id}')

                        context.datasource_id_cache[key] = new_definition['Datasource ID']

                item_map.log(self.id,
                             f'- {new_definition["Datasource Name"]} datasource '
                             f'"{new_definition["Datasource Name"]}" mapped to Datasource ID '
                             f'{new_definition["Datasource ID"]}')
                del new_definition['Datasource Name']

            query_df = pd.DataFrame([new_definition])
            from seeq.spy import _search
            if 'Path' in new_definition:
                # If we're matching based on path, unfortunately we will not be able to match against archived items
                # due to a limitation of the API. See CRAB-18439.
                search_df = _search.search(query_df, workbook=pushed_workbook_id, recursive=False,
                                           ignore_unindexed_properties=False, session=session, quiet=True)
            else:
                search_df = _search.search(query_df, workbook=pushed_workbook_id, include_archived=True,
                                           ignore_unindexed_properties=False, session=session, quiet=True)

            # If several things are returned, but some of them are archived, then filter out the archived ones.
            # Tested by spy.workbooks.tests.test_push.test_datasource_map_by_name()
            if len(search_df) > 1 and 'Archived' in search_df.columns:
                search_df = search_df[~search_df['Archived']]

            if len(search_df) == 0:
                item_map.log(self.id, f'- RegEx-Based Map {regex_map_index}: Item not found on server. Details:')
                _log_criteria()
            elif len(search_df) > 1:
                item_map.log(self.id,
                             f'- RegEx-Based Map {regex_map_index}: Multiple possibilities for item found. Details:')
                _log_criteria()
                item_map.log(self.id, f'  Matching items:')
                item_map.log(self.id, textwrap.indent(f'{str(search_df[["ID", "Name"]])}', '    '))
            else:
                item = Item.pull(search_df.iloc[0]['ID'], session=session)
        else:
            if new_type == 'User':
                context.fetch_all_users()
                relevant_list = context.all_users
                relevant_props = SEARCHABLE_USER_PROPS
            else:
                context.fetch_all_groups()
                relevant_list = context.all_groups
                relevant_props = SEARCHABLE_GROUP_PROPS

            matching_identities = list()
            for identity in relevant_list:
                match = True

                for prop in new_definition.keys():
                    if prop not in relevant_props:
                        searchable_props_string = '\n'.join(relevant_props)
                        raise SPyRuntimeError(
                            f'Datasource Map contains an unsearchable property "{prop}" for {new_type}.'
                            f'Searchable properties:\n{searchable_props_string}')

                    attribute_name = prop.lower().replace(' ', '_')
                    attribute_value = getattr(identity, attribute_name, None)
                    if attribute_name == 'datasource_name':
                        attribute_value = identity.datasource.name
                    elif attribute_name == 'datasource_class':
                        attribute_value = identity.datasource.datasource_class
                    elif attribute_name == 'datasource_id':
                        attribute_value = identity.datasource.datasource_id

                    if attribute_value is None or new_definition.get(prop) is None:
                        match = False
                        break

                    # Doing a case-insensitive match here is different than we do for stored/calculated items, but
                    # it helps reduce variations between servers, especially for emails. There is a chance of two (
                    # cryptic) OAuth 2.0 usernames only differing by case but it's vanishingly small.
                    if attribute_value.lower() != new_definition[prop].lower():
                        match = False
                        break

                if match:
                    matching_identities.append(identity)

            matched_identity = None
            if len(matching_identities) == 0:
                item_map.log(self.id, f'- RegEx-Based Map {regex_map_index}: Identity not found on '
                                      f'server. Details:')
                _log_criteria()
            elif len(matching_identities) > 1:
                item_map.log(self.id,
                             f'- RegEx-Based Map {regex_map_index}: Multiple possibilities for '
                             f'identity found. Details:')
                _log_criteria()
                item_map.log(self.id, f'  Matching identities:')
                if new_type == 'User':
                    item_map.log(self.id, textwrap.indent('\n'.join([
                        f"Username: {u.username}   Email: {u.email}   Name: {u.name}   ID: {u.id}   "
                        f"Datasource Name: {u.datasource_name}"
                        for u in matching_identities
                    ]), '    '))
                else:
                    item_map.log(self.id, textwrap.indent('\n'.join([
                        f"Name: {u.name}   ID: {u.id}   Datasource Name: {u.datasource.name}"
                        for u in matching_identities
                    ]), '    '))
            else:
                matched_identity = matching_identities[0]

            if matched_identity is not None:
                if new_type == 'User':
                    from seeq.spy.workbooks._user import User
                    item = User.pull(matched_identity.id, session=session)
                else:
                    from seeq.spy.workbooks._user import UserGroup
                    item = UserGroup.pull(matched_identity.id, session=session)

        if item is not None:
            item_map.log(self.id, f'- RegEx-Based Map {regex_map_index}: Successfully mapped. Details:')
            _log_criteria(item)

        return item, True


class PushThis(Exception):
    def __init__(self, definition):
        self.definition = definition


class StoredItem(StoredOrCalculatedItem):
    def get_metadata_to_push(self, context: WorkbookPushContext, datasource_maps, datasource_output,
                             item_inventory: dict, *, pushed_workbook_id=None, item_map: ItemMap = None, label=None,
                             item_exists: ItemExists = ItemExists.MAYBE,
                             item_search_preview: ItemSearchPreviewV1 = None):
        try:
            item = self._lookup(context, datasource_output,
                                pushed_workbook_id=pushed_workbook_id, item_map=item_map, label=label,
                                dummy_items_workbook_context=context.dummy_items_workbook_context,
                                item_exists=item_exists, item_search_preview=item_search_preview,
                                item_inventory=item_inventory)
        except PushThis as e:
            return e.definition

        if item.type not in ['User', 'UserGroup']:
            # We need to exclude Example Data, because it is set explicitly by the connector
            datasource_class = item['Datasource Class']
            datasource_id = item['Datasource ID']
            is_example_data = (datasource_class and datasource_class == 'Time Series CSV Files' and
                               datasource_id and datasource_id == 'Example Data')

            if (context.override_max_interp and item.type == 'StoredSignal' and not is_example_data and
                    'Maximum Interpolation' in self):
                src_max_interp = Item._property_input_from_scalar_str(self['Maximum Interpolation'])
                dst_max_interp_prop = item['Maximum Interpolation']
                if (dst_max_interp_prop and hasattr(dst_max_interp_prop, 'value')
                        and hasattr(dst_max_interp_prop, 'unit_of_measure')):
                    dst_max_interp = Item._property_input_from_scalar_str(dst_max_interp_prop.value)
                    if src_max_interp.unit_of_measure != dst_max_interp.unit_of_measure or \
                            src_max_interp.value != dst_max_interp.value:
                        if context is not None and not context.dry_run:
                            Status.log_if(
                                context,
                                f'Setting Override Maximum Interpolation for {item} to {src_max_interp.value} '
                                f'{src_max_interp.unit_of_measure}'
                            )
                            items_api = ItemsApi(context.session.client)
                            items_api.set_property(id=item.id,
                                                   property_name='Override Maximum Interpolation',
                                                   body=src_max_interp)
                        else:
                            Status.log_if(
                                context,
                                f'[Dry Run] Would set Override Maximum Interpolation for {item} to '
                                f'{src_max_interp.value} {src_max_interp.unit_of_measure}'
                            )

        return None

    def _push_dummy_item(self, context: WorkbookPushContext, label: str, item_map: ItemMap,
                         datasource_output: DatasourceOutputV1, dummy_items_workbook_context):
        metadata_dict = self.definition_dict.copy()

        if context.global_inventory == 'overwrite' and not _common.present(self.definition, 'Scoped To'):
            label = None

        metadata_dict['Dummy Item'] = True

        metadata_dict['Original ID'] = metadata_dict['ID']
        metadata_dict['Original Datasource Class'] = metadata_dict['Datasource Class']
        metadata_dict['Original Datasource ID'] = metadata_dict['Datasource ID']

        if 'Data ID' in metadata_dict:
            metadata_dict['Original Data ID'] = metadata_dict['Data ID']

        del metadata_dict['ID']
        metadata_dict['Datasource Class'] = datasource_output.datasource_class
        metadata_dict['Datasource ID'] = datasource_output.datasource_id
        metadata_dict['Data ID'] = self._construct_data_id(
            label, for_item=self, reconcile_by=context.reconcile_inventory_by,
            workbook_id=dummy_items_workbook_context.workbook_object.id)

        if 'Parent ID' in metadata_dict:
            # Dummy items will be pushed with a Path and Asset so that it gets put in a (minimal) tree and therefore can
            # be asset-swapped.
            del metadata_dict['Parent ID']

        # Scope it to the dummy item workbook
        metadata_dict['Scoped To'] = dummy_items_workbook_context.workbook_object.id

        item_map.log(self.id, f'Dummy item pushed: {self}')

        raise PushThis(metadata_dict)

    def _push_local_item(self, context: WorkbookPushContext, label: str, item_map: ItemMap,
                         datasource_output: DatasourceOutputV1, pushed_workbook_id: str,
                         item_inventory: dict, item_exists: bool = False):
        metadata_dict = self.definition_dict.copy()

        metadata_dict['Dummy Item'] = (metadata_dict.get('Type') not in ['Asset', 'Datafile'])

        if 'Parent ID' in metadata_dict:
            if metadata_dict['Parent ID'] == Item.ROOT:
                del metadata_dict['Parent ID']

        metadata_dict['Original ID'] = metadata_dict['ID']
        metadata_dict['Original Datasource Class'] = metadata_dict['Datasource Class']
        metadata_dict['Original Datasource ID'] = metadata_dict['Datasource ID']
        if 'Data ID' in metadata_dict:
            metadata_dict['Original Data ID'] = metadata_dict['Data ID']

        if not item_exists:
            del metadata_dict['ID']
            metadata_dict['Datasource Class'] = datasource_output.datasource_class
            metadata_dict['Datasource ID'] = datasource_output.datasource_id
            metadata_dict['Data ID'] = self._construct_data_id(
                label, for_item=self, reconcile_by=context.reconcile_inventory_by,
                workbook_id=pushed_workbook_id)

            if 'Parent ID' in metadata_dict:
                metadata_dict['Parent Data ID'] = self._construct_data_id(
                    label, for_item=item_inventory[self.definition['Parent ID']],
                    reconcile_by=context.reconcile_inventory_by, workbook_id=pushed_workbook_id)
                del metadata_dict['Parent ID']
        else:
            # get here when round tripping an item that already exists but may be in a different
            # datasource than the workbooks.push operation (i.e. label=None)
            # to still use batch endpoints when possible, scrub the ID for items in the matching datasource
            if (metadata_dict['Datasource Class'] == datasource_output.datasource_class and
                    metadata_dict['Datasource ID'] == datasource_output.datasource_id):
                del metadata_dict['ID']

        # Scope it to the pushed workbook
        metadata_dict['Scoped To'] = pushed_workbook_id

        item_map.log(self.id, f'Local item pushed: {self}')

        raise PushThis(metadata_dict)

    def _lookup(self, context: WorkbookPushContext, datasource_output, *,
                pushed_workbook_id=None, item_map: ItemMap = None, label=None,
                dummy_items_workbook_context=None, item_exists: ItemExists = ItemExists.MAYBE,
                item_search_preview: Optional[ItemSearchPreviewV1] = None,
                item_inventory: Optional[dict] = None):
        status = context.status

        # Note: The caller of this function is in charge of API safety
        if self.id in item_map.data_item_cache:
            cached_item = item_map.data_item_cache[self.id]
            status.log(f'Lookup: Item {self} found in cache: {cached_item}')
            return cached_item

        if self.id in context.failed_mappings:
            raise SPyDependencyNotFound(item_map.explain(self.id))

        local: bool = self['Scoped To'] is not None
        only_override_maps = item_map.only_override_maps
        must_lookup_global = not local and context.global_inventory == 'overwrite'
        if local:
            only_override_maps = True

        force_direct_lookup = label is None or must_lookup_global

        item = self._lookup_item_via_datasource_map(context, pushed_workbook_id, item_map,
                                                    only_override_maps=only_override_maps,
                                                    force_direct_lookup=force_direct_lookup,
                                                    item_exists=item_exists,
                                                    item_search_preview=item_search_preview)

        dry_run_tense = 'Would push' if context.dry_run else 'Pushing'
        if item is None:
            if local:
                status.log(f'{dry_run_tense} local item for {self}')
                if not context.dry_run:
                    self._push_local_item(context, label, item_map, datasource_output, pushed_workbook_id,
                                          item_inventory)
            else:
                if dummy_items_workbook_context is None:
                    status.log(f'Mapping failed for {self}:\n{item_map.explain(self.id)}',
                               level=logging.ERROR)
                    # Add to failed mappings so we don't try again and spam the logs
                    context.failed_mappings.add(self.id)
                    raise SPyDependencyNotFound(item_map.explain(self.id))

                status.log(f'{dry_run_tense} dummy item for {self}')
                self._push_dummy_item(context, label, item_map, datasource_output, dummy_items_workbook_context)
        elif local and context.mode != WorkbookPushMode.IN_PLACE_DATASOURCE_SWAP:
            item_scope = _common.get(item, 'Scoped To')
            item_is_scoped_to_other_workbook = item_scope is not None and item_scope != pushed_workbook_id
            self_already_exists_and_may_need_update = (
                    item_scope is not None
                    and item_scope == pushed_workbook_id
                    and _common.get(self, 'ID') == _common.get(item, 'ID')
                    and not label
            )
            if item_is_scoped_to_other_workbook or self_already_exists_and_may_need_update:
                Status.log_if(
                    context,
                    f'{dry_run_tense} local item because existing item is scoped to another workbook or may need update: '
                    f'{self} (existing item scoped to {item_scope})'
                )
                if not context.dry_run:
                    self._push_local_item(
                        context, label, item_map, datasource_output, pushed_workbook_id, item_inventory,
                        self_already_exists_and_may_need_update)

        item_map[self.id] = item.id
        item_map.data_item_cache[self.id] = item

        return item


class Asset(StoredItem):
    def __init__(self, definition=None, *, provenance=None):
        super().__init__(definition, provenance=provenance)

        if self.provenance == Item.LOAD:
            if self.definition.get('Old Asset Format', True):
                if self.type == 'Asset':
                    if self.definition.get('Path') in [None, '']:
                        self.definition['Path'] = self.definition['Asset']
                    else:
                        self.definition['Path'] += ' >> ' + self.definition['Asset']
                        self.definition['Asset'] = self.definition['Name']

        self.definition['Old Asset Format'] = False


class Datafile(StoredItem):
    pass


class Datasource(StoredItem):
    """
    The SPy representation of a Datasource, the 'source' container for a collection of other items.
    """

    @staticmethod
    def from_datasource_output(datasource_output: Union[DatasourceOutputV1, DatasourcePreviewV1]):
        return Datasource({
            'ID': datasource_output.id,
            'Name': datasource_output.name,
            'Datasource Class': datasource_output.datasource_class,
            'Datasource ID': datasource_output.datasource_id,
            'Archived': datasource_output.is_archived
        })


class CalculatedItem(StoredOrCalculatedItem):
    def _lookup(self, context: WorkbookPushContext, pushed_workbook_id, item_map: ItemMap,
                item_exists: ItemExists, item_search_preview: Optional[ItemSearchPreviewV1]):
        if self.id in item_map.data_item_cache:
            return item_map.data_item_cache[self.id]

        # This is a key piece of datasource mapping logic. CalculatedItems that are in trees are more like "source
        # data" in the context of workbooks/worksheets. In other words, when we push them, we want to map in existing
        # items rather than creating a standalone CalculatedItem that isn't a part of a tree, has no associated asset
        # and cannot be swapped.
        is_standalone_item = _common.get(self, 'Asset') is None

        # So if it's in a global tree, we process the datasource maps just like we would if it were a StoredItem. If
        # it's *not* in a global tree, then we only process datasource maps that have been supplied in a
        # datasource_map_folder and are therefore treated as "overrides". CalculatedItems that are associated with the
        # particular analysis of a workbook should be created/overwritten as part of the push, and since they won't
        # exist in a tree, we purposefully don't attempt to do any mapping and we fall through to the CalculatedItem's
        # create/update code.
        local: bool = self['Scoped To'] is not None
        only_override_maps = item_map.only_override_maps
        if local or is_standalone_item:
            only_override_maps = True

        item = self._lookup_item_via_datasource_map(
            context, pushed_workbook_id, item_map, only_override_maps=only_override_maps,
            item_exists=item_exists, item_search_preview=item_search_preview)

        if item is None and context.mode == WorkbookPushMode.IN_PLACE_DATASOURCE_SWAP:
            # If we didn't explicitly map the item somewhere else, then we're just using the item as-is
            item = self

        if not local and not is_standalone_item and item is None:
            raise SPyDependencyNotFound(item_map.explain(self.id))

        if item:
            item_map[self.id] = item.id
            item_map.data_item_cache[self.id] = item

        return item

    def _find_by_name(self, session: Session, workbook_id):
        return Item.find_item_by_search(session, f'Name=={self.name}', scope=[workbook_id], types=[self.type])

    def get_metadata_to_push(self, context: WorkbookPushContext, datasource_maps, datasource_output,
                             item_inventory: dict, *, pushed_workbook_id=None, item_map: ItemMap = None, label=None,
                             item_exists: ItemExists = ItemExists.MAYBE,
                             item_search_preview: ItemSearchPreviewV1 = None):
        # If global_inventory is 'do not touch' and this is a global item, skip processing it
        if context.global_inventory == 'do not touch' and not _common.present(self.definition, 'Scoped To'):
            Status.log_if(context, f'Ignoring global inventory item: {self}')
            item_map[self.id] = self.id
            return None

        item = self._lookup(context, pushed_workbook_id, item_map, item_exists, item_search_preview)

        if item:
            return None

        item_output = item_search_preview
        if self.provenance == Item.CONSTRUCTOR:
            if item_exists == ItemExists.MAYBE:
                item_output = self.find_me(context.session, label, datasource_output)

            if item_output is None:
                item_output = self._find_by_name(context.session, pushed_workbook_id)

        if context.global_inventory == 'overwrite' and not _common.present(self.definition, 'Scoped To'):
            label = None

        if label is None and item_exists != ItemExists.NO and item_search_preview is None:
            item_output = self.find_me(context.session, label, datasource_output)

        metadata_dict = copy.deepcopy(self.definition_dict)

        if 'Formula' in self.definition:
            metadata_dict['Formula'] = Item.formula_string_from_list(self.definition['Formula'])

        if context.global_inventory == 'copy local' or _common.present(self.definition, 'Scoped To'):
            metadata_dict['Scoped To'] = pushed_workbook_id

        if 'Scoped To' not in metadata_dict:
            pushed_workbook_id = None

        # Custody ID preserves the original ID of the item which helps maintain a consistent Data ID for the same
        # item through multiple round-trips.
        metadata_dict['Custody ID'] = self.get('Custody ID', self.id)

        if (label is None or self.provenance == Item.CONSTRUCTOR) and item_output is not None:
            def _prop(_n):
                if isinstance(item_output, ItemSearchPreviewV1):
                    return item_output.included_properties[_n].value
                elif isinstance(item_output, ItemOutputV1):
                    return [_p.value for _p in item_output.properties if _p.name == _n][0]

            metadata_dict['Datasource Class'] = _prop('Datasource Class')
            metadata_dict['Datasource ID'] = _prop('Datasource ID')
            metadata_dict['Data ID'] = _prop('Data ID')

            if (metadata_dict['Datasource Class'] == datasource_output.datasource_class and
                    metadata_dict['Datasource ID'] == datasource_output.datasource_id):
                # This allows the batch endpoints to be used
                del metadata_dict['ID']
        else:
            del metadata_dict['ID']
            metadata_dict['Datasource Class'] = datasource_output.datasource_class
            metadata_dict['Datasource ID'] = datasource_output.datasource_id
            metadata_dict['Data ID'] = self._construct_data_id(
                label, for_item=self, reconcile_by=context.reconcile_inventory_by, workbook_id=pushed_workbook_id)

            if 'Parent ID' in metadata_dict:
                metadata_dict['Parent Data ID'] = self._construct_data_id(
                    label, for_item=item_inventory[self.definition['Parent ID']],
                    reconcile_by=context.reconcile_inventory_by, workbook_id=pushed_workbook_id)

        return metadata_dict


class StoredSignal(StoredItem):
    """
    The SPy representation of a Stored Signal, a collection of samples composed of timestamp + value pairs.
    These samples may be stored in an external datasource or within the Seeq database.
    """
    pass


class CalculatedSignal(CalculatedItem):
    """
    The SPy representation of a Calculated Signal, a collection of samples composed of timestamp + value pairs.
    These samples are calculated based on formula inputs.
    """

    def _pull(self, session: Session, item_id, status, item_search_preview: ItemSearchPreviewV1):
        super()._pull(session, item_id, status, item_search_preview)

        if item_search_preview is None:
            # Note: The caller of this function is in charge of API safety
            signals_api = SignalsApi(session.client)
            signal_output = signals_api.get_signal(id=item_id)  # type: SignalOutputV1
            self._set_formula_based_item_properties(signal_output.parameters)
        else:
            self._set_formula_based_item_properties(item_search_preview.parameters)


class StoredCondition(StoredItem):
    """
    The SPy representation of a Stored Condition, a collection of capsules composed of start & end timestamps
    plus optional properties.
    These capsules may be stored in an external datasource or within the Seeq database.
    """
    pass


class CalculatedCondition(CalculatedItem):
    """
    The SPy representation of a Calculated Condition, a collection of capsules composed of start & end timestamps
    plus optional properties.
    These capsules are calculated based on formula inputs.
    """

    def _pull(self, session: Session, item_id, status, item_search_preview: ItemSearchPreviewV1):
        super()._pull(session, item_id, status, item_search_preview)

        if item_search_preview is None:
            # Note: The caller of this function is in charge of API safety
            conditions_api = ConditionsApi(session.client)
            condition_output = conditions_api.get_condition(id=item_id)  # type: ConditionOutputV1
            self._set_formula_based_item_properties(condition_output.parameters)
        else:
            self._set_formula_based_item_properties(item_search_preview.parameters)


class LiteralScalar(StoredItem):
    """
    The SPy representation of a Literal Scalar, a single value with an optional unit of measure.
    This value may be stored in an external datasource or within the Seeq database.
    """
    pass


class CalculatedScalar(CalculatedItem):
    """
    The SPy representation of a Calculated Scalar, a single value with an optional unit of measure.
    This value is calculated based on formula inputs.
    """

    def _pull(self, session: Session, item_id, status: Status, item_search_preview: ItemSearchPreviewV1):
        super()._pull(session, item_id, status, item_search_preview)
        if item_search_preview is None:
            # Note: The caller of this function is in charge of API safety
            scalars_api = ScalarsApi(session.client)
            calculated_item_output = scalars_api.get_scalar(id=item_id)  # type: CalculatedItemOutputV1
            self._set_formula_based_item_properties(calculated_item_output.parameters)
        else:
            self._set_formula_based_item_properties(item_search_preview.parameters)


class Chart(CalculatedItem):
    """
    The SPy representation of a Chart or Histogram, a calculation that accepts a time range and computes
    aggregated values within this time range.
    The values are calculated based on formula inputs and the time range.
    """

    def _pull(self, session: Session, item_id, status: Status, item_search_preview: ItemSearchPreviewV1):
        super()._pull(session, item_id, status, item_search_preview)

        if item_search_preview is None:
            # Note: The caller of this function is in charge of API safety
            formulas_api = FormulasApi(session.client)
            calculated_item_output = formulas_api.get_function(id=item_id)  # type: CalculatedItemOutputV1

            self._set_formula_based_item_properties(calculated_item_output.parameters)
        else:
            self._set_formula_based_item_properties(item_search_preview.parameters)

        if 'FormulaParameters' in self.definition:
            # Charts have these superfluous properties
            del self.definition['FormulaParameters']


class ThresholdMetric(CalculatedItem):
    """
    The SPy representation of a Threshold Metric, a table-like calculation aggregates values and can have threshold
    states based on those aggregated values.
    The values are calculated based on formula inputs.
    """

    def _pull(self, session: Session, item_id, status: Status, item_search_preview: ItemSearchPreviewV1):
        super()._pull(session, item_id, status, item_search_preview)
        # Note: The caller of this function is in charge of API safety
        formula_parameters = _metadata.formula_parameters_dict_from_threshold_metric(session, item_id)

        # These properties come through in the GET /items/{id} call, and for clarity's sake we remove them
        for ugly_duplicate_property in ['AggregationFunction', 'BoundingConditionMaximumDuration']:
            if ugly_duplicate_property in self.definition:
                del self.definition[ugly_duplicate_property]

        self.definition['Formula'] = '<ThresholdMetric>'
        self.definition['Formula Parameters'] = formula_parameters
