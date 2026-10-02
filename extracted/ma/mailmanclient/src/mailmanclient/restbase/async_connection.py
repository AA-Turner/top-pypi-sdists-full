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

"""Async connection object."""

__all__ = [
    'Connection',
]

from urllib.error import HTTPError
from mailmanclient.restbase.connection import Connection as BaseConnection


class Connection(BaseConnection):
    """A standard Connection object.

    This is an abstraction over HTTP connections for Mailmanclient. It can be
    initialized with any http client library with and async `request`
    method. The paramters are currently tailored for httpx, but if there are
    folks interested in others, it is easy to provide a wrapper which accept
    such parameters.

    :param client: The http client object with ``request`` method.
    """

    def __init__(self, client, *args, **kw) -> None:
        self.client = client
        super().__init__(*args, **kw)

    async def call(self, path, data=None, method=None):
        params = self._prepare_request(
            path, data, method
            )
        response = await self.client.request(auth=self.auth, **params)
        if response.status_code // 100 != 2:
            raise HTTPError(params.get('url'), response.status_code,
                            response.content, None, None)
        if len(response.content) == 0:
            return response, None
        return response, response.json()
