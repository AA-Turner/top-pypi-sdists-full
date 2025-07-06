# Copyright (C) 2021-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailman.client.
#
# mailman.client is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailman.client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.

"""Base classes for async objects."""

__all__ = [
    'RESTBase',
    'RESTObject',
]

from typing import Sequence, Any, Tuple
from mailmanclient.restobjects.types import (
    ConnectionProto, ResponseType, ContentType)


class RESTBase:

    _properties: Sequence[str] = ['self_link']
    _writable_properties: Sequence[str] = []
    _read_only_properties: Sequence[str] = ['self_link']

    def __init__(self,
                 connection: ConnectionProto, data: ContentType,
                 ) -> None:
        """
        :param connection: API connection object to fetch sub-resources.
        :param data: Data from REST API.
        """
        self._data = data
        self._connection = connection
        self._changed_rest_data = {}

    def __repr__(self) -> str:
        """Provide a default repr for all object types."""
        return '<{} at {}>'.format(self.__class__, self._data.get('self_link'))

    def _get(self, key: str) -> str:
        """Get the value of 'key' from object's REST data.

        :param key: The key to get value for.
        """
        if self._properties is not None:
            # Some REST key/values may not be returned by Mailman if the value
            # is None.
            if key in self._data:
                return self._data.get(key)
            raise KeyError(key)
        else:
            return self._data.get(key)

    def _set(self, key: str, value: Any) -> None:
        if (key in self._read_only_properties or (
                self._writable_properties is not None
                and key not in self._writable_properties)):
            raise ValueError(f'{key} is read-only')
        # Don't check that the key is in _properties, the accepted values for
        # write may be different from the returned values (eg: User.password
        # and User.cleartext_password).
        if self._data.get(key, None) == value:
            return
        self._changed_rest_data[key] = value

    def _reset_cache(self) -> None:
        self._changed_rest_data = {}
        self._data = None

    async def save(self) -> Tuple[ResponseType, ContentType]:
        res = await self._connection.call(
            self._data.get('self_link'),
            self._changed_rest_data,
            method='PATCH'
            )
        self._reset_cache()
        return res


class RESTObject(RESTBase):

    def __getattr__(self, name) -> Any:
        try:
            return self._get(name)
        except KeyError:
            raise AttributeError(
                '"{}" has no attribute "{}"'.format(
                    self.__class__.__name__, name))

    def __setattr__(self, name: str, value: Any):
        if self._properties and (name not in self._properties):
            return super().__setattr__(name, value)
        return self._set(name, value)

    async def delete(self) -> Tuple[ResponseType, ContentType]:
        res = await self.connection.call(
            self._data.get('self_link'), method='DELETE')
        self._reset_cache()
        return res
