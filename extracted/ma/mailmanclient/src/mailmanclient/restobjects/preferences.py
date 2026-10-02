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
from mailmanclient.restbase.base import RESTDict

__metaclass__ = type
__all__ = [
    'Preferences',
    'PreferencesMixin'
]


class Preferences(RESTDict):

    _properties = (
        'acknowledge_posts', 'delivery_mode', 'delivery_status',
        'hide_address', 'preferred_language', 'receive_list_copy',
        'receive_own_postings',
        )

    def delete(self):
        response, content = self._connection.call(self._url, method='DELETE')


class PreferencesMixin:
    """Mixin for restobjects that have preferences."""

    @property
    def preferences(self):
        if getattr(self, '_preferences', None) is None:
            path = '{0}/preferences'.format(self.self_link)
            self._preferences = Preferences(self._connection, path)
        return self._preferences
