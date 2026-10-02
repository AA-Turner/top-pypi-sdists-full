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

"""Address async object."""

__all__ = [
    'Address',
]


from mailmanclient.restbase.async_base import RESTObject
from mailmanclient.asyncobjects.preferences import PreferencesMixin


class Address(RESTObject, PreferencesMixin):
    _properties = ('display_name', 'email', 'original_email', 'registered_on',
                   'self_link', 'verified_on')

    def __repr__(self) -> str:
        return '<Address {!r}>'.format(self.email)
