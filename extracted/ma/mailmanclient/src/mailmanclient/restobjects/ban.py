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

from urllib.error import HTTPError
from urllib.parse import quote_plus

from mailmanclient.restobjects.mailinglist import MailingList
from mailmanclient.restbase.base import RESTList, RESTObject

__metaclass__ = type
__all__ = [
    'Bans',
    'BannedAddress'
]


class Bans(RESTList):
    """
    The list of banned addresses from a mailing-list or from the whole site.
    """

    def __init__(self, connection, url, data=None, mlist=None):
        """
        :param mlist: The corresponding list object, or None if it is a global
            ban list.
        :type mlist: MailingList or None.
        """
        super(Bans, self).__init__(connection, url, data)
        self._mlist = mlist
        self._factory = lambda data: BannedAddress(
            self._connection, data['self_link'], data)

    def __repr__(self):
        if self._mlist is None:
            return '<Global bans>'
        else:
            return '<Bans on {0!r}>'.format(self._mlist.list_id)

    def __contains__(self, item):
        # Accept email addresses and BannedAddress restobjects
        if isinstance(item, BannedAddress):
            item = item.email
        if self._rest_data is not None:
            return item in [data['email'] for data in self._rest_data]
        else:
            # Avoid getting the whole list just to check membership
            try:
                response, content = self._connection.call(
                    '{}/{}'.format(self._url, quote_plus(item)))
            except HTTPError as e:
                if e.code == 404:
                    return False
                else:
                    raise
            else:
                return True

    def add(self, email):
        response, content = self._connection.call(self._url, dict(email=email))
        self._reset_cache()
        return BannedAddress(
            self._connection, response.headers.get('location'))

    def find_by_email(self, email):
        for ban in self:
            if ban.email == email:
                return ban
        return None

    def remove(self, email):
        ban = self.find_by_email(email)
        if ban is not None:
            ban.delete()
            self._reset_cache()
        else:
            raise ValueError('The address {} is not banned'.format(email))


class BannedAddress(RESTObject):

    _properties = ('email', 'list_id', 'self_link')
    _writable_properties = []

    def __repr__(self):
        return '<BannedAddress {!r}>'.format(self.email)

    def __str__(self):
        return self.email

    @property
    def mailinglist(self):
        return MailingList(
            self._connection, 'lists/{0}'.format(self.list_id))
