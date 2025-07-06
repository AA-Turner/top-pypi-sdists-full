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

"""Preferences object and mixins."""

__all__ = [
    'Preferences',
    'PreferencesMixin',
]

from mailmanclient.restbase.async_base import RESTObject


class Preferences(RESTObject):

    _properties = (
        'acknowledge_posts', 'delivery_mode', 'delivery_status',
        'hide_address', 'preferred_language', 'receive_list_copy',
        'receive_own_postings',
        )


class PreferencesMixin:
    """Mixin for restobjects that have preferences."""

    async def preferences(self):
        if getattr(self, '_preferences', None) is None:
            path = '{0}/preferences'.format(self.self_link)
            response, content = await self._connection.call(path)
            self._preferences = Preferences(self._connection, content)
        return self._preferences
