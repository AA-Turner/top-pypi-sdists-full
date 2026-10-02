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

"""Async domain object."""

__all__ = [
    'Domain'
]

from mailmanclient.restbase.async_base import RESTObject


class Domain(RESTObject):

    _properties = ('alias_domain', 'description', 'mail_host', 'self_link')

    def __repr__(self) -> str:
        return '<Domain {}>'.format(self.mail_host)
