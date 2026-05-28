from __future__ import annotations

import copy
import glob
import json
import logging
import os
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Dict, Iterable, List, Optional, Type, Union, Tuple
from urllib.parse import urljoin

import numpy as np
import pandas as pd

from seeq.base import util
from seeq.base.seeq_names import SeeqNames
from seeq.sdk import *
from seeq.spy import _common
from seeq.spy import _metadata
from seeq.spy import _search as _spy_search
from seeq.spy import _url
from seeq.spy import _version
from seeq.spy._context import WorkbookContext
from seeq.spy._errors import *
from seeq.spy._redaction import safely, request_safely
from seeq.spy._session import Session
from seeq.spy._status import Status
from seeq.spy.workbooks import _folder
from seeq.spy.workbooks import _item
from seeq.spy.workbooks import _render
from seeq.spy.workbooks import _search
from seeq.spy.workbooks._annotation import Annotation, Journal
from seeq.spy.workbooks._context import WorkbookPushContext, DatasourceMapList, WorkbookPushMode
from seeq.spy.workbooks._data import Datasource, StoredOrCalculatedItem, ThresholdMetric, CalculatedItem, Chart
from seeq.spy.workbooks._folder import Folder
from seeq.spy.workbooks._item import Item, ItemList, Reference, ItemExists
from seeq.spy.workbooks._item_map import ItemMap
from seeq.spy.workbooks._user import ItemWithOwnerAndAcl
from seeq.spy.workbooks._worksheet import (Worksheet, AnalysisWorksheet, WorksheetForAnalysisOrRoom, TopicDocument,
                                           WorksheetList, RoomView)


class ItemJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Item):
            return o.definition_dict
        else:
            return o


