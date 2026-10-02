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
from mailmanclient.restbase.base import RESTObject

__metaclass__ = type
__all__ = [
    'Queue'
]


class Queue(RESTObject):

    _properties = ('name', 'directory', 'files')

    def __repr__(self):
        return '<Queue: {!r}>'.format(self.name)

    def inject(self, list_id, text):
        self._connection.call(self._url, dict(list_id=list_id, text=text))

    @property
    def files(self):
        # No caching.
        response, content = self._connection.call(self._url)
        return content['files']
