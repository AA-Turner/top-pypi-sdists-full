from __future__ import annotations

import copy
import csv
import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict, Set, Tuple

import pandas as pd

from seeq.base import util
from seeq.sdk import *
from seeq.spy import _common
from seeq.spy._errors import *
from seeq.spy._session import Session
from seeq.spy._status import Status


class DatasourceMapList:
    _maps: List[dict]

    def __init__(self, maps: List[dict] = None):
        self._maps = maps if maps is not None else list()

    def __getitem__(self, key) -> dict:
        return self._maps.__getitem__(key)

    def __setitem__(self, key, val: dict):
        return self._maps.__setitem__(key, val)

    def __len__(self):
        return self._maps.__len__()

    def __repr__(self):
        return self._maps.__repr__()

    def _find(self, datasource_class: str, datasource_id: str) -> int:
        for i in range(len(self._maps)):
            datasource_map = self._maps[i]
            if (datasource_map['Datasource Class'] == datasource_class and
                    datasource_map['Datasource ID'] == datasource_id):
                return i

        return -1

    def __contains__(self, datasource_map: dict) -> bool:
        return self._find(datasource_map['Datasource Class'], datasource_map['Datasource ID']) >= 0

    def get(self, datasource_class: str, datasource_id: str) -> dict:
        index = self._find(datasource_class, datasource_id)
        if index == -1:
            raise SPyValueError(f'Datasource map for Datasource Class "{datasource_class}" and Datasource ID '
                                f'"{datasource_id}" not found')

        return self._maps[index]

    def append(self, datasource_map: dict, overwrite=False):
        if not isinstance(datasource_map, dict):
            raise SPyTypeError('append() requires a dict argument')

        for key in ['Datasource Class', 'Datasource ID']:
            if key not in datasource_map:
                raise SPyValueError(f'append() datasource_map requires a {key}')

        index = self._find(datasource_map['Datasource Class'], datasource_map['Datasource ID'])
        if index >= 0:
            if overwrite:
                self._maps[index] = datasource_map
        else:
            self._maps.append(datasource_map)

    def extend(self, datasource_maps: List[dict], overwrite=False):
        if not isinstance(datasource_maps, (list, DatasourceMapList)):
            raise SPyTypeError('append() requires a list or DatasourceMapList argument')

        for datasource_map in datasource_maps:
            self.append(datasource_map, overwrite=overwrite)

    def copy(self):
        return DatasourceMapList(copy.deepcopy(self._maps))


class WorkbookPushMode:
    NORMAL = 'normal'
    IN_PLACE_DATASOURCE_SWAP = 'in-place datasource swap'


