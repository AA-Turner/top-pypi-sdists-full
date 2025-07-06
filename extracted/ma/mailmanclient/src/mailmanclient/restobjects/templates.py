# Copyright (C) 2017-2023 by the Free Software Foundation, Inc.
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

"""Template objects."""

from __future__ import absolute_import, print_function, unicode_literals

from mailmanclient.restbase.base import RESTList, RESTObject


__all__ = [
    'Template',
    'TemplateList'
]


class TemplateList(RESTList):

    def __init__(self, connection, url,  data=None, context=None):
        super(RESTList, self).__init__(connection, url, data)
        self._factory = lambda data: Template(
            self._connection, data['self_link'], data)


class Template(RESTObject):
    _properties = ('self_link', 'name', 'uri', 'username', 'password')
    _writable_properties = ['uri', 'username', 'password']

    def __repr__(self):
        return '<Template {}>'.format(self.name)
