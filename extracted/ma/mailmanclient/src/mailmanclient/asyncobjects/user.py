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

"""User async object."""

__all__ = [
    'User',
]

from mailmanclient.restbase.async_base import RESTObject
from mailmanclient.restobjects.utils import list_of_objects
from mailmanclient.asyncobjects.preferences import PreferencesMixin


class User(RESTObject, PreferencesMixin):

    _properties = ('created_on', 'display_name', 'is_server_owner',
                   'password', 'self_link', 'user_id')
    _writable_properties = ('cleartext_password', 'display_name',
                            'is_server_owner')

    def __repr__(self):
        return '<User {0!r} ({1})>'.format(self.display_name, self.user_id)

    async def addresses(self):
        from mailmanclient.asyncobjects.address import Address
        url = self.self_link + '/addresses'
        resp, content = await self._connection.call(url)
        return list_of_objects(Address, content, self._connection)
