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
    'ListArchivers'
]


class ListArchivers(RESTDict):
    """
    Represents the activation status for each site-wide available archiver
    for a given list.
    """

    _autosave = True

    def __init__(self, connection, url, mlist):
        """
        :param connection: An API connection object.
        :type connection: Connection.
        :param url: The API url of the list's archiver endpoint.
        :type url: str.
        :param mlist: The corresponding list object.
        :type mlist: MailingList.
        """
        super(ListArchivers, self).__init__(connection, url)
        self._mlist = mlist

    def __repr__(self):
        return '<Archivers on {0!r}>'.format(self._mlist.list_id)

    def __str__(self):
        return 'Archivers on {}'.format(self._mlist.list_id)
