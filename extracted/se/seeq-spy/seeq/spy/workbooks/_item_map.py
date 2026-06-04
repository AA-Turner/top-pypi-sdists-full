from __future__ import annotations

import re
from typing import Dict, List, Optional, Pattern, Tuple, Union

import pandas as pd

from seeq import spy
from seeq.spy import _common
from seeq.spy._errors import *


class ItemMap:
    """
    Represents a map of item identifiers from a source (usually a saved set of workbooks) to the destination on the
    Seeq Server. This class is used extensively by spy.workbooks.push() operations.
    """
    _item_map: Union[dict, ItemMap]
    _lookup_df: Optional[pd.DataFrame]
    _logs: Dict[str, List[str]]
    _dummy_items: pd.DataFrame
    _replace_items_cache: Optional[Tuple[Dict, List[Pattern[str]]]]
    _freeze_replace_patterns: bool
    workstep_mappings: Dict[str, Dict[str, str]]
    image_mappings: Dict[str, Dict[str, str]]
    content_mappings: Dict[str, dict]

    only_override_maps: bool
    fall_through: bool
    data_item_cache: _common.LRUCache

    def __getstate__(self):
        return (self._item_map, self._lookup_df, self._logs, self._dummy_items, self.only_override_maps,
                self.fall_through, self.workstep_mappings, self.image_mappings, self.content_mappings)

    def __setstate__(self, state):
        def get(i, default=None):
            return state[i] if i < len(state) else default

        # Accessing by index with a default allows us to maintain compatibility with previously-pickled ItemMap objects
        self.data_item_cache = _common.LRUCache()
        self._item_map = get(0, dict())
        self._lookup_df = get(1)
        self._logs = get(2, dict())
        self._dummy_items = get(3, pd.DataFrame({'ID': pd.Series(dtype=str)}))
        self.only_override_maps = get(4, False)
        self.fall_through = get(5, False)
        self.workstep_mappings = get(6, dict())
        self.image_mappings = get(7, dict())
        self.content_mappings = get(8, dict())

        self._replace_items_cache = None
        self._freeze_replace_patterns = False

    def __init__(self, item_map=None, lookup_df: Optional[pd.DataFrame] = None):
        self._item_map = item_map if item_map is not None else dict()
        self._lookup_df = lookup_df
        self._logs = dict()
        self._dummy_items = pd.DataFrame({'ID': pd.Series(dtype=str)})
        self._replace_items_cache = None
        self._freeze_replace_patterns = False
        self.workstep_mappings = dict()
        self.image_mappings = dict()
        self.content_mappings = dict()
        self.only_override_maps = False
        self.fall_through = False
        self.data_item_cache = _common.LRUCache()

    def __contains__(self, key: object) -> bool:
        key = _common.ensure_upper_case_id('ID', key)
        contains = self._item_map.__contains__(key)
        if not contains and self._should_fall_through(key):
            return True
        else:
            return contains

    def __getitem__(self, key):
        key = _common.ensure_upper_case_id('ID', key)
        try:
            return self._item_map.__getitem__(key)
        except KeyError:
            if self._should_fall_through(key):
                return key

            raise KeyError(f"Item {key} not found in item map. It is either not in the workbooks' inventory or "
                           f"the inventory is not being pushed as part of this operation.")

    def __setitem__(self, key, val):
        if key is None:
            raise ValueError('ItemMap does not support None as a key')

        key = _common.ensure_upper_case_id('ID', key)
        val = _common.ensure_upper_case_id('ID', val)
        self._item_map.__setitem__(key, val)

        # We don't invalidate if key==val because it means that there's no replacement to be done anyways
        if key != val:
            self.invalidate_replace_patterns()

    def __delitem__(self, key):
        key = _common.ensure_upper_case_id('ID', key)
        self._item_map.__delitem__(key)
        self.invalidate_replace_patterns()

    def get(self, key, default=None):
        key = _common.ensure_upper_case_id('ID', key)
        if key in self._item_map:
            return self._item_map[key]

        if self._should_fall_through(key):
            return key
        else:
            return default

    def keys(self):
        return self._item_map.keys()

    @property
    def has_look_up_df(self):
        return self._lookup_df is not None

    def look_up_id(self, value):
        row = _common.look_up_in_df(value, self._lookup_df)
        return row['ID']

    def invalidate_replace_patterns(self):
        if not self._freeze_replace_patterns:
            self._replace_items_cache = None

    def freeze_replace_patterns(self):
        self._freeze_replace_patterns = True

    def unfreeze_replace_patterns(self):
        self._freeze_replace_patterns = False
        self._replace_items_cache = None

    def replace_items(self, document: str, chunk_size: int = 5000) -> Optional[str]:
        if self._replace_items_cache is None:
            keys = sorted([k for k in self.keys() if k != self[k]], key=len, reverse=True)
            lookup = {k.lower(): self[k] for k in keys}
            chunks = [keys[i:i + chunk_size] for i in range(0, len(keys), chunk_size)]
            self._replace_items_cache = (lookup, [
                re.compile("|".join(map(re.escape, chunk)), flags=re.IGNORECASE)
                for chunk in chunks
            ])

        out = document
        lookup, patterns = self._replace_items_cache
        for pattern in patterns:
            out = pattern.sub(lambda m: lookup.get(m.group(0).lower(), m.group(0)), out)

        return out

    def _should_fall_through(self, key):
        return self.fall_through and _common.is_guid(key)

    def log(self, key, message, at_top=False):
        if key not in self._logs:
            self._logs[key] = list()
        if at_top:
            self._logs[key].insert(0, message)
        else:
            self._logs[key].append(message)

    def add_dummy_item(self, dummy_item: pd.Series):
        self._dummy_items = pd.concat([self._dummy_items, dummy_item.to_frame().T])

    @property
    def dummy_items(self):
        return self._dummy_items

    def explain(self, key: Union[str, pd.DataFrame, pd.Series]):
        """
        Returns a string explaining the mapping outcome of a particular item.
        This is useful for debugging datasource mapping, both for things that
        fail and things that succeed to learn how the mapping was applied.
        Typically, you will use print() to show the returned value in the
        console.

        :param key: The item ID of the item to be explained. This can also be
        a one-row DataFrame or a Series with an 'ID' column. Note that this
        ID is of the item in the source workbook, not the ID of the pushed item
        in the destination workbook.
        :return: A string explaining the mapping outcome of a particular item.
        """
        if isinstance(key, pd.DataFrame):
            if 'ID' not in key.columns:
                raise SPyValueError('explain() requires a one-row DataFrame with an "ID" column')
            if len(key) == 0:
                raise SPyValueError('DataFrame supplied is empty')
            if len(key) > 1:
                raise SPyValueError('DataFrame supplied has more than one row')
            key = key.iloc[0]['ID']
        elif isinstance(key, pd.Series):
            if 'ID' not in key:
                raise SPyValueError('explain() requires a Series with "ID"')
            key = key['ID']
        elif not isinstance(key, str):
            raise SPyTypeError(f'Argument to explain() must be a str, DataFrame, or Series, '
                               f'not {key.__class__.__name__}')

        if key not in self._logs:
            return f'There are no mapping logs for {key}'

        return '\n'.join(self._logs[key])

    def clear_logs(self, key):
        self._logs[key] = list()

    def add_dry_run_placeholder_id(self, item_id: str) -> str:
        value = f'From:{item_id}'
        self[item_id] = value
        return value

    def was_item_pushed(self, item_id: str) -> bool:
        return (
                not str(item_id).startswith('From:') and
                item_id in self._item_map and
                not str(self._item_map[item_id]).startswith('From:')
        )

    def is_real_id(self, item_id: str) -> bool:
        return not str(item_id).startswith('From:')


