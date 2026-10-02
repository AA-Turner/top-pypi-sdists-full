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

"""Member async object."""

__all__ = [
    'Member',
]

from mailmanclient.restbase.async_base import RESTObject
from mailmanclient.asyncobjects.preferences import PreferencesMixin


class Member(RESTObject, PreferencesMixin):

    _properties = ('address', 'delivery_mode', 'email', 'list_id',
                   'moderation_action', 'display_name', 'role', 'self_link',
                   'subscription_mode', 'member_id')
    _writable_properties = ('address', 'delivery_mode', 'moderation_action')

    def __repr__(self):
        return '<Member {0!r} on {1!r} with role {2!r}>'.format(
            self.email, self.list_id, self.role)
