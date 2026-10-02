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

from urllib.parse import quote_plus

from mailmanclient.restobjects.preferences import PreferencesMixin
from mailmanclient.restbase.base import RESTList, RESTObject

__metaclass__ = type
__all__ = [
    'Address',
    'Addresses'
]


class Addresses(RESTList):

    def __init__(self, connection, url, data=None):
        super(Addresses, self).__init__(connection, url, data)
        self._factory = lambda data: Address(
            self._connection, data['self_link'], data)

    def find_by_email(self, email):
        for address in self:
            if address.email == email:
                return address
        return None

    def remove(self, email):
        address = self.find_by_email(email)
        if address is not None:
            address.delete()
            self._reset_cache()
        else:
            raise ValueError('The address {} does not exist'.format(email))


class Address(RESTObject, PreferencesMixin):

    _properties = ('display_name', 'email', 'original_email', 'registered_on',
                   'self_link', 'verified_on')

    def __repr__(self):
        return '<Address {!r}>'.format(self.email)

    def __str__(self):
        return self.email

    @property
    def user(self):
        from mailmanclient.restobjects.user import User
        if 'user' in self.rest_data:
            return User(self._connection, self.rest_data['user'])
        else:
            return None

    @property
    def verified(self):
        return self.verified_on is not None

    def verify(self):
        self._connection.call(
            'addresses/{0}/verify'.format(quote_plus(self.email)),
            method='POST',
            )
        self._reset_cache()

    def unverify(self):
        self._connection.call(
            'addresses/{0}/unverify'.format(quote_plus(self.email)),
            method='POST'
            )
        self._reset_cache()