class OverrideItemMap(ItemMap):
    """
    Takes an existing ItemMap and overrides various keys. This is used extensively in the templating system to
    temporarily (for the extent of a particular frame in a callstack) override the inner ItemMap using
    template_parameters or an override_map.
    """

    _override: dict
    _parameters: Optional[dict]

    def __init__(self, item_map: ItemMap, *, template_parameters: dict = None, override_map: dict = None):
        super().__init__(item_map)

        self._override = dict() if override_map is None else override_map
        self._parameters = None
        if template_parameters:
            self._parameters = template_parameters
            self._override_from_template_parameters(template_parameters)

    def __contains__(self, key):
        key = _common.ensure_upper_case_id('ID', key)
        return self._override.__contains__(key) or self._item_map.__contains__(key)

    def __getitem__(self, key):
        key = _common.ensure_upper_case_id('ID', key)
        if self._override.__contains__(key):
            return self._override.__getitem__(key)
        else:
            return super().__getitem__(key)

    def __delitem__(self, key):
        key = _common.ensure_upper_case_id('ID', key)
        if self._override.__contains__(key):
            self._override.__delitem__(key)
        else:
            self._item_map.__delitem__(key)
        self.invalidate_replace_patterns()

    def get(self, key, default=None):
        key = _common.ensure_upper_case_id('ID', key)
        return self._override.get(key, self._item_map.get(key, default))

    @property
    def has_look_up_df(self):
        return self._item_map.has_look_up_df

    def look_up_id(self, value):
        return self._item_map.look_up_id(value)

    def keys(self):
        keys = set(self._item_map.keys())
        keys.update(self._override.keys())
        return keys

    def override(self, key, value):
        self._override[key] = value

    @property
    def parameters(self):
        if self._parameters is not None:
            return self._parameters

        if isinstance(self._item_map, OverrideItemMap):
            return self._item_map.parameters

        return None

    def log(self, key, message, at_top=False):
        self._item_map.log(key, message, at_top=at_top)

    @property
    def workstep_mappings(self):
        return self._item_map.workstep_mappings

    @workstep_mappings.setter
    def workstep_mappings(self, value):
        self._item_map.workstep_mappings = value

    @property
    def image_mappings(self):
        return self._item_map.image_mappings

    @image_mappings.setter
    def image_mappings(self, value):
        self._item_map.image_mappings = value

    @property
    def content_mappings(self):
        return self._item_map.content_mappings

    @content_mappings.setter
    def content_mappings(self, value):
        self._item_map.content_mappings = value

    def _override_from_template_parameters(self, template_parameters: dict):

        for key, value in template_parameters.items():
            if value is None or (value is float and pd.isna(value)):
                continue

            _id, _type, _fqn = spy.workbooks.ItemTemplate.code_key_tuple(key)

            if _id is None:
                # This is the case of a Mustachioed annotation with {{variable}} tokens in it
                continue

            if isinstance(value, pd.DataFrame):
                if len(value) > 1:
                    raise SPyValueError(f'Multiple rows in template_parameters dict for "{key}":\n{value}')
                if len(value) == 0:
                    raise SPyValueError(f'Empty DataFrame in template_parameters dict for "{key}"')
                value = value.iloc[0].to_dict()
            elif isinstance(value, str):
                value = {'ID': value} if _common.is_guid(value) else {'Name': value}
            elif isinstance(value, spy.workbooks.ItemTemplate):
                continue

            if _common.present(value, 'ID') and not _common.get(value, 'Reference', default=False):
                self._override[_id] = _common.get(value, 'ID')
            else:
                if not self._item_map.has_look_up_df:
                    raise SPyValueError(f'Attempted lookup for template parameter "{key}" but no lookup_df argument '
                                        f'was supplied to spy.workbooks.push(). Perhaps you are using '
                                        f'spy.workbooks.push() when you meant to use spy.push(metadata=<metadata>, '
                                        f'workbook=<workbook>)?\n{value}')

                self._override[_id] = self.look_up_id(value)
