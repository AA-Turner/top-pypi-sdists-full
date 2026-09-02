"""
Panther Core is a Python library for Panther Detections.
Copyright (C) 2020 Panther Labs Inc

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from collections import OrderedDict
from collections.abc import Mapping
from typing import Any, Callable, List, Optional, Sequence, Union

from dateutil import parser as dateparser

from .data_model import E_NO_DATA_MODEL_FOUND, DataModel
from .exceptions import PantherError
from .immutable import ImmutableCaseInsensitiveDict, json_encoder

__all__ = ["PantherEvent"]


class PantherEvent(ImmutableCaseInsensitiveDict):  # pylint: disable=R0901
    """Panther enriched event with unified data model (udm) access."""

    def __init__(self, event: Mapping, data_model: Optional[DataModel] = None):
        """Create data model lookups

        Args:
            event: Dictionary representing the event.
            data_model: the data model used for the LogType associated with this event
        """
        super().__init__(event)
        self.data_model = data_model
        self.lookup_function: Any = None

    def _add_lookup_function(self, lookup_function: Callable[[Any, str, str], Any]) -> Any:
        """Updates the behavior of the event.lookup function to be that of the provided
        lookup function
        """
        self.lookup_function = lookup_function

    def lookup(self, lookup_name: str, lookup_key: str) -> Any:
        """
        Looks up data in the associated lookup table and returns the data
        if it exists, otherwise it will return None


        If no look function is specified the following structure is expected on the event
        {
            "_mocked_lookup_data_": {
                "lookup_table_name": {
                    "lookup_key": "lookup_value"
                }
            }
        }
        """
        if self.lookup_function:
            return self.lookup_function(self, lookup_name, lookup_key)

        return self.deep_get("_mocked_lookup_data_", lookup_name, lookup_key)

    def udm(self, *key: str, default: Any = None) -> Any:
        """
        udm operates in two modes

        Mode 1: Data Model Access
        If a single key is provided it will check to see if it exists on the data
        model mapping. If a mapping is not found it operates in Mode 2.

        Mode 2: p_udm access
        If there was no match against the data model it checks against the p_udm field.
        If there was no match against the p_udm field it will check on the event itself.
        If all other conditions are exhausted the default value is utilized as the return value
        """

        model = self.data_model
        if len(key) == 1 and model:
            match = self._get_json_path(key[0])
            if match:
                return self._ensure_immutable(match.value)
            method = self._get_method(key[0])
            if method:
                return self._ensure_immutable(method(self._ensure_immutable(self._container)))

            # if data model mapping is defined we should short circuit logic
            # to maintain backwards compatability
            if key[0] in model.paths or key[0] in model.methods:
                return default

        pieces = list(key)
        if len(pieces) > 0:
            pieces.insert(0, "p_udm")
            result = self.deep_get(*tuple(pieces))
            if not result:
                result = self.deep_get(*list(key))
            if result:
                return result
        # no matches, return default
        return default

    def udm_path(self, key: str) -> Optional[str]:
        """Returns the JSON path or method name for the mapped field"""
        self._validate()
        # access values via standardized fields
        match = self._get_json_path(key)
        if match:
            return str(match.full_path)
        method = self._get_method(key)
        if method:
            return getattr(method, "__name__", repr(method))
        # no matches, return None by default
        return None

    def deep_walk(
        self, *keys: str, default: Optional[str] = None, return_val: str = "all"
    ) -> Union[Optional[Any], Optional[List[Any]]]:
        """Safely retrieve a value stored in complex dictionary structure

        Similar to deep_get but supports accessing dictionary keys within nested lists as well

        Parameters:
        keys (str): comma-separated list of keys used to traverse the event object
        default (str): the default value to return if the desired key's value is not present
        return_val (str): string specifying which value to return
                        possible values are "first", "last", or "all"

        Returns:
        any | list[any]: A single value if return_val is "first", "last",
                        or if "all" is a list containing one element,
                        otherwise a list of values
        """

        def _empty_list(sub_obj: Any) -> bool:
            return (
                all(_empty_list(next_obj) for next_obj in sub_obj)
                if isinstance(sub_obj, Sequence) and not isinstance(sub_obj, str)
                else False
            )

        obj = self._container

        if not keys:
            return default if _empty_list(obj) or obj is None else obj

        current_key = keys[0]
        found: OrderedDict = OrderedDict()

        if isinstance(obj, Mapping):
            next_key = PantherEvent(obj.get(current_key, default))
            return (
                next_key.deep_walk(*keys[1:], default=default, return_val=return_val)
                if next_key is not None
                else default
            )
        if isinstance(obj, Sequence) and not isinstance(obj, str):
            for item in obj:
                next_item = PantherEvent(item)
                value = next_item.deep_walk(*keys, default=default, return_val=return_val)
                if value is not None:
                    if isinstance(value, Sequence) and not isinstance(value, str):
                        for sub_item in value:
                            found[sub_item] = None
                    else:
                        found[value] = None
        found_list: list[Any] = list(found.keys())
        if not found_list:
            return default
        return {
            "first": found_list[0],
            "last": found_list[-1],
            "all": found_list[0] if len(found_list) == 1 else found_list,
        }.get(return_val, "all")

    def event_time_epoch(self, force_utc: bool = True) -> int:
        """Parses epoch seconds from the p_event_time field.
        Returns 0 if event time is not available."""
        try:
            event_time = self.get("p_event_time") or ""
            if force_utc:
                event_time += " UTC"
            return int(dateparser.parse(event_time).timestamp())
        except dateparser.ParserError:
            return 0

    def _validate(self) -> None:
        if not self.data_model:
            raise PantherError(E_NO_DATA_MODEL_FOUND, self._container.get("p_log_type"))

    def _get_json_path(self, key: str) -> Any:
        if not self.data_model:  # makes linter happy, we never call this if not set
            return None
        if key not in self.data_model.paths:
            return None
        json_path = self.data_model.paths.get(key)
        if not json_path:
            return None
        matches = json_path.find(self._container)
        if len(matches) == 0:
            return None
        if len(matches) == 1:
            return matches[0]
        # pylint:disable=broad-exception-raised
        raise Exception(
            "JSONPath [{}] in DataModel [{}], matched multiple fields.".format(
                json_path, self.data_model.data_model_id
            )
        )

    def _get_method(self, key: str) -> Any:
        if not self.data_model:  # makes linter happy, we never call this if not set
            return None
        if key not in self.data_model.methods:
            return None
        method = self.data_model.methods.get(key)
        if callable(method):
            return method
        # no matches, return None by default
        return None

    json_encoder = json_encoder
