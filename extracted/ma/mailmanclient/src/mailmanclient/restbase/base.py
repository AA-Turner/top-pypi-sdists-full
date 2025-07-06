# Copyright (C) 2010-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailmanclient.
#
# mailmanclient is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailmanclient is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailmanclient.  If not, see <http://www.gnu.org/licenses/>.

from collections.abc import MutableMapping, Sequence

__metaclass__ = type
__all__ = [
    'RESTBase',
    'RESTDict',
    'RESTList',
    'RESTObject'
]


class RESTBase:
    """
    Base class for data coming from the REST API.

    Subclasses can (and sometimes must) define some attributes to handle a
    particular entity.

    :cvar _properties: the list of expected entity properties. This is required
      for API elements that behave like an object, with REST data accessed
      through attributes. If this value is None, the REST data is used to
      list available properties.
    :cvar _writable_properties: list of properties that can be written to using
        a `PATCH` request. If this value is `None`, all properties are
        writable.
    :cvar _read_only_properties: list of properties that cannot be written to
      (defaults to `self_link` only).
    :cvar _autosave: automatically send a `PATCH` request to the API when a
        value is changed. Otherwise, the `save()` method must be called.
    """

    _properties = None
    _writable_properties = None
    _read_only_properties = ['self_link']
    _autosave = False

    def __init__(self, connection, url, data=None):
        """
        :param connection: An API connection object.
        :type connection: Connection.
        :param url: The url of the API endpoint.
        :type url: str.
        :param data: The initial data to use.
        :type data: dict.
        """
        self._connection = connection
        self._url = url
        self._rest_data = data
        self._changed_rest_data = {}

    def __repr__(self):
        return '<{0} at {1}>'.format(self.__class__.__name__, self._url)

    @property
    def rest_data(self):
        """Get data from API and cache it (only once per instance)."""
        if self._rest_data is None:
            response, content = self._connection.call(self._url)
            if isinstance(content, dict) and 'http_etag' in content:
                del content['http_etag']  # We don't care about etags.
            self._rest_data = content
        return self._rest_data

    def _get(self, key):
        if self._properties is not None:
            # Some REST key/values may not be returned by Mailman if the value
            # is None.
            if key in self._properties:
                return self.rest_data.get(key)
            raise KeyError(key)
        else:
            return self.rest_data[key]

    def _set(self, key, value):
        if (key in self._read_only_properties or (
                self._writable_properties is not None
                and key not in self._writable_properties)):
            raise ValueError('value is read-only')
        # Don't check that the key is in _properties, the accepted values for
        # write may be different from the returned values (eg: User.password
        # and User.cleartext_password).
        if key in self.rest_data and self.rest_data[key] == value:
            return  # Nothing to do
        self._changed_rest_data[key] = value
        if self._autosave:
            self.save()

    def _reset_cache(self):
        self._changed_rest_data = {}
        self._rest_data = None

    def save(self):
        response, content = self._connection.call(
            self._url, self._changed_rest_data, method='PATCH')
        self._reset_cache()


class RESTObject(RESTBase):
    """Base class for REST data that behaves like an object with attributes."""

    def __getattr__(self, name):
        try:
            return self._get(name)
        except KeyError:
            # Transform the KeyError into the more appropriate AttributeError
            raise AttributeError(
                "'{0}' object has no attribute '{1}'".format(
                    self.__class__.__name__, name))

    def __setattr__(self, name, value):
        # RESTObject must list REST-specific properties or we won't be able to
        # store the _connection, _url, etc.
        assert self._properties is not None
        if name not in self._properties:
            return super(RESTObject, self).__setattr__(name, value)
        return self._set(name, value)

    def delete(self):
        self._connection.call(self._url, method='DELETE')
        self._reset_cache()


class RESTDict(RESTBase, MutableMapping):
    """Base class for REST data that behaves like a dictionary."""

    def __repr__(self):
        return repr(self.rest_data)

    def __getitem__(self, key):
        return self._get(key)

    def __setitem__(self, key, value):
        self._set(key, value)

    def __delitem__(self, key):
        raise NotImplementedError("REST dictionnary keys can't be deleted.")

    def __iter__(self):
        for key in self.rest_data:
            if self._properties is not None and key not in self._properties:
                continue
            yield key

    def __len__(self):
        return len(self.rest_data)

    def get(self, key, default=None):
        return self.rest_data.get(key, default)

    def keys(self):
        return list(self)

    def update(self, other):
        # Optimize the update to call save() only once
        _old_autosave = self._autosave
        self._autosave = False
        super(RESTDict, self).update(other)
        self._autosave = _old_autosave
        if self._autosave:
            self.save()


class RESTList(RESTBase, Sequence):
    """
    Base class for REST data that behaves like a list.

    The `_factory` attribute is a callable that will be applied on each
    returned member of the list.
    """

    _factory = lambda x: x  # noqa: E731

    @property
    def rest_data(self):
        if self._rest_data is None:
            response, content = self._connection.call(self._url)
            if 'entries' not in content:
                self._rest_data = []
            else:
                self._rest_data = content['entries']
        return self._rest_data

    def __repr__(self):
        return repr(self.rest_data)

    def __getitem__(self, key):
        return self._factory(self.rest_data[key])

    def __delitem__(self, key):
        self[key].delete()
        self._reset_cache()

    def __len__(self):
        return len(self.rest_data)

    def __iter__(self):
        for entry in self.rest_data:
            yield self._factory(entry)

    def clear(self):
        self._connection.call(self._url, method='DELETE')
        self._reset_cache()