class Workbook(ItemWithOwnerAndAcl):
    NULL_DATASOURCE_STRING = '__null__'
    _annotation: Optional[Annotation]
    _item_inventory: dict
    _datasource_maps: DatasourceMapList
    _datasource_inventory: dict
    _pull_errors: set
    _push_errors: set
    _push_context: Optional[WorkbookPushContext]

    worksheets: WorksheetList

    def __new__(cls, *args, **kwargs):
        if cls is Workbook:
            raise SPyTypeError("Workbook may not be instantiated directly, create either Analysis or Topic")

        return object.__new__(cls)

    def __init__(self, definition=None, *, provenance=None):
        if isinstance(definition, str):
            definition = {'Name': definition}

        super().__init__(definition, provenance=provenance)

        self.worksheets = WorksheetList(self)

        self._annotation = None  # Currently only Vantage Room workbook objects populate this
        self._push_context = None
        self._item_inventory = dict()
        self._datasource_maps = DatasourceMapList()
        self._datasource_inventory = dict()
        self._pull_errors = set()
        self._push_errors = set()

        if 'Workbook Type' not in self._definition:
            self._definition['Workbook Type'] = self.__class__.__name__.replace('Template', '')
            if self._definition['Workbook Type'] == 'Room':
                self._definition['Workbook Type'] = 'Vantage'
        if 'Name' not in self._definition:
            self._definition['Name'] = _common.DEFAULT_WORKBOOK_NAME

    @property
    def real(self):
        # This will get overridden in the WorkbookFolderRef case
        return self

    @property
    def url(self):
        # Note that 'URL' won't be filled in if a workbook/worksheet hasn't been pushed/pulled. That's because the
        # IDs may change from the placeholders that get generated.
        return self['URL']

    @property
    def path(self):
        if 'Ancestors' not in self:
            return ''

        parts = list()
        for folder_id in self['Ancestors']:
            if not _common.is_guid(folder_id):
                parts.append(folder_id)
                continue

            folder = self.item_inventory.get(folder_id)

            if folder is None:
                raise SPyRuntimeError(f'Folder ID "{folder_id}" not found in item inventory')

            # Don't include the user's home folder if it is the first item
            if len(parts) == 0 and folder.definition.get(SeeqNames.Properties.unmodifiable) and \
                    folder.definition.get(SeeqNames.Properties.unsearchable):
                continue

            parts.append(folder.name)

        return ' >> '.join(parts)

    @property
    def pull_errors(self):
        return self._pull_errors

    @property
    def pull_errors_str(self):
        return '\n'.join(self._pull_errors)

    @property
    def push_errors(self):
        return self._push_errors

    @push_errors.setter
    def push_errors(self, val):
        self._push_errors = val

    @property
    def push_errors_str(self):
        return '\n'.join(sorted(list(self._push_errors)))

    @property
    def already_pushed(self):
        # This will be overridden in WorkbookFolderRef
        return False

    @property
    def item_inventory(self):
        return self._item_inventory

    def item_inventory_df(self) -> pd.DataFrame:
        return pd.DataFrame([item.definition_dict for item in self.item_inventory.values()])

    @property
    def datasource_maps(self):
        return self._datasource_maps

    @datasource_maps.setter
    def datasource_maps(self, val):
        if isinstance(val, list):
            val = DatasourceMapList(val)
        elif not isinstance(val, DatasourceMapList):
            raise SPyTypeError('datasource_maps must be a list')

        self._datasource_maps = val

    @property
    def datasource_inventory(self):
        return self._datasource_inventory

    @property
    def annotation(self):
        return self._annotation

    def get_workstep_usages(self, use_investigate_range=False, now: pd.Timestamp = None) -> Dict[str, list]:
        if now is not None:
            if not isinstance(now, pd.Timestamp):
                raise SPyTypeError('now must be a pd.Timestamp')
            if now.tz is None:
                raise SPyTypeError('now must have a timezone associated')

        return dict()

    def update_status(self, result, count_increment):
        if self._push_context is None or self._push_context.status is None:
            return

        status = self._push_context.status
        if status.current_df_index is None and len(status.df) == 0:
            status.df.at[0, :] = None
            status.current_df_index = 0
        current_count = status.get('Count') if \
            'Count' in status.df and status.get('Count') is not None else 0
        status.put('Count', current_count + count_increment)
        status.put('Time', status.get_timer())
        status.put('Result', result)
        status.update()

    def refresh_from(self, context: WorkbookPushContext, new_item, item_map: ItemMap, status: Status, *,
                     include_inventory: bool = False, specific_worksheet_ids: Optional[List[str]] = None):
        super().refresh_from(context, new_item, item_map, status)

        for worksheet in self.worksheets:
            if specific_worksheet_ids is not None and worksheet.id not in specific_worksheet_ids:
                continue

            if context.current_params.mode == WorkbookPushMode.IN_PLACE_DATASOURCE_SWAP:
                new_worksheet_id = worksheet.id
            else:
                new_worksheet_id = item_map[worksheet.id]

            new_worksheet_list = [w for w in new_item.worksheets if w.id == new_worksheet_id]
            if len(new_worksheet_list) == 1:
                worksheet.refresh_from(context, new_worksheet_list[0], item_map, status)

        if not include_inventory:
            return

        new_inventory = new_item.item_inventory.copy()
        for inventory_item_id, inventory_item in self.item_inventory.copy().items():
            # noinspection PyBroadException
            try:
                if inventory_item_id not in item_map:
                    if inventory_item.type == 'Folder':
                        # Folders may not have been pushed (depending on spy.workbooks.push arguments) and therefore
                        # won't be in the map, so skip them.
                        continue

                    raise SPyRuntimeError(f'Item "{inventory_item}" not found in item_map')

                new_inventory_item_id = item_map[inventory_item_id]

                if new_inventory_item_id not in new_inventory:
                    # This can happen when something that is scoped to a workbook is not actually referenced by a
                    # worksheet or calculated item in that workbook, and then you are pushing with a label to a
                    # different location. The workbook in that new location will not have the item in its inventory,
                    # so we just remove it during the refresh.
                    del self.item_inventory[inventory_item_id]
                else:
                    new_inventory_item = new_inventory[new_inventory_item_id]
                    inventory_item.refresh_from(context, new_inventory_item, item_map, status)
                    del self.item_inventory[inventory_item_id]
                    self.item_inventory[new_inventory_item_id] = inventory_item

            except Exception as e:
                if status.errors == 'catalog':
                    status.warn(f'Unable to refresh Item {inventory_item}:\n{e}')

        # Transfer the remaining (new) inventory over. This often includes new folders.
        for new_inventory_item_id, new_inventory_item in new_inventory.items():
            if new_inventory_item_id not in self.item_inventory:
                self.item_inventory[new_inventory_item_id] = new_inventory_item

        self._datasource_inventory = new_item.datasource_inventory
        self._datasource_maps = new_item.datasource_maps

    @staticmethod
    def _instantiate(definition=None, *, provenance=None):
        if definition['Type'] == 'Workbook':
            if 'Workbook Type' not in definition:
                if 'Data' not in definition or _common.get_workbook_type(definition['Data']) == 'Analysis':
                    definition['Workbook Type'] = 'Analysis'
                else:
                    definition['Workbook Type'] = 'Topic'
        elif definition['Type'] in ['Analysis', 'Topic', 'Vantage']:
            # This is for backward compatibility with .49 and earlier, which used the same type (Workbook) for both
            # Analysis and Topic. Eventually we may want to deprecate "Workbook Type" and fold it into the "Type"
            # property.
            definition['Workbook Type'] = definition['Type']
            definition['Type'] = 'Workbook'
        else:
            raise SPyValueError(f"Unrecognized workbook type: {definition['Type']}")

        if definition['Workbook Type'] == 'Analysis':
            return Analysis(definition, provenance=provenance)
        elif definition['Workbook Type'] == 'Topic':
            return Topic(definition, provenance=provenance)
        elif definition['Workbook Type'] == 'Vantage':
            return Room(definition, provenance=provenance)

    @staticmethod
    def pull(item_id, *, status: Status = None, extra_workstep_tuples=None, include_inventory=True,
             include_annotations=True, include_images=True, include_access_control=True,
             include_archived: Optional[bool] = None, specific_worksheet_ids: Optional[List[str]] = None,
             item_cache: Optional[_common.LRUCache] = None, session: Optional[Session] = None):
        session = Session.validate(session)
        status = Status.validate(status, session)
        item_output = safely(lambda: Item._get_item_output(session, item_id),
                             action_description=f'pull Workbook {item_id}',
                             on_error=lambda e: status.put('Result', e),
                             status=status)
        if item_output is None:
            return

        definition = Item._dict_from_item_output(item_output)
        workbook = Workbook._instantiate(definition, provenance=Item.PULL)

        status.update('[%d/%d] Pulling %s "%s" (%s)' %
                      (len(status.df[status.df['Result'] != 'Queued']),
                       len(status.df), workbook['Workbook Type'], workbook['Name'], workbook['ID']),
                      Status.RUNNING)

        # noinspection PyBroadException
        try:
            workbook._pull_errors = set()
            status.on_error = lambda error: workbook._pull_errors.add(str(error))
            workbook._pull(session, extra_workstep_tuples=extra_workstep_tuples, include_inventory=include_inventory,
                           include_annotations=include_annotations, include_images=include_images,
                           include_access_control=include_access_control, include_archived=include_archived,
                           item_cache=item_cache, specific_worksheet_ids=specific_worksheet_ids, status=status)
        except Exception:
            status.on_error = None
            raise
        return workbook

    def pull_rendered_content(self, session: Session, status: Status):
        pass

    @staticmethod
    def _get_workbook_output(session: Session, workbook_id: str) -> WorkbookOutputV1:
        workbooks_api = WorkbooksApi(session.client)
        try:
            return workbooks_api.get_workbook(id=workbook_id,
                                              full_ancestry=ItemWithOwnerAndAcl.should_use_full_ancestry(session))
        except TypeError:
            # full_ancestry is not supported in this version of Seeq
            return workbooks_api.get_workbook(id=workbook_id)

    def _pull(self, session: Session, *, workbook_id=None, extra_workstep_tuples=None, include_inventory=True,
              include_images=True, include_access_control=True, include_archived: Optional[bool] = None,
              specific_worksheet_ids: Optional[List[str]] = None, item_cache: Optional[_common.LRUCache] = None,
              status: Status = None, include_annotations=True):
        status = Status.validate(status, session)

        if workbook_id is None:
            workbook_id = self.id
        workbook_output = safely(lambda: Workbook._get_workbook_output(session, workbook_id),
                                 action_description=f'get details for Workbook {workbook_id}',
                                 status=status)  # type: WorkbookOutputV1
        if workbook_output is None:
            return

        ancestors = workbook_output.ancestors.copy()
        if (len(ancestors) >= 2 and session.corporate_folder is not None and ancestors[1].id ==
                session.corporate_folder.id):
            # This happens when full_ancestry=True is passed in to get_workbook() and the item is in the
            # Corporate folder, which is technically a child of the Users folder. That's an implementation detail
            # that ends up being confusing to the user (and also a compatibility issue, since we didn't always
            # have the full_ancestry parameter). So we just remove the Users folder from the ancestors list.
            ancestors.pop(0)

        self._definition['Path'] = _common.path_list_to_string([a.name for a in ancestors])
        self._definition['Workbook Type'] = _common.get_workbook_type(workbook_output)

        for attr, prop in [('locked_metadata', 'Locked Metadata'),
                           ('evidence_table_definition_id', 'Evidence Table Definition ID')]:
            value = getattr(workbook_output, attr, None)
            if value is not None:
                self._definition[prop] = value

        if include_access_control:
            self._pull_owner_and_acl(session, workbook_output.owner, status)

        self._pull_ancestors(session, ancestors)

        self.update_status('Pulling workbook', 1)

        if 'workbookState' in self._definition:
            self._definition['workbookState'] = json.loads(self._definition['workbookState'])

        self._definition['Original Server URL'] = _item.get_canonical_server_url(session)

        self.worksheets = WorksheetList(self)

        if specific_worksheet_ids is not None:
            worksheet_ids = specific_worksheet_ids
        else:
            active_worksheet_ids = Workbook._pull_worksheet_ids(
                session, workbook_id, status,
                get_archived_worksheets=False)

            worksheet_ids = list()
            if active_worksheet_ids is not None:
                worksheet_ids.extend([ws for ws in active_worksheet_ids if ws not in worksheet_ids])

            # The default (include_archived=None) means that archived worksheets are EXCLUDED.
            if include_archived is True:
                archived_worksheet_ids = Workbook._pull_worksheet_ids(
                    session, workbook_id, status,
                    get_archived_worksheets=True)

                if archived_worksheet_ids is not None:
                    worksheet_ids.extend([ws for ws in archived_worksheet_ids if ws not in worksheet_ids])

        if extra_workstep_tuples:
            for workbook_id, worksheet_id, workstep_id in extra_workstep_tuples:
                if workbook_id == self.id and worksheet_id not in worksheet_ids:
                    worksheet_ids.append(worksheet_id)

        for worksheet_id in worksheet_ids:
            self.update_status('Pulling worksheets', 0)
            Worksheet.pull(worksheet_id, workbook=self, extra_workstep_tuples=extra_workstep_tuples,
                           include_images=include_images, include_annotations=include_annotations,
                           include_archived=include_archived, session=session, status=status)
            self.update_status('Pulling worksheets', 1)

        self['URL'] = None
        if len(self.worksheets) > 0:
            link_url = _url.SeeqURL.parse(session.public_url)
            link_url.route = _url.Route.WORKBOOK_EDIT
            link_url.folder_id = self['Ancestors'][-1] if len(self['Ancestors']) > 0 else None
            link_url.workbook_id = self.id
            link_url.worksheet_id = self.worksheets[0].id
            self['URL'] = link_url.url

        self._item_inventory = dict()
        if include_inventory:
            self._scrape_item_inventory(session, status, item_cache, include_access_control, include_archived)
            self._scrape_datasource_inventory(session)
            self._construct_default_datasource_maps()
        else:
            # Need to at least scrape folders so we know what the path is
            self._scrape_folder_inventory(session, status, item_cache, include_access_control)

        if include_annotations and self._annotation is not None:
            self._annotation.pull(session, include_images=include_images,
                                  include_archived=include_archived, status=status)

    def _pull_ancestors(self, session: Session, ancestors: List[ItemPreviewV1]):
        super()._pull_ancestors(session, ancestors)
        _folder.massage_ancestors(session, self)

    @staticmethod
    def _pull_worksheet_ids(session: Session, workbook_id: str, status: Status, *, get_archived_worksheets=False):
        workbooks_api = WorkbooksApi(session.client)

        @request_safely(action_description=f'gather all Worksheets within Workbook {workbook_id}', status=status)
        def _request_worksheet_ids():
            offset = 0
            limit = 1000
            worksheet_ids = list()
            while True:
                worksheet_output_list = workbooks_api.get_worksheets(
                    workbook_id=workbook_id,
                    is_archived=get_archived_worksheets,
                    offset=offset,
                    limit=limit)  # type: WorksheetOutputListV1

                for worksheet_output in worksheet_output_list.worksheets:  # type: WorksheetOutputV1
                    worksheet_ids.append(worksheet_output.id)

                if len(worksheet_output_list.worksheets) < limit:
                    break

                offset = offset + limit
            return worksheet_ids

        return _request_worksheet_ids()

    @staticmethod
    def find_by_name(session: Session, workbook_name, workbook_type, folder_id, status) -> Optional[WorkbookOutputV1]:
        @request_safely(action_description=f'find {workbook_type} "{workbook_name}" in folder {folder_id}',
                        additional_errors=[400], status=status)
        def _find_workbook_by_name_safely():
            folders = _search.get_folders(session, content_filter='owner', folder_id=folder_id,
                                          name_equals_filter=workbook_name, types_filter=[workbook_type])

            for content in folders:  # type: WorkbenchSearchResultPreviewV1
                if content.name.lower() == workbook_name.lower() and content.type == workbook_type:
                    if folder_id and len(content.ancestors) > 0 and content.ancestors[-1].id != folder_id:
                        # A workbook in a nested folder that wasn't explicitly requested. Find a different match.
                        continue

                    return Workbook._get_workbook_output(session, content.id)
            return None

        return _find_workbook_by_name_safely()

    def push(self, *, context: WorkbookPushContext, folder_id=None, item_map: ItemMap = None, label=None,
             include_inventory=True):
        self._push_context = context
        status = context.status
        session = context.session

        try:
            self._push_errors = set()

            def _on_error(_error):
                self._push_context.status.log(str(_error), level=logging.ERROR)
                self._push_errors.add(str(_error))

            self._push_context.status.on_error = _on_error
            if item_map is None:
                item_map = ItemMap()

            if len(self.worksheets) == 0:
                raise SPyValueError(f'{self} must have at least one worksheet before pushing')

            # Handle in-place datasource swap mode
            if context.current_params.mode == WorkbookPushMode.IN_PLACE_DATASOURCE_SWAP:
                return self._push_in_place_datasource_swap(context, item_map)

            datasource_output = context.datasource_output

            # When Workbook Templates were originally created, the Data ID was set to the ID of the workbook which has
            # the label appended to it. This made Template pushes incompatible with plain workbooks pushed with a label,
            # which was unintentional. So in v195 and later, we try to push with consistent Data IDs in both cases but
            # we still handle template workbooks that may have been pushed under the old regime.
            data_id_with_label_suffix_maybe = f"[{label}] {self.id}"
            data_id_without_label_suffix = _common.removesuffix(data_id_with_label_suffix_maybe, f" {label}")

            if self.__class__.__name__.endswith('Template'):
                # First try to find the item using the ID directly within the Data ID (pre-v195 style)
                status.log('Looking for existing workbook using legacy Template Data ID format')
                workbook_item = Item.find_item(session, self.id, datasource_output.datasource_class,
                                               datasource_output.datasource_id, data_id_with_label_suffix_maybe,
                                               label=label, status=status)

                if workbook_item is None:
                    # Now try using the new style, which removes the label from the end of the ID and is therefore
                    # compatible with Data IDs pushed in non-template scenarios.
                    status.log('Looking for existing workbook using newer Template Data ID format')
                    workbook_item = Item.find_item(session, self.id, datasource_output.datasource_class,
                                                   datasource_output.datasource_id, data_id_without_label_suffix,
                                                   label=label, status=status)
            else:
                status.log('Looking for existing workbook')
                workbook_item = self.find_me(session, label, datasource_output, status=status)

            if workbook_item is None and self.provenance == Item.CONSTRUCTOR:
                status.log('Looking for existing workbook by name')
                workbook_item = self.find_by_name(session, self.name, self.definition['Workbook Type'], folder_id,
                                                  status)

            workbooks_api = WorkbooksApi(session.client)
            items_api = ItemsApi(session.client)

            props = list()
            existing_worksheet_identifiers = dict()
            workbook_output: Optional[WorkbookOutputV1] = None

            if not workbook_item:
                workbook_input = WorkbookInputV1()
                workbook_input.name = self.definition['Name']
                workbook_input.description = _common.get(self.definition, 'Description')
                workbook_input.folder_id = folder_id if folder_id != _common.PATH_ROOT else None
                workbook_input.owner_id = self.decide_owner(context, item_map, owner=context.current_params.owner)
                workbook_input.type = self['Workbook Type']
                workbook_input.branch_from = _common.get(self.definition, 'Branch From')

                if not context.dry_run:
                    status.log(f'Create new workbook:\n{workbook_input}')
                    workbook_output = workbooks_api.create_workbook(body=workbook_input)  # type: WorkbookOutputV1

                    if session.options.wants_compatibility_with(194):
                        data_id = data_id_with_label_suffix_maybe
                    else:
                        data_id = data_id_without_label_suffix

                    status.log(f'Set workbook properties for Data ID {data_id}')
                    items_api.set_properties(id=workbook_output.id, body=[
                        ScalarPropertyV1(name='Datasource Class', value=datasource_output.datasource_class),
                        ScalarPropertyV1(name='Datasource ID', value=datasource_output.datasource_id),
                        ScalarPropertyV1(name='Data ID', value=data_id),
                        ScalarPropertyV1(name='workbookState', value=_common.DEFAULT_WORKBOOK_STATE)])
                else:
                    status.log(f'[Dry Run] Would create new workbook:\n{workbook_input}')

            else:
                workbook_output = Workbook._get_workbook_output(session, workbook_item.id)  # type: WorkbookOutputV1

                if workbook_output.is_archived:
                    # If the workbook happens to be archived, un-archive it. If you're pushing a new copy it seems
                    # likely you're intending to revive it.
                    if not context.dry_run:
                        status.log(f'Un-archive existing workbook {workbook_output.id}')
                        items_api.set_properties(id=workbook_output.id,
                                                 body=[ScalarPropertyV1(name='Archived', value=False)])
                    else:
                        status.log(f'[Dry Run] Would un-archive existing workbook {workbook_output.id}')

                if (self._push_context.current_params.specific_worksheet_ids is None or
                        len(self._push_context.current_params.specific_worksheet_ids) > 0):
                    existing_worksheet_identifiers = self._get_existing_worksheet_identifiers(workbook_output)

                owner_id = self.decide_owner(context, item_map, owner=context.current_params.owner,
                                             current_owner_id=workbook_output.owner.id)

                self._push_owner_and_location(session, workbook_output, owner_id, folder_id, status,
                                              dry_run=context.dry_run)

            if workbook_output is not None:
                status.put('Pushed Workbook ID', workbook_output.id)

                item_map[self.id] = workbook_output.id

                if context.current_params.access_control:
                    self._push_acl(context, workbook_output.id, item_map)

            if include_inventory:
                results_df = self._push_inventory(
                    item_map=item_map, label=label,
                    datasource_output=datasource_output, workbook_output=workbook_output
                )
                self._push_context.pushed_inventory[self.id] = results_df

            props.append(ScalarPropertyV1(name='Name', value=self.definition['Name']))
            if _common.present(self.definition, 'Description'):
                props.append(ScalarPropertyV1(name='Description', value=self.definition['Description']))
            if _common.present(self.definition, 'workbookState'):
                props.append(ScalarPropertyV1(name='workbookState', value=json.dumps(self.definition['workbookState'])))

            if not context.dry_run:
                status.log(f'Update workbook properties:\n{props}')
                items_api.set_properties(id=workbook_output.id, body=props)
            else:
                status.log(f'[Dry Run] Would update workbook properties:\n{props}')

            if len(set(self.worksheets)) != len(self.worksheets):
                raise SPyValueError('Worksheet list within Workbook "%s" is not unique: %s' % (self, self.worksheets))

            first_worksheet_id = None
            for worksheet in self.worksheets:  # type: Worksheet
                if (self._push_context.current_params.specific_worksheet_ids is not None and
                        worksheet.id not in self._push_context.current_params.specific_worksheet_ids):
                    continue

                if context.dry_run and workbook_output is None:
                    status.log(f'[Dry Run] Would push worksheet "{worksheet.name}" but workbook was not created')
                    continue

                self.update_status('Pushing worksheet', 1)
                worksheet_output = safely(
                    lambda: worksheet.push(context, workbook_output.id, item_map, datasource_output,
                                           existing_worksheet_identifiers, include_inventory, label),
                    action_description=f'push Worksheet "{worksheet.name}" to Workbook {workbook_output.id}',
                    status=status)

                if (not _common.get(worksheet, 'Archived', False) and first_worksheet_id is None
                        and worksheet_output is not None):
                    first_worksheet_id = worksheet_output.id

            dependencies_not_found = set()
            if self._push_context.current_params.specific_worksheet_ids is None:
                if context.dry_run and workbook_output is None:
                    status.log(f'[Dry Run] Would reorder and archive worksheets but workbook was not created')
                else:
                    self._reorder_and_archive_worksheets(context, item_map, workbook_output)

            # Now go back through all the worksheets to see if any worksteps weren't resolved
            for worksheet in self.worksheets:
                if (self._push_context.current_params.specific_worksheet_ids is not None and
                        worksheet.id not in self._push_context.current_params.specific_worksheet_ids):
                    continue

                dependencies_not_found.update(worksheet.find_unresolved_worksteps(item_map))

            if context.current_params.include_annotations and self._annotation is not None:
                self._annotation.push(context, workbook_output.id, workbook_output.id, item_map,
                                      datasource_output, context.current_params.access_control, push_images=True,
                                      label=label)

            if workbook_output is not None:
                link_url = Workbook.construct_url(
                    session,
                    folder_id,
                    workbook_output.id,
                    first_worksheet_id
                )
                status.put('URL', link_url)

            if len(dependencies_not_found) > 0:
                if not context.dry_run:
                    status.warn('Some worksteps could not be resolved during push:\n%s' %
                                '\n'.join(dependencies_not_found))
                    raise SPyDependencyNotFound('\n'.join(dependencies_not_found))
                else:
                    status.log('[Dry Run] Would warn about unresolved workstep dependencies:\n%s' %
                               '\n'.join(dependencies_not_found))

            return workbook_output

        finally:
            self._push_context.status.on_error = None
            self._push_context = None

    def _reorder_and_archive_worksheets(self, context: WorkbookPushContext, item_map: ItemMap,
                                        workbook_output: WorkbookOutputV1):
        session = context.session
        status = context.status
        workbooks_api = WorkbooksApi(session.client)

        # Pull the set of worksheets and re-order them
        maybe_worksheet_ids = Workbook._pull_worksheet_ids(session, workbook_output.id, status)
        remaining_pushed_worksheet_ids = list() if maybe_worksheet_ids is None else maybe_worksheet_ids

        next_worksheet_id = None
        for worksheet in reversed(self.worksheets):
            if context.dry_run and worksheet.id not in item_map:
                # Can't reorder something that wasn't pushed
                status.log(f'[Dry Run] Would reorder worksheets')
                return

            pushed_worksheet_id = item_map[worksheet.id]
            if next_worksheet_id is None:
                safely(lambda: workbooks_api.move_worksheet(workbook_id=workbook_output.id,
                                                            worksheet_id=pushed_worksheet_id),
                       action_description=f'move worksheet {pushed_worksheet_id} to be last in '
                                          f'workbook {workbook_output.id}',
                       status=status, dry_run=context.dry_run)
            else:
                safely(lambda: workbooks_api.move_worksheet(workbook_id=workbook_output.id,
                                                            worksheet_id=pushed_worksheet_id,
                                                            next_worksheet_id=item_map[next_worksheet_id]),
                       action_description=f'move worksheet {pushed_worksheet_id} to be before '
                                          f'{item_map[next_worksheet_id]} in workbook {workbook_output.id}',
                       status=status, dry_run=context.dry_run)

            if pushed_worksheet_id in remaining_pushed_worksheet_ids:
                remaining_pushed_worksheet_ids.remove(pushed_worksheet_id)

            next_worksheet_id = worksheet.id

        # Archive any worksheets that are no longer active
        items_api = ItemsApi(session.client)
        for remaining_pushed_worksheet_id in remaining_pushed_worksheet_ids:
            safely(
                lambda: items_api.archive_item(id=remaining_pushed_worksheet_id,
                                               note='Archived by SPy because the worksheet is no longer '
                                                    'active in the workbook'),
                action_description=f'archive Worksheet {remaining_pushed_worksheet_id} from '
                                   f'Workbook {workbook_output.id}',
                status=status, dry_run=context.dry_run)

    @staticmethod
    def construct_url(session: Session, folder_id, workbook_id, worksheet_id=None):
        base_url = session.public_url + '/'
        url = base_url

        if folder_id is not None:
            url = urljoin(url, f'{folder_id}/')
        url = urljoin(url, f'workbook/{workbook_id}/')
        if worksheet_id is not None:
            url = urljoin(url, f'worksheet/{worksheet_id}')

        return url

    def _get_existing_worksheet_identifiers(self, workbook_output: WorkbookOutputV1) -> dict:
        workbooks_api = WorkbooksApi(self._push_context.session.client)
        items_api = ItemsApi(self._push_context.session.client)
        existing_worksheet_identifiers = dict()
        for is_archived in [False, True]:
            offset = 0
            limit = 1000
            while True:
                worksheet_output_list = safely(
                    lambda: workbooks_api.get_worksheets(workbook_id=workbook_output.id,
                                                         is_archived=is_archived,
                                                         offset=offset,
                                                         limit=limit),
                    action_description=f'get worksheets for workbook {workbook_output.id}',
                    status=self._push_context.status)  # type: WorksheetOutputListV1
                if worksheet_output_list is None:
                    break

                for worksheet_output in worksheet_output_list.worksheets:  # type: WorksheetOutputV1
                    @request_safely(
                        action_description=f'get Data ID for worksheet '
                                           f'{workbook_output.id}/{worksheet_output.id}',
                        status=self._push_context.status)
                    def _add_worksheet_data_id_to_identifiers():
                        item_output = items_api.get_item_and_all_properties(
                            id=worksheet_output.id)  # type: ItemOutputV1
                        data_id = [p.value for p in item_output.properties if p.name == 'Data ID']
                        spy_id = [p.value for p in item_output.properties if p.name == 'SPy ID']
                        # This is for backward compatibility with worksheets that had been pushed by SPy with a
                        # Data ID. (We switched to "SPy ID" because there's no use in using the Datasource Class
                        # / Datasource ID / Data ID triplet when you can't actually search on it.)
                        if len(data_id) != 0:
                            self._push_context.status.log(
                                f'Worksheet "{worksheet_output.name}" ({worksheet_output.id}) has Data ID {data_id[0]}')
                            existing_worksheet_identifiers[data_id[0]] = worksheet_output.id
                        elif len(spy_id) != 0:
                            self._push_context.status.log(
                                f'Worksheet "{worksheet_output.name}" ({worksheet_output.id}) has SPy ID {spy_id[0]}')
                            existing_worksheet_identifiers[spy_id[0]] = worksheet_output.id

                    existing_worksheet_identifiers[worksheet_output.id] = worksheet_output.id
                    existing_worksheet_identifiers[worksheet_output.name] = worksheet_output.id
                    _add_worksheet_data_id_to_identifiers()

                if len(worksheet_output_list.worksheets) < limit:
                    break

                offset = offset + limit

        return existing_worksheet_identifiers

    def _push_inventory(
            self, *, item_map: ItemMap, label, datasource_output, workbook_output
    ) -> Optional[pd.DataFrame]:
        references_exist = self._do_references_exist()

        metadata_to_push = dict()
        for item in self.item_inventory.values():
            if item is None or item['Type'] in ['Folder']:
                continue

            if item.id in item_map:
                continue

            # noinspection PyBroadException
            try:
                item_exists, item_search_preview = references_exist.get(item.id, (ItemExists.MAYBE, None))
                workbook_output_id = workbook_output.id if workbook_output is not None else None
                to_push = item.get_metadata_to_push(
                    self._push_context, self._push_context.datasource_maps, datasource_output, self.item_inventory,
                    pushed_workbook_id=workbook_output_id, item_map=item_map, label=label, item_exists=item_exists,
                    item_search_preview=item_search_preview
                )

                if to_push is not None:
                    metadata_to_push[item.id] = to_push
                else:
                    self.update_status('Pushing item inventory', 1)
            except KeyboardInterrupt:
                raise
            except SPyDependencyNotFound as e:
                if not e.intentional_no_mapping:
                    self._push_context.status.on_error(e)
                else:
                    self._push_context.status.log(str(e), level=logging.INFO)
            except Exception:
                # Note: This universal catch is more permissive than the newer CRAB-30955 error handling so this
                #  is kept for backwards compatibility
                self._push_context.status.on_error(f'Error processing {item}:\n{_common.format_exception()}')

        if len(metadata_to_push) == 0:
            return None

        results_df = self._push_accumulated_inventory_metadata(metadata_to_push, item_map, datasource_output)
        if results_df is None:
            return None

        for index, row in results_df.iterrows():
            if _common.get(row, 'Push Result') == 'Success':
                item_map[index] = row['ID']
                if _common.get(row, 'Dummy Item'):
                    item_map.add_dummy_item(row)
                self.update_status('Pushing item inventory', 1)

        if results_df.spy.friendly_error_string is not None:
            self._push_context.status.on_error(results_df.spy.friendly_error_string)

        return results_df

    def _do_references_exist(self):
        raw_references = self.referenced_items
        self._push_context.status.log(f'Attempting to find {len(raw_references)} existing items by ID')
        references = Workbook._fill_in_item_search_preview_on_references(self._push_context.status, raw_references)
        items_api = ItemsApi(self._push_context.session.client)
        item_exists: Dict[str, Tuple[ItemExists, Optional[ItemSearchPreviewV1]]] = dict()
        for reference in references:
            if reference.item_search_preview is not None:
                item_exists[reference.id] = (ItemExists.YES, reference.item_search_preview)
                continue
            elif reference.id in self.item_inventory:
                # Due to CRAB-40580, we have to do an extra check when this is a swap item
                item = self.item_inventory.get(reference.id)
                if 'Swap Key' in item:
                    try:
                        self._push_context.status.log(f'Checking existence of swap item {reference.id} explicitly')
                        if items_api.get_item_and_all_properties(id=reference.id) is not None:
                            item_exists[reference.id] = (ItemExists.YES, None)
                            continue
                    except ApiException:
                        pass

            if _version.is_sdk_module_version_at_least(62):
                item_exists[reference.id] = (ItemExists.NO, None)
            else:
                item_exists[reference.id] = (ItemExists.MAYBE, None)
        return item_exists

    def _push_accumulated_inventory_metadata(self, metadata_to_push: Dict[str, Dict],
                                             item_map: ItemMap, datasource_output) -> Optional[pd.DataFrame]:
        new_metadata = dict()
        dependency_problems: Dict[object, SPyDependencyNotFound] = dict()

        def _replace(_dict, _key, _old_id):
            if _old_id in item_map:
                _dict[_key] = item_map[_old_id]
            elif _old_id in metadata_to_push:
                _dict[_key] = {'Data ID': metadata_to_push[_old_id]['Data ID']}
            elif _common.is_guid(_old_id):
                _missing = self.item_inventory.get(_old_id)
                _friendly = str(_missing) if _missing is not None else _old_id
                if _old_id in self._push_context.intentional_no_mappings:
                    raise SPyDependencyNotFound(
                        f'Formula dependency ${_key}={_friendly} intentionally not found/mapped/pushed',
                        item_id, _old_id, intentional_no_mapping=True)
                else:
                    raise SPyDependencyNotFound(
                        f'Formula dependency ${_key}={_friendly} not found/mapped/pushed', item_id, _old_id)

        data_id_maps = dict()
        for item_id, item_dict in metadata_to_push.items():
            new_dict = copy.deepcopy(item_dict)

            if 'Parent ID' in item_dict and 'Parent Data ID' not in item_dict:
                parent_dict = metadata_to_push.get(item_dict['Parent ID'])
                if parent_dict is not None:
                    if (item_dict.get('Datasource Class') == datasource_output.datasource_class and
                            item_dict.get('Datasource ID') == datasource_output.datasource_id and
                            parent_dict.get('Datasource Class') == datasource_output.datasource_class and
                            parent_dict.get('Datasource ID') == datasource_output.datasource_id):
                        new_dict['Parent Data ID'] = parent_dict['Data ID']

            data_key = new_dict.get('Datasource Class'), new_dict.get('Datasource ID'), new_dict.get('Data ID')
            if data_key in data_id_maps:
                error_message = (f'Data ID {data_key} collision:\n'
                                 f'{json.dumps(new_dict, indent=2)}\n{json.dumps(data_id_maps[data_key], indent=2)}')
                self._push_context.status.on_error(error_message)

            data_id_maps[data_key] = new_dict

            if 'Formula Parameters' not in new_dict:
                new_metadata[item_id] = new_dict
                continue

            try:
                param_dict = new_dict['Formula Parameters']
                simplified_type = (new_dict['Type'].replace('Calculated', '').replace('Stored', '')
                                   .replace('Threshold', ''))
                if simplified_type in ['Signal', 'Condition', 'Scalar', 'Chart']:
                    for k, v in param_dict.items():
                        _replace(param_dict, k, v)
                elif simplified_type in ['Metric']:
                    if 'Bounding Condition' in param_dict:
                        _replace(param_dict, 'Bounding Condition', param_dict['Bounding Condition'])
                    if 'Measured Item' in param_dict:
                        _replace(param_dict, 'Measured Item', param_dict['Measured Item'])
                    if 'Thresholds' in param_dict:
                        for threshold in param_dict['Thresholds']:
                            if 'Item ID' in threshold:
                                _replace(threshold, 'Item ID', threshold['Item ID'])

                new_metadata[item_id] = copy.deepcopy(new_dict)
            except SPyDependencyNotFound as e:
                item_map.log(item_id, str(e))
                if e.intentional_no_mapping:
                    # Log at WARN level for items that depend on intentionally unmapped items
                    self._push_context.status.log(
                        f'{_common.repr_from_row(self.item_inventory[item_id])}: {e}\n'
                        f'Item will not be pushed because it depends on an item that was intentionally not mapped.',
                        level=logging.WARNING)
                else:
                    # Keep track of unintentional dependency problems for error reporting
                    dependency_problems[item_id] = SPyDependencyNotFound(
                        f'{_common.repr_from_row(self.item_inventory[item_id])}: {e}',
                        e.dependent_identifier,
                        e.dependency_identifier)

        if len(dependency_problems) > 0:
            self._push_context.status.on_error(SPyDependencyNotFound.generate_error_string(dependency_problems))

        metadata_df = pd.DataFrame.from_dict(new_metadata, orient='index')

        if self._push_context.dry_run:
            self._push_context.status.log(f'[Dry Run] Would push {len(new_metadata)} metadata items:\n'
                                          f'{metadata_df.to_string()}')
            return None

        workbook_context = WorkbookContext()
        if isinstance(self, Analysis):
            workbook_context.workbook_object = Analysis(copy.deepcopy(self.definition_dict))
        else:
            workbook_context.workbook_object = Topic(copy.deepcopy(self.definition_dict))
        workbook_context.workbook_object['ID'] = item_map[self.id]

        self._push_context.status.log(f'Pushing {len(new_metadata)} metadata item(s):\n'
                                      f'{metadata_df.to_string()}')

        inner_status = self._push_context.status.create_inner('Push accumulated metadata', errors='catalog')
        return _metadata.push(self._push_context.session, metadata_df, workbook_context, datasource_output,
                              inner_status,
                              cleanse_data_ids=self._push_context.current_params.reconcile_inventory_by == 'name',
                              default_to_local=False, validate_ui_configs=False)

    def _push_in_place_datasource_swap(self, context: WorkbookPushContext, item_map: ItemMap):
        """
        Handles push in 'in-place datasource swap' mode.
        Only pushes minimal changes: inventory (with datasource swaps), worksteps, and annotations if changed.
        """
        status = context.status
        session = context.session

        status.log('Pushing via "in-place datasource swap" mode')

        status.put('Pushed Workbook ID', self.id)

        # For in-place mode, we don't create any datasource since datasource parameter must be None
        # We get the datasource from the existing workbook/items
        datasource_output = None

        # This step will end up only processing StoredItems and filling the item_map. CalculatedItems will
        # be skipped unless they are explicitly mapped in a Datasource Map override.
        # Create a minimal workbook_output-like object with the existing workbook ID to ensure
        # pushed_workbook_id is correctly set for item scope checking downstream
        workbook_output_stub = SimpleNamespace(id=self.id)
        pushed_inventory_df = self._push_inventory(
            item_map=item_map,
            label=None,
            datasource_output=datasource_output,
            workbook_output=workbook_output_stub
        )
        self._push_context.pushed_inventory[self.id] = pushed_inventory_df

        # Now we handle non-mapped CalculatedItems and ThresholdMetrics for datasource swap by running
        # through the inventory again and updating their formula parameters (or equivalent for ThresholdMetrics).
        self._push_in_place_datasource_swap_calculated_items(context, item_map)

        # Push worksteps only (skip workbook and worksheet updates)
        for worksheet in self.worksheets:
            self._push_in_place_datasource_swap_worksheet(context, self, worksheet, item_map)

        # Push annotations if they have changed (handled in worksheet/workstep push)
        if context.current_params.include_annotations and self._annotation is not None:
            status.log(f'Pushing workbook-level annotation for {self}')
            self._annotation.push(context, self.id, self.id, item_map,
                                  datasource_output, context.current_params.access_control, push_images=False,
                                  label=None)

        # Construct URL for the workbook
        link_url = Workbook.construct_url(session, None, self.id, None)
        status.put('URL', link_url)

    def _push_in_place_datasource_swap_worksheet(self, context: WorkbookPushContext, workbook, worksheet, item_map):
        """
        Pushes only the worksteps and annotations for a worksheet in in-place mode.
        Skips worksheet creation/update.
        """
        status = context.status
        session = context.session
        workbooks_api = WorkbooksApi(session.client)

        if isinstance(worksheet, WorksheetForAnalysisOrRoom):
            status.log(f'Processing worksteps for {worksheet}')

            pushed_current_workstep_id = None

            try:
                # We freeze the replace patterns here because otherwise we unnecessarily recompile the replacement
                # regexes when the workstep IDs are added to the item map, even though worksteps never refer to other
                # worksteps.
                item_map.freeze_replace_patterns()

                for workstep_id, workstep in worksheet.worksteps.items():
                    self.update_status('Pushing worksteps', 0)

                    pushed_workstep_id = workstep.push_to_specific_worksheet(
                        context, workbook.id, worksheet.id,
                        item_map, include_inventory=False, no_workstep_message=True
                    )

                    self.update_status('Pushing worksteps', 1)

                    # Store the workstep mapping
                    if worksheet.id not in item_map.workstep_mappings:
                        item_map.workstep_mappings[worksheet.id] = dict()
                    item_map.workstep_mappings[worksheet.id][workstep_id] = pushed_workstep_id

                    if workstep_id == worksheet.definition['Current Workstep ID']:
                        pushed_current_workstep_id = pushed_workstep_id
            finally:
                item_map.unfreeze_replace_patterns()

            # Set the current workstep if needed
            if pushed_current_workstep_id and not context.dry_run:
                workbooks_api.set_current_workstep(
                    workbook_id=workbook.id,
                    worksheet_id=worksheet.id,
                    workstep_id=pushed_current_workstep_id
                )

        # Push worksheet-level annotations if they exist
        if context.current_params.include_annotations and worksheet.annotation is not None:
            status.log(f'Processing worksheet-level annotation for {worksheet}')
            worksheet.annotation.push(context, workbook.id, worksheet.id, item_map,
                                      None, context.current_params.access_control, push_images=False, label=None)

    def _push_in_place_datasource_swap_calculated_items(self, context: WorkbookPushContext, item_map: ItemMap):
        """
        Updates formula parameters for calculated items during in-place datasource swap mode.
        Handles ThresholdMetrics and Charts differently using their specific APIs.
        """
        status = context.status
        session = context.session
        items_api = ItemsApi(session.client)
        metrics_api = MetricsApi(session.client)
        formulas_api = FormulasApi(session.client)

        status.log('Updating calculated item formula parameters for datasource swap')

        for item_id, item in self.item_inventory.items():
            if not isinstance(item, CalculatedItem):
                continue

            # Skip if already mapped (means it was explicitly mapped in datasource map override)
            if item_id in item_map and item_map[item_id] != item_id:
                status.log(f'Skipping {item} - already explicitly mapped')
                continue

            if context.current_params.global_inventory == 'do not touch' and _common.get(item, 'Scoped To') is None:
                status.log(f'Skipping global {item} -- global_inventory set to "do not touch"')
                continue

            formula_params = item.get('Formula Parameters')
            if not formula_params:
                continue

            # Map the formula parameters to new IDs
            formula_params_str = json.dumps(formula_params)
            mapped_params_str = item_map.replace_items(formula_params_str)
            if formula_params_str == mapped_params_str:
                status.log(f'No formula parameter changes for {item} -- skipping')
                continue

            if _common.get(item, 'Scoped To') is None:
                if context.dry_run:
                    status.log(f'[Dry Run] Global would be modified: {item}', level=logging.WARNING)
                else:
                    status.log(f'Global being modified: {item}', level=logging.WARNING)

            mapped_params = json.loads(mapped_params_str)

            try:
                if isinstance(item, ThresholdMetric):
                    # Handle ThresholdMetrics differently
                    threshold_metric_input = ThresholdMetricInputV1()

                    # First populate basic fields like name, description, etc. from the item
                    _metadata.dict_to_threshold_metric_input(item.definition_dict, threshold_metric_input)

                    # Then fill in the formula parameters (already mapped)
                    _metadata.fill_in_threshold_metric_input_from_formula_parameters(
                        threshold_metric_input, mapped_params)

                    if not context.dry_run:
                        _metadata._put_threshold_metric(metrics_api, item_id, threshold_metric_input)
                        status.log(f'Updated {item}')
                    else:
                        status.log(f'[Dry Run] Would update {item}')
                elif isinstance(item, Chart):
                    # Handle Chart/Function items using FormulasApi
                    function_input = FunctionInputV1()

                    # Populate basic fields like name, description, etc. from the item
                    _metadata.dict_to_function_input(item.definition_dict, function_input)

                    # Set the formula
                    formula = item.get('Formula')
                    if formula:
                        function_input.formula = Item.formula_string_from_list(formula) if isinstance(formula,
                                                                                                      list) else formula

                    # Build the parameters list
                    function_input.parameters = []
                    for param_name, param_value in mapped_params.items():
                        if _common.is_guid(param_value):
                            # It's an item ID reference
                            function_input.parameters.append(FormulaParameterInputV1(name=param_name, id=param_value))
                        else:
                            # It's a formula string
                            function_input.parameters.append(FormulaParameterInputV1(
                                name=param_name, formula=param_value, unbound=True))

                    if not context.dry_run:
                        formulas_api.update_function(id=item_id, body=function_input)
                        status.log(f'Updated {item}')
                    else:
                        status.log(f'[Dry Run] Would update {item}')
                else:
                    # Handle regular calculated items (Signals, Conditions, Scalars)
                    formula = item.get('Formula')
                    if formula:
                        formula_str = Item.formula_string_from_list(formula) if isinstance(formula, list) else formula

                        # Convert mapped_params dict to list of "param_name=param_value" strings
                        params_list = [f'{k}={v}' for k, v in mapped_params.items()]
                        params_list.sort(key=lambda p: p.split('=')[0])

                        if not context.dry_run:
                            items_api.set_formula(id=item_id, body=FormulaUpdateInputV1(
                                formula=formula_str, parameters=params_list))
                            status.log(f'Updated formula parameters for {item}')
                        else:
                            status.log(f'[Dry Run] Would update formula parameters for {item}')
            except Exception as e:
                message = f'Error updating {item}: {str(e)}'
                status.log(message, level=logging.ERROR)
                self._push_errors.add(message)

    def _create_folder_path_if_necessary(self, context: WorkbookPushContext, path: str, owner_id: str):
        session = context.session
        status = context.status

        if path == _folder.ORIGINAL_FOLDER:
            status.log('"path" argument is spy.workbooks.ORIGINAL_FOLDER; recreating original folder path')
            return _folder.ORIGINAL_FOLDER

        if _common.is_guid(path):
            status.log(f'"path" argument is a folder ID; using folder ID {path} directly')
            return path

        folders_api = FoldersApi(session.client)

        if path is None:
            status.log(
                '"path" argument is None; the workbook will stay where it is (if it has already been pushed once)')
            return None

        path = path.strip()

        if not path:
            status.log(
                '"path" argument is empty; the workbook will stay where it is (if it has already been pushed once)')
            return None

        workbook_path = _common.path_string_to_list(path)

        status.log(f'Creating folder path "{path}" if it does not already exist')

        parent_id = None
        folder_id = None
        folder_filter = 'owner'
        for i in range(0, len(workbook_path)):
            existing_content_id = None
            content_name = workbook_path[i]

            if content_name in [_folder.PUBLIC, _folder.SHARED_OR_PUBLIC, _folder.SHARED, _folder.ALL, _folder.USERS]:
                raise SPyRuntimeError(f'"path" argument cannot contain {content_name} folder in "{path}"')

            if content_name == _folder.CORPORATE:
                if not session.corporate_folder:
                    raise SPyRuntimeError(f'Attempting to push to Corporate folder but user does not have access')

                if i > 0:
                    raise SPyRuntimeError(f'"{content_name}" is an illegal name for a subfolder')

                parent_id = session.corporate_folder.id
                folder_id = session.corporate_folder.id
                folder_filter = 'corporate'
                continue
            elif content_name == _folder.MY_FOLDER:
                if i > 0:
                    raise SPyRuntimeError(f'"{content_name}" is an illegal name for a subfolder')

                if owner_id == session.user.id:
                    parent_id = session.my_folder.id
                else:
                    user_folder = _folder.create_user_folder_if_necessary(context, owner_id)
                    if user_folder is None:
                        # This can happen in a dry run where the user folder needs to be created
                        return None

                    parent_id = user_folder.id

                folder_id = parent_id
                continue

            kwargs = {
                'filter': folder_filter,
                'types': [SeeqNames.Types.folder],
                'text_search': content_name,
                'is_exact': True,
                'limit': session.options.search_page_size,
            }

            if parent_id:
                kwargs['folder_id'] = parent_id

            if owner_id and owner_id != session.user.id:
                kwargs['user_id'] = owner_id

            folders = safely(lambda: folders_api.get_folders(**kwargs),
                             action_description=f'get Folders using filter "{folder_filter}" and name "{content_name}" '
                                                f'within {parent_id} for user_id {owner_id}',
                             additional_errors=[400],
                             status=status)  # type: WorkbenchItemOutputListV1

            if folders is not None:
                for content in folders.content:  # type: WorkbenchSearchResultPreviewV1
                    if content.type == 'Folder' and content_name == content.name:
                        if parent_id is not None:
                            # When parent_id is specified, ensure the folder's parent matches
                            if content.ancestors is not None and len(content.ancestors) >= 1 and content.ancestors[-1].id != parent_id:
                                continue
                        else:
                            # When parent_id is None (root level), ensure the folder is at the root level by checking
                            # it has minimal nesting (typically just the user home folder as ancestor).
                            # Skip folders that are nested deeper (e.g., within other user-created folders).
                            if content.ancestors is not None and len(content.ancestors) > 1:
                                # This folder is nested deeper than the root level. Skip it.
                                continue

                        status.log(f'Found existing Folder "{content.name}" ({content.id}) under parent ID '
                                   f'{parent_id} for owner ID {owner_id}')
                        existing_content_id = content.id
                        break

            if not existing_content_id:
                folder_input = FolderInputV1()
                folder_input.name = content_name
                folder_input.description = 'Created by Seeq Data Lab'
                folder_input.owner_id = owner_id
                folder_input.parent_folder_id = parent_id

                if not context.dry_run:
                    _folder.check_for_reserved_folder_name(folder_input.name)
                    folder_output = safely(lambda: folders_api.create_folder(body=folder_input),
                                           action_description=f'create Folder {folder_input.name}',
                                           status=status)  # type: FolderOutputV1
                    if folder_output is not None:
                        existing_content_id = folder_output.id
                        status.log(
                            f'Created Folder "{folder_output.name}" under parent ID {parent_id} for owner ID {owner_id}')
                else:
                    status.log(
                        f'[Dry Run] Would create Folder "{folder_input.name}" under parent ID {parent_id} for owner ID {owner_id}')
                    return None

            parent_id = existing_content_id
            folder_id = existing_content_id

        return folder_id

    def push_containing_folders(self, context: WorkbookPushContext, item_map: ItemMap, use_full_path,
                                path, owner, label, access_control) -> Tuple[Optional[str], Optional[str]]:
        session = context.session
        status = context.status

        owner_id = session.user.id
        if owner is not None:
            owner_id = self.decide_owner(context, item_map, owner=owner)

        parent_folder_id = self._create_folder_path_if_necessary(context, path, owner_id)
        search_folder_id = parent_folder_id

        if 'Ancestors' not in self:
            if parent_folder_id != _folder.ORIGINAL_FOLDER:
                status.log('No Ancestors information available to push containing folders; '
                           'skipping folder creation.')
                return search_folder_id, parent_folder_id
            else:
                status.log('No Ancestors information available to push containing folders; '
                           'preserving existing location.')
                return None, None

        keep_skipping = parent_folder_id in self['Ancestors']
        create_folders_now = False
        skip_next = False
        if parent_folder_id == _folder.ORIGINAL_FOLDER:
            parent_folder_id = None
            keep_skipping = False
            create_folders_now = True

        for ancestor_id in self['Ancestors']:
            if skip_next:
                skip_next = False
                continue

            if keep_skipping and parent_folder_id == ancestor_id:
                keep_skipping = False
                status.log(f'Skipping creation of ancestor folder {ancestor_id}; it is the existing parent folder.')
                continue

            if not create_folders_now and (use_full_path or 'Search Folder ID' not in self):
                status.log(f'Reifying folders from {ancestor_id} down')
                create_folders_now = True

            if create_folders_now:
                if ancestor_id == _folder.CORPORATE:
                    if parent_folder_id is not None:
                        status.log(f'Skipping {ancestor_id} folder level; parent path has been specified')
                        continue

                    if not session.corporate_folder:
                        raise SPyRuntimeError(f'Attempting to push to Corporate folder but user does not have access')
                    status.log(f'Mapping {ancestor_id} to Corporate folder')
                    parent_folder_id = session.corporate_folder.id
                elif ancestor_id in (_folder.ALL, _folder.SHARED_OR_PUBLIC, _folder.SHARED,
                                     _folder.PUBLIC, _folder.MY_FOLDER):
                    if parent_folder_id is not None:
                        status.log(f'Skipping {ancestor_id} folder level; parent path has been specified')
                    else:
                        status.log(f'Root folder is {ancestor_id}; mapping to user home folder')
                    continue
                elif ancestor_id == _folder.USERS:
                    if parent_folder_id is not None:
                        status.log(f'Skipping {ancestor_id} folder level; parent path has been specified')

                        # The next ancestor is the user's home folder, which we shouldn't look at if the user
                        # specified a path argument
                        skip_next = True
                        continue

                    # We'll fall through to the next clause to map to an actual User home folder
                    status.log(f"Skipping {ancestor_id} folder level; mapping to owner's home folder")
                    parent_folder_id = _folder.USERS
                    continue
                elif ancestor_id in self.item_inventory:
                    folder = self.item_inventory[ancestor_id]  # type: Folder

                    if parent_folder_id == _folder.USERS:
                        # In this case, we are pushing to the owner's home folder (as specified by the owner argument)
                        # We ignore the ancestor_id and just retrieve the home folder directly.
                        if owner_id == session.user.id:
                            parent_folder = session.my_folder
                        else:
                            parent_folder = _folder.create_user_folder_if_necessary(context, owner_id)

                        if not context.dry_run and parent_folder is None:
                            owner_reference = f'{owner} ({owner_id})' if owner is not None else owner_id
                            raise SPyRuntimeError(
                                f'Home folder for owner "{owner_reference}" '
                                'does not exist on the target server. Cannot push.'
                            )

                        status.log(f'Mapped owner\'s {folder} to "{parent_folder.name}" ({parent_folder.id})')
                        parent_folder_id = parent_folder.id
                        continue

                    status.log(
                        f'Creating ancestor {folder} under parent folder ID {parent_folder_id}')
                    parent_folder = folder.push(context, parent_folder_id, context.datasource_output,
                                                item_map, owner=owner, label=label)

                    if parent_folder is None:
                        continue

                    parent_folder_id = parent_folder.id

            elif not create_folders_now and self['Search Folder ID'] == ancestor_id:
                status.log(f'Reifying folders from {ancestor_id} down because it is the "Search Folder ID" (a property '
                           f'on the workbook).')
                create_folders_now = True
            else:
                status.log(f'Skipping creation of ancestor folder {ancestor_id} as it already exists in target '
                           f'location.')

        status.log(f'Final parent folder ID for workbook is {parent_folder_id}')
        return search_folder_id, parent_folder_id

    @property
    def referenced_items(self) -> List[Reference]:
        referenced_items = self._get_worksheet_references()

        if self.item_inventory is not None:
            for item in self.item_inventory.values():
                if item['Type'] == 'Folder':
                    continue
                if item['ID'] not in referenced_items:
                    referenced_items[item['ID']] = Reference(item['ID'], Reference.INVENTORY)

        return list(referenced_items.values())

    def _get_worksheet_references(self) -> Dict[str, Reference]:
        references = dict()
        for worksheet in self.worksheets:
            for reference in worksheet.referenced_items:
                references[reference.id] = reference

        return references

    def referenced_items_df(self):
        unique_ids = {r.id for r in self.referenced_items}
        return pd.DataFrame([self.item_inventory[_id].definition_dict for _id in unique_ids])

    @property
    def referenced_workbooks(self):
        references = dict()
        for worksheet in self.worksheets:
            for (workbook_id, worksheet_id, workstep_id) in worksheet.referenced_worksteps:
                if workbook_id not in references:
                    references[workbook_id] = set()

                references[workbook_id].add((workbook_id, worksheet_id, workstep_id))

        return references

    def find_workbook_links(self, session: Session, status: Status):
        # This should only be called during a pull operation, because it requires a connection to the original
        # database in order to resolve the workbook in a view-only link. (See Annotation class.)
        links = dict()
        for worksheet in self.worksheets:
            links.update(worksheet.find_workbook_links(session, status))

        return links

    def _get_default_workbook_folder(self):
        return os.path.join(os.getcwd(), 'Workbook_%s' % self.id)

    @staticmethod
    def _get_workbook_json_file(workbook_folder):
        return os.path.join(workbook_folder, 'Workbook.json')

    @staticmethod
    def _get_items_json_file(workbook_folder):
        return os.path.join(workbook_folder, 'Items.json')

    @staticmethod
    def _get_datasources_json_file(workbook_folder):
        return os.path.join(workbook_folder, 'Datasources.json')

    @staticmethod
    def _get_datasource_map_json_file(workbook_folder, datasource_map):
        return os.path.join(
            workbook_folder, util.cleanse_filename(
                'Datasource_Map_%s_%s_%s.json' % (datasource_map['Datasource Class'],
                                                  datasource_map['Datasource ID'],
                                                  datasource_map['Datasource Name'])))

    def save(self, workbook_folder=None, *, overwrite=False, include_rendered_content=False,
             pretty_print_html=False):
        if not workbook_folder:
            workbook_folder = self._get_default_workbook_folder()

        if util.safe_exists(workbook_folder):
            if overwrite:
                for root, dirs, files in util.safe_walk(workbook_folder):
                    for _file in files:
                        util.safe_remove(os.path.join(root, _file))
                    for _dir in dirs:
                        util.safe_rmtree(os.path.join(root, _dir))
            else:
                raise SPyRuntimeError('"%s" folder exists. Use shutil.rmtree to remove it, but be careful not to '
                                      'accidentally delete your work!' % workbook_folder)

        util.safe_makedirs(workbook_folder, exist_ok=True)

        workbook_json_file = Workbook._get_workbook_json_file(workbook_folder)

        definition_dict = self.definition_dict
        definition_dict['Worksheets'] = list()
        for worksheet in self.worksheets:
            worksheet.save(workbook_folder, include_rendered_content=include_rendered_content,
                           pretty_print_html=pretty_print_html)
            definition_dict['Worksheets'].append(worksheet.id)

        if include_rendered_content:
            _render.toc(self, workbook_folder)

        with util.safe_open(workbook_json_file, 'w', encoding='utf-8') as f:
            json.dump(definition_dict, f, indent=4, sort_keys=True, cls=ItemJSONEncoder)

        items_json_file = Workbook._get_items_json_file(workbook_folder)
        with util.safe_open(items_json_file, 'w', encoding='utf-8') as f:
            json.dump(self.item_inventory, f, indent=4, sort_keys=True, cls=ItemJSONEncoder)

        datasources_json_file = Workbook._get_datasources_json_file(workbook_folder)
        clean_datasource_inventory = {
            (Workbook.NULL_DATASOURCE_STRING if k is None else k): v for k, v in self.datasource_inventory.items()
        }
        with util.safe_open(datasources_json_file, 'w', encoding='utf-8') as f:
            json.dump(clean_datasource_inventory, f, indent=4, sort_keys=True, cls=ItemJSONEncoder)

        for datasource_map in self.datasource_maps:
            datasource_map_file = Workbook._get_datasource_map_json_file(workbook_folder, datasource_map)
            with util.safe_open(datasource_map_file, 'w', encoding='utf-8') as f:
                map_to_save = datasource_map.copy()
                map_to_save.pop('File', None)
                map_to_save.pop('Override', None)
                json.dump(map_to_save, f, indent=4)

        if len(self._pull_errors) > 0:
            pull_errors_file = os.path.join(workbook_folder, 'Pull Errors.json')
            with util.safe_open(pull_errors_file, 'w', encoding='utf-8') as f:
                json.dump(list(self._pull_errors), f, indent=4)

        Workbook.save_push_errors(workbook_folder, self._push_errors)

        # Put the final "complete" file in place in a relatively atomic way so that if the save gets interrupted we
        # know whether the folder is complete and can be trusted (or not)
        open(os.path.join(workbook_folder, 'Complete'), 'w').close()

    @staticmethod
    def load_push_errors(workbook_folder):
        push_errors_file = os.path.join(workbook_folder, 'Push Errors.json')
        if not util.safe_exists(push_errors_file):
            return list()

        with util.safe_open(push_errors_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_push_errors(workbook_folder, push_errors):
        if len(push_errors) > 0:
            push_errors_file = os.path.join(workbook_folder, 'Push Errors.json')
            with util.safe_open(push_errors_file, 'w', encoding='utf-8') as f:
                json.dump(list(push_errors), f, indent=4)

    @staticmethod
    def load(workbook_folder):
        if not util.safe_exists(workbook_folder):
            raise SPyRuntimeError('Workbook folder "%s" does not exist' % workbook_folder)

        workbook_json_file = Workbook._get_workbook_json_file(workbook_folder)
        if not util.safe_exists(workbook_json_file):
            raise SPyRuntimeError('Workbook JSON file "%s" does not exist' % workbook_json_file)

        with util.safe_open(workbook_json_file, 'r', encoding='utf-8') as f:
            definition = json.load(f)

        workbook = Workbook._instantiate(definition, provenance=Item.LOAD)
        workbook._load(workbook_folder)

        pull_errors_file = os.path.join(workbook_folder, 'Pull Errors.json')
        if util.safe_exists(pull_errors_file):
            with util.safe_open(pull_errors_file, 'r', encoding='utf-8') as f:
                workbook._pull_errors = set(json.load(f))

        push_errors_file = os.path.join(workbook_folder, 'Push Errors.json')
        if util.safe_exists(push_errors_file):
            with util.safe_open(push_errors_file, 'r', encoding='utf-8') as f:
                workbook._push_errors = set(json.load(f))

        return workbook

    def _load(self, workbook_folder):
        self.worksheets = WorksheetList(self)
        for worksheet_id in self.definition['Worksheets']:
            Worksheet.load_from_workbook_folder(self, workbook_folder, worksheet_id)

        del self._definition['Worksheets']

        self._item_inventory = Workbook._load_inventory(Workbook._get_items_json_file(workbook_folder))

        self._datasource_inventory = Workbook._load_inventory(Workbook._get_datasources_json_file(workbook_folder))
        self._datasource_maps = Workbook.load_datasource_maps(workbook_folder)

    @staticmethod
    def load_datasource_maps(folder, *, overrides: bool = False, status: Optional[Status] = None) -> DatasourceMapList:
        if not util.safe_exists(folder):
            raise SPyRuntimeError('Datasource map folder "%s" does not exist' % folder)

        folder_escaped = glob.escape(folder)
        datasource_map_files = util.safe_glob(os.path.join(folder_escaped, 'Datasource_Map_*.json'))
        datasource_maps = DatasourceMapList()
        for datasource_map_file in datasource_map_files:
            with util.safe_open(datasource_map_file, 'r', encoding='utf-8') as f:
                try:
                    datasource_map = json.load(f)
                except json.JSONDecodeError as e:
                    raise SPyRuntimeError(f'Error reading datasource map JSON file {datasource_map_file}:\n{e}')

                datasource_map['File'] = datasource_map_file

                # Specifying Override = True causes the StoredItem push code to try to look up an item based on the map
                # instead of directly using the item's ID. This allows for pulling a workbook and then pushing it with a
                # datasource map to swap the items within it.
                if overrides:
                    datasource_map['Override'] = True

                if datasource_map in datasource_maps:
                    other_datasource_map = datasource_maps.get(datasource_map["Datasource Class"], datasource_map[
                        "Datasource ID"])
                    raise SPyRuntimeError(f'Duplicate datasource map for Datasource Class '
                                          f'{datasource_map["Datasource Class"]} and {datasource_map["Datasource ID"]}:'
                                          f'\n{datasource_map_file}\n{other_datasource_map["File"]}')

                if status is not None:
                    status.log(f'Loaded {"override" if overrides else "non-override"} datasource map from '
                               f'{datasource_map_file}')

                datasource_maps.append(datasource_map)

        return datasource_maps

    @staticmethod
    def _load_inventory(file_name):
        with util.safe_open(file_name, 'r', encoding='utf-8') as f:
            loaded_inventory = json.load(f)

        inventory_dict = dict()
        for item_id, item_def in loaded_inventory.items():
            if item_id == Workbook.NULL_DATASOURCE_STRING:
                item_id = None
            inventory_dict[item_id] = Item.load(item_def)

        return inventory_dict

    def _scrape_datasource_inventory(self, session: Session):
        referenced_datasources: Dict[str, Union[DatasourceOutputV1, DatasourcePreviewV1]] = dict()
        referenced_datasources.update(self._scrape_auth_datasources(session))
        for item in self.item_inventory.values():  # type: Item
            referenced_datasources.update(item._scrape_auth_datasources(session))
            if item.datasource:
                referenced_datasources[item.datasource.id] = item.datasource

        self._datasource_inventory = dict()
        for datasource in referenced_datasources.values():
            self.datasource_inventory[datasource.id] = Datasource.from_datasource_output(datasource)

    def _construct_default_datasource_maps(self):
        self._datasource_maps = DatasourceMapList()
        for _id, datasource in self.datasource_inventory.items():
            datasource_map = {
                'Datasource Class': datasource['Datasource Class'],
                'Datasource ID': datasource['Datasource ID'],
                'Datasource Name': datasource['Name'],
                _common.DATASOURCE_MAP_ITEM_LEVEL_MAP_FILES: list(),
                _common.DATASOURCE_MAP_REGEX_BASED_MAPS: [
                    {
                        'Old': {
                            'Type': r'(?<type>.*)',

                            'Datasource Class':
                                _common.escape_regex(datasource['Datasource Class']) if datasource[
                                    'Datasource Class'] else None,

                            'Datasource Name': _common.escape_regex(datasource['Name']) if datasource['Name'] else None
                        },
                        'New': {
                            'Type': '${type}',

                            # Why isn't datasource['Datasource Class'] re.escaped? Because in
                            # StoredOrCalculatedItem._lookup_in_regex_based_map() we use ItemsApi.search_items() to
                            # look up a Datasource by its name and Datasource Class is not a property that can accept
                            # a regex. See CRAB-21154 for more context on what led to this.
                            'Datasource Class': datasource['Datasource Class'],

                            'Datasource Name': _common.escape_regex(datasource['Name']) if datasource['Name'] else None
                        }
                    }
                ]
            }

            if datasource['Datasource Class'] in ['Auth', 'Windows Auth', 'LDAP', 'OAuth 2.0']:
                datasource_map['RegEx-Based Maps'].append(copy.deepcopy(datasource_map['RegEx-Based Maps'][0]))

                datasource_map['RegEx-Based Maps'][0]['Old']['Type'] = 'User'
                datasource_map['RegEx-Based Maps'][0]['Old']['Username'] = r'(?<username>.*)'
                datasource_map['RegEx-Based Maps'][0]['New']['Type'] = 'User'
                datasource_map['RegEx-Based Maps'][0]['New']['Username'] = '${username}'

                datasource_map['RegEx-Based Maps'][1]['Old']['Type'] = 'UserGroup'
                datasource_map['RegEx-Based Maps'][1]['Old']['Name'] = r'(?<name>.*)'
                datasource_map['RegEx-Based Maps'][1]['New']['Type'] = 'UserGroup'
                datasource_map['RegEx-Based Maps'][1]['New']['Name'] = '${name}'
            else:
                datasource_map['RegEx-Based Maps'][0]['Old']['Data ID'] = r'(?<data_id>.*)'
                datasource_map['RegEx-Based Maps'][0]['New']['Data ID'] = '${data_id}'

            self.datasource_maps.append(datasource_map)

    @dataclass
    class ItemInventoryProgress:
        scraped: int
        expected: int

    def _scrape_item_inventory(self, session: Session, status: Status, item_cache: Optional[_common.LRUCache],
                               include_access_control: bool, include_archived: Optional[bool]):
        progress = self.ItemInventoryProgress(0, 0)

        self._scrape_folder_inventory(session, status, item_cache, include_access_control)

        scope_references = self._scrape_references_from_scope(status)
        scope_references.update(self._get_worksheet_references())

        references = Workbook._fill_in_item_search_preview_on_references(status, scope_references.values())

        dep_references: Dict[str, Reference] = dict()
        for reference in references:
            self._scrape_inventory_from_item_async(status, progress, reference, item_cache,
                                                   dep_references=dep_references, include_archived=include_archived)

        status.execute_jobs(session, simple=True)

        self.update_status(f'Scraped item inventory ({progress.scraped}/{progress.expected})', progress.scraped)

        Workbook._fill_in_item_search_preview_on_references(status, dep_references.values())

        for dep_reference in dep_references.values():
            self._scrape_inventory_from_item_async(status, progress, dep_reference, item_cache,
                                                   include_archived=include_archived)

        status.execute_jobs(session, simple=True)

        ancestor_references = self._scrape_references_from_ancestors(session, status)
        for ancestor_reference in ancestor_references:
            self._scrape_inventory_from_item_async(status, progress, ancestor_reference, item_cache,
                                                   include_archived=include_archived)

        status.execute_jobs(session, simple=True)

        trees_api = TreesApi(session.client)
        offset = 0
        limit = 1000
        while True:
            asset_tree_output = trees_api.get_tree_root_nodes(scope=[self.id], exclude_globally_scoped=True,
                                                              offset=offset, limit=limit)

            for child in asset_tree_output.children:
                if child.id in self.item_inventory:
                    self.item_inventory[child.id]['Parent ID'] = Item.ROOT

            if len(asset_tree_output.children) < limit:
                break

            offset = offset + limit

    def _scrape_references_from_ancestors(self, session: Session, status: Status) -> List[Reference]:
        ancestors_to_scrape = set()
        for item in self._item_inventory.values():
            if item.type == 'Folder' or 'Parent ID' not in item:
                continue

            parent_id = item['Parent ID']
            if parent_id in self._item_inventory:
                continue

            if parent_id in ancestors_to_scrape:
                continue

            if parent_id == Item.ROOT:
                continue

            ancestors_to_scrape.add(parent_id)

            trees_api = TreesApi(session.client)
            asset_tree_output = safely(
                lambda: trees_api.get_tree(id=parent_id),
                action_description=f'pull parent ancestry {parent_id}',
                status=status)

            if asset_tree_output is not None and asset_tree_output.item is not None:
                for ancestor in asset_tree_output.item.ancestors:
                    ancestors_to_scrape.add(ancestor.id)

        return [Reference(ancestor_id, Reference.ANCESTOR) for ancestor_id in ancestors_to_scrape]

    @staticmethod
    def _fill_in_item_search_preview_on_references(
            status: Status, references: Iterable[Reference]) -> List[Reference]:
        new_references = list(references)
        if not _version.is_sdk_module_version_at_least(62):
            return new_references

        filtered_references = [r for r in new_references if r.item_search_preview is None]
        if len(filtered_references) == 0:
            return new_references
        context = _spy_search.SearchContext(status.session, status)
        context.items_api = ItemsApi(status.session.client)
        context.include_properties = _spy_search.ALL_PROPERTIES
        identifiers = [{'ID': r.id} for r in filtered_references]
        search_by_id_helper = _spy_search.SearchByIDHelper(context, identifiers)
        for i in range(len(filtered_references)):
            reference: Reference = filtered_references[i]
            item_found = search_by_id_helper.get_by_index(i)
            if item_found is None:
                # This can happen due to edge cases like CRAB-40580
                continue
            reference.item_search_preview = item_found

        return new_references

    def _scrape_folder_inventory(self, session: Session, status: Status, item_cache: Optional[_common.LRUCache],
                                 include_access_control):
        if 'Ancestors' not in self:
            return

        for ancestor_id in self['Ancestors']:
            if not _common.is_guid(ancestor_id):
                # This is a synthetic folder, analogous to "Users" and "Shared" in the Seeq Home Screen
                continue

            self.update_status('Scraping folders', 0)

            if item_cache is not None and ancestor_id in item_cache:
                item = item_cache[ancestor_id]
            else:
                item = safely(
                    lambda: Folder.pull(ancestor_id, session=session, status=status,
                                        include_access_control=include_access_control),
                    action_description=f'pull Folder {ancestor_id}',
                    status=status)

            self.update_status('Scraping folders', 1)

            if item is None:
                continue

            if item_cache is not None:
                item_cache[ancestor_id] = item

            self.add_to_inventory(item)

    def _scrape_inventory_from_item_async(self, status: Status, progress: ItemInventoryProgress,
                                          reference: Reference, item_cache: Optional[_common.LRUCache],
                                          *, dep_references: Dict[str, Reference] = None,
                                          include_archived: Optional[bool] = None):
        if reference.id in self.item_inventory or reference.id in status.jobs:
            return

        # The default (include_archived=None) means that archived inventory is INCLUDED.
        if (reference.item_search_preview is not None and include_archived is False and
                reference.item_search_preview.is_archived):
            return

        what = 'inventory' if dep_references is not None else 'dependencies'

        if dep_references is not None:
            progress.expected += 1

        allowed_types = [
            'Asset',
            'StoredSignal',
            'CalculatedSignal',
            'StoredCondition',
            'CalculatedCondition',
            'LiteralScalar',
            'CalculatedScalar',
            'Chart',
            'ThresholdMetric',
            'Datafile'
        ]

        def _in_dep_references(_id):
            return dep_references is not None and _id in dep_references

        def _item_pull(_reference: Reference):
            _pulled_item: Item = safely(
                lambda: Item.pull(_reference.id, allowed_types=allowed_types,
                                  item_search_preview=_reference.item_search_preview,
                                  session=status.session, status=status),
                action_description=f'pull inventory from item {_reference.id}', ignore_errors=[404],
                status=status)

            if dep_references is None or _pulled_item is None:
                return _pulled_item, list()

            # The default (include_archived=None) means that archived inventory is INCLUDED.
            if include_archived is False and _pulled_item.get('Archived', False):
                return None, list()

            if isinstance(_pulled_item, ThresholdMetric):
                return _pulled_item, Workbook._scrape_references_from_dependencies(status, _reference.id)

            # If all formula parameters are already in the dep_references, we can skip this expensive call
            for k, v in _pulled_item.get('Formula Parameters', dict()).items():
                if v not in status.jobs and not _in_dep_references(v):
                    return _pulled_item, Workbook._scrape_references_from_dependencies(status, _reference.id)

            return _pulled_item, list()

        def _after_item_pull(_, _job_result):
            if _job_result is None:
                return

            _job_item, _job_dependencies = _job_result

            progress.scraped += 1
            if progress.scraped % 50 == 0:
                self.update_status(
                    f'Scraping item {what} '
                    f'({progress.scraped}/{progress.expected})',
                    0)

            if _job_item is None:
                return

            _job_item, _job_dependencies = _job_result

            progress.scraped += 1
            if progress.scraped % 50 == 0:
                self.update_status(
                    f'Scraping item {what} '
                    f'({progress.scraped}/{progress.expected})',
                    0)

            if _job_item is None:
                return

            if item_cache is not None:
                item_cache[_job_item.id] = _job_result

            if _common.get(_job_item, 'Is Generated', False):
                return

            self.add_to_inventory(_job_item)

            for _dependency in _job_dependencies:
                if _dependency.id in status.jobs or _in_dep_references(_dependency.id):
                    continue

                progress.expected += 1

                if dep_references is not None:
                    dep_references[_dependency.id] = _dependency

        if item_cache is not None and reference.id in item_cache:
            _after_item_pull(reference.id, item_cache[reference.id])
        else:
            status.add_job(reference.id, (_item_pull, reference), _after_item_pull)

    def _scrape_references_from_scope(self, status: Status) -> Dict[str, Reference]:
        items_api = ItemsApi(status.session.client)

        scope_references: Dict[str, Reference] = dict()
        offset = 0
        while True:
            kwargs = {
                'filters': ['', '@excludeGloballyScoped', '@includeUnsearchable'],
                'scope': [self.id],
                'offset': offset,
                'limit': status.session.options.search_page_size
            }

            if _version.is_sdk_module_version_at_least(62):
                kwargs['include_properties'] = [SeeqNames.API.Flags.all_properties]

            self.update_status(f'Scraping scope references (search offset: {offset})', 0)

            # noinspection PyBroadException
            search_results = safely(
                lambda: items_api.search_items(**kwargs),
                action_description=f'scrape items scoped to workbook {self.id}',
                status=status)  # type: ItemSearchPreviewPaginatedListV1

            if search_results is None:
                break

            scope_references.update({item.id: Reference(item.id, Reference.SCOPED,
                                                        item_search_preview=item) for item in search_results.items})

            for item in search_results.items:
                for ancestor in item.ancestors:
                    if ancestor.id not in scope_references:
                        scope_references[ancestor.id] = Reference(ancestor.id, Reference.ANCESTOR)

            if len(search_results.items) < search_results.limit:
                break

            offset += search_results.limit

            self.update_status(f'Scraping scope references ({offset})', 0)

        return scope_references

    @staticmethod
    def _scrape_references_from_dependencies(status: Status, item_id):
        items_api = ItemsApi(status.session.client)
        referenced_items = list()

        dependencies = safely(lambda: items_api.get_formula_dependencies(id=item_id),
                              action_description=f'scraping dependencies for item {item_id}',
                              ignore_errors=[404], status=status)

        if dependencies is not None:
            for dependency in dependencies.dependencies:  # type: ItemParameterOfOutputV1
                referenced_items.append(Reference(
                    dependency.id,
                    Reference.DEPENDENCY
                ))

        return referenced_items

    def add_to_scope(self, item):
        if item.get('Datasource Class') is not None and item.get('Datasource Class') != 'Seeq Data Lab':
            raise SPyValueError(f'Item {item} is not a Seeq Data Lab item and cannot be scoped to a workbook')

        self.add_to_inventory(item)

        if not isinstance(item, Folder):
            item['Scoped To'] = self.id

    def add_to_inventory(self, item):
        if not isinstance(item, (StoredOrCalculatedItem, Folder)):
            raise SPyTypeError(
                f'Workbook.add_to_inventory only accepts Stored or Calculated items. You tried to add:\n{item}')

        self.item_inventory[item.id] = item

    def _new_worksheet(self, clazz: Type[Worksheet], name: str, create: bool = True) -> Optional[Worksheet]:
        existing_worksheet = self._get_worksheet(name)
        if existing_worksheet:
            # noinspection PyTypeChecker
            return existing_worksheet
        elif not create:
            return None

        return clazz(self, {'Name': name})

    def _get_worksheet(self, name) -> Optional[Worksheet]:
        for worksheet in self.worksheets:
            if worksheet.name == name:
                return worksheet

        return None

    def _put_worksheet(self, worksheet: Worksheet):
        worksheets_that_match_object = [w for w in self.worksheets if w is worksheet]
        worksheets_that_match_id = [w for w in self.worksheets if w.id == worksheet.id]
        worksheets_that_match_name = [w for w in self.worksheets if w.name == worksheet.name]

        if len(worksheets_that_match_object) > 0:
            # This specific worksheet object already exists on the workbook-- do nothing
            return

        if len(worksheets_that_match_id) > 0:
            self.worksheets[self.worksheets.index(worksheets_that_match_id[0])] = worksheet
            return

        if len(worksheets_that_match_name) > 0:
            # Force the incoming worksheet to adopt the ID of the existing worksheet
            index = self.worksheets.index(worksheets_that_match_name[0])
            old_worksheet = self.worksheets[index]
            worksheet['ID'] = old_worksheet['ID']
            self.worksheets[index] = worksheet
            return

        self.worksheets.append(worksheet)


class Analysis(Workbook):

    def worksheet(self, name: str, create: bool = True) -> Optional[AnalysisWorksheet]:
        return self._new_worksheet(AnalysisWorksheet, name, create=create)

    def get_workstep_usages(self, use_investigate_range=False, now: pd.Timestamp = None) -> Dict[str, list]:
        usages: Dict[str, list] = super().get_workstep_usages(use_investigate_range=use_investigate_range, now=now)
        attr = 'investigate_range' if use_investigate_range else 'display_range'
        for worksheet in self.worksheets:
            for workstep in worksheet.worksteps.values():
                # Note that we grab all the worksteps, because if they were pulled down, they were referenced by
                # something and it may have been a Journal link. We don't want to miss those.
                range_to_use = getattr(workstep, attr, None)
                if range_to_use is None or 'Start' not in range_to_use or 'End' not in range_to_use:
                    continue

                usage_periods = usages.setdefault(workstep.id, list())
                if not pd.isna(range_to_use['Start']) and not pd.isna(range_to_use['End']):
                    usage_periods.append({'Start': range_to_use['Start'], 'End': range_to_use['End']})

        return usages


class Topic(Workbook):

    def document(self, name: str, create: bool = True) -> Optional[TopicDocument]:
        return self._new_worksheet(TopicDocument, name, create=create)

    @property
    def documents(self):
        return self.worksheets

    def put_document(self, document: TopicDocument):
        if not isinstance(document, TopicDocument):
            raise SPyTypeError('put_document() requires argument of type TopicDocument')
        super()._put_worksheet(document)

    def pull_rendered_content(self, session: Session, status: Status):
        for worksheet in self.worksheets:
            timer = _common.timer_start()
            worksheet.pull_rendered_content(session, status=status.create_inner(f'Pull Embedded Content {worksheet}'))
            status.df.at[worksheet.id, 'Name'] = worksheet.name
            if worksheet.report.rendered_content_images is None:
                status.df.at[worksheet.id, 'Count'] = np.nan
            else:
                status.df.at[worksheet.id, 'Count'] = len(worksheet.report.rendered_content_images)
            status.df.at[worksheet.id, 'Time'] = _common.timer_elapsed(timer)

    def get_workstep_usages(self, use_investigate_range=False, now: pd.Timestamp = None) -> Dict[str, list]:
        usages: Dict[str, list] = super().get_workstep_usages(use_investigate_range=use_investigate_range, now=now)
        if now is None:
            now = pd.Timestamp.utcnow()

        for document in self.documents:
            for content in document.content.values():
                usage_periods = usages.setdefault(content['Workstep ID'], list())
                date_range = content.date_range
                if date_range is None:
                    # DateRange is inherited from the workstep/worksheet, and since we don't have a workstep object
                    # we can't get the date range. That's OK for the primary use case (spy.workbooks.job.pull())
                    # because it will cover the inherent date ranges for all worksteps in all pulled Analysis workbooks.
                    continue

                if date_range.get('Auto Enabled', False):
                    for key in ['Auto Duration', 'Auto Offset', 'Auto Offset Direction']:
                        if key not in date_range:
                            continue

                    auto_duration = _common.parse_str_time_to_timedelta(date_range['Auto Duration'])
                    auto_offset = _common.parse_str_time_to_timedelta(date_range['Auto Offset'])
                    if date_range['Auto Offset Direction'] == 'Past':
                        auto_offset *= -1
                    start = now - auto_offset - auto_duration
                    end = now - auto_offset
                    usage_periods.append({'Start': pd.Timestamp(start), 'End': pd.Timestamp(end)})
                else:
                    for key in ['Start', 'End']:
                        if key not in date_range:
                            continue

                    usage_periods.append({
                        'Start': pd.Timestamp(date_range['Start']),
                        'End': pd.Timestamp(date_range['End'])}
                    )

        return usages


class WorkbookList(ItemList):
    # noinspection PyTypeChecker
    def __getitem__(self, key) -> Union[Analysis, Topic, Room]:
        return super().__getitem__(key)

    def __setitem__(self, key, val: Workbook):
        return super().__setitem__(key, val)


class Room(Workbook):
    def __init__(self, definition=None, *, provenance=None):
        super().__init__(definition, provenance=provenance)

        self._annotation = Journal(self)

    def view(self, name: str, create: bool = True) -> Optional[RoomView]:
        return self._new_worksheet(RoomView, name, create=create)

    @property
    def journal(self):
        """
        Returns the "Journal" object, which is an "Annotation" that houses the HTML and other metadata about the
        Journal attached to this worksheet.
        """
        return self._annotation

    @property
    def views(self):
        return self.worksheets
