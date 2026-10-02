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
from mailmanclient.restobjects.preferences import PreferencesMixin
from mailmanclient.restbase.base import RESTObject

__metaclass__ = type
__all__ = [
    'Member'
]


class Member(RESTObject, PreferencesMixin):

    _properties = ('address', 'delivery_mode', 'email', 'list_id',
                   'moderation_action', 'display_name', 'role', 'self_link',
                   'subscription_mode', 'member_id', 'bounce_score',
                   'last_bounce_received', 'last_warning_sent',
                   'total_warnings_sent')
    _writable_properties = ('address', 'delivery_mode', 'moderation_action')

    def __repr__(self):
        return '<Member {0!r} on {1!r} with role {2!r}>'.format(
            self.email, self.list_id, self.role)

    def __str__(self):
        return 'Member "{0}" on "{1}"'.format(self.email, self.list_id)

    @property
    def address(self):
        from mailmanclient.restobjects.address import Address
        return Address(self._connection, self.rest_data['address'])

    @property
    def user(self):
        from mailmanclient.restobjects.user import User
        return User(self._connection, self.rest_data['user'])

    def unsubscribe(self):
        """Unsubscribe the member from a mailing list."""
        response, json = self._connection.call(self.self_link, method='DELETE')
        if response.status_code == 202:
            return json
