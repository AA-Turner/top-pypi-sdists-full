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
    'Configuration'
]


class Configuration(RESTDict):

    _writable_properties = ()

    def __init__(self, connection, name):
        super(Configuration, self).__init__(
            connection, 'system/configuration/{}'.format(name))
        self.name = name

    def __repr__(self):
        return '<Configuration: {!r}>'.format(self.name)