@dataclass
class WorkbookPushContext:
    access_control: Optional[str]
    datasource: Optional[str]
    dummy_items_workbook_context: Optional[Any]
    include_annotations: Optional[bool]
    override_max_interp: Optional[bool]
    owner: Optional[str]
    reconcile_inventory_by: str
    global_inventory: str
    session: Session
    specific_worksheet_ids: Optional[List[str]]
    pushed_inventory: Optional[Dict[str, pd.DataFrame]]
    status: Status
    dry_run: bool
    mode: str = WorkbookPushMode.NORMAL
    datasource_maps: Optional[DatasourceMapList] = None
    datasource_id_cache: Dict[Tuple[str, str], str] = field(default_factory=dict)
    failed_mappings: Set[str] = field(default_factory=set)
    intentional_no_mappings: Set[str] = field(default_factory=set)
    errors_displayed_count: int = 0
    annotations_to_fixup: Dict[str, Any] = field(default_factory=dict)
    all_users: Optional[List[UserOutputV1]] = None
    all_groups: Optional[List[IdentityPreviewV1]] = None

    def add_server_scoped_item_level_map_files(self, datasource_map_list: DatasourceMapList):
        # These "server-scoped item-level map files" serve as a sort of cache, one that
        # skips the expensive search on the server if it has been encountered before. It's
        # especially useful for datasource map folders that get re-used across multiple
        # pushes. If the datasource map definition changes at all, it would change the
        # hash in the filename and effectively "invalidate" the cache.
        for datasource_map in datasource_map_list:
            self._set_server_scoped_item_level_map_file_name(datasource_map)
            server_scoped_filename = datasource_map[_common.DATASOURCE_MAP_SERVER_SCOPED_ITEM_LEVEL_MAP_FILE]
            item_level_map_files = datasource_map.setdefault(_common.DATASOURCE_MAP_ITEM_LEVEL_MAP_FILES, list())
            item_level_map_files_set = {f.lower() for f in item_level_map_files}
            if server_scoped_filename.lower() in item_level_map_files_set:
                continue

            if util.safe_exists(server_scoped_filename):
                self.status.log(f'Datasource map "{os.path.basename(datasource_map["File"])}" has server-scoped '
                                f'item-level datasource map file: {server_scoped_filename}')
                item_level_map_files.append(server_scoped_filename)

    def _set_server_scoped_item_level_map_file_name(self, datasource_map):
        json_to_hash = copy.deepcopy(datasource_map)
        filename = json_to_hash.pop('File')
        json_to_hash.pop('DataFrames', None)
        json_to_hash.pop(_common.DATASOURCE_MAP_SERVER_SCOPED_ITEM_LEVEL_MAP_FILE, None)
        json_str = json.dumps(json_to_hash, sort_keys=True)
        hostname = self.session.public_url.replace('https://', '').replace('http://', '').replace(':', '_').lower()
        hash_object = hashlib.md5(json_str.encode())
        hash_hex = hash_object.hexdigest()[:8]
        server_scoped_filename = f'Server_Scoped_Item_Level_Datasource_Map_{hostname}_{hash_hex}.csv'
        server_scoped_fullpath = os.path.join(os.path.dirname(filename), server_scoped_filename)
        datasource_map[_common.DATASOURCE_MAP_SERVER_SCOPED_ITEM_LEVEL_MAP_FILE] = server_scoped_fullpath

    def append_to_server_scoped_item_level_map_file(self, datasource_map, source_item, destination_item):
        if _common.DATASOURCE_MAP_SERVER_SCOPED_ITEM_LEVEL_MAP_FILE not in datasource_map:
            return

        server_scoped_filename = datasource_map[_common.DATASOURCE_MAP_SERVER_SCOPED_ITEM_LEVEL_MAP_FILE]

        file_exists = util.safe_isfile(server_scoped_filename)
        with util.safe_open(server_scoped_filename, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Old Type', 'Old ID', 'Old Datasource Class', 'Old Datasource Name', 'Old Datasource ID',
                          'Old Path', 'Old Asset', 'Old Name',
                          'New Type', 'New ID', 'New Datasource Class', 'New Datasource Name', 'New Datasource ID',
                          'New Path', 'New Asset', 'New Name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            destination_datasource_name = source_item.get('Datasource Name')
            if destination_datasource_name is None and destination_item.datasource is not None:
                destination_datasource_name = destination_item.datasource.name

            writer.writerow({
                'Old Type': source_item.type,
                'Old ID': source_item.id,
                'Old Datasource Class': source_item.get('Datasource Class'),
                'Old Datasource Name': source_item.get('Datasource Name'),
                'Old Datasource ID': source_item.get('Datasource ID'),
                'Old Path': source_item.get('Path'),
                'Old Asset': source_item.get('Asset'),
                'Old Name': source_item.name,
                'New Type': destination_item.type,
                'New ID': destination_item.id,
                'New Datasource Class': destination_item.get('Datasource Class'),
                'New Datasource Name': destination_datasource_name,
                'New Datasource ID': destination_item.get('Datasource ID'),
                'New Path': destination_item.get('Path'),
                'New Asset': destination_item.get('Asset'),
                'New Name': destination_item.name
            })

        self.status.log(f'Appended item-level mapping to {os.path.basename(server_scoped_filename)}: '
                        f'{source_item.id} -> {destination_item.id}')

    def fetch_all_users(self):
        if self.all_users is not None:
            return

        users_api = UsersApi(self.session.client)

        offset = 0
        limit = 10_000
        self.all_users = list()
        auth_providers_dict = {p.name: p for p in self.session.auth_providers}
        while True:
            user_output_list = users_api.get_users(offset=offset, limit=limit)

            # UserOutputV1 doesn't have a datasource sub-object, but it's much easier
            # to treat Users and Groups similarly if we just plant it there anyways
            for user_output in user_output_list.users:  # type: UserOutputV1
                setattr(user_output, 'datasource', auth_providers_dict[user_output.datasource_name])

            self.all_users.extend(user_output_list.users)

            if len(user_output_list.users) < limit:
                break

            offset += limit

    def fetch_all_groups(self):
        if self.all_groups is not None:
            return

        user_groups_api = UserGroupsApi(self.session.client)

        offset = 0
        limit = 10_000
        self.all_groups = list()
        while True:
            identity_preview_list = user_groups_api.get_user_groups(offset=offset, limit=limit)
            self.all_groups.extend(identity_preview_list.items)

            if len(identity_preview_list.items) < limit:
                break

            offset += limit
